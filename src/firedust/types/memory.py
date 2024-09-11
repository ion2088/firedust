from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import Field, field_serializer, field_validator

from firedust.utils import checks

from .base import UNIX_TIMESTAMP, BaseConfig

MAX_MEMORY_CONTENT: int = 4000  # max characters for the context of a memory item


class MemoryItem(BaseConfig):
    """
    A memory used by the AI assistant. Memories are data items that are stored in the assistant's database
    and, when relevant, used as context to answer questions and perform tasks.

    Args:
        assistant (str): Assistant name.
        content (str): The content of the memory.
        embedding (Sequence[float]): The embedding of the memory.
        timestamp (UNIX_TIMESTAMP): The time when the memory was created.
        type (Literal["text", "image", "audio", "video"]): The type of the memory. Defaults to "text".
        source (str, optional): The source of the memory. Defaults to None.
        relevance (float, optional): Relevance score, provided by the vector search.
    """

    assistant: str = Field(...)
    content: str = Field(..., max_length=MAX_MEMORY_CONTENT)
    timestamp: UNIX_TIMESTAMP = Field(
        default_factory=lambda: datetime.now().timestamp()
    )
    type: Literal["text", "image", "audio", "video"] = Field(default="text")
    source: Optional[str] = Field(default=None)
    relevance: Optional[float] = Field(default=None)

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, timestamp: UNIX_TIMESTAMP) -> UNIX_TIMESTAMP:
        # Check that the timestamp is UNIX format
        try:
            checks.is_unix_timestamp(timestamp)
        except ValueError as e:
            raise ValueError(f"Invalid timestamp: {e}")
        return timestamp

    @field_serializer("assistant", when_used="always")
    def serialize_collection_id(self, value: UUID) -> str:
        return str(value)
