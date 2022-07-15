from concurrent.futures import ThreadPoolExecutor, wait
import os
import pickle
from time import time

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
            "/*any": 8,
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
    assert match == 1
    assert params == [("bar", "baz")]


cpu_count = os.cpu_count()


@pytest.mark.skipif(
    not cpu_count or cpu_count < 2, reason="this test requires at least 2 CPU cores"
)
def test_gil_release() -> None:
    # make a really large routing tree so that we spend a good chunk of time in Rust
    total_routes = 100_000
    routes = {
        f"/:part1_{n}" + f"/foo/bar/baz" * 1_000 + f"/:part2_{n}": n
        for n in range(total_routes)
    }
    router = Router(routes)

    def match() -> None:
        for n in range(total_routes):
            path = f"/part1_{n}" + f"/foo/bar/baz" * 1_000 + f"/part2_{n}"
            match = router.find(path)
            assert match is not None

    start = time()
    match()
    match()
    end = time()
    elapsed_sequential = end - start

    start = time()
    with ThreadPoolExecutor(max_workers=2) as exec:
        futures = (
            exec.submit(match),
            exec.submit(match),
        )
        wait(futures)
    end = time()
    elapsed_threads = end - start

    assert elapsed_threads < elapsed_sequential * 0.75, (
        elapsed_threads,
        elapsed_sequential,
    )


if __name__ == "__main__":
    pytest.main()
