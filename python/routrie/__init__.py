from __future__ import annotations

from typing import Generic, Mapping, Optional, Sequence, Tuple, Type, TypeVar

from routrie._routrie import Router as _Router

T = TypeVar("T")

Route = Tuple[str, T]
Params = Sequence[Tuple[str, str]]
Match = Tuple[T, Params]


class Router(Generic[T]):
    __slots__ = ("_router", "_routes")

    _router: _Router[T]
    _routes: Mapping[str, T]

    def __init__(self, routes: Mapping[str, T]) -> None:
        self._router = _Router()
        self._routes = dict(routes)
        for path, value in routes.items():
            self._router.insert(path, value)

    def find(self, path: str) -> Optional[Match[T]]:
        return self._router.find(path)

    def __reduce__(
        self,
    ) -> Tuple[Type[Router[T]], Tuple[Mapping[str, T]]]:
        return (self.__class__, (self._routes,))
