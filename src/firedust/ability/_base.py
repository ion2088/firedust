"""
Ability base module for the Firedust assistant.

There are two types of abilities:
    - Built-in abilities, available to all assistants
    - Custom abilities, created by the user

Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_NAME")

    # Check available abilities
    abilities = assistant.ability.list()

    # Use a built-in ability
    assistant.ability.email.write(to="joe@pozole.com", instruction="Write an email to let Joe know about the most recent status of the project.")

    # Use a custom ability
    assistant.ability.custom("CUSTOM_ABILITY_ID").execute()

    # Create a custom ability
    assistant.ability.custom.create(
        name="My Custom Ability",
        description="A short description of the ability",
        instructions=["A list of instructions how to use the ability"],
        examples=["A list of examples how to use the ability"]
        endpoint="http://example.com/ability",
    )
"""

from firedust.ability.code import CodeAbility
from firedust.ability.custom import CustomAbility
from firedust.ability.math import MathAbility
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.types.assistant import AssistantConfig


class Abilities:
    """
    A collection of methods to configure and engage with assistant's abilities.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Abilities class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

        # built-in abilities
        self.math = MathAbility(self.config, self.api_client)
        self.code = CodeAbility(self.config, self.api_client)

        # custom abilities
        self.custom = CustomAbility(self.config, self.api_client)

    def update(self, ability: str) -> None:
        """
        Updates the abilities.
        """
        raise NotImplementedError("The update method is not implemented.")

    def add_instruction(self, ability_id: str, instruction: str) -> None:
        """
        Adds an instruction to the ability.

        Args:
            ability_id (str): The ID of the ability.
            instruction (str): The instruction to add.
        """
        raise NotImplementedError("The add_instruction method is not implemented.")


class AsyncAbilities:
    """
    A collection of methods to configure and engage with assistant's abilities asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncAbilities class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: AsyncAPIClient = api_client

    async def update(self, ability: str) -> None:
        """
        Updates the abilities.
        """
        raise NotImplementedError("The update method is not implemented.")

    async def add_instruction(self, ability_id: str, instruction: str) -> None:
        """
        Adds an instruction to the ability.

        Args:
            ability_id (str): The ID of the ability.
            instruction (str): The instruction to add.
        """
        raise NotImplementedError("The add_instruction method is not implemented.")
