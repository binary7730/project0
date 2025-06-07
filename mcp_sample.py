import sys
from typing import List


def min_cost_path(cost: List[List[int]]) -> int:
    if not cost or not cost[0]:
        raise ValueError("Cost matrix must not be empty")

    rows, cols = len(cost), len(cost[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = cost[0][0]

    # initialize first column
    for i in range(1, rows):
        dp[i][0] = dp[i-1][0] + cost[i][0]

    # initialize first row
    for j in range(1, cols):
        dp[0][j] = dp[0][j-1] + cost[0][j]

    # fill the rest
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = cost[i][j] + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[-1][-1]


if __name__ == "__main__":
    sample_cost = [
        [1, 2, 3],
        [4, 8, 2],
        [1, 5, 3],
    ]
    result = min_cost_path(sample_cost)
    print("Minimum cost path:", result)
