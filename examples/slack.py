from uuid import uuid4

import firedust
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.inference import InferenceConfig
from firedust._utils.types.interface import SlackTokens
from firedust._utils.types.memory import MemoryConfig

# TODO: Remove AssistantConfig from the parameters and add them separately
# TODO: Simplify AssistantConfig - simplify memory, inference, remove id
# TODO: Change used_id parameters to user
# TODO: Remove memories collection concept - memories are tied to the assistant and can be shared among them
# TODO: Interact with assistants (create/delete etc) just by name - it has to be unique
# TODO: Remvove .create and .load from the assistant class, add them to firedust.assistant.*
# TODO: Make .delete a class component joe.delte(joe.config.id) is ridiculous
# TODO: Add some kind of pretty print to show when the assistant is called. Reference the github page with the examples.
# TODO: Having both config and assistant_config in SlackInterface is clunky, we need to refactor that.
# TODO: Add a readme to the slackapp and slack interface folders
# TODO: Instead of httpx.Response, return an APIResponse in firedust._utils.api
# TODO: Update starship to use response.is_success and always return an APIResponse

# STEP 1
# add your slack configuration token, you can find it here: https://api.slack.com/apps
SLACK_CONFIGURATION_ACCESS_TOKEN = "xoxe.xoxp-1-Mi0yLTY4MDA5NjI4MDg2MjQtNjc5MDgzMjE2ODY0MS02ODMwMjc0MTcwMTE5LTcwNDI0NzYwNTUxNTItYzhhYTA5NTMxYmY0ZDQ3MzY5YTdjNWI2OGEyYjVkNTJhZjAyZDY3YWM0YmJlZTc5ZjYxMjkzZjdmNjk1YTA2YQ"

# create an assistant, let's name it Joe
assistant_config = AssistantConfig(
    id=uuid4(),
    name="Joe",
    instructions="Joe likes pizza, NY Knicks and can give you a 'How you doin?' when you need it most.",
    memory=MemoryConfig(),
    inference=InferenceConfig(provider="openai", model="gpt-4"),
)
joe = firedust.assistant.Assistant.create(assistant_config)

# create a slack app for the assistant
joe.interface.slack.create_app(
    description="A short description of the assistant. This will be displayed in .",
    configuration_token=SLACK_CONFIGURATION_ACCESS_TOKEN,
)

# STEP 2
# install the app in your slack workspace and generate tokens. See here: https://api.slack.com/apps/
SLACK_APP_TOKEN = "xapp-1-A070FC8FEUW-7024538598692-66911ca67ea7db95b85715c8e7f146c1708c3b9c8c10daa5a1d8ee0ba9096b7b"
SLACK_BOT_TOKEN = "xoxb-6800962808624-7007527987511-172tvospuZv01hmx77QaX3Yq"

joe.interface.slack.set_tokens(
    tokens=SlackTokens(app_token=SLACK_APP_TOKEN, bot_token=SLACK_BOT_TOKEN)
)

# STEP 3
# deploy the assistant
joe.interface.slack.deploy()

# Now you can interact with the assistant in your Slack workspace!
