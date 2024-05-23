from typing import Any, Literal

from pydantic import BaseModel

from .base import UNIX_TIMESTAMP


class APIContent(BaseModel):
    """
    Represents the API content model.
    """

    status: Literal["success", "error"]
    timestamp: UNIX_TIMESTAMP
    data: Any = {}
    message: str | None
