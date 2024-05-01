import os
from uuid import uuid4

import firedust
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.inference import InferenceConfig
from firedust.utils.types.memory import MemoryConfig

# check if the api key is set, if not, add it
if os.environ.get("FIREDUST_API_KEY") is None:
    os.environ["FIREDUST_API_KEY"] = "your_api_key"

# create an assistant, let's name it Sam
assistant_config = AssistantConfig(
    id=uuid4(),
    name="Sam",
    instructions="You are the assistant of the ring bearer, Frodo. You must protect him at all costs.",
    memory=MemoryConfig(),
    inference=InferenceConfig(provider="openai", model="gpt-4"),
)
sam = firedust.assistant.Assistant.create(assistant_config)
