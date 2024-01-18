from pydantic import BaseModel
from typing import Literal


class Inference(BaseModel):
    """
    Inference Model used by the assistant for inference.
    """

    model: Literal["openai/gpt4", "mistral/medium"]
