from enum import Enum
from typing import Any, Callable

from dataclasses_json.utils import CatchAllVar
from marshmallow import ValidationError

class UndefinedParameterAction:
    @staticmethod
    def handle_from_dict(obj: type[Any], kvs: dict[Any, Any]) -> dict[str, Any]: ...
    @staticmethod
    def handle_to_dict(obj: Any, kvs: dict[Any, Any]) -> dict[Any, Any]: ...
    @staticmethod
    def handle_dump(obj: Any) -> dict[Any, Any]: ...
    @staticmethod
    def create_init(obj: Any) -> Callable: ...

class Undefined(Enum):
    INCLUDE: type[UndefinedParameterAction] = ...
    RAISE: type[UndefinedParameterAction] = ...
    EXCLUDE: type[UndefinedParameterAction] = ...

class UndefinedParameterError(ValidationError):
    pass

CatchAll = CatchAllVar | None
