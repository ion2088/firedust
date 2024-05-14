import os

import firedust

# check if the api key is set, if not, add it
if os.environ.get("FIREDUST_API_KEY") is None:
    os.environ["FIREDUST_API_KEY"] = "your_api_key"

# create an assistant, let's name it Sam
sam = firedust.assistant.create(
    name="Sam",
    instructions="You are the assistant of the ring bearer, Frodo. You must protect him at all costs.",
)
