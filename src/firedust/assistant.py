"""
firedust.assistant
~~~~~~~~~~~~~~~~~~

The main entry point.
This module implements the Assistant class and its related functions.

Quickstart:
    ```python
    import os
    from firedust.assistant import Assistant

    # Set your key
    os.environ["FIREDUST_API_KEY"] = "your_api_key"

    # Create a new assistant with a default configuration
    assistant = Assistant.create()

    # Train the assistant on your data
    documents = [
        "Book of the Dead...",
        "Book of the Living...",
        "Customer support examples..."
    ]

    for doc in documents:
        assistant.learn.fast(doc)

    # Chat with the assistant, training data is available immediately
    response = assistant.chat.stream("Tell me about the Book of the Dead")

    for msg in response:
        print(msg)

    # Deploy the assistant
    assistant.deploy.slack(SLACK_CONFIG)
    ```
"""

import logging
from typing import List
from uuid import UUID, uuid4

from firedust.ability._base import Abilities
from firedust.interface._base import Interface
from firedust.interface.chat import Chat
from firedust.learning._base import Learning
from firedust.memory._base import Memory
from firedust.utils.api import APIClient
from firedust.utils.errors import APIError, AssistantError
from firedust.utils.types.api import APIContent
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.inference import InferenceConfig
from firedust.utils.types.memory import MemoryConfig

DEFAULT_CONFIG = AssistantConfig(
    id=uuid4(),
    name="Sam",
    instructions="You are a helpful assistant.",
    inference=InferenceConfig(),
    memory=MemoryConfig(),
)
LOG = logging.getLogger("firedust")

_start_assistant_example = """
    ```py
    from firedust.assistant import Assistant \n\n

    new_assistant = Assistant.create(assistant_config) \n
    existing_assistant = Assistant.load(assistant_id)

    # See available assistants
    assistants_list = Assistant.list()
    ````
"""


class Assistant:
    """
    The Assistant class is the main entry point for interacting with Firedust.
    It is used to create, load, train, deploy and interact with an AI assistant.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (APIClient): The API client.
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
    _api_client: APIClient

    _update: "_Update"
    _interface: Interface
    _learn: Learning
    _chat: Chat
    _memory: Memory
    _ability: Abilities

    # assistant should be instantiated using the create and load classmethods
    _allow_instantiation: bool = False

    def __init__(
        self, config: AssistantConfig, api_client: APIClient | None = None
    ) -> None:
        f"""
        Initializes a new instance of the Assistant class.

        To create or load an assistant, use the following methods:
        { _start_assistant_example }

        Args:
            config (AssistantConfig, optional): The assistant configuration. Defaults to DEFAULT_CONFIG.
            api_client (APIClient, optional): The API client. Defaults to None.
        """

        # prevent direct instantiation
        if not self._allow_instantiation:
            raise AssistantError(
                f"""
                To load an assistant or create a new one, use the following methods: \n\n
                
                { _start_assistant_example }
                """
            )

        # configuration
        self._config = config
        self._api_client = api_client or APIClient()

        # management
        self._update = _Update(self)
        self._interface = Interface(self._config, self._api_client)

        # essence
        self._learn = Learning(self._config, self._api_client)
        self._chat = Chat(self._config, self._api_client)
        self._memory = Memory(self._config, self._api_client)
        self._ability = Abilities(self._config, self._api_client)

    def __setattr__(self, key: str, value: str) -> None:
        """
        Raise a custom error when trying to set an attribute directly.
        To update the assistant, use the methods assistant.update.* or create a new one.
        """
        if not key.startswith("_"):
            self._raise_setter_error(key)
        return super().__setattr__(key, value)

    @property
    def config(self) -> AssistantConfig:
        return self._config

    @property
    def api_client(self) -> APIClient:
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

    @property
    def ability(self) -> Abilities:
        return self._ability

    @classmethod
    def _create_instance(
        cls, config: AssistantConfig, api_client: APIClient
    ) -> "Assistant":
        """
        Reserved for internal use only with the create and load methods.
        Creates a new instance of the Assistant class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.

        Returns:
            Assistant: A new instance of the Assistant class.
        """
        cls._allow_instantiation = True
        assistant = cls(config, api_client)
        cls._allow_instantiation = False
        return assistant

    @classmethod
    def create(
        cls,
        config: AssistantConfig = DEFAULT_CONFIG,
        api_client: APIClient | None = None,
    ) -> "Assistant":
        """
        Creates a new assistant with the specified configuration.

        Args:
            config (AssistantConfig): The assistant configuration. Defaults to DEFAULT_CONFIG.
            api_client (APIClient, optional): The API client. Defaults to None.

        Returns:
            Assistant: A new instance of the Assistant class.
        """
        api_client = api_client or APIClient()
        response = api_client.post("/assistant/create", data=config.model_dump())
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to create the assistant with config {config}: {response.text}",
            )
        LOG.info(
            f"Assistant {config.name} (ID: {config.id}) was created successfully and saved to the cloud."
        )
        return cls._create_instance(config, api_client)

    @classmethod
    def load(
        cls, assistant_id: UUID, api_client: APIClient | None = None
    ) -> "Assistant":
        """
        Loads an existing assistant with the specified ID.

        Args:
            assistant_id (UUID): The unique identifier of the assistant.
            api_client (APIClient, optional): The API client. Defaults to None.

        Returns:
            Assistant: A new instance of the Assistant class.
        """
        api_client = api_client or APIClient()
        response = api_client.get(f"/assistant/{assistant_id}/load")
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to load the assistant with id {assistant_id}: {response.text}",
            )
        content = APIContent(**response.json())
        config = AssistantConfig(**content.data["assistant"])
        return cls._create_instance(config, api_client)

    @staticmethod
    def list(api_client: APIClient | None = None) -> List[AssistantConfig]:
        """
        Lists all the existing assistants.

        Args:
            api_client (APIClient, optional): The API client. Defaults to None.
        """
        api_client = api_client or APIClient()
        response = api_client.get("/assistant/list")
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to list the assistants: {response.text}",
            )
        content = APIContent(**response.json())
        return [
            AssistantConfig(**assistant) for assistant in content.data["assistants"]
        ]

    @staticmethod
    def delete(
        assistant_id: UUID,
        api_client: APIClient | None = None,
        confirm_delete: bool = False,
    ) -> None:
        """
        Deletes an existing assistant with the specified ID.

        Args:
            assistant_id (UUID): The unique identifier of the assistant.
            api_client (APIClient, optional): The API client. Defaults to None.
        """
        if not confirm_delete:
            raise AssistantError(
                "Assistant and all its memories will be permanently deleted. To confirm, set confirm_delete=True."
            )

        api_client = api_client or APIClient()
        response = api_client.delete(f"/assistant/{assistant_id}/delete")
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"An error occured while deleting the assistant with id {assistant_id}: {response.text}",
            )
        LOG.info(f"Successfully deleted assistant {assistant_id}.")
        return

    @staticmethod
    def _raise_setter_error(attribute: str) -> None:
        raise AttributeError(
            f"""
                Unable to set attribute '{attribute}'. Assistant class is immutable and doesn't support direct attribute assignment.\n
                To update assistant, use assistant.update.* methods or create a new assistant with the desired configuration following the example below:\n\n
                { _start_assistant_example }
            """
        )


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
    def api_client(self) -> APIClient:
        return self.assistant.api_client

    def name(self, name: str) -> None:
        """
        Updates the name of the assistant.

        Args:
            name (str): The new name of the assistant.
        """
        response = self.api_client.put(
            f"/assistant/{self.assistant.config.id}/update/name/{name}",
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the name of the assistant with id {self.assistant.config.id}: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            id=self.assistant._config.id,
            name=name,
            instructions=self.assistant._config.instructions,
            inference=self.assistant._config.inference,
            memory=self.assistant._config.memory,
        )

    def instructions(self, instructions: str) -> None:
        """
        Updates the instructions of the assistant.

        Args:
            instructions (List[str]): The new instructions of the assistant.
        """
        response = self.api_client.post(
            "/assistant/update/instructions",
            data={
                "assistant_id": str(self.assistant.config.id),
                "instructions": instructions,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the instructions of the assistant with id {self.assistant.config.id}: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            id=self.assistant._config.id,
            name=self.assistant._config.name,
            instructions=instructions,
            inference=self.assistant._config.inference,
            memory=self.assistant._config.memory,
        )

    def inference(self, inference_config: InferenceConfig) -> None:
        """
        Updates the inference configuration of the assistant.

        Args:
            inference_config (InferenceConfig): The new inference configuration.
        """
        response = self.api_client.post(
            "/assistant/update/inference",
            data={
                "assistant_id": str(self.assistant.config.id),
                "inference": inference_config.model_dump(),
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update the inference configuration of the assistant with id {self.assistant.config.id}: {response.text}",
            )
        self.assistant._config = AssistantConfig(
            id=self.assistant._config.id,
            name=self.assistant._config.name,
            instructions=self.assistant._config.instructions,
            inference=inference_config,
            memory=self.assistant._config.memory,
        )
