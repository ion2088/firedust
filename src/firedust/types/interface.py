from typing import Literal

from pydantic import BaseModel


class InterfaceConfig(BaseModel):
    """
    Represents an interface of the assistant.
    """

    interface: Literal["slack"]  # space for more interfaces


class SlackTokens(BaseModel):
    """
    Represents the credentials of a Slack app.
    """

    app_token: str
    bot_token: str


class SlackCredentials(BaseModel):
    """
    Represents the credentials of a Slack app.
    """

    signing_secret: str
    client_id: str
    client_secret: str


class SlackConfig(InterfaceConfig):
    """
    Configuration for Slack InterfaceConfig.
    """

    description: str
    greeting: str  # A message that the assistant will greet users with.
    interface: Literal["slack"] = "slack"
    app_id: str | None = None  # This is filled-in by the API
    credentials: SlackCredentials | None = None  # This is filled-in by the API
    tokens: SlackTokens | None = None  # This is filled-in by the API


class Interfaces(BaseModel):
    """
    Represents the interfaces of the assistant.
    """

    slack: SlackConfig | None = None
    # add more interfaces as they come along
