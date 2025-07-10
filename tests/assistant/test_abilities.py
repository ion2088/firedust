import json
import os
import random

import pytest

import firedust
from firedust.types import FunctionDefinition, Tool

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _build_weather_tool(description: str) -> Tool:
    """Return a simple weather function tool definition."""

    return Tool(
        function=FunctionDefinition(
            name="get_current_weather",
            description=description,
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the location, e.g. San Francisco, Paris, etc.",
                    }
                },
                "required": ["location"],
            },
        )
    )


def _update_weather_tool(tool: Tool) -> Tool:
    return Tool(
        function=FunctionDefinition(
            name=tool.function.name,
            description=tool.function.description,
            parameters={
                "type": "object",
                "properties": {
                    "coordinates": {
                        "type": "array",
                        "description": "The coordinates of the location, e.g. [40.7128, -74.0060]",
                        "items": {"type": "number"},
                    }
                },
                "required": ["coordinates"],
            },
        )
    )


# ---------------------------------------------------------------------------
# Synchronous abilities test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_abilities_lifecycle() -> None:  # noqa: WPS210 (many variables is OK in test)
    """End-to-end test for adding, updating and removing assistant abilities."""

    assistant_name = f"test-assistant-abilities-{random.randint(1, 10_000)}"
    assistant = firedust.assistant.create(name=assistant_name)

    try:
        # ------------------------------------------------------------------
        # 1. Add ability
        # ------------------------------------------------------------------
        tool_v1 = _build_weather_tool("Get the current weather for a location.")
        assistant.abilities.add(tool_v1)

        assert any(
            t.function.name == tool_v1.function.name for t in assistant.config.abilities
        ), "Ability was not added to assistant config."

        # ------------------------------------------------------------------
        # 2. Send a message that should trigger the tool call (optional)
        # ------------------------------------------------------------------
        response = assistant.chat.message(
            "What's the weather like in Paris today?", add_to_memory=False
        )
        if response.tool_calls is None:
            raise ValueError(
                f"Tool calls is empty: {response.content} {response.tool_calls}"
            )

        # Basic structural validation
        assert isinstance(response.tool_calls, list)
        for call in response.tool_calls:
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "Paris"}

        # ------------------------------------------------------------------
        # 3. Update the ability (change description)
        # ------------------------------------------------------------------
        tool_v2 = _update_weather_tool(tool_v1)
        assistant.abilities.update(tool_v2)

        response = assistant.chat.message(
            "What's the weather like in Paris today?", add_to_memory=False
        )
        if response.tool_calls is None:
            raise ValueError(
                f"Tool calls is empty: {response.content} {response.tool_calls}"
            )

        # Basic structural validation
        assert isinstance(response.tool_calls, list)
        for call in response.tool_calls:
            assert call.function.name == tool_v2.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args.get("coordinates") is not None
            assert len(function_args.get("coordinates")) == 2

        # ------------------------------------------------------------------
        # 4. Remove the ability
        # ------------------------------------------------------------------
        assistant.abilities.remove(tool_v2.function.name)
        assert all(
            t.function.name != tool_v2.function.name for t in assistant.config.abilities
        ), "Ability was not removed from config."

    finally:
        assistant.delete(confirm=True)


# ---------------------------------------------------------------------------
# Asynchronous abilities test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_abilities_lifecycle() -> (
    None
):  # noqa: WPS210 (many variables is OK in test)
    """Async variant of the abilities lifecycle test."""

    assistant_name = f"test-async-abilities-{random.randint(1, 10_000)}"
    assistant = await firedust.assistant.async_create(name=assistant_name)

    try:
        # ------------------------------------------------------------------
        # 1. Add ability
        # ------------------------------------------------------------------
        tool_v1 = _build_weather_tool("Get the current weather for a location.")
        await assistant.abilities.add(tool_v1)

        assert any(
            t.function.name == tool_v1.function.name for t in assistant.config.abilities
        ), "Ability was not added to assistant config."

        # ------------------------------------------------------------------
        # 2. Send a message that should trigger the tool call (optional)
        # ------------------------------------------------------------------
        response = await assistant.chat.message(
            "What's the weather like in London now?", add_to_memory=False
        )
        if response.tool_calls is None:
            raise ValueError(
                f"Tool calls is empty: {response.content} {response.tool_calls}"
            )

        for call in response.tool_calls:
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "London"}

        # ------------------------------------------------------------------
        # 3. Update the ability
        # ------------------------------------------------------------------
        tool_v2 = _update_weather_tool(tool_v1)
        await assistant.abilities.update(tool_v2)

        response = await assistant.chat.message(
            "What's the weather like in London now?", add_to_memory=False
        )
        if response.tool_calls is None:
            raise ValueError(
                f"Tool calls is empty: {response.content} {response.tool_calls}"
            )

        for call in response.tool_calls:
            assert call.function.name == tool_v2.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args.get("coordinates") is not None
            assert len(function_args.get("coordinates")) == 2

        # ------------------------------------------------------------------
        # 4. Remove the ability
        # ------------------------------------------------------------------
        await assistant.abilities.remove(tool_v2.function.name)
        assert all(
            t.function.name != tool_v2.function.name for t in assistant.config.abilities
        ), "Ability was not removed from config."

    finally:
        await assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_abilities_streaming() -> None:
    """Test abilities (tool calls) using the streaming chat API."""
    assistant_name = f"test-assistant-abilities-stream-{random.randint(1, 10_000)}"
    assistant = firedust.assistant.create(name=assistant_name)

    try:
        # 1. Add ability
        tool_v1 = _build_weather_tool("Get the current weather for a location.")
        assistant.abilities.add(tool_v1)
        assert any(
            t.function.name == tool_v1.function.name for t in assistant.config.abilities
        ), "Ability was not added to assistant config."

        # 2. Send a message that should trigger the tool call (streaming)
        text_parts: list[str] = []
        calls = {}
        for ev in assistant.chat.stream(
            "What's the weather like in Paris today?", add_to_memory=False
        ):
            if ev.content:
                text_parts.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls, "Tool calls missing at stream end"
        for call in calls.values():
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "Paris"}

        # 3. Update the ability (change description)
        tool_v2 = _update_weather_tool(tool_v1)
        assistant.abilities.update(tool_v2)
        text_parts = []
        calls = {}
        for ev in assistant.chat.stream(
            "What's the weather like in Paris today?", add_to_memory=False
        ):
            if ev.content:
                text_parts.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls, "Tool calls missing at stream end"
        for call in calls.values():
            assert call.function.name == tool_v2.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args.get("coordinates") is not None
            assert len(function_args.get("coordinates")) == 2

        # 4. Remove the ability
        assistant.abilities.remove(tool_v2.function.name)
        assert all(
            t.function.name != tool_v2.function.name for t in assistant.config.abilities
        ), "Ability was not removed from config."
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_async_abilities_streaming() -> None:
    """Async test for abilities (tool calls) using the streaming chat API."""
    assistant_name = f"test-async-abilities-stream-{random.randint(1, 10_000)}"
    assistant = await firedust.assistant.async_create(name=assistant_name)

    try:
        # 1. Add ability
        tool_v1 = _build_weather_tool("Get the current weather for a location.")
        await assistant.abilities.add(tool_v1)
        assert any(
            t.function.name == tool_v1.function.name for t in assistant.config.abilities
        ), "Ability was not added to assistant config."

        # 2. Send a message that should trigger the tool call (streaming)
        text_parts: list[str] = []
        calls = {}
        async for ev in assistant.chat.stream(
            "What's the weather like in London now?", add_to_memory=False
        ):
            if ev.content:
                text_parts.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls, "Tool calls missing at stream end"
        for call in calls.values():
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "London"}

        # 3. Update the ability
        tool_v2 = _update_weather_tool(tool_v1)
        await assistant.abilities.update(tool_v2)
        text_parts = []
        calls = {}
        async for ev in assistant.chat.stream(
            "What's the weather like in London now?", add_to_memory=False
        ):
            if ev.content:
                text_parts.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls, "Tool calls missing at stream end"
        for call in calls.values():
            assert call.function.name == tool_v2.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args.get("coordinates") is not None
            assert len(function_args.get("coordinates")) == 2

        # 4. Remove the ability
        await assistant.abilities.remove(tool_v2.function.name)
        assert all(
            t.function.name != tool_v2.function.name for t in assistant.config.abilities
        ), "Ability was not removed from config."
    finally:
        await assistant.delete(confirm=True)
