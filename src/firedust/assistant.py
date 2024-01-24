"""
firedust.assistant
~~~~~~~~~~~~~~~~~~

The main entry point.
This module implements the Assistant class and its related functions.

Quickstart:
    import firedust

    firedust.assistant.connect("API_KEY")

    # Create a new assistant with a default configuration
    assistant = firedust.assistant.create()

    # Train the assistant on your data
    documents = [
        "Book of the Dead...",
        "Book of the Living...",
        "Customer support examples..."
    ]

    for doc in documents:
        assistant.learn.fast(doc)

    # Chat with the assistant
    response = assistant.chat.stream("Tell me about the Book of the Dead")

    for msg in response:
        print(msg)

    # Deploy the assistant
    assistant.deploy.slack(SLACK_CONFIG)
"""

import os
import logging
from uuid import UUID
from typing import List

from firedust.learning._base import Learning
from firedust.interface._base import Interface
from firedust.memory._base import Memory
from firedust.ability._base import Abilities
from firedust.interface.chat import Chat
from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.inference import InferenceConfig
from firedust._utils.errors import AssistantError

DEFAULT_CONFIG = AssistantConfig()
LOG = logging.getLogger("firedust")


class Assistant:
    """
    The Assistant class is the main entry point for interacting with Firedust.
    It is used to create, load, train, deploy and interact with an assistant.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        update (Update): Methods to update the configuration of the assistant.
        interface (Interface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (Learning): Methods to train the assistant on your data.
        chat (Chat): Methods to chat with the assistant.
        memory (Memory): Methods to interact with the assistant's memory.
        ability (Ability): Methods to manage and interact with the assistant's abilities.
    """

    def __init__(self, config: AssistantConfig = DEFAULT_CONFIG) -> None:
        """
        Initializes a new instance of the Assistant class.

        Args:
            config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
        """

        # configuration
        api_client = APIClient()
        self.config = config
        _validate(config, api_client)

        # management
        self.update = Update(self.config, api_client)
        self.interface = Interface(self.config, api_client)

        # essence
        self.learn = Learning(self.config, api_client)
        self.chat = Chat(config, api_client)
        self.memory = Memory(config, api_client)
        self.ability = Abilities(config, api_client)

    def __repr__(self) -> str:
        "Return a string representation of the Assistant"
        return f"<{self.__class__.__name__}>\n\n{self.config}"


class Update:
    """
    A collection of methods to update the configuration of the assistant.

    To update the assistant, you can use the following methods:
        assistant.update.name("Sam")
        assistant.update.add_instruction("You are a helpful assistant.")
        assistant.update.remove_instruction("You are a helpful assistant.")
        assistant.update.inference_config(InferenceConfig())
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Update class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    def name(self, name: str) -> None:
        """
        Updates the name of the assistant.

        Args:
            name (str): The new name of the assistant.
        """
        self.config.name = name
        self.api_client.put(
            f"assistant/{self.config.id}/update/name/{name}",
        )

    def add_instruction(self, instruction: str) -> None:
        """
        Adds an instruction to the assistant.

        Args:
            instruction (str): The instruction to add.
        """
        self.config.instructions.append(instruction)
        self.api_client.put(
            f"assistant/{self.config.id}/update/instructions/add/{instruction}",
        )

    def remove_instruction(self, instruction: str) -> None:
        """
        Removes an instruction from the assistant.

        Args:
            instruction (str): The instruction to remove.
        """
        self.config.instructions.remove(instruction)
        self.api_client.put(
            f"assistant/{self.config.id}/update/instructions/remove/{instruction}",
        )

    def inference_config(self, inference_config: InferenceConfig) -> None:
        """
        Updates the inference configuration of the assistant.

        Args:
            inference_config (InferenceConfig): The new inference configuration.
        """
        self.config.inference = inference_config
        self.api_client.put(
            f"assistant/{self.config.id}/update/inference",
            data=inference_config.model_dump(),
        )


def create(
    config: AssistantConfig = DEFAULT_CONFIG, api_client: APIClient = APIClient()
) -> Assistant | None:
    """
    Creates a new assistant.

    Args:
        config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
        api_client (APIClient): The API client.
    """
    response = api_client.post(
        f"{api_client.base_url}/assistant",
        data=config.model_dump(),
    )

    if response["status"] != 200:
        # TODO: Add error handlers and more explicit msgs
        raise AssistantError("An error occured while creating the assistant")

    LOG.info("Assistant created successfully in the cloud.")

    return Assistant(config)


def load(id: UUID, api_client: APIClient = APIClient()) -> Assistant:
    """
    Loads an existing assistant from the cloud.

    Args:
        id (UUID): The ID of the assistant to load.

    Returns:
        Assistant: The loaded assistant.
    """
    response = api_client.get(f"{api_client.base_url}/assistant/{id}/load")

    if response["status"] != 200:
        # TODO: Add more explicit error handling
        raise AssistantError(
            f"An error occured while loading the assistant with id {id}"
        )

    assistant_config = AssistantConfig(**response["data"])
    return Assistant(assistant_config)


def list(api_client: APIClient = APIClient()) -> List[AssistantConfig]:
    """
    Lists all the available assistants.

    Returns:
        List[AssistantConfig]: A list of all the assistants.
    """
    response = api_client.get(f"{api_client.base_url}/assistants/list")

    if response["status"] != 200:
        # TODO: Add more explicit error handling
        raise AssistantError("An error occured while listing the assistants")

    assistants = []
    for assistant in response["data"]:
        assistants.append(AssistantConfig(**assistant))

    return assistants


def delete(id: UUID, api_client: APIClient = APIClient()) -> None:
    """
    Deletes an existing assistant from the cloud.

    Args:
        id (UUID): The ID of the assistant to delete.
    """
    response = api_client.delete(f"{api_client.base_url}/assistant/{id}/delete")

    if response["status"] != 200:
        # TODO: Add more explicit error handling
        raise AssistantError(
            f"An error occured while deleting the assistant with id {id}"
        )

    LOG.info(f"Assistant with id {id} deleted successfully.")


def connect(api_key: str) -> None:
    """
    Connect to the Firedust cloud. Method is reserved to handle
    more complex authentication procedures in the future.

    Args:
        api_key (str): The API key to authenticate requests.
    """
    os.environ["FIREDUST_API_KEY"] = api_key


def _validate(config: AssistantConfig, api_client: APIClient = APIClient()) -> None:
    """
    Validates the assistant configuration.
    If the assistant ID already exists, the configuration will be validated.

    For new assistants, use firedust.assistant.create(assistant_config)

    Args:
        config (AssistantConfig): The assistant configuration.
        api_client (APIClient): The API client.
    """
    response = api_client.post(
        f"{api_client.base_url}/assistant/{config.id}/validate",
        data=config.model_dump(),
    )

    if response["status"] == 401:
        # Assistant with the same ID but different configuration exists
        raise AssistantError(
            f"""
            An assistant with id {config.id} but a with different 
            configuration already exists. To create a new assistant, please
            use firedust.assistant.create(assistant_config)
            """
        )
