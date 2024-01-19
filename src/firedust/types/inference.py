from pydantic import BaseModel
from typing import Literal


class InferenceConfig(BaseModel):
    """
    Configuration used by the assistant for inference.
    """

    model: Literal["openai/gpt4", "mistral/medium", "writer/palmyrax"]
    endpoint: str
    api_key: str
