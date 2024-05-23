"""
Memory module for the Firedust assistant. 

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_NAME")

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

from firedust.types import APIContent, AssistantConfig, MemoryItem
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Memory:
    """
    A collection of methods to interact with the assistant's memory.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Memory class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

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

        # Fetch memories
        response = self.api_client.post(
            "/assistant/memory/recall",
            data={
                "assistant": self.config.name,
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

    def get(self, memory_ids: List[UUID]) -> List[MemoryItem]:
        """
        Retrieve a list of memory items by their IDs.

        Args:
            memory_ids (List[UUID]): A list of memory IDs.

        Returns:
            List[MemoryItem]: A list of memory items.

        Raises:
            APIError: If the API request fails.
        """
        response = self.api_client.post(
            "/assistant/memory/get",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to get memories: {response.text}")

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data["memories"]]

    def add(self, memories: List[MemoryItem]) -> None:
        """
        Adds a new memory item to the assistant's default memory collection.

        Args:
            memories (List[MemoryItem]): The list of memory items to add.
        """
        response = self.api_client.post(
            "/assistant/memory/add",
            data={
                "assistant": self.config.name,
                "memories": [memory.model_dump() for memory in memories],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to add memory: {response.text}")

    def delete(self, memory_ids: List[UUID]) -> None:
        """
        Removes memories from the assistant's default memory collection.

        Args:
            memory_ids (List[UUID]): The list of memory IDs to remove.
        """
        response = self.api_client.post(
            "/assistant/memory/delete",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to remove memory: {response.text}")

    def list(self) -> List[UUID]:
        """
        List all memory items available to the assistant.

        Returns:
            List[UUID]: A list of memory IDs.
        """
        response = self.api_client.get(
            f"/assistant/memory/list/{self.config.name}",
        )

        if not response.is_success:
            raise APIError(f"Failed to list memories: {response.text}")

        content = APIContent(**response.json())
        return [UUID(memory_id) for memory_id in content.data["memory_ids"]]

    def attach_memories(self, assistant: str) -> None:
        """
        Attach a collection of memories from another assistant.

        Args:
            assistant (str): The name of the assistant whose memories to attach.
        """
        if assistant == self.config.name:
            raise ValueError("Cannot attach memories from the same assistant.")

        response = self.api_client.put(
            f"/assistant/memory/attach/{self.config.name}/{assistant}",
        )
        if not response.is_success:
            raise APIError(f"Failed to attach collection: {response.text}")

        self.config.attached_memories.append(assistant)

    def detach_memories(self, assistant: str) -> None:
        """
        Detach a collection of memories that belongs to another assistant.

        Args:
            assistant (str): The name of the assistant whose memories to detach.
        """
        attached_memories = self.config.attached_memories
        if assistant not in attached_memories:
            raise ValueError("Collection not attached to the assistant.")

        response = self.api_client.delete(
            f"/assistant/memory/detach/{self.config.name}/{assistant}",
        )
        if not response.is_success:
            raise APIError(f"Failed to detach collection: {response.text}")

        attached_memories.remove(assistant)

    def erase_chat_history(self, user: str) -> str:
        """
        Erase the chat history of a user from the assistant's memory.

        Args:
            user (str): The unique identifier of the user.

        Returns:
            str: The response from the API.
        """
        response = self.api_client.delete(
            f"/assistant/memory/chat_history/forget/{self.config.name}/{user}",
        )
        if not response.is_success:
            raise APIError(f"Failed to erase chat history: {response.text}")

        return response.text


class AsyncMemory:
    """
    A collection of methods to interact with the assistant's memory asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncMemory class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (ASyncAPIClient): The API client.
        """
        self.config = config
        self.api_client = api_client

    async def recall(self, query: str, limit: int = 50) -> List[MemoryItem]:
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

        # Fetch memories
        response = await self.api_client.post(
            "/assistant/memory/recall",
            data={
                "assistant": self.config.name,
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

    async def get(self, memory_ids: List[UUID]) -> List[MemoryItem]:
        """
        Retrieve a list of memory items by their IDs.

        Args:
            memory_ids (List[UUID]): A list of memory IDs.

        Returns:
            List[MemoryItem]: A list of memory items.

        Raises:
            APIError: If the API request fails.
        """
        response = await self.api_client.post(
            "/assistant/memory/get",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to get memories: {response.text}")

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data["memories"]]

    async def add(self, memories: List[MemoryItem]) -> None:
        """
        Adds a new memory item to the assistant's default memory collection.

        Args:
            memories (List[MemoryItem]): The list of memory items to add.
        """
        response = await self.api_client.post(
            "/assistant/memory/add",
            data={
                "assistant": self.config.name,
                "memories": [memory.model_dump() for memory in memories],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to add memory: {response.text}")

    async def delete(self, memory_ids: List[UUID]) -> None:
        """
        Removes memories from the assistant's default memory collection.

        Args:
            memory_ids (List[UUID]): The list of memory IDs to remove.
        """
        response = await self.api_client.post(
            "/assistant/memory/delete",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to remove memory: {response.text}")

    async def list(self) -> List[UUID]:
        """
        List all memory items available to the assistant.

        Returns:
            List[UUID]: A list of memory IDs.
        """
        response = await self.api_client.get(
            f"/assistant/memory/list/{self.config.name}",
        )

        if not response.is_success:
            raise APIError(f"Failed to list memories: {response.text}")

        content = APIContent(**response.json())
        return [UUID(memory_id) for memory_id in content.data["memory_ids"]]

    async def attach_memories(self, assistant: str) -> None:
        """
        Attach a collection of memories from another assistant.

        Args:
            assistant (str): The name of the assistant whose memories to attach.
        """
        if assistant == self.config.name:
            raise ValueError("Cannot attach memories from the same assistant.")

        response = await self.api_client.put(
            f"/assistant/memory/attach/{self.config.name}/{assistant}",
        )
        if not response.is_success:
            raise APIError(f"Failed to attach collection: {response.text}")

        self.config.attached_memories.append(assistant)

    async def detach_memories(self, assistant: str) -> None:
        """
        Detach a collection of memories that belongs to another assistant.

        Args:
            assistant (str): The name of the assistant whose memories to detach.
        """
        attached_memories = self.config.attached_memories
        if assistant not in attached_memories:
            raise ValueError("Collection not attached to the assistant.")

        response = await self.api_client.delete(
            f"/assistant/memory/detach/{self.config.name}/{assistant}",
        )
        if not response.is_success:
            raise APIError(f"Failed to detach collection: {response.text}")

        attached_memories.remove(assistant)

    async def erase_chat_history(self, user: str) -> str:
        """
        Erase the chat history of a user from the assistant's memory.

        Args:
            user (str): The unique identifier of the user.

        Returns:
            str: The response from the API.
        """
        response = await self.api_client.delete(
            f"/assistant/memory/chat_history/forget/{self.config.name}/{user}",
        )
        if not response.is_success:
            raise APIError(f"Failed to erase chat history: {response.text}")

        return response.text
