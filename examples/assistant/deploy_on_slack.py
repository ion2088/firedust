import firedust

# you can deploy your assistants to Slack with just a few lines of code
# add them to your workspaces, interact with them in DMs or groups
# they will learn the history of the channel they are added to and use it in combination
# with their own knowledge to provide the best possible answers

# when deployed, the data you add to the assistant will become available
# in real-time to assist you and your team, see how to add data in the quickstart example

assistant = firedust.assistant.create(name="Sam")
# or load an existing one
assistant = firedust.assistant.load(name="Sam")

# create a slack app
assistant.interface.slack.create_app(
    description="A short description of the assistant. This will be displayed in the app's home tab.",
    configuration_token="INPUT_CONFIG_TOKEN",  # you can find your configuration token here: https://api.slack.com/apps
)

# install the app in your slack workspace UI and generate tokens. See here: https://api.slack.com/apps/
app_token = "INPUT_APP_TOKEN"
bot_token = "INPUT_BOT_TOKEN"

# set the tokens
assistant.interface.slack.set_tokens(
    app_token=app_token,
    bot_token=bot_token,
)

# deploy the assistant
assistant.interface.slack.deploy()

# That's it. Now you can interact with the assistant in your Slack workspace!
