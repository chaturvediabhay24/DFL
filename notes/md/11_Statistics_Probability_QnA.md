**Statistics & Probability**

*Interview Q&A --- Deep Dive*

**Core Probability**

1.  **Explain Bayes\' Theorem and its use in ML.**

> Bayes\' Theorem: P(A\|B) = P(B\|A) \* P(A) / P(B). In ML: Naive Bayes
> classification computes P(class \| features) ∝ P(features \| class) \*
> P(class). In Bayesian ML: P(θ\|data) ∝ P(data\|θ) \* P(θ) --- the
> posterior over parameters combines the likelihood with a prior
> (encoding domain knowledge or regularisation). This framework
> naturally handles uncertainty quantification. Bayesian hyperparameter
> optimisation (TPE in Optuna) uses Bayes\' theorem to model which
> hyperparameter configurations are likely to perform well given past
> trials.

2.  **What is the Central Limit Theorem and why is it fundamental to
    ML?**

> CLT states that the sampling distribution of the sample mean
> approaches a normal distribution as sample size increases, regardless
> of the population distribution (given finite variance). Fundamental to
> ML because: (1) Statistical hypothesis tests (t-test, z-test) assume
> normality of sample statistics --- CLT justifies this for large N. (2)
> A/B test significance analysis relies on CLT to compute p-values for
> metric differences. (3) SGD gradient estimates (averages of per-sample
> gradients) are approximately Gaussian for large batch sizes, which is
> why Gaussian noise in DP-SGD is well-calibrated.

**Hypothesis Testing**

3.  **Explain p-value, Type I error, Type II error, and statistical
    power.**

> p-value: probability of observing data at least as extreme as
> measured, assuming the null hypothesis is true. Not the probability
> that H0 is true. Type I error (α): false positive --- rejecting H0
> when it is true. Controlled by significance threshold (α = 0.05 means
> 5% chance of false positive). Type II error (β): false negative ---
> failing to reject H0 when it is false. Statistical power (1-β):
> probability of correctly detecting a real effect. Power depends on
> effect size, sample size, and α. For A/B tests: run a power analysis
> before the test to determine required sample size --- underpowered
> tests produce unreliable results even with significant p-values.

4.  **What is the difference between frequentist and Bayesian
    inference?**

> Frequentist: parameters are fixed unknowns; probability represents
> long-run frequency. Makes point estimates (MLE) and uses confidence
> intervals (which are often misinterpreted). Bayesian: parameters have
> probability distributions; probability represents degree of belief.
> Prior + data → posterior. Provides credible intervals (e.g., \'there
> is 95% probability the true value is in this interval\' --- the
> intuitive interpretation people mistakenly apply to frequentist CIs).
> For ML: MLE training is frequentist; Bayesian neural networks and GP
> models are Bayesian and provide uncertainty estimates naturally.

**Distributions**

5.  **Explain when to use Gaussian, Bernoulli, Poisson, and Beta
    distributions in ML.**

> Gaussian (Normal): continuous features, errors, and noise. Assumption
> in linear regression residuals, many statistical tests. Bernoulli:
> binary outcomes (0/1) --- models single binary events (click/no-click,
> fraud/not). Logistic regression models the Bernoulli parameter.
> Poisson: count data --- models the number of events in a fixed time
> interval (number of transactions per hour, server requests per
> minute). Assumption: events are independent and occur at a constant
> rate. Beta: probability values in \[0,1\]. Conjugate prior for the
> Bernoulli/Binomial likelihood in Bayesian inference. Used in Thompson
> Sampling for multi-armed bandits and click-through rate modelling.

**Dimensionality & PCA**

6.  **Explain PCA intuitively. What is the role of eigenvalues and
    eigenvectors?**

> PCA finds the directions (principal components) of maximum variance in
> the data. Mathematically: compute the covariance matrix of the centred
> data; eigenvectors are the principal component directions; eigenvalues
> represent the variance explained by each component. Project data onto
> the top-k eigenvectors to reduce dimensionality while retaining
> maximum variance. Intuition: PCA rotates the coordinate system so the
> first axis captures the most spread, second axis the next most
> (orthogonal), etc. Use cases in ML: visualisation (t-SNE/UMAP are
> non-linear alternatives), noise reduction, and decorrelating features
> for downstream models.

**Resampling & Confidence Intervals**

7.  **What is bootstrap sampling and how is it used for confidence
    intervals in ML?**

> Bootstrap: repeatedly sample N observations with replacement from the
> dataset (generating B bootstrap samples), compute the statistic of
> interest (e.g., model accuracy) on each sample. The distribution of
> these B estimates approximates the sampling distribution. Confidence
> interval: take the 2.5th and 97.5th percentiles of the bootstrap
> distribution (percentile method). Use in ML: confidence intervals for
> model evaluation metrics when test set is small, measuring uncertainty
> in A/B test uplift estimates, and ensemble methods (bagging trains
> each model on a bootstrap sample --- Random Forest).

**MLE & MAP**

8.  **Explain Maximum Likelihood Estimation (MLE) vs Maximum A
    Posteriori (MAP).**

> MLE: finds parameters θ that maximise the likelihood P(data\|θ) ---
> equivalently, minimise negative log-likelihood. No prior on
> parameters. For Gaussian errors, MLE = least squares regression. MAP:
> finds θ that maximises the posterior P(θ\|data) ∝ P(data\|θ) \* P(θ).
> Equivalent to MLE with regularisation: a Gaussian prior on θ → L2
> regularisation (Ridge); a Laplace prior → L1 regularisation (Lasso).
> This is the deep connection between Bayesian inference and
> regularisation: adding a prior to MLE is equivalent to adding a
> regularisation penalty.
