import firedust
from firedust.types import Message

# you can add previous chat history to the assistant to help
# it understand the context of the conversation and provide better answers
assistant = firedust.assistant.create("Sam")

message1 = Message(
    assistant="Sam",
    chat_group="product_team",
    content="Based on the last discussion, we've made the following changes to the product...",
    author="user",
    username="John",
)
message2 = Message(
    assistant="Sam",
    chat_group="product_team",
    content="John, could you please share the updated product roadmap?",
    author="user",
    username="Helen",
)
message3 = Message(
    assistant="Sam",
    chat_group="product_team",
    content="Sure, the new roadmap is the following...",
    author="user",
    username="John",
)

assistant.chat.add_history([message1, message2, message3])

response = assistant.chat.message(
    message="Who is sharing the new product roadmap?",
    chat_group="product_team",  # Previous conversations are available only to the same user
)
assert "John" in response.content
