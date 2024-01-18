from uuid import UUID, uuid4
from pydantic import BaseModel, validator
from typing import List, Literal


class LLM(BaseModel):
    """
    Language Model used by the assistant for inference.
    """

    model: Literal["openai/gpt4", "mistral/medium"]


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


class Ability(BaseModel):
    """
    Represents an ability of the assistant.
    """

    id: UUID = uuid4()
    name: str
    description: str
    instructions: List[str]
    endpoint: str


class AssistantConfig(BaseModel):
    """
    Represents the configuration of an AI Assistant.
    """

    id: UUID = uuid4()
    name: str = "Adam"
    instructions: List[str] = ["You are a helpful assistant."]
    llm: LLM = LLM(model="openai/gpt4")
    memories: Memories | None = None
    abilities: List[Ability] | None = None

    @validator("name")
    def validate_name_length(cls, name: str) -> str | Exception:
        if len(name) > 50:
            raise ValueError("Name exceeds maximum length of 140 characters")
        return name

    @validator("instructions")
    def validate_instructions_length(
        cls, instructions: List[str]
    ) -> List[str] | Exception:
        for instruction in instructions:
            if len(instruction) > 500:
                raise ValueError("Instruction exceeds maximum length of 500 characters")
        return instructions

    @validator("llm")
    def check_llm_credentials(cls, llm: LLM) -> LLM | Exception:
        # TODO: Add check
        return llm

    @validator("memories")
    def check_memories(cls, memories: Memories) -> Memories | Exception | None:
        # TODO: Add vectordb check
        return memories
