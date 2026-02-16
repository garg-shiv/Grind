from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        
        mp: dict[int, int] = {}
        
        for i in range(len(nums)):
            req = target - nums[i]
            
            if req in mp:
                return [mp[req], i]
            
            mp[nums[i]] = i
        
        return []
