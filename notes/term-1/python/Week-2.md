# 2.1 Expressions, Operators and walrus

## 2.1.1 Expressions and operators
An expression is a combination of values, variables and operators that is evaluated to produce a single resulting value.

Examples:
- Literals: 42, "hello", True
- Variable/attribute access: x, obj.attr
- Calls: f(3)
- Compound: (a + b) * c, x if cond else y

Operator categories
- Arithmetic: +, -, *, /, //, %, **
- Comparison: ==, !=, <, <=, >, >=
- Logical: not, and, or
- Bitwise: &, |, ^, ~, <<, >>
- Assignment: =
- Augmented assignment: +=, -=, *=, ...
- Membership: in, not in
- Identity: is, is not
- Conditional expression (ternary): x if cond else y

Operator overloading
- Many operators behave differently depending on operand types.
  - 1 + 2 -> 3
  - "a" + "b" -> "ab"
  - [1] + [2] -> [1, 2]
- Classes can implement special methods (__add__, __eq__, etc.) to customize operator behavior.

Precedence and associativity
- Operators have a precedence order; use parentheses to avoid ambiguity.
- Common pitfall: unary not has lower precedence than comparison? (see boolean precedence below).

## 2.1.2 Walrus operator (:=)
The walrus operator assigns and returns a value in a single expression.

Examples:
- if (n := len(s)) > 10:
    print(f"long string {n}")
- filtered = [x for x in data if (v := f(x)) is not None]

Notes:
- Useful to avoid repeating expensive calls.
- Use sparingly for readability.

## 2.1.3 Chained assignment, tuple/list unpacking, swapping
- Chained assignment: a = b = 0  # both reference the same object (for mutable objects be careful)
- Unpacking:
  - a, b = 1, 2
  - a, *rest = [1,2,3,4]  # rest = [2,3,4]
- Swapping: a, b = b, a
- Useful in loops: for i, (x, y) in enumerate(pairs): ...

## 2.2.1 Lambda expressions
Syntax: lambda args: expression

- Creates an anonymous function object that evaluates the single expression and returns its value.
- Example: square = lambda x: x * x
- Common use: key functions for sorting, map/filter, short callbacks.
  - sorted(items, key=lambda x: x.attr)

Restrictions:
- Body must be a single expression (no statements).
- For complex logic prefer def.

## 2.2.2 Boolean operator precedence and short-circuiting
Precedence (highest to lowest for boolean ops):
1. not
2. and
3. or

Short-circuit behavior and value rules:
- and: returns first falsy operand, otherwise returns last operand
  - a and b -> a if not a else b
- or: returns first truthy operand, otherwise returns last operand
  - a or b -> a if a else b
- not: returns boolean negation of its operand

Examples:
- None or [] -> []       (None is falsy, [] is falsy -> returns last)
- 0 and "x" -> 0        (0 is falsy -> returned)
- "" or "default" -> "default"
- x = y or default_value  # common idiom for fallback

## Revision — Expressions & Operators (short)
- Expression: evaluates to a value (literals, variables, calls, combinations).
- Operators: categories include arithmetic, comparison, logical, bitwise, assignment, membership, identity.
- Operator overloading: same symbol can do different things for different types; classes can override via special methods.
- Walrus operator (:=): inline assignment inside expressions; good for avoiding repetition.
- Unpacking: a, b = ... ; use *rest for variable-length parts; swap with a, b = b, a.
- Lambda: small anonymous function for single-expression logic; prefer def for complex functions.
- Boolean precedence: not > and > or. Logical ops short-circuit and return operand values (not just True/False).

Quick examples
- if (n := len(items)) > 0: ...
- a, b = b, a
- sorted(arr, key=lambda x: x[1])
- result = value or default_value
