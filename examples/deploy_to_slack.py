import firedust
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.inference import InferenceConfig
from firedust.utils.types.interface import SlackTokens
from firedust.utils.types.memory import MemoryConfig

# TODO: Remove AssistantConfig from the parameters and add them separately
# TODO: Simplify AssistantConfig - simplify memory, inference, remove id
# TODO: Change used_id parameters to user
# TODO: Remove memories collection concept - memories are tied to the assistant and can be shared among them
# TODO: Interact with assistants (create/delete etc) just by name - it has to be unique
# TODO: Remvove .create and .load from the assistant class, add them to firedust.assistant.*
# TODO: Make .delete a class component joe.delete(joe.config.id) is ridiculous
# TODO: Add some kind of pretty print to show when the assistant is called. Reference the github page with the examples.
# TODO: Having both config and assistant_config in SlackInterface is clunky, we need to refactor that.
# TODO: Add a readme to the slackapp and slack interface folders
# TODO: Instead of httpx.Response, return an APIResponse in firedust._utils.api
# TODO: Update starship to use response.is_success and always return an APIResponse
# TODO: Files that should not be accessed by end users should be market with a leading underscore.
# TODO: Add a way to get the assistant by name, not by id
# TODO: Add git tags to each incremental change in version <git tag> before push
# TODO: Add wrapper to firedust and slackapp to assign a error id and encourage users to contact support@firedust.com

# STEP 1
# add your slack configuration token, you can find it here: https://api.slack.com/apps
SLACK_CONFIGURATION_ACCESS_TOKEN = "xoxe.xoxp-1-Mi0yLTY4MDA5NjI4MDg2MjQtNjc5MDgzMjE2ODY0MS02ODMwMjc0MTcwMTE5LTcwMjU4MDgzMDM0NzktNWNkYWVhMTVmNTE3ZTNlZjk4NTRkYjhjNjg4YjYzZDM4ZmM2OGNlZmFjNTBiZTY3MDk4NzhiNTNjZTMwZWEyYg"

# create an assistant, let's name it Joe
assistant_config = AssistantConfig(
    name="Joe",
    instructions="Joe likes pizza, NY Knicks and can give you a 'How you doin?' when you need it most.",
    memory=MemoryConfig(),
    inference=InferenceConfig(provider="openai", model="gpt-4"),
)
joe = firedust.assistant.create(assistant_config)

# create a slack app for the assistant
joe.interface.slack.create_app(
    description="A short description of the assistant. This will be displayed in .",
    configuration_token=SLACK_CONFIGURATION_ACCESS_TOKEN,
)

# STEP 2
# install the app in your slack workspace and generate tokens. See here: https://api.slack.com/apps/
SLACK_APP_TOKEN = "xapp-1-A070RQPJEDD-7040405227762-c94d1accf4b9b9fc528267b8e44836a0103c41d9e5ffc1b17144cfb8c266caa4"
SLACK_BOT_TOKEN = "xoxb-6800962808624-7063189460304-0BXUkWie0dGn5Zyiv9SqLcWx"

joe.interface.slack.set_tokens(
    tokens=SlackTokens(app_token=SLACK_APP_TOKEN, bot_token=SLACK_BOT_TOKEN)
)

# STEP 3
# deploy the assistant
joe.interface.slack.deploy()

# Now you can interact with the assistant in your Slack workspace!
