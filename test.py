# import numpy as np

# def normalize_scores(scores: list[list[int]]) -> float:
#     # Your code here
#     scores_np=np.array(scores)
#     n_row,c_col=scores_np.shape
#     sum=np.sum(scores_np,axis=0)
#     sum_mean=sum/n_row
#     normalized_scores=scores_np-sum_mean
#     mean=np.mean(normalized_scores)
#     rounded_mean=np.round(mean,2)
#     return rounded_mean


# scores=[[80, 75, 90], [85, 88, 92], [78, 82, 85], [90, 91, 88]]
# result=normalize_scores(scores)
# print(result)


# import numpy as np

# def apply_discounts(prices: list[list[int]], discounts: list[int]) -> float:
#     # Your code here
#     np_prices=np.array(prices)
#     np_discounts=np.array(discounts)
#     np_discounts_multiplier=1-np_discounts/100
#     discounted_price=np_prices*np_discounts_multiplier
#     result=discounted_price.max()
#     return result.round(2)
# prices=[[100, 110, 120, 105], [150, 160, 140, 155], [200, 210, 190, 205]]
# discount=[10, 15, 20, 5]
# apply_discounts(prices,discount)

from typing import List
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        letters={'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
        

        result=[]
        intermediate=[]

        def search(idx):
            if len(intermediate)==len(digits):
                result.append(intermediate.copy())
                # print(result)
                return 
            for letter in letters[digits[idx]]:
                intermediate.append(letter)
                # print(intermediate)
                search(idx+1)
                intermediate.pop()

        search(0)
        return result        


if __name__=="__main__":
    digits = "23"
    ans=Solution().letterCombinations(digits)
    print(ans)