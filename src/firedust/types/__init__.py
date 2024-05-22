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
from firedust.types.assistant import AssistantMessage as AssistantMessage
from firedust.types.assistant import Message as Message
from firedust.types.assistant import UserMessage as UserMessage
from firedust.types.memory import MemoryItem as MemoryItem
from firedust.types.api import APIContent as APIContent
from firedust._assistant.base.assistant import Assistant as Assistant
from firedust._assistant.base.assistant import AsyncAssistant as AsyncAssistant


__all__ = [
    "Assistant",
    "AsyncAssistant",
    "AssistantConfig",
    "Message",
    "UserMessage",
    "AssistantMessage",
    "MemoryItem",
    "APIContent",
]
