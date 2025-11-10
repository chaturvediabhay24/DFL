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

## 1.1.3 Functions
Function is a relation, where every element Ris cross product of A and B

for every ele of A should be uniquely related ele B

domain and co domain of function
range: possibl values in b for each a val;ues
range is subset of co domain B

#### surjective function - onto function
where every element in codomain is in range

#### injective function -  one one ffunction

for each ele domain should match to distict element of range co domain

#### bijective -  which is both injective and subjective
 
#### inverse of a function: 
 for binjective function b inverse in f-1:B-> A
inverse for non bijective function
write example of these for revision
f-1=pow(b)->pow(a)

#### composition of function
g of f
write example
composite of bijective function is bijective function

### Revision — Functions & Counting (short)
- Function f: A -> B assigns each a in A exactly one f(a) in B.
- Domain: A. Codomain: B. Range (image): f(A) ⊆ B.

- Injective (one-to-one): f(a1)=f(a2) ⇒ a1=a2. No two domain elements share the same image.
- Surjective (onto): f(A)=B (every b∈B is f(a) for some a∈A).
- Bijective: both injective and surjective. Bijective ⇔ has an inverse f^{-1}: B -> A.

- Inverse: If f is bijective then f^{-1}(f(a)) = a for all a∈A and f(f^{-1}(b)) = b for all b∈B.

- Composition: If f: A->B and g: B->C, the composition g∘f: A->C is defined by (g∘f)(a)=g(f(a)).
  - Composition of injective (resp. surjective, bijective) functions is injective (resp. surjective, bijective).

- Quick examples:
  - f(x)=2x from Z->Z is injective but not surjective (odd integers not in range).
  - f(x)=x mod n from Z->{0,...,n-1} is surjective; not injective.
  - f(x)=x on R is bijective.

- Counting rules (reminder):
  1) Multiplicative rule: if an action has k1 choices then k2, ... , kn choices independently, total choices = k1·k2·...·kn.
  2) Additive rule: for disjoint sets A and B, |A ∪ B| = |A| + |B|.
  3) Principle of Inclusion–Exclusion (two sets): |A ∪ B| = |A| + |B| − |A ∩ B|.
     (Three sets: |A ∪ B ∪ C| = |A|+|B|+|C| − |A∩B|−|A∩C|−|B∩C| + |A∩B∩C|.)


## 1.2.1. Additive and Multiplicative Rules
 #### Counting:
 finding size of a set, from its components
 1.  multiplicative rule
 if you take two set and take cross product the size will be sum of size of individual sets
 2. Additive rule:
 finding size of set a union b where these are disjoint
 is size of a + size of b
 3. Principle of inclusion and exclusion
|A U B| = |A|+|B|-|A N B|
write for 3 set A, B, C


