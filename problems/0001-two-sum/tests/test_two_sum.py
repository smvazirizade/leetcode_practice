"""Tests for Two Sum, run against every solution in ../solutions/.

The parametrization is filesystem-driven: adding a solution module adds a case to each test
below with no edit here.
"""

import pytest

from harness import load_solutions

SOLUTIONS = load_solutions(__file__, "twoSum")


def assert_valid_pair(nums: list[int], target: int, result) -> None:
    """Assert `result` is an acceptable answer for Two Sum.

    LeetCode accepts the indices in either order, so this checks the properties an answer
    must have rather than equality against one literal list.
    """
    assert isinstance(result, (list, tuple)), f"expected a list of two indices, got {result!r}"
    assert len(result) == 2, f"expected two indices, got {result!r}"

    i, j = result
    assert i != j, f"the same element was used twice (index {i})"
    assert 0 <= i < len(nums), f"index {i} out of range"
    assert 0 <= j < len(nums), f"index {j} out of range"
    assert nums[i] + nums[j] == target, (
        f"nums[{i}] + nums[{j}] == {nums[i] + nums[j]}, expected {target}"
    )


@pytest.mark.parametrize("two_sum", SOLUTIONS)
@pytest.mark.parametrize(
    ("nums", "target"),
    [
        pytest.param([2, 7, 11, 15], 9, id="example-1"),
        pytest.param([3, 2, 4], 6, id="example-2"),
        pytest.param([3, 3], 6, id="example-3-duplicate-values"),
    ],
)
def test_leetcode_examples(two_sum, nums, target):
    assert_valid_pair(nums, target, two_sum(nums, target))


@pytest.mark.parametrize("two_sum", SOLUTIONS)
@pytest.mark.parametrize(
    ("nums", "target"),
    [
        pytest.param([1, 2], 3, id="minimum-length"),
        pytest.param([-3, 4, 3, 90], 0, id="negatives"),
        pytest.param([-1, -2, -3, -4], -7, id="all-negative"),
        pytest.param([0, 4, 3, 0], 0, id="two-zeros"),
        pytest.param([5, 1, 7, 2, 9], 11, id="answer-at-the-end"),
        pytest.param([10**9, 10**9], 2 * 10**9, id="constraint-bounds"),
    ],
)
def test_edge_cases(two_sum, nums, target):
    assert_valid_pair(nums, target, two_sum(nums, target))


@pytest.mark.parametrize("two_sum", SOLUTIONS)
def test_larger_input(two_sum):
    """A thousand elements: enough to catch an accidental O(n^3), small enough that the
    legitimate O(n^2) brute force still finishes instantly."""
    nums = list(range(1, 1001))
    target = 1999  # only 999 + 1000 reaches it

    assert_valid_pair(nums, target, two_sum(nums, target))


@pytest.mark.parametrize("two_sum", SOLUTIONS)
def test_does_not_mutate_input(two_sum):
    """Indices must refer to the caller's array, so a solution may not reorder it in place."""
    nums = [5, 1, 7, 2, 9]
    original = list(nums)

    two_sum(nums, 11)

    assert nums == original, "the input list was modified"
