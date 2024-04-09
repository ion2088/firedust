from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import field_serializer, field_validator

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

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str | Exception:
        if len(name) > 50:
            raise ValueError("Assistant name exceeds maximum length of 50 characters")
        if len(name) < 1:
            raise ValueError("Assistant name must be at least 1 character")
        return name

    @field_validator("instructions")
    @classmethod
    def validate_instructions(cls, instructions: str) -> str | Exception:
        if len(instructions) < 20:
            raise ValueError("Assistant instructions must be at least 20 characters")
        return instructions


class UserMessage(BaseConfig, frozen=True):
    """
    Represents a message from the user to the assistant.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (str, optional): The unique identifier of the user.
        message (str): The text of the message.
        timestamp (UNIX_TIMESTAMP): The timestamp of the message.
    """

    assistant_id: UUID
    user_id: str | None = None
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    message: str

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)


class AssistantMessage(BaseConfig, frozen=True):
    """
    Represents a message from the assistant to the user.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (str, optional): The unique identifier of the user.
        response_to_id (UUID): The unique identifier of the message to which the assistant is responding.
        message (str): The text of the message.
        timestamp (UNIX_TIMESTAMP): The time when the message was sent.
        memory_refs (List[UUID], optional): The unique identifiers of the memories referenced by the message. Defaults to [].
        conversation_refs (List[UUID], optional): The unique identifiers of the conversations referenced by the message. Defaults to [].
    """

    assistant_id: UUID
    user_id: str | None = None
    response_to_id: UUID
    timestamp: UNIX_TIMESTAMP
    message: str
    memory_refs: List[UUID] = []
    conversation_refs: List[UUID] = []

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("response_to_id", when_used="always")
    def serialize_response_to_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("memory_refs", when_used="always")
    def serialize_memory_refs(self, value: List[UUID]) -> List[str]:
        return [str(x) for x in value]

    @field_serializer("conversation_refs", when_used="always")
    def serialize_conversation_refs(self, value: List[UUID]) -> List[str]:
        return [str(x) for x in value]
