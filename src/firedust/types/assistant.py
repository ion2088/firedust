from typing import List

from pydantic import BaseModel, field_validator

from .base import INFERENCE_MODEL
from .interface import Interfaces

ASSISTANT_NAME = str


class AssistantConfig(BaseModel, frozen=True):
    """
    The configuration of an AI Assistant.

    Args:
        name (str): The name of the assistant.
        instructions (str): The instructions of the assistant.
        model (INFERENCE_MODEL, optional): The inference model used by the assistant. Defaults to "openai/gpt-4".
        attached_memories (List[ASSISTANT_NAME], optional): A list of assistant names whose memories are accessible by the current assistant. Defaults to [].
        abilities (Sequence[Ability], optional): The abilities of the assistant. Defaults to None.
        interfaces (Sequence[Interface], optional): The deployments of the assistant. Defaults to None.
    """

    name: str
    instructions: str
    model: INFERENCE_MODEL = "openai/gpt-4"
    attached_memories: List[ASSISTANT_NAME] = []
    interfaces: Interfaces = Interfaces()

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str | Exception:
        if len(name) > 50:
            raise ValueError("Assistant name exceeds maximum length of 50 characters")
        if len(name) < 1:
            raise ValueError("Assistant name must be at least 1 character")
        return name
