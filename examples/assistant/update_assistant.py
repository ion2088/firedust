import firedust

# Load an existing assistant (or create one if it doesn't exist)
assistant = firedust.assistant.load("Sam")
# assistant = firedust.assistant.create(name="Sam")  # alternative: create a new one

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
