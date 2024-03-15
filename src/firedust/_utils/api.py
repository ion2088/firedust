import os
from typing import Any, AsyncIterator, Dict, Iterator

import httpx

from firedust._utils.errors import MissingFiredustKeyError

BASE_URL = "https://api.firedustx.com/v1"
# BASE_URL = "http://0.0.0.0:8080"


class APIClient:
    """
    A client for interacting with the Firedust API.

    Attributes:
        base_url (str): The base URL of the Firedust API.
        api_key (str): The API key used for authentication.
        headers (Dict[str, str]): The headers to be included in the requests.
    """

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL) -> None:
        """
        Initializes a new instance of the APIClient class.

        Args:
            api_key (str, optional): The API key to authenticate requests. If not provided, it will be fetched from the environment variable "FIREDUST_API_KEY". Defaults to None.
            base_url (str, optional): The base URL of the Firedust API. Defaults to BASE_URL.

        Raises:
            MissingFiredustKeyError: If the API key is not provided and not found in the environment variable.
        """
        api_key = api_key or os.environ.get("FIREDUST_API_KEY")
        if not api_key:
            raise MissingFiredustKeyError()

        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    # sync methods
    def get(self, url: str, params: Dict[str, Any] | None = None) -> httpx.Response:
        return self._request_sync("get", url, params=params)

    def post(self, url: str, data: Dict[str, Any] | None = None) -> httpx.Response:
        return self._request_sync("post", url, data=data)

    def put(self, url: str, data: Dict[str, Any] | None = None) -> httpx.Response:
        return self._request_sync("put", url, data=data)

    def delete(self, url: str) -> httpx.Response:
        return self._request_sync("delete", url)

    def get_stream(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> Iterator[bytes]:
        url = self.base_url + url
        with httpx.stream("get", url, params=params, headers=self.headers) as response:
            for chunk in response.iter_bytes():
                yield chunk

    def post_stream(
        self, url: str, data: Dict[str, Any] | None = None
    ) -> Iterator[bytes]:
        url = self.base_url + url
        with httpx.stream(
            "post", url, json=data, headers=self.headers, timeout=300
        ) as response:
            for chunk in response.iter_bytes():
                yield chunk

    # async methods
    async def get_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> httpx.Response:
        return await self._request_async("get", url, params=params)

    async def post_async(
        self, url: str, data: Dict[str, Any] | None = None
    ) -> httpx.Response:
        return await self._request_async("post", url, data=data)

    async def put_async(
        self, url: str, data: Dict[str, Any] | None = None
    ) -> httpx.Response:
        return await self._request_async("put", url, data=data)

    async def delete_async(self, url: str) -> httpx.Response:
        return await self._request_async("delete", url)

    async def get_stream_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> AsyncIterator[bytes]:
        url = self.base_url + url
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "get", url, params=params, headers=self.headers
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    async def post_stream_async(
        self, url: str, data: Dict[str, Any] | None = None
    ) -> AsyncIterator[bytes]:
        url = self.base_url + url
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "post", url, json=data, headers=self.headers
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    # request methods
    def _request_sync(
        self,
        method: str,
        url: str,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> httpx.Response:
        url = self.base_url + url
        response = httpx.request(
            method, url, params=params, json=data, headers=self.headers, timeout=30
        )
        return response

    async def _request_async(
        self,
        method: str,
        url: str,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> httpx.Response:
        url = self.base_url + url
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, params=params, json=data, headers=self.headers, timeout=30
            )
            return response
