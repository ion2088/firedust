import firedust

# you can deploy your assistants to Slack with just a few lines of code
# add them to your workspaces, interact with them in DMs or groups
# they will learn the history of the channel they are added to and use it in combination
# with their own knowledge to provide the best possible answers

# when deployed, the data you add to the assistant will become available
# in real-time to assist you and your team, see how to add data in the quickstart example

assistant = firedust.assistant.create(name="Dan")
# or load an existing one
assistant = firedust.assistant.load(name="Dan")

# create a slack app
assistant.interface.slack.create_app(
    description="A short description of the assistant. This will be displayed in the app's home tab.",
    greeting="A message that the assistant will greet users with.",
    configuration_token="xoxe.xoxp-1-Mi0yLTY4MDA5NjI4MDg2MjQtNjc5MDgzMjE2ODY0MS02ODMwMjc0MTcwMTE5LTczMTY4Njg2MzA5ODItNmE3ODZiMzBiMWJmOThkMDIyZDk4Mzk2MTM5YWU4Y2NkZTRjMjZiOTBhZmQxZmE4YTZmZTc5MWRjOWMxODM5Nw",  # you can find your configuration token here: https://api.slack.com/apps
)

# install the app in your slack workspace UI and generate tokens. See here: https://api.slack.com/apps/
app_token = "xapp-1-A079ARNEPPG-7316877561574-d876e83aca757d8ada18df4b99d94f3767aeecbecd1c2cd3dd959c0a4e674e6b"
bot_token = "xoxb-6800962808624-7320602658149-8HzEJFXxocqDrBYWUt2f6RWq"

# set the tokens
assistant.interface.slack.set_tokens(
    app_token=app_token,
    bot_token=bot_token,
)

# deploy the assistant
assistant.interface.slack.deploy()

# That's it. Now you can interact with the assistant in your Slack workspace!
