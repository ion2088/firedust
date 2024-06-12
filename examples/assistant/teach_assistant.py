import firedust

assistant = firedust.assistant.create("Sam")
# or load an existing assistant
assistant = firedust.assistant.load("Sam")

# add your data, in string format
important_data = [
    "Do not trust Smeagol.",
    "The ring is evil, it must be destroyed.",
]
for data in important_data:
    assistant.learn.fast(data)

# data becomes available in real-time
response = assistant.chat.message("What should I do with the ring?")
assert "destroy" in response.message.lower()
