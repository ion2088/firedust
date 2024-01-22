from pydantic import BaseModel
from typing import Literal


class Deployment(BaseModel):
    """
    Represents an interface of the assistant.
    """

    name: Literal["slack", "github", "discord"]


class SlackConfig(Deployment):
    """
    Configuration for Slack Deployment.
    """

    name: Literal["slack"] = "slack"
    token: str
    signing_secret: str
    channel: str


class DiscordConfig(Deployment):
    """
    Configuration for Discord Deployment.
    """

    name: Literal["discord"] = "discord"
    token: str
    channel: str


class GithubConfig(Deployment):
    """
    Configuration for Github Deployment.
    """

    name: Literal["github"] = "github"
    token: str
    channel: str
