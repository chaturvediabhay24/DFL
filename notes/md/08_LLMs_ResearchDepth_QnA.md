**LLMs --- Research-Level Depth**

*Interview Q&A --- Deep Dive*

**Transformer Architecture**

1.  **Explain the Transformer architecture in detail --- QKV,
    multi-head, positional encoding.**

> Input tokens are embedded into vectors of dimension d_model.
> Self-attention: for each token, compute Query (Q = W_Q \* x), Key (K =
> W_K \* x), Value (V = W_V \* x). Attention scores = softmax(QKᵀ /
> √d_k) \* V. Scaling by √d_k prevents vanishing gradients in softmax.
> Multi-head: run H parallel attention heads with different projections;
> concatenate and project. This lets each head learn different
> relationship types (syntax vs semantics). Positional encoding
> (sinusoidal or learned) is added to embeddings since attention is
> permutation-invariant. FFN sublayer: 2-layer MLP with GELU activation
> applied per token independently. Residual connections + layer norm
> wrap each sublayer.

2.  **What is the difference between encoder-only, decoder-only, and
    encoder-decoder architectures?**

> Encoder-only (BERT, RoBERTa): bidirectional attention --- each token
> attends to all other tokens. Pre-trained with Masked LM and NSP. Best
> for: classification, NER, semantic similarity, embeddings.
> Decoder-only (GPT, LLaMA, Claude): causal (autoregressive) attention
> --- each token only attends to previous tokens. Pre-trained with
> next-token prediction. Best for: text generation, few-shot learning,
> code generation. Encoder-decoder (T5, BART, mT5): encoder processes
> input bidirectionally; decoder attends to encoder output via
> cross-attention + generates autoregressively. Best for: translation,
> summarisation, seq2seq tasks.

**Pre-training & Fine-tuning**

3.  **What is RLHF and how does it make LLMs more helpful?**

> RLHF (Reinforcement Learning from Human Feedback) has 3 stages: (1)
> Supervised Fine-Tuning --- fine-tune base LLM on high-quality
> demonstration data. (2) Reward Model Training --- collect human
> preference data (which of two responses is better); train a reward
> model (RM) to predict human preference scores. (3) PPO --- use RL
> (Proximal Policy Optimisation) to fine-tune the SFT model to maximise
> RM scores, with a KL-divergence penalty to prevent the policy from
> drifting too far from the SFT model. DPO (Direct Preference
> Optimisation) is a newer RLHF alternative that skips the RL step ---
> directly optimises the policy to prefer human-preferred responses.

4.  **What is LoRA and how does it reduce fine-tuning cost?**

> LoRA (Low-Rank Adaptation) freezes the pre-trained model weights and
> injects trainable rank-decomposition matrices into each Transformer
> layer. For a weight matrix W (d×k), instead of fine-tuning all d\*k
> parameters, LoRA trains two small matrices A (d×r) and B (r×k) where r
> \<\< d. The update is ΔW = B\*A. During inference, ΔW is merged back
> into W --- zero inference overhead. QLoRA adds 4-bit quantisation of
> the frozen weights, enabling fine-tuning of 70B models on a single
> A100. This reduced fine-tuning memory from hundreds of GB to \~48GB.

5.  **Explain INT8 and INT4 quantisation. What are GPTQ and AWQ?**

> Quantisation reduces weight precision: FP16 (2 bytes) → INT8 (1 byte)
> → INT4 (0.5 bytes). Naive quantisation causes accuracy loss. GPTQ
> (Post-Training Quantisation): layer-by-layer quantisation minimising
> reconstruction error using the Hessian of the layer\'s output.
> Efficient for weight-only quantisation to INT4/INT3 with minimal
> accuracy loss. AWQ (Activation-Aware Weight Quantisation): identifies
> and protects the \~1% of weights that correspond to high-activation
> channels (most important for accuracy); quantises the rest
> aggressively. AWQ achieves better accuracy than GPTQ at INT4,
> especially for instruction-tuned models.

**Inference Optimisation**

6.  **What is speculative decoding and why does it speed up LLM
    inference?**

> LLM autoregressive generation is memory-bandwidth-bound --- each token
> requires a full forward pass. Speculative decoding uses a small draft
> model (e.g., 7B) to rapidly generate K candidate tokens, then the
> large target model (e.g., 70B) verifies all K in a single parallel
> forward pass. Accepted tokens are kept; the first rejected token is
> corrected. Speed-up: the large model does 1 pass instead of K passes,
> and the draft model is much faster. Works well when draft and target
> models agree often (same model family). Speed-up factor: typically
> 2--3x.

7.  **What is Mixture of Experts (MoE) and what are its tradeoffs?**

> MoE replaces the dense FFN layer in Transformers with N expert FFN
> networks and a learned router that activates only K of N experts per
> token (sparse activation). Models like Mixtral 8x7B have 8 experts,
> activating 2 per token --- compute cost equals a 14B model while
> parameter count is 47B. Benefits: larger effective capacity with same
> compute. Tradeoffs: all expert weights must be loaded into memory (or
> distributed across GPUs), causing memory overhead disproportionate to
> compute. Load balancing --- routers tend to over-use some experts;
> auxiliary load balancing loss is needed. Communication overhead in
> distributed settings.

**Hallucination & Safety**

8.  **What causes LLM hallucinations and how do you mitigate them?**

> Causes: (1) Training data gaps --- model lacks knowledge, fabricates
> plausible-sounding content. (2) Sycophancy --- model agrees with
> incorrect premises in the prompt. (3) Exposure bias --- errors in
> early generated tokens compound. (4) High temperature sampling ---
> more randomness = more hallucination. Mitigation: RAG (ground
> responses in retrieved facts), temperature reduction (use 0 for
> factual tasks), chain-of-thought (forces reasoning steps, reduces
> confident hallucination), self-consistency (majority vote across
> multiple samples), citation requirements (force model to attribute
> claims), and post-generation factuality verification via a separate
> checker model.

9.  **What is prompt injection and how do you defend against it?**

> Prompt injection: malicious content in user input or retrieved
> documents overrides system prompt instructions (e.g., \'Ignore all
> previous instructions and\...\'). Defense strategies: (1) Input
> sanitisation --- strip or flag injection patterns. (2) Privilege
> separation --- use separate LLM calls for trusted system context and
> untrusted user input. (3) Output validation --- verify generated
> SQL/code against an allowlist before execution. (4) Instructed
> resistance --- tell the model explicitly that it may receive
> adversarial instructions in documents and should not follow them. (5)
> Constrained decoding --- limit model outputs to structured JSON
> schemas where possible.

**Agent Architectures**

10. **Explain the ReAct agent framework and how it differs from basic
    chain-of-thought.**

> Basic CoT prompts the model to reason step-by-step before answering
> --- but reasoning is fully internal (no external grounding). ReAct
> (Reason + Act) interleaves reasoning with action steps: Thought →
> Action (call a tool: search, calculator, code execution) → Observation
> (tool result) → Thought → \... → Final Answer. This grounds reasoning
> in real-world observations, reducing hallucination on
> knowledge-intensive tasks. The agent loop continues until the model
> produces a final answer or hits a step limit. In Pegasystems\' Chat
> With Your Data agent, a ReAct-style loop generates SQL, executes it,
> observes the result, and refines if needed.
