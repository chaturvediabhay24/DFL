**MLOps --- Production Maturity**

*Interview Q&A --- Deep Dive*

**Deployment Strategies**

1.  **Explain canary deployment, blue-green deployment, and shadow
    deployment for ML models.**

> Blue-Green: maintain two identical production environments; switch
> traffic from blue (current) to green (new) instantly. Rollback =
> switch back. Zero downtime, but doubles infrastructure cost. Canary:
> gradually route a small % of traffic (e.g., 5%) to the new model;
> monitor metrics; increase % if healthy, rollback if not. Minimises
> blast radius. Shadow: new model receives a copy of production traffic
> but responses are discarded --- allows full production-load testing
> with zero user impact. Use shadow before canary for high-risk model
> changes (e.g., replacing a core fraud model). For GenAI: shadow deploy
> to collect evaluation data before any user exposure.

2.  **What is the difference between data drift, concept drift, and
    prediction drift?**

> Data drift (covariate shift): the distribution of input features
> changes (e.g., user demographics shift). Model performance may degrade
> even if the true relationship between features and labels is
> unchanged. Concept drift: the underlying relationship between features
> and labels changes (e.g., fraud patterns evolve). The most dangerous
> --- the model\'s learned patterns become wrong. Prediction drift:
> output distribution changes without a clear cause --- can be an early
> signal of upstream data issues. Detection: statistical tests (KS test
> for continuous features, chi-squared for categorical, PSI ---
> Population Stability Index is standard in banking). Threshold PSI \>
> 0.2 typically triggers investigation.

3.  **How do you design an automated model retraining pipeline?**

> Components: (1) Drift detection service --- monitors PSI/KS stats on
> incoming feature distributions, publishes alerts to Kafka/SQS. (2)
> Trigger logic --- alert + performance threshold breach activates an
> Airflow DAG. (3) Data validation --- Great Expectations checks schema,
> nulls, and distribution before training. (4) Training DAG --- fetches
> recent data, trains with DDP/Ray, tracks with MLflow. (5) Evaluation
> gate --- new model must beat champion on holdout + business metrics.
> (6) Champion/Challenger registry --- promote new model to staging,
> shadow deploy, then promote to production. (7) Rollback trigger ---
> automated rollback if production metrics degrade post-deployment.

**Observability in ML**

4.  **What should you monitor for an ML model in production beyond
    accuracy?**

> Input monitoring: feature distribution drift (PSI per feature), null
> rates, schema violations, cardinality changes in categorical features.
> Prediction monitoring: output distribution drift, prediction
> confidence distribution, class balance in predictions. Performance
> monitoring (if labels available): rolling accuracy/F1/AUC with
> lag-adjusted label joins. Operational monitoring: inference latency
> (p50/p95/p99), throughput (requests/sec), error rates, GPU/CPU
> utilisation, memory usage, queue depth. Business KPIs: CTR, conversion
> rate, fraud caught rate --- the ultimate validation that the model is
> working. Tie model version to business metric dashboards.

5.  **What is model versioning and how do you implement it?**

> Model versioning tracks model artefacts (weights, hyperparameters,
> training data version, code version, evaluation metrics) across
> iterations. Implementation: MLflow Model Registry --- models progress
> through stages (Staging → Production → Archived). Tag models with git
> commit hash, dataset version (via DVC tag), and evaluation results.
> Serve models by alias (\'production\', \'champion\') not by version
> number --- decouples deployment from version tracking. For LLMs:
> version the prompt templates and system prompts alongside the model,
> since prompt changes can alter behaviour as much as weight changes.

**Feature Stores & Reproducibility**

6.  **What is point-in-time correctness in feature stores and why is it
    critical?**

> Point-in-time correctness ensures that when computing training labels
> at time T, features used are the values that were available AT time T
> (not future values). Without it, you have feature leakage --- the
> model sees information it couldn\'t have had in production, inflating
> training metrics and causing production degradation. Example: a
> user\'s 30-day purchase count at the time of the transaction, not
> their 30-day count as of today. Feature stores like Feast implement
> time-travel queries (as_of_time parameter) to retrieve historical
> feature snapshots correctly.

7.  **What is DVC and how does it enable ML reproducibility?**

> DVC (Data Version Control) tracks large data files and model artefacts
> in a content-addressed store (S3, GCS) using small pointer files
> committed to Git. A DVC pipeline defines stages (data → preprocess →
> train → evaluate) with dependencies and outputs; DVC detects which
> stages need re-running based on input hashes. This enables:
> reproducing any historical experiment by checking out a git commit +
> running \'dvc repro\', data lineage tracking, and sharing datasets
> across teams without duplicating large files in Git.

**SLA Design & Reliability**

8.  **How do you design SLAs for an ML inference service?**

> Define SLIs (Service Level Indicators): latency (p99 \< 200ms),
> availability (99.9%), error rate (\<0.1%), throughput (1000 req/s).
> Set SLOs (Objectives) as targets. Error budget = 1 - SLO availability
> (e.g., 43 min/month for 99.9%). Design for the SLO: load test with
> Locust to find breaking points; add horizontal scaling headroom
> (target 60-70% CPU at peak); implement circuit breakers for downstream
> LLM API failures; cache frequent queries. Burn rate alerts: alert when
> error budget is consumed faster than expected (e.g., 14x burn rate =
> budget exhausted in 1 hour).
