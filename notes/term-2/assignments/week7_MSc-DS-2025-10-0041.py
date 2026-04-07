# week7_MSc-DS-2025-10-0041.py

def find_lcs_length(x, y):
    """
    Calculates the length of the Longest Common Subsequence.
    Complexity: O(n1 * n2)
    Uses two rows instead of full DP table: Space O(min(n1, n2))
    """
    n1 = len(x)
    n2 = len(y)

    # Ensure y is the shorter string for space optimisation
    if n1 < n2:
        x, y = y, x
        n1, n2 = n2, n1

    # Two-row DP: prev holds dp[i-1][*], curr holds dp[i][*]
    prev = [0] * (n2 + 1)
    curr = [0] * (n2 + 1)

    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev

    return prev[n2]


if __name__ == "__main__":
    # Input handling
    str_x = input().strip()
    str_y = input().strip()

    # Function call and output
    print(find_lcs_length(str_x, str_y))
