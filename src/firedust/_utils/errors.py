"""
This module contains custom errors used in the Firedust SDK.
"""


# AUTHENTICATION ERRORS
class MissingFiredustKeyError(Exception):
    def __init__(self) -> None:
        message = """
        The FIREDUST_API_KEY environment variable is not found. 
        Please, run firedust.connect.cloud(api_key) to set the API key.
        """
        super().__init__(message)


# API ERRORS
class APIError(Exception):
    def __init__(self, message: str, code: int = 500) -> None:
        self.code = code
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


class MemoryError(Exception):
    """
    Default error for the Memory class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


# INTERFACE ERRORS
class InterfaceError(Exception):
    """
    Default error for the Interface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmailError(InterfaceError):
    """
    Default error for the Email and EmailInterface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class SlackError(InterfaceError):
    """
    Default error for the Slack and SlackInterface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class GithubError(InterfaceError):
    """
    Default error for the Github and GithubInterface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DiscordError(InterfaceError):
    """
    Default error for the Discord and DiscordInterface class.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
