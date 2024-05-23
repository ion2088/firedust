"""
To interact with Assistant and AsyncAssistant classes, use the modules in firedust.assistant.*.
"""

import logging

from firedust._assistant.chat.base import AsyncChat, Chat
from firedust._assistant.interface.base import AsyncInterface, Interface
from firedust._assistant.learning.base import AsyncLearning, Learning
from firedust._assistant.memory.base import AsyncMemory, Memory
from firedust.types import AssistantConfig
from firedust.types.base import INFERENCE_MODEL
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError, AssistantError

LOG = logging.getLogger("firedust")


class Assistant:
    """
    The Assistant class is the main entry point for interacting with Firedust.
    It is used to create, load, train, deploy and interact with an AI assistant.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (SyncAPIClient): The API client.
        update (Update): Methods to update the configuration of the assistant.
        interface (Interface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (Learning): Methods to train the assistant on your data.
        chat (Chat): Methods to chat with the assistant.
        memory (Memory): Methods to interact with the assistant's memory.
        ability (Ability): Methods to manage and interact with the assistant's abilities.

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

    # assistant should be instantiated using the create and load classmethods
    _allow_instantiation: bool = False

    def __init__(
        self, config: AssistantConfig, api_client: SyncAPIClient | None = None
    ) -> None:
        """
        Initializes a new instance of the Assistant class.

        To create or load an assistant, use the following methods:
        TODO: Add link to github example code.

        Args:
            config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
            api_client (SyncAPIClient, optional): The API client. Defaults to None.
        """

        # prevent direct instantiation
        if not self._allow_instantiation:
            raise AssistantError(
                """
                To load an assistant or create a new one, use the following methods:
                TODO: Add link to github example code.
                """
            )

        # configuration
        self._config = config
        self._api_client = api_client or SyncAPIClient()

        # management
        self._update = _Update(self)
        self._interface = Interface(self._config, self._api_client)

        # essence
        self._learn = Learning(self._config, self._api_client)
        self._chat = Chat(self._config, self._api_client)
        self._memory = Memory(self._config, self._api_client)

    def __setattr__(self, key: str, value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To update the assistant, use the methods assistant.update.* or create a new one.
        """
        if not key.startswith("_"):
            self._raise_setter_error(key)
        return super().__setattr__(key, value)

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the Assistant instance.
        Includes all attributes for easy inspection and debugging.
        """
        return (
            "Assistant("
            f"name={self.config.name!r}, "
            f"instructions={self.config.instructions!r}, "
            f"model={self.config.model!r}"
            ")"
        )

    def __str__(self) -> str:
        """
        Provides a user-friendly string representation of the Assistant instance.
        Gives an overview with just the assistant's name and ID.
        """
        return f"Assistant {self.config.name}"

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
        Reserved for internal use only with the create and load methods.
        Creates a new instance of the Assistant class.

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
                Unable to set attribute '{attribute}'. Assistant class is immutable and doesn't support direct attribute assignment.\n
                To update assistant, use assistant.update.* methods or create a new assistant with the desired configuration following the example below:\n\n
                
                TODO: Add link to github example code.
            """
        )

    def delete(
        self,
        api_client: SyncAPIClient | None = None,
        confirm: bool = False,
    ) -> None:
        """
        Deletes an existing assistant with the specified ID.

        Args:
            api_client (SyncAPIClient, optional): The API client. Defaults to None.
        """
        if not confirm:
            raise AssistantError(
                "Assistant and all its memories will be permanently deleted. To confirm, set confirm=True."
            )

        api_client = api_client or SyncAPIClient()
        response = api_client.delete(f"/assistant/delete/{self.config.name}")
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"An error occured while deleting the assistant {self.config.name}: {response.text}",
            )
        LOG.info(f"Successfully deleted assistant {self.config.name}.")


class _Update:
    """
    A collection of methods to update the configuration of the assistant.

    To update the assistant, you can use the following methods:
        assistant.update.name("Sam")
        assistant.update.instructions("You are a helpful assistant..."])
        assistant.update.inference_config(new_config)
    """

    def __init__(self, assistant: Assistant) -> None:
        """
        Initializes a new instance of the Update class.

        Args:
            assistant (Assistant): The assistant.
        """
        self._assistant = assistant

    def __setattr__(self, __name: str, __value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To change the assistant, use assistant.update.* methods or create a new one.
        """
        if not __name.startswith("_"):
            self.assistant._raise_setter_error(__name)
        return super().__setattr__(__name, __value)

    @property
    def assistant(self) -> Assistant:
        return self._assistant

    @property
    def api_client(self) -> SyncAPIClient:
        return self.assistant.api_client

    def instructions(self, instructions: str) -> None:
        """
        Updates the instructions of the assistant.

        Args:
            instructions (List[str]): The new instructions of the assistant.
        """
        response = self.api_client.post(
            "/assistant/update/instructions",
            data={
                "assistant": str(self.assistant.config.name),
                "instructions": instructions,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the instructions of the assistant {self.assistant.config.name}: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            name=self.assistant._config.name,
            instructions=instructions,
            model=self.assistant._config.model,
        )

    def model(self, new_model: INFERENCE_MODEL) -> None:
        """
        Updates the inference model of the assistant.

        Args:
            new_model (INFERENCE_MODEL): The new inference model.
        """
        response = self.api_client.post(
            "/assistant/update/model",
            data={
                "assistant": str(self.assistant.config.name),
                "model": new_model,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the inference configuration: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            name=self.assistant._config.name,
            instructions=self.assistant._config.instructions,
            model=new_model,
        )


class AsyncAssistant:
    """
    The AsyncAssistant class is the main entry point for interacting with Firedust asynchronously.
    It is used to create, load, train, deploy and interact with an AI assistant.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (AsyncAPIClient): The API client.
        update (Update): Methods to update the configuration of the assistant.
        interface (Interface): Deploy and interact with the assistant on Slack, email, Discord and other interfaces.
        learn (Learning): Methods to train the assistant on your data.
        chat (Chat): Methods to chat with the assistant.
        memory (Memory): Methods to interact with the assistant's memory.

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
        """
        Initializes a new instance of the AsyncAssistant class.

        To create or load an assistant, use the following methods:
        TODO: Add link to github example code.

        Args:
            config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
            api_client (AsyncAPIClient, optional): The API client. Defaults to None.
        """

        # prevent direct instantiation
        if not self._allow_instantiation:
            raise AssistantError(
                """
                To load an assistant or create a new one, use the following methods:
                TODO: Add link to github example code.
                """
            )

        # configuration
        self._config = config
        self._api_client = api_client or AsyncAPIClient()

        # management
        self._update = _AsyncUpdate(self)
        self._interface = AsyncInterface(self._config, self._api_client)

        # essence
        self._learn = AsyncLearning(self._config, self._api_client)
        self._chat = AsyncChat(self._config, self._api_client)
        self._memory = AsyncMemory(self._config, self._api_client)

    def __setattr__(self, key: str, value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To update the assistant, use the methods assistant.update.* or create a new one.
        """
        if not key.startswith("_"):
            self._raise_setter_error(key)
        return super().__setattr__(key, value)

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the AsyncAssistant instance.
        Includes all attributes for easy inspection and debugging.
        """
        return (
            "AsyncAssistant("
            f"name={self.config.name!r}, "
            f"instructions={self.config.instructions!r}, "
            f"model={self.config.model!r}"
            ")"
        )

    def __str__(self) -> str:
        """
        Provides a user-friendly string representation of the AsyncAssistant instance.
        Gives an overview with just the assistant's name and ID.
        """
        return f"AsyncAssistant {self.config.name}"

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
        Reserved for internal use only with the create and load methods.
        Creates a new instance of the AsyncAssistant class.

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
                Unable to set attribute '{attribute}'. AsyncAssistant class is immutable and doesn't support direct attribute assignment.\n
                To update assistant, use assistant.update.* methods or create a new assistant with the desired configuration following the example below:\n\n
                
                TODO: Add link to github example code.
            """
        )

    async def delete(
        self,
        api_client: AsyncAPIClient | None = None,
        confirm: bool = False,
    ) -> None:
        """
        Deletes an existing assistant with the specified ID.

        Args:
            api_client (AsyncAPIClient, optional): The API client. Defaults to None.
        """
        if not confirm:
            raise AssistantError(
                "Assistant and all its memories will be permanently deleted. To confirm, set confirm=True."
            )

        api_client = api_client or self._api_client
        response = await api_client.delete(f"/assistant/delete/{self.config.name}")
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"An error occured while deleting the assistant {self.config.name}: {response.text}",
            )
        LOG.info(f"Successfully deleted assistant {self.config.name}.")


class _AsyncUpdate:
    """
    A collection of methods to update the configuration of the assistant.

    To update the assistant, you can use the following methods:
        assistant.update.name("Sam")
        assistant.update.instructions("You are a helpful assistant..."])
        assistant.update.inference_config(new_config)
    """

    def __init__(self, assistant: AsyncAssistant) -> None:
        """
        Initializes a new instance of the Update class.

        Args:
            assistant (AsyncAssistant): The assistant.
        """
        self._assistant = assistant

    def __setattr__(self, __name: str, __value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To change the assistant, use assistant.update.* methods or create a new one.
        """
        if not __name.startswith("_"):
            self.assistant._raise_setter_error(__name)
        return super().__setattr__(__name, __value)

    @property
    def assistant(self) -> AsyncAssistant:
        return self._assistant

    @property
    def api_client(self) -> AsyncAPIClient:
        return self.assistant.api_client

    async def instructions(self, instructions: str) -> None:
        """
        Updates the instructions of the assistant.

        Args:
            instructions (List[str]): The new instructions of the assistant.
        """
        response = await self.api_client.post(
            "/assistant/update/instructions",
            data={
                "assistant": str(self.assistant.config.name),
                "instructions": instructions,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the instructions of the assistant {self.assistant.config.name}: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            name=self.assistant._config.name,
            instructions=instructions,
            model=self.assistant._config.model,
        )

    async def model(self, new_model: INFERENCE_MODEL) -> None:
        """
        Updates the inference model of the assistant.

        Args:
            new_model (INFERENCE_MODEL): The new inference model.
        """
        response = await self.api_client.post(
            "/assistant/update/model",
            data={
                "assistant": str(self.assistant.config.name),
                "model": new_model,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the inference configuration: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            name=self.assistant._config.name,
            instructions=self.assistant._config.instructions,
            model=new_model,
        )
