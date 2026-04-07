import sys
input = sys.stdin.readline

def main():
    n = int(input())
    boxes = []
    for _ in range(n):
        l, w, h = map(int, input().split())
        boxes.append((l, w, h))

    boxes.sort()

    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if boxes[j][0] <= boxes[i][0] and boxes[j][1] <= boxes[i][1] and boxes[j][2] <= boxes[i][2]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1

    print(max(dp))

main()
