# Firedust

Firedust makes it simple to build and deploy AI tools, minimizing the time from idea to working product.

## Features

### Assistants
- **Rapid Deployment**: Deploy AI assistants in seconds for quick testing and iteration.
- **Model Flexibility**: Seamlessly switch between GPT-4, Mistral, or other models to find the best fit.
- **Integration Options**: Deploy to Slack or integrate via API into your apps.
- **Real-time Training**: Add your data and train the assistant in real-time.
- **Dynamic Context Recall**: Assistants utilize past conversations and user-added data to generate responses, clearly referencing the specific data sources used in their answers.
- **Group Chat**: Support for both group and one-on-one interactions.
- **Privacy and Security**: Chats are private, with data encrypted both in transit and at rest.
- **Asynchronous Support**: Fully supports asynchronous programming.
- **Seamless Updates**: Configure and update assistants without downtime.

## Quickstart

Get your api key [here](https://tally.so/r/wbkB1L) and set it as an environment variable:
```sh
export FIREDUST_API_KEY=your_api_key
```

Install the package:
```sh
pip install firedust
```

## Examples

### Create a new assistant

Your assistant is ready to chat in seconds.

```python
import firedust

assistant = firedust.assistant.create(
    name="Samwise",
    instructions="1. Protect the ring bearer. 2. Do not let the ring corrupt you.",
    model="mistral/mistral-medium", # you can easily switch between models
)

# ask a question
question = "What is the shortest way to Mordor?"
response = assistant.chat.message(question)
print(response.message)

# stream
for event in assistant.chat.stream(question):
    print(event.message)
```

### Load an existing assistant

Load your assistants anywhere in your code to interact, add more data, deploy or change configuration.

```python
import firedust

assistant = firedust.assistant.load("Samwise")
```

### Add your data

Integrate your data into the assistant's memory for real-time accessibility. Users can effortlessly retrieve information by simply chatting with the assistant, making natural language the new way to query data.

```python
important_data = [
    "Do not trust Smeagol.",
    "The ring is evil, it must be destroyed.",
]
for data in important_data:
    assistant.learn.fast(data)

response = assistant.chat.message("What should I do with the ring?")
assert "destroy" in response.message.lower()

# see which data sources were used in the response
print(response.references)
```

### Deploy to Slack

Deploy your assistants to slack to chat in groups or one-on-one. Firedust handles the deployment, server management and scaling for you. The slack app is [open sourced](https://github.com/ion2088/firedust-slack).

```python
config_token = "CONFIGURATION_TOKEN" # you can find your configuration token here: https://api.slack.com/apps
assistant.interface.slack.create_app(
    description="A short description of the assistant.",
    greeting="A greeting message for the users.",
    configuration_token=config_token,  
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
```

### Group chat

Engage in group chats by simply annotating messages for different users. You can also add previous chat history to improve the responses.

```python
import firedust

assistant = firedust.assistant.load(name="Sam")

# add previous chat history to the assistant's memory
message1 = Message(
    assistant="Sam",
    user="product_team", # group name
    message="John: Based on the last discussion, we've made the following changes to the product...", # annotate each message with the username
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

assistant.memory.add_chat_history([message1, message2, message3])

# chat in a group
response = assistant.chat.message(
    message="Troy: @Sam, who is sharing the new product roadmap?",
    user="product_team", # group name
)
assert "John" in response.message
```

### Manage memories

Gain granular control over the assistant's memory. You can recall, add, list, retrieve, and delete data points. Assistants' memories can also be fully synced, ensuring precise management of the data available to your users.

```python
import firedust

sam = firedust.assistant.create(name="Samwise")

# add data to the assistant's memory
data = [
    "To reach Mordor, follow the path through the Mines of Moria.",
    "The ring must be destroyed in the fires of Mount Doom.",
]
for item in data:
    sam.learn.fast(item)

# list all available memories (with pagination)
memory_ids = sam.memory.list(limit=100, offset=0)

# load the content of specific memories
memories = sam.memory.get(memory_ids[:10])

# recall memories based on a query
query = "Guidance to reach Mordor."
mordor_memories = sam.memory.recall(query)

# share selected memories with another assistant
frodo = firedust.assistant.create(name="Frodo")
frodo.memory.add(mordor_memories)

# sync all memories with another assistant
sam.memory.share(assistant_receiver="Frodo")

# stop sharing memories with another assistant
sam.memory.unshare(assistant_receiver="Frodo")

# delete specific memories
sam.memory.delete(memory_ids[:10])
```

### Update assistant

Easily update configurations without downtime.

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

Conversations with the assistant are always private.

```python
import firedust

assistant = firedust.assistant.load("Sam")

user1 = "Pippin"
user2 = "Merry"

# user1 shares some important information with the assistant
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
```

### Asynchronous support

All methods support asynchronous programming. You can use the async/await syntax to interact with the assistant.

```python
import asyncio
import firedust

async def main() -> None:
    assistant = await firedust.assistant.async_load(name="Sam")

    # add data
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