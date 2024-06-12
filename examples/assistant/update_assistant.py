import firedust

assistant = firedust.assistant.create(name="Sam")
# or load an existing assistant
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
