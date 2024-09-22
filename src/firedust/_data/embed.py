from typing import List

from firedust.utils.api import SyncAPIClient
from firedust.utils.errors import APIError


def text(content: str) -> List[float]:
    """
    Generates embeddings for the given string.

    Args:
        content (str): The text to generate embeddings for.

    Returns:
        List[float]: The embeddings for the text.
    """
    api_client = SyncAPIClient()
    response = api_client.post(
        "/data/embed/text",
        {
            "content": content,
        },
    )
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to generate embeddings: {response.text}",
        )
    embeddings: List[float] = response.json()["data"]["embedding"]
    return embeddings
