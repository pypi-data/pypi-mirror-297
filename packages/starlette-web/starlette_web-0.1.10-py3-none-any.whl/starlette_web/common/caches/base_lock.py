import exceptiongroup
import math
import sys
from typing import Optional

import anyio
from anyio._core._tasks import TaskGroup

from starlette_web.common.caches.base import CacheLockError
from starlette_web.common.http.exceptions import NotSupportedError


class BaseLock:
    EXIT_MAX_DELAY = 60.0

    def __init__(
        self,
        name: str,
        timeout: Optional[float] = None,
        blocking_timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        self._name = name
        if timeout is None:
            timeout = math.inf
        self._timeout = timeout
        if self._timeout is not None and self._timeout < 0:
            raise RuntimeError("timeout cannot be negative")

        self._blocking_timeout = blocking_timeout
        if self._blocking_timeout is not None and self._blocking_timeout < 0:
            raise RuntimeError("blocking_timeout cannot be negative")

        self._task_group: Optional[TaskGroup] = None
        self._acquire_event: Optional[anyio.Event] = None
        self._is_acquired = False

    async def __aenter__(self):
        self._task_group = anyio.create_task_group()
        await self._task_group.__aenter__()
        self._acquire_event = anyio.Event()
        if self._blocking_timeout is not None:
            self._task_group.cancel_scope.deadline = anyio.current_time() + self._blocking_timeout
        self._task_group.start_soon(self._acquire)

        try:
            await self._acquire_event.wait()
            self._is_acquired = self._acquire_event.is_set()
        except BaseException as exc:
            await self._task_group.__aexit__(*sys.exc_info())
            self._is_acquired = False

            # https://anyio.readthedocs.io/en/stable/cancellation.html#finalization
            if type(exc) is anyio.get_cancelled_exc_class():
                raise exc

            raise CacheLockError(details=str(exc)) from exc

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, exceptiongroup.BaseExceptionGroup):
            if len(exc_val.exceptions) == 1:
                exc_tb = exc_val.__traceback__
                exc_type = type(exc_val.exceptions[0])
                exc_val = exc_val.exceptions[0]

        try:
            with anyio.move_on_after(self.EXIT_MAX_DELAY, shield=True):
                await self._release()

        finally:
            if exc_type == anyio.get_cancelled_exc_class():
                retval = await self._task_group.__aexit__(exc_type, exc_val, exc_tb)
            else:
                # Avoid re-raising exception as BaseExceptionGroup
                retval = await self._task_group.__aexit__(None, None, None)

        try:
            if exc_type is not None and exc_type not in [
                CacheLockError,
                anyio.get_cancelled_exc_class(),
            ]:
                # The lock itself is supposed to always raise CacheLockError on any inner error.
                # Furthermore, lock may be cancelled from outside with CancelledError.
                # Any other error is propagated.
                retval = False

            elif self._task_group.cancel_scope.cancel_called:
                raise CacheLockError(
                    message=f"Could not acquire FileLock within {self._timeout} seconds.",
                    details=str(sys.exc_info()[1]),
                ) from exc_val
        finally:
            self._acquire_event = None
            self._task_group = None

        return retval

    async def _acquire(self):
        raise NotSupportedError(details=f"{self.__class__.__name__} does not support _acquire")

    async def _release(self):
        raise NotSupportedError(details=f"{self.__class__.__name__} does not support _release")
