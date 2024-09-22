from datetime import datetime
from typing import List, Literal, Optional, Sequence
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from .base import UNIX_TIMESTAMP, BaseConfig
from .structured import STRUCTURED_RESPONSE, STRUCTURED_SCHEMA


class Message(BaseConfig):
    """
    Represents a message between a user and an assistant.
    """

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
    content: str = Field(..., description="The text of the message.")
    author: Literal["user", "assistant"] = Field(
        ..., description="The author of the message."
    )


class UserMessage(Message):
    author: Literal["user"] = Field(
        "user",
        description="Indicates that the author of the message is the user.",
    )


class StructuredUserMessage(UserMessage):
    schema_: STRUCTURED_SCHEMA = Field(
        ..., description="The schema of the structured request."
    )


class AssistantMessage(Message):
    author: Literal["assistant"] = Field(
        "assistant",
        description="Indicates that the author of the message is the assistant.",
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


class StructuredAssistantMessage(BaseConfig):
    # Unable to build of AssistantMessage because we redefine message type
    assistant: str = Field(..., description="The name of the assistant.")
    chat_group: str = Field(
        "default",
        description="The unique identifier of the chat group. All messages in a group are private.",
    )
    name: Optional[str] = Field(
        None,
        description="A username to diferentiate between users with the same chat_group. Applicable to both users and assistants.",
    )
    timestamp: UNIX_TIMESTAMP = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="The timestamp of the message.",
    )
    content: STRUCTURED_RESPONSE = Field(
        ..., description="The schema of the structured request."
    )
    author: Literal["assistant"] = Field(
        "assistant",
        description="Indicates that the author of the message is the assistant.",
    )
    references: Optional[MessageReferences] = Field(
        None,
        description="References to memories and conversations used by the assistant as context to answer the query.",
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


# from datetime import datetime
# from typing import Literal, Optional, Sequence, Union
# from uuid import UUID

# from pydantic import BaseModel, Field, field_serializer

# from .base import UNIX_TIMESTAMP, BaseConfig
# from .structured import STRUCTURED_RESPONSE, STRUCTURED_SCHEMA


# class Message(BaseConfig, frozen=True):
#     """
#     Represents a message between a user and an assistant.

#     Args:
#         assistant (str): The name of the assistant.
#         user (str): The unique identifier of the user.
#         timestamp (UNIX_TIMESTAMP): The timestamp of the message.
#         message (str): The text of the message.
#         author (Literal["user", "assistant"]): The author of the message.
#     """

#     assistant: str = Field(...)
#     user: str = Field(...)
#     timestamp: UNIX_TIMESTAMP = Field(
#         default_factory=lambda: datetime.now().timestamp()
#     )
#     message: str = Field(...)
#     author: Literal["user", "assistant"] = Field(...)


# class UserMessage(Message):
#     author: Literal["user"] = Field(default="user")


# class StructuredUserMessage(UserMessage):
#     schema_: STRUCTURED_SCHEMA = Field(...)


# class AssistantMessage(Message):
#     author: Literal["assistant"] = Field(default="assistant")


# class MessageReferences(BaseModel):
#     """
#     References to the memories and messages used by the assistant as context to generate a response.

#     Args:
#         memories (Sequence[UUID]): The references to the relevant memories.
#         conversations (Sequence[UUID]): The references to the relevant conversations.
#     """

#     memories: Sequence[UUID] = Field(...)
#     conversations: Sequence[UUID] = Field(...)

#     @field_serializer("memories", when_used="always")
#     def serialize_memory_refs(self, value: Sequence[UUID]) -> Sequence[str]:
#         return [str(ref) for ref in value]

#     @field_serializer("conversations", when_used="always")
#     def serialize_conversation_refs(self, value: Sequence[UUID]) -> Sequence[str]:
#         return [str(ref) for ref in value]


# class StructuredAssistantMessage(BaseConfig, frozen=True):
#     assistant: str = Field(...)
#     user: str = Field(...)
#     timestamp: UNIX_TIMESTAMP = Field(...)
#     message: STRUCTURED_RESPONSE = Field(...)
#     author: Literal["assistant"] = Field(default="assistant")
#     references: Union[MessageReferences, None] = Field(default=None)


# class ReferencedMessage(Message, frozen=True):
#     references: Optional[MessageReferences] = Field(default=None)


# class MessageStreamEvent(ReferencedMessage, frozen=True):
#     stream_ended: bool = Field(...)
