import firedust

# create a new assistant
assistant = firedust.assistant.create(
    name="Sam",
    instructions="""
        1. Assume the character of Samwise Gamgee from The Lord of the Rings. Do not break character.
        2. Protect the ring bearer. 
        3. Do not let the ring corrupt you.
        """,
    model="openai/gpt-4o",
)

# ask a question
question = "What is the shortest way to Mordor?"
response = assistant.chat.message(question)
print(response.content)

# stream messages
for event in assistant.chat.stream(question):
    print(event.content)

# add your data to the assistant's memory
important_data = [
    "Do not trust Smeagol.",
    "The ring is evil, it must be destroyed.",
]
for data in important_data:
    assistant.learn.fast(data)

# data becomes available in real-time
response = assistant.chat.message("What should I do with the ring?")
assert "destroy" in response.content.lower()

# recall memories
memories = assistant.memory.recall("Information about Smeagol.")
any("Do not trust Smeagol." in m.content for m in memories)

# list all available assistants
all_assistants = firedust.assistant.list()

# load an existing assistant
assistant = firedust.assistant.load(name="Sam")

# delete an assistant
assistant.delete(confirm=True)
