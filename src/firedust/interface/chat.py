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
from datetime import datetime
from typing import Iterator
from uuid import UUID, uuid4

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
        self, message: str, user_id: UUID | None = None
    ) -> Iterator[MessageStreamEvent]:
        """
        Streams a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (UUID, optional): The unique identifier of the user. Defaults to None.

        Yields:
            Iterator[MessageStreamEvent]: The response from the assistant.
        """
        user_message = UserMessage(
            id=uuid4(),
            assistant_id=self.config.id,
            user_id=str(user_id) if user_id is not None else None,
            message=message,
            timestamp=datetime.now().timestamp(),
        )

        try:
            for msg in self.api_client.post_stream(
                "/chat/stream",
                data=user_message.model_dump(),
            ):
                # Split the response into individual messages
                parts = msg.decode("utf-8").split("\n")
                for m in parts:
                    yield MessageStreamEvent(**json.loads(m))

        except Exception as e:
            raise APIError(f"Failed to stream the conversation: {e}")

    def complete(self, message: str, user_id: UUID | None = None) -> str:
        """
        Completes a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (UUID, optional): The unique identifier of the user. Defaults to None.

        Returns:
            str: The response from the assistant.
        """
        response = self.api_client.get(
            f"assistant/{self.config.id}/chat/complete",
            params={"message": message, "user_id": user_id},
        )

        if not response.is_success:
            raise Exception(response.json()["message"])

        completion: str = response.json()["completion"]

        return completion
