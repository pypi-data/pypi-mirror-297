import abc
from typing import Any, Callable, TypeVar, overload

from dataclasses_json.cfg import LetterCase
from dataclasses_json.core import Json
from dataclasses_json.mm import JsonInput, SchemaType
from dataclasses_json.undefined import Undefined
from marshmallow import types

T = TypeVar("T")
U = TypeVar("U", bound="DataClassJsonMixin")

class DataClassJsonMixin(abc.ABC):
    dataclass_json_config: dict[str, Any] | None
    def to_json(
        self,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        default: Callable[[Any], Any] | None = None,
        sort_keys: bool = False,
        **kwargs: dict[str, Any]
    ) -> str: ...
    @classmethod
    def from_json(
        cls: type[U],
        s: JsonInput,
        *,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        infer_missing: bool = False,
        **kwargs: dict[str, Any]
    ) -> U: ...
    @classmethod
    def from_dict(cls: type[U], kvs: Json, *, infer_missing: bool = False) -> U: ...
    def to_dict(self, encode_json: bool = False) -> dict[str, Json]: ...
    @classmethod
    def schema(
        cls: type[U],
        *,
        infer_missing: bool = False,
        only: types.StrSequenceOrSet | None = None,
        exclude: types.StrSequenceOrSet = (),
        many: bool = False,
        context: dict[str, Any] | None = None,
        load_only: types.StrSequenceOrSet = (),
        dump_only: types.StrSequenceOrSet = (),
        partial: bool = False,
        unknown: str | None = None
    ) -> "SchemaType[U]": ...

@overload
def dataclass_json(_cls: type[T]) -> type[T]: ...
@overload
def dataclass_json(
    *,
    letter_case: Callable[[str], str] | LetterCase | None = ...,
    undefined: str | Undefined | None = ...
) -> Callable[[type[T]], type[T]]: ...
def dataclass_json(
    _cls: type[T] | None = None,
    *,
    letter_case: Callable[[str], str] | LetterCase | None = None,
    undefined: str | Undefined | None = None
) -> Callable[[type[T]], type[T]] | type[T]: ...
