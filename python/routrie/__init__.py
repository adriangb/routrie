from __future__ import annotations

import typing

from routrie.routrie import Match, Param
from routrie.routrie import Router as _Router

__all__ = ("Router", "Match", "Param")


T = typing.TypeVar("T")


class Router(typing.Generic[T]):
    __slots__ = ("_router",)

    _router: _Router[T]

    def __init__(self) -> None:
        self._router = _Router()

    def insert(self, path: str, value: T) -> None:
        self._router.insert(path, value)

    def find(self, path: str) -> typing.Optional[Match[T]]:
        return self._router.find(path)
