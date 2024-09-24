from typing import Type

from marshmallow import Schema, fields

from starlette_web.common.conf import settings
from starlette_web.common.http.exceptions import ImproperlyConfigured
from starlette_web.common.utils import import_string


__ERROR_RESPONSE_SCHEMA = None


class ErrorResponseSchema(Schema):
    error = fields.String(required=True, allow_none=False)
    details = fields.Raw(required=False, allow_none=True)


def get_error_schema_class() -> Type[Schema]:
    global __ERROR_RESPONSE_SCHEMA
    if __ERROR_RESPONSE_SCHEMA is not None:
        return __ERROR_RESPONSE_SCHEMA

    try:
        __ERROR_RESPONSE_SCHEMA = import_string(settings.ERROR_RESPONSE_SCHEMA)
    except (SystemError, ImportError, TypeError, ValueError):
        raise ImproperlyConfigured(
            details=(
                "Invalid value settings.ERROR_RESPONSE_SCHEMA "
                f"= {settings.ERROR_RESPONSE_SCHEMA}"
            )
        )

    return __ERROR_RESPONSE_SCHEMA
