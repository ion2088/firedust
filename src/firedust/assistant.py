"""
firedust.assistant
~~~~~~~~~~~~~~~~~~

The main entry point.
This module implements the Assistant class and its related functions.
"""

import os
import logging
from uuid import UUID
from typing import List

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust.learning._base import Learning
from firedust._utils.errors import AssistantError

DEFAULT_CONFIG = AssistantConfig()
LOG = logging.getLogger("firedust")


class Assistant:
    """
    The Assistant class is the main entry point for interacting with Firedust.
    It is used to create, load, train, deploy and interact with an assistant.
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
        validate(config, api_client)

        # # management
        # self.update = Update(config, api_client)
        # self.deploy = Deploy(config, api_client)

        # essence
        self.learn = Learning(config, api_client)
        # self.chat = Chat(config, api_client)
        # self.memory = Memory(config, api_client)
        # self.ability = Ability(config, api_client)
        # self.imagine = Imagination(config, api_client)
        # self.think = Reasoning(config, api_client)

    def __repr__(self) -> str:
        "Return a string representation of the Assistant"
        return f"<{self.__class__.__name__}>\n\n{self.config}"


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
        raise
    ("An error occured while creating the assistant")

    LOG.info("Assistant created successfully.")
    return Assistant(config)


def validate(config: AssistantConfig, api_client: APIClient) -> None:
    """
    Validates the assistant configuration.
    If the assistant ID already exists, the configuration will be validated.

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
            An assistant with the id {config.id} but a with different 
            configuration already exists. To create a new assistant, please
            use firedust.assistant.create(assistant_config)
            """
        )


def load(id: UUID) -> Assistant:
    "Load an existing assistant"
    raise NotImplementedError()


def list() -> List[Assistant]:
    "List all available assistants"
    raise NotImplementedError()


def delete(id: UUID) -> None:
    "Delete an existing assistant from the cloud"
    raise NotImplementedError()


def connect(api_key: str) -> None:
    """
    Connect to the Firedust cloud. Method is reserved to handle
    more complex authentication procedures in the future.

    Args:
        api_key (str): The API key to authenticate requests.
    """
    os.environ["FIREDUST_API_KEY"] = api_key
