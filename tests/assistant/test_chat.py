import os
import random

import pytest

import firedust
from firedust.types import (
    JSONSchema,
    JSONSchemaConfig,
    Message,
    MessageStreamEvent,
    ReferencedMessage,
    ResponseFormat,
)


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
            assert isinstance(_e.content, str)

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
            "What product categories are we almost always in various stages of transitioning the architecture?"
        ):
            answer += _e.content
        assert any(
            [
                "data center" in answer.lower(),
                "professional visualization" in answer.lower(),
                "gaming" in answer.lower(),
            ]
        )

        # Check that the new stuff is referenced in the last event
        assert _e.references is not None
        assert memory_ids[0] in _e.references.memory_ids
        assert memory_ids[1] in _e.references.memory_ids
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
        assert isinstance(response.content, str)
    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_character() -> None:
    # Create a test assistant with a role-playing scenario
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="""
        You are a roleplay assistant. When a character is specified, respond as that character in first person.
        
        Character backgrounds:
        - Brave Knight (Sir Galahad): A noble knight devoted to justice and protecting the innocent. Speaks with honor and chivalry, uses formal language, and always puts duty before self.
        - Wise Wizard (Merlin): An ancient wizard with vast knowledge of magic and the world. Speaks cryptically with wisdom, often references ancient lore, and sees the bigger picture.
        - Evil Sorcerer (Morgoth): A dark sorcerer consumed by power and ambition. Speaks with arrogance and malice, delights in chaos, and seeks to dominate others.
        """,
    )

    try:
        # Test Brave Knight character roleplay - identity question
        response = assistant.chat.message(
            message="What is your name?",
            character="Brave Knight",
        )
        assert isinstance(response, ReferencedMessage)
        knight_response = response.content.lower()
        assert (
            "galahad" in knight_response
        ), f"Knight should identify as Galahad. Got: {response.content}"

        # Test Wise Wizard character roleplay - knowledge question
        response = assistant.chat.message(
            message="Who are you?",
            character="Wise Wizard",
        )
        assert isinstance(response, ReferencedMessage)
        wizard_response = response.content.lower()
        assert (
            "merlin" in wizard_response or "wizard" in wizard_response
        ), f"Wizard should identify as Merlin or Wizard. Got: {response.content}"

        # Test Evil Sorcerer character roleplay - power question
        response = assistant.chat.message(
            message="Who are you?",
            character="Evil Sorcerer",
        )
        assert isinstance(response, ReferencedMessage)
        sorcerer_response = response.content.lower()
        assert (
            "morgoth" in sorcerer_response or "sorcerer" in sorcerer_response
        ), f"Sorcerer should identify as Morgoth or Sorcerer. Got: {response.content}"

    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_instructions() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant.",
    )

    try:
        # Send a message with specific instructions
        response = assistant.chat.message(
            message="What is 2+2?",
            instructions="Answer only with the number, no additional text.",
        )
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)

        response_value = int(response.content)
        assert response_value == 4

    finally:
        # Remove the test assistant
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_structured_response() -> None:
    # Create a test assistant
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant.",
    )

    try:
        # Create a JSON schema for structured response
        schema = JSONSchema(
            type="object",
            properties={
                "name": JSONSchema(type="string", description="The name of the person"),
                "occupation": JSONSchema(
                    type="string", description="The occupation of the person"
                ),
            },
            required=["name", "occupation"],
            additionalProperties=False,
        )

        response_format = ResponseFormat(
            type="json_schema",
            json_schema=JSONSchemaConfig(
                name="person_info",
                description="Extract person information",
                schema=schema,
            ),
        )

        # Send a message with structured response format
        response = assistant.chat.message(
            message="My name is John Doe and I'm a software engineer.",
            response_format=response_format,
            add_to_memory=False,
        )

        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)
        # The response should be valid JSON
        import json

        parsed_response = json.loads(response.content)
        assert "name" in parsed_response
        assert "occupation" in parsed_response
        assert parsed_response["name"] == "John Doe"
        assert "software engineer" in parsed_response["occupation"].lower()

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
    )

    try:
        response = assistant.chat.stream("Hi, how are you?")

        # Check the response
        async for _e in response:
            assert isinstance(_e, MessageStreamEvent)
            assert isinstance(_e.content, str)

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
            "What product categories are we almost always in various stages of transitioning the architecture?"
        ):
            answer += _e.content
        assert any(
            [
                "data center" in answer.lower(),
                "professional visualization" in answer.lower(),
                "gaming" in answer.lower(),
            ]
        )

        # Check that the new stuff is referenced in the last event
        assert _e.references is not None
        assert memory_ids[0] in _e.references.memory_ids
        assert memory_ids[1] in _e.references.memory_ids
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
        assert isinstance(response.content, str)
    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_instructions() -> None:
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant.",
    )
    try:
        response = await assistant.chat.message(
            message="What is 2+2?",
            instructions="Answer only with the number, no additional text.",
        )
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)

        response_value = int(response.content)
        assert response_value == 4
    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_character() -> None:
    # Create a test assistant with a role-playing scenario
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="""
        You are a roleplay assistant. When a character is specified, respond as that character in first person.
        
        Character backgrounds:
        - Brave Knight (Sir Galahad): A noble knight devoted to justice and protecting the innocent. Speaks with honor and chivalry, uses formal language, and always puts duty before self.
        - Wise Wizard (Merlin): An ancient wizard with vast knowledge of magic and the world. Speaks cryptically with wisdom, often references ancient lore, and sees the bigger picture.
        - Evil Sorcerer (Morgoth): A dark sorcerer consumed by power and ambition. Speaks with arrogance and malice, delights in chaos, and seeks to dominate others.
        """,
    )

    try:
        # Test Brave Knight character roleplay
        response = await assistant.chat.message(
            message="What is your name?",
            character="Brave Knight",
        )
        assert isinstance(response, ReferencedMessage)
        knight_response = response.content.lower()
        assert (
            "galahad" in knight_response
        ), f"Knight should identify as Galahad. Got: {response.content}"

        # Test Wise Wizard character roleplay
        response = await assistant.chat.message(
            message="What is your name?",
            character="Wise Wizard",
        )
        assert isinstance(response, ReferencedMessage)
        wizard_response = response.content.lower()
        assert (
            "merlin" in wizard_response
        ), f"Wizard should identify as Merlin. Got: {response.content}"

        # Test Evil Sorcerer character roleplay
        response = await assistant.chat.message(
            message="What is your name?",
            character="Evil Sorcerer",
        )
        assert isinstance(response, ReferencedMessage)
        sorcerer_response = response.content.lower()
        assert (
            "morgoth" in sorcerer_response
        ), f"Sorcerer should identify as Morgoth. Got: {response.content}"

    finally:
        # Remove the test assistant
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_structured_response() -> None:
    # Create a test assistant
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant.",
    )

    try:
        # Create a JSON schema for structured response
        schema = JSONSchema(
            type="object",
            properties={
                "name": JSONSchema(type="string", description="The name of the person"),
                "occupation": JSONSchema(
                    type="string", description="The occupation of the person"
                ),
            },
            required=["name", "occupation"],
            additionalProperties=False,
        )

        response_format = ResponseFormat(
            type="json_schema",
            json_schema=JSONSchemaConfig(
                name="person_info",
                description="Extract person information",
                schema=schema,
            ),
        )

        # Send a message with structured response format
        response = await assistant.chat.message(
            message="My name is Jane Smith and I'm a data scientist.",
            response_format=response_format,
            add_to_memory=False,
        )

        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)
        # The response should be valid JSON
        import json

        parsed_response = json.loads(response.content)
        assert "name" in parsed_response
        assert "occupation" in parsed_response
        assert parsed_response["name"] == "Jane Smith"
        assert "data scientist" in parsed_response["occupation"].lower()

    finally:
        # Remove the test assistant
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_add_get_delete_chat_hisoty() -> None:
    assistant = firedust.assistant.create(f"test-assistant-{random.randint(1, 1000)}")
    try:
        message1 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="John",
            content="Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="Helen",
            content="John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="John",
            content="Sure, the new roadmap is the following...",
            author="user",
        )
        messages = [message1, message2, message3]

        # Add chat history
        assistant.chat.add_history(messages)

        # Test that the history is available in context
        response = assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            chat_group="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.content

        # Get chat history
        history = assistant.chat.get_history(chat_group="product_team")
        history_ids = [message.id for message in history]
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m.id in history_ids for m in messages)

        # Erase chat history
        assistant.chat.erase_history(chat_group="product_team", confirm=True)

        # Check that the history is erased
        history = assistant.chat.get_history(chat_group="product_team")
        assert len(history) == 0
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_add_get_delete_history() -> None:
    assistant = await firedust.assistant.async_create(
        f"test-assistant-{random.randint(1, 1000)}"
    )
    try:
        message1 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="John",
            content="Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="Helen",
            content="John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant=assistant.config.name,
            chat_group="product_team",
            name="John",
            content="Sure, the new roadmap is the following...",
            author="user",
        )
        messages = [message1, message2, message3]

        # Add chat history
        await assistant.chat.add_history(messages)

        # Test that the history is available in context
        response = await assistant.chat.message(
            message="Who is sharing the new product roadmap?",
            chat_group="product_team",  # Previous conversations are available only to the same user
        )
        assert "John" in response.content

        # Get chat history
        history = await assistant.chat.get_history(chat_group="product_team")
        history_ids = [message.id for message in history]
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m.id in history_ids for m in messages)

        # Erase chat history
        await assistant.chat.erase_history(chat_group="product_team", confirm=True)

        # Check that the history is erased
        history = await assistant.chat.get_history(chat_group="product_team")
        assert len(history) == 0
    finally:
        await assistant.delete(confirm=True)
