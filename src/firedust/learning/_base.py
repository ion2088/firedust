from typing import Union
from pathlib import Path
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.api import APIClient


class Learning:
    """
    A collection of methods to train the assistant on various types of data.
    The data is embedded into the assistant's knowledge graph (memory) and
    is accesed when completing a relevant task or answering a question.
    """

    def __init__(self, assistant: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Learning class.

        Args:
            assistant (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.assistant = assistant
        self.api_client = api_client

    def fast(self, text: str) -> None:
        """
        The fastest way to teach the assistant is by providing data in
        string format. This can be documentation, code, examples, or any
        other data that you want the assistant to learn from.

        Args:
            text (str): The text to learn.
        """
        self.api_client.post(
            f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/text",
            data={"text": text},
        )

    def from_pdf(self, pdf: Union[str, Path]) -> None:
        """
        Teaches the assistant from a PDF file.

        Args:
            pdf (Union[str, Path]): The path to the PDF file.
        """
        with open(pdf, "rb") as f:
            self.api_client.post(
                f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/pdf",
                data={"pdf": f},
            )

    def from_url(self, url: str) -> None:
        """
        Teaches the assistant from a URL.

        Args:
            url (str): The URL to the resource.
        """
        self.api_client.post(
            f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/url",
            data={"url": url},
        )

    def from_image(self, image: Union[str, Path]) -> None:
        """
        Teaches the assistant from an image.

        Args:
            image (Union[str, Path]): The path to the image.
        """
        with open(image, "rb") as f:
            self.api_client.post(
                f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/image",
                data={"image": f},
            )

    def from_audio(self, audio: Union[str, Path]) -> None:
        """
        Teaches the assistant from an audio file.

        Args:
            audio (Union[str, Path]): The path to the audio file.
        """
        with open(audio, "rb") as f:
            self.api_client.post(
                f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/audio",
                data={"audio": f},
            )

    def from_video(self, video: Union[str, Path]) -> None:
        """
        Teaches the assistant from a video file.

        Args:
            video (Union[str, Path]): The path to the video file.
        """
        with open(video, "rb") as f:
            self.api_client.post(
                f"{self.api_client.base_url}/assistant/{self.assistant.id}/learn/video",
                data={"video": f},
            )
