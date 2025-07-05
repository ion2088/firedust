# isort: skip_file
"""
Make the main types easily accessible.

```python
from firedust.types import Assistant, AssistantConfig, Message, ReferencedMessage, MessageStreamEvent, ResponseFormat, ResponseConfiguration, MemoryConfiguration, ChatRequest, JSONSchema, JSONSchemaConfig, UserMessage, SystemMessage, AssistantMessage, MemoryItem, APIContent, INFERENCE_MODEL

def custom_funk(assistant: Assistant) -> ...:
    ...
```
"""

from firedust.types.assistant import AssistantConfig as AssistantConfig
from firedust.types.chat import (
    Message as Message,
    ReferencedMessage as ReferencedMessage,
    MessageStreamEvent as MessageStreamEvent,
    ResponseFormat as ResponseFormat,
    ResponseConfiguration as ResponseConfiguration,
    MemoryConfiguration as MemoryConfiguration,
    ChatRequest as ChatRequest,
    JSONSchema as JSONSchema,
    JSONSchemaConfig as JSONSchemaConfig,
    UserMessage as UserMessage,
    SystemMessage as SystemMessage,
    AssistantMessage as AssistantMessage,
    MessageReferences as MessageReferences,
    MessageContext as MessageContext,
)
from firedust.types.base import INFERENCE_MODEL as INFERENCE_MODEL
from firedust.types.memory import MemoryItem as MemoryItem
from firedust.types.api import APIContent as APIContent
from firedust.types.tools import (
    Tools,
    ToolCalls,
    Tool,
    FunctionDefinition,
    ToolCall,
    FunctionCall,
)
from firedust._assistant.base.assistant import (
    Assistant as Assistant,
    AsyncAssistant as AsyncAssistant,
)
from .safety import SafetyCheck

__all__ = [
    "Assistant",
    "AsyncAssistant",
    "AssistantConfig",
    "Message",
    "ReferencedMessage",
    "MessageStreamEvent",
    "ResponseFormat",
    "ResponseConfiguration",
    "MemoryConfiguration",
    "ChatRequest",
    "JSONSchema",
    "JSONSchemaConfig",
    "UserMessage",
    "SystemMessage",
    "AssistantMessage",
    "MessageReferences",
    "MessageContext",
    "MemoryItem",
    "APIContent",
    "INFERENCE_MODEL",
    "SafetyCheck",
    "Tools",
    "ToolCalls",
    "Tool",
    "FunctionDefinition",
    "ToolCall",
    "FunctionCall",
]
