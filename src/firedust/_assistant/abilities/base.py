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

    _PATH: str = "/assistant"  # unified PATCH endpoint

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self._config = config
        self._api_client = api_client

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------

    def add(self, ability: Tool) -> None:
        """Add a new ability to the assistant."""
        # Build updated abilities list (server expects full replacement)
        updated_abilities = [*self._config.abilities, ability]

        response = self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in updated_abilities],
            },
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add ability '{ability.function.name}': {response.text}",
            )
        # Update local config
        self._config.abilities = updated_abilities

    def update(self, ability: Tool) -> None:
        """Update an existing ability (matched by *name*)."""
        # Replace or append ability locally
        updated = False
        new_list = []
        for existing in self._config.abilities:
            if existing.function.name == ability.function.name:
                new_list.append(ability)
                updated = True
            else:
                new_list.append(existing)
        if not updated:
            new_list.append(ability)

        response = self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in new_list],
            },
        )

        if response.is_success:
            self._config.abilities = new_list
        else:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update ability '{ability.function.name}': {response.text}",
            )

    def remove(self, ability_name: str) -> None:
        """Remove an ability by *name*."""
        pruned_list = [
            tool
            for tool in self._config.abilities
            if tool.function.name != ability_name
        ]

        response = self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in pruned_list],
            },
        )

        if response.is_success:
            self._config.abilities = pruned_list
        else:
            raise APIError(
                code=response.status_code,
                message=f"Failed to remove ability '{ability_name}': {response.text}",
            )


class AsyncAbilities:
    """Asynchronous wrapper around *ability* management endpoints."""

    _PATH: str = "/assistant"  # unified PATCH endpoint

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self._config = config
        self._api_client = api_client

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    async def add(self, ability: Tool) -> None:
        updated_abilities = [*self._config.abilities, ability]

        response = await self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in updated_abilities],
            },
        )

        if response.is_success:
            self._config.abilities = updated_abilities
        else:
            raise APIError(
                code=response.status_code,
                message=f"Failed to add ability '{ability.function.name}': {response.text}",
            )

    async def update(self, ability: Tool) -> None:
        new_list = []
        updated = False
        for existing in self._config.abilities:
            if existing.function.name == ability.function.name:
                new_list.append(ability)
                updated = True
            else:
                new_list.append(existing)
        if not updated:
            new_list.append(ability)

        response = await self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in new_list],
            },
        )

        if response.is_success:
            self._config.abilities = new_list
        else:
            raise APIError(
                code=response.status_code,
                message=f"Failed to update ability '{ability.function.name}': {response.text}",
            )

    async def remove(self, ability_name: str) -> None:
        pruned_list = [
            tool
            for tool in self._config.abilities
            if tool.function.name != ability_name
        ]

        response = await self._api_client.patch(
            self._PATH,
            data={
                "assistant": self._config.name,
                "abilities": [tool.model_dump() for tool in pruned_list],
            },
        )

        if response.is_success:
            self._config.abilities = pruned_list
        else:
            raise APIError(
                code=response.status_code,
                message=f"Failed to remove ability '{ability_name}': {response.text}",
            )
