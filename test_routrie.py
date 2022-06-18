import pytest

from routrie import Router


def test_routing() -> None:
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
    router: Router[int] = Router()
    router.insert("/", 0)

    # No match
    node = router.find("/noway-jose")
    assert node is None


if __name__ == "__main__":
    pytest.main()
