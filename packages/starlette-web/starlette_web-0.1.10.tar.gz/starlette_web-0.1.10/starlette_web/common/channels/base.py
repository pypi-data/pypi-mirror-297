from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator, Optional, Any, Dict, Set

import anyio
from anyio._core._tasks import TaskGroup
from anyio.streams.memory import (
    MemoryObjectReceiveStream,
    MemoryObjectSendStream,
    EndOfStream,
    ClosedResourceError,
    BrokenResourceError,
)

from starlette_web.common.channels.layers.base import BaseChannelLayer
from starlette_web.common.channels.event import Event
from starlette_web.common.channels.exceptions import ListenerClosed


class Channel:
    EXIT_MAX_DELAY = 60

    def __init__(self, channel_layer: BaseChannelLayer):
        self._task_group: Optional[TaskGroup] = None
        self._channel_layer = channel_layer
        self._subscribers: Dict[str, Set[MemoryObjectSendStream]] = dict()
        self._manager_lock = anyio.Lock()

    async def __aenter__(self) -> "Channel":
        await self.connect()
        self._task_group = anyio.create_task_group()
        await self._task_group.__aenter__()
        self._task_group.start_soon(self._listener)
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any):
        try:
            self._task_group.cancel_scope.cancel()
            retval = await self._task_group.__aexit__(*args)
        finally:
            del self._task_group
            self._subscribers.clear()
            with anyio.fail_after(self.EXIT_MAX_DELAY, shield=True):
                await self.disconnect()

        return retval

    async def connect(self) -> None:
        await self._channel_layer.connect()

    async def disconnect(self) -> None:
        await self._channel_layer.disconnect()

    async def _listener(self) -> None:
        async def _safe_send(_send_stream: MemoryObjectSendStream, _event: Event):
            try:
                await _send_stream.send(_event)
            except (BrokenResourceError, ClosedResourceError):
                pass

        async with anyio.create_task_group() as task_group:
            while True:
                try:
                    event = await self._channel_layer.next_published()
                except ListenerClosed:
                    break

                async with self._manager_lock:
                    subscribers_list = list(self._subscribers.get(event.group, []))

                for send_stream in subscribers_list:
                    task_group.start_soon(_safe_send, send_stream, event)

        async with self._manager_lock:
            for group in self._subscribers.keys():
                for recv_channel in self._subscribers[group]:
                    recv_channel.close()

    async def publish(self, group: str, message: Any, **kwargs) -> None:
        await self._channel_layer.publish(group, message, **kwargs)

    @asynccontextmanager
    async def subscribe(
        self,
        group: str,
        max_buffer_size: float = 0,
        **kwargs,
    ) -> AsyncGenerator["Subscriber", None]:
        send_stream, receive_stream = anyio.create_memory_object_stream(max_buffer_size)

        try:
            async with self._manager_lock:
                if not self._subscribers.get(group):
                    await self._channel_layer.subscribe(group, **kwargs)
                    self._subscribers[group] = {
                        send_stream,
                    }
                else:
                    self._subscribers[group].add(send_stream)

            yield Subscriber(receive_stream)

        finally:
            try:
                with anyio.fail_after(self.EXIT_MAX_DELAY, shield=True):
                    async with self._manager_lock:
                        self._subscribers[group].remove(send_stream)
                        if not self._subscribers.get(group):
                            del self._subscribers[group]
                            await self._channel_layer.unsubscribe(group, **kwargs)

            finally:
                send_stream.close()


class Subscriber:
    def __init__(self, receive_stream: MemoryObjectReceiveStream) -> None:
        self._receive_stream = receive_stream

    async def __aiter__(self) -> AsyncIterator[Event]:
        async with self._receive_stream:
            try:
                while True:
                    event: Event = await self._receive_stream.receive()
                    yield event
            except (EndOfStream, ClosedResourceError):
                pass
