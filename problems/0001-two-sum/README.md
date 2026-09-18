# 1. Two Sum

[leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum/) — Easy

## Problem

Given an array of integers `nums` and an integer `target`, return the indices of the two
numbers that add up to `target`.

You may assume exactly one valid answer exists, and you may not use the same element twice.
The answer may be returned in any order.

## Examples

| `nums` | `target` | Output | Why |
| --- | --- | --- | --- |
| `[2, 7, 11, 15]` | `9` | `[0, 1]` | `nums[0] + nums[1] == 9` |
| `[3, 2, 4]` | `6` | `[1, 2]` | `nums[1] + nums[2] == 6` |
| `[3, 3]` | `6` | `[0, 1]` | the two equal values are distinct elements |

## Constraints

- `2 <= len(nums) <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Exactly one valid answer exists.

## Solutions

| File | Approach | Time | Space |
| --- | --- | --- | --- |
| [`brute_force.py`](solutions/brute_force.py) | Check every pair | O(n²) | O(1) |
| [`hash_map.py`](solutions/hash_map.py) | One pass, value → index dict | O(n) | O(n) |

## Notes

Because any order is accepted, the tests assert that the returned pair is *valid* — two
distinct in-range indices whose values sum to the target — rather than comparing against one
literal expected list.

The third example is the case that catches a common bug: a solution that builds its whole
lookup table before scanning will match `3` against itself and return `[0, 0]`.
