from enum import Enum
from typing import Any, Callable, TypeVar

from dataclasses_json.undefined import Undefined
from marshmallow.fields import Field

T = TypeVar("T")
U = TypeVar("U")

global_config: _GlobalConfig

class _GlobalConfig: ...

class Exclude:
    ALWAYS: Callable[[], bool]
    NEVER: Callable[[], bool]

class LetterCase(Enum):
    CAMEL: Callable[[str], str]
    KEBAB: Callable[[str], str]
    SNAKE: Callable[[str], str]
    PASCAL: Callable[[str], str]

def config(
    metadata: dict[str, Any] | None = None,
    *,
    encoder: Callable[[U], str] | None = None,
    decoder: Callable[[str], U] | None = None,
    mm_field: Field | None = None,
    letter_case: Callable[[str], str] | LetterCase | None = None,
    undefined: str | Undefined | None = None,
    field_name: str | None = None,
    exclude: Callable[[str, T], bool] | Exclude | None = None,
) -> dict[str, Any]: ...
