import os

import pytest

from firedust.assistant import Assistant


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_streaming() -> None:
    assistant = Assistant.create()
    response = assistant.chat.stream("Hi, how are you?")

    for x in response:
        print(x.message)

    w = 10
