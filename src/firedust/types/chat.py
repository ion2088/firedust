from datetime import datetime
from typing import Literal, Optional, Sequence, Union
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from .base import UNIX_TIMESTAMP, BaseConfig
from .structured import STRUCTURED_RESPONSE, STRUCTURED_SCHEMA


class Message(BaseConfig, frozen=True):
    """
    Represents a message between a user and an assistant.

    Args:
        assistant (str): The name of the assistant.
        user (str): The unique identifier of the user.
        timestamp (UNIX_TIMESTAMP): The timestamp of the message.
        message (str): The text of the message.
        author (Literal["user", "assistant"]): The author of the message.
    """

    assistant: str = Field(...)
    user: str = Field(...)
    timestamp: UNIX_TIMESTAMP = Field(
        default_factory=lambda: datetime.now().timestamp()
    )
    message: str = Field(...)
    author: Literal["user", "assistant"] = Field(...)


class UserMessage(Message):
    author: Literal["user"] = Field(default="user")


class StructuredUserMessage(UserMessage):
    schema_: STRUCTURED_SCHEMA = Field(...)


class AssistantMessage(Message):
    author: Literal["assistant"] = Field(default="assistant")


class MessageReferences(BaseModel):
    """
    References to the memories and messages used by the assistant as context to generate a response.

    Args:
        memories (Sequence[UUID]): The references to the relevant memories.
        conversations (Sequence[UUID]): The references to the relevant conversations.
    """

    memories: Sequence[UUID] = Field(...)
    conversations: Sequence[UUID] = Field(...)

    @field_serializer("memories", when_used="always")
    def serialize_memory_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]

    @field_serializer("conversations", when_used="always")
    def serialize_conversation_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]


class StructuredAssistantMessage(BaseConfig, frozen=True):
    assistant: str = Field(...)
    user: str = Field(...)
    timestamp: UNIX_TIMESTAMP = Field(...)
    message: STRUCTURED_RESPONSE = Field(...)
    author: Literal["assistant"] = Field(default="assistant")
    references: Union[MessageReferences, None] = Field(default=None)


class ReferencedMessage(Message, frozen=True):
    references: Optional[MessageReferences] = Field(default=None)


class MessageStreamEvent(ReferencedMessage, frozen=True):
    stream_ended: bool = Field(...)
