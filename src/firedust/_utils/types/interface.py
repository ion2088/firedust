from pydantic import BaseModel
from typing import Literal


class Interface(BaseModel):
    """
    Represents an interface of the assistant.
    """

    name: Literal["slack", "github", "discord"]
    # TODO: Add the configurations
