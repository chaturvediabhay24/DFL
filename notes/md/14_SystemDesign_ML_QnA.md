**System Design for ML Engineers**

*Interview Q&A --- End-to-End ML System Designs*

**ML System Design Framework**

1.  **How do you approach an ML system design interview?**

> Structured framework: (1) Clarify requirements --- scale (users, QPS),
> latency SLA, accuracy target, offline vs real-time, retraining
> frequency. (2) Define the ML problem --- what to predict, label
> definition, success metrics (offline: AUC, NDCG; online: CTR,
> revenue). (3) Data pipeline --- sources, feature engineering, feature
> store, data quality checks. (4) Model selection --- candidate models,
> training infrastructure, experiment tracking. (5) Serving architecture
> --- online vs batch inference, latency budget, caching strategy. (6)
> Evaluation & iteration --- A/B testing framework, monitoring,
> retraining triggers. Always tie design decisions back to requirements.

**Classic ML System Designs**

2.  **Design YouTube\'s video recommendation system.**

> Two-stage architecture: Candidate Generation (recall) --- matrix
> factorisation or neural collaborative filtering retrieves \~1000
> candidates from millions of videos using user watch history
> embeddings + video embeddings (FAISS ANN index). Ranking --- a
> wide-and-deep or two-tower neural network scores candidates using rich
> features: user demographics, video metadata, watch time, freshness,
> co-watch signals. Feature store serves pre-computed user embeddings
> (updated hourly) and real-time session context. Serving: pre-compute
> and cache candidate lists; run ranking in \<100ms. A/B test new models
> on 1% traffic; promote on CTR + watch time improvement.

3.  **Design a search autocomplete / query suggestion system.**

> Components: (1) Trie or prefix hash map for exact prefix matching of
> popular queries --- served from in-memory Redis. (2) ML ranker ---
> given the prefix, rank candidate completions by: query frequency,
> personalisation (user history), recency, and semantic similarity
> (embedding-based). (3) Personalised suggestions --- user\'s recent
> searches + collaborative filtering. (4) Real-time updates --- new
> trending queries propagate via Kafka to update the trie. (5) Caching
> --- cache completions for top-10K prefixes (80% of traffic). Latency
> target: \<50ms. Fallback: frequency-based suggestions if ML ranker
> times out.

4.  **Design an ML pipeline for real-time credit scoring.**

> Ingestion: Kafka stream of transaction events + credit bureau batch
> data (daily). Feature engineering: real-time features (transaction
> velocity, amount z-score vs user baseline) via Flink streaming;
> historical features (payment history, utilisation ratio) from Redis
> feature store. Model: gradient boosted tree (LightGBM) ---
> interpretable, fast inference, handles tabular data well. SHAP values
> generated per prediction for regulatory explainability. Serving:
> FastAPI on Kubernetes, \<100ms p99 latency SLA. Monitoring: PSI on
> feature distributions, rolling AUC on labelled outcomes (30-day lag),
> Prometheus alerts. Retraining: weekly triggered by drift detection.

**LLM System Designs**

5.  **Design a production RAG system for enterprise document QA.**

> Indexing pipeline (offline): document ingestion (PDF/DOCX parsers) →
> chunking strategy (semantic chunking or fixed-size with overlap) →
> embedding generation (text-embedding-3-large or BGE) → upsert to
> vector DB (Pinecone/MongoDB Atlas) + document metadata to PostgreSQL.
> Query pipeline (online): query → embedding → ANN search (top-k=20) →
> reranking (cross-encoder model for precision) → LLM generation with
> retrieved context. Guardrails: input sanitisation, output faithfulness
> check (does the answer cite retrieved docs?). Evaluation: retrieval
> recall@k, answer faithfulness (RAGAS), and latency budget breakdown.
> Latency target: embedding (50ms) + retrieval (30ms) + LLM (1-3s) =
> \~3s total.

6.  **Design a multi-agent LLM orchestration system.**

> Architecture: Orchestrator agent receives user request, decomposes
> into subtasks, routes to specialist agents. Specialist agents:
> DataQueryAgent (SQL generation + execution), AnalysisAgent
> (statistical analysis + visualisation), SearchAgent (web retrieval),
> CodeAgent (Python execution sandbox). Communication: agents pass
> structured messages (JSON schema) via a shared message bus;
> orchestrator maintains conversation state and handles agent failures.
> Reliability: each agent call has timeout + retry; orchestrator falls
> back to simpler single-agent approach on failure. Observability: trace
> all agent calls with OpenTelemetry (span per agent invocation, token
> counts, latency). Safety: code execution in isolated sandbox
> (Docker/Firecracker), SQL agent uses read-only DB credentials.

**Infrastructure Design**

7.  **Design a model serving platform that supports 10+ models at 10K
    QPS.**

> Components: (1) API Gateway --- routes requests by model_id, handles
> auth, rate limiting, request logging. (2) Model registry --- stores
> model artefacts (S3) with version metadata; serves model configs to
> inference nodes. (3) Inference fleet --- heterogeneous nodes: GPU
> nodes for deep learning models (Triton Inference Server), CPU nodes
> for tree models (lightweight FastAPI containers). K8s HPA scales each
> model\'s deployment independently. (4) Shared feature cache --- Redis
> cluster for hot feature lookups (user embeddings, product metadata).
> (5) Async batch endpoint --- for non-latency-sensitive bulk scoring
> jobs. (6) Monitoring --- per-model latency, throughput, error rate
> dashboards; automated rollback on p99 spike.
