from datetime import datetime
from typing import Literal, Sequence
from uuid import UUID

from pydantic import BaseModel, field_serializer

from .base import UNIX_TIMESTAMP, BaseConfig


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

    assistant: str
    user: str
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    message: str
    author: Literal["user", "assistant"]


class UserMessage(Message):
    author: Literal["user"] = "user"


class AssistantMessage(Message):
    author: Literal["assistant"] = "assistant"


class MessageReferences(BaseModel):
    """
    References to the memories and messages used by the assistant as context to generate a response.

    Args:
        memories (Sequence[UUID]): The references to the relevant memories.
        conversations (Sequence[UUID]): The references to the relevant conversations.
    """

    memories: Sequence[UUID]
    conversations: Sequence[UUID]

    @field_serializer("memories", when_used="always")
    def serialize_memory_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]

    @field_serializer("conversations", when_used="always")
    def serialize_conversation_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]


class ReferencedMessage(Message, frozen=True):
    references: MessageReferences | None = None


class MessageStreamEvent(ReferencedMessage, frozen=True):
    stream_ended: bool
