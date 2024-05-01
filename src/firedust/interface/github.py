"""
WIP

This module is responsible for interfacing with GitHub.
"""

from firedust.utils.api import APIClient
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.interface import GithubConfig


class GithubInterface:
    """
    A collection of methods to to deploy and interact with the assistant
    on GitHub.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the GithubInterface class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """

        # configuration
        self.config = config
        self.api_client = api_client

    def deploy(self, config: GithubConfig) -> None:
        """
        Deploy the assistant on GitHub.

        Args:
            config (GithubConfig): The GitHub configuration.
        """
        raise NotImplementedError
