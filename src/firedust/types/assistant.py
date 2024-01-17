from uuid import UUID, uuid4
from pydantic import BaseModel, validator
from typing import List, Literal


class LLM(BaseModel):
    provider: Literal["oai", "mistral", "sand"]
    model: str


class Memory(BaseModel):
    id: UUID = uuid4()
    title: str
    context: str
    embedding: List[float] | None = None

    @validator("context")
    def validate_context_length(cls, context: str) -> str | Exception:
        words = context.split()
        if len(words) > 512:
            raise ValueError("Memory context exceeds maximum length of 512 words")
        return context


class Memories(BaseModel):
    id: UUID = uuid4()
    collection: List[UUID] | None = None


class Ability(BaseModel):
    id: UUID = uuid4()
    name: str
    description: str
    instructions: List[str]
    endpoint: str


class AssistantConfig(BaseModel):
    id: UUID = uuid4()
    name: str = "Adam"
    instructions: List[str] = ["You are a helpful assistant."]
    llm: LLM = LLM(provider="oai", model="gpt4")
    memories: Memories | None = None
    abilities: List[Ability] | None = None
