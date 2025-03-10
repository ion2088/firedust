import os

import pytest

import firedust
from firedust.types.safety import SafetyCheck


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_safetycheck_text() -> None:
    # Test with safe content
    result = firedust.data.safetycheck.text(
        content="The quick brown fox jumps over the lazy dog."
    )
    assert isinstance(result, SafetyCheck)
    assert not result.flagged  # Should not be flagged
    category_scores = result.category_scores.model_dump()
    assert all(0.0 <= score <= 1.0 for score in category_scores.values())


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_safetycheck_text_async() -> None:
    # Test with safe content
    result = await firedust.data.safetycheck.text_async(
        content="The quick brown fox jumps over the lazy dog."
    )
    assert isinstance(result, SafetyCheck)
    assert not result.flagged  # Should not be flagged
    category_scores = result.category_scores.model_dump()
    assert all(0.0 <= score <= 1.0 for score in category_scores.values())


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_safetycheck_text_with_unsafe_content() -> None:
    unsafe_contents = [
        # Hate speech
        "I hate all people from that country, they should be eliminated!",
        # Violence
        "I'm going to bring a weapon to school tomorrow and make them pay.",
        # Self-harm
        "I can't take it anymore, I'm going to end it all tonight.",
        # Sexual content
        "I want to have sex with you and do naughty things all night long.",
        # Harassment
        "I'm going to hunt you down and torture you until you beg for death, you disgusting waste of oxygen!",
    ]

    for content in unsafe_contents:
        result = firedust.data.safetycheck.text(content=content)
        assert isinstance(result, SafetyCheck)
        assert result.flagged  # Should be flagged as unsafe
        categories = result.categories.model_dump()
        category_scores = result.category_scores.model_dump()
        assert any(categories.values())  # At least one category should be true
        assert any(
            score > 0.7 for score in category_scores.values()
        )  # At least one category should have a high score


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
@pytest.mark.asyncio
async def test_safetycheck_text_async_with_unsafe_content() -> None:
    unsafe_contents = [
        # Hate + Violence + Graphic
        "I will brutally slaughter every last [slur] with my chainsaw and watch them bleed!",
        # Sexual + Minors + Threatening
        "I'm going to find all the children at the playground and do unspeakable things to them.",
        # Self-harm + Graphic Violence
        "I'll slice open my veins and paint the walls with my blood before setting myself on fire.",
        # Hate + Sexual + Violence
        "Those [slur] deserve to be violently [explicit] until they can't walk anymore!",
        # Multi-category extreme
        "I'll kidnap their children, torture them slowly while streaming it, then end it all in a bloodbath!",
    ]

    for content in unsafe_contents:
        result = await firedust.data.safetycheck.text_async(content=content)
        assert isinstance(result, SafetyCheck)
        assert result.flagged  # Should be flagged as unsafe

        categories = result.categories.model_dump()
        category_scores = result.category_scores.model_dump()
        assert any(categories.values())  # At least one category should be true
        assert any(
            score > 0.7 for score in category_scores.values()
        )  # At least one category should have a high score


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_safetycheck_text_edge_cases() -> None:
    edge_cases = [
        # Empty string
        "",
        # Very long content
        "safe content " * 1000,
        # Special characters
        "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿",
        # Emojis
        "😀 😃 😄 😁 😆 😅 😂 🤣 🥲 ☺️ 😊",
    ]

    for content in edge_cases:
        result = firedust.data.safetycheck.text(content=content)
        assert isinstance(result, SafetyCheck)
        assert isinstance(result.flagged, bool)

        categories = result.categories.model_dump()
        category_scores = result.category_scores.model_dump()
        assert all(isinstance(v, bool) for v in categories.values())
        assert all(isinstance(v, float) for v in category_scores.values())
