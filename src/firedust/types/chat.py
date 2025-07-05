from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Sequence, Union
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

from .base import UNIX_TIMESTAMP, BaseConfig
from .tools import ToolCalls

_author = Literal["user", "assistant", "system"]


class Message(BaseConfig):
    """
    Represents a message between a user and an assistant.
    """

    type: Literal["text", "json"] = Field(
        "text",
        description="The type of the message.",
    )
    assistant: str = Field(..., description="The name of the assistant.")
    chat_group: str = Field(
        "default",
        description="The unique identifier of the chat group. All messages in a group are private.",
    )
    name: Optional[str] = Field(
        None,
        description="A name to diferentiate between users within the same chat_group. Applicable to both users and assistants.",
    )
    timestamp: UNIX_TIMESTAMP = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="The timestamp of the message.",
    )
    content: str = Field(..., description="The content of the message.")
    author: _author = Field(..., description="The author of the message.")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the message.",
    )


class UserMessage(Message):
    author: Literal["user"] = Field(
        "user",
        description="Indicates that the author of the message is the user.",
    )


class SystemMessage(Message):
    author: Literal["system"] = Field(
        "system",
        description="Indicates that the author of the message is the system.",
    )


class AssistantMessage(Message):
    author: Literal["assistant"] = Field(
        "assistant",
        description="Indicates that the author of the message is the assistant.",
    )
    tool_calls: Optional[ToolCalls] = Field(
        None,
        description="Tool calls requested by the assistant, if any.",
    )


class MessageReferences(BaseModel):
    """
    Represents the references to the memories and messages used by the assistant to generate a response.
    """

    memory_ids: Sequence[UUID] = Field(
        ..., description="The references to the relevant memories."
    )
    message_ids: Sequence[UUID] = Field(
        ..., description="The references to the relevant conversations."
    )

    @field_serializer("memory_ids", when_used="always")
    def serialize_memory_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]

    @field_serializer("message_ids", when_used="always")
    def serialize_conversation_refs(self, value: Sequence[UUID]) -> Sequence[str]:
        return [str(ref) for ref in value]


class ReferencedMessage(Message):
    references: Optional[MessageReferences] = Field(
        None,
        description="References to memories and conversations used by the assistant as context to answer the query.",
    )
    tool_calls: Optional[ToolCalls] = Field(
        None,
        description="Tool calls requested by the assistant, if any.",
    )


class MessageStreamEvent(ReferencedMessage):
    stream_ended: bool = Field(
        ..., description="Indicates whether the message stream has ended."
    )


class MessageContext(MessageReferences):
    """
    Represents the context of a message.
    """

    message_id: UUID = Field(..., description="The unique identifier of the message.")
    messages: List[Message] = Field(..., description="The messages in the chat.")
    instructions: str = Field(
        ..., description="The instructions related to the message."
    )

    @field_serializer("message_id", when_used="always")
    def serialize_message_id(self, value: UUID) -> str:
        return str(value)


# ------------------------------------------------------------------
# Response format definitions (structured outputs)
# ------------------------------------------------------------------


# ------------------------------------------------------------
# Minimal JSON Schema representation
# ------------------------------------------------------------


class JSONSchema(BaseModel):
    """A *minimal* yet **deterministic** representation of a JSON Schema.

    The goal is **not** to cover the full JSON Schema spec (which is huge) but
    to validate the subset required by Starship for structured outputs.

    The model enforces the presence of the ``type`` keyword and validates
    additional keywords for common cases (objects & arrays).  Extra fields are
    allowed so that the schema can still include other, less common keywords
    without breaking validation.
    """

    # Core keywords -----------------------------------------------------
    type: Literal[
        "object",
        "array",
        "string",
        "number",
        "integer",
        "boolean",
        "null",
    ] = Field(..., description="The JSON type the schema validates.")

    description: Optional[str] = Field(None, description="Schema description.")
    enum: Optional[List[Union[str, int, float, bool, None]]] = Field(
        None, description="Enumeration of allowed literal values."
    )

    # Object-specific keywords -----------------------------------------
    properties: Optional[Dict[str, "JSONSchema"]] = Field(
        None, description="Property definitions when type == 'object'."
    )
    required: Optional[List[str]] = Field(
        None, description="List of required property names (object schemas)."
    )
    additionalProperties: Union[bool, "JSONSchema", None] = Field(
        None,
        description=(
            "Whether additional properties are allowed (or schema for them) when type == 'object'."
        ),
    )

    # Array-specific keywords ------------------------------------------
    items: Union["JSONSchema", List["JSONSchema"], None] = Field(
        None, description="Item schema definition when type == 'array'."
    )

    class Config:
        extra = (
            "allow"  # Allow additional JSON-Schema keywords we don't explicitly model
        )

    # -----------------------------------------------------------------
    # Custom validation
    # -----------------------------------------------------------------

    @model_validator(mode="after")
    def _validate_schema(
        self,
    ) -> "JSONSchema":  # noqa: D401 – simple name is clear enough
        """Enforce minimal correctness for the supported subset."""

        if self.type == "object":
            if self.properties is None:
                raise ValueError("Object schema must include 'properties'.")
            if self.additionalProperties is None:
                raise ValueError(
                    "Object schema must explicitly set 'additionalProperties' (True/False or schema)."
                )

            # Ensure every required key exists inside properties
            if self.required is not None:
                missing = [k for k in self.required if k not in (self.properties or {})]
                if missing:
                    raise ValueError(
                        f"Required property/properties not defined in 'properties': {', '.join(missing)}"
                    )

        if self.type == "array" and self.items is None:
            raise ValueError("Array schema must include 'items'.")

        return self


class JSONSchemaConfig(BaseModel):
    """Configuration for ``json_schema`` response format (OpenAI Structured Outputs).

    strict is pinned to ``True`` to always request strict adherence, as required.
    """

    name: str = Field(
        ...,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Name of the response format (a-z, A-Z, 0-9, underscores, dashes)",
    )
    description: Optional[str] = Field(
        None,
        description="Optional description to help the model understand the format.",
    )
    schema: JSONSchema = Field(  # type: ignore[assignment]
        ...,
        alias="schema",
        serialization_alias="schema",  # pydantic ≥2.6
        description="JSON Schema describing the expected structure.",
    )
    strict: bool = Field(
        default=True,
        description="Strict schema adherence always enabled.",
    )


class ResponseFormat(BaseModel):
    """Union-like model for ``response_format`` accepted by providers."""

    type: Literal["json_schema", "text"] = Field(
        "json_schema",
        description="The type of the response format.",
    )
    json_schema: JSONSchemaConfig = Field(
        ...,
        description="The JSON schema configuration for the response format.",
    )

    @field_validator("json_schema", mode="after")
    def _validate_schema_presence(
        cls, v: Optional[JSONSchemaConfig], info: ValidationInfo
    ) -> Optional[JSONSchemaConfig]:
        r_type = (info.data or {}).get("type")
        if r_type == "json_schema" and v is None:
            raise ValueError(
                "'json_schema' must be provided when type is 'json_schema'."
            )
        if r_type == "json_object" and v is not None:
            raise ValueError("'json_schema' must be None when type is 'json_object'.")
        return v


class ResponseConfiguration(BaseModel):
    """
    Represents the configuration of the response.
    """

    character: Optional[str] = Field(
        None,
        description="The name of the persona the assistant should embody in the response. Defaults to None.",
    )
    instructions: Optional[str] = Field(
        None,
        description="Additional instructions for this specific request. These are added as a system message at the end and are not saved to memory.",
    )
    response_format: Optional[ResponseFormat] = Field(
        None,
        description="Structured output configuration forwarded to the provider APIs.",
    )


class MemoryConfiguration(BaseModel):
    add_to_memory: bool = True
    use_memory: bool = True


class ChatRequest(BaseModel):
    """
    Represents a request to chat with an assistant.
    """

    message: Message = Field(..., description="The message to chat with the assistant.")
    response_config: Optional[ResponseConfiguration] = Field(
        None, description="The configuration of the response."
    )
    memory_config: Optional[MemoryConfiguration] = Field(
        None, description="The configuration for memory behavior."
    )
