"""
Ability to solve math problems.

Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_NAME")

    # Solve a math problem
    assistant.ability.math.solve("What is 2 + 2?")
"""

from firedust.utils.api import SyncAPIClient
from firedust.utils.types.assistant import AssistantConfig


class MathAbility:
    """
    A collection of methods to solve and validate math problems.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the MathAbility class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

    def solve(self, problem: str) -> str:
        """
        Assistant solves the given math problem.

        Args:
            problem (str): The math problem to solve.
        """
        raise NotImplementedError("This method is not implemented yet.")
