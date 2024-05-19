"""
WIP

This module is responsible for interfacing with GitHub.
"""

from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.interface import DiscordConfig


class DiscordInterface:
    """
    A collection of methods to to deploy and interact with the assistant
    on Discord.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the DiscordInterface class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
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


class AsyncDiscordInterface:
    """
    A collection of methods to to deploy and interact with the assistant
    on Discord asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncDiscordInterface class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.
        """

        # configuration
        self.config = config
        self.api_client = api_client

    async def deploy(self, config: DiscordConfig) -> None:
        """
        Deploy the assistant on Discord asynchronously.

        Args:
            config (DiscordConfig): The Discord configuration.
        """
        raise NotImplementedError
