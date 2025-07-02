from typing import Any, Dict, List, Literal, Mapping, Optional

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypeAlias

# ----------------------------------------------------------------------------
# Tool definition types (what CAN the model call?)
# ----------------------------------------------------------------------------

# A [JSON Schema](https://json-schema.org/) object represented as an ordinary
# ``dict``.
JSONSchema: TypeAlias = Dict[str, Any]

# The only supported tool *type* at the moment.
FUNCTION_TOOL_TYPE = Literal["function"]


class FunctionDefinition(BaseModel):
    """Definition of a callable function exposed to the model.

    The structure follows the OpenAI specification exactly::

        {
          "name": "search_documents",
          "description": "Short description of what the function does",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {"type": "string", "description": "..."}
            },
            "required": ["query"]
          }
        }
    """

    name: str = Field(..., description="The function name. Must be a valid identifier.")
    description: Optional[str] = Field(
        None, description="A short, human-readable description of the function."
    )
    parameters: JSONSchema = Field(
        default_factory=dict,
        description=(
            "JSON-Schema definition of the function parameters. Must follow the "
            "Draft-07 (or later) specification and use an *object* as the root "
            "schema."
        ),
        examples=[
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            }
        ],
    )

    # ---------------------------------------------------------------------
    # Validators
    # ---------------------------------------------------------------------

    @field_validator("parameters", mode="before")
    @classmethod
    def _validate_root_schema(cls, v: JSONSchema) -> JSONSchema:
        """Ensure the *parameters* schema complies with the basic requirements."""
        # Basic structural validation — this is *not* a full JSON-Schema validator.
        if not isinstance(v, Mapping):
            raise ValueError("Parameters must be a mapping (JSON object).")

        if v.get("type") != "object":
            raise ValueError("Top-level 'type' must be 'object'.")

        if "properties" not in v:
            raise ValueError("Schema must contain a 'properties' key.")

        if not isinstance(v["properties"], Mapping):
            raise ValueError("'properties' must be an object.")

        return v


class Tool(BaseModel):
    """Representation of a *function* tool accepted by OpenAI APIs."""

    type: FUNCTION_TOOL_TYPE = Field("function")
    function: FunctionDefinition


Tools = List[Tool]
"""Convenience alias for a list of :class:`Tool` objects."""

# ----------------------------------------------------------------------------
# Function-call invocation types (what DID the model call?)
# ----------------------------------------------------------------------------


class FunctionCall(BaseModel):
    """Arguments of a *function* tool invocation returned by the model."""

    name: str = Field(..., description="The name of the function to invoke.")
    arguments: str = Field(
        ...,
        description="A JSON-encoded string with the function call arguments.",
    )


class ToolCall(BaseModel):
    """Single tool-call element in ``choices.message.tool_calls`` from OpenAI."""

    id: str = Field(..., description="Unique identifier of the tool call.")
    type: FUNCTION_TOOL_TYPE = Field("function")
    function: FunctionCall = Field(..., description="The function call details.")


ToolCalls = List[ToolCall]
"""Convenience alias for a list of :class:`ToolCall` objects."""
