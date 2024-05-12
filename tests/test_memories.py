import os

import pytest

import firedust
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.memory import MemoryItem


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_memories() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create()

    # Create a few test memories
    memories = [
        MemoryItem(
            assistant=assistant.config.id,
            content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
        ),
        MemoryItem(
            assistant=assistant.config.id,
            content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
        ),
    ]
    memory_ids = [mem.id for mem in memories]

    # Add memories to the assistant
    assistant.memory.add(memories)

    # Check that the memories were added
    retrieved_memories = assistant.memory.get(memory_ids=[mem.id for mem in memories])
    assert all(mem.id in memory_ids for mem in retrieved_memories)

    # Test list all memories
    all_memories = assistant.memory.list()
    assert all(_id in memory_ids for _id in all_memories)

    # Test delete memories
    assistant.memory.delete(memory_ids=memory_ids)

    # Check that the memories were deleted
    retrieved_memories = assistant.memory.get(memory_ids=memory_ids)
    assert retrieved_memories == []

    # Remove the test assistant
    assistant.delete(confirm_delete=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_shared_memories() -> None:
    # Create two test assistants
    assistant1 = firedust.assistant.create(
        config=AssistantConfig(
            name="Assistant 1", instructions="You are a helpful assistant."
        )
    )
    assistant2 = firedust.assistant.create(
        config=AssistantConfig(
            name="Assistant 2", instructions="You are a helpful assistant."
        )
    )

    # Create a few test memories
    memories = [
        MemoryItem(
            assistant=assistant1.config.id,
            content="Due to our product introduction cycles, we are almost always in various stages of transitioning the architecture of our Data Center, Professional Visualization, and Gaming products. We will have a broader and faster Data Center product launch cadence to meet a growing and diverse set of AI opportunities.",
        ),
        MemoryItem(
            assistant=assistant1.config.id,
            content="Deployment of new products to customers creates additional challenges due to the complexity of our technologies, which has impacted and may in the future impact the timing of customer purchases or otherwise impact our demand.",
        ),
    ]
    memory_ids = [mem.id for mem in memories]

    # Add memories to the first assistant
    assistant1.memory.add(memories)

    # Share the memories with the second assistant
    assistant2.memory.attach_collection(assistant1.config.id)

    # Check that the memories were shared
    shared_memories = assistant2.memory.list()
    assert all(_id in memory_ids for _id in shared_memories)

    # Detach the shared memories
    assistant2.memory.detach_collection(assistant1.config.id)

    # Check that the memories were detached
    shared_memories = assistant2.memory.list()
    assert shared_memories == []

    # Remove test assistants
    assistant1.delete(confirm_delete=True)
    assistant2.delete(confirm_delete=True)
