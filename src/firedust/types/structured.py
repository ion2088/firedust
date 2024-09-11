from typing import Any, Dict, List, Literal, Mapping, Optional, Union

from pydantic import BaseModel


class BooleanResponse(BaseModel):
    response: bool
    conviction: float


class BaseField(BaseModel):
    type: Literal["float", "bool", "str", "list", "dict", "category"]
    hint: str
    optional: bool = False


class FloatField(BaseField):
    type: Literal["float"] = "float"
    min_: Optional[float] = None
    max_: Optional[float] = None


class BooleanField(BaseField):
    type: Literal["bool"] = "bool"


class StringField(BaseField):
    type: Literal["str"] = "str"


class CategoryField(BaseField):
    type: Literal["category"] = "category"
    categories: List[str]


class ListField(BaseField):
    type: Literal["list"] = "list"
    items: Union[FloatField, BooleanField, StringField, "ListField", "DictField"]


class DictField(BaseField):
    type: Literal["dict"] = "dict"
    items: Dict[
        str,
        Union[
            FloatField, BooleanField, StringField, CategoryField, ListField, "DictField"
        ],
    ]


FIELD_TYPE = Union[
    FloatField, BooleanField, StringField, CategoryField, ListField, DictField
]
ALLOWED_PRIMATY_VALUE_TYPES = Union[float, bool, str, None]
ALLOWED_VALUE_TYPES = Union[
    float,
    bool,
    str,
    List[Any],  # List[ALLOWED_VALUE_TYPES],
    Dict[str, Any],  # Dict[str, ALLOWED_VALUE_TYPES],
    None,
]
STRUCTURED_RESPONSE = Mapping[str, ALLOWED_VALUE_TYPES]
STRUCTURED_SCHEMA = Mapping[str, FIELD_TYPE]
