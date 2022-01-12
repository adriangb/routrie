from typing import Iterable, List, Tuple

import pytest

from routrie import Router, Param


def params_to_tuple(params: Iterable[Param]) -> List[Tuple[str, str]]:
    return [(p.name, p.value) for p in params]


def test_routing():
    router: Router[int] = Router()
    router.insert("/", 0)
    router.insert("/users", 1)
    router.insert("/users/:id", 2)
    router.insert("/users/:id/:org", 3)
    router.insert("/users/:user_id/repos", 4)
    router.insert("/users/:user_id/repos/:id", 5)
    router.insert("/users/:user_id/repos/:id/*any", 6)
    router.insert("/:username", 7)
    router.insert("/*any", 8)
    router.insert("/about", 9)
    router.insert("/about/", 10)
    router.insert("/about/us", 11)
    router.insert("/users/repos/*any", 12)

    # Matched "/"
    node = router.find("/")
    assert node is not None
    assert node.value == 0
    assert params_to_tuple(node.params) == []

    # Matched "/:username"
    node = router.find("/username")
    assert node is not None
    assert node.value == 7
    assert params_to_tuple(node.params) == [("username", "username")]

    # Matched "/*any"
    node = router.find("/user/s")
    assert node is not None
    assert node.value == 8
    assert params_to_tuple(node.params) == [("any", "user/s")]


if __name__ == "__main__":
    pytest.main()
