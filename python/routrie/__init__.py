from __future__ import annotations

from typing import Generic, List, Optional, Tuple, TypeVar

from routrie._routrie import Router as _Router

T = TypeVar("T")

Params = List[Tuple[str, str]]
Match = Tuple[T, Params]


class Router(Generic[T]):
    __slots__ = ("_router",)

    _router: "_Router[T]"

    def __init__(self) -> None:
        self._router = _Router()

    def insert(self, path: str, value: T) -> None:
        self._router.insert(path, value)

    def find(self, path: str) -> Optional[Match[T]]:
        return self._router.find(path)
