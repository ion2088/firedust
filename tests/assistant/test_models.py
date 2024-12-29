import os
import random
from typing import List

import pytest

import firedust
from firedust.types.base import INFERENCE_MODEL

# List of all available models to test
MODELS: List[INFERENCE_MODEL] = [
    "mistral/mistral-medium",
    "mistral/mistral-small",
    "mistral/mistral-tiny",
    "openai/gpt-4",
    "openai/gpt-4-turbo-preview",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "openai/gpt-3.5-turbo",
    "groq/llama-3.3-70b-versatile",
    "groq/llama-3.1-8b-instant",
]


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_models_sync() -> None:
    for model in MODELS:
        assistant = firedust.assistant.create(
            name=f"test-assistant-{random.randint(1, 1000)}",
            instructions="You are a helpful assistant.",
            model=model,
        )

        try:
            # Test completion
            response = assistant.chat.message("What is 2+2?")
            assert isinstance(response.content, str)
            assert len(response.content) > 0

            # Test streaming
            stream_content = ""
            for event in assistant.chat.stream("What is 3+3?"):
                assert isinstance(event.content, str)
                stream_content += event.content
            assert len(stream_content) > 0

        finally:
            assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_models_async() -> None:
    for model in MODELS:
        assistant = await firedust.assistant.async_create(
            name=f"test-assistant-{random.randint(1, 1000)}",
            instructions="You are a helpful assistant.",
            model=model,
        )

        try:
            # Test completion
            response = await assistant.chat.message("What is 2+2?")
            assert isinstance(response.content, str)
            assert len(response.content) > 0

            # Test streaming
            stream_content = ""
            async for event in assistant.chat.stream("What is 3+3?"):
                assert isinstance(event.content, str)
                stream_content += event.content
            assert len(stream_content) > 0

        finally:
            await assistant.delete(confirm=True)
