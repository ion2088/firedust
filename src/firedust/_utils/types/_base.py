from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_serializer

UNIX_TIMESTAMP = float  # see: https://www.unixtimestamp.com/


class BaseConfig(BaseModel):
    """
    Represents the base configuration model.
    All configuration models should inherit from this class.
    """

    id: UUID

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "id":
            raise AttributeError("Cannot set attribute 'id', it is immutable.")

        return super().__setattr__(key, value)

    @field_serializer("id", when_used="always")
    def serialize_id(self, value: UUID) -> str:
        return str(value)
