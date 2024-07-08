from typing import Iterable, List
from uuid import UUID

import firedust
from firedust.types import APIContent, AssistantConfig, MemoryItem, Message
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Memory:
    """
    A collection of methods to interact with the assistant's memory.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client

    def recall(self, query: str, limit: int = 50, offset: int = 0) -> List[MemoryItem]:
        """
        Recall memories based on a query.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        memories = assistant.memory.recall("Information about late deliveries.")
        ```

        Args:
            query (str): The query to search memories for.
            limit (int): The maximum number of memories to return.
            offset (int): The offset to start from.

        Returns:
            List[MemoryItem]: The list of memories that are related to the query.
        """
        response = self.api_client.post(
            "/assistant/memory/recall",
            data={
                "assistant": self.config.name,
                "query": query,
                "limit": limit,
                "offset": offset,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to recall memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data]

    def get(self, memory_ids: List[UUID]) -> List[MemoryItem]:
        """
        Retrieve a list of memory items by their IDs.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        response = assistant.chat.message("What are the latest sales figures?")

        # Retrieve memories that the assistant used to generate the response
        memory_ids = response.references.memories
        memories = assistant.memory.get(memory_ids)
        ```

        Args:
            memory_ids (List[UUID]): A list of memory IDs.

        Returns:
            List[MemoryItem]: A list of memory items.
        """
        if len(memory_ids) == 0:
            return []

        response = self.api_client.post(
            "/assistant/memory/list",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to get memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data]

    def add(self, memories: List[MemoryItem]) -> None:
        """
        Add new memory items to the assistant's memory collection. It is useful for memory management,
        for example, when selectively migrating some memories from one assistant to another.

        Example:
        ```python
        import firedust

        assistant1 = firedust.assistant.load("ASSISTANT_NAME1")
        assistant2 = firedust.assistant.load("ASSISTANT_NAME2")

        memories = assistant1.memory.recall("User feedback")
        assistant2.memory.add(memories)
        ```

        Args:
            memories (List[MemoryItem]): The list of memory items to add.
        """
        response = self.api_client.put(
            "/assistant/memory/list",
            data={
                "assistant": self.config.name,
                "memories": [memory.model_dump() for memory in memories],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add memories: {response.text}",
            )

    def delete(self, memory_ids: List[UUID]) -> None:
        """
        Removes memories from the assistant's memory. It is useful for memory management,
        for example, when selectively removing memories from an assistant.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        memory_ids = assistant.memory.recall("User feedback")
        assistant.memory.delete(memory_ids)
        ```

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
            raise APIError(
                code=response.status_code,
                message=f"Failed to remove memory: {response.text}",
            )

    def list(self, limit: int = 100, offset: int = 0) -> List[UUID]:
        """
        List all memory items available to the assistant.

        Returns:
            List[UUID]: A list of memory IDs.
        """
        response = self.api_client.get(
            "/assistant/memory/list",
            params={"assistant": self.config.name, "limit": limit, "offset": offset},
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to list memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [UUID(memory_id) for memory_id in content.data]

    def share(self, assistant_receiver: str) -> None:
        """
        Share all assistant's memories with another assistant. It makes the memories
        available for the other assistant to use when answering questions or performing tasks.
        It's a full sync and applies to both past memories and the ones added in the future.

        To share memories selectively use the assistant.memory.add method.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_SHARER")
        assistant.memory.share("ASSISTANT_RECEIVER")
        ```

        Args:
            assistant_receiver (str): The name of the assistant who will access the memories.
        """
        if assistant_receiver == self.config.name:
            raise ValueError("Cannot attach memories from the same assistant.")

        receiver_config = firedust.assistant.load(assistant_receiver)
        if self.config.name in receiver_config.config.attached_memories:
            raise ValueError(
                f"The memories of {self.config.name} are already shared to the {assistant_receiver}."
            )

        response = self.api_client.put(
            "/assistant/memory/share",
            data={
                "assistant_sharer": self.config.name,
                "assistant_receiver": assistant_receiver,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to share memories: {response.text}",
            )

    def unshare(self, assistant_receiver: str) -> None:
        """
        Memories of the assistant will no longer be shared with the assistant receiver.

        Example:
        ```python
        import firedust

        assistant_sharer = firedust.assistant.load("ASSISTANT_SHARER")
        assistant_sharer.memory.unshare("ASSISTANT_RECEIVER")
        ```

        Args:
            assistant (str): The name of the assistant who will lose access to the memories.
        """
        if assistant_receiver == self.config.name:
            raise ValueError("Cannot detach memories from the same assistant.")

        reciver_config = firedust.assistant.load(assistant_receiver)
        if self.config.name not in reciver_config.config.attached_memories:
            raise ValueError(
                f"The memories of {self.config.name} are not shared to the {assistant_receiver}."
            )

        response = self.api_client.delete(
            "/assistant/memory/share",
            params={
                "assistant_receiver": assistant_receiver,
                "assistant_sharer": self.config.name,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to detach collection: {response.text}",
            )

    def add_chat_history(self, messages: Iterable[Message]) -> None:
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
            user="product_team",
            message="John: Based on the last discussion, we've made the following changes to the product...",
            author="user",
        )
        message2 = Message(
            assistant="ASSISTANT_NAME",
            user="product_team",
            message="Helen: John, could you please share the updated product roadmap?",
            author="user",
        )
        message3 = Message(
            assistant="ASSISTANT_NAME",
            user="product_team",
            message="John: Sure, the new roadmap is the following...",
            author="user",
        )

        assistant.memory.add_chat_history([message1, message2, message3])
        ```

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = self.api_client.put(
            "/assistant/memory/chat_history",
            data={
                "assistant": self.config.name,
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add chat history: {response.text}",
            )

    def erase_chat_history(self, user: str, confirm: bool = False) -> None:
        """
        Irreversebly delete the chat history of a user from the assistant's memory.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.memory.erase_chat_history(user="product_team", confirm=True)
        ```

        Args:
            user (str): The unique identifier of the user.
            confirm (bool): Confirm the deletion. Defaults to False.
        """
        if confirm is False:
            raise ValueError("Please confirm the deletion by setting confirm=True")

        response = self.api_client.delete(
            "/assistant/memory/chat_history",
            params={
                "assistant": self.config.name,
                "user": user,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to erase chat history: {response.text}",
            )


class AsyncMemory:
    """
    A collection of asynchronous methods to interact with the assistant's memory asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client

    async def recall(
        self, query: str, limit: int = 50, offset: int = 0
    ) -> List[MemoryItem]:
        """
        Recall memories based on a query, asynchronously.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            memories = await assistant.memory.recall("Information about late deliveries.")

        asyncio.run(main())
        ```

        Args:
            query (str): The query to search memories for.
            limit (int): The maximum number of memories to return.
            offset (int): The offset to start from.

        Returns:
            List[MemoryItem]: The list of memories that are related to the query.
        """
        response = await self.api_client.post(
            "/assistant/memory/recall",
            data={
                "assistant": self.config.name,
                "query": query,
                "limit": limit,
                "offset": offset,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to recall memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data]

    async def get(self, memory_ids: List[UUID]) -> List[MemoryItem]:
        """
        Retrieve a list of memory items by their IDs, asynchronously. It is used for memory management.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            response = await assistant.chat.message("What are the latest sales figures?")

            # Retrieve memories that the assistant used to answer the question
            memory_ids = response.references.memories
            memories = await assistant.memory.get(memory_ids)

        asyncio.run(main())
        ```

        Args:
            memory_ids (List[UUID]): A list of memory IDs.

        Returns:
            List[MemoryItem]: A list of memory items.
        """
        response = await self.api_client.post(
            "/assistant/memory/list",
            data={
                "assistant": self.config.name,
                "memory_ids": [str(memory_id) for memory_id in memory_ids],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to get memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [MemoryItem(**memory) for memory in content.data]

    async def add(self, memories: List[MemoryItem]) -> None:
        """
        Adds new memory items to the assistant's memory collection, asynchronously. It is useful for memory management.
        For example, when selectively migrating some memories from one assistant to another.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant1 = await firedust.async_load("ASSISTANT_NAME1")
            assistant2 = await firedust.async_load("ASSISTANT_NAME2")

            memories = await assistant1.memory.recall("User feedback")
            await assistant2.memory.add(memories)

        asyncio.run(main())
        ```

        Args:
            memories (List[MemoryItem]): The list of memory items to add.
        """
        response = await self.api_client.put(
            "/assistant/memory/list",
            data={
                "assistant": self.config.name,
                "memories": [memory.model_dump() for memory in memories],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add memories: {response.text}",
            )

    async def delete(self, memory_ids: List[UUID]) -> None:
        """
        Removes memories from the assistant's default memory collection, async. It is useful for memory management,
        for example, when selectively removing memories from an assistant.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            memory_ids = await assistant.memory.list(limit=10)
            await assistant.memory.delete(memory_ids)

        asyncio.run(main())
        ```

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
            raise APIError(
                code=response.status_code,
                message=f"Failed to delete memories: {response.text}",
            )

    async def list(self, limit: int = 100, offset: int = 0) -> List[UUID]:
        """
        List all memory items available to the assistant.

        Returns:
            List[UUID]: A list of memory IDs.
        """
        response = await self.api_client.get(
            "/assistant/memory/list",
            params={"assistant": self.config.name, "limit": limit, "offset": offset},
        )

        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to list memories: {response.text}",
            )

        content = APIContent(**response.json())
        return [UUID(memory_id) for memory_id in content.data]

    async def share(self, assistant_receiver: str) -> None:
        """
        Share all assistant's memories with another assistant, asynchronously. It makes the memories
        available for the assistant receiver to use when answering questions or performing tasks.
        It's a full memory sync and applies to both past memories and the ones added in the future.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_SHARER")
            await assistant.memory.share("ASSISTANT_RECEIVER")

        asyncio.run(main())
        ```

        Args:
            assistant_receiver (str): The name of the assistant who will access the memories.
        """
        if assistant_receiver == self.config.name:
            raise ValueError("Cannot share memories from the same assistant.")

        receiver_config = await firedust.assistant.async_load(assistant_receiver)
        if self.config.name in receiver_config.config.attached_memories:
            raise ValueError(
                f"The memories of {self.config.name} are already shared to the {assistant_receiver}."
            )

        response = await self.api_client.put(
            "/assistant/memory/share",
            data={
                "assistant_receiver": assistant_receiver,
                "assistant_sharer": self.config.name,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to share memories: {response.text}",
            )

    async def unshare(self, assistant_receiver: str) -> None:
        """
        Memories of the assistant will no longer be shared with the assistant receiver.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_SHARER")
            await assistant.memory.unshare("ASSISTANT_RECEIVER")

        asyncio.run(main())
        ```

        Args:
            assistant (str): The name of the assistant who will lose access to the memories.
        """
        if assistant_receiver == self.config.name:
            raise ValueError("Cannot unshare memories from the same assistant.")

        reciver_config = await firedust.assistant.async_load(assistant_receiver)
        if self.config.name not in reciver_config.config.attached_memories:
            raise ValueError(
                f"The memories of {self.config.name} are not shared with {assistant_receiver}."
            )

        response = await self.api_client.delete(
            "/assistant/memory/share",
            params={
                "assistant_sharer": self.config.name,
                "assistant_receiver": assistant_receiver,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to unshare collection: {response.text}",
            )

    async def add_chat_history(self, messages: Iterable[Message]) -> None:
        """
        Adds a chat message history to the assistant's memory, asynchronously. It helps the assistant
        learn from past conversations to improve the quality of responses.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")

            message1 = Message(
                assistant="ASSISTANT_NAME",
                user="product_team",
                message="John: Based on the last discussion, we've made the following changes to the product...",
                author="user",
            )
            message2 = Message(
                assistant="ASSISTANT_NAME",
                user="product_team",
                message="Helen: John, could you please share the updated product roadmap?",
                author="user",
            )
            message3 = Message(
                assistant="ASSISTANT_NAME",
                user="product_team",
                message="John: Sure, the new roadmap is the following...",
                author="user",
            )

            await assistant.memory.add_chat_history([message1, message2, message3])

        asyncio.run(main())
        ```

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = await self.api_client.put(
            "/assistant/memory/chat_history",
            data={
                "assistant": self.config.name,
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add chat history: {response.text}",
            )

    async def erase_chat_history(self, user: str, confirm: bool = False) -> None:
        """
        Irreversebly delete the chat history of a user from the assistant's memory, asynchronously.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.async_load("ASSISTANT_NAME")
            await assistant.memory.erase_chat_history(user="product_team", confirm=True)

        asyncio.run(main())
        ```

        Args:
            user (str): The unique identifier of the user.
            confirm (bool): Confirm the deletion. Defaults to False.
        """
        if confirm is False:
            raise ValueError("Please confirm the deletion by setting confirm=True")

        response = await self.api_client.delete(
            "/assistant/memory/chat_history",
            params={
                "assistant": self.config.name,
                "user": user,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to erase chat history: {response.text}",
            )
