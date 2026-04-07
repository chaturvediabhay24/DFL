# Your AI Agent is Forgetting Things — Here's How DTOC Fixes That

*A simple explanation of Dynamic Tool Output Compression, and why it matters for the future of AI agents*

---

Have you ever been in a long meeting where the person taking notes just kept writing everything — every single word — and by the end, nobody could find the important stuff because it was buried under too much information?

That is exactly what is happening inside your AI agents today.

Let me explain.

---

## First, What is an AI Agent?

Think of an AI agent as a smart assistant that can use tools — it can search the internet, read files, run code, check databases, and so on. Every time it uses a tool, the result comes back and gets added to its "memory" — what we call the **context window**.

The context window is basically the AI's short-term memory. It can only hold so much at a time.

Now imagine you ask this agent to do a research task that takes 20 steps. After step 1, it searches the web and gets back 3,000 words. After step 2, it reads a document — another 2,000 words. Step 3, another search. Step 4, reads some code...

By step 10 or 12, the context window is almost full. The agent is drowning in its own notes.

---

## The Problem: Context Rot

Here is something that makes this worse — even if the AI has a large context window (say, 1,28,000 tokens, which is roughly 96,000 words), it doesn't actually work well when it is filled up completely.

There is a real effect called **"Context Rot"** — as the context gets longer and longer, the AI starts losing track of things that were written early on. Like how we forget the first paragraph of a very long article by the time we reach the end.

So a model that *claims* to handle 1,28,000 tokens might actually start making mistakes after 60,000 tokens. That is only half its capacity!

And what typically gets pushed out or forgotten? The most important things — like the original instructions, the user's main goal, key constraints. The stuff from the beginning of the conversation.

---

## What Do People Do Today? (And Why It Doesn't Work Well)

There are three common ways people try to handle this problem today:

**1. Hard Truncation — Just Cut the Old Stuff**

The simplest approach: once the memory is full, delete the oldest messages. Done.

The problem? Sometimes the oldest message is the most important one — it might contain the original task, a safety rule, or a key piece of data. Once it's deleted, it's gone forever. The agent doesn't even know what it lost.

**2. LLM Summarization — Let the AI Summarize Its Own Notes**

A smarter approach: instead of deleting, ask another AI to summarize the old content. Keep the summary, throw away the details.

The problem? Summaries are lossy — details get lost. Error codes, exact numbers, specific identifiers — these get "smoothed over" in summaries. And sometimes the AI summarizes incorrectly (hallucination). Worse, summaries take time and add latency. Systems like OpenHands and Cursor use this approach, but it introduces its own failures.

**3. Static Masking — Hide Old Outputs Based on Rules**

Hide tool outputs that are older than, say, 4 steps. Simple rule, easy to implement.

The problem? Rules don't understand context. Maybe step 2's output is the most important thing for step 18. The rule doesn't know that. Once hidden (or deleted), the agent has to re-run the tool again — wasting time and compute.

---

## Enter DTOC: A Smarter Way

**DTOC stands for Dynamic Tool Output Compression.**

The core idea is beautifully simple:

> Instead of deleting or summarizing old tool outputs, just *hide* them temporarily. Keep the full content safe on the server. Show the agent only a small placeholder. When the agent needs the old output again, it can ask for it back — and get the *exact original content*.

Think of it like this: you have a big desk full of papers. Instead of throwing papers away, you put them in a drawer. Your desk stays clean and you can focus. But if you need one of those papers again, you can just open the drawer and take it out. Nothing is lost.

That's DTOC.

---

## How Does It Actually Work?

Let's walk through it step by step.

**Step 1: Every tool output gets a label**

When the AI calls a tool and gets a result, the system wraps that result in a small envelope:

```
{
  "tool_id": "tool_001",
  "tool_result": "...the actual content...",
  "estimated_tokens": 1200
}
```

Every output has a unique ID, the actual content, and an approximate size.

**Step 2: A special "manage context" tool is given to the agent**

The agent now has one extra tool it can use — `manage_context`. This tool takes two lists:
- `disable`: IDs of outputs to hide
- `enable`: IDs of outputs to bring back

**Step 3: Agent decides what to hide**

When the agent feels its memory is getting full, it can say: "Tool 001 and Tool 003 are not relevant right now — let me hide them."

In the context window, those outputs are replaced by tiny placeholders:

```
tool_001 | ~1200 tokens | hidden | [timestamp]
```

The desk is now clean. Only the currently relevant stuff is visible.

**Step 4: Agent can always bring back what it needs**

Later, if the agent realizes it needs tool_001's output again, it simply calls `manage_context(enable=["tool_001"])` and the full original content comes back. No re-running the tool. No summarization errors. The exact original data.

This is **lossless and reversible** — the two most important properties of DTOC.

---

## A Real Example: Debugging Code

Imagine an AI agent debugging a large codebase.

- Step 1: It reads `auth.py` — 4,000 tokens
- Step 2: It reads `database.py` — 3,500 tokens
- Step 3: It reads `config.py` — 2,000 tokens
- Step 4: It searches for error logs — 5,000 tokens
- Step 5: It reads `api_handler.py` — 4,500 tokens

By step 5, it's using ~19,000 tokens just from file reads.

With DTOC, after step 3, the agent might think: "I've already understood auth.py and the config. I don't need their full content right now. Let me hide them."

It hides steps 1 and 3. Context drops by 6,000 tokens. The agent can now focus on the error logs and api_handler.

Later, if it finds a bug in api_handler that links back to auth.py, it simply re-enables step 1's output. Full content, instantly available. No repeated file read. No summarization.

---

## Does It Actually Work? The Numbers Say Yes

The paper tested DTOC on three tasks — answering complex questions (HotpotQA), research synthesis, and code bug detection — and compared it against the three older approaches.

**Multi-Hop Question Answering (100 questions):**

| Approach | Success Rate | Context Used |
|---|---|---|
| No Compression | 78.2% | 89K tokens |
| Static Masking | 76.8% | 45K tokens |
| **DTOC** | **87.6%** | **63K tokens** |

DTOC used 30% less context AND got better answers. Static masking used less context but actually got *worse* answers because it threw away useful information.

**Research Synthesis (50 tasks):**

| Approach | Quality (0-10) | Context | Time |
|---|---|---|---|
| No Compression | 8.2 | 94K | 18.5s |
| Static Threshold | 7.1 | 48K | 16.2s |
| LLM Summarization | 8.0 | 56K | 28.3s |
| **DTOC** | **8.3** | **65K** | **21.8s** |

DTOC scored the highest quality while using much less context than no compression. LLM summarization was 50% slower and still scored lower!

**Code Bug Detection (30 codebases):**

| Approach | Bugs Found | Context | File Re-reads |
|---|---|---|---|
| No Compression | 60.1% | 102K | 0 |
| Static Threshold | 72.0% | 52K | 4.2 avg |
| LLM Summarization | 73.3% | 58K | 0.1 avg |
| **DTOC** | **93.3%** | **61K** | **0** |

This one is striking. DTOC found bugs in 93.3% of codebases compared to just 60.1% with no compression. Why? Because when the context is cleaner and more focused, the AI can think better. It's not distracted by irrelevant old data.

---

## The Key Insight: Less Clutter = Better Thinking

This is the most important thing to understand from this research.

**More context is not always better.**

When the AI's "desk" is cluttered with 20 tool outputs, it gets confused — it loses focus, gets distracted by old information, and misses important things. By keeping the active context clean and focused, DTOC actually *improves* performance, not just efficiency.

It's like the difference between a tidy workspace and a messy one. You can work better when you're not surrounded by unnecessary clutter.

---

## The "Re-enable" Feature is Critical

One thing the paper specifically tested: what if you only allow hiding but not re-enabling?

| Configuration | Success Rate | Context |
|---|---|---|
| No compression | 78.2% | 89K |
| Disable only (no re-enable) | 81.4% | 57K |
| **Full DTOC (enable + disable)** | **83.6%** | **61K** |

"Disable only" is better than nothing, but it still has the risk of losing important information permanently. Full DTOC — where you can always get things back — gives the best results with zero re-reads.

The ability to say "I need that back" is what makes DTOC safe and reliable.

---

## One Funny Side Effect: Context Paranoia

Researchers noticed something amusing during testing. Some agents, when given the ability to re-enable outputs, started re-enabling *everything* "just in case." Like a worried student who keeps all their textbooks open on the desk even when they only need one.

This defeats the purpose.

The fix? Show the agent its current token usage — like a fuel gauge. "You are at 71% of your budget. Consider optimizing." When agents can see the cost of their decisions, they make smarter choices.

---

## What's Next? Three Improvements Being Explored

**1. Budget-Aware Prompting**

Show the agent a live "context status" at each step:

```
Current tokens: 64,234 / 128,000 (50.2%)
Effective budget: 89,600 tokens
Status: APPROACHING THRESHOLD
```

This makes context feel like a real resource, not an invisible limit. Early tests show this reduces forced truncation by 40%.

**2. Chunked Tool Output Retrieval**

What if a single tool output is 30,000 tokens? (Think: a large log file, a full codebase, an entire research paper.) DTOC can't hide it fast enough before it fills the context.

Solution: break large outputs into smaller pieces automatically. Return the first piece, give summaries of the rest, and let the agent ask for specific chunks. Like reading a book chapter by chapter instead of all at once.

**3. Handling Large User Inputs**

Sometimes the *user* pastes a huge document — a 50,000-token research paper — before the agent even starts. The agent is already half-full before doing anything.

This is trickier because DTOC normally manages outputs the agent creates, not inputs from the user. Future work will address how to handle this pre-emptively.

---

## Why This Matters for Everyone Building AI

If you are building AI agents — for customer support, code review, research, data analysis, anything with multiple steps — context management is not a side problem. It is a core problem.

The old way: hope the context window is big enough, and when it fills up, truncate or summarize and hope for the best.

The DTOC way: treat context as a managed resource. Hide what's not needed now. Restore what becomes needed later. Never lose anything.

The result? Better answers, lower costs (fewer tokens = cheaper API calls), and more reliable agents.

---

## The Big Picture

DTOC is not just a technical trick. It represents a shift in how we think about AI agents.

Today, most agents are passive about their memory — they just accumulate information until something breaks.

DTOC makes agents *active managers of their own memory*. The agent decides what to remember, what to temporarily forget, and what to bring back. This is much closer to how humans actually think during complex tasks.

We don't try to hold everything in our head at once. We focus on what's relevant now, keep notes for later, and refer back when needed.

DTOC gives AI agents the same ability.

---

## Summary: What You Need to Remember

- AI agents have limited "working memory" called a context window
- As agents do more steps, this fills up — causing errors and forgetting
- Old solutions (delete, summarize, static rules) all lose information permanently
- **DTOC hides tool outputs temporarily, keeping full content safe on the server**
- Agents can re-enable any output at any time — nothing is ever truly lost
- This reduces context usage by 30-50% while actually *improving* performance
- It works across different models (GPT-4o, Claude) and different tasks
- It's simple to implement — just one extra tool in the agent's toolkit

---

*This article is based on the research paper "Context Engineering for AI Agents: DTOC — Dynamic Tool Output Compression" by Abhay Chaturvedi.*

---

**If you found this useful, do give a clap and share it with others who are building AI agents. Questions? Drop them in the comments — happy to explain further.**
