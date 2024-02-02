from typing import Literal

from pydantic import BaseModel


class InferenceConfig(BaseModel):
    """
    Configuration used by the assistant for inference.
    """

    model: Literal[
        "openai/gpt4", "mistral/medium", "writer/palmyrax"
    ] = "mistral/medium"
