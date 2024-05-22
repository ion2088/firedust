from datetime import datetime
from typing import List, Literal, Sequence
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator

from .base import INFERENCE_MODEL, UNIX_TIMESTAMP, BaseConfig
from .interface import Interfaces

_assistant_name = str


class AssistantConfig(BaseModel, frozen=True):
    """
    Represents the configuration of an AI Assistant.

    Args:
        name (str): The name of the assistant.
        instructions (str): The instructions of the assistant.
        model (INFERENCE_MODEL, optional): The inference model of the assistant. Defaults to "openai/gpt-4".
        attached_memories (List[_assistant_name], optional): Attached memories from other assistants. Defaults to [].
        abilities (Sequence[Ability], optional): The abilities of the assistant. Defaults to None.
        interfaces (Sequence[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: str
    model: INFERENCE_MODEL = "openai/gpt-4"
    attached_memories: List[_assistant_name] = []
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


class Message(BaseConfig, frozen=True):
    """
    Represents a message between the user and the assistant.

    Args:
        assistant (str): The name of the assistant.
        user (str): The unique identifier of the user.
        timestamp (UNIX_TIMESTAMP): The timestamp of the message.
        message (str): The text of the message.
        author (Literal["user", "assistant"]): The author of the message.
    """

    assistant: str
    user: str
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    message: str
    author: Literal["user", "assistant"]


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
