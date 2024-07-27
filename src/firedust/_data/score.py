from typing import Literal, Optional

from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


def fast(
    text: str,
    instructions: str,
    score_min: float = 0.0,
    score_max: float = 1.0,
    distribution: Literal["uniform", "normal", "exponential"] = "uniform",
    good_example: Optional[str] = None,
    bad_example: Optional[str] = None,
) -> float:
    """
    Scores the given text using the Firedust API.

    Args:
        text (str): The text to be scored.
        instructions (str): The instructions for scoring the text.
        score_min (float, optional): The minimum score. Defaults to 0.0.
        score_max (float, optional): The maximum score. Defaults to 1.0.
        distribution (Literal["uniform", "normal", "exponential"], optional): The distribution of the scores. Defaults to "uniform".
        good_example (str, optional): A good example of the text. Defaults to None.
        bad_example (str, optional): A bad example of the text. Defaults to None.

    Returns:
        float: The score of the text.
    """
    api_client = SyncAPIClient()
    response = api_client.post(
        "/data/score/fast",
        {
            "text": text,
            "instructions": instructions,
            "score_min": score_min,
            "score_max": score_max,
            "distribution": distribution,
            "good_example": good_example,
            "bad_example": bad_example,
        },
    )
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to score text: {response.text}",
        )
    return float(response.json()["data"]["score"])


async def fast_async(
    text: str,
    instructions: str,
    score_min: float = 0.0,
    score_max: float = 1.0,
    distribution: Literal["uniform", "normal", "exponential"] = "uniform",
    good_example: Optional[str] = None,
    bad_example: Optional[str] = None,
) -> float:
    """
    Scores the given text using the Firedust API asynchronously.

    Args:
        text (str): The text to be scored.
        instructions (str): The instructions for scoring the text.
        score_min (float, optional): The minimum score. Defaults to 0.0.
        score_max (float, optional): The maximum score. Defaults to 1.0.
        distribution (Literal["uniform", "normal", "exponential"], optional): The distribution of the scores. Defaults to "uniform".
        good_example (str, optional): A good example of the text. Defaults to None.
        bad_example (str, optional): A bad example of the text. Defaults to None.

    Returns:
        float: The score of the text.
    """
    api_client = AsyncAPIClient()
    response = await api_client.post(
        "/data/score/fast",
        {
            "text": text,
            "instructions": instructions,
            "score_min": score_min,
            "score_max": score_max,
            "distribution": distribution,
            "good_example": good_example,
            "bad_example": bad_example,
        },
    )
    if not response.is_success:
        raise APIError(
            code=response.status_code,
            message=f"Failed to score text: {response.text}",
        )
    return float(response.json()["data"]["score"])
