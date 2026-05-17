"""
Name : Abhay Chaturvedi
Roll Number : MSc-DS-2025-10-0041
Time Complexity Analysis :
The outer loop runs N times (once per item) and the inner loop runs W times
(once per capacity unit), giving O(N * W) time complexity. The backtracking
step is O(N + W) which is dominated by O(N * W). Space complexity is also
O(N * W) for the DP table.
"""

def solve_knapsack(n, capacity, weights, values):
    # Initialize DP table: dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Fill the DP Table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            # Take item i if it fits
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Backtrack to find the indices of items included
    selected_indices = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_indices.append(i)  # 1-indexed
            w -= weights[i - 1]

    max_val = dp[n][capacity]
    return max_val, selected_indices


if __name__ == "__main__":
    import sys
    # Input Handling
    try:
        n = int(input())
        w_limit = int(input())
        weights = []
        values = []
        for _ in range(n):
            w, v = map(int, input().split())
            weights.append(w)
            values.append(v)

        max_val, items = solve_knapsack(n, w_limit, weights, values)
        print(max_val)
        print(*(sorted(items)))
    except EOFError:
        pass
