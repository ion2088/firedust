import json
import re
from datetime import datetime
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator, List, Optional

from firedust.types import (
    AssistantConfig,
    Message,
    MessageStreamEvent,
    ReferencedMessage,
)
from firedust.types.chat import (
    ChatRequest,
    MemoryConfiguration,
    ResponseConfiguration,
    ResponseFormat,
    UserMessage,
)
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Chat:
    """
    A collection of methods to chat with the assistant.
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
        instructions: Optional[str] = None,
        add_to_memory: bool = True,
        use_memory: bool = True,
        response_format: Optional[ResponseFormat] = None,
    ) -> Iterator[MessageStreamEvent]:
        """
        Streams the assistant's response to a message. The assistant uses relevant memories and
        previous conversations to generate a response. Conversations with the given user are private,
        and the assistant does not share the information with other users.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        query = "Summarize the research papers about..."

        for event in assistant.chat.stream(query):
            print(event.content)

        # See which memories the assistant used to generate the response. The references
        # are always provided in the last event of the stream.
        memory_ids = event.references.memory_ids
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            message (str): The message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The username of the user. Defaults to None.
            character (str, optional): The name of the persona the assistant should embody in the response. Defaults to None.
            instructions (str, optional): Additional instructions for this specific request. Defaults to None.
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.
            use_memory (bool, optional): Whether to use memory for generating the response. Defaults to True.
            response_format (ResponseFormat, optional): Structured output configuration. Defaults to None.

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

        # Build the request using the new ChatRequest structure
        chat_request = ChatRequest(
            message=user_message,
            response_config=ResponseConfiguration(
                character=character,
                instructions=instructions,
                response_format=response_format,
            ),
            memory_config=MemoryConfiguration(
                add_to_memory=add_to_memory,
                use_memory=use_memory,
            ),
        )

        try:
            for msg in self.api_client.post_stream(
                "/assistant/chat/stream",
                data=chat_request.model_dump(),
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
        instructions: Optional[str] = None,
        add_to_memory: bool = True,
        use_memory: bool = True,
        response_format: Optional[ResponseFormat] = None,
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
        memory_ids = response.references.memory_ids
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            message (str): The message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The username of the user. Defaults to None.
            character (str, optional): The name of the persona the assistant should embody in the response. Defaults to None.
            instructions (str, optional): Additional instructions for this specific request. Defaults to None.
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.
            use_memory (bool, optional): Whether to use memory for generating the response. Defaults to True.
            response_format (ResponseFormat, optional): Structured output configuration. Defaults to None.

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

        # Build the request using the new ChatRequest structure
        chat_request = ChatRequest(
            message=user_message,
            response_config=ResponseConfiguration(
                character=character,
                instructions=instructions,
                response_format=response_format,
            ),
            memory_config=MemoryConfiguration(
                add_to_memory=add_to_memory,
                use_memory=use_memory,
            ),
        )

        response = self.api_client.post(
            "/assistant/chat/message",
            data=chat_request.model_dump(),
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )
        return ReferencedMessage(**response.json()["data"])

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
            content="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant="ASSISTANT_NAME",
            chat_group="product_team",
            content="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant="ASSISTANT_NAME",
            chat_group="product_team",
            content="John: Sure, the new roadmap is the following...",
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
        Irreversibly delete the chat history of a chat group from the assistant's memory.

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
            print(message.content)
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
        instructions: Optional[str] = None,
        add_to_memory: bool = True,
        use_memory: bool = True,
        response_format: Optional[ResponseFormat] = None,
    ) -> AsyncIterator[MessageStreamEvent]:
        """
        Streams the assistant's response to a message. The assistant uses relevant memories and
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
                print(event.content)

            # See which memories the assistant used to generate the response. The references
            # are always provided in the last event of the stream.
            memory_ids = event.references.memory_ids
            memories = await assistant.memory.get(memory_ids)

        asyncio.run(main())
        ```

        Args:
            message (str): The message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The username of the user. Defaults to None.
            character (str, optional): The name of the persona the assistant should embody in the response. Defaults to None.
            instructions (str, optional): Additional instructions for this specific request. Defaults to None.
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.
            use_memory (bool, optional): Whether to use memory for generating the response. Defaults to True.
            response_format (ResponseFormat, optional): Structured output configuration. Defaults to None.

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

        # Build the request using the new ChatRequest structure
        chat_request = ChatRequest(
            message=user_message,
            response_config=ResponseConfiguration(
                character=character,
                instructions=instructions,
                response_format=response_format,
            ),
            memory_config=MemoryConfiguration(
                add_to_memory=add_to_memory,
                use_memory=use_memory,
            ),
        )

        try:
            async for msg in self.api_client.post_stream(
                "/assistant/chat/stream",
                data=chat_request.model_dump(),
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
        instructions: Optional[str] = None,
        add_to_memory: bool = True,
        use_memory: bool = True,
        response_format: Optional[ResponseFormat] = None,
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
            print(response.content)

            # See which memories the assistant used to generate the response.
            memory_ids = response.references.memory_ids
            memories = await assistant.memory.get(memory_ids)

        asyncio.run(main())
        ```

        Args:
            message (str): The message to send.
            chat_group (str, optional): The unique identifier of the chat group. Defaults to "default".
            username (str, optional): The username of the user. Defaults to None.
            character (str, optional): The name of the persona the assistant should embody in the response. Defaults to None.
            instructions (str, optional): Additional instructions for this specific request. Defaults to None.
            add_to_memory (bool, optional): Whether to add the interaction to memory. Defaults to True.
            use_memory (bool, optional): Whether to use memory for generating the response. Defaults to True.
            response_format (ResponseFormat, optional): Structured output configuration. Defaults to None.

        Returns:
            ReferencedMessage: The response from the assistant.
        """
        user_message = UserMessage(
            assistant=self.config.name,
            chat_group=chat_group,
            name=username,
            content=message,
            timestamp=datetime.now().timestamp(),
        )

        # Build the request using the new ChatRequest structure
        chat_request = ChatRequest(
            message=user_message,
            response_config=ResponseConfiguration(
                character=character,
                instructions=instructions,
                response_format=response_format,
            ),
            memory_config=MemoryConfiguration(
                add_to_memory=add_to_memory,
                use_memory=use_memory,
            ),
        )

        response = await self.api_client.post(
            "/assistant/chat/message",
            data=chat_request.model_dump(),
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )

        return ReferencedMessage(**response.json()["data"])

    async def add_history(self, messages: Iterable[Message]) -> None:
        """
        Adds a chat message history to the assistant's memory, asynchronously. It helps the assistant
        learn from past conversations to improve the quality of responses.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")

            message1 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                content="John: Based on the last discussion, we've made the following changes to the product...",
                author="user",
            )
            message2 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                content="Helen: John, could you please share the updated product roadmap?",
                author="user",
            )
            message3 = Message(
                assistant="ASSISTANT_NAME",
                chat_group="product_team",
                content="John: Sure, the new roadmap is the following...",
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
        Irreversibly delete the chat history of a user from the assistant's memory, asynchronously.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
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
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            history = await assistant.chat.get_history(chat_group="product_team", limit=10)

            for message in history:
                print(message.content)

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
