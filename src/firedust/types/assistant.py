from uuid import UUID, uuid4
from pydantic import BaseModel, validator
from typing import List
from .inference import Inference
from .memory import Memories
from .ability import Ability
from .interface import Interface


class AssistantConfig(BaseModel):
    """
    Represents the configuration of an AI Assistant.
    """

    id: UUID = uuid4()
    name: str = "Adam"
    instructions: List[str] = ["You are a helpful assistant."]
    inference: Inference = Inference(model="openai/gpt4")
    memories: Memories | None = None
    abilities: List[Ability] | None = None
    interfaces: List[Interface] | None = None

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

    @validator("inference")
    def check_inference_credentials(cls, inference: Inference) -> Inference | Exception:
        # TODO: Add check
        return inference

    @validator("memories")
    def check_memories(cls, memories: Memories) -> Memories | Exception | None:
        # TODO: Add vectordb check
        return memories
