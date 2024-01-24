"""
Code writing and execution abilities.

Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Train the assistant with code examples
    code_examples = []
    for example in code_examples:
        assistant.learn.fast(example)

    # Use the code ability to write and execute code
    code = assistant.ability.code.write(instruction="Write a script that...")
    assistant.ability.code.execute(code)

    # This ability is most useful when the assistant is asked to perform 
    # a task that requires writing and executing code.
"""

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig


class CodeAbility:
    """
    A collection of methods to write and execute code.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the CodeAbility class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

    def write(self, instruction: str) -> str:
        """
        Assistant writes code based on the given instruction.

        Args:
            instruction (str): The instruction for the assistant.
        """
        response = self.api_client.post(
            f"assistant/{self.config.id}/ability/code/write",
            data={"instruction": instruction},
        )
        code: str = response["data"]["code"]
        return code

    def execute(self, code: str) -> None:
        """
        Assistant executes the given code.

        Args:
            code (str): The code to execute.
        """
        # TODO: How do we execute non-python code?
        raise NotImplementedError
