from firedust.types.safety import SafetyCheck
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


def text(content: str) -> SafetyCheck:
    """
    Checks the safety of the given text using the Firedust API.

    Args:
        content (str): The text to check for safety.

    Returns:
        SafetyCheck: A model with safety scores for each category.
    """
    api_client = SyncAPIClient()
    response = api_client.post(
        "/data/safetycheck/text",
        {"content": content},
    )
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to check text safety: {response.text}",
        )

    return SafetyCheck.model_validate(response.json()["data"])


async def text_async(content: str) -> SafetyCheck:
    """
    Checks the safety of the given text using the Firedust API asynchronously.

    Args:
        content (str): The text to check for safety.

    Returns:
        SafetyCheck: A model with safety scores for each category.
    """
    api_client = AsyncAPIClient()
    response = await api_client.post(
        "/data/safetycheck/text",
        {"content": content},
    )
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to check text safety: {response.text}",
        )

    return SafetyCheck.model_validate(response.json()["data"])
