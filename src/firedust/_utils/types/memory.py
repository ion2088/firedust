from typing import Any, List, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, field_validator

from firedust._utils import checks

from ._base import UNIX_TIMESTAMP, BaseConfig


class MemoryItem(BaseConfig):
    """
    A memory used by the AI assistant. The assistant recalls memories and their
    context to answer questions and perform tasks.

    Args:
        collection (UUID): The collection that contains the memory.
        context (str): The context of the memory.
        embedding (List[float]): The embedding of the memory.
        timestamp (UNIX_TIMESTAMP): The time when the memory was created.
        type (Literal["text", "image", "audio", "video"]): The type of the memory. Defaults to "text".
        source (str, optional): The source of the memory. Defaults to None.
    """

    collection: UUID
    context: str
    embedding: List[float]
    timestamp: UNIX_TIMESTAMP
    type: Literal["text", "image", "audio", "video"] = "text"
    source: str | None = None

    @field_validator("context")
    def validate_context_length(cls, context: str) -> str | Exception:
        if len(context) > 2000:
            raise ValueError("Memory context exceeds maximum length of 2000 characters")
        return context

    @field_validator("timestamp")
    def validate_timestamp(
        cls, timestamp: UNIX_TIMESTAMP
    ) -> UNIX_TIMESTAMP | Exception:
        # Check that the timestamp is UNIX format
        try:
            checks.is_unix_timestamp(timestamp)
        except ValueError as e:
            raise ValueError(f"Invalid timestamp: {e}")
        return timestamp


class MemoriesCollectionItem(BaseConfig):
    """
    Represents a collection of memories used by the assistant.
    """

    collection: List[UUID] | None = None


class MemoryConfig(BaseModel):
    """
    Configuration for Assistant's memory.
    """

    embedding_model: Literal[
        "sand/MiniLM-L6-v2", "sand/UAE-Large-v1"
    ] = "sand/MiniLM-L6-v2"
    default_collection: UUID = uuid4()
    extra_collections: List[UUID] = []

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "embedding_model":
            raise AttributeError(
                """
                Cannot set attribute 'embedding_model', it is immutable.
                To use a different embedding model, create a new Assistant.
                """
            )
        if key == "default_collection":
            raise AttributeError(
                """
                Cannot set attribute 'default_collection', it is immutable.
                To add an extra memory collection use assistant.memory.collection.add method.
                """
            )

        return super().__setattr__(key, value)
