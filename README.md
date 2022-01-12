# routrie

![CI](https://github.com/adriangb/routrie/actions/workflows/python.yaml/badge.svg)

A Python wrapper for Rust's `path-tree` router ([path-tree repo], [path-tree crate]).

This is a blazingly fast HTTP URL router with support for matching path parameters and catch-all URLs.

Usage:

```python
from routrie import Router, Param

# the generic parameter is the value being stored
# normally this will be an endpoint / route instance
router: Router[int] = Router()

router.insert("/users", 1)
router.insert("/users/:id", 2)
router.insert("/users/repos/*any", 3)

matched = router.find("/foo-bar-baz")
assert matched is None

matched = router.find("/users/routrie")
assert matched is not None
assert matched.value == 2
assert matched.params[0].name == "id"
assert matched.params[0].value == "routrie"

matched = router.find("/users")
assert matched is not None
assert matched.value == 1
assert matched.params == []

matched = router.find("/users/repos/)
assert matched is not None
assert matched.value == 3
assert matched.params == []

matched = router.find("/users/repos/something)
assert matched is not None
assert matched.value == 3
assert matched.params[0].name = "any"
assert matched.params[0].value = "something"
```

## Contributing

1. Clone the repo.
1. Run `make init`
1. Run `make test`
1. Make your changes
1. Push and open a pull request
1. Wait for CI to run.

If your pull request gets approved and merged, it will automatically be relased to PyPi (every commit to `main` is released).

[path-tree repo]: https://github.com/viz-rs/path-tree
[path-tree crate]: https://crates.io/crates/path-tree/0.1.8/dependencies
