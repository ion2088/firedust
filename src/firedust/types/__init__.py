# isort: skip_file
"""
Make the main types easily accessible.

```python
from firedust.types import Assistant, AssistantConfig, Message, ReferencedMessage, MessageStreamEvent, StructuredAssistantMessage, StructuredUserMessage, STRUCTURED_SCHEMA, BooleanField, DictField, FloatField, ListField, CategoryField, StringField, MemoryItem, APIContent, INFERENCE_MODEL

def custom_funk(assistant: Assistant) -> ...:
    ...
```
"""

from firedust.types.assistant import AssistantConfig as AssistantConfig
from firedust.types.chat import (
    Message as Message,
    ReferencedMessage as ReferencedMessage,
    MessageStreamEvent as MessageStreamEvent,
    StructuredAssistantMessage as StructuredAssistantMessage,
    StructuredUserMessage as StructuredUserMessage,
)
from firedust.types.structured import (
    STRUCTURED_SCHEMA as STRUCTURED_SCHEMA,
    BooleanField as BooleanField,
    DictField as DictField,
    FloatField as FloatField,
    ListField as ListField,
    CategoryField as CategoryField,
    StringField as StringField,
)
from firedust.types.base import INFERENCE_MODEL as INFERENCE_MODEL
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
    "STRUCTURED_SCHEMA",
    "BooleanField",
    "DictField",
    "FloatField",
    "ListField",
    "CategoryField",
    "StringField",
    "StructuredAssistantMessage",
    "StructuredUserMessage",
    "INFERENCE_MODEL",
]
