"""
firedust.assistant
~~~~~~~~~~~~~~~~~~

The main entry point.
This module implements the Assistant class and its related functions.

Quickstart:
    ```python
    import os
    from firedust.assistant import Assistant

    # Set your key
    os.environ["FIREDUST_API_KEY"] = "your_api_key"

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

    # Chat with the assistant, training data is available immediately
    response = assistant.chat.stream("Tell me about the Book of the Dead")

    for msg in response:
        print(msg)

    # Deploy the assistant
    assistant.deploy.slack(SLACK_CONFIG)
    ```
"""

import logging
from typing import List

from firedust.types import Assistant, AsyncAssistant
from firedust.types.api import APIContent
from firedust.types.assistant import AssistantConfig
from firedust.types.base import INFERENCE_MODEL
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError

LOG = logging.getLogger("firedust")


def create(
    name: str,
    instructions: str,
    model: INFERENCE_MODEL = "mistral/mistral-medium",
) -> Assistant:
    """
    Creates a new assistant with the specified configuration.

    Args:
        name (str): The name of the assistant.
        instructions (str): The instructions for the assistant.
        model (INFERENCE_MODEL, optional): The inference model to use. Defaults to "mistral/mistral-medium".

    Returns:
        Assistant: A new instance of the assistant class.
    """
    config = AssistantConfig(name=name, instructions=instructions, model=model)
    api_client = SyncAPIClient()

    response = api_client.post("/assistant/create", data=config.model_dump())
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to create an assistant with config {config}: {response.text}",
        )
    LOG.info(
        f"Assistant {config.name} was created successfully and saved to the cloud."
    )

    return Assistant._create_instance(config, api_client)


async def async_create(
    name: str,
    instructions: str,
    model: INFERENCE_MODEL = "mistral/mistral-medium",
) -> AsyncAssistant:
    """
    Asynchronously creates a new assistant with the specified configuration.

    Args:
        name (str): The name of the assistant.
        instructions (str): The instructions for the assistant.
        model (INFERENCE_MODEL, optional): The inference model to use. Defaults to "mistral/mistral-medium".

    Returns:
        AsyncAssistant: A new instance of the AsyncAssistant class.
    """
    config = AssistantConfig(name=name, instructions=instructions, model=model)
    api_client = AsyncAPIClient()

    response = await api_client.post("/assistant/create", data=config.model_dump())
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to create an assistant with config {config}: {response.text}",
        )
    LOG.info(
        f"Assistant {config.name} was created successfully and saved to the cloud."
    )

    return await AsyncAssistant._create_instance(config, api_client)


def load(name: str) -> Assistant:
    """
    Loads an existing assistant with the specified name.

    Args:
        name (str): The name of the assistant to load.

    Returns:
        Assistant: A new instance of the Assistant class.
    """
    api_client = SyncAPIClient()
    response = api_client.get(f"/assistant/{name}/load")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to load the assistant with id {name}: {response.text}",
        )
    content = APIContent(**response.json())
    config = AssistantConfig(**content.data["assistant"])
    return Assistant._create_instance(config, api_client)


async def async_load(name: str) -> AsyncAssistant:
    """
    Asynchronously loads an existing assistant with the specified name.

    Args:
        name (str): The name of the assistant to load.

    Returns:
        AsyncAssistant: A new instance of the AsyncAssistant class.
    """
    api_client = AsyncAPIClient()
    response = await api_client.get(f"/assistant/{name}/load")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to load the assistant with id {name}: {response.text}",
        )
    content = APIContent(**response.json())
    config = AssistantConfig(**content.data["assistant"])
    return await AsyncAssistant._create_instance(config, api_client)


def list() -> List[Assistant]:
    """
    Lists all existing assistants.

    Returns:
        List[Assistant]: A list of Assistant objects.
    """
    api_client = SyncAPIClient()
    response = api_client.get("/assistant/list")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to list the assistants: {response.text}",
        )
    content = APIContent(**response.json())
    configs = [AssistantConfig(**assistant) for assistant in content.data["assistants"]]
    return [Assistant._create_instance(config, api_client) for config in configs]


async def async_list() -> List[AsyncAssistant]:
    """
    Asynchronously lists all existing assistants.

    Returns:
        List[AsyncAssistant]: A list of AsyncAssistant objects.
    """
    api_client = AsyncAPIClient()
    response = await api_client.get("/assistant/list")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to list the assistants: {response.text}",
        )
    content = APIContent(**response.json())
    configs = [AssistantConfig(**assistant) for assistant in content.data["assistants"]]
    return [
        await AsyncAssistant._create_instance(config, api_client) for config in configs
    ]
