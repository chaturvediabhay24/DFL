# Week 7 Revision Notes: Branch Predictors, Out-of-Order Execution & Cache Basics

---

## Part 1: Branch Predictors

### What is a Control Hazard?

When the CPU is running a pipeline, it tries to keep every stage busy at all times. The problem with **branch instructions** (like `if`, `while`, `for` loops) is that the CPU doesn't know which instruction to fetch next until it has actually evaluated the branch condition — which happens a few pipeline stages later.

This waiting time is called a **control hazard** (or branch hazard).

**Fun fact from the slides:** Every 6th instruction is a branch. That is a lot of branching!

---

### Simple Techniques to Handle Control Hazards

Here are the four basic approaches the CPU can take:

#### 1. Always Stall
- Every time there is a branch, just pause the pipeline and wait until we know the result.
- Simple but very wasteful — you are basically doing nothing every 6 instructions.

#### 2. Assume Not Taken
- Optimistically assume the branch will NOT be taken and keep fetching instructions from the next sequential address (PC + 4).
- If you were right — great, no penalty.
- If you were wrong (branch IS taken) — you need hardware to **cancel** (flush/squash) the wrongly fetched instruction. The processor acts as if that instruction never happened.

#### 3. Branch Delay Slot
- Fetch the instruction right after the branch (this slot is called the **branch delay slot**) and execute it no matter what.
- If the branch is taken and the delay slot instruction is actually useful (i.e., it is the same instruction you would run anyway) — you get free useful work.
- If the branch is taken and the delay slot instruction is on the wrong path — you hope the program state is not messed up (i.e., the instruction is harmless or can be a NOP — No Operation).
- This is a compiler trick as much as a hardware trick.

#### 4. Branch Prediction (Smart Guess)
- Make an educated guess about whether the branch will be taken and which target to jump to.
- Fetch instructions from the **expected target** address immediately.
- This is the most powerful approach and is what modern CPUs use.

---

### Pipeline Without a Branch Predictor

```
PC --> IF (fetch branch) --> [stage] --> Reg Read / Compare / Compute Branch Target --> ...
       |                                        |
       +-------- PC + 4 (default) <-------------+  (feedback after we know the outcome)
```

- After fetching the branch, the PC just increments by 4 (next sequential instruction) while we wait.
- The branch target is not known until the **Reg Read / Compare** stage.
- So the PC only gets updated with the correct target address **after** that stage — potentially wasting several cycles.

---

### Pipeline With a Branch Predictor

```
PC --> IF (fetch branch) --> [stage] --> Reg Read / Compare / Compute Branch Target --> ...
       |         |                               |
       |    Branch Predictor                     | (verifies prediction, corrects if wrong)
       |         |
       +---------+  (PC is updated based on prediction immediately)
```

- A **Branch Predictor** sits alongside the fetch stage.
- As soon as the branch instruction is fetched, the predictor makes a guess and **immediately** updates the PC with the predicted target.
- By the time the actual branch outcome is computed, we have already fetched several instructions from the predicted path.
- If the prediction was **correct** — no penalty, no wasted cycles.
- If the prediction was **wrong** — we flush the wrongly-fetched instructions (penalty = branch misprediction cost).

---

### The Bimodal Predictor

This is the classic, simple branch predictor. Think of it as a table of "opinions" — one opinion per branch.

#### How it works:

1. You have a **table of 16K entries** (16,384 rows).
2. Each entry holds a **2-bit saturating counter**.
3. To look up the prediction for a branch, you use **14 bits of the Branch PC (Program Counter)** as the index into the table (2^14 = 16384 entries).
4. Based on the counter value, you predict taken or not taken.

#### What is a 2-bit Saturating Counter?

Think of it as a mood meter with 4 states:

```
Strongly Not Taken (00) <--> Weakly Not Taken (01) <--> Weakly Taken (10) <--> Strongly Taken (11)
```

- If the branch is **taken**: increment the counter (up to max 11 — "strongly taken")
- If the branch is **not taken**: decrement the counter (down to min 00 — "strongly not taken")
- It **saturates** — meaning it does not overflow or wrap around. 11 + 1 = still 11.

**Prediction rule:**
- Counter >= 2 (i.e., 10 or 11) → predict **Taken**
- Counter < 2 (i.e., 00 or 01) → predict **Not Taken**

**Analogy:** Imagine you have a friend who usually takes the highway to work. Even if one day they took a side road, you still predict "highway" next time because their habit is strong. They would need to deviate twice in a row before you change your prediction. That is the 2-bit counter — one outlier does not flip your prediction.

#### Why 2-bit instead of 1-bit?

With a 1-bit counter, a single misprediction flips the prediction immediately. Consider a loop that runs 99 times (taken) and then exits (not taken) — with 1-bit, you get 2 mispredictions per loop. With 2-bit, you only get 1 misprediction (on the exit) because the counter was "strongly taken" and needs two not-taken events to flip below the midpoint.

#### The 14-bit ID (Generalizing)

- You use 14 bits of the branch's PC address to index into the table.
- With 14 bits, you get 2^14 = 16,384 unique entries — enough to track many different branches.
- Different branch instructions at different addresses in the program map to different rows in the table.

#### Context Switch Problem

- When the OS switches between programs (a **context switch**), the branch predictor table still contains entries from the previous program.
- Those old entries can cause mispredictions for the new program until the predictor "warms up" again.
- This is a known weakness of the bimodal predictor.

#### Combination Branch Predictor

- A single predictor design may not be optimal for all types of branches.
- A **combination (hybrid) predictor** uses multiple predictor types and a selector that chooses which predictor's output to trust.
- Example: combine a bimodal predictor with a global history predictor — the selector learns which one is more accurate for each branch.

---

## Part 2: Out-of-Order Execution

### The Problem: Waiting Around for Slow Instructions

In a simple in-order pipeline, if instruction 3 is waiting for a slow memory load, instructions 4, 5, 6... all have to wait too — even if they have nothing to do with instruction 3. That is wasted time.

**Out-of-Order (OoO) Execution** solves this by letting instructions that are ready to go ahead and execute, even if earlier instructions are still waiting.

---

### Multicycle Instructions and Multiple Pipelines

Modern CPUs have **multiple parallel execution units**, each with a different number of stages:

| Unit | Purpose | Stages |
|---|---|---|
| Integer Unit (EX) | Simple add/subtract | 1 stage |
| FP/Integer Multiply | Multiply operations | 7 stages (M1–M7) |
| FP Adder | Floating-point add | 4 stages (A1–A4) |
| FP/Integer Divider | Division | Many stages (DIV) |

- Instructions that need multiplication take longer than simple adds.
- Since they take different amounts of time, **instructions can finish out of order**.
- The hardware must ensure that when two instructions both try to write to the same register, the write from the **logically later instruction** wins — not just the physically faster one.

---

### An Out-of-Order Processor: The Key Components

Here is the full picture of an OoO processor:

```
[Branch Prediction + Instruction Fetch]
           |
           v
   [Instruction Fetch Queue]   <-- holds fetched instructions
           |
           v
     [Decode & Rename]         <-- renames registers to avoid false dependencies
           |
           +--------------------> [Reorder Buffer (ROB)]  <-- tracks all in-flight instructions
           |
           v
     [Issue Queue (IQ)]        <-- waits until operands are ready, then fires instruction
           |
           v
    [ALU / ALU / ALU]          <-- multiple execution units running in parallel
           |
           v
   Results written to ROB, tags broadcast to IQ (to wake up waiting instructions)
           |
           v
   When instruction reaches head of ROB and is done --> write to [Register File R1-R32]
```

#### What is Register Renaming?

The **Decode & Rename** stage translates the original register names (R1, R2, R3...) into temporary names called **tags** (T1, T2, T3...).

**Why?** To eliminate false dependencies caused by reuse of register names.

**Example from the slides:**

Original code:
```
R1 <- R1 + R2    ; instruction 1
R2 <- R1 + R3    ; instruction 2
BEQZ R2          ; instruction 3 (branch)
R3 <- R1 + R2    ; instruction 4
R1 <- R3 + R2    ; instruction 5
```

After renaming:
```
T1 <- R1 + R2    ; instruction 1 (T1 is the new name for the result of instr 1)
T2 <- T1 + R3    ; instruction 2 (uses T1, not stale R1)
BEQZ T2          ; instruction 3
T4 <- T1 + T2    ; instruction 4
T5 <- T4 + T2    ; instruction 5
```

Each instruction's result gets a unique tag. Instructions now wait for specific tags, not architectural register names. This avoids **WAR (Write After Read)** and **WAW (Write After Write)** hazards.

#### What is the Reorder Buffer (ROB)?

- Every instruction that enters the pipeline gets a slot in the ROB.
- The ROB keeps instructions in their **original program order**.
- Instructions execute out of order (based on when their operands are ready), but they **commit** (write their final result to the register file) only when they reach the **head of the ROB** and are complete.
- This ensures the program appears to execute in order from the programmer's perspective.
- If a branch was mispredicted, you flush all instructions after the branch from the ROB.

#### What is the Issue Queue (IQ)?

- After decode/rename, instructions sit in the **Issue Queue** waiting for their source operands to become available.
- When an instruction completes in an ALU, it broadcasts its tag and result.
- Any instruction in the IQ that was waiting for that tag can now "wake up" and become ready to issue.
- This is called **tag broadcasting** or **wakeup and select**.

---

### Example: In-Order vs Out-of-Order Completion Times

From the slides:

```
Instruction         In-Order completion    OoO completion
ADD R1, R2, R3          5                      5
ADD R4, R1, R2          6                      6
LW  R5, 8(R4)           7                      7
ADD R7, R6, R5          9                      9
ADD R8, R7, R5         10                     10
LW  R9, 16(R4)         11                      7   <-- BIG WIN!
ADD R10, R6, R9        13                      9
ADD R11, R10, R9       14                     10
```

**What happened?**

- `LW R9, 16(R4)` only depends on R4, which was ready at time 6.
- In-order, it had to wait for everything above it (including `ADD R7`, `ADD R8`) to finish, so it started late and finished at time 11.
- Out-of-order, it could start as soon as R4 was ready (time 6) and finish at time 7.
- This allowed `ADD R10` and `ADD R11` to also finish earlier.
- **Total saving: 4 cycles** for the last instruction (14 vs 10).

**Analogy:** Imagine a checkout queue at a supermarket. In-order means everyone must wait their turn even if the person in front has 100 items and you only have 1. Out-of-order is like having multiple checkout lanes — you find a free lane and go, regardless of who arrived before you. The store (CPU) still bills you in the right order, but the actual work happens in parallel.

---

## Part 3: Cache Basics

### Why Not Just Use RAM for Everything?

**DRAM (Dynamic RAM)** — the main memory chips — can store lots of data (gigabytes) but is **slow**: accessing data from DRAM can take up to **300 cycles**.

**SRAM (Static RAM)** — used in caches — is much faster but holds far less data and is more expensive per bit.

**Analogy:** DRAM is like your library (huge but slow to access). SRAM cache is like your desk (small but instant access). You keep the books you are currently using on your desk.

---

### The Memory Hierarchy

The key rule: **as you go further from the CPU, capacity goes up but speed goes down.**

```
Registers  -->  L1 Cache  -->  L2 Cache  -->  Main Memory (DRAM)  -->  Disk
  1 KB            32 KB          2 MB              16 GB               1 TB
  1 cycle         2 cycles      15 cycles          300 cycles         10M cycles
  (fastest)                                                            (slowest)
```

- **Registers**: Directly inside the CPU. Tiny but blazing fast. 1 cycle access.
- **L1 Cache**: On the chip, very close to the CPU core. Split into instruction cache and data cache. 2 cycles.
- **L2 Cache**: Still on the chip (usually). Larger than L1 but slower. 15 cycles.
- **Main Memory**: DRAM off the chip. Huge but 300 cycles.
- **Disk**: Enormous storage but outrageously slow. Used for persistent data.

---

### Why Do Caches Work? Locality!

Caches would be useless if programs accessed memory in a totally random pattern. They work because programs exhibit **locality** — a tendency to access the same or nearby memory repeatedly.

#### Temporal Locality
- "If you used some data recently, you will likely use it again soon."
- Example: a variable in a loop — you access it on every iteration.
- The cache keeps recently-used data, so the next access is a fast cache hit.

#### Spatial Locality
- "If you used some data recently, you will likely access nearby data soon."
- Example: an array — when you access element `a[0]`, you will soon access `a[1]`, `a[2]`, etc.
- Caches load data in **blocks** (cache lines), not just single bytes, to exploit this.

---

### Cache Performance Formula

**Average Memory Access Time (AMAT):**

```
AMAT = (hit rate × hit time) + (miss rate × (hit time + miss penalty))
```

Or simplified (where miss penalty includes the time to go to main memory):

```
AMAT = hit rate × L1 time + miss rate × (L1 time + memory time)
```

**Example from the slides:**

- No cache: AMAT = **300 cycles** (every access goes to DRAM)
- With a 32KB L1 cache (1 cycle), 95% hit rate:
  - AMAT = 0.95 × 1 + 0.05 × (1 + 300)
  - AMAT = 0.95 + 0.05 × 301
  - AMAT = 0.95 + 15.05
  - AMAT = **~16 cycles**

That is nearly a **19x speedup** just from adding a small, fast cache. Huge win!

**Breaking it down:**
- 95% of the time: data is in the cache, costs 1 cycle.
- 5% of the time: miss, must go to memory. Costs 1 (check cache) + 300 (go to DRAM) = 301 cycles.
- Weighted average = 16 cycles.

---

## Revision Checklist

### Branch Predictors
- [ ] I can explain what a control hazard is and why it happens in a pipeline
- [ ] I know all four techniques to handle control hazards: stall, assume-not-taken, branch delay slot, and branch prediction
- [ ] I understand how the pipeline differs with and without a branch predictor
- [ ] I can describe the structure of a bimodal predictor (14-bit PC index, 16K entries, 2-bit saturating counters)
- [ ] I can draw and explain the 2-bit saturating counter state machine and its 4 states
- [ ] I know why 2-bit counters are better than 1-bit counters for loop branches
- [ ] I understand what a context switch is and why it can hurt bimodal predictor accuracy
- [ ] I know what a combination/hybrid branch predictor is

### Out-of-Order Execution
- [ ] I understand why multicycle instructions cause out-of-order completion
- [ ] I know the different execution units (integer, FP multiply, FP adder, divider) and that they have different numbers of stages
- [ ] I can name and describe the key components of an OoO processor: Instruction Fetch Queue, Decode & Rename, Reorder Buffer (ROB), Issue Queue (IQ), ALUs
- [ ] I understand register renaming: what it is, why we do it, and how tags (T1, T2, ...) replace architectural register names
- [ ] I understand the role of the Reorder Buffer (ROB): in-order commit even with out-of-order execution
- [ ] I understand the Issue Queue (IQ): instructions wait here until operands are ready
- [ ] I understand tag broadcasting: when an ALU finishes, it broadcasts the result to wake up waiting IQ entries
- [ ] I can work through the example code and explain why `LW R9, 16(R4)` completes at cycle 7 instead of 11 in OoO execution

### Cache Basics
- [ ] I know the difference between DRAM (slow, high capacity) and SRAM (fast, low capacity)
- [ ] I can list the memory hierarchy levels in order: Registers, L1, L2, DRAM, Disk — with approximate sizes and latencies
- [ ] I understand temporal locality (reuse of recently accessed data) and can give an example
- [ ] I understand spatial locality (access to nearby data) and can give an example
- [ ] I can apply the AMAT formula: AMAT = hit_rate × hit_time + miss_rate × (hit_time + miss_penalty)
- [ ] I can work through the example: 95% hit rate, 1-cycle L1, 300-cycle memory → AMAT = 16 cycles
- [ ] I understand why adding even a small cache gives a huge speedup (the 19x example)
