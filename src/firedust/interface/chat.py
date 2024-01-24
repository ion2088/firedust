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

from typing import Iterator
from uuid import UUID
from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig


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

    def stream(self, message: str, user_id: UUID | None = None) -> Iterator[bytes]:
        """
        Streams a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (str): An optional user id. Defaults to None.
        """

        for msg in self.api_client.get_stream(
            f"assistant/{self.config.id}/chat/stream",
            params={"message": message, "user_id": user_id},
        ):
            yield msg

    def complete(self, message: str, user_id: UUID | None = None) -> str:
        """
        Completes a conversation with the assistant.
        Add a user id to keep chat histories separate for different users.

        Args:
            message (str): The message to send.
            user_id (str): An optional user id. Defaults to None.

        Returns:
            str: The response from the assistant.
        """
        response = self.api_client.get(
            f"assistant/{self.config.id}/chat/complete",
            params={"message": message, "user_id": user_id},
        )

        if response["status_code"] != 200:
            raise Exception(response["message"])

        completion: str = response["completion"]

        return completion
