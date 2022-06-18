from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")

Params = List[Tuple[str, str]]

class Router(Generic[T]):
    def insert(self, path: str, value: T, /) -> None: ...
    def find(self, path: str, /) -> Tuple[T, Params]: ...
