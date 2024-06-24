import httpx

from firedust.types import AssistantConfig
from firedust.types.interface import SlackConfig, SlackTokens
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import SlackError


class SlackInterface:
    """
    Slack interface module for the Firedust assistant. Deploy the assistant to Slack
    to interact with it in your workspace.

    Example:
    https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

    def create_app(
        self, description: str, greeting: str, configuration_token: str
    ) -> httpx.Response:
        """
        Creates a Slack app for the assistant.

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py

        Args:
            description (str): A short description of the assistant.
            greeting (str): A message that the assistant will greet users with.
            configuration_token (str): The Slack configuration token.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/assistant/interface/slack",
            data={
                "assistant": self.config.name,
                "description": description,
                "greeting": greeting,
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

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py

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

        response = self.api_client.put(
            "/assistant/interface/slack/tokens",
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

    def set_greeting(self, greeting: str) -> httpx.Response:
        """
        Sets the Slack greeting message.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.interface.slack.set_greeting("Hello! I'm here to help you.")
        ```

        Args:
            greeting (str): The greeting message.
        """
        if self.config.interfaces.slack is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interface.slack.create_app()"
            )

        response = self.api_client.put(
            "/assistant/interface/slack/greeting",
            data={
                "assistant": self.config.name,
                "greeting": greeting,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack greeting: {response.text}")

        self.config.interfaces.slack.greeting = greeting
        return response

    def deploy(self) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack.py
        """
        response = self.api_client.put(
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
        Removes the assistant deployment from Slack.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.interface.slack.remove_deployment()
        ```
        """
        response = self.api_client.delete(
            "/assistant/interface/slack/deploy",
            params={"assistant": self.config.name},
        )
        if not response.is_success:
            raise SlackError(f"Failed to remove deployment from Slack: {response.text}")

        return response

    def delete_app(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack app. Requires a configuration token from your Slack workspace.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.interface.slack.delete_app("SLACK_CONFIGURATION_TOKEN")
        ```

        Args:
            configuration_token (str): The Slack configuration token.
        """
        response = self.api_client.delete(
            "/assistant/interface/slack",
            params={
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
    https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack_async.py
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.config: AssistantConfig = config
        self.api_client: AsyncAPIClient = api_client

    async def create_app(
        self, description: str, configuration_token: str
    ) -> httpx.Response:
        """
        Creates a Slack app for the assistant asynchronously.

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack_async.py

        Args:
            description (str): A short description of the assistant.
            configuration_token (str): The Slack configuration token.
        """
        response = await self.api_client.post(
            "/assistant/interface/slack",
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

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack_async.py

        Args:
            app_token (str): The Slack app token.
            bot_token (str): The Slack bot token.
        """
        if self.config.interfaces.slack is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interface.slack.create_app()"
            )

        response = await self.api_client.put(
            "/assistant/interface/slack/tokens",
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

    async def set_greeting(self, greeting: str) -> httpx.Response:
        """
        Sets the Slack greeting message.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.load("ASSISTANT_NAME")
            await assistant.interface.slack.set_greeting("Hello! I'm here to help you.")

        asyncio.run(main())
        ```

        Args:
            greeting (str): The greeting message.
        """
        if self.config.interfaces.slack is None:
            raise SlackError(
                "Slack configuration not found. Please, create an app first. Hint: assistant.interface.slack.create_app()"
            )

        response = await self.api_client.put(
            "/assistant/interface/slack/greeting",
            data={
                "assistant": self.config.name,
                "greeting": greeting,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack greeting: {response.text}")

        self.config.interfaces.slack.greeting = greeting
        return response

    async def deploy(self) -> httpx.Response:
        """
        Deploys the assistant to Slack.

        Example:
        https://github.com/ion2088/firedust/blob/master/examples/deploy_to_slack_async.py
        """
        response = await self.api_client.put(
            f"/assistant/interface/slack/deploy?assistant={self.config.name}"
        )
        if not response.is_success:
            raise SlackError(f"Failed to deploy Slack app: {response.text}")

        return response

    async def remove_deployment(self) -> httpx.Response:
        """
        Removes the assistant deployment from Slack.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.load("ASSISTANT_NAME")
            await assistant.interface.slack.remove_deployment()

        asyncio.run(main())
        """
        response = await self.api_client.delete(
            "/assistant/interface/slack/deploy",
            params={"assistant": self.config.name},
        )
        if not response.is_success:
            raise SlackError(f"Failed to remove deployment from Slack: {response.text}")

        return response

    async def delete_app(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack app. Requires a configuration token from your Slack workspace.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.load("ASSISTANT_NAME")
            await assistant.interface.slack.delete_app("SLACK_CONFIGURATION_TOKEN")

        asyncio.run(main())
        """
        response = await self.api_client.delete(
            "/assistant/interface/slack",
            params={
                "assistant": self.config.name,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to delete Slack interface: {response.text}")

        return response
