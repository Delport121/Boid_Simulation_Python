from typing import List

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        value: int = 0
        new_digits: List[int] = []
        for i in range(0, len(digits), 1):
            value += digits[i] * (10 ** (len(digits) - i -1))

        value += 1

        while value > 0:
            new_digits.insert(0, value % 10)
            value = value // 10

        return new_digits
    
if __name__ == '__main__':
    Test_list = [1,2,3]
    sol = Solution()
    print(sol.plusOne(Test_list))
