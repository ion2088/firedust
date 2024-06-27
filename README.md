# Firedust

Firedust makes it simple to build and deploy AI tools. It is designed to minimize the time from idea to working product. It abstracts away the complexity of building and deploying AI tools and allows you to focus on the core of your idea. It takes care of the memory persistance, context management, storage and deployment of your AI tools. Privacy and data encryption comes as default.

## Features

### Assistants
- Build and deploy AI assistants in seconds
- Deploy to Slack or use the API to integrate in your own app
- Add your own data and train the assistant in real-time
- Chat in groups or one-on-one
- Privacy and data encryption comes as default
- Asynchronous support
- Load and use anywhere
- Easily configure and update your assitants without downtime. Would you like to switch from GPT4 to Mistral? It takes one line of code and zero downtime.

## Quickstart

Get your api key here: [Firedust](https://firedust.ai) and set it as an environment variable.

```sh
export FIREDUST_API_KEY=your_api_key
```

Install the python package using pip, poetry or any other package manager.
```sh
pip install firedust
```

## Examples

### Create a new assistant
```python
import firedust

assistant = firedust.assistant.create("Samwise")

# ask a question
question = "What is the shortest way to Mordor?"
response = assistant.chat.message(question)
print(response.message)

# stream
for event in assistant.chat.stream(question):
    print(event.message)
```

### Load an existing assistant
```python
import firedust

assistant = firedust.assistant.load("Samwise")
```

### Add your data
```python
import firedust

assistant = firedust.assistant.load("Samwise")

important_data = [
    "Do not trust Smeagol.",
    "The ring is evil, it must be destroyed.",
]
for data in important_data:
    assistant.learn.fast(data)

# data becomes available in real-time
response = assistant.chat.message("What should I do with the ring?")
assert "destroy" in response.message.lower()
```

### Deploy to Slack
```python
import firedust

assistant = firedust.assistant.load(name="Samwise")

# create a slack app
assistant.interface.slack.create_app(
    description="A short description of the assistant.",
    greeting="A greeting message for the users.",
    configuration_token="CONFIGURATION_TOKEN",  # you can find your configuration token here: https://api.slack.com/apps
)

# install the app in your slack workspace UI and generate tokens. See here: https://api.slack.com/apps/
app_token = "APP_TOKEN"
bot_token = "BOT_TOKEN"

# set the tokens
assistant.interface.slack.set_tokens(
    app_token=app_token,
    bot_token=bot_token,
)

# deploy the assistant
assistant.interface.slack.deploy()

# That's it. Now you can interact with the assistant in your Slack workspace!
```

### Manage memories
```python
import firedust

sam = firedust.assistant.create(name="Samwise")
# or load an existing assistant
sam = firedust.assistant.load(name="Samwise")

# add some data to the memory
data = [
    "To reach Mordor, follow the path through the Mines of Moria.",
    "The ring must be destroyed in the fires of Mount Doom.",
]
for item in data:
    sam.learn.fast(item)

# list all available memories
memory_ids = sam.memory.list(limit=100, offset=0)

# load memory content
memories = sam.memory.get(memory_ids[:10])

# recall memories by query
query = "Guidance to reach Mordor."
mordor_memories = sam.memory.recall(query)

# add selected memories to another assistant
frodo = firedust.assistant.create(name="Frodo")
frodo.memory.add(mordor_memories)

# share all memories with another assistant, this
# is a full memory sync and applies to existing memories as well
# as the ones created in the future
sam.memory.share(assistant_receiver="Frodo")

# stop sharing memories
sam.memory.unshare(assistant_receiver="Frodo")

# delete memories
sam.memory.delete(memory_ids[:10])
```

### Update assistant
```python
import firedust

assistant = firedust.assistant.load(name="Sam")

# update the assistant's inference model
assistant.update.model("mistral/mistral-medium")

# update the assistant's instructions
assistant.update.instructions(
    """
    1. Protect the ring bearer. 
    2. Do not let the ring corrupt you.
    """
)

# all changes are saved and applied immediately
```

### User privacy
```python
import firedust

assistant = firedust.assistant.create("Sam")
# or load an existing assistant
assistant = firedust.assistant.load("Sam")

# all conversations are private and persist in the assistant's memory
user1 = "Pippin"
user2 = "Merry"

# user1 shares some important information which will be
# stored in the assistant's memory
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

# the conversations are private and persist in the assistant's memory. The assistant will recall the conversations to answer questions and perform tasks
```

### Asynchronous support
```python

import asyncio

import firedust

# to use async, you just need to create or load the assistant using dedicated async functions all the other methods are mirrored


async def main() -> None:
    assistant = await firedust.assistant.async_create(name="Sam")
    # or load an existing one
    assistant = await firedust.assistant.async_load(name="Sam")

    # add some data
    await assistant.learn.fast("Gandalf is a good friend.")

    # chat
    response = await assistant.chat.message("Who is Gandalf?")
    assert "friend" in response.message.lower()

    # stream
    async for event in assistant.chat.stream("Who is Gandalf?"):
        print(event.message)

    # delete assistant
    await assistant.delete(confirm=True)


asyncio.run(main())
```
