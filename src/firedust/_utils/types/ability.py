from typing import List
from uuid import UUID, uuid4

from ._base import BaseConfig

ABILITY_ID = UUID


class AbilityConfig(BaseConfig):
    """
    Represents a configuration for an ability.
    """

    id: ABILITY_ID = uuid4()
    name: str
    description: str
    instructions: List[str]
    examples: List[str]  # Examples how to use the ability


class CustomAbilityConfig(BaseConfig):
    """
    Represents a configuration for a custom ability.
    """

    id: ABILITY_ID = uuid4()
    name: str
    description: str
    instructions: List[str]
    endpoint: str
    examples: List[str]  # Examples how to use the ability


class BuiltInAbilityConfig(BaseConfig):
    """
    Represents a configuration for a built-in ability.
    """

    id: ABILITY_ID = uuid4()
    name: str
    description: str
    instructions: List[str]
    examples: List[str]  # Examples how to use the ability
