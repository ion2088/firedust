"""
firedust.assistant.chat
~~~~~~~~~~~~~~~~~~~~~~~

A collection of methods to chat with the assistant.
"""

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from typing import Iterator


class Chat:
    """
    A collection of methods to chat with the assistant.

    To chat with the assistant, you can use the following methods:

        response = assistant.chat.stream("Hello")

        for msg in response:
            print(msg)
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

    def stream(self, message: str) -> Iterator[bytes]:
        """
        Streams a conversation with the assistant.
        """

        for msg in self.api_client.get_stream(
            f"assistant/{self.config.id}/chat/stream", params={"message": message}
        ):
            yield msg
