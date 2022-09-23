import pickle

import pytest

from routrie import Router


def test_routing() -> None:
    router = Router(
        routes={
            "/": 0,
            "/users": 1,
            "/users/:id": 2,
            "/users/:id/:org": 3,
            "/users/:user_id/repos": 4,
            "/users/:user_id/repos/:id": 5,
            "/users/:user_id/repos/:id/*any": 6,
            "/:username": 7,
            "/:any*": 8,
            "/about": 9,
            "/about/": 10,
            "/about/us": 11,
            "/users/repos/*any": 12,
        }
    )

    # Matched "/"
    node = router.find("/")
    assert node is not None
    match, params = node
    assert match == 0
    assert params == []

    # Matched "/:username"
    node = router.find("/username")
    assert node is not None
    match, params = node
    assert match == 7
    assert params == [("username", "username")]

    # Matched "/*any"
    node = router.find("/user/s")
    assert node is not None
    match, params = node
    assert match == 8
    assert params == [("any", "user/s")]


def test_no_match() -> None:
    router = Router(routes={"/": 0})

    # No match
    node = router.find("/noway-jose")
    assert node is None


def test_empty_path() -> None:
    router = Router(routes={"/": 0, "": 1,})

    node = router.find("/")
    assert node is not None
    match, params = node
    assert match == 0
    assert params == []

    node = router.find("")
    assert node is not None
    match, params = node
    assert match == 1
    assert params == []


def test_serialization() -> None:
    router = Router({"/": 0})

    router: Router[int] = pickle.loads(pickle.dumps(router))

    # No match
    node = router.find("/noway-jose")
    assert node is None
    # Match
    node = router.find("/")
    assert node is not None
    match, params = node
    assert match == 0
    assert params == []


def test_duplicate_route() -> None:
    # only the last one is preserved
    router = Router(
        routes=dict(
            [
                ("/:foo", 0),
                ("/:bar", 1),
            ]
        )
    )

    node = router.find("/baz")
    assert node is not None
    match, params = node
    assert match == 0
    assert params == [("foo", "baz")]


if __name__ == "__main__":
    pytest.main()
