**ML Theory --- Deep Dive**

*Interview Q&A*

**Bias, Variance & Regularisation**

1.  **Explain the bias-variance tradeoff.**

> Bias is error from wrong assumptions --- high bias models
> (underfitting) miss true patterns. Variance is error from sensitivity
> to training data fluctuations --- high variance models (overfitting)
> memorise noise. Total error = Bias² + Variance + Irreducible noise.
> The tradeoff: reducing bias (more complex model) typically increases
> variance, and vice versa. The goal is finding the sweet spot of model
> complexity. Regularisation, dropout, and ensembles manage this
> tradeoff.

2.  **Explain L1 vs L2 regularisation. When to use each?**

> L2 (Ridge): adds λ \* Σwᵢ² to the loss --- penalises large weights,
> shrinks all towards zero but rarely to exactly zero. Produces dense
> solutions. L1 (Lasso): adds λ \* Σ\|wᵢ\| --- penalises absolute
> magnitude, produces sparse solutions (some weights exactly zero) ---
> acts as feature selection. Elastic Net: combines both (α \* L1 + (1-α)
> \* L2). Use L2 when all features are expected to contribute. Use L1
> for high-dimensional sparse data (text features) where automatic
> feature selection is valuable.

**Optimisation**

3.  **Explain SGD, Adam, and AdamW. What are their differences?**

> SGD (Stochastic Gradient Descent): updates weights using gradient of a
> mini-batch. Simple but sensitive to learning rate and doesn\'t adapt
> per-parameter. Momentum SGD adds a velocity term. Adam: adaptive
> learning rates per parameter using first moment (mean gradient) and
> second moment (uncentred variance). Formula: θ = θ - lr \* m̂ / (√v̂ +
> ε). Converges fast but can generalise worse than SGD in some settings
> (marginal value issue). AdamW: decouples weight decay from the
> gradient update (fixes Adam\'s weight decay bug) --- standard for
> Transformer training. For CV: SGD with momentum + cosine LR schedule
> often beats Adam. For LLMs: AdamW is standard.

4.  **What are learning rate schedulers? Which do you use for
    Transformers?**

> Schedulers adjust the learning rate during training. Common types:
> StepLR (halve every N epochs), CosineAnnealing (LR follows cosine
> curve to near-zero), OneCycleLR (warm up then decay --- fast
> convergence), ReduceLROnPlateau (decay on metric stagnation). For
> Transformers: linear warmup + linear/cosine decay is standard. Warmup
> is critical because early random weights produce large gradient
> variance --- starting with a small LR and ramping up prevents early
> instability. PyTorch: use get_linear_schedule_with_warmup from
> transformers library.

**Normalisation Layers**

5.  **Explain Batch Norm, Layer Norm, and RMS Norm. Why do Transformers
    use Layer Norm?**

> Batch Norm: normalises across the batch dimension for each feature ---
> statistics depend on batch size, ineffective for small batches, can\'t
> be used in RNNs/Transformers with variable-length sequences. Layer
> Norm: normalises across the feature dimension for each sample
> independently --- no batch dependency, works with any batch size and
> sequence length. RMS Norm: simpler variant of Layer Norm without the
> mean subtraction (only divides by root mean square) --- faster, used
> in LLaMA and modern LLMs. Transformers use Layer Norm (or RMS Norm)
> because they process variable-length sequences and training often uses
> small effective batch sizes (large hidden dims instead).

**Evaluation & Calibration**

6.  **When would you use AUC-PR instead of AUC-ROC?**

> AUC-ROC measures the tradeoff between TPR and FPR --- it\'s optimistic
> on imbalanced datasets because the large number of true negatives
> inflates TPR performance. AUC-PR (Precision-Recall) focuses only on
> the positive class --- more informative when positives are rare (e.g.,
> fraud detection: 0.1% fraud rate). A model with 0.95 AUC-ROC may have
> only 0.3 AUC-PR on an imbalanced dataset. Use AUC-PR as the primary
> metric for fraud, medical diagnosis, anomaly detection, and
> information retrieval tasks.

7.  **What is model calibration and when does it matter?**

> A calibrated model outputs probabilities that reflect actual
> frequencies --- if it predicts 0.8 probability for 1000 samples,
> roughly 800 should be positive. Measured with calibration curves
> (reliability diagrams). Uncalibrated models are problematic when
> probabilities drive decisions (e.g., risk scores, expected value
> calculations). Calibration methods: Platt Scaling (logistic regression
> over raw scores), Isotonic Regression (more flexible), Temperature
> Scaling (for neural networks --- divide logits by learned scalar T).
> XGBoost and tree ensembles are often poorly calibrated out of the box.

8.  **What is NDCG and MRR? Where are they used?**

> NDCG (Normalised Discounted Cumulative Gain): measures ranking quality
> with position-discounted relevance. A highly relevant item at position
> 1 contributes more than the same item at position 5. Normalised by the
> ideal ranking\'s DCG. Used for recommendation systems and search
> ranking evaluation. MRR (Mean Reciprocal Rank): average of 1/rank of
> the first relevant item across queries. Used when only the first
> correct result matters (QA systems, entity linking). Both are standard
> metrics for evaluating RAG retrieval quality and recommendation
> engines.

**Class Imbalance**

9.  **How do you handle severe class imbalance in ML models?**

> Strategies at different levels: Data level --- oversampling positives
> (SMOTE generates synthetic minority samples via interpolation),
> undersampling majority, combined approaches (SMOTEENN). Algorithm
> level --- class_weight=\'balanced\' in sklearn/XGBoost reweights the
> loss inversely proportional to class frequency; adjust decision
> threshold using precision-recall analysis. Evaluation level --- always
> use AUC-PR, F1, or business-specific cost-weighted metrics instead of
> accuracy. For deep learning: focal loss (down-weights easy negatives,
> up-weights hard positives) is highly effective for imbalanced
> detection tasks.

**Hyperparameter Tuning**

10. **Compare grid search, random search, and Bayesian optimisation
    (Optuna).**

> Grid Search: exhaustive, covers all combinations --- exponential cost
> with more parameters. Only practical for 2--3 parameters. Random
> Search: samples configurations randomly --- more efficient than grid
> (Bergstra & Bengio 2012 showed random search finds better configs in
> same budget when some params matter more than others). Bayesian
> Optimisation (Optuna, Hyperopt): builds a probabilistic model (Tree
> Parzen Estimator or Gaussian Process) of the objective surface,
> intelligently selecting next trial to balance
> exploration/exploitation. Most efficient for expensive evaluations
> (e.g., training large models). Optuna adds pruning --- early-stopping
> unpromising trials via Successive Halving.
