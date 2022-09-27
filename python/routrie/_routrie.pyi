from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")

Params = List[Tuple[str, str]]

class Router(Generic[T]):
    def insert(self, __path: str, __value: T) -> None: ...
    def find(self, __path: str) -> Tuple[T, Params]: ...
