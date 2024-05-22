import os
import random

import pytest

import firedust
from firedust.types.memory import MemoryItem


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
def test_attached_memories() -> None:
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
        assistant2.memory.attach_memories(assistant1.config.name)

        # Check that the memories were shared
        assistant2_memories = assistant2.memory.list()
        assert all(_id in memory_ids for _id in assistant2_memories)
        assert assistant1.config.name in assistant2.config.attached_memories

        # Detach the shared memories
        assistant2.memory.detach_memories(assistant1.config.name)

        # Check that the memories were detached
        assistant2_memories = assistant2.memory.list()
        assert assistant2_memories == []
        assert assistant2.config.attached_memories == []
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
async def test_async_attached_memories() -> None:
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
        await assistant2.memory.attach_memories(assistant1.config.name)

        # Check that the memories were shared
        assistant2_memories = await assistant2.memory.list()
        assert all(_id in memory_ids for _id in assistant2_memories)
        assert assistant1.config.name in assistant2.config.attached_memories

        # Detach the shared memories
        await assistant2.memory.detach_memories(assistant1.config.name)

        # Check that the memories were detached
        assistant2_memories = await assistant2.memory.list()
        assert assistant2_memories == []
        assert assistant2.config.attached_memories == []
    finally:
        # Remove test assistants
        await assistant1.delete(confirm=True)
        await assistant2.delete(confirm=True)
