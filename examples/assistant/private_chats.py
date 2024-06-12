import firedust

assistant = firedust.assistant.create("Sam")
# or load an existing assistant
assistant = firedust.assistant.load("Sam")

# all conversations are private to a given user and
# persist in the assistant's memory
user1 = "Pippin"
user2 = "Merry"

# user1 shares some important information that the
# assistant will remember
assistant.chat.message(
    message="My favourite desert is cinnamon bun.",
    user=user1,
)
response = assistant.chat.message(
    message="What is my favourite desert?",
    user=user1,
)
assert "cinnamon bun" in response.message.lower()

# user2 has no access to this information
response = assistant.chat.message(
    message="What is Pippin's favourite desert?",
    user=user2,
)
assert "cinnamon bun" not in response.message.lower()

# the conversations are private and persist in the assistant's
# memory. The assistant will recall the conversations
# to answer questions and perform tasks
