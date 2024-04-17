from typing import Literal

from pydantic import BaseModel


class InterfaceConfig(BaseModel):
    """
    Represents an interface of the assistant.
    """

    interface: Literal["slack", "github", "discord", "email", "whatsapp"]


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
    interface: Literal["slack"] = "slack"
    app_id: str | None = None  # This is filled-in by the API
    credentials: SlackCredentials | None = None  # This is filled-in by the API
    tokens: SlackTokens | None = None  # This is filled-in by the API


class DiscordConfig(InterfaceConfig):
    """
    Configuration for Discord InterfaceConfig.
    """

    interface: Literal["discord"] = "discord"
    token: str
    channel: str


class GithubConfig(InterfaceConfig):
    """
    Configuration for Github InterfaceConfig.
    """

    interface: Literal["github"] = "github"
    token: str
    channel: str


# EMAIL
class EmailConfig(InterfaceConfig):
    """
    Configuration for Email InterfaceConfig.
    """

    interface: Literal["email"] = "email"
    email: str
    password: str
    host: str
    port: int
    tls: bool = True
    ssl: bool = True
    channel: str


class Email(BaseModel):
    """
    Represents an email.
    """

    subject: str
    body: str


class Interfaces(BaseModel):
    """
    Represents the interfaces of the assistant.
    """

    slack: SlackConfig | None = None
    github: GithubConfig | None = None
    discord: DiscordConfig | None = None
    email: EmailConfig | None = None
