"""Ability management helpers for the Firedust SDK.

These utility classes provide a convenient wrapper around the newly introduced
REST endpoints that manage an assistant's *abilities* (aka function-calling
*tools*).

Synchronous usage::

    assistant.abilities.add(tool)
    assistant.abilities.update(tool)
    assistant.abilities.remove("search_documents")

Asynchronous usage::

    await assistant.abilities.add(tool)
    await assistant.abilities.update(tool)
    await assistant.abilities.remove("search_documents")
"""

from __future__ import annotations

from typing import List

from firedust.types.assistant import AssistantConfig
from firedust.types.tools import Tool
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError

__all__: List[str] = [
    "Abilities",
    "AsyncAbilities",
]


class Abilities:
    """Synchronous wrapper around *ability* management endpoints."""

    _PATH: str = "/assistant/abilities"

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self._config = config
        self._api_client = api_client

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------

    def add(self, ability: Tool) -> None:
        """Add a new ability to the assistant."""
        response = self._api_client.post(
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability": ability.model_dump(),
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add ability '{ability.function.name}': {response.text}",
            )
        # Update local config
        self._config.abilities.append(ability)

    def update(self, ability: Tool) -> None:
        """Update an existing ability (matched by *name*)."""
        response = self._api_client.put(
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability": ability.model_dump(),
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update ability '{ability.function.name}': {response.text}",
            )
        # Replace in local config if present, else append
        found = False
        for idx, existing in enumerate(self._config.abilities):
            if existing.function.name == ability.function.name:
                self._config.abilities[idx] = ability
                found = True
                break
        if not found:
            self._config.abilities.append(ability)

    def remove(self, ability_name: str) -> None:
        """Remove an ability by *name*."""
        # DELETE with JSON body – using the protected `_request` helper to allow body.
        response = self._api_client._request(
            "delete",
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability_name": ability_name,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to remove ability '{ability_name}': {response.text}",
            )
        # Prune from local config
        self._config.abilities = [
            tool
            for tool in self._config.abilities
            if tool.function.name != ability_name
        ]


class AsyncAbilities:
    """Asynchronous wrapper around *ability* management endpoints."""

    _PATH: str = "/assistant/abilities"

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self._config = config
        self._api_client = api_client

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    async def add(self, ability: Tool) -> None:
        response = await self._api_client.post(
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability": ability.model_dump(),
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add ability '{ability.function.name}': {response.text}",
            )
        self._config.abilities.append(ability)

    async def update(self, ability: Tool) -> None:
        response = await self._api_client.put(
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability": ability.model_dump(),
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update ability '{ability.function.name}': {response.text}",
            )
        found = False
        for idx, existing in enumerate(self._config.abilities):
            if existing.function.name == ability.function.name:
                self._config.abilities[idx] = ability
                found = True
                break
        if not found:
            self._config.abilities.append(ability)

    async def remove(self, ability_name: str) -> None:
        response = await self._api_client._request(
            "delete",
            self._PATH,
            data={
                "assistant": self._config.name,
                "ability_name": ability_name,
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to remove ability '{ability_name}': {response.text}",
            )
        self._config.abilities = [
            tool
            for tool in self._config.abilities
            if tool.function.name != ability_name
        ]
