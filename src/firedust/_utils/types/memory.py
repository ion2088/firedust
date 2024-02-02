from typing import List, Literal, Any
from pydantic import BaseModel, field_validator
from uuid import UUID, uuid4

from ._base import BaseConfig

MEMORY_ID = UUID
MEMORY_COLLECTION_ID = UUID


class MemoryItem(BaseConfig):
    """
    A memory used by the assistant. The assistant recalls the title and
    the context to answer questions and perform tasks.
    """

    id: MEMORY_ID = uuid4()
    title: str
    context: str
    tags: List[str] | None = None
    embedding: List[float] | None = None

    @field_validator("context")
    def validate_context_length(cls, context: str) -> str | Exception:
        if len(context) > 2000:
            raise ValueError("Memory context exceeds maximum length of 2000 characters")
        return context

    @field_validator("title")
    def validate_title_length(cls, title: str) -> str | Exception:
        if len(title) > 140:
            raise ValueError("Title exceeds maximum length of 140 characters")
        return title


class MemoriesCollectionItem(BaseConfig):
    """
    Represents a collection of memories used by the assistant.
    """

    id: MEMORY_COLLECTION_ID = uuid4()
    collection: List[MEMORY_ID] | None = None


class MemoryConfig(BaseModel):
    """
    Configuration for Assistant's memory.
    """

    embedding_model: Literal[
        "sand/MiniLM-L6-v2", "sand/UAE-Large-v1"
    ] = "sand/MiniLM-L6-v2"
    default_collection: MEMORY_COLLECTION_ID = uuid4()
    extra_collections: List[MEMORY_COLLECTION_ID] = []

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
