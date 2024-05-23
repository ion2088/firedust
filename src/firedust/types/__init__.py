# isort: skip_file
"""
Make the main types easily accessible.

```python
from firedust.types import Assistant

def custom_funk(assistant: Assistant) -> ...:
    ...
```
"""

from firedust.types.assistant import AssistantConfig as AssistantConfig
from firedust.types.chat import (
    Message as Message,
    ReferencedMessage as ReferencedMessage,
    MessageStreamEvent as MessageStreamEvent,
)
from firedust.types.memory import MemoryItem as MemoryItem
from firedust.types.api import APIContent as APIContent
from firedust._assistant.base.assistant import (
    Assistant as Assistant,
    AsyncAssistant as AsyncAssistant,
)

__all__ = [
    "Assistant",
    "AsyncAssistant",
    "AssistantConfig",
    "Message",
    "ReferencedMessage",
    "MessageStreamEvent",
    "MemoryItem",
    "APIContent",
]
