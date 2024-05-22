"""
Chat interface module for the Firedust assistant.

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_NAME")

    # Stream a conversation with the assistant
    response = assistant.chat.stream("Tell me about the Book of the Dead")

    for e in response:
        print(e.message)

    # Simple chat
    # Send a query and wait for the full response of the assistant
    response = assistant.chat.complete("Tell me about the Book of the Dead")
    print(response)
"""

import json
import re
from datetime import datetime
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator

from firedust.types.api import MessagePayload, MessageStreamEvent
from firedust.types.assistant import AssistantConfig, UserMessage
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Chat:
    """
    A collection of synchronous methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Chat class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The synchronous API client.
        """
        self.config = config
        self.api_client = api_client
        self._previous_stream_chunk = ""

    def stream(
        self, message: str, user: str = "default"
    ) -> Iterator[MessageStreamEvent]:
        """
        Streams an assistant response to a message.

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Yields:
            MessageStreamEvent: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        try:
            for msg in self.api_client.post_stream(
                "/chat/stream", data=user_message.model_dump()
            ):
                msg_decoded = msg.decode("utf-8")
                for event in _process_stream_chunk(
                    msg_decoded, self._previous_stream_chunk
                ):
                    yield event
        except Exception as e:
            raise APIError(f"Failed to stream the conversation: {e}")
        finally:
            self._previous_stream_chunk = ""

    def message(self, message: str, user: str = "default") -> MessagePayload:
        """
        Returns a response from the assistant to a message.

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Returns:
            MessagePayload: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        response = self.api_client.post("/chat/message", data=user_message.model_dump())
        if not response.is_success:
            raise APIError(response.json())
        return MessagePayload(**response.json()["data"])


class AsyncChat:
    """
    A collection of asynchronous methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncChat class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The asynchronous API client.
        """
        self.config = config
        self.api_client = api_client
        self._previous_stream_chunk = ""

    async def stream(
        self, message: str, user: str = "default"
    ) -> AsyncIterator[MessageStreamEvent]:
        """
        Streams an assistant response to a message.

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Yields:
            MessageStreamEvent: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        try:
            async for msg in self.api_client.post_stream(
                "/chat/stream", data=user_message.model_dump()
            ):
                msg_decoded = msg.decode("utf-8")
                async for event in _async_process_stream_chunk(
                    msg_decoded, self._previous_stream_chunk
                ):
                    yield event
        except Exception as e:
            raise APIError(f"Failed to stream the conversation: {e}")
        finally:
            self._previous_stream_chunk = ""

    async def message(self, message: str, user: str = "default") -> MessagePayload:
        """
        Returns a response from the assistant to a message.

        Args:
            message (str): The message to send.
            user (str, optional): The unique identifier of the user. Defaults to "default".

        Returns:
            str: The response from the assistant.
        """
        user_message = _create_user_message(self.config.name, message, user)
        response = await self.api_client.post(
            "/chat/message", data=user_message.model_dump()
        )
        if not response.is_success:
            raise APIError(response.json())
        return MessagePayload(**response.json()["data"])


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
        if not data:
            continue
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
        if not data:
            continue
        if previous_chunk:
            data = previous_chunk + data
            previous_chunk = ""
        data = re.sub(r"^data: ", "", data).strip()
        try:
            yield MessageStreamEvent(**json.loads(data))
        except json.JSONDecodeError:
            previous_chunk = data


def _create_user_message(config_name: str, message: str, user: str) -> UserMessage:
    """
    Create a UserMessage object.

    Args:
        config_name (str): The name of the assistant configuration.
        message (str): The message to send.
        user (str): The unique identifier of the user.

    Returns:
        UserMessage: The created user message.
    """
    return UserMessage(
        assistant=config_name,
        user=user,
        message=message,
        timestamp=datetime.now().timestamp(),
    )
