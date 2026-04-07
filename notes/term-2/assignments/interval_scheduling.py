"""
Complexity Analysis
-------------------
Sorting criterion: sort by END TIME (ascending).

Why sorting by end time guarantees the optimal solution:
    By always picking the activity that finishes earliest (and doesn't
    conflict with the previously selected activity), we leave the maximum
    possible remaining time for future activities. This is the classic
    greedy choice for the Activity Selection / Interval Scheduling problem.

    Proof sketch (exchange argument):
        Let OPT be any optimal solution and let G be the greedy solution.
        We can show |G| >= |OPT| by inductively replacing each activity in
        OPT with the corresponding greedy choice. Because the greedy choice
        always has an end time <= the replaced activity's end time, no new
        conflicts are introduced, so the replacement is valid. Therefore
        the greedy solution is optimal.

    Why other criteria fail:
        - Sorting by start time: e.g. [0, 100], [1, 2], [3, 4] — picking
          the earliest start grabs [0, 100] and blocks everything else.
        - Sorting by duration: e.g. [0, 3], [2, 5], [4, 7] — the shortest
          interval [2, 5] conflicts with both others, yielding only 1
          instead of the optimal 2.

Time  complexity: O(n log n)  — dominated by the sort.
Space complexity: O(n)        — storing the list of intervals.
"""


def max_scheduled_activities(intervals):
    """Return the maximum number of non-conflicting activities.

    Parameters
    ----------
    intervals : list[list[int]]
        Each element is [start, end] with start < end.

    Returns
    -------
    int
        Maximum count of mutually non-overlapping intervals.
    """
    # Sort by end time; ties broken by start time (not strictly necessary)
    intervals.sort(key=lambda x: x[1])

    count = 0
    last_end = -1  # nothing selected yet

    for start, end in intervals:
        if start >= last_end:  # no overlap (touching endpoints are OK)
            count += 1
            last_end = end

    return count


if __name__ == "__main__":
    n = int(input())
    intervals = []
    for _ in range(n):
        s, e = map(int, input().split())
        intervals.append([s, e])
    print(max_scheduled_activities(intervals))
