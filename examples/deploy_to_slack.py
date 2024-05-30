import firedust

# TODO: Add wrapper to firedust and slackapp to assign a error id and encourage users to contact support@firedust.com
# TODO: Simplify error types in firedust - two error types: user error and system error
# TODO: Update and fix example docstrings
# TODO: Add api documentation in redocly
# TODO: Add user and credit management
# TODO: Add index and offset to the endpoint of big queries
# TODO: Update firedust url everywhere
# TODO: Add slack interface update (to update to a specific version, based on github tags)
# TODO: Add slack greeting message to the configuration
# TODO: Add data encryption before storing in the database and decrypt it before sending it to the user
# TODO: Measure the credist of users
# TODO: Learn from pdf, audio and urls
# TODO: Slackapp - add capability to /learn stuff
# TODO: Skackapp - add capability to read and process files

# STEP 1
# add your slack configuration token, you can find it here: https://api.slack.com/apps
SLACK_CONFIGURATION_ACCESS_TOKEN = "xoxe.xoxp-1-Mi0yLTY4MDA5NjI4MDg2MjQtNjc5MDgzMjE2ODY0MS02ODMwMjc0MTcwMTE5LTcxMzE2MDc4MTM1MDQtMzJmNThmOTMyNzFiNmFmZmMwNmJjMzQ1NzlkMGQ4NjBjNWMwMjExYjc4NTM0MjFiOTA0YTA0NzViZDk0OWMwZg"

# create an assistant, let's name it Joey
joey = firedust.assistant.create(
    name="Joey",
    instructions="You are a helpful assistant.",
)

# create a slack app for the assistant
joey.interface.slack.create_app(
    description="A short description of the assistant. This will be displayed in the app's home tab.",
    configuration_token=SLACK_CONFIGURATION_ACCESS_TOKEN,
)

# STEP 2
# install the app in your slack workspace and generate tokens. See here: https://api.slack.com/apps/
slack_app_token = "xapp-1-A073VNP6GD6-7121656385473-59aee28040d00ecf0fd2db86696e3d3f9f4a3fcd56aad02050a2e59b1a53632c"
slack_bot_token = "xoxb-6800962808624-7108988266034-mTIlUnoxGQyycw4H0FtdLYfG"

joey.interface.slack.set_tokens(app_token=slack_app_token, bot_token=slack_bot_token)

# STEP 3
# deploy the assistant
joey.interface.slack.deploy()

# Now you can interact with the assistant in your Slack workspace!
