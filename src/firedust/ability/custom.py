"""
Module to add and execute custom abilities.
This is achieved by creating a custom ability endpoint that is 
called by the assistant when the ability is used.

Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Create a custom ability
    ability_config = CustomAbilityConfig(
        id=uuid4(),
        name="My Custom Ability",
        description="A short description of the ability",
        instructions=["A list of instructions how and when to use the ability"],
        examples=["A list of examples how to call the endpoint"],
        endpoint="http://example.com/ability"
    )
    assistant.ability.custom.create(ability_config)

    # Use the custom ability
    assistant.ability.custom.execute(ability_config.id)
"""

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.ability import CustomAbilityConfig
from firedust._utils.errors import CustomAbilityError


class CustomAbility:
    """
    A collection of methods to add and execute custom abilities.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the CustomAbility class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

    def create(self, config: CustomAbilityConfig) -> None:
        """
        Creates a new custom ability.

        Args:
            config (CustomAbilityConfig): The custom ability configuration.
        """
        response = self.api_client.post(
            f"assistants/{self.config.id}/abilities/custom/create",
            data=config.model_dump(),
        )

        if response["status_code"] != 200:
            raise CustomAbilityError("Failed to create custom ability.")

    def execute(self, ability_id: str) -> str:
        """
        Executes a custom ability.

        Args:
            ability_id (str): The ID of the custom ability.
        """
        response = self.api_client.post(
            f"assistants/{self.config.id}/abilities/custom/execute",
            data={"id": ability_id},
        )

        if response["status_code"] != 200:
            raise CustomAbilityError("Failed to execute custom ability.")

        result: str = response["data"]["result"]
        return result
