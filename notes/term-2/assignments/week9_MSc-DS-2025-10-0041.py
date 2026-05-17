"""
Name : Abhay Chaturvedi
Roll Number : MSc-DS-2025-10-0041
Time Complexity Analysis :
The Interval DP has three nested loops:
  1. Outer loop over chain length L: runs from 2 to n  → O(n) iterations.
  2. Middle loop over starting index i: for each L, i runs over ~n positions → O(n).
  3. Inner loop over split point k: for each (i, j) pair, k ranges from i to j-1 → O(n).
Total: O(n) * O(n) * O(n) = O(n^3).
Space is O(n^2) for the two 2D tables m and s.
"""

def solve_land_partition(p):
    n = len(p) - 1
    # m[i][j] stores the minimum cost to join blocks i..j (1-indexed)
    m = [[0] * (n + 1) for _ in range(n + 1)]
    # s[i][j] stores the index of the optimal split k
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # L is the chain length (number of blocks in the subproblem)
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m[1][n], s[1][n]

if __name__ == "__main__":
    dims = list(map(int, input().split()))
    min_cost, best_k = solve_land_partition(dims)
    print(min_cost)
    print(best_k)
