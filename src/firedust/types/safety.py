from pydantic import BaseModel


class SafetyCategories(BaseModel):
    """
    Represents the boolean flags for each safety category.

    Example:
        {
            "hate": true,
            "hate_threatening": true,
            "self_harm": true,
            "sexual": true,
            "sexual_minors": true,
            "violence": true,
            "violence_graphic": true
        }
    """

    hate: bool
    hate_threatening: bool
    self_harm: bool
    sexual: bool
    sexual_minors: bool
    violence: bool
    violence_graphic: bool


class SafetyCategoryScores(BaseModel):
    """
    Represents the scores for each safety category.

    Example:
        {
            "hate": 0.9,
            "hate_threatening": 0.9,
            "self_harm": 0.9,
            "sexual": 0.9,
            "sexual_minors": 0.9,
            "violence": 0.9,
            "violence_graphic": 0.9
        }
    """

    hate: float
    hate_threatening: float
    self_harm: float
    sexual: float
    sexual_minors: float
    violence: float
    violence_graphic: float


class SafetyCheck(BaseModel):
    """
    Represents the complete safety check response.

    Example:
        {
            "flagged": true,
            "categories": {
                "hate": true,
                "hate_threatening": true,
                "self_harm": true,
                "sexual": true,
                "sexual_minors": true,
                "violence": true,
                "violence_graphic": true
            },
            "category_scores": {
                "hate": 0.9,
                "hate_threatening": 0.9,
                "self_harm": 0.9,
                "sexual": 0.9,
                "sexual_minors": 0.9,
                "violence": 0.9,
                "violence_graphic": 0.9
            }
        }
    """

    flagged: bool
    categories: SafetyCategories
    category_scores: SafetyCategoryScores
