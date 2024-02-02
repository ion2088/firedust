from typing import Literal

from pydantic import BaseModel


class InterfaceConfig(BaseModel):
    """
    Represents an interface of the assistant.
    """

    name: Literal["slack", "github", "discord", "email", "whatsapp"]


class SlackConfig(InterfaceConfig):
    """
    Configuration for Slack InterfaceConfig.
    """

    name: Literal["slack"] = "slack"
    token: str
    signing_secret: str
    channel: str


class DiscordConfig(InterfaceConfig):
    """
    Configuration for Discord InterfaceConfig.
    """

    name: Literal["discord"] = "discord"
    token: str
    channel: str


class GithubConfig(InterfaceConfig):
    """
    Configuration for Github InterfaceConfig.
    """

    name: Literal["github"] = "github"
    token: str
    channel: str


# EMAIL
class EmailConfig(InterfaceConfig):
    """
    Configuration for Email InterfaceConfig.
    """

    name: Literal["email"] = "email"
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
