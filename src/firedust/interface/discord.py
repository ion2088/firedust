"""
WIP

This module is responsible for interfacing with GitHub.
"""

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.interface import DiscordConfig


class DiscordInterface:
    """
    A collection of methods to to deploy and interact with the assistant
    on Discord.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the DiscordInterface class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """

        # configuration
        self.config = config
        self.api_client = api_client

    def deploy(self, config: DiscordConfig) -> None:
        """
        Deploy the assistant on Discord.

        Args:
            config (DiscordConfig): The Discord configuration.
        """
        raise NotImplementedError
