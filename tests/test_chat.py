import os

import pytest

from firedust.assistant import Assistant
from firedust.utils.types.api import MessageStreamEvent


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_streaming() -> None:
    # Create a test assistant
    assistant = Assistant.create()
    response = assistant.chat.stream("Hi, how are you?")

    # Check the response
    for _e in response:
        assert isinstance(_e, MessageStreamEvent)
        assert isinstance(_e.message, str)

    # Learn new stuff
    memory_id1 = assistant.learn.fast(
        "Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities."
    )
    memory_id2 = assistant.learn.fast(
        "Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand."
    )
    memory_ids = memory_id1 + memory_id2

    # Check that the response takes into consideration the new stuff
    answer = ""
    for _e in assistant.chat.stream(
        "Why are we almost a always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products?"
    ):
        answer += _e.message
    assert "product introduction cycles" in answer.lower()

    # Check that the new stuff is referenced in the last event
    assert memory_ids[0] in _e.memory_refs
    assert memory_ids[1] in _e.memory_refs

    # Remove the test assistant
    Assistant.delete(assistant.config.id, confirm_delete=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_complete() -> None:
    # Create a test assistant
    assistant = Assistant.create()
    response = assistant.chat.message("Hi, how are you?")
    assert isinstance(response, str)

    # Remove the test assistant
    Assistant.delete(assistant.config.id, confirm_delete=True)
