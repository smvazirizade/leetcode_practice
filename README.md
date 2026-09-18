# leetcode_practice

I created this repo to share my solution for some Leetcode problems. I hope that will be useful
for you.

Each problem gets a folder holding the problem statement, its unit tests, and one or more
solutions. Tests discover solutions from the filesystem, so every solution in a problem's
`solutions/` folder is run against that problem's full test suite on every push.

## Layout

```
problems/
  0001-two-sum/
    README.md              problem statement, constraints, examples
    solutions/             one file per approach
      brute_force.py
      hash_map.py
    tests/
      test_two_sum.py      runs against every file in solutions/
harness.py                 load_solutions() -- the discovery helper
pyproject.toml             pytest + ruff config
requirements-dev.txt       pytest, ruff
.github/workflows/ci.yml   lint, format check, tests
```

## Running the tests

```
pip install -r requirements-dev.txt
pytest -v
```

`-v` shows one case per solution, e.g. `test_leetcode_examples[example-1-hash_map]`.

To run a single problem:

```
pytest problems/0001-two-sum -v
```

Lint and format, the same two checks CI runs:

```
ruff check .
ruff format --check .
```

## Adding a solution to an existing problem

Drop a new `.py` file in that problem's `solutions/` folder with a `Solution` class exposing the
same method name the problem already uses:

```python
"""One line on the approach. Time O(n), space O(n)."""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        return []  # your approach here
```

That is the whole step. No test file changes — `load_solutions` finds the file, and CI runs it
against the existing tests on the next push. The test ids use the filename, so name it after the
approach (`hash_map`, `sorted_two_pointer`) rather than `solution2`.

A solution that fails to import, or that lacks the expected class or method, fails only its own
test cases; the other solutions still run.

## Adding a new problem

1. `mkdir -p problems/<NNNN>-<slug>/{solutions,tests}` — four-digit LeetCode id, hyphenated slug.
2. Write `README.md` with the statement, constraints, and examples.
3. Add at least one solution under `solutions/`.
4. Add `tests/test_<slug>.py`. The only bespoke line is the method name:

```python
from harness import load_solutions

SOLUTIONS = load_solutions(__file__, "<methodName>")


@pytest.mark.parametrize("solve", SOLUTIONS)
def test_examples(solve):
    assert solve([2, 7, 11, 15], 9) == [0, 1]
```

Prefer asserting that an answer is *valid* over comparing it to one literal expected value —
many LeetCode problems accept more than one correct output, and an over-strict assertion will
reject a correct solution.

## License

MIT — see [LICENSE](LICENSE).
