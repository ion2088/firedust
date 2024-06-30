import json
import re
from datetime import datetime
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator

from firedust.types import (
    AssistantConfig,
    Message,
    MessageStreamEvent,
    ReferencedMessage,
)
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
        self, message: str, user: str = "default"
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
        user_message = _create_user_message(self.config.name, message, user)
        try:
            for msg in self.api_client.post_stream(
                "/assistant/chat/stream", data=user_message.model_dump()
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

    def message(self, message: str, user: str = "default") -> ReferencedMessage:
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
        print(response.message)

        # See which memories the assistant used to generate the response.
        memory_ids = response.references.memories
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Returns:
            ReferencedMessage: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        response = self.api_client.post(
            "/assistant/chat/message", data=user_message.model_dump()
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )
        return ReferencedMessage(**response.json()["data"])


class AsyncChat:
    """
    A collection of asynchronous methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client
        self._previous_stream_chunk = ""

    async def stream(
        self, message: str, user: str = "default"
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
        user_message = _create_user_message(self.config.name, message, user)
        try:
            async for msg in self.api_client.post_stream(
                "/assistant/chat/stream", data=user_message.model_dump()
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

    async def message(self, message: str, user: str = "default") -> ReferencedMessage:
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
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Returns:
            str: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        response = await self.api_client.post(
            "/assistant/chat/message", data=user_message.model_dump()
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to send the message: {response.text}",
            )

        return ReferencedMessage(**response.json()["data"])


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
        # if not data:
        #     continue
        if previous_chunk:
            data = previous_chunk + data
            previous_chunk = ""
        data = re.sub(r"^data: ", "", data).strip()
        try:
            yield MessageStreamEvent(**json.loads(data))
        except json.JSONDecodeError:
            previous_chunk = data


def _create_user_message(config_name: str, message: str, user: str) -> Message:
    """
    Create a UserMessage object.

    Args:
        config_name (str): The name of the assistant configuration.
        message (str): The message to send.
        user (str): The unique identifier of the user.

    Returns:
        UserMessage: The created user message.
    """
    return Message(
        assistant=config_name,
        user=user,
        message=message,
        timestamp=datetime.now().timestamp(),
        author="user",
    )
