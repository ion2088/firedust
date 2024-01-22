from uuid import uuid4, UUID
from pydantic import BaseModel
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
    deployments: List[Interface] | None = None
