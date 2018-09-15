class Solution(object):
    def twoSum(self,nums,target):
        if len(nums) <= 1:
            return False
        buff_dict = {}
        for i in range(len(nums)):
            if nums[i] in buff_dict:
                return [buff_dict[nums[i]],i]
            else:
                buff_dict[target - nums[i]] = i

if __name__=="__main__":
    twoSum = Solution()
    print(twoSum.twoSum([2,7,11,2,15],9))