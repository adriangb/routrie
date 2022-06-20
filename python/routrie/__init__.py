from __future__ import annotations

from typing import Callable, Dict, Generic, List, Optional, Tuple, TypeVar

from routrie._routrie import Router as _Router

T = TypeVar("T")

Params = List[Tuple[str, str]]
Match = Tuple[T, Params]


def _deserialize(routes: Dict[str, T]) -> "Router[T]":
    router: "Router[T]" = Router()
    for path, value in routes.items():
        router.insert(path, value)
    return router


class Router(Generic[T]):
    __slots__ = ("_router", "_routes")

    _router: _Router[T]
    _routes: Dict[str, T]

    def __init__(self) -> None:
        self._router = _Router()
        self._routes = {}

    def insert(self, path: str, value: T) -> None:
        self._router.insert(path, value)
        self._routes[path] = value

    def find(self, path: str) -> Optional[Match[T]]:
        return self._router.find(path)

    def __reduce__(
        self,
    ) -> Tuple[Callable[[Dict[str, T]], Router[T]], Tuple[Dict[str, T]]]:
        return (_deserialize, (self._routes,))
