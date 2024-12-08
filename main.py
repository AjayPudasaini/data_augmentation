# def binary_search(arr, target):
#     low = 0
#     high = len(arr)
    
#     while low <= high:
#         mid = (low + high) // 2
#         if arr[mid] == target:
#             return mid
#         elif arr[mid] < target:
#             low = mid + 1
#         else:
#             high = mid - 1
#     return -1


# data = [50,20, 30, 40, 60, 70, 80, 90, 100]

# target = 5000
# result = binary_search(data, target)
# print(result)


class Solution:
    def twoSum(self, nums, target):
        d = {}

        for c, i in enumerate(nums):
            ss = target - i

            if ss in d:
                return [d[ss], c]

            d[i] = c

        return []


nums = [2,7,11,15]


obj = Solution()

f = obj.twoSum(nums, 9)

print(f)
