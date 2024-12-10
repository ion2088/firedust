import os
from types import TracebackType
from typing import Any, AsyncIterator, Dict, Iterator, Optional, Type

import httpx

from firedust.utils.errors import MissingFiredustKeyError

# Use environment variable with fallback to production URL
BASE_URL = os.getenv("FIREDUST_API_URL", "https://api.firedust.dev")
TIMEOUT = 300


class BaseAPIClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL) -> None:
        api_key = api_key or os.environ.get("FIREDUST_API_KEY")
        if not api_key:
            raise MissingFiredustKeyError()

        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }


class SyncAPIClient(BaseAPIClient):
    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL) -> None:
        super().__init__(api_key, base_url)
        self.client: httpx.Client = httpx.Client(timeout=TIMEOUT, headers=self.headers)

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.client.close()

    def __del__(self) -> None:
        self.client.close()

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("get", url, params=params)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("post", url, data=data)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("put", url, data=data)

    def delete(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        return self._request("delete", url, params=params)

    def get_stream(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Iterator[bytes]:
        url = self.base_url + url
        with self.client.stream("get", url, params=params) as response:
            for chunk in response.iter_bytes():
                yield chunk

    def post_stream(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> Iterator[bytes]:
        url = self.base_url + url
        with self.client.stream("post", url, json=data) as response:
            for chunk in response.iter_bytes():
                yield chunk

    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        url = self.base_url + url
        response = self.client.request(method, url, params=params, json=data)
        return response

    def close(self) -> None:
        """
        Close the underlying HTTP client.
        """
        self.client.close()


class AsyncAPIClient(BaseAPIClient):
    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL) -> None:
        super().__init__(api_key, base_url)
        self.client = httpx.AsyncClient(timeout=TIMEOUT, headers=self.headers)
        self._closed = False

    async def __aenter__(self) -> "AsyncAPIClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if not self._closed:
            await self.client.aclose()
            self._closed = True

    async def get(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        return await self._request("get", url, params=params)

    async def post(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        return await self._request("post", url, data=data)

    async def put(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        return await self._request("put", url, data=data)

    async def delete(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        return await self._request("delete", url, params=params)

    async def get_stream(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[bytes]:
        url = self.base_url + url
        async with self.client.stream("get", url, params=params) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

    async def post_stream(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[bytes]:
        url = self.base_url + url
        async with self.client.stream("post", url, json=data) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

    async def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        url = self.base_url + url
        response = await self.client.request(method, url, params=params, json=data)
        return response
