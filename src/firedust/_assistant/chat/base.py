import json
import re
from datetime import datetime
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator, List, Optional

from firedust.types import (
    STRUCTURED_SCHEMA,
    AssistantConfig,
    Message,
    MessageStreamEvent,
    ReferencedMessage,
    StructuredAssistantMessage,
    StructuredUserMessage,
)
from firedust.types.chat import UserMessage
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Chat:
    """
    A collection of asynchronous methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client
        self._previous_stream_chunk = ""

    def stream(
        self,
        message: str,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> Iterator[MessageStreamEvent]:
        """
        Streams the assistant's response to a message. The assistants uses relevant memories and
        previous conversations to generate a response. Conversations with the given user are private,
        and the assistant does not share the information with other users.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        query = "Summarize the research papers about..."

        for event in assistant.chat.stream(query):
            print(event.message)

        # See which memories the assistant used to generate the response. The references
        # are always provided in the last event of the stream.
        memory_ids = event.references.memories
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Yields:
            MessageStreamEvent: The response from the assistant.
        """
        user_message = UserMessage(
            assistant=self.config.name,
            name=username,
            content=message,
            chat_group=chat_group,
            timestamp=datetime.now().timestamp(),
        )
        try:
            for msg in self.api_client.post_stream(
                "/assistant/chat/stream",
                data={
                    "message": user_message.model_dump(),
                    "response_config": {
                        "character": character,
                    },
                    "add_to_memory": add_to_memory,
                },
            ):
                msg_decoded = msg.decode("utf-8")
                for event in _process_stream_chunk(
                    msg_decoded, self._previous_stream_chunk
                ):
                    yield event
        except Exception as e:
            raise APIError(
                code=500,
                message=f"Failed to stream conversation: {e}",
            )
        finally:
            self._previous_stream_chunk = ""

    def message(
        self,
        message: str,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> ReferencedMessage:
        """
        Returns a full response from the assistant to a message. It takes longer to get a response
        compared to the stream method because the assistant processes the entire message before
        responding. The assistant uses relevant memories and previous conversations to generate a
        response. Conversations with the given user are private, and the assistant does not share the
        information with other users.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        query = "Summarize the research papers about..."

        response = assistant.chat.message(query)
        print(response.content)

        # See which memories the assistant used to generate the response.
        memory_ids = response.references.memories
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            content (str): The content of the message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The username of the user. Defaults to None.
            character (str, optional): The name of the persona the assistant should embody in the response. Defaults to None.

        Returns:
            ReferencedMessage: The response from the assistant.
        """
        user_message = UserMessage(
            assistant=self.config.name,
            name=username,
            content=message,
            chat_group=chat_group,
            timestamp=datetime.now().timestamp(),
        )

        response = self.api_client.post(
            "/assistant/chat/message",
            data={
                "message": user_message.model_dump(),
                "response_config": {
                    "character": character,
                },
                "add_to_memory": add_to_memory,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )
        return ReferencedMessage(**response.json()["data"])

    def structured(
        self,
        message: str,
        schema: STRUCTURED_SCHEMA,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> StructuredAssistantMessage:
        """
        Returns a json response that is structured based on the given schema.

        Example:
        ```python
        import firedust
        from firedust.types import ...

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        schema: STRUCTURED_SCHEMA = {
            "name": StringField(hint="The name of the person."),
            "occupation": StringField(hint="The occupation of the person."),
        }
        response = assistant.chat.structured(
            message="My name is John Doe and I'm a software engineer.",
            user="test_user",
            schema=schema,
        )
        print(response.message)
        ```

        Args:
            message (str): The message to send.
            schema (STRUCTURED_SCHEMA): The schema to structure the response.
            user (str, optional): The unique identifier of the user. Defaults to "default".
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.

        Returns:
            StructuredAssistantMessage: The structured response from the assistant.
        """
        user_message = StructuredUserMessage(
            assistant=self.config.name,
            chat_group=chat_group,
            name=username,
            content=message,
            schema_=schema,
            timestamp=datetime.now().timestamp(),
        )
        response = self.api_client.post(
            "/assistant/chat/structured",
            data={
                "add_to_memory": add_to_memory,
                "message": {**user_message.model_dump()},
                "response_config": {
                    "character": character,
                },
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )

        return StructuredAssistantMessage(**response.json()["data"])

    def add_history(self, messages: Iterable[Message]) -> None:
        """
        Adds chat message history. It will become available for the assistant to
        learn from past conversations to improve the quality of responses.

        Example:
        ```python
        import firedust
        from firedust.types import Message

        assistant = firedust.assistant.load("ASSISTANT_NAME")

        message1 = Message(
            assistant="ASSISTANT_NAME",
            chat_group="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant="ASSISTANT_NAME",
            chat_group="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant="ASSISTANT_NAME",
            chat_group="product_team",
            message="John: Sure, the new roadmap is the following...",
            author="user",
        )

        assistant.chat.add_history([message1, message2, message3])
        ```

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = self.api_client.put(
            "/assistant/chat/history",
            data={
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add chat history: {response.text}",
            )

    def erase_history(self, chat_group: str, confirm: bool = False) -> None:
        """
        Irreversebly delete the chat history of a chat group from the assistant's memory.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.chat.erase_history(chat_group="product_team", confirm=True)
        ```

        Args:
            chat_group (str): The unique identifier of the chat group.
            confirm (bool): Confirm the deletion. Defaults to False.
        """
        if confirm is False:
            raise ValueError("Please confirm the deletion by setting confirm=True")

        response = self.api_client.delete(
            "/assistant/chat/history",
            params={
                "assistant": self.config.name,
                "chat_group": chat_group,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to erase chat history: {response.text}",
            )

    def get_history(
        self, chat_group: str, limit: int = 25, offset: int = 0
    ) -> List[Message]:
        """
        Get the chat history of a user from the assistant's memory.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        history = assistant.chat.get_history(chat_group="product_team", limit=10)

        for message in history:
            print(message.message)
        ```

        Args:
            chat_group (str): The unique identifier of the chat group.
            limit (int): The maximum number of messages to return. Defaults to 25.
            offset (int): The number of messages to skip. Defaults to 0.

        Returns:
            List[Message]: The chat history of the user
        """
        response = self.api_client.get(
            "/assistant/chat/history",
            params={
                "assistant": self.config.name,
                "chat_group": chat_group,
                "limit": limit,
                "offset": offset,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to get chat history: {response.text}",
            )

        return [Message(**msg) for msg in response.json()["data"]]


class AsyncChat:
    """
    A collection of asynchronous methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client
        self._previous_stream_chunk = ""

    async def stream(
        self,
        message: str,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> AsyncIterator[MessageStreamEvent]:
        """
        Streams the assistant's response to a message. The assistants uses relevant memories and
        previous conversations to generate a response. Conversations with the given user are private and
        are not shared with other users.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            query = "Summarize the research papers about..."

            async for event in assistant.chat.stream(query):
                print(event.message)

            # See which memories the assistant used to generate the response. The references
            # are always provided in the last event of the stream.
            memory_ids = event.references.memories
            memories = await assistant.memory.async_get(memory_ids)

        asyncio.run(main())
        ```

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Yields:
            MessageStreamEvent: The response from the assistant.
        """
        user_message = UserMessage(
            assistant=self.config.name,
            chat_group=chat_group,
            name=username,
            content=message,
            timestamp=datetime.now().timestamp(),
        )
        try:
            async for msg in self.api_client.post_stream(
                "/assistant/chat/stream",
                data={
                    "message": user_message.model_dump(),
                    "response_config": {
                        "character": character,
                    },
                    "add_to_memory": add_to_memory,
                },
            ):
                msg_decoded = msg.decode("utf-8")
                async for event in _async_process_stream_chunk(
                    msg_decoded, self._previous_stream_chunk
                ):
                    yield event
        except Exception as e:
            raise APIError(
                code=500,
                message=f"Failed to stream the conversation: {e}",
            )
        finally:
            self._previous_stream_chunk = ""

    async def message(
        self,
        message: str,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> ReferencedMessage:
        """
        Returns a full response from the assistant to a message. It takes longer to get a response
        compared to the stream method because the assistant processes the entire message before
        responding. The assistant uses relevant memories and previous conversations to generate a
        response. Conversations with the given user are private and are not shared with other users.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            query = "Summarize the research papers about..."

            response = await assistant.chat.message(query)
            print(response.message)

            # See which memories the assistant used to generate the response.
            memory_ids = response.references.memories
            memories = await assistant.memory.async_get(memory_ids)

        asyncio.run(main())
        ```

        Args:
            message (str): The message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The unique identifier of the user. Defaults to "default".
            character (str, optional): The character of the assistant. Defaults to "default".
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.

        Returns:
            str: The response from the assistant.
        """
        user_message = UserMessage(
            assistant=self.config.name,
            chat_group=chat_group,
            name=username,
            content=message,
            timestamp=datetime.now().timestamp(),
        )
        response = await self.api_client.post(
            "/assistant/chat/message",
            data={
                "message": {**user_message.model_dump()},
                "response_config": {
                    "character": character,
                },
                "add_to_memory": add_to_memory,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )

        return ReferencedMessage(**response.json()["data"])

    async def structured(
        self,
        message: str,
        schema: STRUCTURED_SCHEMA,
        chat_group: str = "default",
        username: Optional[str] = None,
        character: Optional[str] = None,
        add_to_memory: bool = True,
    ) -> StructuredAssistantMessage:
        """
        Returns a json response that is structured based on the given schema, asynchronously.

        Example:
        ```python
        import firedust
        from firedust.types import STRUCTURED_SCHEMA, StringField
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            schema: STRUCTURED_SCHEMA = {
                "name": StringField(hint="The name of the person."),
                "occupation": StringField(hint="The occupation of the person."),
            }
            message = "My name is John Doe and I'm a software engineer."

            response = await assistant.chat.structured(message, schema)
            print(response.message)

        asyncio.run(main())
        ```

        Args:
            message (str): The message to send.
            schema (STRUCTURED_SCHEMA): The schema to structure the response.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The unique identifier of the user. Defaults to "default".
            character (str, optional): The character of the assistant. Defaults to "default".
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.

        Returns:
            StructuredAssistantMessage: The structured response from the assistant.
        """
        user_message = StructuredUserMessage(
            assistant=self.config.name,
            chat_group=chat_group,
            name=username,
            content=message,
            schema_=schema,
            timestamp=datetime.now().timestamp(),
        )
        response = await self.api_client.post(
            "/assistant/chat/structured",
            data={
                "add_to_memory": add_to_memory,
                "message": {**user_message.model_dump()},
                "response_config": {
                    "character": character,
                },
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )

        return StructuredAssistantMessage(**response.json()["data"])

    async def add_history(self, messages: Iterable[Message]) -> None:
        """
        Adds a chat message history to the assistant's memory, asynchronously. It helps the assistant
        learn from past conversations to improve the quality of responses.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")

            message1 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                message="John: Based on the last discussion, we've made the following changes to the product...",
                author="user",
            )
            message2 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                message="Helen: John, could you please share the updated product roadmap?",
                author="user",
            )
            message3 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                message="John: Sure, the new roadmap is the following...",
                author="user",
            )

            await assistant.chat.add_history([message1, message2, message3])

        asyncio.run(main())
        ```

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = await self.api_client.put(
            "/assistant/chat/history",
            data={
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add chat history: {response.text}",
            )

    async def erase_history(
        self,
        chat_group: str = "default",
        confirm: bool = False,
    ) -> None:
        """
        Irreversebly delete the chat history of a user from the assistant's memory, asynchronously.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            await assistant.chat.erase_history(chat_group="product_team", confirm=True)

        asyncio.run(main())
        ```

        Args:
            chat_group (str): The unique identifier of the chat group. Defaults to "default".
            confirm (bool): Confirm the deletion. Defaults to False.
        """
        if confirm is False:
            raise ValueError("Please confirm the deletion by setting confirm=True")

        response = await self.api_client.delete(
            "/assistant/chat/history",
            params={
                "assistant": self.config.name,
                "chat_group": chat_group,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to erase chat history: {response.text}",
            )

    async def get_history(
        self,
        chat_group: str = "default",
        limit: int = 25,
        offset: int = 0,
    ) -> List[Message]:
        """
        Get the chat history of a user from the assistant's memory, asynchronously.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            history = await assistant.chat.get_history(chat_group="product_team", limit=10)

            for message in history:
                print(message.message)

        asyncio.run(main())
        ```

        Args:
            chat_group (str): The unique identifier of the chat group. Defaults to "default".
            limit (int): The maximum number of messages to return. Defaults to 25.
            offset (int): The number of messages to skip. Defaults to 0.

        Returns:
            List[Message]: The chat history of the user
        """
        response = await self.api_client.get(
            "/assistant/chat/history",
            params={
                "assistant": self.config.name,
                "chat_group": chat_group,
                "limit": limit,
                "offset": offset,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to get chat history: {response.text}",
            )

        return [Message(**msg) for msg in response.json()["data"]]


def _process_stream_chunk(
    chunk: str, previous_chunk: str
) -> Iterable[MessageStreamEvent]:
    """
    Process a chunk of streamed data and yield MessageStreamEvent objects.

    Args:
        chunk (str): The current chunk of data.
        previous_chunk (str): The previous chunk of data, in case of incomplete data.

    Yields:
        MessageStreamEvent: The processed event from the data chunk.
    """
    chunk_split = re.split(r"\n\ndata: ", chunk)
    for data in chunk_split:
        if previous_chunk:
            data = previous_chunk + data
            previous_chunk = ""
        data = re.sub(r"^data: ", "", data).strip()
        try:
            yield MessageStreamEvent(**json.loads(data))
        except json.JSONDecodeError:
            previous_chunk = data


async def _async_process_stream_chunk(
    chunk: str, previous_chunk: str
) -> AsyncIterable[MessageStreamEvent]:
    """
    Asynchronously process a chunk of streamed data and yield MessageStreamEvent objects.

    Args:
        chunk (str): The current chunk of data.
        previous_chunk (str): The previous chunk of data, in case of incomplete data.

    Yields:
        MessageStreamEvent: The processed event from the data chunk.
    """
    chunk_split = re.split(r"\n\ndata: ", chunk)
    for data in chunk_split:
        if previous_chunk:
            data = previous_chunk + data
            previous_chunk = ""
        data = re.sub(r"^data: ", "", data).strip()
        try:
            yield MessageStreamEvent(**json.loads(data))
        except json.JSONDecodeError:
            previous_chunk = data
