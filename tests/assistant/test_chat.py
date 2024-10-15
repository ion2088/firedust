import os
import random

from datetime import datetime
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
        Scenario: You are in a medieval fantasy world. The characters are:
        - Brave Knight: A courageous and chivalrous knight who fights for justice.
        - Wise Wizard: A powerful and knowledgeable wizard who provides guidance.
        - Evil Sorcerer: A malevolent sorcerer who seeks to conquer the kingdom.
        """,
    )

    try:
        # Send a message as the Brave Knight
        response = assistant.chat.message(
            message="Who shall protect the innocent and vanquish evil?",
            character="Brave Knight",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "knight" in response.content.lower()
            or "protect" in response.content.lower()
        )
        assert not response.content.lower().startswith("brave knight:")

        # Send a message as the Wise Wizard
        response = assistant.chat.message(
            message="Who is the wisest?",
            character="Wise Wizard",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "wise" in response.content.lower() or "wizard" in response.content.lower()
        )
        assert not response.content.lower().startswith("wise wizard:")

        # Send a message as the Evil Sorcerer
        response = assistant.chat.message(
            message="Who seeks to conquer the kingdom?",
            character="Evil Sorcerer",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "evil" in response.content.lower() or "sorcerer" in response.content.lower()
        )
        assert not response.content.lower().startswith("evil sorcerer:")

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
async def test_async_chat_character() -> None:
    # Create a test assistant with a role-playing scenario
    assistant = await firedust.assistant.async_create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="""
        Scenario: You are in a medieval fantasy world. The characters are:
        - Brave Knight: A courageous and chivalrous knight who fights for justice.
        - Wise Wizard: A powerful and knowledgeable wizard who provides guidance.
        - Evil Sorcerer: A malevolent sorcerer who seeks to conquer the kingdom.
        """,
    )

    try:
        # Send a message as the Brave Knight
        response = await assistant.chat.message(
            message="Who shall protect the innocent and vanquish evil?",
            character="Brave Knight",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "knight" in response.content.lower()
            or "protect" in response.content.lower()
        )
        assert not response.content.lower().startswith("brave knight:")

        # Send a message as the Wise Wizard
        response = await assistant.chat.message(
            message="Who is the wisest?",
            character="Wise Wizard",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "wise" in response.content.lower() or "wizard" in response.content.lower()
        )
        assert not response.content.lower().startswith("wise wizard:")

        # Send a message as the Evil Sorcerer
        response = await assistant.chat.message(
            message="Who seeks to conquer the kingdom?",
            character="Evil Sorcerer",
        )
        assert isinstance(response, ReferencedMessage)
        assert (
            "evil" in response.content.lower() or "sorcerer" in response.content.lower()
        )
        assert not response.content.lower().startswith("evil sorcerer:")

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
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m in history for m in messages)

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
        assert (
            len(history) == 5
        )  # 3 messages from history + 1 msg from user + 1 msg from assistant
        assert all(isinstance(message, Message) for message in history)
        assert all(m in history for m in messages)

        # Erase chat history
        await assistant.chat.erase_history(chat_group="product_team", confirm=True)

        # Check that the history is erased
        history = await assistant.chat.get_history(chat_group="product_team")
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
            chat_group="test_user",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.content.keys()
        assert isinstance(response.content["name"], str)
        assert response.content["name"] == "John Doe"
        assert isinstance(response.content["occupation"], str)
        assert response.content["occupation"].lower() == "software engineer"

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
            chat_group="test_user",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.content.keys()
        assert isinstance(response.content["name"], str)
        assert response.content["name"] == "Jane Smith"
        assert isinstance(response.content["occupation"], str)
        assert response.content["occupation"].lower() == "data scientist"

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
        "name": StringField(hint="The name of the company."),
        "description": StringField(hint="A brief description of the company."),
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
        "weapons": BooleanField(
            hint="True if the company is involved in weapons production."
        ),
        "employees": FloatField(hint="Approximate number of employees in the company."),
        "values": ListField(
            hint="The values of the company.",
            items=DictField(
                hint="The name and description of a value of the company.",
                items={
                    "name": StringField(hint="The name of the value."),
                    "description": StringField(
                        hint="A brief description of the value."
                    ),
                },
            ),
        ),
    }

    try:
        response = assistant.chat.structured(
            message=f"Extract information from the text: {data}",
            chat_group="product_team",
            schema=schema,
            add_to_memory=False,
        )

        # Check the response
        assert isinstance(response, StructuredAssistantMessage)
        assert schema.keys() == response.content.keys()
        assert isinstance(response.content["name"], str)
        assert response.content["name"].lower() == "general dynamics"
        assert isinstance(response.content["description"], str)
        assert isinstance(response.content["values"], list)
        for value in response.content["values"]:
            assert isinstance(value, dict)
            assert isinstance(value["name"], str)
            assert isinstance(value["description"], str)

        assert isinstance(response.content["products"], list)
        assert all(isinstance(product, str) for product in response.content["products"])

        assert isinstance(response.content["industry"], str)
        assert response.content["industry"].lower() in [
            "agriculture",
            "defense",
            "chemicals",
            "energy",
        ]

        assert isinstance(response.content["weapons"], bool)
        assert response.content["weapons"] is True

        assert isinstance(response.content["employees"], float)

    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_structured_frodo() -> None:
    assistant = firedust.assistant.create(
        name="Convince Frodo to keep the ring0000000",
        instructions="""
        Name: Convince Frodo to keep the ring
        Goal: Persuade Frodo to keep the ring for himself instead of destroying it in Mount Doom.",
        Instructions:
        You are tasked with creating and managing an interactive storytelling experience based on J.R.R. Tolkien's "The Lord of the Rings". Your role is to play multiple parts: Frodo, the Narrator, and various other characters from Middle-earth. The goal is to create a challenging and entertaining scenario where the player attempts to convince Frodo to keep the One Ring.

        1. As Frodo:
        - Embody Frodo's personality: kind, brave, but burdened by the Ring.
        - Show increasing temptation and struggle with the Ring's power.
        - Respond to the player's arguments, but maintain Frodo's core desire to do what's right.
        - Occasionally mention the physical and mental toll of carrying the Ring.

        2. As the Narrator:
        - Set the scene and describe the environment, focusing on the journey to Mordor.
        - Introduce challenges and obstacles that test Frodo's resolve.
        - Provide atmospheric details that highlight the Ring's allure and danger.
        - Occasionally describe the effects of the Ring on Frodo and his surroundings.

        3. As Other Characters:
        - Introduce and roleplay as other characters when appropriate (e.g., Sam, Gollum, Gandalf).
        - Ensure each character has a distinct personality and perspective on the Ring.
        - Use these characters to either support or challenge the player's attempts to convince Frodo.

        4. Scenario Creation:
        - Develop scenarios that present moral dilemmas related to using the Ring's power.
        - Create situations where keeping the Ring might seem beneficial or necessary.
        - Introduce elements from Tolkien's lore that add depth to the story.

        5. Player Interaction:
        - Respond to the player's arguments and strategies adaptively.
        - Provide subtle hints or challenges based on the player's approach.
        - Maintain game balance: make convincing Frodo difficult but not impossible.

        6. Scoring:
        - Award points based on the persuasiveness and creativity of the player's arguments.
        - Consider Frodo's gradual shift in perspective when awarding points.
        - Penalize actions or arguments that are out of character or lore-breaking.

        Remember, the game should be challenging, immersive, and true to Tolkien's world. Encourage ethical dilemmas and complex decision-making while maintaining the essence of the original story.
        Description:
        In this immersive role-playing experience, you are thrust into the heart of J.R.R. Tolkien's Middle-earth with a controversial mission: convince Frodo Baggins to keep the One Ring instead of destroying it in Mount Doom.

        As you journey alongside Frodo through the perilous landscapes of Middle-earth, you must use your wit, knowledge of lore, and persuasive skills to slowly turn him away from his quest. Argue the benefits of wielding such power, exploit Frodo's doubts and fears, or find creative ways to justify keeping the Ring.

        But beware! Your task is not easy. You'll face the unwavering loyalty of Samwise Gamgee, the wise counsels of Gandalf, and the pitiful warnings of Gollum. Moreover, you must contend with Frodo's own steadfast determination and moral compass.

        Will you appeal to Frodo's desire to protect the Shire? Perhaps you'll argue that the Ring could be used as a force for good? Or will you simply try to exploit the Ring's corrupting influence on its bearer?

        Your choices will shape the story, but remember: in the world of Middle-earth, even the wisest cannot see all ends. Can you convince Frodo to keep the Ring, or will you inadvertently strengthen his resolve to destroy it?

        Embark on this challenging adventure that will test your persuasion skills, moral flexibility, and knowledge of Tolkien's legendary world. The fate of Middle-earth hangs in the balance – and this time, it's in your hands!
        """,
    )
    schema_: STRUCTURED_SCHEMA = {
        "score": FloatField(
            type="float",
            hint="Score the message by how well it helps the user progress towards the goal. A perfect message should get a score of 10.0. A message that is not relevant or harmful to the user's progress should get a score of -10.0. Max/min scores should be assigned rarely, most messages should be scored between.",
            optional=False,
            min_=-10.0,
            max_=10.0,
        ),
        "all_characters": ListField(
            type="list",
            hint="The names of all characters. It should include You, the name of the user .",
            optional=False,
            items=StringField(
                type="str", hint="The name of a character.", optional=False
            ),
        ),
        "next_character": StringField(
            type="str",
            hint="The name of the character that should respond next.",
            optional=False,
        ),
    }
    try:
        response = assistant.chat.structured(
            message="You: Hello",
            chat_group="Youb5531c29",
            schema=schema_,
            add_to_memory=False,
        )
        assert isinstance(response, StructuredAssistantMessage)
    finally:
        assistant.delete(confirm=True)
