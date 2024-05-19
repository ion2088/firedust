import os
import random

import pytest

import firedust
from firedust.utils.types.api import MessageStreamEvent


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_streaming() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
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
    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_complete() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        response = assistant.chat.message("Hi, how are you?")
        assert isinstance(response, str)
    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_streaming() -> None:
    # Create a test assistant
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        response = assistant.chat.stream("Hi, how are you?")

        # Check the response
        async for _e in response:
            assert isinstance(_e, MessageStreamEvent)
            assert isinstance(_e.message, str)

        # Learn new stuff
        memory_id1 = await assistant.learn.fast(
            "Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities."
        )
        memory_id2 = await assistant.learn.fast(
            "Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand."
        )
        memory_ids = memory_id1 + memory_id2

        # Check that the response takes into consideration the new stuff
        answer = ""
        async for _e in assistant.chat.stream(
            "Why are we almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products?"
        ):
            answer += _e.message
        assert "product introduction cycles" in answer.lower()

        # Check that the new stuff is referenced in the last event
        assert memory_ids[0] in _e.memory_refs
        assert memory_ids[1] in _e.memory_refs
    finally:
        # Remove the test assistant
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_complete() -> None:
    # Create a test assistant
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        response = await assistant.chat.message("Hi, how are you?")
        assert isinstance(response, str)
    finally:
        # Remove the test assistant
        await assistant.delete(confirm=True)
