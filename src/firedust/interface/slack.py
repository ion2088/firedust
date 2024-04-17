import httpx

from firedust._utils.api import APIClient
from firedust._utils.errors import SlackError
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.interface import SlackConfig, SlackTokens


class SlackInterface:
    """
    Slack interface module for the Firedust assistant.

    Example:
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_ID")

        # Get your App Configuration Token from https://api.slack.com/apps
        configuration_token="SLACK_CONFIGURATION_TOKEN"

        # Create a Slack app for the assistant
        description="A short description of the assistant."
        assistant.interface.slack.create_app(slack_config)

        # Install the app and set the Slack App and Bot tokens, you can find them here:
        # https://api.slack.com/apps/<app_id>
        # https://api.slack.com/apps/<app_id>/oauth
        tokens = firedust.interface.SlackTokens(
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
            "/interface/slack/create_app",
            data={
                "assistant_id": self.assistant_config.id,
                "description": description,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to create Slack app: {response.text}")

        self.slack_config = SlackConfig(**response.json()["data"])

        return response

    def set_tokens(self, tokens: SlackTokens) -> httpx.Response:
        """
        Sets the Slack tokens.

        Args:
            tokens (SlackTokens): App and bot tokens.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/interface/slack/set_tokens",
            data={
                "assistant_id": self.assistant_config.id,
                "app_token": tokens.app_token,
                "bot_token": tokens.bot_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to set Slack tokens: {response.text}")

        self.slack_config.tokens = tokens
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
                "assistant_id": self.assistant_config.id,
                "api_key": self.api_client.api_key,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to deploy Slack app: {response.text}")

        return response

    # def update_credentials(self, credentials: SlackCredentials) -> httpx.Response:
    #     """
    #     Updates the signing secret.

    #     Args:
    #         credentials (SlackCredentials): The new credentials.

    #     Returns:
    #         httpx.Response: The response from the API.
    #     """
    #     response = self.api_client.post(
    #         "/interface/slack/update_signing_secret",
    #         data={
    #             "assistant_id": self.assistant_config.id,
    #             **credentials.model_dump(),
    #         },
    #     )
    #     if not response.is_success:
    #         raise SlackError(f"Failed to set Slack signing secret: {response.text}")

    #     self.assistant_config.interfaces.slack = self.slack_config
    #     return response

    # def update_description(
    #     self, description: str, configuration_token: str
    # ) -> httpx.Response:
    #     """
    #     Updates the Slack description. A slack configuration token is required to update the app manifest.

    #     Args:
    #         description (str): The new description.
    #         configuration_token (str): The configuration token.

    #     Returns:
    #         httpx.Response: The response from the API.
    #     """
    #     response = self.api_client.post(
    #         "/interface/slack/update_description",
    #         data={
    #             "assistant_id": self.assistant_config.id,
    #             "description": description,
    #             "configuration_token": configuration_token,
    #         },
    #     )
    #     if not response.is_success:
    #         raise SlackError(f"Failed to update Slack description: {response.text}")

    #     self.slack_config.description = description
    #     return response

    # def activity(self, last: int = 100) -> httpx.Response:
    #     """
    #     Not implemented.

    #     Get latest Slack activity of the assistant.

    #     Returns:
    #         httpx.Response: The response from the API.
    #     """
    #     # response = self.api_client.get(
    #     #     "/interface/slack/activity",
    #     #     params={
    #     #         "assistant_id": self.assistant_config.id,
    #     #     },
    #     # )
    #     # if not response.is_success:
    #     #     raise SlackError(f"Failed to get Slack activity: {response.text}")

    #     # return response
    #     raise NotImplementedError("This method is not implemented yet.")

    def delete(self, configuration_token: str) -> httpx.Response:
        """
        Deletes the Slack interface.

        Returns:
            httpx.Response: The response from the API.
        """
        response = self.api_client.post(
            "/interface/slack/delete",
            data={
                "assistant_id": self.assistant_config.id,
                "configuration_token": configuration_token,
            },
        )
        if not response.is_success:
            raise SlackError(f"Failed to delete Slack interface: {response.text}")

        return response
