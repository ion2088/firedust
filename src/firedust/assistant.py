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

from firedust._private._assistant import Assistant
from firedust.utils.api import APIClient
from firedust.utils.errors import APIError
from firedust.utils.types.api import APIContent
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.inference import INFERENCE_MODEL

LOG = logging.getLogger("firedust")


def create(
    name: str,
    instructions: str,
    model: INFERENCE_MODEL = "mistral/mistral-medium",
    api_client: APIClient | None = None,
) -> Assistant:
    """
    Creates a new assistant with the specified configuration.

    Args:
        config (AssistantConfig): The assistant configuration. Defaults to DEFAULT_CONFIG.
        api_client (APIClient, optional): The API client. Defaults to None.

    Returns:
        Assistant: A new instance of the Assistant class.
    """
    config = AssistantConfig(name=name, instructions=instructions, model=model)

    api_client = api_client or APIClient()
    response = api_client.post("/assistant/create", data=config.model_dump())
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to create the assistant with config {config}: {response.text}",
        )
    LOG.info(
        f"Assistant {config.name} was created successfully and saved to the cloud."
    )
    return Assistant._create_instance(config, api_client)


def load(name: str, api_client: APIClient | None = None) -> "Assistant":
    """
    Loads an existing assistant with the specified name.

    Args:
        name (str): The name of the assistant to load.
        api_client (APIClient, optional): The API client. Defaults to None.

    Returns:
        Assistant: A new instance of the Assistant class.
    """
    api_client = api_client or APIClient()
    response = api_client.get(f"/assistant/{name}/load")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to load the assistant with id {name}: {response.text}",
        )
    content = APIContent(**response.json())
    config = AssistantConfig(**content.data["assistant"])
    return Assistant._create_instance(config, api_client)


def list(api_client: APIClient | None = None) -> List[AssistantConfig]:
    """
    Lists all existing assistants.

    Args:
        api_client (APIClient, optional): The API client. Defaults to None.
    """
    api_client = api_client or APIClient()
    response = api_client.get("/assistant/list")
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to list the assistants: {response.text}",
        )
    content = APIContent(**response.json())
    return [AssistantConfig(**assistant) for assistant in content.data["assistants"]]
