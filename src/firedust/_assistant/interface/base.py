"""
Interface module for the Firedust assistant.
Interact with the assistant by chatting with it on Slack, Github,
email or other available interfaces.

Example:
    import firedust

    firedust.connect(api_key)

    # Create a new assistant
    assistant = firedust.assistant.create(assistant_config)

    # Deploy the assistant on email
    assistant.interface.email.deploy(email_config)

    # Deploy the assistant on Slack
    assistant.interface.slack.deploy(slack_config)

    # You can now chat with the assistant on Slack or send it an email
    # to interact with it.

    # See the list of interfaces where the assistant is deployed
    assistant.config.interfaces
"""

from firedust._assistant.interface.slack import AsyncSlackInterface, SlackInterface
from firedust.types import AssistantConfig
from firedust.utils.api import AsyncAPIClient, SyncAPIClient


class Interface:
    """
    A collection of methods to to deploy and interact with the assistant
    on various interfaces.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Deploy class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """

        # configuration
        self.config = config
        self.api_client = api_client

        # interfaces
        self.slack = SlackInterface(self.config, self.api_client)


class AsyncInterface:
    """
    A collection of methods to to deploy and interact with the assistant
    on various interfaces asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the Deploy class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.
        """

        # configuration
        self.config = config
        self.api_client = api_client

        # interfaces
        self.slack = AsyncSlackInterface(self.config, self.api_client)
