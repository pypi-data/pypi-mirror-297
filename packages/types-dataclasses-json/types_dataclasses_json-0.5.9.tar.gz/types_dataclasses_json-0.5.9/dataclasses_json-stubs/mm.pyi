from typing import Any, Generic, TypeVar, overload

from marshmallow import Schema

T = TypeVar("T")
JsonInput = str | bytes | bytearray
EncodedDict = dict[str, Any]
OneOrMany = T | list[T]
OneOrManyEncoded = EncodedDict | list[EncodedDict]

class SchemaF(Schema, Generic[T]):
    """Lift Schema into a type constructor"""

    def __init__(self, *args, **kwargs) -> None: ...
    @overload
    def dump(self, obj: list[T], many: bool | None = None) -> list[EncodedDict]: ...
    @overload
    def dump(self, obj: T, many: bool | None = None) -> EncodedDict: ...
    def dump(self, obj: OneOrMany, many: bool | None = None) -> OneOrManyEncoded: ...
    @overload
    def dumps(self, obj: list[T], many: bool | None = None, *args, **kwargs) -> str: ...
    @overload
    def dumps(self, obj: T, many: bool | None = None, *args, **kwargs) -> str: ...
    def dumps(
        self, obj: OneOrMany, many: bool | None = None, *args, **kwargs
    ) -> str: ...
    @overload
    def load(
        self,
        data: list[EncodedDict],
        many: bool = True,
        partial: bool | None = None,
        unknown: str | None = None,
    ) -> list[T]: ...
    @overload
    def load(
        self,
        data: EncodedDict,
        many: bool | None = None,
        partial: bool | None = None,
        unknown: str | None = None,
    ) -> T: ...
    def load(
        self,
        data: OneOrManyEncoded,
        many: bool | None = None,
        partial: bool | None = None,
        unknown: str | None = None,
    ) -> OneOrMany: ...
    @overload
    def loads(
        self,
        json_data: JsonInput,
        many: bool = True,
        partial: bool | None = None,
        unknown: str | None = None,
        **kwargs,
    ) -> list[T]: ...
    @overload
    def loads(
        self,
        json_data: JsonInput,
        many: bool | None = None,
        partial: bool | None = None,
        unknown: str | None = None,
        **kwargs,
    ) -> T: ...
    def loads(
        self,
        json_data: JsonInput,
        many: bool | None = None,
        partial: bool | None = None,
        unknown: str | None = None,
        **kwargs,
    ) -> OneOrMany: ...

SchemaType = SchemaF[T]
