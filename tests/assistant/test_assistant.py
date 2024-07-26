import os
import random

import pytest

import firedust
from firedust.types import Assistant, AsyncAssistant
from firedust.types.base import INFERENCE_MODEL
from firedust.utils.errors import APIError


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_create_list_load_delete_assistant() -> None:
    assert os.environ.get("FIREDUST_API_KEY") != ""

    # Create an assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    assert isinstance(assistant, Assistant)

    # Use try-finally to ensure the assistant is deleted even if the test fails
    try:
        # List all assistants
        assistants_list = firedust.assistant.list()
        existing_assistants = [assistant.config.name for assistant in assistants_list]
        assert assistant.config.name in existing_assistants

        # Update
        new_instructions = """
            1. Do not let the ring corrupt you.
            2. Take it to Modrdor.
            3. Destroy it in the fires of Mount Doom.
            4. Take care of Sam.
        """
        new_model: INFERENCE_MODEL = "mistral/mistral-medium"
        assistant.update.instructions(new_instructions)
        assistant.update.model(new_model)

        # Load
        loaded_assistant = firedust.assistant.load(assistant.config.name)
        assert isinstance(loaded_assistant, Assistant)
        assert loaded_assistant.config.instructions == new_instructions
        assert loaded_assistant.config.model == new_model
    finally:
        # Delete
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_create_existing_assistant() -> None:
    assistant_name = f"test-assistant-{random.randint(1, 1000)}"
    assistant1 = firedust.assistant.create(
        name=assistant_name,
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    # Use try-finally to ensure the assistant is deleted even if the test fails
    try:
        firedust.assistant.create(
            name=assistant_name,
            instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
        )
    except APIError as e:
        assert e.code == 409
        assert f"Assistant with the name {assistant_name} already exists." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"
    finally:
        assistant1.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_load_non_existing_assistant() -> None:
    try:
        firedust.assistant.load("non-existing-assistant")
    except APIError as e:
        assert e.code == 404
        assert "Assistant not found." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_create_list_load_delete_assistant() -> None:
    assert os.environ.get("FIREDUST_API_KEY") != ""

    # Create an assistant
    assistant_name = f"test-assistant-{random.randint(1, 1000)}"
    assistant = await firedust.assistant.async_create(
        name=assistant_name,
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    assert isinstance(assistant, AsyncAssistant)

    # Use try-finally to ensure the assistant is deleted even if the test fails
    try:
        # List all assistants
        assistants_list = await firedust.assistant.async_list()
        existing_assistants = [assistant.config.name for assistant in assistants_list]
        assert assistant.config.name in existing_assistants

        # Update
        new_instructions = """
            1. Do not let the ring corrupt you.
            2. Take it to Modrdor.
            3. Destroy it in the fires of Mount Doom.
            4. Take care of Sam.
        """
        new_model: INFERENCE_MODEL = "mistral/mistral-medium"
        await assistant.update.instructions(new_instructions)
        await assistant.update.model(new_model)

        # Load
        loaded_assistant = await firedust.assistant.async_load(assistant.config.name)
        assert isinstance(loaded_assistant, AsyncAssistant)
        assert loaded_assistant.config.instructions == new_instructions
        assert loaded_assistant.config.model == new_model
    finally:
        # Delete
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_create_existing_assistant() -> None:
    assistant_name = f"test-assistant-{random.randint(1, 1000)}"
    assistant1 = await firedust.assistant.async_create(
        name=assistant_name,
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    # Use try-finally to ensure the assistant is deleted even if the test fails
    try:
        await firedust.assistant.async_create(
            name=assistant_name,
            instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
        )
    except APIError as e:
        assert e.code == 409
        assert f"Assistant with the name {assistant_name} already exists." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"
    finally:
        await assistant1.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_load_non_existing_assistant() -> None:
    try:
        await firedust.assistant.async_load("non-existing-assistant")
    except APIError as e:
        assert e.code == 404
        assert "Assistant not found." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"
