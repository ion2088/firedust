from firedust.utils.logging import configure_logger

from . import types
from .entrypoint import assistant

__all__ = ["assistant", "types"]

configure_logger()
