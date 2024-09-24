from uuid import UUID

from orjson import dumps
from pydantic import BaseModel


def value_serializer(value: UUID | BaseModel) -> bytes:
    if isinstance(value, BaseModel):
        value = value.model_dump()

    return dumps(value)
