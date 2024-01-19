from typing import List
from pydantic import BaseModel, validator
from uuid import UUID, uuid4

MEMORY_ID = UUID
MEMORIES_COLLECTION_ID = UUID


class Memory(BaseModel):
    """
    A memory used by the assistant. The assistant recalls the title and
    the context to answer questions and perform tasks.
    """

    id: MEMORY_ID = uuid4()
    title: str
    context: str
    embedding: List[float] | None = None

    @validator("context")
    def validate_context_length(cls, context: str) -> str | Exception:
        if len(context) > 2000:
            raise ValueError("Memory context exceeds maximum length of 2000 characters")
        return context

    @validator("title")
    def validate_title_length(cls, title: str) -> str | Exception:
        if len(title) > 140:
            raise ValueError("Title exceeds maximum length of 140 characters")
        return title


class MemoriesCollection(BaseModel):
    """
    Represents a collection of memories used by the assistant.
    """

    id: MEMORIES_COLLECTION_ID = uuid4()
    collection: List[MEMORY_ID] | None = None


class QdrantCloudConfig(BaseModel):
    """
    A configuration for a Qdrant Cloud instance.
    """

    host: str
    api_key: str


class MemoryConfig(BaseModel):
    """
    Configuration for Assistant's memory.
    """

    vectordb: QdrantCloudConfig | None = None
    default_collection: MEMORIES_COLLECTION_ID | None = None
    extra_collections: List[MEMORIES_COLLECTION_ID] | None = None
