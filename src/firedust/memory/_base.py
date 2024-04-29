"""
Memory module for the Firedust assistant. 

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Recall existing memories based on a query
    query = "Information about late deliveries over the past month."
    memories = assistant.memory.recall(query)

    # Add a new memory explicitly
    new_memory = MemoryItem(title="Example of responding to late delivery queries", context="Dear customer,...")
    assistant.memory.add(new_memory)

    # For most use cases, use assistant.learn.fast to train the assistant and add memories.

    # Remove an existing memory
    assistant.memory.remove(memory_id)

    # Attach a collection of memories to the assistant
    # This makes it possible to share knowledge bases between assistants without the need to retrain them.
    assistant.memory.collections.attach("COLLECTION_ID")

    # Detach a collection of memories from the assistant
    assistant.memory.collections.detach("COLLECTION_ID")
"""

from typing import List
from uuid import UUID

from firedust._utils.api import APIClient
from firedust._utils.errors import APIError, MemoryError
from firedust._utils.types.api import APIContent
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.memory import MemoryItem


class Memory:
    """
    A collection of methods to interact with the assistant's memory.
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
        self.collections = MemoriesCollection(config, api_client)

    def recall(self, query: str, limit: int = 50) -> List[MemoryItem]:
        """
        Recall memories based on a query.

        Args:
            query (str): The query to search memories for.
            limit (int): The maximum number of memories to return.

        Returns:
            List[MemoryItem]: The list of memories that match the query.

        Raises:
            AttributeError: If the query or limit are invalid.
            APIError: If the API request fails.
        """

        # Check if the query and limit are within the allowed limits
        if limit > 500:
            raise AttributeError("Recall limit cannot exceed 500.")
        if len(query) > 1900:
            raise AttributeError("Query exceeds maximum length of 1900 characters.")

        # Fetch memories from the API
        response = self.api_client.post(
            "/memory/recall",
            data={
                "assistant_id": str(self.config.id),
                "query": query,
                "limit": limit,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to recall memories: {response.text}",
            )
        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data["memories"]]

    def add(self, memory: MemoryItem) -> None:
        """
        Adds a new memory item to the assistant's default memory collection.

        Args:
            memory (MemoryItem): The memory item to add.
        """
        self.api_client.post(
            f"/assistant/{self.config.id}/memory/add/",
            data={"memory": memory.model_dump()},
        )

    def remove(self, memory_id: UUID) -> None:
        """
        Removes a memory from the assistant's default memory collection.

        Args:
            memory_id (UUID): The ID of the memory item to remove.
        """
        self.api_client.delete(
            f"/assistant/{self.config.id}/memory/remove/{memory_id}",
        )

    def list(self, collection_id: UUID | None = None) -> List[UUID]:
        """
        List all memory items in a given collection id. If no collection id is provided,
        the default collection is used.
        """

        if collection_id is None:
            collection_id = self.config.memory.default_collection

        response = self.api_client.get(
            f"/assistant/{self.config.id}/memory/collections/list/{collection_id}",
        )

        if response.status_code == 200:
            memory_ids: List[UUID] = response.json()["collection"]
            return memory_ids
        elif response.status_code == 401:
            raise MemoryError("Memory collection not found.")
        else:
            raise MemoryError(f"Unknown response: {response}")


class MemoriesCollection:
    """
    Methods to interact with assistant's memories collections.
    A memory collection is a set of memories that were learned or added
    to the assistant.

    There are two types of memory collections:
        1. The default collection, which is immutable and is used to learn new memories
        and remember interactions with the users.
        2. Extra collections, borrowed from other assistants. It makes it possible to
        share knowledge bases between assistants without the need to retrain them.

    Check available collections attached to the assistant:
        assistant.memory.collection.list()

    Add an extra collection:
        assistant.memory.collections.attach("COLLECTION_ID")

    Remove an extra collection:
        assistant.memory.collections.detach("COLLECTION_ID")
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the MemoriesCollection class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    def attach(self, id: UUID) -> None:
        """
        Attaches an existing memory collection to the assistant.
        """
        response = self.api_client.post(
            f"/assistant/{self.config.id}/memory/collections/attach/{id}",
        )

        if response.status_code == 200:
            self.config.memory.extra_collections.append(id)
            return
        elif response.status_code == 401:
            raise MemoryError("Memory collection not found.")
        elif response.status_code == 402:
            raise MemoryError("Memory collection already attached.")
        else:
            raise MemoryError(f"Unknown response: {response}")

    def detach(self, id: UUID) -> None:
        """
        Detaches an existing memory collection from the assistant.
        """
        response = self.api_client.post(
            f"/assistant/{self.config.id}/memory/collections/detach/{id}",
        )

        if response.status_code == 200:
            self.config.memory.extra_collections.remove(id)
            return
        elif response.status_code == 401:
            raise MemoryError("Memory collection not found.")
        elif response.status_code == 402:
            raise MemoryError("Memory collection already detached.")
        elif response.status_code == 403:
            raise MemoryError("Cannot detach default memory collection.")
        else:
            raise MemoryError(f"Unknown response: {response}")

    def list(self) -> List[UUID]:
        """
        List all memory collections attached to the assistant.
        """
        collection_ids = [
            self.config.memory.default_collection
        ] + self.config.memory.extra_collections
        return collection_ids
