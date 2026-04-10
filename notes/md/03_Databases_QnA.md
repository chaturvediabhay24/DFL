**Databases --- Deep Level**

*Interview Q&A --- Deep Dive*

**ACID & Transactions**

1.  **Explain ACID properties in databases.**

> Atomicity: a transaction is all-or-nothing --- if any part fails, the
> entire transaction is rolled back. Consistency: a transaction brings
> the DB from one valid state to another, respecting all constraints.
> Isolation: concurrent transactions execute as if they were serial ---
> intermediate states are not visible. Durability: once committed, data
> survives crashes (written to disk/WAL). In ML systems: ACID is
> critical for experiment metadata (you don\'t want a partial write
> making a run appear complete) and audit logs for fraud decisions.

2.  **Explain transaction isolation levels and their anomalies.**

> Read Uncommitted: can read dirty data (uncommitted changes from other
> transactions). Dirty Read anomaly. Read Committed (PostgreSQL
> default): only reads committed data. Non-repeatable Read possible ---
> re-reading a row may give different values. Repeatable Read: same row
> read twice gives same result. Phantom Read still possible --- new rows
> from another committed transaction may appear. Serialisable: full
> isolation, no anomalies. Implemented via 2PL or MVCC serialisation
> checks. Higher isolation = more locking overhead. For ML pipelines,
> Read Committed is usually sufficient.

**Indexing & Query Optimisation**

3.  **Explain B-tree indexing. When does an index not help?**

> A B-tree index is a balanced tree structure maintaining sorted keys
> with O(log N) lookup, range scans, and ordered traversal. An index
> does NOT help when: (1) query selects \>10-20% of rows (full scan is
> cheaper). (2) Column has very low cardinality (e.g., boolean --- index
> not selective enough). (3) Query applies a function to the column
> (e.g., WHERE LOWER(email) = \'\...\' --- add a functional index
> instead). (4) Write-heavy tables where index maintenance overhead
> dominates.

4.  **What is a covering index?**

> A covering index includes all columns needed to satisfy a query ---
> the DB can answer the query entirely from the index without touching
> the base table (avoids a \'heap fetch\'). E.g., for SELECT name, score
> FROM models WHERE model_type = \'xgboost\', an index on (model_type,
> name, score) covers the query. Critical for read-heavy ML metadata
> queries.

5.  **How do you use EXPLAIN/EXPLAIN ANALYZE in PostgreSQL?**

> EXPLAIN shows the query plan (Seq Scan, Index Scan, Hash Join, etc.)
> with estimated costs. EXPLAIN ANALYZE actually executes the query and
> shows actual vs estimated rows/time --- reveals row estimation errors
> that cause bad plans. Key things to look for: Seq Scan on large tables
> (missing index), high actual vs estimated row count mismatch (stale
> statistics --- run ANALYZE), and nested loop joins on large result
> sets (should be hash join).

6.  **What are window functions in SQL? Give an example.**

> Window functions compute values over a set of rows related to the
> current row, without collapsing them (unlike GROUP BY). Syntax: func()
> OVER (PARTITION BY \... ORDER BY \...). Examples: ROW_NUMBER() OVER
> (PARTITION BY user_id ORDER BY timestamp DESC) to get the most recent
> event per user. LAG()/LEAD() for time-series comparisons. RANK() for
> leaderboards. In ML: used to compute rolling averages, rank features
> by importance, or assign train/test splits by time partitions.

7.  **What is a CTE and when would you use it over a subquery?**

> A CTE (Common Table Expression, WITH clause) creates a named temporary
> result set within a query. Use CTEs for: readability (breaking complex
> queries into named steps), recursive queries (hierarchical data ---
> org trees, graph traversal), and referencing the same subquery
> multiple times without repeating it. In PostgreSQL, CTEs are
> optimisation fences (pre-9.x) --- the planner cannot push predicates
> into them. From PG 12, WITH \... AS NOT MATERIALIZED hints the planner
> to inline them.

**Normalisation & Schema Design**

8.  **Explain 1NF, 2NF, 3NF and when to denormalise.**

> 1NF: atomic values, no repeating groups, primary key defined. 2NF:
> 1NF + no partial dependency on composite PK (non-key columns depend on
> the whole PK). 3NF: 2NF + no transitive dependencies (non-key columns
> depend only on PK, not on other non-key columns). When to denormalise:
> for read-heavy analytical workloads (data warehouses, ML feature
> stores) where joins are expensive and data is mostly read. Star schema
> (fact + dimension tables) is a common denormalised pattern.

**CAP Theorem & Distributed Databases**

9.  **Explain the CAP theorem.**

> CAP states that a distributed system can guarantee at most 2 of 3:
> Consistency (every read gets the latest write), Availability (every
> request gets a non-error response), Partition Tolerance (system works
> despite network partitions). Since network partitions are inevitable,
> real systems choose CP (consistent + partition-tolerant, e.g., HBase,
> MongoDB in strong mode) or AP (available + eventually consistent,
> e.g., Cassandra, DynamoDB). For ML feature stores: AP with eventual
> consistency is often acceptable; for fraud decision logs, CP is
> required.

10. **What is database sharding and when do you need it?**

> Sharding horizontally partitions data across multiple DB nodes by a
> shard key (e.g., user_id mod N). Each shard holds a subset of rows.
> Benefits: scales writes and storage beyond a single node. Challenges:
> cross-shard queries (expensive), rebalancing when adding nodes, and
> choosing a good shard key (avoid hotspots --- e.g., don\'t shard by
> timestamp). For ML: shard user feature tables by user_id for
> horizontal scale; keep small reference tables (model metadata)
> unsharded.

**Indexing for Vectors & ML**

11. **How does vector indexing work in FAISS vs MongoDB Vector Search?**

> FAISS IVF (Inverted File Index): partitions the vector space into
> Voronoi cells using k-means; at query time, only searches the nearest
> nprobe cells instead of all vectors. HNSW (Hierarchical Navigable
> Small World): a graph where each node links to its approximate nearest
> neighbours at multiple hierarchy levels; provides excellent
> recall/speed tradeoff. MongoDB Atlas Vector Search uses HNSW
> internally and integrates with document filters (hybrid search). FAISS
> is in-memory and requires custom serving; MongoDB handles persistence
> and scaling.
