**Coding, Algorithms & Data Structures**

*Interview Q&A --- Deep Dive*

**Complexity & Core DS**

1.  **What is the time and space complexity of common data structures?**

> Array: O(1) access, O(n) search/insert/delete. Hash Map: O(1) avg
> get/set, O(n) worst (hash collisions). Linked List: O(n) search, O(1)
> insert/delete at known node. Binary Search Tree (balanced): O(log n)
> get/insert/delete. Heap (min/max): O(log n) insert/extract-min, O(1)
> peek. For ML system design: use hash maps for feature lookups and
> caching, heaps for top-k scoring (beam search), and arrays/NumPy for
> vectorised computation. Understanding complexity helps choose the
> right data structure for feature stores and real-time inference
> pipelines.

2.  **Explain the sliding window technique and give an ML use case.**

> Sliding window maintains a window of size k over a sequence, advancing
> one element at a time. Avoids O(nk) nested loops by updating the
> window incrementally in O(1). Classic problems: maximum sum subarray
> of size k, longest substring without repeating characters. ML use
> case: computing rolling statistics for real-time features (30-day
> transaction sum per user). Maintain a running sum --- add new element,
> subtract element leaving the window --- O(1) per update instead of
> recomputing the sum from scratch.

**Sorting & Searching**

3.  **Explain quicksort, merge sort, and heap sort. When to use each?**

> Quicksort: O(n log n) avg, O(n²) worst (poor pivot), O(log n) space.
> In-place, cache-friendly, fast in practice --- Python\'s sort uses
> Timsort (hybrid merge+insertion). Merge sort: O(n log n) always, O(n)
> extra space. Stable, preferred for linked lists and external sort
> (datasets larger than RAM). Heap sort: O(n log n) always, O(1) extra
> space. Not stable, poor cache performance. In ML: use Python\'s
> built-in sort (Timsort) for in-memory data; use merge sort logic for
> external sorting of large training datasets; use partial_sort
> (heap-based) for top-k retrieval.

4.  **How would you find the top-k most frequent elements in a stream?**

> Use a min-heap of size k: iterate through elements, maintaining a
> frequency count (hash map). Push each element\'s frequency to the
> heap; if heap size \> k, pop the minimum. At the end, heap contains
> the k most frequent. Time: O(n log k), Space: O(n) for frequency map +
> O(k) for heap. For streaming/infinite streams: Count-Min Sketch
> (probabilistic) estimates frequencies with O(width \* depth) space,
> far less than exact counting --- suitable when exact counts are not
> required for recommendation or trending topics.

**Graphs & Trees**

5.  **Explain BFS vs DFS and their use cases in ML systems.**

> BFS (Breadth-First Search): explores layer by layer using a queue.
> Finds shortest path in unweighted graphs. O(V+E). Use cases in ML:
> knowledge graph traversal to find related entities within k hops,
> computing graph features for GNNs, and distributed computation graphs
> for operator placement. DFS (Depth-First Search): explores deep along
> each branch using a stack (or recursion). O(V+E). Use cases:
> topological sort for ML pipeline DAGs (determines execution order of
> Airflow tasks), cycle detection in dependency graphs, and tree-based
> data structures.

6.  **How do you detect a cycle in a directed graph? Application to ML
    pipelines.**

> Use DFS with three states per node: unvisited, in-progress (in current
> DFS stack), visited. If you encounter an in-progress node, a cycle
> exists. Alternatively, Kahn\'s algorithm (BFS-based topological sort):
> compute in-degrees, start from zero in-degree nodes; if not all nodes
> are processed, a cycle exists. ML application: Airflow DAG validation
> runs cycle detection before scheduling --- a cycle would cause tasks
> to wait for each other indefinitely. MLflow\'s model lineage graph and
> computation graphs in TensorFlow/PyTorch also use topological ordering
> for correct execution.

**Dynamic Programming**

7.  **What is dynamic programming? Explain memoisation vs tabulation.**

> DP solves problems by breaking them into overlapping subproblems and
> caching results to avoid recomputation. Memoisation (top-down):
> recursive solution with a cache (dict); only computes subproblems
> needed. Tabulation (bottom-up): iteratively fills a table from base
> cases. Tabulation is typically more space-efficient (no call stack
> overhead). ML connections: the Viterbi algorithm (CRF decoding for
> NER/POS tagging) is DP over the sequence. Edit distance (Levenshtein)
> for fuzzy string matching. DTW (Dynamic Time Warping) for time-series
> similarity. Beam search in LLM decoding uses DP-like state expansion
> with pruning.

**Concurrency & Parallelism**

8.  **Explain race conditions, deadlocks, and how to prevent them.**

> Race condition: two threads access shared state concurrently and the
> result depends on execution order. Prevention: locks (mutex), atomic
> operations, or using thread-safe data structures (queue.Queue in
> Python). Deadlock: two threads each hold a resource the other needs,
> waiting indefinitely. Prevention: lock ordering (always acquire locks
> in the same order), timeout-based lock acquisition, or using a single
> lock for both resources. In ML: race conditions arise in shared
> feature caches (use read-write locks or Redis atomic operations);
> deadlocks arise in complex Kafka consumer group rebalances (proper
> timeout configuration prevents them).

**System Design Coding**

9.  **How would you implement an LRU Cache in Python?**

> Use an OrderedDict (maintains insertion/access order): on get, move
> the accessed key to the end; on put, add to end, and if over capacity,
> pop the first (least recently used) item. Time: O(1) for both get and
> put. Alternative: doubly linked list + hash map --- hash map gives
> O(1) lookup; DLL gives O(1) move-to-front and eviction. Python\'s
> functools.lru_cache decorator uses this pattern. ML use case: cache
> the most recently computed embedding vectors for hot user IDs in a
> recommendation system, avoiding repeated model inference.
