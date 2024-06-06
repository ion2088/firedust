from firedust._assistant.interface.slack import AsyncSlackInterface, SlackInterface
from firedust.types import AssistantConfig
from firedust.utils.api import AsyncAPIClient, SyncAPIClient


class Interface:
    """
    A collection of methods to to deploy and interact with the assistant
    on various interfaces.

    Examples:
    - https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py
    -
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        # configuration
        self.config = config
        self.api_client = api_client

        # interfaces
        self.slack = SlackInterface(self.config, self.api_client)


class AsyncInterface:
    """
    A collection of async methods to to deploy and interact with the assistant
    on various interfaces asynchronously.

    Examples:
    - https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py
    -
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        # configuration
        self.config = config
        self.api_client = api_client

        # interfaces
        self.slack = AsyncSlackInterface(self.config, self.api_client)
