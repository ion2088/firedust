from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import field_serializer, field_validator

from firedust.utils import checks

from .base import UNIX_TIMESTAMP, BaseConfig

MEX_MEMORY_CONTENT: int = 4000  # max characters for the context of a memory item


class MemoryItem(BaseConfig):
    """
    A memory used by the AI assistant. Memories are data items that are storred in the assistant's database
    and, when relevant, used as context to answer questions and perform tasks.

    Args:
        assistant (str): Assistant name.ß
        content (str): The content of the memory.
        embedding (Sequence[float]): The embedding of the memory.
        timestamp (UNIX_TIMESTAMP): The time when the memory was created.
        type (Literal["text", "image", "audio", "video"]): The type of the memory. Defaults to "text".
        source (str, optional): The source of the memory. Defaults to None.
        relevance (float, optional): Relevance score, provided by the vector search.
    """

    assistant: str
    content: str
    timestamp: UNIX_TIMESTAMP = datetime.now().timestamp()
    type: Literal["text", "image", "audio", "video"] = "text"
    source: str | None = None
    relevance: float | None = None

    @field_validator("content")
    @classmethod
    def validate_context_length(cls, context: str) -> str | Exception:
        if len(context) > MEX_MEMORY_CONTENT:
            raise ValueError(
                f"Memory content exceeds maximum length of {MEX_MEMORY_CONTENT} characters"
            )
        return context

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(
        cls, timestamp: UNIX_TIMESTAMP
    ) -> UNIX_TIMESTAMP | Exception:
        # Check that the timestamp is UNIX format
        try:
            checks.is_unix_timestamp(timestamp)
        except ValueError as e:
            raise ValueError(f"Invalid timestamp: {e}")
        return timestamp

    @field_serializer("assistant", when_used="always")
    def serialize_collection_id(self, value: UUID) -> str:
        return str(value)
