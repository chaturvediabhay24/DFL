**Python --- Language Internals & Best Practices**

*Interview Q&A --- Deep Dive*

**GIL, Memory & Runtime**

1.  **What is the GIL in CPython and why does it exist?**

> The Global Interpreter Lock (GIL) is a mutex in CPython that allows
> only one thread to execute Python bytecode at a time. It exists
> because CPython\'s memory management (reference counting) is not
> thread-safe --- without the GIL, two threads could simultaneously
> modify the reference count of an object, causing memory corruption.
> The GIL simplifies CPython\'s implementation significantly. The
> downside: CPU-bound multi-threaded programs cannot truly run in
> parallel in CPython.

2.  **How do you work around the GIL for CPU-bound tasks?**

> Options: (1) multiprocessing --- spawns separate OS processes each
> with their own Python interpreter and GIL, true parallelism. (2) Use C
> extensions that release the GIL (NumPy, pandas, PyTorch all release
> the GIL during heavy computation). (3) Use PyPy which has a different
> GIL implementation, or GraalPy. (4) In Python 3.13+, there is an
> experimental no-GIL build (PEP 703) being trialled. For IO-bound work,
> asyncio or threading is sufficient since the GIL is released during IO
> waits.

3.  **How does Python\'s garbage collection work? What is reference
    counting vs cyclic GC?**

> Python uses two mechanisms: (1) Reference counting --- every object
> has a refcount; when it drops to zero the object is immediately
> deallocated. Fast and deterministic but cannot handle reference cycles
> (A→B→A). (2) Cyclic garbage collector --- a generational GC (3
> generations) that periodically detects and collects reference cycles.
> Objects that survive GC cycles are promoted to older generations
> checked less frequently. The gc module allows manual control:
> gc.collect(), gc.disable(). Avoid cycles in performance-critical code
> to minimise GC pressure.

4.  **Explain Python\'s memory model --- how are objects stored?**

> All Python objects live on the heap. Variables are references
> (pointers) to objects, not the objects themselves. CPython uses a
> private memory allocator (pymalloc) for objects ≤512 bytes, grouping
> allocations into arenas/pools for efficiency. Immutable objects
> (integers -5 to 256, short strings) are interned --- the same object
> is reused across references. This is why \'a is b\' can be True for
> small integers but not for larger ones.

5.  **What is the difference between \'is\' and \'==\' in Python?**

> \'==\' checks value equality (calls \_\_eq\_\_). \'is\' checks
> identity --- whether two variables point to the exact same object in
> memory (same id()). Due to interning, \'a is b\' may be True for small
> integers or interned strings even when they were assigned separately.
> Never use \'is\' to compare values; always use \'==\' except when
> explicitly checking for None (e.g., \'x is None\' is idiomatic and
> faster).

**Decorators, Context Managers & Metaclasses**

6.  **How do decorators work internally in Python?**

> A decorator is a callable that takes a function as input and returns a
> new callable. \'@decorator\' above a function definition is syntactic
> sugar for \'func = decorator(func)\'. They work because functions are
> first-class objects. A typical decorator wraps the original function
> using functools.wraps (to preserve \_\_name\_\_, \_\_doc\_\_) and adds
> behaviour before/after the call. Decorators can be stacked (applied
> bottom-up) and can accept arguments by adding an extra layer of
> nesting (a decorator factory returning the actual decorator).

7.  **What is a context manager and how do you implement one?**

> A context manager defines setup/teardown logic for a \'with\' block.
> Implement via: (1) Class-based: define \_\_enter\_\_ (setup, returns
> value bound to \'as\') and \_\_exit\_\_ (teardown, receives exception
> info; return True to suppress exceptions). (2) Generator-based using
> \@contextlib.contextmanager: yield inside a try/finally --- code
> before yield is \_\_enter\_\_, after yield is \_\_exit\_\_. Used for
> resource management (file handles, DB connections, locks, timing).

8.  **What is a metaclass in Python?**

> A metaclass is the class of a class --- it controls how classes are
> created. \'type\' is the default metaclass. Custom metaclasses inherit
> from \'type\' and override \_\_new\_\_ or \_\_init\_\_ to intercept
> class creation. Use cases: enforcing interface contracts (e.g., all
> subclasses must implement a method), automatic registration of
> subclasses, ORM field discovery (Django models), and adding
> class-level validation. Syntax: class MyClass(metaclass=MyMeta). In
> modern Python, \_\_init_subclass\_\_ and class decorators often
> replace metaclasses for simpler use cases.

9.  **What are descriptors in Python?**

> A descriptor is an object that defines \_\_get\_\_, \_\_set\_\_,
> and/or \_\_delete\_\_ methods, controlling attribute access on the
> class that owns it. Non-data descriptors define only \_\_get\_\_
> (e.g., functions --- this is how method binding works). Data
> descriptors define \_\_get\_\_ and \_\_set\_\_ (e.g., property,
> classmethod, staticmethod). When you access instance.attr, Python\'s
> attribute lookup calls the descriptor\'s \_\_get\_\_ if one is found
> in the class\'s MRO. This powers \@property, ORM fields, and
> validation attributes.

**Async, Generators & Functional**

10. **Explain Python\'s async/await and the event loop.**

> async/await implements cooperative concurrency via coroutines. \'async
> def\' defines a coroutine function; \'await\' suspends it, yielding
> control back to the event loop which can run other coroutines.
> asyncio\'s event loop is single-threaded --- it uses a selector
> (epoll/kqueue) to monitor IO readiness and resumes the appropriate
> coroutine when data is available. This is ideal for IO-bound
> concurrency (HTTP requests, DB queries) with thousands of concurrent
> connections without OS thread overhead. It does NOT help CPU-bound
> tasks.

11. **What is the difference between a generator and a coroutine?**

> Generators (yield) produce values lazily --- they are pulled by the
> caller via next(). Coroutines (async def / await) are driven by an
> event loop and designed for concurrency --- they pause at await points
> waiting for IO, not producing values for the caller. Technically,
> coroutines are built on top of generators in CPython (both use the
> frame suspension mechanism), but they have different semantics:
> generators are for iteration, coroutines are for concurrency.

12. **What is asyncio.gather vs asyncio.create_task?**

> asyncio.gather(\*coros) schedules multiple coroutines concurrently and
> waits for all to complete, returning results in order.
> asyncio.create_task(coro) schedules a coroutine as a Task immediately
> (runs in background) and returns a Task object you can await later.
> Key difference: create_task starts execution immediately even if you
> don\'t await it; gather is cleaner for fan-out/fan-in patterns. For
> ML: use gather to fire parallel LLM API requests concurrently.

13. **Explain itertools and give practical ML use cases.**

> itertools provides memory-efficient iterator building blocks. ML use
> cases: itertools.chain --- combine multiple dataset iterators without
> loading all into memory. itertools.islice --- take the first N batches
> from an infinite data generator. itertools.product --- grid search
> parameter combinations. itertools.groupby --- group sorted data by a
> key (e.g., group evaluation results by category). These avoid
> materialising large lists, critical for large-scale data pipelines.

**Type System & Code Quality**

14. **What are Python type hints and how does Pydantic use them?**

> Type hints (PEP 484) annotate variable and function types for static
> analysis tools (mypy, pyright) and documentation. They are not
> enforced at runtime by default. Pydantic uses type hints to build
> runtime-validated data models: when you instantiate a Pydantic
> BaseModel, it coerces and validates input data against the declared
> types, raising ValidationError on failure. This is invaluable for
> FastAPI request/response validation and LLM structured output parsing.

15. **What is the difference between \@dataclass, NamedTuple, and
    Pydantic BaseModel?**

> \@dataclass (stdlib): auto-generates \_\_init\_\_, \_\_repr\_\_,
> \_\_eq\_\_ from type-annotated fields. Mutable by default, no runtime
> validation. NamedTuple: immutable, tuple subclass with named fields,
> memory-efficient, supports unpacking. Pydantic BaseModel: full runtime
> validation/coercion, JSON serialisation, schema generation (used by
> FastAPI). Choose dataclass for simple data containers, NamedTuple for
> immutable records, Pydantic when you need validation or API contracts.

**Profiling & Debugging**

16. **How do you profile a slow Python program?**

> Workflow: (1) cProfile for function-level profiling --- \'python -m
> cProfile -s cumtime script.py\' shows cumulative time per function.
> (2) line_profiler (@profile decorator) for line-by-line timing of hot
> functions. (3) memory_profiler for memory usage per line. (4) py-spy
> for sampling profiler with zero overhead on production processes
> (attaches to a running PID). (5) For async code, use pyinstrument
> which understands coroutine call stacks. Always profile before
> optimising --- never guess the bottleneck.

17. **What tools do you use for debugging in Python?**

> pdb (stdlib): breakpoint() drops into interactive debugger. Commands:
> n (next), s (step into), c (continue), p (print), l (list code), bt
> (backtrace). ipdb: enhanced pdb with IPython REPL. VSCode/PyCharm
> debuggers: visual breakpoints, watch expressions, conditional
> breakpoints --- preferred for complex codebases. For ML: use
> torch.autograd.set_detect_anomaly(True) for NaN/Inf gradient debugging
> in PyTorch. For production: Sentry for exception tracking with stack
> traces.

**Packaging & Environment**

18. **Explain Python virtual environments and dependency management.**

> Virtual environments (venv, conda) isolate project dependencies to
> avoid version conflicts between projects. pip + requirements.txt is
> the baseline; limitations: no lock file by default, no dependency
> resolution. Poetry adds: pyproject.toml for metadata, poetry.lock for
> reproducible installs, virtual env management, and publish tooling.
> pip-tools (pip-compile) generates pinned requirements.txt from
> high-level requirements.in. For ML projects, conda is common for
> managing non-Python dependencies (CUDA libraries, C extensions).
