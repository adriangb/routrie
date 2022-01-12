import typing

T = typing.TypeVar("T")

class Param:
    name: str
    value: str

class Match(typing.Generic[T]):
    value: T
    params: typing.Sequence[Param]

class Router(typing.Generic[T]):
    def insert(self, path: str, value: T, /) -> None: ...
    def find(self, path: str, /) -> typing.Optional[Match[T]]: ...
