"""
The main entry point to create, load, and list your AI assistants.

Example:
    ```python
    import firedust

    # create a new assistant and interact with it
    assistant = firedust.assistant.create(
        name="Sam",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    response = assistant.chat.message("What is the shortest way to Mordor?")
    print(response.message)

    # stream messages
    for event in assistant.chat.stream("What is the shortest way to Mordor?"):
        print(event.message)

    # add your data to the assistant's memory
    important_data = [
        "Do not trust Smeagol.",
        "The ring is evil, it must be destroyed.",
    ]
    for data in important_data:
        assistant.learn.fast(data)
    response = assistant.chat.message("What should I do with the ring?")
    assert "destroy" in response.message.lower()

    # list all assistants
    assistants = firedust.assistant.list()

    # load an existing assistant
    assistant = firedust.assistant.load("Sam")
    ```

    For more examples, check:
    https://github.com/ion2088/firedust/tree/master/examples
"""

from typing import List

from firedust.types import APIContent, Assistant, AssistantConfig, AsyncAssistant
from firedust.types.base import INFERENCE_MODEL
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError
from firedust.utils.logging import LOG


def create(
    name: str,
    instructions: str = "",
    model: INFERENCE_MODEL = "openai/gpt-4",
) -> Assistant:
    """
    Creates a new assistant with the specified configuration.

    Arg
        name (str): The name of the assistant.
        instructions (str): The instructions for the assistant.
        model (INFERENCE_MODEL, optional): The inference model to use. Defaults to "mistral/mistral-medium".

    Returns:
        Assistant: A new instance of the assistant class.
    """
    config = AssistantConfig(name=name, instructions=instructions, model=model)
    api_client = SyncAPIClient()

    response = api_client.post("/assistant", data=config.model_dump())
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
    instructions: str = "",
    model: INFERENCE_MODEL = "openai/gpt-4",
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

    response = await api_client.post("/assistant", data=config.model_dump())
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
    response = api_client.get("/assistant", params={"name": name})
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to load assistant {name}: {response.text}",
        )
    content = APIContent(**response.json())
    config = AssistantConfig(**content.data)
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
    response = await api_client.get("/assistant", params={"name": name})
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to load the assistant with id {name}: {response.text}",
        )
    content = APIContent(**response.json())
    config = AssistantConfig(**content.data)
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
    configs = [AssistantConfig(**assistant) for assistant in content.data]
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
    configs = [AssistantConfig(**assistant) for assistant in content.data]
    return [
        await AsyncAssistant._create_instance(config, api_client) for config in configs
    ]
