# FILEPATH: /firedust/tests/test_assistant.py
from unittest.mock import MagicMock, patch

from firedust._utils.types.assistant import AssistantConfig
from firedust.ability._base import Abilities
from firedust.assistant import Assistant, Update, connect
from firedust.interface._base import Interface
from firedust.interface.chat import Chat
from firedust.learning._base import Learning
from firedust.memory._base import Memory


@patch("firedust.assistant.APIClient.post")
def test_assistant_initialization(mock_post: MagicMock) -> None:
    connect(api_key="test_key")
    config = AssistantConfig()
    assistant = Assistant(config)

    assert isinstance(assistant.config, AssistantConfig)
    assert isinstance(assistant.update, Update)
    assert isinstance(assistant.interface, Interface)
    assert isinstance(assistant.learn, Learning)
    assert isinstance(assistant.chat, Chat)
    assert isinstance(assistant.memory, Memory)
    assert isinstance(assistant.ability, Abilities)


@patch("firedust.assistant.APIClient.post")
def test_assistant_repr(mock_post: MagicMock) -> None:
    connect(api_key="test_key")
    config = AssistantConfig()
    assistant = Assistant(config)

    assert repr(assistant) == f"<{assistant.__class__.__name__}>\n\n{assistant.config}"
