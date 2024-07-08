from pathlib import Path
from typing import List, Union
from uuid import UUID

from firedust.types import AssistantConfig
from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.errors import APIError


class Learning:
    """
    A collection of methods add various types of data to the assistant's
    knowledge graph. The data is embedded into the assistant's memory and
    is used when a relevant taskor question is asked.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        self.assistant = config
        self.api_client = api_client

    def fast(self, text: str) -> List[UUID]:
        """
        The fastest way to add data to the assistant's memory. It becomes
        available real-time for the assistant to use when answering questions
        or performing tasks.

        Example:
        ```python
        import firedust

        assistant = firedust.assistant.load("ASSISTANT_NAME")
        assistant.learn.fast("The quick brown fox jumps over the lazy dog.")

        response = assistant.chat.message("Who jumps over the lazy dog?")
        assert "brown fox" in response.message.lower()
        ```

        Args:
            text (str): The text to learn.

        Returns:
            memory_ids (List[UUID]): A list of memory ids for the memory items that were created.
        """
        response = self.api_client.post(
            "/assistant/learn/fast",
            data={"assistant": self.assistant.name, "text": text},
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to teach the assistant: {response.text}",
            )

        memory_ids = [UUID(_id) for _id in response.json()["data"]]
        return memory_ids

    def pdf(self, pdf: Union[str, Path]) -> None:
        """
        Learn the content of a PDF file.

        Args:
            pdf (Union[str, Path]): The path to the PDF file.
        """
        raise NotImplementedError()
        # with open(pdf, "rb") as f:
        #     response = self.api_client.post(
        #         "/assistant/learn/pdf",
        #         data={"assistant": self.assistant.name, "pdf": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    def url(self, url: str) -> None:
        """
        Learn the content of a web page.

        Args:
            url (str): The URL to the resource.
        """
        raise NotImplementedError()
        # response = self.api_client.post(
        #     "/assistant/learn/url",
        #     data={"assistant": self.assistant.name, "url": url},
        # )
        # if not response.is_success:
        #     raise APIError(f"Failed to teach the assistant: {response.text}")

    def image(self, image: Union[str, Path]) -> None:
        """
        Learn the content of an image.

        Args:
            image (Union[str, Path]): The path to the image.
        """
        raise NotImplementedError()
        # with open(image, "rb") as f:
        #     response = self.api_client.post(
        #         "/assistant/learn/image",
        #         data={"assistant": self.assistant.name, "image": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    def audio(self, audio: Union[str, Path]) -> None:
        """
        Learn the content of an audio file.

        Args:
            audio (Union[str, Path]): The path to the audio file.
        """
        raise NotImplementedError()
        # with open(audio, "rb") as f:
        #     response = self.api_client.post(
        #         "/assistant/learn/audio",
        #         data={"assistant": self.assistant.name, "audio": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    def video(self, video: Union[str, Path]) -> None:
        """
        Learn the content of a video file.

        Args:
            video (Union[str, Path]): The path to the video file.
        """
        raise NotImplementedError()


class AsyncLearning:
    """
    A collection of async methods add various types of data to the assistant's
    knowledge graph. The data is embedded into the assistant's memory and
    is used when a relevant taskor question is asked.
    """

    def __init__(self, assistant: AssistantConfig, api_client: AsyncAPIClient) -> None:
        self.assistant = assistant
        self.api_client = api_client

    async def fast(self, text: str) -> List[UUID]:
        """
        The fastest way to add data to the assistant's memory. It becomes available
        real-time for the assistant to use when answering questions or performing tasks.

        Example:
        ```python
        import firedust
        import asyncio

        async def main():
            assistant = await firedust.assistant.async_load("ASSISTANT_NAME")
            memory_ids = await assistant.learn.fast("The quick brown fox jumps over the lazy dog.")

            response = await assistant.chat.message("Who jumps over the lazy dog?")
            assert "brown fox" in response.message.lower()

        asyncio.run(main())
        ```

        Args:
            text (str): The text to learn.

        Returns:
            memory_ids (List[UUID]): A list of memory ids.
        """
        response = await self.api_client.post(
            "/assistant/learn/fast",
            data={"assistant": self.assistant.name, "text": text},
        )
        if not response.is_success:
            raise APIError(
                code=response.status_code,
                message=f"Failed to teach the assistant: {response.text}",
            )

        memory_ids = [UUID(_id) for _id in response.json()["data"]]
        return memory_ids

    async def pdf(self, pdf: Union[str, Path]) -> None:
        """
        Learn the content of a PDF file.

        Args:
            pdf (Union[str, Path]): The path to the PDF file.
        """
        raise NotImplementedError()
        # with open(pdf, "rb") as f:
        #     response = await self.api_client.post(
        #         "/assistant/learn/pdf",
        #         data={"assistant": self.assistant.name, "pdf": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    async def url(self, url: str) -> None:
        """
        Learn the content of a web page.

        Args:
            url (str): The URL to the resource.
        """
        raise NotImplementedError()
        # response = await self.api_client.post(
        #     "/assistant/learn/url",
        #     data={"assistant": self.assistant.name, "url": url},
        # )
        # if not response.is_success:
        #     raise APIError(f"Failed to teach the assistant: {response.text}")

    async def image(self, image: Union[str, Path]) -> None:
        """
        Learn the content of an image.

        Args:
            image (Union[str, Path]): The path to the image.
        """
        raise NotImplementedError()
        # with open(image, "rb") as f:
        #     response = await self.api_client.post(
        #         "/assistant/learn/image",
        #         data={"assistant": self.assistant.name, "image": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    async def audio(self, audio: Union[str, Path]) -> None:
        """
        Learn the content of an audio file.

        Args:
            audio (Union[str, Path]): The path to the audio file.
        """
        raise NotImplementedError()
        # with open(audio, "rb") as f:
        #     response = await self.api_client.post(
        #         "/assistant/learn/audio",
        #         data={"assistant": self.assistant.name, "audio": f},
        #     )
        #     if not response.is_success:
        #         raise APIError(f"Failed to teach the assistant: {response.text}")

    async def video(self, video: Union[str, Path]) -> None:
        """
        Learn the content of a video file.

        Args:
            video (Union[str, Path]): The path to the video file.
        """
        raise NotImplementedError()
