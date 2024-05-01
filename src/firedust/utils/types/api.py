from typing import Any, List, Literal
from uuid import UUID

from pydantic import BaseModel, field_serializer

from ._base import UNIX_TIMESTAMP


class APIContent(BaseModel):
    """
    Represents the API content model.
    """

    status: Literal["success", "error"]
    timestamp: UNIX_TIMESTAMP
    data: Any = {}
    message: str | None


class MessageStreamEvent(BaseModel, frozen=True):
    """
    Represents a message stream event model.
    """

    assistant_id: UUID
    user_id: str
    timestamp: UNIX_TIMESTAMP
    message: str
    stream_ended: bool
    memory_refs: List[UUID] = []
    conversation_refs: List[UUID] = []

    @field_serializer("assistant_id", when_used="always")
    def serialize_assistant_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("memory_refs", when_used="always")
    def serialize_memory_refs(self, value: List[UUID]) -> List[str]:
        return [str(x) for x in value]

    @field_serializer("conversation_refs", when_used="always")
    def serialize_conversation_refs(self, value: List[UUID]) -> List[str]:
        return [str(x) for x in value]
