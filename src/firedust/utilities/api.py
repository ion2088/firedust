import httpx
import os

from firedust.utilities.errors import MissingFiredustKeyError
from typing import Optional, Dict, Any
from firedust.utilities.errors import APIError

BASE_URL = "https://api.firedust.ai/v1"


class APIClient:
    """
    A client for interacting with the Firedust API.

    Attributes:
        base_url (str): The base URL of the Firedust API.
        api_key (str): The API key used for authentication.
        headers (Dict[str, str]): The headers to be included in the requests.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL) -> None:
        """
        Initializes a new instance of the APIClient class.

        Args:
            api_key (str, optional): The API key to authenticate requests. If not provided, it will be fetched from the environment variable "FIREDUST_API_KEY". Defaults to None.
            base_url (str, optional): The base URL of the Firedust API. Defaults to BASE_URL.

        Raises:
            MissingFiredustKeyError: If the API key is not provided and not found in the environment variable.
        """
        api_key = api_key or os.environ.get("FIREDUST_API_KEY")
        if api_key is None:
            raise MissingFiredustKeyError()

        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    # sync methods
    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request_sync("get", url, params=params)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request_sync("post", url, data=data)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request_sync("put", url, data=data)

    def delete(self, url: str) -> Dict[str, Any]:
        return self._request_sync("delete", url)

    # async methods
    async def get_async(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return await self._request_async("get", url, params=params)

    async def post_async(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return await self._request_async("post", url, data=data)

    async def put_async(
        self, url: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return await self._request_async("put", url, data=data)

    async def delete_async(self, url: str) -> Dict[str, Any]:
        return await self._request_async("delete", url)

    def _request_sync(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any] | Any:
        url = self.base_url + url
        response = httpx.request(
            method, url, params=params, json=data, headers=self.headers
        )
        response.raise_for_status()

        # Process status codes and raise errors
        _process_status_codes(response)

        return response.json()

    async def _request_async(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any] | Any:
        url = self.base_url + url
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, params=params, json=data, headers=self.headers
            )
            response.raise_for_status()

            # Process status codes and raise errors
            _process_status_codes(response)

            return response.json()


def _process_status_codes(response: httpx.Response) -> None:
    if response.status_code == 400:
        raise APIError("Bad Request", response.status_code)
    elif response.status_code == 401:
        raise APIError("Unauthorized", response.status_code)
    elif response.status_code == 403:
        raise APIError("Forbidden", response.status_code)
    elif response.status_code == 404:
        raise APIError("Not Found", response.status_code)
    elif response.status_code == 500:
        raise APIError("Internal Server Error", response.status_code)
    # TODO: Customize status codes and error messages
