**Interview Preparation Guide**

Abhay Chaturvedi --- AI/ML Engineer

*Comprehensive Q&A --- All Topics*

**1. Introduction & Background**

1.  **Tell me about yourself.**

> I\'m Abhay Chaturvedi, an AI/ML Engineer currently at Pegasystems in
> Bengaluru. I hold an M.S. in Data Science from IIIT Hyderabad and a
> B.Tech in Computer Science from IIIT Gwalior. Over the past \~5 years
> I\'ve worked across the full ML lifecycle --- from building fraud
> detection systems at UnitedHealth Group, to deploying personalised
> recommendation engines at ShareChat, to building no-code ML platforms
> at AwoneAI, and now leading GenAI and LLM infrastructure work at
> Pegasystems.

2.  **Why did you choose Data Science / AI-ML as your career?**

> My B.Tech in CS gave me a strong algorithms foundation, and I became
> fascinated by how statistical learning could automate pattern
> recognition at scale. During my UnitedHealth internship I saw
> first-hand how an ML model could cut false-positive fraud alerts by
> 15% weekly --- that real-world impact solidified my direction. The
> rapid evolution of LLMs and GenAI has only deepened my interest.

3.  **Walk me through your career progression.**

> I started as a Data Science intern at UnitedHealth Group (2020),
> deploying Triton Inference Server configs. I then interned at
> ShareChat building a Neural Collaborative Filtering recommendation
> engine (2021). After graduating I joined UnitedHealth as full-time
> Data Scientist, containerising fraud detection on AWS EKS. I then
> moved to AwoneAI as a Data Scientist (2022--2024) building a no-code
> ML platform powered by the Ray framework. Since July 2024 I\'ve been
> an AI/ML Engineer at Pegasystems, leading GenAI assistant
> infrastructure, LLM deployment, and evaluation frameworks.

4.  **What is your greatest professional achievement?**

> At Pegasystems, deploying the Chat With Your Data AI Agent that serves
> 50+ enterprise clients and 400+ internal users --- driving a 4X
> increase in daily query volume --- is my proudest achievement because
> it directly empowered non-technical users with data self-service at
> scale.

**2. Generative AI & LLMs**

5.  **Explain your experience with LLMs. Which models have you worked
    with?**

> I have production experience with OpenAI GPT models, Anthropic Claude
> (via API), Google Vertex models, and open-source GPT-OSS 20B and 120B
> models. I\'ve integrated these into a unified Generative AI Assistant
> Service at Pegasystems, and deployed open-source LLMs using vLLM with
> FlashAttention on A100 GPUs.

6.  **What is vLLM and why did you use it over other inference
    engines?**

> vLLM is an LLM serving library that implements PagedAttention --- a
> memory management technique inspired by OS virtual memory --- to
> efficiently manage the KV cache. It achieves high throughput by
> batching requests dynamically. I chose it for GPT-OSS 120B because it
> delivered 5x faster inference and 50% lower memory overhead compared
> to naive HuggingFace serving, especially for large-context workloads.
>
> [▶ Paged Attention Explained](https://www.youtube.com/watch?v=6uPnLkCiy5g) 
> GPU memory fragmentation and KV Cache Waste are two issues.
> paged attention solve by dividing into fixed size blocks and blocks gets dynamicaly replaced once completed. no bottleneck for waiting for batch and the request is not allocated sequentially but the dynamicaally in batches to occu[py whole memory and replace non working blocks].

7.  **What is FlashAttention and how does it improve LLM inference?**

> FlashAttention rewrites the attention computation to be IO-aware:
> instead of materialising the full N×N attention matrix in GPU HBM, it
> tiles the computation in SRAM (which is much faster), reducing memory
> reads/writes from O(N²) to O(N). This makes inference faster and
> allows handling longer context windows within the same GPU memory
> budget.

8.  **Explain your Generative AI Assistant Service architecture at
    Pegasystems.**

> The service provides a unified interface over multiple LLM providers
> (OpenAI, Anthropic, Vertex). It includes a routing layer that selects
> the best model per request type, a caching layer for repeated queries,
> and async parallel API calls that reduced overall latency by 70%.
> Resource consumption was cut 20% through batching and request
> deduplication.

9.  **What is RAG (Retrieval-Augmented Generation) and how have you used
    it?**

> RAG grounds LLM responses in external documents by: (1) encoding
> documents into vector embeddings stored in a vector DB (e.g., FAISS or
> MongoDB Vector), (2) at query time, retrieving the top-k semantically
> similar chunks, and (3) injecting them into the LLM prompt as context.
> I used RAG in the \'Chat With Your Data\' agent so users could query
> proprietary datasets without fine-tuning the model.

10. **What vector databases have you worked with and how do they
    differ?**

> I\'ve used FAISS (Facebook AI Similarity Search) and MongoDB Vector
> Search. FAISS is a highly optimised in-memory library ideal for
> offline or single-node high-speed similarity search; it supports IVF
> and HNSW indexing. MongoDB Vector Search integrates vector indices
> alongside document storage, making it convenient when data already
> lives in MongoDB and you need hybrid (keyword + semantic) retrieval
> without a separate infrastructure component.

11. **How does LangChain help in building LLM applications?**

> LangChain provides abstractions for chains (sequential LLM calls),
> agents (LLM + tool use), memory (conversation history), and document
> loaders/splitters for RAG pipelines. It significantly reduces
> boilerplate. For example, building a RAG pipeline that was 200+ lines
> of raw API code reduces to \~30 lines with LangChain\'s RetrievalQA
> chain.

12. **What is your AI Evaluation Framework and how does LLM-as-a-judge
    work?**

> The framework automates quality assessment of agent outputs.
> \'LLM-as-a-judge\' uses a powerful LLM (e.g., GPT-4) as an evaluator
> that scores or ranks candidate outputs against a reference answer on
> criteria like faithfulness, relevance, and coherence. Pairwise
> comparison presents two outputs and asks the judge which is better.
> This reduced per-evaluation time by 30 minutes compared to manual
> review.

13. **What are the limitations of LLM-as-a-judge?**

> Key limitations include: positional bias (judges favour the first
> option presented), verbosity bias (longer answers rated higher
> regardless of quality), self-enhancement bias (a model rates its own
> outputs higher), and inconsistency across runs. Mitigation strategies
> include randomising order, calibrating with human labels, and using
> ensemble judging.

14. **What is prompt engineering? What techniques do you apply?**

> Prompt engineering shapes LLM behaviour through input design.
> Techniques I use: (1) Few-shot examples to steer format and style, (2)
> Chain-of-thought (CoT) prompting for reasoning tasks, (3) System
> prompt constraints to restrict scope, (4) Structured output
> instructions (e.g., \'respond only in JSON\'), (5) Role prompting
> (\'You are an expert data analyst\'), and (6) Iterative refinement
> with temperature tuning.

15. **How did you build the AI Tracer for agent orchestration?**

> The tracer instruments each agent node to capture wall-clock time,
> token counts per call, tool invocations, and intermediate outputs. It
> uses structured logging exported to a time-series store (with
> Prometheus/Grafana dashboards). By making token consumption and
> latency visible per step, it achieved a 50% improvement in agent
> performance tracking efficiency.

**3. Machine Learning & Deep Learning**

16. **Explain Neural Collaborative Filtering (NCF) and your ShareChat
    implementation.**

> NCF replaces the inner product of matrix factorisation with a
> multi-layer perceptron to learn non-linear user-item interactions. At
> ShareChat I implemented it with PyTorch: user and item embeddings fed
> into MLP layers producing a click probability score. The model was
> trained on implicit feedback (clicks) and improved CVR by 1.9% ---
> significant at ShareChat\'s scale.

17. **What is the difference between collaborative filtering and
    content-based filtering?**

> Collaborative filtering (CF) recommends items based on patterns across
> many users (user-item interaction matrix) without needing item
> features. Content-based filtering recommends items similar to ones a
> user liked based on item attributes. CF suffers from cold-start for
> new users/items; content-based requires rich item metadata. Hybrid
> systems combine both.

18. **What is XGBoost and when would you use it over a neural network?**

> XGBoost is a gradient boosted decision tree ensemble that uses
> second-order gradients, regularisation (L1/L2), and approximate tree
> learning for speed. I prefer it over NNs for structured/tabular data
> where: training data is limited (\<100K rows), interpretability is
> needed (SHAP values integrate natively), training speed matters, or
> there\'s no strong benefit from feature representation learning.

19. **Explain UNet and its use cases.**

> UNet is an encoder-decoder CNN architecture with skip connections
> between encoder and decoder at each resolution level. Originally
> designed for biomedical image segmentation, it preserves fine-grained
> spatial information via the skip connections. Beyond medical imaging,
> it\'s used for satellite image segmentation, depth estimation, and
> image-to-image translation.

20. **What are Vision Transformers (ViT) and how do they differ from
    CNNs?**

> ViT splits an image into fixed-size patches, linearly embeds each
> patch, adds positional encodings, and feeds the sequence into a
> standard Transformer encoder. Unlike CNNs, ViT has no inductive bias
> for locality or translation equivariance --- it learns spatial
> relationships purely from data (requiring more data or pre-training).
> ViTs excel on large datasets and transfer well to downstream tasks.

21. **What is Representation Learning? How is it relevant to your
    work?**

> Representation Learning focuses on learning dense, meaningful feature
> vectors from raw data. In my work it underpins: user/item embeddings
> in NCF, text embeddings in RAG pipelines, and contrastive learning for
> tabular data in the CiBi platform. Good representations enable
> downstream tasks (classification, retrieval) to train faster with less
> labelled data.

22. **Explain Reinforcement Learning and any exposure you have to it.**

> RL trains an agent to maximise cumulative reward through environment
> interactions (state → action → reward cycle). My exposure includes
> RLHF concepts used in LLM fine-tuning, where a reward model trained on
> human preferences guides the policy (LLM) via PPO. I\'ve also studied
> Q-learning and policy gradient methods academically.

23. **What is Explainable AI? Explain SHAP and LIME.**

> SHAP (SHapley Additive exPlanations) uses game-theory Shapley values
> to fairly attribute each feature\'s marginal contribution to a
> prediction, guaranteeing consistency and local accuracy. LIME (Local
> Interpretable Model-agnostic Explanations) fits a simple linear model
> in the local neighbourhood of a prediction. SHAP is preferred for tree
> models due to TreeSHAP\'s O(TLD²) efficiency; LIME is model-agnostic
> but less stable.

24. **What is Distributed Data Parallel (DDP) and how did you use it at
    AwoneAI?**

> DDP (PyTorch) replicates the model on each GPU, performs
> forward/backward passes in parallel on data shards, then uses an
> all-reduce operation (ring-reduce) to synchronise gradients. At
> AwoneAI I integrated DDP into the CiBi no-code platform\'s training
> backend, reducing training time by 60% and improving model accuracy by
> 12% through better convergence on larger effective batch sizes.

25. **How did you fine-tune models for enterprise clients at AwoneAI?**

> I used transfer learning: starting from pre-trained checkpoints and
> fine-tuning on client-specific datasets (sales forecasting, ops
> workflows). The workflow included: data profiling, feature
> engineering, hyperparameter search with MLflow tracking, and automated
> deployment. This improved forecast accuracy by 15--20% over baseline
> models.

26. **What is MLflow and how do you use it for experiment tracking?**

> MLflow tracks ML experiments by logging parameters, metrics, artefacts
> (models, plots), and environment metadata per run. I use it to compare
> model versions, reproduce results, and promote champion models to the
> model registry. In AwoneAI\'s Ray-based pipeline it auto-logged each
> trial\'s hyperparameters and validation metrics, enabling no-code
> experiment comparison.

**4. MLOps & Infrastructure**

27. **Describe your experience with Kubernetes and Docker.**

> At UnitedHealth I containerised the fraud detection model with Docker
> and orchestrated it on AWS EKS (Kubernetes). I wrote Dockerfiles for
> reproducible inference environments, Kubernetes Deployment and Service
> manifests, Horizontal Pod Autoscalers for load-based scaling, and
> ConfigMaps/Secrets for configuration management. This achieved 80%
> latency reduction via auto-scaling.

28. **What is AWS EKS and how does it differ from self-managed
    Kubernetes?**

> EKS is Amazon\'s managed Kubernetes control plane --- AWS handles
> control plane availability, upgrades, and etcd backups. Compared to
> self-managed Kubernetes (e.g., kubeadm on EC2), EKS reduces
> operational overhead significantly. I used EKS with managed node
> groups for automatic worker node provisioning and IAM roles for
> service accounts (IRSA) for fine-grained pod-level AWS permissions.

29. **Explain CI/CD in the ML context and your Jenkins experience.**

> In ML, CI/CD automates: code linting, unit tests for data pipelines,
> model training on new data, evaluation against baseline, and
> deployment if quality gates pass. I used Jenkins pipelines (Groovy
> DSL) to trigger on Git commits: build Docker images, run pytest
> suites, execute model training in a staging cluster, compare metrics,
> and push to EKS on success. This removed manual deployment steps and
> reduced error risk.

30. **What is Apache Kafka and in what context have you used it?**

> Kafka is a distributed log-based message streaming platform providing
> high-throughput, durable pub-sub messaging. In ML pipelines it enables
> real-time feature streaming (e.g., user events → feature store) and
> decouples producers from consumers. I\'ve used Kafka to stream
> inference requests to model servers and feed prediction logs back to
> monitoring systems.

31. **What is Apache Airflow and how does it fit in an ML pipeline?**

> Airflow is a workflow orchestration tool where pipelines are defined
> as DAGs (Directed Acyclic Graphs) of tasks in Python. In ML it
> orchestrates: data ingestion, preprocessing, training, evaluation, and
> deployment steps with scheduling, retries, and alerting. I used it at
> AwoneAI to schedule nightly retraining jobs and trigger downstream
> deployment DAGs on metric improvement.

32. **What is NVIDIA Triton Inference Server and how did you optimise
    it?**

> Triton is a production inference serving platform supporting multiple
> frameworks (TensorFlow, PyTorch, TensorRT, ONNX). At UnitedHealth I
> tuned Triton\'s dynamic batching (max_queue_delay_microseconds,
> preferred_batch_size), instance group concurrency, and TensorRT
> optimised model plans. This improved inference latency by 35% and
> pushed GPU utilisation to 100%.

33. **What is TensorRT and how does it optimise models?**

> TensorRT is NVIDIA\'s deep learning inference optimiser. It takes a
> trained model and applies: layer fusion (merging conv+BN+ReLU into one
> op), precision calibration (FP32→FP16/INT8), kernel auto-tuning, and
> memory optimisation. The result is a serialised engine binary with
> significantly lower latency and higher throughput than the original
> framework.

34. **What is Prometheus and Grafana and how did you use them?**

> Prometheus is a time-series metrics scraping and storage system;
> Grafana is a visualisation dashboard. In my AI Tracer, I exported
> token counts and latency histograms as Prometheus metrics via a
> /metrics endpoint, then built Grafana dashboards showing p50/p95/p99
> latency per agent, token budget consumption, and error rates ---
> enabling real-time performance monitoring.

35. **Explain the Ray framework and how you automated ML workflows with
    it.**

> Ray is a distributed computing framework with high-level libraries:
> Ray Train (distributed training), Ray Tune (hyperparameter search),
> Ray Serve (model serving), and Ray Data (scalable data processing). At
> AwoneAI I used Ray\'s DAG API to wire dataset ingestion →
> preprocessing → training → evaluation → deployment into a fully
> automated no-code pipeline, reducing manual setup by 80% and
> accelerating model iteration 3x.

36. **What is PySpark and when would you use it over pandas?**

> PySpark is the Python API for Apache Spark, enabling distributed
> in-memory data processing across a cluster. I use PySpark when: data
> exceeds single-node RAM (GBs--TBs), transformations are
> parallelisable, or I need Spark SQL for structured data at scale.
> Pandas is preferred for data that fits in memory (\<a few GB) due to
> its simpler API and faster local iteration.

37. **What is A/B Testing and how is it applied in ML?**

> A/B testing randomly splits users into control (model A) and treatment
> (model B) groups and measures metric differences with statistical
> significance testing (t-test, z-test). In ML it validates that a new
> model genuinely improves business KPIs (e.g., CTR, revenue) vs. the
> current production model. Key considerations: sufficient sample size
> (power analysis), avoiding novelty effects, and monitoring for metric
> interference.

38. **What is Locust.io and how did you use it?**

> Locust is a Python-based load testing tool that simulates concurrent
> users hitting an API. I used it to stress-test ML inference endpoints
> --- ramping up to thousands of concurrent requests to measure
> throughput, latency degradation, and error rates under load. This
> informed Kubernetes HPA thresholds and Triton batching configurations.

**5. Data Engineering & Databases**

39. **Explain your experience with PostgreSQL and MongoDB.**

> PostgreSQL (relational): I use it for structured feature stores,
> experiment metadata, and audit logging --- leveraging JOINs, window
> functions, and JSONB for semi-structured data. MongoDB (document): I
> use it for storing unstructured inference logs, RAG document chunks,
> and vector embeddings (MongoDB Vector Search), where schema
> flexibility and horizontal shaling outweigh relational needs.

40. **When would you choose SQL over NoSQL?**

> Choose SQL when: data is highly structured and relational, ACID
> transactions are critical (payments, healthcare records), or complex
> multi-table queries are common. Choose NoSQL when: schema evolves
> rapidly, horizontal scalability is needed, or data is
> document/graph/time-series-natured (e.g., JSON events, social graphs,
> IoT streams).

41. **What is a Feature Store and why is it important in ML systems?**

> A feature store is a centralised repository for computing, storing,
> and serving ML features. It solves training-serving skew (ensuring
> training and inference use identical feature logic), enables feature
> reuse across teams, and provides point-in-time correctness for
> time-series features. Examples: Feast, Tecton, Hopsworks.

**6. Project Deep Dives**

**Fraud Detection --- UnitedHealth Group**

42. **How did you architect the fraud detection system on AWS EKS?**

> The architecture: (1) Kafka stream ingests transaction events, (2) a
> FastAPI inference service (containerised with Docker) runs the XGBoost
> fraud model, (3) deployed on AWS EKS with Horizontal Pod Autoscaler
> based on CPU/memory, (4) predictions stored to PostgreSQL for audit,
> (5) Jenkins CI/CD pipeline rebuilds and redeploys on model updates.
> This achieved 80% latency reduction vs. the batch predecessor.

43. **How did you reduce false positive alerts by 15%?**

> By iterating on the decision threshold using precision-recall curves
> calibrated on domain-specific cost matrices (cost of false positive \>
> cost of false negative for the client\'s ops team). I also added
> feature engineering --- rolling aggregates (transaction velocity,
> merchant category frequency) --- and used SHAP to identify and remove
> noisy features that increased false positives.

**Chat With Your Data Agent --- Pegasystems**

44. **How does the \'Chat With Your Data\' agent work end-to-end?**

> Users type natural language queries. The agent: (1) classifies intent,
> (2) retrieves relevant data schema and sample rows from a vector DB,
> (3) generates SQL or API calls via the LLM, (4) executes the query,
> (5) formats the result with an LLM-generated natural language summary.
> Guardrails prevent unsafe SQL (DROP, DELETE). This served 50+ clients
> with a 4X increase in daily query volume.

45. **How did you ensure the agent\'s SQL generation is safe and
    accurate?**

> Safety: schema-only context (no raw PII in prompts), allowlisted SQL
> operations (SELECT only), and post-generation regex validation
> rejecting DDL/DML statements. Accuracy: few-shot prompting with schema
> examples, chain-of-thought for complex joins, and a retry loop that
> re-prompts with the SQL error message if execution fails.

**CiBi No-Code ML Platform --- AwoneAI**

46. **What technical challenges did you face integrating Tabular, CV,
    NLP, and GenAI into one platform?**

> Key challenges: (1) Unified data ingestion --- different modalities
> need different loaders/preprocessors, solved with a plugin
> architecture. (2) Framework heterogeneity --- tabular uses
> sklearn/XGBoost, CV uses PyTorch, NLP uses HuggingFace; solved with a
> common Trainer interface abstracting each. (3) DDP compatibility ---
> not all libraries natively support it; I wrapped non-DDP models in
> custom launchers. (4) Experiment tracking consistency --- unified
> MLflow schema across modalities.

**7. NLP & Computer Vision**

47. **Explain the Transformer architecture.**

> Transformers use self-attention: each token attends to all other
> tokens via Query-Key-Value projections (QKV). Multi-head attention
> learns different relationship types in parallel. Positional encodings
> inject order information. Encoder-only (BERT): bidirectional context
> for classification/NER. Decoder-only (GPT): causal/autoregressive for
> generation. Encoder-decoder (T5, BART): seq2seq for
> translation/summarisation.

48. **What are word embeddings? How do Word2Vec and modern embeddings
    differ?**

> Word2Vec produces static embeddings --- one vector per word regardless
> of context --- using CBOW or Skip-gram. Modern embeddings (from BERT,
> sentence-transformers) are contextual: the same word has different
> vectors depending on surrounding tokens. Sentence-transformers produce
> single sentence-level embeddings via mean pooling, ideal for semantic
> similarity and RAG retrieval.

49. **What is fine-tuning vs. prompt engineering vs. RAG? When to use
    each?**

> Prompt engineering (zero/few-shot): fastest, cheapest, no training;
> works when the base model already has the knowledge. RAG: adds
> external knowledge at inference without training; best for
> proprietary/frequently-updated data. Fine-tuning: updates model
> weights on domain-specific data; best when style, format, or
> specialised knowledge must be baked in. Cost/complexity order: prompt
> \< RAG \< fine-tuning.

50. **Explain object detection vs. image segmentation.**

> Object detection (YOLO, Faster-RCNN) predicts bounding boxes and class
> labels for objects. Semantic segmentation (FCN, DeepLab) classifies
> every pixel into a class category. Instance segmentation (Mask R-CNN)
> combines both --- per-instance pixel masks. UNet (which I\'ve used)
> performs semantic segmentation. The right choice depends on whether
> you need pixel-level precision or just bounding boxes.

**8. System Design (ML Systems)**

51. **Design a real-time fraud detection system.**

> Components: (1) Kafka ingests transaction events at high throughput.
> (2) Flink/Spark Streaming computes real-time features (velocity,
> z-score vs. user history). (3) Feature store (Redis) for low-latency
> feature lookup. (4) FastAPI inference service with pre-loaded XGBoost
> model on Kubernetes. (5) Async decision return (\<50ms SLA). (6)
> Decisions logged to PostgreSQL for model retraining. (7)
> Grafana/Prometheus for latency and model drift monitoring.

52. **Design a scalable recommendation system for a social media app.**

> Two-stage architecture: (1) Candidate generation --- ANN lookup using
> NCF/matrix factorisation embeddings (FAISS index) to retrieve top-1000
> candidates from millions. (2) Ranking --- a full-feature MLP/gradient
> boosting model scores the 1000 candidates using rich contextual
> features (user history, content metadata, recency). (3) Serving ---
> FastAPI + Redis caching of user embeddings, updated hourly. (4) A/B
> testing framework for model iteration.

53. **How would you design an LLM-powered customer support system?**

> Components: (1) Intent classifier (LLM or fine-tuned BERT) routes
> queries to FAQ/retrieval/agent. (2) RAG pipeline over documentation +
> past resolved tickets. (3) LLM generates the response grounded in
> retrieved context. (4) Confidence thresholding --- low confidence
> escalates to human agent. (5) Conversation memory for multi-turn
> context. (6) Evaluation pipeline (LLM-as-judge) for continuous quality
> monitoring. (7) Feedback loop: thumbs up/down refines retrieval
> ranking.

54. **How do you handle model drift in production?**

> Monitor: (1) Data drift --- statistical tests (KS test, PSI) on
> feature distributions vs. training baseline. (2) Prediction drift ---
> shifts in output distribution. (3) Performance drift --- ground truth
> labels arrive with lag; track rolling accuracy/F1. Response: automated
> alerting at thresholds, triggered retraining pipelines (Airflow DAG),
> and shadow deployment of the retrained model before cutover.

**9. Behavioural & Situational Questions**

55. **Tell me about a time you faced a significant technical
    challenge.**

> At Pegasystems, the GPT-OSS 120B model OOM\'d on A100s during initial
> deployment. I profiled memory usage and discovered the KV cache was
> the bottleneck for long-context requests. I switched from naive
> HuggingFace generation to vLLM with PagedAttention, which manages KV
> cache in non-contiguous blocks. Combined with FlashAttention and FP16
> quantisation, memory overhead dropped 50% and throughput increased 5x.

56. **Describe a time you had to work with cross-functional
    stakeholders.**

> At Pegasystems, the \'Chat With Your Data\' agent required alignment
> with data engineering (for schema access), security (for SQL injection
> guardrails), and 50+ enterprise client teams (for use-case
> requirements). I ran weekly syncs with data engineering to maintain
> schema versioning, co-designed the security model with the infosec
> team, and used client feedback sessions to iteratively improve query
> accuracy.

57. **How do you keep up to date with the rapidly evolving AI
    landscape?**

> I read Arxiv daily (cs.LG, cs.CL sections), follow newsletters like
> The Batch and Alpha Signal, engage with the ML engineering community
> on Medium (I write there too), and implement key papers in side
> projects. I also attend internal knowledge-sharing sessions and track
> production ML blogs from companies like Databricks, Hugging Face, and
> Anthropic.

58. **Why are you looking for a new opportunity?**

> I\'m looking for a role where I can work at the cutting edge of
> applied AI at larger scale, tackle harder research-to-production
> challenges, and deepen my impact on product-level AI systems. I\'m
> especially interested in \[Company\'s\] work on \[specific area\],
> which aligns with my experience in LLM infrastructure and GenAI
> product development.

59. **Where do you see yourself in 5 years?**

> I see myself as a senior ML engineer or technical lead specialising in
> large-scale AI systems --- bridging research and production. I want to
> have shipped multiple LLM-powered products that measurably move
> business KPIs, published applied research, and mentored junior
> engineers. I\'m also interested in the architecture side --- designing
> ML platform infrastructure that enables teams to move from idea to
> production faster.

60. **What are your strengths and areas of improvement?**

> Strengths: strong full-stack ML knowledge from data pipelines to
> inference optimisation, ability to translate research papers into
> production systems quickly, and cross-functional communication. Area
> of improvement: I tend to dive deep into optimisation details early
> --- I\'m actively practising time-boxing proof-of-concepts and
> validating assumptions with stakeholders before optimising.

**10. Education & Academic Background**

61. **How did your M.S. in Data Science at IIIT Hyderabad complement
    your industry experience?**

> The M.S. formalised my understanding of advanced ML theory ---
> probabilistic graphical models, optimisation, Bayesian methods ---
> that I had been applying pragmatically. It also exposed me to research
> methodology: reading papers critically, designing controlled
> experiments, and writing about results rigorously. This directly
> improved my ability to evaluate and adopt new techniques like RAG and
> RLHF faster.

62. **What relevant coursework or research did you do during your
    M.S.?**

> Core courses included Deep Learning, Natural Language Processing,
> Computer Vision, Reinforcement Learning, and Distributed Computing. My
> thesis/projects focused on representation learning and LLM
> fine-tuning. I complemented coursework with industry projects at
> AwoneAI, running in parallel with my studies.

**11. Coding, Algorithms & Data Structures**

63. **What is the time complexity of the attention mechanism in
    Transformers and why is it a problem?**

> Standard self-attention is O(N²) in both time and memory where N is
> the sequence length, because every token attends to every other token.
> For N=16K tokens this is 256M attention weights per layer per head ---
> infeasible. Solutions include FlashAttention (IO-aware exact
> attention), sparse attention (Longformer, BigBird), and sliding window
> attention.

64. **How would you implement a rate limiter for an LLM API service?**

> Use the Token Bucket algorithm: each user has a bucket with a max
> capacity of T tokens replenished at rate R tokens/second. Each request
> consumes tokens proportional to its cost (input + output tokens). If
> the bucket is empty, the request is rejected or queued. Implement with
> Redis (INCR + EXPIRE commands) for distributed enforcement across
> multiple API nodes.

65. **Explain a hash map and its use in ML systems.**

> A hash map stores key-value pairs with O(1) average-case lookup/insert
> via a hash function mapping keys to array indices. In ML systems:
> feature lookups (entity ID → feature vector), vocabulary indexing
> (token → ID), in-memory caching of embeddings, and deduplication of
> training examples. Python dicts are implemented as hash maps.

66. **What is the difference between Python\'s multiprocessing and
    multithreading for ML workloads?**

> Python\'s GIL (Global Interpreter Lock) prevents true parallel thread
> execution for CPU-bound tasks, making multithreading unsuitable for
> CPU-intensive ML preprocessing. Multiprocessing spawns separate OS
> processes each with their own Python interpreter and GIL, enabling
> true CPU parallelism. For IO-bound tasks (network requests to LLM
> APIs), asyncio or threading is sufficient and lighter-weight.

**12. Company & Role-Specific Questions**

67. **What do you know about Pegasystems and your current role there?**

> Pegasystems is a CRM and BPM software company known for its low-code
> platform and AI-driven automation (Next Best Action). In my role I
> build the AI/ML infrastructure powering Pega\'s GenAI capabilities ---
> the assistant service, LLM deployment, evaluation framework, and data
> analytics agents --- which are consumed by enterprise clients across
> industries like insurance, banking, and healthcare.

68. **Why do you want to join \[Target Company\]?**

> I\'m drawn to \[Company\] because of \[specific
> product/technology/mission\]. My experience in \[relevant area ---
> e.g., LLM infrastructure, RAG, ML platform\] directly maps to what
> your team is building. I\'m particularly excited about \[specific
> challenge/project mentioned in JD\] because it would let me push the
> boundaries of what I\'ve done at Pegasystems --- moving from
> single-model serving to \[multi-agent / enterprise-scale /
> research-driven\] applications.

69. **What questions do you have for us?**

> Good questions to ask: (1) What does the model development lifecycle
> look like here --- how long from idea to production? (2) How do you
> approach evaluation of GenAI systems, especially for open-ended
> outputs? (3) What is the biggest ML infrastructure challenge your team
> is currently tackling? (4) How does the ML team collaborate with
> product and data engineering? (5) What does success look like in the
> first 90 days?

***End of Interview Preparation Guide***

**Good luck, Abhay!**
