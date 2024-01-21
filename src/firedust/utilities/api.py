import requests
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

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("get", url, params=params)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("post", url, data=data)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("put", url, data=data)

    def delete(self, url: str) -> Dict[str, Any]:
        return self._request("delete", url)

    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any] | Any:
        url = self.base_url + url
        response = requests.request(
            method, url, params=params, json=data, headers=self.headers
        )
        response.raise_for_status()

        if response.status_code > 299:
            raise APIError(response.text, response.status_code)

        return response.json()
