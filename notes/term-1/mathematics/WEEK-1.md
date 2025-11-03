# 1.1 Sets, relations and functions

## 1.1.1 Sets

- Set: a collection of distinct objects (elements).
- Empty set: ∅ (also written {}), |∅| = 0.
- Cardinality: |A| denotes the number of elements in set A.

### Power set
- Power set of A, written P(A), is the set of all subsets of A.
- Example: if A = {1, 2} then P(A) = {∅, {1}, {2}, {1, 2}}.
- If |A| = n then |P(A)| = 2^n.

### Union, intersection, difference, complement
- Union: A ∪ B = {x : x ∈ A or x ∈ B}.
- Intersection: A ∩ B = {x : x ∈ A and x ∈ B}.
- Set difference: A \ B = {x : x ∈ A and x ∉ B}.
- Universal set: U (the domain under consideration).
- Complement: A^c = U \ A = {x ∈ U : x ∉ A}.

### Cardinality formulas and inequalities
- |A ∪ B| = |A| + |B| − |A ∩ B|.
- In particular |A ∪ B| ≤ |A| + |B|.
- |A ∩ B| ≤ min(|A|, |B|).

### Laws (important identities)
- Distributive law: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C).
- De Morgan's laws:
  - (A ∪ B)^c = A^c ∩ B^c
  - (A ∩ B)^c = A^c ∪ B^c




## 1.2 Relations
### Cartesian product
The Cartesian product of two sets A and B is

\[A \times B = \{(a,b) : a \in A,\; b \in B\}.\]

Example: if A = {1,2} and B = {x,y} then

\[A \times B = \{(1,x),(1,y),(2,x),(2,y)\}.\]

Note: in general A \times B \neq B \times A (the ordered pairs are reversed).

If X = {0,1} then X^n denotes the n-fold Cartesian product X \times X \times \cdots \times X (n times).

Properties of Cartesian product
- A \times (B \cup C) = (A \times B) \cup (A \times C)
- A \times \varnothing = \varnothing

### Relations
A relation R from A to B is any subset R \subseteq A \times B. When A = B we say R is a relation on A.

We write (a,b) \in R equivalently as "a R b".

Example: the "less than or equal" relation on integers is

\[R = \{(m,n) \in \mathbb{Z} \times \mathbb{Z} : m \le n\}.\]

Common properties of relations (for R on a set A):

1. Reflexive: for all a \in A, (a,a) \in R.
  - Example: \(\le\) on numbers is reflexive, but "<" is not.

2. Symmetric: for all a,b \in A, if (a,b) \in R then (b,a) \in R.
  - Example: equality (=) is symmetric; \(\le\) is not.

3. Antisymmetric: for all a,b \in A, if (a,b) \in R and (b,a) \in R then a = b.
  - Example: \(\le\) is antisymmetric on numbers.

4. Transitive: for all a,b,c \in A, if (a,b) \in R and (b,c) \in R then (a,c) \in R.
  - Many order relations are transitive.

5. Irreflexive (or anti-reflexive): for all a \in A, (a,a) \notin R.
  - Example: the strict "<" relation is irreflexive.

Notes on combinations:
- An equivalence relation is a relation that is reflexive, symmetric and transitive.
  - Example: equality (=) and congruence modulo n on integers.

- A partial order is a relation that is reflexive, antisymmetric and transitive.
  - Example: \(\le\) on numbers.

- A total (or linear) order is a partial order in which any two elements are comparable: for all a,b \in A, either (a,b) \in R or (b,a) \in R (or both).

### Examples
1. Equality on any set A:
  - R = { (a,a) : a \in A } (this relation is reflexive, symmetric, transitive — in fact it's the prototypical equivalence relation).

2. "Less than or equal" (\(\le\)) on real numbers:
  - Reflexive, antisymmetric, transitive — so it's a partial order; since any two reals are comparable it's a total order.

3. A non-transitive relation example:
  - On A = {a,b,c}, let R = { (a,b), (b,c) } then (a,c) \notin R, so R is not transitive.
