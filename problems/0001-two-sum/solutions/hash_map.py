"""Single pass, remembering each value's index as we go.

For every number we ask whether its complement has already been seen, which turns the
inner search of the brute force into a dict lookup.

Time O(n), space O(n).
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
