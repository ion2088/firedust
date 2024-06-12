import firedust

# you can create an assistant
assistant = firedust.assistant.create(name="Sam")
# or load an existing one anywhere in your code
assistant = firedust.assistant.load(name="Sam")

# add more data
assistant.learn.fast("Gandalf is a good friend.")

# data becomes available in real-time and persists in memory
response = assistant.chat.message("Who is Gandalf?")
assert "friend" in response.message.lower()
