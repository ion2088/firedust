import firedust
from firedust.types import Message

# you can add previous chat history to the assistant to help
# it understand the context of the conversation and provide better answers
assistant = firedust.assistant.create("Sam")

message1 = Message(
    assistant="Sam",
    user="product_team",
    message="John: Based on the last discussion, we've made the following changes to the product...",
    author="user",
)
message2 = Message(
    assistant="Sam",
    user="product_team",
    message="Helen: John, could you please share the updated product roadmap?",
    author="user",
)
message3 = Message(
    assistant="Sam",
    user="product_team",
    message="John: Sure, the new roadmap is the following...",
    author="user",
)

assistant.chat.add_history([message1, message2, message3])

response = assistant.chat.message(
    message="Who is sharing the new product roadmap?",
    user="product_team",  # Previous conversations are available only to the same user
)
assert "John" in response.message
