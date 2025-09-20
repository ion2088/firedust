import os
import random
from base64 import b64encode
from datetime import datetime

import pytest

import firedust
from firedust.types import ReferencedMessage
from firedust.types.chat import (
    FileContentPart,
    FileData,
    ImageContentPart,
    ImageUrl,
    TextContentPart,
    UserMessage,
)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_multimodal_message() -> None:
    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant capable of understanding images.",
    )

    try:
        # Compose a multimodal user message (text + image)
        text_part = TextContentPart(text="What is pictured in this image?")
        image_part = ImageContentPart(
            image_url=ImageUrl(
                url=(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/640px-Cat03.jpg"
                ),
                detail="auto",
            )
        )

        user_msg = UserMessage(
            assistant=assistant.config.name,
            chat_group="test",
            content=[text_part, image_part],
            author="user",
            timestamp=datetime.now().timestamp(),
        )

        response = assistant.chat.message(message=user_msg)
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)
        assert len(response.content) > 0
        assert "cat" in response.content.lower()
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_multimodal_file_message() -> None:
    """Send a message that includes a file (base64 text file) along with a question."""

    assistant = firedust.assistant.create(
        name=f"test-assistant-{random.randint(1, 1000)}",
        instructions="You are a helpful assistant capable of reading attached files.",
    )

    try:
        # Build minimal PDF (with 'Hello' text) so mime-type is application/pdf
        minimal_pdf = (
            b"%PDF-1.4\n1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n"
            b"2 0 obj <</Type/Pages/Count 1/Kids[3 0 R]>> endobj\n"
            b"3 0 obj <</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]/Contents 4 0 R>> endobj\n"
            b"4 0 obj <</Length 44>>stream\nBT /F1 24 Tf 72 150 Td (Hello) Tj ET\nendstream endobj\n"
            b"xref 0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000062 00000 n \n0000000114 00000 n \n0000000200 00000 n \ntrailer <</Size 5/Root 1 0 R>>\nstartxref 300\n%%EOF"
        )

        pdf_b64 = b64encode(minimal_pdf).decode()
        data_uri = f"data:application/pdf;base64,{pdf_b64}"

        text_part = TextContentPart(text="What is the first word in the attached file?")
        file_part = FileContentPart(
            file=FileData(filename="hello.pdf", file_data=data_uri)
        )

        user_msg = UserMessage(
            assistant=assistant.config.name,
            chat_group="test",
            content=[text_part, file_part],
            author="user",
            timestamp=datetime.now().timestamp(),
        )

        response = assistant.chat.message(message=user_msg)
        assert isinstance(response, ReferencedMessage)
        assert isinstance(response.content, str)
        assert "hello" in response.content.lower()
    finally:
        assistant.delete(confirm=True)


@pytest.mark.skipif(
    os.environ.get("FIREDUST_API_KEY") is None,
    reason="The environment variable FIREDUST_API_KEY is not set.",
)
def test_chat_multimodal_audio_message() -> None:
    """Send a message that includes an audio clip asking what is said."""
    pytest.skip("Audio content is not supported by current models")
