from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.interface import SlackConfig, GithubConfig


class Deploy:
    """
    A collection of methods to deploy the assistant to an interface.
    Interact with the assistant by chatting with it on Slack, Github,
    Discord or any other interface.

    To deploy the assistant, you can use the following methods:
        assistant.deploy.slack(SlackConfig())
        assistant.deploy.github(GithubConfig())
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Deploy class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    def slack(self, slack_config: SlackConfig) -> None:
        """
        Deploys the assistant to Slack.

        Args:
            slack_config (SlackConfig): The Slack configuration.
        """
        self.config.deployments.append(slack_config)
        self.api_client.post(
            f"{self.api_client.base_url}/assistant/{self.config.id}/deploy/slack",
            data=slack_config.model_dump(),
        )

    def github(self, github_config: GithubConfig) -> None:
        """
        Deploys the assistant to Github.

        Args:
            github_config (GithubConfig): The Github deployment configuration.
        """
        if github_config in self.config.deployments:
            raise ValueError("The assistant is already deployed to Github.")

        self.config.deployments.append(github_config)
        self.api_client.post(
            f"{self.api_client.base_url}/assistant/{self.config.id}/deploy/github",
            data=github_config.model_dump(),
        )
