# Firedust

Firedust makes it simple to build and deploy AI tools. It is designed to minimize the time from idea to working product. It abstracts away the complexity of building and deploying AI tools and allows you to focus on the core of your idea. It takes care of the memory persistance, context management, storage and deployment of your AI tools. Privacy and data encryption comes as default.

## Features

### Assistants
- **Rapid Deployment**: Build and deploy AI assistants in seconds, allowing you to quickly test and iterate on your ideas.
- **Model Flexibility**: Use GPT-4, Mistral, or any other model and switch between them effortlessly to find the best fit for your application.
- **Integration Options**: Deploy to Slack or use the API to integrate into your own app, making it easy to incorporate AI into your existing workflows.
- **Real-time Training**: Add your data and train the assistant in real-time, ensuring that it can provide up-to-date and relevant responses.
- **Group Chat**: Support for group chats or one-on-one interactions, catering to different communication needs.
- **Privacy and Security**: Privacy and data encryption come as default, protecting user data and maintaining trust.
- **Asynchronous Support**: Fully supports asynchronous programming for non-blocking operations, enhancing performance in high-traffic scenarios.
- **Seamless Updates**: Easily configure and update your assistants without downtime, ensuring continuous availability and improvement.

## Quickstart

Get your api key [here](https://firedust.ai) and set it as an environment variable.

```sh
export FIREDUST_API_KEY=your_api_key
```

Install the python package using pip, poetry or any other package manager.
```sh
pip install firedust
```

## Examples

### Create a new assistant

Your assistant is ready to chat in seconds.

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

Your assistants are saved and you can load them anywhere in your code to interact with them, add more data, deploy or change configuration.

```python
import firedust

assistant = firedust.assistant.load("Samwise")
```

### Add your data

Add your data to the assistant's memory to make it available in real-time. It's like a database that your users can access by simply chatting with your assistant. Natural language is the new SQL.


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

Deploy your assistants to slack to chat in groups or one-on-one. Firedust handles the deployment, server management and scaling for you. The slack app is open sourced. You can self-host it or improve. [Source code](https://github.com/ion2088/firedust-slack)

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

The assistant's memory can be managed in real-time. You can add, list, get, delete and share memories with other assistants. It allows you granular control over what data is available to your users.

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

You can easily update the assistant's configuration without any downtime. Would like to switch the inference model from GPT-4 to Mistral, or update the instructions? No problem, you can do it in a few lines of code.

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

The assistant's memories can be used to answer questions for all users, but the conversations themselves are always private. 

```python
import firedust

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
