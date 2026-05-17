"""
Name             : Abhay Chaturvedi
Roll Number      : MSc-DS-2025-10-0041
Time Complexity Analysis :
    Each cell (i, j) is processed by dfs exactly once — on the first call,
    we compute and store memo[i][j]; subsequent calls return immediately.
    Each dfs call examines at most 4 neighbours, so total work is O(4 * m * n)
    = O(m * n). The outer loop also iterates over all m * n cells, giving
    overall time complexity O(m * n).
"""

import sys
sys.setrecursionlimit(100000)

def longest_increasing_path(m, n, matrix):
    if m == 0 or n == 0:
        return 0

    # Memoization table: memo[i][j] = length of longest increasing
    # path STARTING at cell (i, j).
    memo = [[0 for _ in range(n)] for _ in range(m)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(i, j):
        if memo[i][j] != 0:
            return memo[i][j]

        best = 1
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                best = max(best, 1 + dfs(ni, nj))

        memo[i][j] = best
        return best

    longest = 0
    for i in range(m):
        for j in range(n):
            longest = max(longest, dfs(i, j))

    return longest


if __name__ == "__main__":
    try:
        m, n = map(int, input().split())
        matrix = []
        for _ in range(m):
            row = list(map(int, input().split()))
            matrix.append(row)

        result = longest_increasing_path(m, n, matrix)
        print(result)
    except EOFError:
        pass
