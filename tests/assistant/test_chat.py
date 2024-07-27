import os
import random

import pytest

import firedust
from firedust.types import Message, MessageStreamEvent, ReferencedMessage


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
        assert (
            "ai opportunities" in answer.lower()
            or "development cycles" in answer.lower()
        )

        # Check that the new stuff is referenced in the last event
        assert _e.references is not None
        assert memory_ids[0] in _e.references.memories
        assert memory_ids[1] in _e.references.memories
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
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.message, str)
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
        assert (
            "ai opportunities" in answer.lower()
            or "development cycles" in answer.lower()
        )

        # Check that the new stuff is referenced in the last event
        assert _e.references is not None
        assert memory_ids[0] in _e.references.memories
        assert memory_ids[1] in _e.references.memories
    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_complete() -> None:
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    try:
        response = await assistant.chat.message("Hi, how are you?")
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.message, str)
    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_add_get_delete_chat_hisoty() -> None:
    assistant = firedust.assistant.create("Sam")
    try:
        message1 = Message(
            assistant="Sam",
            user="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant="Sam",
            user="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant="Sam",
            user="product_team",
            message="John: Sure, the new roadmap is the following...",
            author="user",
        )
        messages = [message1, message2, message3]

        # Add chat history
        assistant.chat.add_history(messages)

        # Test that the history is available in context
        response = assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            user="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.message

        # Get chat history
        history = assistant.chat.get_history(user="product_team")
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m in history for m in messages)

        # Erase chat history
        assistant.chat.erase_history(user="product_team", confirm=True)

        # Check that the history is erased
        history = assistant.chat.get_history(user="product_team")
        assert len(history) == 0
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_add_get_delete_history() -> None:
    assistant = await firedust.assistant.async_create("Sam")
    try:
        message1 = Message(
            assistant="Sam",
            user="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant="Sam",
            user="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant="Sam",
            user="product_team",
            message="John: Sure, the new roadmap is the following...",
            author="user",
        )
        messages = [message1, message2, message3]

        # Add chat history
        await assistant.chat.add_history(messages)

        # Test that the history is available in context
        response = await assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            user="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.message

        # Get chat history
        history = await assistant.chat.get_history(user="product_team")
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m in history for m in messages)

        # Erase chat history
        await assistant.chat.erase_history(user="product_team", confirm=True)

        # Check that the history is erased
        history = await assistant.chat.get_history(user="product_team")
        assert len(history) == 0
    finally:
        await assistant.delete(confirm=True)
