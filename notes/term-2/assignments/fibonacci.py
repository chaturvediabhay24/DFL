"""
Complexity Analysis
-------------------
The naive recursive or iterative approach computes F(n) in O(n) time by
calculating every term from F(1) up to F(n). Matrix exponentiation exploits
the relation:

    | F(n+1) |   | 1  1 |^(n-1)   | F(2) |
    | F(n)   | = | 1  0 |       *  | F(1) |

Instead of multiplying the matrix n-1 times (which would still be O(n)),
we use exponentiation by squaring (binary exponentiation). At each step we
square the current matrix (halving the remaining exponent), so we perform
only O(log n) matrix multiplications. Each 2x2 matrix multiplication is a
constant-time operation (eight multiplications and four additions), giving
an overall time complexity of O(log n) and O(1) auxiliary space.
"""

MOD = 10**9 + 7


def mat_mult(A, B):
    """Multiply two 2x2 matrices under MOD."""
    return [
        [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % MOD,
         (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % MOD],
        [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % MOD,
         (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % MOD],
    ]


def mat_pow(M, p):
    """Raise a 2x2 matrix M to the power p using binary exponentiation."""
    result = [[1, 0],
              [0, 1]]  # identity matrix
    while p:
        if p & 1:
            result = mat_mult(result, M)
        M = mat_mult(M, M)
        p >>= 1
    return result


def fibonacci(n):
    """Return F(n) mod 10^9+7 with F(1)=1, F(2)=2 via matrix exponentiation."""
    if n == 1:
        return 1
    if n == 2:
        return 2
    T = [[1, 1],
         [1, 0]]
    # T^(n-2) * [F(2), F(1)]^T gives [F(n), F(n-1)]^T
    Tn = mat_pow(T, n - 2)
    return (Tn[0][0] * 2 + Tn[0][1] * 1) % MOD


if __name__ == "__main__":
    n = int(input())
    print(fibonacci(n))
