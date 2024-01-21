from uuid import UUID
from typing import List

from firedust.utilities.api import APIClient
from firedust.utilities.types.assistant import AssistantConfig


DEFAULT_CONFIG = AssistantConfig()


class Assistant:
    "Assistant base class"

    def __init__(self, config: AssistantConfig = DEFAULT_CONFIG) -> None:
        "Initialize the Assistant"
        # Send the configuration to the server
        # if the config is new, create a new assistant
        # else, load the assistant

        api_client = APIClient()

        self.config = config
        # self.learn = resources.Learn(config)

        raise NotImplementedError()

    def __repr__(self) -> str:
        "Return a string representation of the Assistant"
        return f"<{self.__class__.__name__}>\n\n{self.config}"

    def update(self, config: AssistantConfig) -> None:
        "Update the configuration of the assistant"
        raise NotImplementedError()

    def learn(self) -> None:
        "Add the given memory to the assistant"
        raise NotImplementedError()

    def forget(self) -> None:
        "Remove the given memory from the assistant"
        raise NotImplementedError()

    def decide(self) -> None:
        "Make a decision about the next action based on the given query"
        raise NotImplementedError()

    def chat(self) -> None:
        "Streaming chat with the assistant"
        raise NotImplementedError()

    def complete(self) -> None:
        "Complete the given query"
        raise NotImplementedError()


def create(config: AssistantConfig = DEFAULT_CONFIG) -> Assistant:
    "Create an assistant"
    # Send the configuration to the server
    return Assistant(config)


def load(id: UUID) -> Assistant:
    "Load an existing assistant"
    raise NotImplementedError()


def list() -> List[Assistant]:
    "List all available assistants"
    raise NotImplementedError()


def delete(id: UUID) -> None:
    "Delete an existing assistant from the cloud"
    raise NotImplementedError()
