from pydantic import BaseModel
from typing import Literal


class Interface(BaseModel):
    """
    Represents an interface of the assistant.
    """

    name: Literal["slack", "github", "discord"]


class SlackConfig(Interface):
    """
    Configuration for Slack interface.
    """

    name: Literal["slack"] = "slack"
    token: str
    signing_secret: str
    channel: str


class DiscordConfig(Interface):
    """
    Configuration for Discord interface.
    """

    name: Literal["discord"] = "discord"
    token: str
    channel: str


class GithubConfig(Interface):
    """
    Configuration for Github interface.
    """

    name: Literal["github"] = "github"
    token: str
    channel: str
