import os

import pytest

import firedust


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_score_fast() -> None:
    score = firedust.data.score.fast(
        text="The quick brown fox jumps over the lazy dog.",
        instructions="Score fox's survival skills.",
        score_max=1.0,
        score_min=0.0,
    )
    assert 0.0 <= score <= 1.0


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_score_fast_async() -> None:
    score = await firedust.data.score.fast_async(
        text="The quick brown fox jumps over the lazy dog.",
        instructions="Score fox's survival skills.",
        score_max=1.0,
        score_min=0.0,
    )
    assert 0.0 <= score <= 1.0
