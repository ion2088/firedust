from typing import List
from pydantic import BaseModel, validator
from uuid import UUID, uuid4


class Memory(BaseModel):
    """
    A memory used by the assistant. The assistant recalls the title and
    the context to answer questions and perform tasks.
    """

    id: UUID = uuid4()
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


class Memories(BaseModel):
    """
    Represents a collection of memories used by the assistant.
    """

    id: UUID = uuid4()
    collection: List[UUID] | None = None
