# 1.1 Introduction to Python Programming

## 1.1.1 Act of programming

### Why write programs?
- To delegate computational and repetitive tasks to machines.
- Automate time-consuming processes and reduce human error.
- Streamline repeatable workflows and improve consistency.
- Replace manual, mechanical procedures with precise automated steps.
- Requires clear understanding of the task and a deterministic procedure to accomplish it.

### What are we programming?
- We program computers (real machines) to perform desired computations.
- Understanding interactions with hardware and system resources is useful for performance and correctness.

### What is a program?
- A program is a sequence of instructions that communicates computational intent to a machine.
- It specifies the steps needed to compute a result and modify machine state.

### What is a programming language?
- A formal language used to write programs.
- Conveys computational intent to machines and removes ambiguities of natural language.
- Languages range from low-level (close to hardware) to high-level (more abstract).

#### Low-level vs High-level languages
- Low-level:
  - Interact closely with hardware.
  - Provide fine-grained control and efficiency.
- High-level:
  - Provide abstraction and greater developer productivity.
  - Emphasize readability and maintainability.
  - Python is a high-level language.

## 1.1.2 Syntax and semantics
- Syntax: Rules that define correctly structured programs.
- Semantics: The meaning and runtime behavior of syntactically valid code.

### Formal syntax — Backus-Naur Form (BNF)
- Language grammars are often described using BNF.
- Typical processing pipeline: Characters → Tokens → Expressions → Statements → Programs.
- Operational semantics describe how each construct changes program state.

### Python
- Python's syntax defines valid program structure; its semantics describe execution effects.
- Reference: https://docs.python.org/
- CPython is the reference and most widely used implementation.

## 1.1.3 Programming errors
- Syntax errors: Program fails to parse and will not run.
- Runtime errors: Errors that occur during execution (exceptions).
- Semantic (logic) errors: Program runs but produces incorrect results.

## 1.1.4 Core elements of Python

### The Zen of Python
- A set of guiding principles emphasizing readability, simplicity, and explicitness (see `import this`).

### Multi-paradigm nature
- Imperative: Write sequences of commands that change program state.
- Object-oriented: Structure code using classes and objects.
- Functional: Use functions as first-class values and higher-order functions.

### Batteries included
- Rich standard library and ecosystem (for example, NumPy and pandas) enable rapid development.

### Common pitfalls and mitigations
- Performance considerations:
  - Python is generally slower and uses more memory than lower-level compiled languages.
  - Its interpreted and dynamically typed nature affects performance.
- Mitigations:
  - Use optimized libraries (NumPy, pandas) and native extensions for compute-heavy tasks.
  - Consider alternative interpreters (PyPy) or JIT compilers (Numba) for acceleration.
  - Adopt optional typing (typing module) and static analysis to improve maintainability.
  - Optimize algorithms, data structures, and concurrency where appropriate.
  - Profile and apply targeted optimizations; handle errors gracefully.
