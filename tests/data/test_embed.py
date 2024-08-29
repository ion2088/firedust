import os

import pytest

import firedust


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_embed_text() -> None:
    embeddings = firedust.data.embed.text(
        "The quick brown fox jumps over the lazy dog."
    )
    assert all(isinstance(embedding, float) for embedding in embeddings)
