import json
import os
import random
from datetime import datetime
from typing import List

import pytest

import firedust
from firedust.types import FunctionDefinition, Tool
from firedust.types.chat import ToolMessage

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
        response = assistant.chat.message("What's the weather like in Paris today?")
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
        # 2b. Send back a ToolMessage simulating the tool execution result
        # ------------------------------------------------------------------
        first_call = response.tool_calls[0]
        tool_reply = ToolMessage(
            assistant=assistant_name,
            chat_group="default",
            author="tool",
            name=first_call.function.name,
            tool_call_id=first_call.id,
            content=json.dumps(
                {
                    "status": "success",
                    "result": {
                        "temperature": "15°C",
                        "condition": "Sunny",
                    },
                }
            ),
            timestamp=datetime.now().timestamp(),
        )

        follow_up = assistant.chat.message(tool_reply)
        # Basic validation – assistant should reply with some content
        assert follow_up.content is not None and len(follow_up.content) > 0
        print("Assistant after tool execution:", follow_up.content)

        # ------------------------------------------------------------------
        # 3. Update the ability (change description)
        # ------------------------------------------------------------------
        tool_v2 = _update_weather_tool(tool_v1)
        assistant.abilities.update(tool_v2)

        response = assistant.chat.message("What's the weather like in Paris today?")
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
        # 3b. Send back a ToolMessage simulating the tool execution result
        # ------------------------------------------------------------------
        first_call = response.tool_calls[0]
        tool_reply = ToolMessage(
            assistant=assistant_name,
            chat_group="default",
            author="tool",
            name=first_call.function.name,
            tool_call_id=first_call.id,
            content=json.dumps(
                {
                    "status": "success",
                    "result": {
                        "temperature": "15°C",
                        "condition": "Sunny",
                    },
                }
            ),
            timestamp=datetime.now().timestamp(),
        )
        follow_up = assistant.chat.message(tool_reply)
        # Basic validation – assistant should reply with some content
        assert follow_up.content is not None and len(follow_up.content) > 0
        print("Assistant after tool execution:", follow_up.content)

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
            "What's the weather like in London now?"
        )
        if response.tool_calls is None:
            raise ValueError(
                f"Tool calls is empty: {response.content} {response.tool_calls}"
            )

        for call in response.tool_calls:
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "London"}

        # Send a ToolMessage back (async)
        tool_reply_async = ToolMessage(
            assistant=assistant_name,
            chat_group="default",
            author="tool",
            name=response.tool_calls[0].function.name,
            tool_call_id=response.tool_calls[0].id,
            content=json.dumps(
                {"status": "success", "result": {"temperature": "14°C"}}
            ),
            timestamp=datetime.now().timestamp(),
        )

        follow_up_async = await assistant.chat.message(tool_reply_async)
        assert follow_up_async.content is not None and len(follow_up_async.content) > 0

        # ------------------------------------------------------------------
        # 3. Update the ability
        # ------------------------------------------------------------------
        tool_v2 = _update_weather_tool(tool_v1)
        await assistant.abilities.update(tool_v2)

        response = await assistant.chat.message(
            "What's the weather like in London now?"
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
        # 3b. Send back a ToolMessage simulating the tool execution result
        # ------------------------------------------------------------------
        first_call = response.tool_calls[0]
        tool_reply = ToolMessage(
            assistant=assistant_name,
            chat_group="default",
            author="tool",
            name=first_call.function.name,
            tool_call_id=first_call.id,
            content=json.dumps(
                {"status": "success", "result": {"temperature": "14°C"}}
            ),
            timestamp=datetime.now().timestamp(),
        )
        follow_up_async = await assistant.chat.message(tool_reply)
        assert follow_up_async.content is not None and len(follow_up_async.content) > 0

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
        text_parts2: List[str] = []
        calls2 = {}
        for ev in assistant.chat.stream("What's the weather like in Paris today?"):
            if ev.content:
                text_parts2.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls2[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls2, "Tool calls missing at stream end"
        for call in calls2.values():
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "Paris"}

        # 3. Update the ability (change description)
        tool_v2 = _update_weather_tool(tool_v1)
        assistant.abilities.update(tool_v2)
        text_parts = []  # type: List[str]
        calls = {}
        for ev in assistant.chat.stream("What's the weather like in Paris today?"):
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
        text_parts2: List[str] = []
        calls2 = {}
        async for ev in assistant.chat.stream("What's the weather like in London now?"):
            if ev.content:
                text_parts2.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls2[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls2, "Tool calls missing at stream end"
        for call in calls2.values():
            assert call.function.name == tool_v1.function.name
            function_args = json.loads(call.function.arguments)
            assert function_args == {"location": "London"}

        # 3. Update the ability
        tool_v2 = _update_weather_tool(tool_v1)
        await assistant.abilities.update(tool_v2)
        text_parts3: List[str] = []
        calls3 = {}
        async for ev in assistant.chat.stream("What's the weather like in London now?"):
            if ev.content:
                text_parts3.append(ev.content)
            if ev.tool_calls:
                for tc in ev.tool_calls:
                    calls3[tc.id] = tc
            if ev.stream_ended:
                break

        assert calls3, "Tool calls missing at stream end"
        for call in calls3.values():
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
