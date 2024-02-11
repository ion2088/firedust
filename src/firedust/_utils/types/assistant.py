from typing import Any, List, Literal
from uuid import UUID

from pydantic import BaseModel, field_serializer

from ._base import UNIX_TIMESTAMP, BaseConfig
from .ability import AbilityConfig
from .inference import InferenceConfig
from .interface import Interfaces
from .memory import MemoryConfig


class AssistantConfig(BaseConfig):
    """
    Represents the configuration of an AI Assistant.

    Args:
        name (str): The name of the assistant.
        instructions (List[str]): The instructions of the assistant.
        inference (InferenceConfig): The inference configuration of the assistant.
        memory (MemoryConfig): The memory configuration of the assistant.
        abilities (List[Ability], optional): The abilities of the assistant. Defaults to None.
        deployments (List[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: List[str]
    inference: InferenceConfig
    memory: MemoryConfig
    abilities: List[AbilityConfig] = []
    interfaces: Interfaces = Interfaces()

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "memory":
            raise AttributeError(
                """
                Cannot set attribute 'memory', it is immutable.
                To use a different memory configuration, create a new Assistant.
            """
            )

        return super().__setattr__(key, value)


class Message(BaseModel):
    """
    Represents a message between the user and the assistant.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (UUID, optional): The unique identifier of the user. Defaults to None.
        author (Literal["user", "assistant"]): The author of the message.
        text (str): The text of the message.
        timestamp (UNIX_TIMESTAMP, optional): The timestamp of the message. Defaults to None.
    """

    assistant_id: UUID
    user_id: UUID | None = None
    author: Literal["user", "assistant"]
    text: str
    timestamp: UNIX_TIMESTAMP

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("user_id", when_used="always")
    def serialize_user_id(self, value: UUID | None) -> str | None:
        if value is None:
            return None
        return str(value)
