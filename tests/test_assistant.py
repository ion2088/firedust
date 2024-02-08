import os

import firedust
from firedust.assistant import Assistant

# def test_create_list_load_delete_assistant() -> None:
#     assert os.environ.get("FIREDUST_API_KEY") is not None

#     # Create an assistant
#     assistant = firedust.assistant.create()
#     assert isinstance(assistant, Assistant)

#     # List all assistants
#     assistants = firedust.assistant.list()

#     # Load the assistant
#     loaded_assistant = firedust.assistant.load(assistant.config.id)

#     # Delete the assistant
#     firedust.assistant.delete(assistant.config.id)
