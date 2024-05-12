from datetime import datetime
from typing import List, Literal, Sequence
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator

from ._base import UNIX_TIMESTAMP, BaseConfig
from .ability import AbilityConfig
from .inference import InferenceConfig
from .interface import Interfaces

ASSISTANT_ID = UUID


class AssistantConfig(BaseConfig, frozen=True):
    """
    Represents the configuration of an AI Assistant.

    Args:
        name (str): The name of the assistant.
        instructions (str): The instructions of the assistant.
        inference (InferenceConfig): The inference configuration of the assistant.
        shared_memories (List[ASSISTANT_ID], optional): A list of assistant IDs whose memories are accessible by the current assistant. Defaults to [].
        abilities (Sequence[Ability], optional): The abilities of the assistant. Defaults to None.
        interfaces (Sequence[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: str
    inference: InferenceConfig = InferenceConfig()
    shared_memories: List[ASSISTANT_ID] = []
    abilities: Sequence[AbilityConfig] = []
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

    @field_serializer("shared_memories", when_used="always")
    def serialize_shared_memories(self, value: List[ASSISTANT_ID]) -> List[str]:
        return [str(ref) for ref in value]


class Message(BaseConfig, frozen=True):
    """
    Represents a message between the user and the assistant.

    Args:
        assistant_id (UUID): The unique identifier of the assistant.
        user_id (str): The unique identifier of the user.
        timestamp (UNIX_TIMESTAMP): The timestamp of the message.
        message (str): The text of the message.
        author (Literal["user", "assistant"]): The author of the message.
    """

    assistant_id: UUID
    user_id: str
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    message: str
    author: Literal["user", "assistant"]

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)


class UserMessage(Message):
    author: Literal["user"] = "user"


class AssistantMessage(Message):
    author: Literal["assistant"] = "assistant"


class AssistantMessageReferences(BaseModel, frozen=True):
    """
    References to the memories and messages used by the assistant to generate a response.

    Args:
        message_id (UUID): The unique identifier of the assistant message.
        memory_refs (Sequence[UUID]): The references to the relevant memories.
        conversation_refs (Sequence[UUID]): The references to the relevant conversations.
    """

    message_id: UUID
    memories: Sequence[UUID]
    messages: Sequence[UUID]

    @field_serializer("message_id", when_used="always")
    def serialize_message_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("memories", when_used="always")
    def serialize_memory_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]

    @field_serializer("messages", when_used="always")
    def serialize_conversation_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]


class Context(AssistantMessageReferences):
    """
    Represents the context used to provide an AI assistant with useful data to answer a query.

    Args:
        instructions (str): The instructions for the assistant.
    """

    instructions: str
