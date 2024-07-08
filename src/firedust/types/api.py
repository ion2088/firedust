from typing import Any, Literal, Optional

from pydantic import BaseModel

from .base import UNIX_TIMESTAMP


class APIContent(BaseModel):
    """
    Represents the API content model.
    """

    status: Literal["success", "error"]
    timestamp: UNIX_TIMESTAMP
    data: Any = {}
    message: Optional[str] = None
