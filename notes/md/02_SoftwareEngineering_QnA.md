**Software Engineering Fundamentals**

*Interview Q&A --- Deep Dive*

**SOLID Principles**

1.  **Explain the SOLID principles with examples.**

> S --- Single Responsibility: a class/module should have one reason to
> change. E.g., separate ModelTrainer from ModelSerializer. O ---
> Open/Closed: open for extension, closed for modification. E.g., add
> new model types via subclassing, not editing existing code. L ---
> Liskov Substitution: subclasses must be usable wherever the parent is
> expected without breaking behaviour. I --- Interface Segregation:
> prefer many specific interfaces over one fat interface. E.g., separate
> Trainable and Serialisable interfaces. D --- Dependency Inversion:
> high-level modules depend on abstractions, not concretions. E.g.,
> ModelService depends on IModelStore interface, not a concrete
> PostgreSQLStore.

2.  **What is the difference between composition and inheritance? When
    to use each?**

> Inheritance (\'is-a\'): a subclass inherits implementation from a
> parent. Use when there is a genuine type hierarchy and shared
> behaviour. Risk: tight coupling, fragile base class problem.
> Composition (\'has-a\'): an object holds references to other objects
> and delegates behaviour to them. Preferred in most cases --- it\'s
> more flexible, testable, and avoids deep inheritance trees. Rule of
> thumb: \'Favour composition over inheritance\' (GoF). In ML: a
> Pipeline composes Preprocessor, Trainer, and Evaluator rather than
> inheriting from all of them.

**Design Patterns**

3.  **Explain the Factory and Abstract Factory patterns.**

> Factory Method: defines an interface for creating an object but lets
> subclasses decide which class to instantiate. E.g.,
> ModelFactory.create(\'xgboost\') returns an XGBoostModel;
> .create(\'transformer\') returns a TransformerModel. Abstract Factory:
> creates families of related objects without specifying concrete
> classes. E.g., a CloudFactory could produce AWSStorage + AWSCompute or
> GCPStorage + GCPCompute, ensuring components from the same family are
> used together.

4.  **Explain the Observer pattern. Where is it used in ML systems?**

> Observer: a subject maintains a list of observers and notifies them on
> state changes. E.g., a ModelTrainer (subject) notifies MetricLogger,
> EarlyStopper, and CheckpointSaver (observers) at the end of each
> epoch. In ML frameworks: PyTorch Lightning\'s Callback system, Keras
> callbacks, and MLflow autologging all use the Observer pattern. It
> decouples the training loop from monitoring/logging concerns.

5.  **What is the Strategy pattern? Give an ML example.**

> Strategy defines a family of algorithms, encapsulates each, and makes
> them interchangeable. E.g., an Optimizer strategy: the training loop
> accepts any optimizer (SGD, Adam, AdamW) via a common interface. The
> caller selects the strategy at runtime without changing the training
> loop code. In production ML systems, model inference routing (try LLM
> provider A, fallback to B) follows the Strategy pattern.

6.  **What is the Singleton pattern and its pitfalls?**

> Singleton ensures a class has only one instance (e.g., a DB connection
> pool, a model registry). Pitfall: it\'s global state --- makes testing
> harder (need to reset between tests), creates hidden coupling, and is
> not thread-safe without locks. In Python, module-level variables are
> naturally singletons. Prefer dependency injection over Singletons in
> production code; use them only for stateless shared resources.

**REST API Design**

7.  **What are the principles of RESTful API design?**

> REST principles: (1) Resource-based URLs --- nouns not verbs (/models
> not /getModel). (2) HTTP methods semantics --- GET (read), POST
> (create), PUT (replace), PATCH (partial update), DELETE (remove). (3)
> Statelessness --- server holds no client session; all context in
> request. (4) Idempotency --- GET, PUT, DELETE are idempotent (same
> request = same result); POST is not. (5) Consistent error codes ---
> 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found,
> 422 Unprocessable Entity, 500 Server Error. (6) Versioning ---
> /api/v1/\... for backward compatibility.

8.  **How do you version an API and handle backward compatibility?**

> Strategies: (1) URL versioning: /api/v1/, /api/v2/ --- simplest,
> explicit. (2) Header versioning: Accept: application/vnd.myapi.v2+json
> --- cleaner URLs. (3) Query param: /api/resource?version=2. Backward
> compatibility rules: never remove fields from responses (add, don\'t
> remove), never change field types, deprecate before removing. Use an
> API changelog, set deprecation headers, and communicate sunset dates
> to clients.

9.  **What is idempotency and why does it matter in distributed ML
    systems?**

> An operation is idempotent if calling it multiple times produces the
> same result as calling it once. GET, PUT, DELETE are idempotent; POST
> is not. In distributed ML: network failures can cause duplicate
> retries. An idempotent inference endpoint (keyed by request ID) safely
> handles retries --- the second call is a no-op if the first succeeded.
> For model training jobs, idempotency means re-running a job with the
> same parameters should not create a new experiment or overwrite
> results unexpectedly.

**Caching**

10. **Explain caching strategies: TTL, LRU, write-through, write-back.**

> TTL (Time-To-Live): cached entries expire after a fixed time. Simple,
> safe for frequently-changing data. LRU (Least Recently Used): evicts
> the least recently accessed entry when cache is full --- maximises
> cache utility for access-pattern-driven workloads. Write-through:
> writes go to cache AND DB simultaneously --- strong consistency,
> higher write latency. Write-back (write-behind): writes go to cache
> first, flushed to DB asynchronously --- lower write latency but risk
> of data loss on cache failure. In ML: cache LLM prompt→response pairs
> (TTL-based) and embedding vectors (LRU, since model doesn\'t change).

**Clean Code & Code Review**

11. **What makes code \'clean\'? How do you approach code reviews?**

> Clean code is readable, intention-revealing, and minimal. Principles:
> meaningful names (avoid abbreviations), small functions (one
> responsibility), avoid deep nesting (early returns), no magic numbers
> (use named constants), comments explain \'why\' not \'what\'. In code
> reviews I look for: correctness (edge cases, error handling),
> testability (dependency injection, no hidden state), security (input
> validation, no hardcoded secrets), performance (N+1 queries,
> unnecessary allocations), and adherence to team conventions. I give
> specific, actionable feedback and distinguish blocking issues from
> suggestions.
