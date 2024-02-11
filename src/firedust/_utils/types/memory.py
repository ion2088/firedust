from typing import Any, Dict, List, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_serializer, field_validator

from firedust._utils import checks

from ._base import UNIX_TIMESTAMP, BaseConfig

EMBEDDING_MODELS = Literal["mistral-embed"]
EMBEDDING_PROVIDERS = Literal["mistral"]

EMBEDDING_MODELS_MAP: Dict[EMBEDDING_PROVIDERS, List[EMBEDDING_MODELS]] = {
    "mistral": ["mistral-embed"],
}


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
    @classmethod
    def validate_context_length(cls, context: str) -> str | Exception:
        if len(context) > 2000:
            raise ValueError("Memory context exceeds maximum length of 2000 characters")
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

    @field_serializer("collection", when_used="always")
    def serialize_id(self, value: UUID) -> str:
        return str(value)


class MemoriesCollection(BaseConfig):
    """
    Represents a collection of memories used by the assistant.
    """

    collection_id: UUID
    memory_ids: List[UUID] | None = None

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "collection_id":
            raise AttributeError(
                """
                Cannot set attribute 'collection_id', it is immutable.
                To add a memory to the collection use assistant.memory.collection.add method.
                """
            )

        return super().__setattr__(key, value)

    @field_serializer("collection_id", when_used="always")
    def serialize_collection_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("memory_ids", when_used="always")
    def serialize_memory_ids(self, value: List[UUID] | None) -> List[str] | None:
        if value is None:
            return None
        return [str(memory_id) for memory_id in value]


class MemoryConfig(BaseModel):
    """
    Configuration for Assistant's memory.
    """

    default_collection: UUID = Field(default_factory=uuid4)
    embedding_model: EMBEDDING_MODELS = "mistral-embed"
    embedding_model_provider: EMBEDDING_PROVIDERS = "mistral"
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

    @field_serializer("default_collection", when_used="always")
    def serialize_default_collection(self, value: UUID) -> str:
        return str(value)

    @field_serializer("extra_collections", when_used="always")
    def serialize_extra_collections(self, value: List[UUID]) -> List[str]:
        return [str(collection) for collection in value]
