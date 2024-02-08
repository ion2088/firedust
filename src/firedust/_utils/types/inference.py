from typing import Dict, List, Literal

from pydantic import BaseModel

TOKENS = int

INFERENCE_PROVIDER = Literal["mistral", "openai"]
INFERENCE_MODEL = Literal[
    "mistral-medium",
    "mistral-small",
    "mistral-tiny",
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo",
]

INFERENCE_MODELS_MAP: Dict[INFERENCE_PROVIDER, List[INFERENCE_MODEL]] = {
    "mistral": [
        "mistral-medium",
        "mistral-small",
        "mistral-tiny",
    ],
    "openai": [
        "gpt-4",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo",
    ],
}


class InferenceConfig(BaseModel):
    provider: INFERENCE_PROVIDER = "mistral"
    model: INFERENCE_MODEL = "mistral-medium"
