from pathlib import Path
from typing import Iterable, List, Union
from uuid import UUID

from firedust.types import AssistantConfig, Message
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Learning:
    """
    A collection of methods to train the assistant on various types of data.
    The data is embedded into the assistant's knowledge graph (memory) and
    is accesed when completing a relevant task or answering a question.
    """

    def __init__(self, assistant: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Learning class.

        Args:
            assistant (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.assistant = assistant
        self.api_client = api_client

    def fast(self, text: str) -> List[UUID]:
        """
        The fastest way to teach the assistant is by providing data in
        string format. This can be documentation, code, examples, or any
        other data. The assistant will learn the information and use it
        to answer questions and perform tasks.

        Args:
            text (str): The text to learn.

        Returns:
            memory_ids (List[UUID]): A list of memory ids.
        """
        response = self.api_client.post(
            "/learn/fast",
            data={"assistant": self.assistant.name, "text": text},
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")

        memory_ids = [UUID(_id) for _id in response.json()["data"]["memory_ids"]]
        return memory_ids

    def from_pdf(self, pdf: Union[str, Path]) -> None:
        """
        Learn the content of a PDF file.

        Args:
            pdf (Union[str, Path]): The path to the PDF file.
        """
        with open(pdf, "rb") as f:
            response = self.api_client.post(
                "/learn/pdf",
                data={"assistant": self.assistant.name, "pdf": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    def from_url(self, url: str) -> None:
        """
        Learn the content of a web page.

        Args:
            url (str): The URL to the resource.
        """
        response = self.api_client.post(
            "/learn/url",
            data={"assistant": self.assistant.name, "url": url},
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")

    def from_image(self, image: Union[str, Path]) -> None:
        """
        Learn the content of an image.

        Args:
            image (Union[str, Path]): The path to the image.
        """
        with open(image, "rb") as f:
            response = self.api_client.post(
                "/learn/image",
                data={"assistant": self.assistant.name, "image": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    def from_audio(self, audio: Union[str, Path]) -> None:
        """
        Learn the content of an audio file.

        Args:
            audio (Union[str, Path]): The path to the audio file.
        """
        with open(audio, "rb") as f:
            response = self.api_client.post(
                "/learn/audio",
                data={"assistant": self.assistant.name, "audio": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    def from_video(self, video: Union[str, Path]) -> None:
        """
        Learn the content of a video file.

        Args:
            video (Union[str, Path]): The path to the video file.
        """
        raise NotImplementedError()

    def chat_messages(self, messages: Iterable[Message]) -> None:
        """
        Adds a chat message history to the assistant's memory. To ensure privacy
        between users, the Messages will be available as context only if prompted
        by the same user id. MemoryItems on the other hand are available to all users.

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = self.api_client.post(
            "/learn/chat_messages",
            data={
                "assistant": self.assistant.name,
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")


class AsyncLearning:
    """
    A collection of methods to train the assistant on various types of data asynchronously.
    The data is embedded into the assistant's knowledge graph (memory) and
    is accessed when completing a relevant task or answering a question.
    """

    def __init__(self, assistant: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncLearning class.

        Args:
            assistant (AssistantConfig): The assistant configuration.
            api_client (ASyncAPIClient): The API client.
        """
        self.assistant = assistant
        self.api_client = api_client

    async def fast(self, text: str) -> List[UUID]:
        """
        The fastest way to teach the assistant is by providing data in
        string format. This can be documentation, code, examples, or any
        other data. The assistant will learn the information and use it
        to answer questions and perform tasks.

        Args:
            text (str): The text to learn.

        Returns:
            memory_ids (List[UUID]): A list of memory ids.
        """
        response = await self.api_client.post(
            "/learn/fast",
            data={"assistant": self.assistant.name, "text": text},
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")

        memory_ids = [UUID(_id) for _id in response.json()["data"]["memory_ids"]]
        return memory_ids

    async def from_pdf(self, pdf: Union[str, Path]) -> None:
        """
        Learn the content of a PDF file.

        Args:
            pdf (Union[str, Path]): The path to the PDF file.
        """
        with open(pdf, "rb") as f:
            response = await self.api_client.post(
                "/learn/pdf",
                data={"assistant": self.assistant.name, "pdf": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    async def from_url(self, url: str) -> None:
        """
        Learn the content of a web page.

        Args:
            url (str): The URL to the resource.
        """
        response = await self.api_client.post(
            "/learn/url",
            data={"assistant": self.assistant.name, "url": url},
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")

    async def from_image(self, image: Union[str, Path]) -> None:
        """
        Learn the content of an image.

        Args:
            image (Union[str, Path]): The path to the image.
        """
        with open(image, "rb") as f:
            response = await self.api_client.post(
                "/learn/image",
                data={"assistant": self.assistant.name, "image": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    async def from_audio(self, audio: Union[str, Path]) -> None:
        """
        Learn the content of an audio file.

        Args:
            audio (Union[str, Path]): The path to the audio file.
        """
        with open(audio, "rb") as f:
            response = await self.api_client.post(
                "/learn/audio",
                data={"assistant": self.assistant.name, "audio": f},
            )
            if not response.is_success:
                raise APIError(f"Failed to teach the assistant: {response.text}")

    async def from_video(self, video: Union[str, Path]) -> None:
        """
        Learn the content of a video file.

        Args:
            video (Union[str, Path]): The path to the video file.
        """
        raise NotImplementedError()

    async def chat_messages(self, messages: Iterable[Message]) -> None:
        """
        Learn a chat message history.

        Args:
            messages (Iterable[Message]): The chat messages.
        """
        response = await self.api_client.post(
            "/learn/chat_messages",
            data={
                "assistant": self.assistant.name,
                "messages": [msg.model_dump() for msg in messages],
            },
        )
        if not response.is_success:
            raise APIError(f"Failed to teach the assistant: {response.text}")
