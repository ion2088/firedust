from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_serializer

UNIX_TIMESTAMP = float  # see: https://www.unixtimestamp.com/
STREAM_STOP_EVENT = "[[STOP]]"
TOKENS = int
INFERENCE_MODEL = Literal[
    "mistral/mistral-medium",
    "mistral/mistral-small",
    "mistral/mistral-tiny",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "openai/o3-mini",
    "openai/o3",
    "openai/o4-mini",
    "openai/gpt-4.1",
    "groq/llama-3.3-70b-versatile",
    "groq/llama-3.1-8b-instant",
    "groq/deepseek-r1-distill-llama-70b",
]


class BaseConfig(BaseModel):
    """
    Represents the base configuration model.
    All configuration models should inherit from this class.
    """

    id: UUID = Field(default_factory=uuid4)

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "id":
            raise AttributeError("Cannot set attribute 'id', it is immutable.")

        return super().__setattr__(key, value)

    @field_serializer("id", when_used="always")
    def serialize_config_id(self, value: UUID) -> str:
        return str(value)
