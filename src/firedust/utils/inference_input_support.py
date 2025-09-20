from typing import Dict, Iterable, Set, Union

from firedust.types.base import INFERENCE_MODEL

# -----------------------------------------------------------------------------
# Model → supported content types mapping
# -----------------------------------------------------------------------------
# NOTE: This list is derived from official provider documentation as of 2025-07.
# • "text" is always supported and therefore implied / omitted from the sets.
# • "image_url" – vision input via URL or base64 image.
# • "input_audio" – raw audio (base64 WAV/MP3) input.
# • "file" – inline PDF file input (data-URI) for retrieval-augmented context.
# -----------------------------------------------------------------------------

_MODEL_CONTENT_SUPPORT: Dict[INFERENCE_MODEL, Set[str]] = {
    # OpenAI ----------------------------------------------------------
    "openai/gpt-4o": {"image_url", "file"},
    "openai/gpt-4o-mini": {"image_url", "file"},
    # GPT-4.1 (preview) – text & vision image inputs (per 2025-05 docs)
    "openai/gpt-4.1": {"image_url", "file"},
    # o3 and gpt-5 models support vision (images) and files but NOT raw audio (use separate transcribe models)
    "openai/o3-mini": {"image_url", "file"},
    "openai/o3": {"image_url", "file"},
    "openai/o4-mini": {"image_url", "file"},
    "openai/gpt-5": {"image_url", "file"},
    "openai/gpt-5-mini": {"image_url", "file"},
    # Mistral ---------------------------------------------------------
    "mistral/mistral-medium": set(),
    "mistral/mistral-small": set(),
    # Groq (open-source models) --------------------------------------
    "groq/llama-3.3-70b-versatile": set(),
    "groq/llama-3.1-8b-instant": set(),
    "groq/deepseek-r1-distill-llama-70b": set(),
}


def supported_content_types(model: INFERENCE_MODEL) -> Set[str]:
    """Return the set of *extra* content types (excluding plain text) supported
    by *model*.
    """
    return _MODEL_CONTENT_SUPPORT.get(model, set())


def validate_message_content(
    model: INFERENCE_MODEL, content: Union[str, Iterable[object]]
) -> None:
    """Validate *content* against the model capabilities.

    Raises:
        ValueError: when the content includes at least one unsupported type.
    """

    # Plain text always valid

    if isinstance(content, str):
        return

    unsupported: Set[str] = set()
    allowed = supported_content_types(model)

    # *content* is an iterable of content parts.
    for part in content:  # content is Iterable[object]
        ctype = getattr(part, "type", None)
        if ctype == "text":
            continue  # Plain text is universally supported
        if ctype and ctype not in allowed:
            unsupported.add(ctype)

    if unsupported:
        raise ValueError(
            f"Model '{model}' does not support content type(s): {', '.join(sorted(unsupported))}."
        )
