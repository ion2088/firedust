"""
This module contains custom errors used in the Firedust SDK.
"""


# AUTHENTICATION ERRORS
class MissingFiredustKeyError(Exception):
    def __init__(self) -> None:
        message = """
        FIREDUST_API_KEY environment variable is not found. 
        Get your API key at https://tally.so/r/wbkB1L
        """
        super().__init__(message)


# API ERRORS
class APIError(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.code = code
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"APIError (code={self.code}): {super().__str__()}"


# ASSISTANT ERRORS
class AssistantError(Exception):
    """
    Default error for the Assistant class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


# MEMORY ERRORS
class MemoryError(Exception):
    """
    Default error for the Memory class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


# INTERFACE ERRORS
class SlackError(Exception):
    """
    Default error for the Slack and SlackInterface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
