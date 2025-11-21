# 2.1 Counting, Permutations and Combinations

## 2.1.1 Factorial and basic counting
- Factorial: for n ∈ Z_{
 0},
	n! = 1·2·3·…·n, with 0! = 1.
- Use factorials to count ordered arrangements of n distinct items.

## 2.1.2 Permutations
- Permutation: an ordered arrangement of distinct objects.
- Number of k-permutations of n distinct objects (ordered choices of k):

\[P(n,k)={}_nP_k = \frac{n!}{(n-k)!}.\]

- Special case: permutations of all n objects (k=n) gives n!.

## 2.1.3 Combinations (binomial coefficients)
- Combination: an unordered selection of k objects from n (order does not matter).
- Binomial coefficient ("n choose k"):

\[{n \choose k} = \frac{n!}{k!(n-k)!}.\]

- Relationship with permutations: {n \choose k} = P(n,k)/k!.

### Pascal's identity
\[{n \choose k} = {n-1 \choose k-1} + {n-1 \choose k}.\]

This gives Pascal's triangle and a quick recurrence for computing binomial coefficients.

### Binomial theorem
For any numbers x,y and non-negative integer n:

\[(x+y)^n = \sum_{k=0}^n {n \choose k} x^{n-k} y^k.\]

This expands powers and directly uses binomial coefficients as coefficients.

## 2.2 Graph theory basics

### Basic definitions
- Graph G = (V, E) where V is a set of vertices and E is a set of edges.
- Undirected graph: edges are unordered pairs {u,v}.
- Directed graph (digraph): edges are ordered pairs (u,v).
- Simple graph: no loops (edges from a vertex to itself) and no multiple edges between same vertices.

### Degree
- Degree (undirected): deg(v) is number of edges incident to v.
- For directed graphs: out-degree deg^+(v) (edges leaving v) and in-degree deg^-(v) (edges entering v).

### Paths, cycles and connectivity
- Path: a sequence of vertices with consecutive vertices connected by edges. Length = number of edges.
- Simple path: no repeated vertices.
- Cycle: a path that starts and ends at the same vertex with length ≥ 1 (simple cycle has no repeated vertices except start=end).
- Connected (undirected): there is a path between every pair of vertices.
- Strongly connected (directed): for every u,v there is a directed path u→v and v→u.

### Special graphs
- Bipartite graph: vertices can be partitioned into two disjoint sets U and W such that every edge goes between U and W (no edges inside U or W).
	- Equivalent condition: graph contains no odd-length cycles.
- DAG (Directed Acyclic Graph): a directed graph with no directed cycles. DAGs admit topological orderings.

### Useful facts
- Handshaking lemma (undirected): sum_{v∈V} deg(v) = 2|E|.
- A tree is a connected acyclic undirected graph. For a tree with |V|=n, |E| = n-1.

If you want, I can add small examples and solved exercises (compute P(n,k), {n \choose k}, simple graph diagrams) for each subsection.