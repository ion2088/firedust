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

import logging
import os
from typing import List
from uuid import UUID, uuid4

from firedust._utils.api import APIClient
from firedust._utils.errors import APIError, AssistantError
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.inference import InferenceConfig
from firedust._utils.types.memory import MemoryConfig
from firedust.ability._base import Abilities
from firedust.interface._base import Interface
from firedust.interface.chat import Chat
from firedust.learning._base import Learning
from firedust.memory._base import Memory

DEFAULT_CONFIG = AssistantConfig(
    id=uuid4(),
    name="Sam",
    instructions=["You are a helpful assistant."],
    inference=InferenceConfig(),
    memory=MemoryConfig(),
)
LOG = logging.getLogger("firedust")


class Assistant:
    """
    The Assistant class is the main entry point for interacting with Firedust.
    It is used to create, load, train, deploy and interact with an assistant.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (APIClient): The API client.
        update (Update): Methods to update the configuration of the assistant.
        interface (Interface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (Learning): Methods to train the assistant on your data.
        chat (Chat): Methods to chat with the assistant.
        memory (Memory): Methods to interact with the assistant's memory.
        ability (Ability): Methods to manage and interact with the assistant's abilities.
    """

    config: AssistantConfig
    api_client: APIClient

    update: "Update"
    interface: Interface
    learn: Learning
    chat: Chat
    memory: Memory
    ability: Abilities

    def __init__(self) -> None:
        raise AssistantError(
            """
            The Assistant class is not meant to be instantiated directly. \n\n
            
            To create or load an assistant, use the following methods: \n
            firedust.assistant.create(assistant_config) \n
            firedust.assistant.load(assistant_id)
            """
        )

    @classmethod
    def _init(self, config: AssistantConfig) -> "Assistant":
        """
        Initializes a new instance of the Assistant class.

        The initialization method is reserved for internal use only.
        To create or load an assistant, use the following methods:
        ```
            firedust.assistant.create(assistant_config)
            firedust.assistant.load(assistant_id)
        ```

        Args:
            config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.

        Returns:
            Assistant: The assistant instance.
        """

        # Create a new Assistant instance
        assistant = self.__new__(self)

        # configuration
        assistant.api_client = APIClient()
        assistant.config = config
        # _validate(config, assistant.api_client)

        # management
        assistant.update = Update(assistant.config, assistant.api_client)
        assistant.interface = Interface(assistant.config, assistant.api_client)

        # essence
        assistant.learn = Learning(assistant.config, assistant.api_client)
        assistant.chat = Chat(config, assistant.api_client)
        assistant.memory = Memory(config, assistant.api_client)
        assistant.ability = Abilities(config, assistant.api_client)

        return assistant

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
            f"/assistant/{self.config.id}/update/name/{name}",
        )

    def instructions(self, instructions: List[str]) -> None:
        """
        Updates the instructions of the assistant.

        Args:
            instructions (List[str]): The new instructions of the assistant.
        """
        self.config.instructions = instructions
        self.api_client.post(
            "/assistant/update/instructions",
            data={"id": str(self.config.id), "instructions": instructions},
        )

    def inference_config(self, inference_config: InferenceConfig) -> None:
        """
        Updates the inference configuration of the assistant.

        Args:
            inference_config (InferenceConfig): The new inference configuration.
        """
        self.config.inference = inference_config
        self.api_client.post(
            "/assistant/update/inference",
            data={
                "id": str(self.config.id),
                "inference": inference_config.model_dump(),
            },
        )


def create(
    config: AssistantConfig = DEFAULT_CONFIG, api_client: APIClient | None = None
) -> Assistant | None:
    """
    Creates a new assistant.

    Args:
        config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
        api_client (APIClient): The API client.
    """
    api_client = api_client or APIClient()
    response = api_client.post("/assistant/create", data=config.model_dump())
    response_json = response.json()
    if response.status_code != 200:
        raise APIError(
            f"An error occured while creating the assistant: {response_json['message']}"
        )

    LOG.info(
        f"Assistant {config.name} (ID: {config.id}) was created successfully and saved in the cloud."
    )

    return Assistant._init(config)


def load(assistant_id: UUID, api_client: APIClient | None = None) -> Assistant:
    """
    Loads an existing assistant from the cloud.

    Args:
        id (UUID): The ID of the assistant to load.

    Returns:
        Assistant: The loaded assistant.
    """
    api_client = api_client or APIClient()
    response = api_client.get(f"/assistant/{assistant_id}/load")
    response_json = response.json()
    if response.status_code != 200:
        raise AssistantError(
            f"An error occured while loading the assistant with id {assistant_id}: {response_json['message']}"
        )

    assistant_config = AssistantConfig(**response_json["data"]["assistant"])
    return Assistant._init(config=assistant_config)


def list(api_client: APIClient | None = None) -> List[AssistantConfig]:
    """
    Lists all the available assistants.

    Returns:
        List[AssistantConfig]: A list of all the assistants.
    """
    api_client = api_client or APIClient()
    response = api_client.get("/assistant/list")
    response_json = response.json()
    if response.status_code != 200:
        # TODO: Add more explicit error handling
        raise APIError(
            f"An error occured while listing the assistants: {response_json['message']}"
        )

    assistants = []
    for assistant in response_json["data"]["assistants"]:
        assistants.append(AssistantConfig(**assistant))

    return assistants


def delete(id: UUID, api_client: APIClient | None = None) -> None:
    """
    Deletes an existing assistant from the cloud.

    Args:
        id (UUID): The ID of the assistant to delete.
    """
    api_client = api_client or APIClient()
    response = api_client.delete(f"/assistant/{id}/delete")
    response_json = response.json()
    if response.status_code != 200:
        raise APIError(
            f"An error occured while deleting the assistant with id {id}: {response_json['message']}"
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


def _validate(config: AssistantConfig, api_client: APIClient | None = None) -> None:
    """
    Validates the assistant configuration.
    If the assistant ID already exists, the configuration will be validated.

    For new assistants, use firedust.assistant.create(assistant_config)

    Args:
        config (AssistantConfig): The assistant configuration.
        api_client (APIClient): The API client.
    """
    api_client = api_client or APIClient()
    response = api_client.post(
        f"/assistant/{config.id}/validate",
        data={"assistant": config.model_dump()},
    )

    if response.status_code == 401:
        # Assistant with the same ID but different configuration exists
        raise AssistantError(
            f"""
            An assistant with id {config.id} but a with different 
            configuration already exists. To create a new assistant, please
            use firedust.assistant.create(assistant_config)
            """
        )
