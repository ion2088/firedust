"""
Ability to solve math problems.

Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Solve a math problem
    assistant.ability.math.solve("What is 2 + 2?")
"""

from firedust.utils.api import APIClient
from firedust.utils.types.assistant import AssistantConfig


class MathAbility:
    """
    A collection of methods to solve and validate math problems.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the MathAbility class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

    def solve(self, problem: str) -> str:
        """
        Assistant solves the given math problem.

        Args:
            problem (str): The math problem to solve.
        """
        response = self.api_client.post(
            f"assistant/{self.config.id}/ability/math/solve",
            data={"problem": problem},
        )
        solution: str = response.json()["data"]["solution"]

        return solution
