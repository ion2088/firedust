import httpx

from firedust.types import AssistantConfig
from firedust.types.interface import SlackConfig, SlackTokens
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import SlackError


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

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Slack class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

    def create_app(self, description: str, configuration_token: str) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Args:
            config (SlackConfig): The Slack configuration.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/assistant/interface/slack/create_app",
            data={
                "assistant": self.config.name,
                "description": description,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to create Slack app: {response.text}")

        self.config.interfaces.slack = SlackConfig(**response.json()["data"])

        return response

    def set_tokens(self, app_token: str, bot_token: str) -> httpx.Response:
        """
        Sets the Slack tokens.

        Args:
            app_token (str): The Slack app token.
            bot_token (str): The Slack bot token.

        Returns:
            httpx.Response: The response from the API.
        """
        if self.config.interfaces.slack is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interfece.slack.create_app()"
            )

        response = self.api_client.post(
            "/assistant/interface/slack/set_tokens",
            data={
                "assistant": self.config.name,
                "app_token": app_token,
                "bot_token": bot_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack tokens: {response.text}")

        self.config.interfaces.slack.tokens = SlackTokens(
            app_token=app_token, bot_token=bot_token
        )
        return response

    def deploy(self) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/assistant/interface/slack/deploy",
            data={
                "assistant": self.config.name,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to deploy Slack app: {response.text}")

        return response

    def remove_deployment(self) -> httpx.Response:
        """
        Removes the assistant from Slack.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/assistant/interface/slack/remove_deployment",
            data={
                "assistant": self.config.name,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to remove deployment from Slack: {response.text}")

        return response

    def delete_app(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack interface.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/assistant/interface/slack/delete_app",
            data={
                "assistant": self.config.name,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to delete Slack interface: {response.text}")

        return response


class AsyncSlackInterface:
    """
    Async Slack interface module for the Firedust assistant.

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

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncSlackInterface class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: AsyncAPIClient = api_client

    async def create_app(
        self, description: str, configuration_token: str
    ) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Args:
            config (SlackConfig): The Slack configuration.

        Returns:
            httpx.Response: The response from the API.
        """
        response = await self.api_client.post(
            "/assistant/interface/slack/create_app",
            data={
                "assistant": self.config.name,
                "description": description,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to create Slack app: {response.text}")

        self.config.interfaces.slack = SlackConfig(**response.json()["data"])

        return response

    async def set_tokens(self, app_token: str, bot_token: str) -> httpx.Response:
        """
        Sets the Slack tokens.

        Args:
            tokens (SlackTokens): App and bot tokens.

        Returns:
            httpx.Response: The response from the API.
        """
        if self.config.interfaces.slack is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interface.slack.create_app()"
            )

        response = await self.api_client.post(
            "/assistant/interface/slack/set_tokens",
            data={
                "assistant": self.config.name,
                "app_token": app_token,
                "bot_token": bot_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack tokens: {response.text}")

        self.config.interfaces.slack.tokens = SlackTokens(
            app_token=app_token, bot_token=bot_token
        )
        return response

    async def deploy(self) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Returns:
            httpx.Response: The response from the API.
        """
        response = await self.api_client.post(
            "/assistant/interface/slack/deploy",
            data={
                "assistant": self.config.name,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to deploy Slack app: {response.text}")

        return response

    async def remove_deployment(self) -> httpx.Response:
        """
        Removes the assistant from Slack.

        Returns:
            httpx.Response: The response from the API.
        """
        response = await self.api_client.post(
            "/assistant/interface/slack/remove_deployment",
            data={
                "assistant": self.config.name,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to remove deployment from Slack: {response.text}")

        return response

    async def delete_app(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack interface.

        Returns:
            httpx.Response: The response from the API.
        """
        response = await self.api_client.post(
            "/assistant/interface/slack/delete_app",
            data={
                "assistant": self.config.name,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to delete Slack interface: {response.text}")

        return response
