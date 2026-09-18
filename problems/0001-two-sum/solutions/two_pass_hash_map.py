"""Two passes: index every value first, then look up each complement.

Time O(n), space O(n).
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        index = {num: i for i, num in enumerate(nums)}
        for i, num in enumerate(nums):
            j = index.get(target - num)
            if j is not None:
                return [i, j]
        return []
