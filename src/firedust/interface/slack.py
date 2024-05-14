import httpx

from firedust.utils.api import APIClient
from firedust.utils.errors import SlackError
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.interface import SlackConfig, SlackTokens


class SlackInterface:
    """
    Slack interface module for the Firedust assistant.

    Example:
        import firedust
        from firedust.interface import SlackTokens

        assistant = firedust.assistant.load("ASSISTANT_NAME")

        # Get your App Configuration Token from https://api.slack.com/apps
        configuration_token="SLACK_CONFIGURATION_TOKEN"

        # Create a Slack app for the assistant
        description="A short description of the assistant."
        assistant.interface.slack.create_app(slack_config)

        # Install the app and set the Slack App and Bot tokens, you can find them here:
        # https://api.slack.com/apps/<app_id>
        # https://api.slack.com/apps/<app_id>/oauth
        tokens = SlackTokens(
            app_token="SLACK_APP_TOKEN",
            bot_token="SLACK_BOT_TOKEN",
        )
        assistant.interface.slack.set_tokens(tokens)

        # Deploy the assistant to Slack
        assistant.interface.slack.deploy()

        # Now you can interact with the assistant in your Slack workspace!
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
        self.config: SlackConfig | None = config.interfaces.slack

    def create_app(self, description: str, configuration_token: str) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Args:
            config (SlackConfig): The Slack configuration.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/interface/slack/create",
            data={
                "assistant": self.assistant_config.name,
                "description": description,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to create Slack app: {response.text}")

        self.config = SlackConfig(**response.json()["data"])

        return response

    def set_tokens(self, tokens: SlackTokens) -> httpx.Response:
        """
        Sets the Slack tokens.

        Args:
            tokens (SlackTokens): App and bot tokens.

        Returns:
            httpx.Response: The response from the API.
        """
        if self.config is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interfece.slack.create_app()"
            )

        response = self.api_client.post(
            "/interface/slack/set_tokens",
            data={
                "assistant": self.assistant_config.name,
                "app_token": tokens.app_token,
                "bot_token": tokens.bot_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack tokens: {response.text}")

        self.config.tokens = tokens
        return response

    def deploy(self) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/interface/slack/deploy",
            data={
                "assistant": self.assistant_config.name,
                "api_key": self.api_client.api_key,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to deploy Slack app: {response.text}")

        return response

    def delete(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack interface.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/interface/slack/delete",
            data={
                "assistant": self.assistant_config.name,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to delete Slack interface: {response.text}")

        return response
