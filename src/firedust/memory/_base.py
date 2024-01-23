from typing import List

from firedust._utils.api import APIClient
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.memory import MemoryItem, MEMORY_ID


class Memory:
    """
    A collection of methods to interact with the assistant's memory.

    To interact with the assistant's memory, you can use the following methods:

        # Recall existing memories based on a query
        memories = assistant.memory.recall("Information about late delivery queries.")

        # Add a new memory
        # * best way to add new memories is to use assistant.learn.fast() method.
        assistant.memory.add(MemoryItem(title="Example of responding to late delivery queries", context="Dear customer,..."))

        # Remove an existing memory
        assistant.memory.remove(memory_id)
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Memory class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    def recall(self, query: str) -> List[MemoryItem]:
        """
        Recall memories based on a query.

        Args:
            query (str): The query to search memories for.
        """
        response = self.api_client.get(
            f"assistant/{self.config.id}/memory/recall/{query}",
        )
        return [MemoryItem(**memory) for memory in response["memories"]]

    def add(self, memory: MemoryItem) -> None:
        """
        Adds a new memory item to the assistant.

        Args:
            memory (MemoryItem): The memory item to add.
        """
        self.api_client.post(
            f"assistant/{self.config.id}/memory/add/",
            data=memory.model_dump(),
        )

    def remove(self, memory_id: MEMORY_ID) -> None:
        """
        Removes a memory from the assistant.

        Args:
            memory_id (MEMORY_ID): The ID of the memory item to remove.
        """
        self.api_client.delete(
            f"assistant/{self.config.id}/memory/remove/{memory_id}",
        )
