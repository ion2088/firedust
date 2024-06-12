import asyncio

import firedust

# assistant supports async operations
# to use async, you just need to create or load the assistant
# using dedicated async functions. All other operations are mirrored


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
