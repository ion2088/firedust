from datetime import datetime
from typing import List
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
        instructions (str): The instructions of the assistant.
        inference (InferenceConfig): The inference configuration of the assistant.
        memory (MemoryConfig): The memory configuration of the assistant.
        abilities (List[Ability], optional): The abilities of the assistant. Defaults to None.
        interfaces (List[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: str
    inference: InferenceConfig
    memory: MemoryConfig
    abilities: List[AbilityConfig] = []
    interfaces: Interfaces = Interfaces()


class UserMessage(BaseConfig, frozen=True):
    """
    Represents a message from the user to the assistant.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (UUID, optional): The unique identifier of the user.
        message (str): The text of the message.
        timestamp (UNIX_TIMESTAMP): The timestamp of the message.
    """

    assistant_id: UUID
    user_id: UUID | None = None
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    message: str

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("user_id", when_used="always")
    def serialize_user_id(self, value: UUID | None) -> str | None:
        if value is None:
            return None
        return str(value)


class AssistantMessage(BaseConfig, frozen=True):
    """
    Represents a message from the assistant to the user.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (UUID): The unique identifier of the user.
        response_to_id (UUID): The unique identifier of the message to which the assistant is responding.
        message (str): The text of the message.
        timestamp (UNIX_TIMESTAMP): The time when the message was sent.
        context (str): The context of the message.
        memory_refs (List[UUID], optional): The memory references of the message. Defaults to None.
        conversation_refs (List[UUID], optional): The conversation references of the message. Defaults to None.
    """

    assistant_id: UUID
    user_id: UUID | None = None
    response_to_id: UUID
    timestamp: UNIX_TIMESTAMP
    message: str
    context: "Context"

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("user_id", when_used="always")
    def serialize_user_id(self, value: UUID | None) -> str | None:
        if value is None:
            return None
        return str(value)

    @field_serializer("response_to_id", when_used="always")
    def serialize_response_to_id(self, value: UUID) -> str:
        return str(value)


class Context(BaseModel):
    instructions: str
    memory_refs: List[UUID]
    conversation_refs: List[UUID]

    @field_serializer("memory_refs", when_used="always")
    def serialize_memory_refs(self, value: List[UUID]) -> List[str]:
        return [str(ref) for ref in value]

    @field_serializer("conversation_refs", when_used="always")
    def serialize_conversation_refs(self, value: List[UUID]) -> List[str]:
        return [str(ref) for ref in value]
