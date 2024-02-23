from typing import Any, List, Literal
from uuid import UUID

from pydantic import BaseModel, field_serializer

from ._base import UNIX_TIMESTAMP, BaseConfig
from .ability import AbilityConfig
from .inference import InferenceConfig
from .interface import Interfaces
from .memory import MemoryConfig


class AssistantConfig(BaseConfig, frozen=True):
    """
    Represents the configuration of an AI Assistant.

    Args:
        name (str): The name of the assistant.
        instructions (List[str]): The instructions of the assistant.
        inference (InferenceConfig): The inference configuration of the assistant.
        memory (MemoryConfig): The memory configuration of the assistant.
        abilities (List[Ability], optional): The abilities of the assistant. Defaults to None.
        interfaces (List[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: List[str]
    inference: InferenceConfig
    memory: MemoryConfig
    abilities: List[AbilityConfig] = []
    interfaces: Interfaces = Interfaces()


class Message(BaseModel, frozen=True):
    """
    Represents a message between the user and the assistant.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        timestamp (UNIX_TIMESTAMP, optional): The timestamp of the message. Defaults to None.
        user_id (UUID, optional): The unique identifier of the user. Defaults to None.
        author (Literal["user", "assistant"]): The author of the message.
        text (str): The text of the message.
        memory_references (List[UUID], optional): The references to memories. Defaults to None.
        conversation_references (List[UUID], optional): The references to conversations. Defaults to None.
    """

    assistant_id: UUID
    timestamp: UNIX_TIMESTAMP
    user_id: UUID | None = None
    author: Literal["user", "assistant"]
    text: str
    memory_references: List[UUID] | None = None
    conversation_references: List[UUID] | None = None

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("user_id", when_used="always")
    def serialize_user_id(self, value: UUID | None) -> str | None:
        if value is None:
            return None
        return str(value)

    @field_serializer("memory_references", when_used="always")
    def serialize_memory_references(self, value: List[UUID] | None) -> List[str] | None:
        if value is None:
            return None
        return [str(ref) for ref in value]

    @field_serializer("conversation_references", when_used="always")
    def serialize_conversation_references(
        self, value: List[UUID] | None
    ) -> List[str] | None:
        if value is None:
            return None
        return [str(ref) for ref in value]
