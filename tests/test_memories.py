import os
import random

import pytest

import firedust
from firedust.types import MemoryItem, Message
from firedust.utils.errors import APIError


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_memories() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        # Create a few test memories
        memories = [
            MemoryItem(
                assistant=assistant.config.name,
                content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
            ),
            MemoryItem(
                assistant=assistant.config.name,
                content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
            ),
        ]
        memory_ids = [mem.id for mem in memories]

        # Add memories to the assistant
        assistant.memory.add(memories)

        # Check that the memories were added
        retrieved_memories = assistant.memory.get(
            memory_ids=[mem.id for mem in memories]
        )
        assert all(mem.id in memory_ids for mem in retrieved_memories)

        # Test list all memories
        all_memories = assistant.memory.list()
        assert all(_id in memory_ids for _id in all_memories)

        # Test delete memories
        assistant.memory.delete(memory_ids=memory_ids)

        # Check that the memories were deleted
        retrieved_memories = assistant.memory.get(memory_ids=memory_ids)
        assert retrieved_memories == []
    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_share_memories() -> None:
    # Create two test assistants
    assistant1 = firedust.assistant.create(
        name=f"test-assistant-1-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    assistant2 = firedust.assistant.create(
        name=f"test-assistant-2-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        # Create a few test memories
        memories = [
            MemoryItem(
                assistant=assistant1.config.name,
                content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
            ),
            MemoryItem(
                assistant=assistant1.config.name,
                content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
            ),
        ]
        memory_ids = [mem.id for mem in memories]

        # Add memories to the first assistant
        assistant1.memory.add(memories)

        # Share the memories with the second assistant
        assistant1.memory.share(assistant2.config.name)

        # Check that the memories were shared
        assistant2_memories = assistant2.memory.list()
        assert all(_id in memory_ids for _id in assistant2_memories)

        # Check that the name of assistant1 is in the attached memories of assistant2
        assistant2 = firedust.assistant.load(assistant2.config.name)
        assert assistant1.config.name in assistant2.config.attached_memories

        # Detach the shared memories
        assistant1.memory.unshare(assistant2.config.name)

        # Check that the memories were unshared
        assistant2_memories = assistant2.memory.list()
        assert assistant2_memories == []

        # Check that the name of assistant1 is not in the attached memories of assistant2
        assistant2 = firedust.assistant.load(assistant2.config.name)
        assert assistant2.config.attached_memories == []

        # Sharing memories with a non-existing assistant should raise an error
        with pytest.raises(APIError) as _:
            assistant1.memory.share("non-existing-assistant")

        # Sharing memories with yourself should raise an error
        with pytest.raises(ValueError) as _:
            assistant1.memory.share(assistant1.config.name)

        # Unsharing memories with a non-existing assistant should raise an error
        with pytest.raises(APIError) as _:
            assistant1.memory.unshare("non-existing-assistant")
    finally:
        # Remove test assistants
        assistant1.delete(confirm=True)
        assistant2.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_memories() -> None:
    # Create a test assistant
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        # Create a few test memories
        memories = [
            MemoryItem(
                assistant=assistant.config.name,
                content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
            ),
            MemoryItem(
                assistant=assistant.config.name,
                content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
            ),
        ]
        memory_ids = [mem.id for mem in memories]

        # Add memories to the assistant
        await assistant.memory.add(memories)

        # Check that the memories were added
        retrieved_memories = await assistant.memory.get(
            memory_ids=[mem.id for mem in memories]
        )
        assert all(mem.id in memory_ids for mem in retrieved_memories)

        # Test list all memories
        all_memories = await assistant.memory.list()
        assert all(_id in memory_ids for _id in all_memories)

        # Test delete memories
        await assistant.memory.delete(memory_ids=memory_ids)

        # Check that the memories were deleted
        retrieved_memories = await assistant.memory.get(memory_ids=memory_ids)
        assert retrieved_memories == []
    finally:
        # Remove the test assistant
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_share_memories() -> None:
    # Create two test assistants
    assistant1 = await firedust.assistant.async_create(
        name=f"test-assistant-1-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )
    assistant2 = await firedust.assistant.async_create(
        name=f"test-assistant-2-{random.randint(1, 1000)}",
        instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    )

    try:
        # Create a few test memories
        memories = [
            MemoryItem(
                assistant=assistant1.config.name,
                content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
            ),
            MemoryItem(
                assistant=assistant1.config.name,
                content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
            ),
        ]
        memory_ids = [mem.id for mem in memories]

        # Add memories to the first assistant
        await assistant1.memory.add(memories)

        # Share the memories with the second assistant
        await assistant1.memory.share(assistant2.config.name)

        # Check that the memories were shared
        assistant2_memories = await assistant2.memory.list()
        assert all(_id in memory_ids for _id in assistant2_memories)

        # Check that the name of assistant1 is in the attached memories of assistant2
        assistant2 = await firedust.assistant.async_load(assistant2.config.name)
        assert assistant1.config.name in assistant2.config.attached_memories

        # Unshare memories
        await assistant1.memory.unshare(assistant2.config.name)

        # Check that the memories were detached
        assistant2_memories = await assistant2.memory.list()
        assert assistant2_memories == []

        # Check that the name of assistant1 is not in the attached memories of assistant2
        assistant2 = await firedust.assistant.async_load(assistant2.config.name)
        assert assistant2.config.attached_memories == []

        # Sharing memories with a non-existing assistant should raise an error
        with pytest.raises(APIError) as _:
            await assistant1.memory.share("non-existing-assistant")

        # Sharing memories with yourself should raise an error
        with pytest.raises(ValueError) as _:
            await assistant1.memory.share(assistant1.config.name)

        # Unsharing memories with a non-existing assistant should raise an error
        with pytest.raises(APIError) as _:
            await assistant1.memory.unshare("non-existing-assistant")
    finally:
        # Remove test assistants
        await assistant1.delete(confirm=True)
        await assistant2.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_add_chat_history() -> None:
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

        assistant.memory.add_chat_history([message1, message2, message3])

        response = assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            user="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.message
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_add_chat_history() -> None:
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

        await assistant.memory.add_chat_history([message1, message2, message3])

        response = await assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            user="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.message
    finally:
        await assistant.delete(confirm=True)
