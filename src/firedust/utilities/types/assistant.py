from uuid import uuid4, UUID
from pydantic import BaseModel, validator
from typing import List
from .inference import InferenceConfig
from .memory import MemoryConfig
from .ability import Ability
from .interface import Interface


class AssistantConfig(BaseModel):
    """
    Represents the configuration of an AI Assistant.
    """

    id: UUID = uuid4()
    name: str = "Joe"
    instructions: List[str] = ["You are a helpful assistant."]
    inference: InferenceConfig = InferenceConfig()
    memory: MemoryConfig = MemoryConfig()
    abilities: List[Ability] | None = None
    interfaces: List[Interface] | None = None

    @validator("instructions")
    def validate_instructions_length(
        cls, instructions: List[str]
    ) -> List[str] | Exception:
        for instruction in instructions:
            if len(instruction) > 500:
                raise ValueError("Instruction exceeds maximum length of 500 characters")
        return instructions

    @validator("inference")
    def check_inference_credentials(
        cls, inference: InferenceConfig
    ) -> InferenceConfig | Exception:
        # TODO: Add check
        return inference
