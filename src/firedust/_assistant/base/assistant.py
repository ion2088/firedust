"""
This is a private file. To interact with Assistant and AsyncAssistant classes, use the modules in firedust.assistant.*.

Example:
```python
import firedust

assistant = firedust.assistant.create("ASSISTANT_NAME")
response = assistant.chat.message("Hello, how are you?")
print(response.message)
```
"""

from firedust._assistant.chat.base import AsyncChat, Chat
from firedust._assistant.interface.base import AsyncInterface, Interface
from firedust._assistant.learning.base import AsyncLearning, Learning
from firedust._assistant.memory.base import AsyncMemory, Memory
from firedust.types import AssistantConfig
from firedust.types.base import INFERENCE_MODEL
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError, AssistantError
from firedust.utils.logging import LOG


class Assistant:
    """
    The main class to interact with firedust AI assistants. The class doesn't support direct
    instantiation. To create a new assistant, load an existing one or update it, use the methods
    firedust.assistant.create, firedust.assistant.load, and assistant.update.*.

    Example:
    ```python
    import firedust

    assistant = firedust.assistant.create("ASSISTANT_NAME")
    response = assistant.chat.message("Hello, how are you?")
    print(response.message)

    assistant = firedust.assistant.load("ASSISTANT_NAME")
    assistant.update.instructions("1. Protect the ring bearer. 2. Do not let the ring corrupt you.")
    ```

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (SyncAPIClient): The API client.
        update (Update): Methods to update the configuration of the assistant.
        interface (Interface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (Learning): Methods to add your data to the assistant's knowledge.
        chat (Chat): Methods to chat with the assistant.
        memory (Memory): Methods to interact with the assistant's memory.

    Private Attributes:
        _allow_instantiation (bool): A private attribute to discourage direct instantiation of the Assistant class.
    """

    _config: AssistantConfig
    _api_client: SyncAPIClient

    _update: "_Update"
    _interface: Interface
    _learn: Learning
    _chat: Chat
    _memory: Memory

    # assistant should be started with firedust.assistant.create or .load methods
    _allow_instantiation: bool = False

    def __init__(
        self, config: AssistantConfig, api_client: SyncAPIClient | None = None
    ) -> None:
        # prevent direct instantiation
        # use firedust.assistant.create or .load methods
        if not self._allow_instantiation:
            raise AssistantError(
                """
                To load an assistant or create a new one use firedust.assitant.create or .load methods.
                
                Example:
                ```python
                import firedust

                assistant = firedust.assistant.create("ASSISTANT_NAME")
                # or
                assistant = firedust.assistant.load("ASSISTANT_NAME")

                response = assistant.chat.message("Hello, how are you?")
                print(response.message)
                """
            )

        # configuration
        self._config = config
        self._api_client = api_client or SyncAPIClient()

        # management
        self._update = _Update(self._config, self._api_client)
        self._interface = Interface(self._config, self._api_client)

        # essence
        self._learn = Learning(self._config, self._api_client)
        self._chat = Chat(self._config, self._api_client)
        self._memory = Memory(self._config, self._api_client)

    def __setattr__(self, key: str, value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To update the assistant, use the methods assistant.update.* or create a new one.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        # or
        assistant = firedust.assistant.create("ASSISTANT_NAME")

        assistant.update.instructions("1. Protect the ring bearer. 2. Do not let the ring corrupt you.")
        assistant.update.model("mistral/mistral-medium")
        ```
        """
        if not key.startswith("_"):
            self._raise_setter_error(key)
        return super().__setattr__(key, value)

    def __repr__(self) -> str:
        return (
            "Assistant("
            f"name={self.config.name!r}, "
            f"instructions={self.config.instructions!r}, "
            f"model={self.config.model!r}"
            ")"
        )

    def __str__(self) -> str:
        return (
            f"assistant: {self.config.name}, "
            f"model: {self.config.model}, "
            f"instructions: {self.config.instructions}"
        )

    @property
    def config(self) -> AssistantConfig:
        return self._config

    @property
    def api_client(self) -> SyncAPIClient:
        return self._api_client

    @property
    def update(self) -> "_Update":
        return self._update

    @property
    def interface(self) -> Interface:
        return self._interface

    @property
    def learn(self) -> Learning:
        return self._learn

    @property
    def chat(self) -> Chat:
        return self._chat

    @property
    def memory(self) -> Memory:
        return self._memory

    @classmethod
    def _create_instance(
        cls, config: AssistantConfig, api_client: SyncAPIClient
    ) -> "Assistant":
        """
        Reserved for internal use only. To create an assistant use firedust.assistant.create method

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.create("ASSISTANT_NAME")
        response = assistant.chat.message("Hello, how are you?")
        print(response.message)
        ```

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.

        Returns:
            Assistant: A new instance of the Assistant class.
        """
        cls._allow_instantiation = True
        assistant = cls(config, api_client)
        cls._allow_instantiation = False
        return assistant

    @staticmethod
    def _raise_setter_error(attribute: str) -> None:
        raise AttributeError(
            f"""
                Unable to set attribute '{attribute}'. Assistant class is immutable and doesn't support direct attribute assignment.
                To update assistant, use assistant.update.* methods or create a new assistant.
                
                Example:
                ```python
                import firedust

                assistant = firedust.assistant.load("ASSISTANT_NAME")
                assistant.update.instructions("1. Protect the ring bearer. 2. Do not let the ring corrupt you.")
                assistant.update.model("mistral/mistral-medium")
                ```
            """
        )

    def delete(
        self,
        confirm: bool = False,
    ) -> None:
        """
        Delete the assistant irreversibly.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.delete(confirm=True)
        ```

        Args:
            confirm (bool, optional): Confirm the deletion of the assistant. Defaults to False.
        """
        if not confirm:
            raise AssistantError(
                "Assistant and all its memories will be permanently deleted. To confirm, set confirm=True."
            )

        response = self.api_client.delete(
            "/assistant", params={"name": self.config.name}
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"An error occured while deleting the assistant {self.config.name}: {response.text}",
            )
        LOG.info(f"Successfully deleted assistant {self.config.name}.")


class _Update:
    """
    A collection of methods to update an existing assistant.

    Example:
    ```python
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_NAME")

    new_instructions = "1. Protect the ring bearer. 2. Do not let the ring corrupt you."
    new_model = "mistral/mistral-medium"

    assistant.update.instructions(new_instructions)
    assistant.update.model(new_model)
    ```
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client

    def instructions(self, instructions: str) -> None:
        """
        Updates the instructions of the assistant.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")

        new_instructions = "1. Protect the ring bearer. 2. Do not let the ring corrupt you."
        assistant.update.instructions(new_instructions)
        ```

        Args:
            instructions (str): The new instructions for the assistant.
        """
        response = self.api_client.put(
            "/assistant/instructions",
            data={
                "assistant": str(self.config.name),
                "instructions": instructions,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the instructions of the assistant {self.config.name}: {response.text}",
            )
        self.config.instructions = instructions

    def model(self, new_model: INFERENCE_MODEL) -> None:
        """
        Updates the inference model of the assistant.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.update.model("mistral/mistral-medium")
        ```

        Args:
            new_model (INFERENCE_MODEL): The new inference model.
        """
        response = self.api_client.put(
            "/assistant/model",
            data={
                "assistant": str(self.config.name),
                "model": new_model,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the inference configuration: {response.text}",
            )
        self.config.model = new_model


class AsyncAssistant:
    """
    The main class to interact with firedust AI assistants asynchronously. The class doesn't support direct
    instantiation. To create a new assistant, load an existing one or update it, use the methods
    firedust.assistant.async_create, firedust.assistant.async_load, and assistant.update.*.

    Example:
    ```python
    import firedust
    import asyncio

    async def main():
        assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
        response = await assistant.chat.message("Hello, how are you?")
        print(response.message)

    asyncio.run(main())
    ```

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (AsyncAPIClient): The API client.
        update (_AsyncUpdate): Methods to update the configuration of the assistant.
        interface (AsyncInterface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (AsyncLearning): Methods to train the assistant on your data.
        chat (AsyncChat): Methods to chat with the assistant.
        memory (AsyncMemory): Methods to interact with the assistant's memory.

    Private Attributes:
        _allow_instantiation (bool): A private attribute to discourage direct instantiation of the AsyncAssistant class.
    """

    _config: AssistantConfig
    _api_client: AsyncAPIClient

    _update: "_AsyncUpdate"
    _interface: AsyncInterface
    _learn: AsyncLearning
    _chat: AsyncChat
    _memory: AsyncMemory

    # assistant should be instantiated using the create and load classmethods
    _allow_instantiation: bool = False

    def __init__(
        self, config: AssistantConfig, api_client: AsyncAPIClient | None = None
    ) -> None:
        # prevent direct instantiation
        if not self._allow_instantiation:
            raise AssistantError(
                """
                To load an assistant or create a new one use firedust.assitant.async_create or .async_load methods.
                
                Example:
                ```python
                import firedust
                import asyncio

                async def main():
                    assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
                    # or
                    assistant = await firedust.assistant.async_create("ASSISTANT_NAME")
                    
                    response = await assistant.chat.message("Hello, how are you?")
                    print(response.message)

                asyncio.run(main())
                """
            )

        # configuration
        self._config = config
        self._api_client = api_client or AsyncAPIClient()

        # management
        self._update = _AsyncUpdate(self._config, self._api_client)
        self._interface = AsyncInterface(self._config, self._api_client)

        # essence
        self._learn = AsyncLearning(self._config, self._api_client)
        self._chat = AsyncChat(self._config, self._api_client)
        self._memory = AsyncMemory(self._config, self._api_client)

    def __setattr__(self, key: str, value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To update the assistant, use the methods assistant.update.* or create a new one.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            # or
            assistant = await firedust.assistant.async_create("ASSISTANT_NAME")

            await assistant.update.instructions("1. Protect the ring bearer. 2. Do not let the ring corrupt you.")
            await assistant.update.model("mistral/mistral-medium")

        asyncio.run(main())
        ```
        """
        if not key.startswith("_"):
            self._raise_setter_error(key)
        return super().__setattr__(key, value)

    def __repr__(self) -> str:
        return (
            "AsyncAssistant("
            f"name={self.config.name!r}, "
            f"instructions={self.config.instructions!r}, "
            f"model={self.config.model!r}"
            ")"
        )

    def __str__(self) -> str:
        return (
            f"assistant: {self.config.name}, "
            f"model: {self.config.model}, "
            f"instructions: {self.config.instructions}"
        )

    @property
    def config(self) -> AssistantConfig:
        return self._config

    @property
    def api_client(self) -> AsyncAPIClient:
        return self._api_client

    @property
    def update(self) -> "_AsyncUpdate":
        return self._update

    @property
    def interface(self) -> AsyncInterface:
        return self._interface

    @property
    def learn(self) -> AsyncLearning:
        return self._learn

    @property
    def chat(self) -> AsyncChat:
        return self._chat

    @property
    def memory(self) -> AsyncMemory:
        return self._memory

    @classmethod
    async def _create_instance(
        cls, config: AssistantConfig, api_client: AsyncAPIClient
    ) -> "AsyncAssistant":
        """
        Reserved for internal use only. To create an assistant use firedust.assistant.async_create method.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_create("ASSISTANT_NAME")
            response = await assistant.chat.message("Hello, how are you?")
            print(response.message)

        asyncio.run(main())
        ```
        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.

        Returns:
            AsyncAssistant: A new instance of the AsyncAssistant class.
        """
        cls._allow_instantiation = True
        assistant = cls(config, api_client)
        cls._allow_instantiation = False
        return assistant

    @staticmethod
    def _raise_setter_error(attribute: str) -> None:
        raise AttributeError(
            f"""
                Unable to set attribute '{attribute}'. AsyncAssistant class is immutable and doesn't support direct attribute assignment.
                To update assistant, use assistant.update.* methods or create a new assistant.

                Example:
                ```python
                import firedust
                import asyncio

                async def main():
                    assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
                    # or
                    assistant = await firedust.assistant.async_create("ASSISTANT_NAME")

                    await assistant.update.instructions("1. Protect the ring bearer. 2. Do not let the ring corrupt you.")
                    await assistant.update.model("mistral/mistral-medium")

                asyncio.run(main())
            """
        )

    async def delete(
        self,
        confirm: bool = False,
    ) -> None:
        """
        Deletes an existing assistant irreversibly.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            await assistant.delete(confirm=True)

        asyncio.run(main())
        ```

        Args:
            confirm (bool, optional): Confirm the deletion of the assistant. Defaults to False.
        """
        if not confirm:
            raise AssistantError(
                f"Assistant {self.config.name} and all its memories will be permanently deleted. To confirm, set confirm=True."
            )

        response = await self.api_client.delete(
            "/assistant", params={"name": self.config.name}
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"An error occured while deleting the assistant {self.config.name}: {response.text}",
            )
        LOG.info(f"Successfully deleted assistant {self.config.name}.")


class _AsyncUpdate:
    """
    A collection of methods to update an existing assistant asynchronously.

    Example:
    ```python
    import firedust
    import asyncio

    async def main():
        assistant = await firedust.assistant.async_load("ASSISTANT_NAME")

        new_instructions = "1. Protect the ring bearer. 2. Do not let the ring corrupt you."
        new_model = "mistral/mistral-medium"

        await assistant.update.instructions(new_instructions)
        await assistant.update.model(new_model)

    asyncio.run(main())
    ```
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.config = config
        self.api_client = api_client

    async def instructions(self, instructions: str) -> None:
        """
        Updates the instructions of the assistant.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")

            new_instructions = "1. Protect the ring bearer. 2. Do not let the ring corrupt you."
            await assistant.update.instructions(new_instructions)

        asyncio.run(main())
        ```

        Args:
            instructions (str): The new instructions of the assistant.
        """
        response = await self.api_client.put(
            "/assistant/instructions",
            data={
                "assistant": str(self.config.name),
                "instructions": instructions,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the instructions of the assistant {self.config.name}: {response.text}",
            )
        self.config = AssistantConfig(
            name=self.config.name,
            instructions=instructions,
            model=self.config.model,
        )

    async def model(self, new_model: INFERENCE_MODEL) -> None:
        """
        Updates the inference model of the assistant.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            await assistant.update.model("mistral/mistral-medium")

        asyncio.run(main())
        ```

        Args:
            new_model (INFERENCE_MODEL): The new inference model.
        """
        response = await self.api_client.put(
            "/assistant/model",
            data={
                "assistant": str(self.config.name),
                "model": new_model,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the inference configuration: {response.text}",
            )
        self.config = AssistantConfig(
            name=self.config.name,
            instructions=self.config.instructions,
            model=new_model,
        )
