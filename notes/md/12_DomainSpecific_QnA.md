**Domain-Specific ML Knowledge**

*Healthcare, Ads, Enterprise SaaS, NLP --- Interview Q&A*

**Healthcare ML**

1.  **What special constraints apply to ML in healthcare settings?**

> Regulatory: HIPAA (US) requires PHI to be de-identified or consented;
> models accessing patient data need Business Associate Agreements. GDPR
> (EU) adds \'right to explanation\' --- model decisions affecting
> patients must be explainable. Interpretability: clinical stakeholders
> require explainable outputs (SHAP, LIME, attention visualisation);
> black-box models face adoption resistance. Class imbalance: rare
> diseases, rare adverse events --- require careful threshold tuning and
> AUC-PR focus. Data scarcity: small labelled datasets for specialised
> conditions --- few-shot learning, transfer from general models, and
> federated learning (training across hospitals without sharing raw
> data) are key approaches.

2.  **How do you handle class imbalance in fraud detection?**

> Fraud is typically \<1% of transactions. Strategy stack: (1) Data:
> SMOTE or ADASYN for minority oversampling; random undersampling of
> majority. (2) Algorithm: scale_pos_weight in XGBoost (ratio of
> negative to positive class); class_weight in sklearn. (3) Loss: focal
> loss down-weights easy negatives during neural network training. (4)
> Evaluation: AUC-PR as primary metric, not accuracy. (5) Threshold:
> select decision threshold by minimising total cost (cost_FP \*
> FP_count + cost_FN \* FN_count) --- fraud teams can define these
> costs. (6) Anomaly detection: train only on normal transactions; flag
> anomalies --- avoids class imbalance entirely.

**Ad & Recommendation Systems**

3.  **Explain the explore-exploit tradeoff and bandit algorithms.**

> Explore-exploit dilemma: should you show the ad/item you think is best
> (exploit) or try a new option to learn if it\'s better (explore)? Too
> much exploitation = miss better options; too much exploration = waste
> impressions. Bandit algorithms: Epsilon-Greedy (exploit with prob 1-ε,
> explore randomly with ε). UCB (Upper Confidence Bound): select item
> with highest UCB = mean_reward + c \* sqrt(ln(t)/n_pulls) ---
> optimistic under uncertainty. Thompson Sampling: sample from Beta
> posterior for each arm, select arm with highest sample --- Bayesian,
> naturally balances explore/exploit. In production recommendation:
> Thompson Sampling is standard for new content bootstrapping.

4.  **What is position bias in recommendation systems and how do you
    correct for it?**

> Position bias: items shown at higher positions get more clicks
> regardless of relevance --- contaminating click data as implicit
> relevance feedback. Correction methods: (1) Inverse Propensity Scoring
> (IPS) --- weight each click by 1/P(shown at position k), where
> propensity is estimated from randomised experiments or click models.
> (2) Regression EM (position-aware click model) --- jointly model
> examination probability and relevance. (3) Randomise positions in a
> small traffic fraction to collect unbiased training data. Unaddressed
> position bias causes the model to learn \'show at top\' = relevant,
> reinforcing existing rankings.

5.  **How do you handle the cold start problem in recommendation
    systems?**

> Cold start types: New User --- no interaction history. New Item --- no
> engagement data. Solutions for new users: onboarding questionnaire to
> capture preferences, demographic-based recommendations
> (content-based), popular items fallback, transfer from similar users
> (collaborative). Solutions for new items: content-based features
> (title, description, category embeddings), meta-learning (train a
> model to adapt quickly from few interactions), and exploration
> policies that intentionally expose new items. Hybrid systems: use
> content-based features until sufficient interactions exist, then
> switch to collaborative filtering.

**Enterprise SaaS ML**

6.  **How do you handle multi-tenancy in ML systems --- different models
    or data per client?**

> Approaches by isolation level: (1) Shared model --- one model for all
> clients; simplest, risks client data leakage if not careful, cannot
> personalise. (2) Client-specific fine-tuning --- shared base model,
> per-client LoRA adapters loaded at inference; balances personalisation
> with resource efficiency. (3) Federated learning --- train on each
> client\'s data locally, aggregate gradients centrally; strong privacy
> but complex. (4) Per-client feature namespacing --- prefix all
> features with client_id to prevent cross-client influence in a shared
> model. For the \'Chat With Your Data\' agent: per-client schema
> context in the RAG pipeline isolates data without separate models.

**NLP for Enterprise Data**

7.  **Explain Named Entity Recognition (NER) and how you would build an
    enterprise NER system.**

> NER identifies and classifies entities in text (person, organisation,
> location, date, product, custom types). For enterprise: start with a
> pre-trained model (spaCy\'s transformer-based models, BERT-based token
> classifiers) fine-tuned on domain-specific annotated examples. Custom
> entity types (contract clauses, product codes, regulatory terms)
> require 500--2000 labelled examples per entity type. Active learning:
> use model uncertainty to select the most informative samples for
> annotation. Deploy with a confidence threshold --- low-confidence
> predictions go to human review. Use BIOES tagging scheme for
> multi-token entities.

8.  **What is intent classification and slot filling in enterprise
    chatbots?**

> Intent classification identifies what the user wants (e.g.,
> \'query_sales\', \'create_report\', \'explain_anomaly\'). Slot filling
> extracts the parameters needed to fulfil the intent (e.g., date_range:
> \'last quarter\', region: \'APAC\'). Traditional NLU systems use
> separate classifiers for each task. Modern approach: fine-tune a joint
> model (BERT-based) that does both simultaneously --- shared encoder,
> two output heads. For LLM-based systems: use structured output
> prompting to extract intent + slots in one pass (prompt the model to
> respond in JSON with intent and slots fields). Validate extracted
> slots against schemas before executing actions.
