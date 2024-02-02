from pydantic import BaseModel
from typing import Any
from uuid import UUID


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
