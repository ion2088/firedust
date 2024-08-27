import os
import random

import pytest

import firedust
from firedust.types import (
    STRUCTURED_SCHEMA,
    BooleanField,
    CategoryField,
    DictField,
    FloatField,
    ListField,
    Message,
    MessageStreamEvent,
    ReferencedMessage,
    StringField,
    StructuredAssistantMessage,
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
            "What product categories are we almost always in various stages of transitioning the architecture?"
        ):
            answer += _e.message
        assert any(
            [
                "data center" in answer.lower(),
                "professional visualization" in answer.lower(),
                "gaming" in answer.lower(),
            ]
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
            "What product categories are we almost always in various stages of transitioning the architecture?"
        ):
            answer += _e.message
        assert any(
            [
                "data center" in answer.lower(),
                "professional visualization" in answer.lower(),
                "gaming" in answer.lower(),
            ]
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
    assistant = firedust.assistant.create(f"test-assistant-{random.randint(1, 1000)}")
    try:
        message1 = Message(
            assistant=assistant.config.name,
            user="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant=assistant.config.name,
            user="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant=assistant.config.name,
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
    assistant = await firedust.assistant.async_create(
        f"test-assistant-{random.randint(1, 1000)}"
    )
    try:
        message1 = Message(
            assistant=assistant.config.name,
            user="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant=assistant.config.name,
            user="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant=assistant.config.name,
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


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_structured_simple() -> None:
    assistant = firedust.assistant.create(f"test-assistant-{random.randint(1, 1000)}")
    schema: STRUCTURED_SCHEMA = {
        "name": StringField(hint="The name of the person."),
        "occupation": StringField(hint="The occupation of the person."),
    }

    try:
        response = assistant.chat.structured(
            message="My name is John Doe and I'm a software engineer.",
            user="test_user",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.message.keys()
        assert isinstance(response.message["name"], str)
        assert response.message["name"] == "John Doe"
        assert isinstance(response.message["occupation"], str)
        assert response.message["occupation"] == "software engineer"

    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_chat_structured_simple() -> None:
    assistant = await firedust.assistant.async_create(
        f"test-assistant-{random.randint(1, 1000)}"
    )
    schema: STRUCTURED_SCHEMA = {
        "name": StringField(hint="The name of the person."),
        "occupation": StringField(hint="The occupation of the person."),
    }

    try:
        response = await assistant.chat.structured(
            message="My name is Jane Smith and I'm a data scientist.",
            user="test_user",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.message.keys()
        assert isinstance(response.message["name"], str)
        assert response.message["name"] == "Jane Smith"
        assert isinstance(response.message["occupation"], str)
        assert response.message["occupation"] == "data scientist"

    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_structured_complex_message() -> None:
    data = """
        From Gulfstream business jets and combat vehicles to nuclear-powered submarines and communications systems, people around the world depend on our products and services for their safety and security.
        We offer a broad portfolio of innovative products and services in business aviation; combat vehicles, weapons systems and munitions; IT and C4ISR solutions; and shipbuilding and ship repair.
        General Dynamics is organized into four business groups: Aerospace, Marine Systems, Combat Systems and Technologies.
        We have a balanced business model which gives each business unit the flexibility to stay agile and maintain an intimate understanding of customer requirements.
        Each business unit is responsible for the execution of its strategy and operational performance. Our corporate leaders set the overall strategy of the business and manage allocation of capital. This unique model keeps us focused on what matters — delivering on our promises to customers through relentless improvement, continued growth, boosting return on invested capital and disciplined capital deployment.
        
        Our Ethos
        Each of us has an obligation to behave according to our values. In that way, we can ensure that we continue to be good stewards of the investments in us by our shareholders, customers, employees and communities, now and in the future.
        
        Leadership
        General Dynamics employs thousands of people across the globe, with locations in more than 45 countries. We rely on the skills of our employees and their knowledge of customer requirements to deliver best-in-class products and services.
        
        Our History
        General Dynamics employees have pushed the boundaries by embracing change for more than 65 years. We draw on this rich history of service to the aerospace and defense communities and an agile culture of continuous improvement to create ever-growing value for our customers.
        
        Responsibility
        Our set of values inform our commitment to good corporate citizenship, sustainable business practices and community support. We pride ourselves on our responsible and ethical practices.
        """

    assistant = firedust.assistant.create(f"test-assistant-{random.randint(1, 1000)}")
    schema: STRUCTURED_SCHEMA = {
        "company": DictField(
            hint="The details of the company.",
            items={
                "name": StringField(hint="The name of the company."),
                "description": StringField(hint="A brief description of the company."),
                "values": DictField(
                    hint="The values of the company.",
                    items={
                        "name": StringField(hint="The name of the value."),
                        "description": StringField(
                            hint="A brief description of the value."
                        ),
                    },
                ),
            },
        ),
        "products": ListField(
            hint="The products and services offered by the company.",
            items=StringField(hint="The product or service name."),
        ),
        "industry": CategoryField(
            hint="The industry of the company.",
            categories=[
                "agriculture",
                "defense",
                "chemicals",
                "energy",
            ],
        ),
        "weapons": BooleanField(hint="Whether the company produces weapons."),
        "employees": FloatField(
            hint="The estimated number of employees, assumed from context."
        ),
    }

    try:
        response = assistant.chat.structured(
            message=f"Extract information from the text: {data}",
            user="product_team",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.message.keys()

        assert isinstance(response.message["company"], dict)
        assert isinstance(response.message["company"]["name"], str)
        assert response.message["company"]["name"].lower() == "general dynamics"

        assert isinstance(response.message["products"], list)
        assert all(isinstance(product, str) for product in response.message["products"])

        assert isinstance(response.message["industry"], str)
        assert "defense" == response.message["industry"].lower()

        assert isinstance(response.message["weapons"], bool)
        assert response.message["weapons"] is True

        assert isinstance(response.message["employees"], float)

    finally:
        assistant.delete(confirm=True)
