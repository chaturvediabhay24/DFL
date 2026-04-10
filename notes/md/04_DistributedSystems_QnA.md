**Distributed Systems**

*Interview Q&A --- Deep Dive*

**Consistency & Consensus**

1.  **What are the different consistency models in distributed
    systems?**

> Strong consistency: every read reflects the latest write ---
> equivalent to a single-node system. Requires coordination overhead.
> Sequential consistency: operations appear to execute in some global
> sequential order consistent with each process\'s order. Causal
> consistency: causally related operations are seen in order; concurrent
> ops can be seen in any order. Eventual consistency: given no new
> updates, all replicas will converge to the same value --- fastest but
> allows stale reads. In ML: model serving can tolerate eventual
> consistency for embeddings; prediction audit logs need strong
> consistency.

2.  **Explain the Raft consensus algorithm at a conceptual level.**

> Raft elects a leader via randomised election timeouts --- the first
> node to time out becomes candidate, requests votes, wins with
> majority. The leader handles all client writes: it appends the entry
> to its log, replicates to followers, and commits once a majority
> acknowledges. If the leader fails, a new election occurs. Raft
> guarantees that committed entries are never lost. It\'s simpler than
> Paxos and used in etcd (Kubernetes\' store), CockroachDB, and TiKV.

3.  **What is distributed locking and how do you implement it?**

> Distributed locking prevents concurrent modifications across nodes.
> Implementation options: (1) Redis SETNX (SET if Not eXists) with TTL
> --- fast, but requires Redlock algorithm for correctness across Redis
> replicas. (2) ZooKeeper ephemeral sequential nodes --- nodes compete
> for a path; smallest sequence number wins. (3) Database-level advisory
> locks (PostgreSQL pg_advisory_lock). In ML: use distributed locks to
> prevent concurrent model deployments overwriting each other.

**Message Delivery & Kafka Internals**

4.  **Explain Kafka\'s message delivery guarantees.**

> At-most-once: producer fires and forgets (acks=0); consumer
> auto-commits before processing. Messages may be lost but never
> duplicated. At-least-once: producer retries on failure (acks=all);
> consumer commits after processing. Messages may be duplicated on
> retry. Exactly-once: producer uses idempotent writes
> (enable.idempotence=true) + transactions; consumer uses transactional
> consumers. Most expensive but critical for financial event processing.
> For ML inference logging, at-least-once is usually acceptable with
> idempotent consumers.

5.  **Explain Kafka partitions, consumer groups, and offset
    management.**

> Partitions: a topic is split into N ordered, immutable log partitions.
> Producers route messages by key hash (deterministic partitioning) or
> round-robin. Consumer Groups: each partition is consumed by exactly
> one consumer in a group, enabling parallel processing --- add
> consumers to scale. Offset: each message has a sequential offset;
> consumers commit their position. Rebalancing occurs when consumers
> join/leave. For ML: partition by user_id to ensure ordered per-user
> events land on the same consumer; scale consumers = partitions.

6.  **What is backpressure and how do you handle it in ML pipelines?**

> Backpressure occurs when a downstream consumer can\'t keep up with
> upstream producer throughput, causing memory bloat or message loss.
> Handling strategies: (1) Bounded queues --- reject/block producers
> when queue is full, propagating pressure upstream. (2) Kafka consumer
> lag monitoring --- alert when lag grows, scale consumers horizontally.
> (3) Batch inference --- accumulate N requests before processing to
> amortise model loading overhead. (4) Circuit breaker --- shed load
> gracefully by returning cached/default responses when the system is
> overwhelmed.

**Distributed Transactions**

7.  **What is the two-phase commit (2PC) protocol and its limitations?**

> 2PC coordinates distributed transactions across multiple nodes: Phase
> 1 (Prepare) --- coordinator asks all participants if they can commit;
> each responds yes/no and durably logs the decision. Phase 2
> (Commit/Rollback) --- coordinator sends final decision; participants
> execute. Limitations: (1) Blocking --- if the coordinator fails after
> Phase 1, participants are locked waiting indefinitely. (2) Not
> partition-tolerant --- one unreachable participant blocks the whole
> transaction. Alternative: the Saga pattern.

8.  **What is the Saga pattern?**

> Saga breaks a distributed transaction into a sequence of local
> transactions, each publishing an event. If a step fails, compensating
> transactions undo previous steps. Two types: Choreography --- services
> react to events directly (no central coordinator, harder to track).
> Orchestration --- a saga orchestrator commands each step and handles
> compensation. In ML pipelines: a model deployment saga might involve
> steps: validate model → update registry → swap traffic → monitor. If
> monitoring fails, compensating steps roll back traffic and registry.

**Idempotency & Reliability**

9.  **How do you design idempotent services in a microservices
    architecture?**

> Include an idempotency key (client-generated UUID) in each request.
> The server stores processed keys with their results (in Redis or DB
> with TTL). On receiving a request: check if key already processed ---
> if yes, return cached result; if no, process and store. This makes
> retries safe. For ML inference: the idempotency key could be a hash of
> (model_version, input_features) --- identical requests return cached
> predictions without re-running the model.
