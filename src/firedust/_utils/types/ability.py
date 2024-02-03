from abc import ABC
from typing import Any, List, Literal
from uuid import UUID, uuid4

from ._base import BaseConfig

ABILITY_ID = UUID


class AbilityConfig(BaseConfig, ABC):
    """
    Represents a configuration for an ability.
    """

    id: ABILITY_ID = uuid4()
    name: str
    description: str
    instructions: List[str]
    examples: List[str]  # Examples how to use the ability


class CustomAbilityConfig(AbilityConfig):
    """
    Represents a configuration for a custom ability.
    """

    endpoint: str


class BuiltInAbilityConfig(AbilityConfig):
    """
    Represents a configuration for a built-in ability.
    """

    type: Literal[
        "send_email",
        "code",
        "translate",
        "math",
        "web_search",
        "label_data",
        "extract_data",
    ]

    def __setattr__(self, key: str, value: Any) -> None:
        # set immutable attributes
        if key == "type":
            raise AttributeError("Cannot set attribute 'type', it is immutable.")
        elif key == "name":
            raise AttributeError("Cannot set attribute 'name', it is immutable.")
        elif key == "description":
            raise AttributeError("Cannot set attribute 'description', it is immutable.")
        elif key == "instructions":
            raise AttributeError(
                "Cannot set attribute 'instructions', it is immutable."
            )
        elif key == "examples":
            raise AttributeError("Cannot set attribute 'examples', it is immutable.")

        return super().__setattr__(key, value)
