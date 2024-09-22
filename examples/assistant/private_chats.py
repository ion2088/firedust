import firedust

assistant = firedust.assistant.create("Sam")
# or load an existing assistant
assistant = firedust.assistant.load("Sam")

# all conversations are private to a given chat group and
# persist in the assistant's memory
user1 = "Pippin"
user2 = "Merry"

# user1 shares some important information which will be
# stored in the assistant's memory
assistant.chat.message(
    message="My favourite desert is cinnamon bun.",
    username=user1,
    chat_group="1",
)
response = assistant.chat.message(
    message="What is my favourite desert?",
    username=user1,
    chat_group="1",
)
assert "cinnamon bun" in response.content.lower()

# user2 has no access to this information if they are not part of the chat group
response = assistant.chat.message(
    message="What is Pippin's favourite desert?",
    username=user2,
    chat_group="2",
)
assert "cinnamon bun" not in response.content.lower()

# the conversations are private and persist in the assistant's
# memory. The assistant will recall the conversations
# to answer questions and perform tasks
