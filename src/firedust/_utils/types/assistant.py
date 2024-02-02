from uuid import uuid4, UUID
from typing import Any, List
from ._base import BaseConfig
from .inference import InferenceConfig
from .memory import MemoryConfig
from .ability import AbilityConfig
from .interface import Interfaces


class AssistantConfig(BaseConfig):
    """
    Represents the configuration of an AI Assistant.

    Args:
        id (UUID, optional): The unique identifier of the assistant. Defaults to uuid4().
        name (str, optional): The name of the assistant. Defaults to "Sam".
        instructions (List[str], optional): The instructions of the assistant. Defaults to ["You are a helpful assistant."].
        inference (InferenceConfig, optional): The inference configuration of the assistant. Defaults to InferenceConfig().
        memory (MemoryConfig, optional): The memory configuration of the assistant. Defaults to MemoryConfig().
        abilities (List[Ability], optional): The abilities of the assistant. Defaults to None.
        deployments (List[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    id: UUID = uuid4()
    name: str = "Sam"
    instructions: List[str] = ["You are a helpful assistant."]
    inference: InferenceConfig = InferenceConfig()
    memory: MemoryConfig = MemoryConfig()
    abilities: List[AbilityConfig] = []
    interfaces: Interfaces = Interfaces()

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "memory":
            raise AttributeError(
                """
                Cannot set attribute 'memory', it is immutable.
                To use a different memory configuration, create a new Assistant.
            """
            )

        return super().__setattr__(key, value)
