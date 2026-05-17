"""
Time Complexity Analysis:
=========================
Karatsuba Algorithm achieves O(n^1.58) vs naive O(n^2) digit-wise multiplication.

Naive multiplication: multiplying two n-digit numbers requires n^2 single-digit
multiplications (each digit of one number multiplied by each digit of the other).

Karatsuba reduces this by splitting each n-digit number into two halves of size n/2:
    M = m1 * 10^k + m0
    N = n1 * 10^k + n0

Normally this split gives 4 recursive multiplications (m0*n0, m0*n1, m1*n0, m1*n1).
Karatsuba observes that the middle term can be computed as:
    (m0+m1)*(n0+n1) - m0*n0 - m1*n1

This requires only 3 recursive multiplications instead of 4:
    z0 = m0 * n0
    z1 = (m0 + m1) * (n0 + n1)
    z2 = m1 * n1
    middle = z1 - z0 - z2

Recurrence relation: T(n) = 3T(n/2) + O(n)
  - 3 recursive calls on inputs of size n/2  →  3T(n/2)
  - Splitting numbers and combining results takes O(n) time  →  O(n)

By the Master Theorem (case 1): a=3, b=2, f(n)=O(n)
    log_b(a) = log_2(3) ≈ 1.585
    Since f(n) = O(n^1) < O(n^log2(3)), the solution is:
    T(n) = O(n^log2(3)) ≈ O(n^1.585)

This beats the naive O(n^2) significantly for large numbers.
"""


def karatsuba(m, n, depth=0):
    # Base case for single-digit numbers
    if m < 10 or n < 10:
        return m * n

    # Calculate the split point (half the digits of the larger number)
    n_digits = max(len(str(m)), len(str(n)))
    half = n_digits // 2
    k = 10 ** half

    # Split M and N into high (m1, n1) and low (m0, n0) parts
    # M = m1 * 10^half + m0
    # N = n1 * 10^half + n0
    m0 = m % k
    m1 = m // k
    n0 = n % k
    n1 = n // k

    # Three recursive multiplications (Karatsuba's key insight)
    z0 = karatsuba(m0, n0, depth + 1)          # z0 = m0 * n0
    z1 = karatsuba(m0 + m1, n0 + n1, depth + 1)  # z1 = (m0+m1) * (n0+n1)
    z2 = karatsuba(m1, n1, depth + 1)          # z2 = m1 * n1

    # Print intermediate values only for the top-level (first) call
    if depth == 0:
        print(f"z0: {z0} ({m0} x {n0})")
        print(f"z1: {z1} (({m0}+{m1}) x ({n0}+{n1}))")
        print(f"z2: {z2} ({m1} x {n1})")

    # Combine: M*N = z2 * 10^(2*half) + (z1 - z2 - z0) * 10^half + z0
    final_result = (z2 * k * k) + ((z1 - z2 - z0) * k) + z0
    return final_result


if __name__ == "__main__":
    m = int(input().strip())
    n = int(input().strip())
    result = karatsuba(m, n)
    print(f"Result: {result}")
