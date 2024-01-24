"""
Slack interface module for the Firedust assistant.

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Deploy the assistant to Slack
    assistant.interface.slack.deploy(slack_config)

    # Chat with the assistant on Slack

    # Use Slack interface in custom workflows
    assistant.interface.slack.send("Tell me about the Book of the Dead")
"""

from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.api import APIClient
from firedust._utils.types.interface import SlackConfig
from firedust._utils.errors import SlackError


class SlackInterface:
    """
    A collection of methods to interact with the assistant on Slack.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Slack class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.assistant_config: AssistantConfig = config
        self.api_client: APIClient = api_client
        self.slack_config: SlackConfig | None = None

    def deploy(self, config: SlackConfig) -> None:
        """
        Deploys the assistant to Slack.

        Args:
            config (SlackConfig): The Slack configuration.
        """
        response = self.api_client.post(
            f"assistant/{self.assistant_config.id}/interface/slack/deploy",
            data=config.dict(),
        )

        if response["status_code"] != 200:
            raise SlackError("Failed to deploy assistant to Slack.")

        self.slack_config = SlackConfig(**response["data"])
        self.assistant_config.interfaces.slack = self.slack_config

    def send(self) -> None:
        """
        Sends a message to the assistant on Slack.
        """
        raise NotImplementedError
