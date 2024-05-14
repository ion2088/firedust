from typing import Literal

TOKENS = int

INFERENCE_MODEL = Literal[
    "mistral/mistral-medium",
    "mistral/mistral-small",
    "mistral/mistral-tiny",
    "openai/gpt-4",
    "openai/gpt-4-turbo-preview",
    "openai/gpt-3.5-turbo",
]
