"""
Chat interface module for the Firedust assistant.

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Stream a conversation with the assistant
    response = assistant.chat.stream("Tell me about the Book of the Dead")

    for msg in response:
        print(msg)

    # Simple chat
    # Send a query and wait for the full response of the assistant
    response = assistant.chat.complete("Tell me about the Book of the Dead")
    print(response)
"""

import json
import re
from datetime import datetime
from typing import Iterable, Iterator
from uuid import uuid4

from firedust._utils.api import APIClient
from firedust._utils.errors import APIError
from firedust._utils.types.api import MessageStreamEvent
from firedust._utils.types.assistant import AssistantConfig, UserMessage


class Chat:
    """
    A collection of methods to chat with the assistant.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Chat class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    def stream(
        self, message: str, user_id: str | None = None
    ) -> Iterator[MessageStreamEvent]:
        """
        Streams a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (str, optional): The unique identifier of the user. Defaults to None.

        Yields:
            Iterator[MessageStreamEvent]: The response from the assistant.
        """
        user_message = UserMessage(
            id=uuid4(),
            assistant_id=self.config.id,
            user_id=user_id,
            message=message,
            timestamp=datetime.now().timestamp(),
        )

        # Processing stream response
        self._previous_stream_chunk = ""

        def _process_stream_chunk(chunk: str) -> Iterable[MessageStreamEvent]:
            chunk_split = re.split(r"\n\ndata: ", chunk)

            # Process each data object in the chunk
            for data in chunk_split:
                if not data:
                    continue

                # Manage incomplete data objects
                if self._previous_stream_chunk:
                    # If the delimiter \n\ndata is present in the combined chunks, it means we have to split and re-process it
                    data = self._previous_stream_chunk + data
                    self._previous_stream_chunk = ""
                    yield from _process_stream_chunk(data)

                # Remove the first "data: " from the first chunk and trailing whitespace
                data = re.sub(r"^data: ", "", data).strip()

                try:
                    data_dict = json.loads(data)
                except json.JSONDecodeError as _:
                    # Probably incomplete data, so we keep it for the next chunk
                    self._previous_stream_chunk = data
                    continue

                yield MessageStreamEvent(**data_dict)

        try:
            for msg in self.api_client.post_stream(
                "/chat/stream",
                data=user_message.model_dump(),
            ):
                msg_decoded = msg.decode("utf-8")
                yield from _process_stream_chunk(msg_decoded)

        except Exception as e:
            raise APIError(f"Failed to stream the conversation: {e}")

    def complete(self, message: str, user_id: str | None = None) -> str:
        """
        Completes a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (str, optional): The unique identifier of the user. Defaults to None.

        Returns:
            str: The response from the assistant.
        """
        user_message = UserMessage(
            id=uuid4(),
            assistant_id=self.config.id,
            user_id=user_id,
            message=message,
            timestamp=datetime.now().timestamp(),
        )

        response = self.api_client.post(
            "/chat/complete",
            data=user_message.model_dump(),
        )
        if not response.is_success:
            raise Exception(response.json()["message"])

        completion: str = response.json()["message"]
        return completion
