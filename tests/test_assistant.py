import os
import uuid

import pytest

from firedust._utils.errors import APIError
from firedust._utils.types.inference import InferenceConfig
from firedust.assistant import Assistant


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_create_list_load_delete_assistant() -> None:
    assert os.environ.get("FIREDUST_API_KEY") != ""

    # Create an assistant
    assistant = Assistant.create()
    assert isinstance(assistant, Assistant)
    assistant_id = assistant.config.id

    # List all assistants
    assistants_list = Assistant.list()
    existing_ids = [assistant.id for assistant in assistants_list]
    assert assistant_id in existing_ids

    # Update
    new_name = "Frodo"
    new_instructions = """
        1. Do not let the ring corrupt you.
        2. Take it to Modrdor.
        3. Destroy it in the fires of Mount Doom.
        4. Take care of Sam.
    """
    new_inference_config = InferenceConfig(provider="openai", model="gpt-4")
    assistant.update.name(new_name)
    assistant.update.instructions(new_instructions)
    assistant.update.inference(new_inference_config)

    # Load
    loaded_assistant = Assistant.load(assistant_id)
    assert isinstance(loaded_assistant, Assistant)
    assert loaded_assistant.config.id == assistant_id
    assert loaded_assistant.config.name == new_name
    assert loaded_assistant.config.instructions == new_instructions
    assert loaded_assistant.config.inference == new_inference_config

    # Delete
    Assistant.delete(assistant_id, confirm_delete=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_delete_non_existing_assistant() -> None:
    try:
        Assistant.delete(uuid.uuid4(), confirm_delete=True)
    except APIError as e:
        assert e.code == 404
        assert "Assistant not found." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_load_non_existing_assistant() -> None:
    try:
        Assistant.load(uuid.uuid4())
    except APIError as e:
        assert e.code == 404
        assert "Assistant not found." in e.message
    except Exception as e:
        assert False, f"Unexpected exception: {e}"
