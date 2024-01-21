from typing import List
from pydantic import BaseModel
from uuid import UUID, uuid4


class Ability(BaseModel):
    """
    Represents an ability of the assistant.
    """

    id: UUID = uuid4()
    name: str
    description: str
    instructions: List[str]
    endpoint: str
