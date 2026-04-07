# Week 6 – Pipelining Hazards

---

## 1. The 5-Stage Pipeline – Quick Recap

Before diving into hazards, remember the 5 stages every instruction passes through:

| Stage | Name | What it does |
|-------|------|--------------|
| 1 | **IF** – Instruction Fetch | Grabs the instruction from memory |
| 2 | **D/R** – Decode / Register Read | Figures out what the instruction means and reads the input registers |
| 3 | **ALU** – Execute | Does the actual arithmetic/logic (or computes a memory address) |
| 4 | **DM** – Data Memory | Reads from or writes to memory (only load/store need this) |
| 5 | **RW** – Register Write | Writes the result back into a register |

**Analogy:** Think of a car wash with 5 stations (rinse, soap, scrub, wax, dry). Once one car moves from rinse to soap, a new car can start rinsing. That is pipelining — multiple instructions overlapping in different stages.

The pipeline lets you start a new instruction every cycle. Without it, each instruction would have to wait for the previous one to fully finish.

---

## 2. What is a Hazard?

A **hazard** is anything that prevents the next instruction from starting (or continuing) in the very next clock cycle. Hazards create wasted cycles — called **pipeline stalls** or **bubbles** — where a stage sits doing nothing useful.

There are **three types**:

1. **Structural Hazard** — two instructions want to use the same piece of hardware at the same time
2. **Data Hazard** — an instruction needs a value that an earlier instruction hasn't finished computing yet
3. **Control Hazard** — the processor doesn't know which instruction to fetch next because a branch hasn't been resolved yet

---

## 3. Structural Hazards

### What is it?

Two instructions in different stages both need the same resource in the same clock cycle, but there is only one copy of that resource.

**Classic example:** A single unified cache for both instructions AND data.
- Stage 1 (IF) needs to read an instruction from the cache.
- Stage 4 (DM) needs to read/write data from the same cache.
- Both cannot happen simultaneously — they clash!

So stage 1 and stage 4 can **never be active at the same time** on the same cache.

### What happens?

The instruction in stage 1 (or the instruction trying to enter stage 1) is **stalled** — it and everything behind it are delayed. These empty, wasted slots in the pipeline are called **pipeline bubbles**.

**Analogy:** Two people trying to walk through the same door at the same time. One has to wait outside until the other gets through.

### How to fix it?

Simple — add more hardware so there is no conflict:
- Use **separate instruction cache and data cache** (split cache). Now IF and DM can both run simultaneously.
- Add **more register file ports** so multiple instructions can read registers at the same time.

Structural hazards are the easiest to fix — just throw hardware at the problem.

---

## 4. Data Hazards

### What is it?

One instruction **produces** (writes) a value in a later pipeline stage. A subsequent instruction **consumes** (reads) that value in an earlier pipeline stage. If the consumer runs before the producer has finished, it reads a stale (wrong) value.

**Analogy:** You ask your friend to compute something, and before they finish you grab what they wrote — but they haven't written it yet, so you read garbage.

The rule is:
> The **time of consumption** must be **after** the time of production.

If it isn't, you must **stall** the consumer instruction until the value is ready.

### Two approaches: No Bypassing vs Bypassing

#### No Bypassing (stall and wait)

Without any special hardware, the processor must wait until the result has been written all the way back to the register file (RW stage) before the next instruction can read it in D/R.

#### Bypassing (forwarding)

With bypassing, you add extra wires/multiplexers that "forward" the result directly from wherever it is in the pipeline (e.g., right after the ALU stage) to wherever it is needed (e.g., the input of the ALU for the next instruction). This eliminates or reduces stalls.

---

## 5. Worked Example 1 – No Bypassing

**Instructions:**
```
I1: R1 + R2 -> R3       (produces R3)
I2: R3 + R4 -> R5       (consumes R3 — depends on I1)
I3: R7 + R8 -> R9       (no dependency)
```

**The problem:** I2 needs R3, which I1 writes in the RW (register write) stage. Without bypassing, I2 can only read R3 during its D/R stage, but only AFTER I1 has completed RW.

**Pipeline diagram (No Bypassing):**

```
         CYC-1  CYC-2  CYC-3  CYC-4  CYC-5  CYC-6  CYC-7  CYC-8

I1:        IF    D/R    ALU     DM     RW
I2:              IF    D/R    D/R    D/R    ALU     DM     RW
                        (stall)(stall)
I3:                     IF     IF     IF    D/R    ALU     DM ...
```

- I2 is fetched in cycle 2 but cannot decode/read registers until R3 is ready.
- I1 writes R3 at the END of cycle 5 (RW stage).
- I2 can read R3 at the START of cycle 6 (D/R stage reads what RW wrote).
- So I2 must stall in D/R for **2 extra cycles** (cycles 3 and 4), then execute in cycle 5–6 onwards.
- I3 also stalls because I2 is stalled in front of it (like a traffic jam).
- Total penalty: **2 stall cycles** inserted (bubbles in the ALU, DM stages).

**Key insight:** Without bypassing, between two back-to-back dependent ALU instructions, you need 2 stall cycles (wait for RW to complete, then D/R can read).

---

## 6. Worked Example 2 – With Bypassing

**Instructions:**
```
I1: R1 + R2 -> R3       (produces R3)
I2: R3 + R4 -> R5       (consumes R3 — depends on I1)
I3: R3 + R8 -> R9       (also consumes R3 — depends on I1)
```

With bypassing, as soon as the ALU produces a result, it can be forwarded directly to the next instruction's ALU input — no waiting for the value to be written to the register file and read back.

**Pipeline diagram (With Bypassing):**

```
         CYC-1  CYC-2  CYC-3  CYC-4  CYC-5  CYC-6  CYC-7

I1:        IF    D/R    ALU     DM     RW
I2:              IF    D/R    ALU     DM     RW
I3:                     IF    D/R    ALU     DM     RW
```

- **No stalls at all!** Instructions flow through one per cycle.
- I2 needs R3 in its ALU stage (cycle 4). I1 produced R3 at the END of its ALU stage (cycle 3). With bypassing, the result is forwarded from **I1's ALU output latch (L3)** directly into I2's ALU input.
- I3 also needs R3. By the time I3 hits ALU (cycle 5), I1 is in DM stage. The result is forwarded from **I1's DM input latch (L4)**.

**Input latches (where the bypassed value comes from):**

The pipeline has latches between each stage. They are labelled by the stage they sit after:
- **L3** = latch after ALU (holds ALU result)
- **L4** = latch after DM (holds result going to RW)
- **L5** = latch after RW (holds final written value)

For I2's operand R3: forwarded from **L3** (I1 just finished ALU, result is in L3).
For I3's operand R3: forwarded from **L4** (I1 has now moved to DM, result is in L4).

---

## 7. Problem 0 – Detailed Worked Example

```
add $1, $2, $3      # writes $1
add $5, $1, $4      # reads $1 (depends on above)
```

**Without bypassing:**
```
add $1, $2, $3:   IF   DR   AL   DM   RW
add $5, $1, $4:        IF   DR   DR   DR   AL   DM   RW
                                 ^--- stalls here (2 extra DR cycles)
```
- Point of **Production** = end of RW stage of instruction 1
- Point of **Consumption** = D/R stage of instruction 2
- Without bypassing, $1 is only ready after RW (cycle 5). Instruction 2 reads it in D/R. It must wait until cycle 6 to read D/R. So it stalls 2 cycles in the DR stage.

**With bypassing:**
```
add $1, $2, $3:   IF   DR   AL   DM   RW
add $5, $1, $4:        IF   DR   AL   DM   RW
                                 ^--- value forwarded from AL output of instr 1
```
- Point of **Production** = end of ALU stage of instruction 1 (cycle 3)
- Point of **Consumption** = ALU stage of instruction 2 (cycle 4)
- Bypassing forward the result from the ALU output latch to the ALU input of the next instruction. **Zero stalls.**

---

## 8. Problem 1 – add then lw

```
add $1, $2, $3      # writes $1
lw  $4, 8($1)       # reads $1 as base address
```

**With bypassing, how many stalls?**

```
add $1, $2, $3:   IF   D/R   ALU   DM   RW
lw  $4, 8($1):         IF    D/R   ALU  DM   RW
```

- `lw` needs $1 to compute the address, which is used in its **ALU** stage.
- `add` produces $1 at the end of its **ALU** stage.
- These two ALU stages are **back-to-back** (one cycle apart).
- With bypassing, the result from `add`'s ALU output is forwarded directly into `lw`'s ALU input.
- **Result: 0 stalls with bypassing.**

The diagram shows 4 rows of pipeline stages because 4 instructions are in flight simultaneously, and both `add` and `lw` flow cleanly without stalling.

---

## 9. Problem 2 – lw then lw (load-use hazard)

```
lw $1, 8($2)        # loads a value from memory into $1
lw $4, 8($1)        # uses $1 as a base address
```

This is called a **load-use hazard** — one of the nastiest data hazards!

**Why is it different from add-then-lw?**

With `add`, the result is available at the END of the ALU stage. You can bypass it to the next instruction's ALU.

With `lw`, the result is only available at the END of the **DM (Data Memory)** stage — because you first have to compute the address (ALU), then actually go read memory (DM).

```
lw $1, 8($2):    IF   D/R   ALU   DM   RW
lw $4, 8($1):         IF    D/R   ALU  DM   RW
                                   ^--- needs $1 here
                                   but $1 only ready after DM above
```

- The second `lw` needs $1 for its **ALU** stage (cycle 4 if no stalls).
- The first `lw` produces $1 at the end of its **DM** stage (also cycle 4 if no stalls).
- These happen **at the same time** — you can't bypass a value that isn't ready yet!
- **Result: 1 mandatory stall cycle, even with bypassing.**

The diagram shows 4 rows of pipeline stages — the second `lw` must be pushed back one cycle, creating a bubble.

**Analogy:** You asked a friend to look up a word in a dictionary (takes time), then immediately ask them to use that word in a sentence. They can't — they haven't found it yet. You have to wait one moment.

---

## 10. Problem 3 – lw then sw

```
lw  $1, 8($2)       # loads value into $1
sw  $1, 8($3)       # stores $1 to memory
```

- `sw` needs $1 to **store** it to memory. It uses $1 in the **DM** stage (as the data to write).
- `lw` produces $1 at the end of its **DM** stage.

Timing:
```
lw $1, 8($2):    IF   D/R   ALU   DM   RW
sw $1, 8($3):         IF    D/R   ALU  DM   RW
```

- `lw` finishes DM in cycle 4 (produces $1).
- `sw` needs $1 in its DM stage = cycle 5.
- **Result: 0 stalls with bypassing!** The result from `lw`'s DM stage output can be forwarded to `sw`'s DM stage input (one cycle later). The forwarding path works here.

The diagram also shows 4 simultaneous instructions flowing cleanly.

---

## 11. Problem 4 – Longer Pipeline (7 or 9 stages)

Some CPUs have longer pipelines where stages like Register Read (RR) and Register Write (RW) each take a full stage of their own. The pipeline might look like:

```
IF | IF | Dec | Dec | RR | ALU | RW        (for add/ALU ops)
IF | IF | Dec | Dec | RR | ALU | DM | DM | RW   (for load/store)
```

**Example:**
```
lw  $1, 8($2)        # loads into $1
add $4, $1, $3       # uses $1
```

In a 7/9-stage pipeline, the gap between production and consumption is larger. You need to count more carefully:
- `lw` produces $1 at the end of its second DM stage.
- `add` needs $1 at its RR stage or ALU stage.
- Depending on the exact pipeline design, more stall cycles may be needed because the forwarding paths span more stages.

**Key takeaway:** The deeper the pipeline, the more potential stall cycles for a load-use hazard, unless forwarding paths are extended across more stages.

---

## 12. Control Hazards

### What is it?

When the processor hits a **branch instruction** (like "if X then jump to Y"), it doesn't know which instruction to fetch next until the branch outcome is resolved. Meanwhile, the pipeline keeps fetching — potentially fetching the wrong instructions!

**Analogy:** You're driving and come to a split road. You don't know which way to turn yet, but you have to keep driving. You might go down the wrong road for a few seconds before realising and turning back.

**Important fact from the slides:** On average, **every 6th instruction is a branch**. So control hazards happen very frequently. This makes them a major performance concern.

### Four techniques to handle control hazards

#### Technique 1: Stall every time (always wait)

- Whenever you see a branch, freeze the pipeline and do nothing until you know the outcome.
- Simple, safe, but **wastes 1+ cycle for every branch**.
- Given branches every 6 instructions, this is a significant slowdown.

#### Technique 2: Predict not-taken

- Assume the branch is NOT taken and keep fetching the instructions that come after the branch sequentially.
- If you were right (branch not taken), great — no wasted cycles.
- If you were wrong (branch WAS taken), you need hardware to **cancel/flush** the wrong instructions already in the pipeline (turn them into bubbles).
- Works well when branches are mostly not taken (e.g., in the last iteration of a loop).

#### Technique 3: Branch Delay Slot

- Always execute the instruction that comes immediately AFTER the branch, regardless of which way the branch goes. This instruction slot is the **branch delay slot**.
- The compiler/programmer fills this slot with a useful instruction that should run no matter what (ideally one that was going to run before the branch anyway).
- If the slot can be filled with useful work, you get a "free" instruction even while waiting for the branch to resolve.
- If no useful instruction exists, the slot is filled with a NOP (do nothing).
- If the branch was wrong and the slot instruction was on the wrong path, the processor must ensure it doesn't damage program state.

**Two strategies for filling the delay slot (from slides):**

**a. From before ("from before" strategy):**
```
BEFORE:                         AFTER:
  add $s1, $s2, $s3               if $s2 = 0 then [branch target]
  if $s2 = 0 then ...    -->        add $s1, $s2, $s3    <-- delay slot
  [delay slot]
```
Move an instruction from BEFORE the branch into the delay slot. Safe because that instruction runs regardless of branch outcome — it was always going to execute.

**b. From target ("from target" strategy):**
```
BEFORE:                         AFTER:
  sub $t4, $t5, $t6               add $s1, $s2, $s3
  ...                             if $s1 = 0 then [branch target]
  add $s1, $s2, $s3    -->          sub $t4, $t5, $t6   <-- delay slot
  if $s1 = 0 then ...
```
Take the first instruction AT the branch target and put it in the delay slot. The branch target instruction now runs one cycle earlier (in the delay slot). Only safe if the branch is **usually taken** (otherwise you run a target instruction when you shouldn't).

#### Technique 4: Branch Prediction

- Use smarter guessing hardware (a **branch predictor**) to predict whether the branch will be taken or not, and start fetching from the predicted path.
- Modern CPUs use very sophisticated predictors (like tournament predictors, TAGE predictors) with >95% accuracy.
- If the prediction is correct: no wasted cycles.
- If wrong: flush the wrongly-fetched instructions (mis-prediction penalty).

---

## 13. Key Formulas and Rules of Thumb

### Stall cycles without bypassing
For an ALU instruction followed immediately by a dependent ALU instruction:
```
Stall cycles = (stage of production) - (stage of consumption)
             = RW stage - D/R stage
             = 5 - 2 = 3... but adjusted for overlap = 2 stall cycles
```
**Rule:** Back-to-back dependent ALU instructions need **2 stall cycles** without bypassing.

### Stall cycles with bypassing
- **ALU -> ALU (back-to-back):** 0 stall cycles (forward from ALU output to ALU input)
- **LW -> ALU (back-to-back):** 1 stall cycle (load-use hazard — unavoidable)
- **LW -> SW (back-to-back):** 0 stall cycles (can forward from DM output to DM input)

### Branch penalty
- Without any mitigation: **1 stall per branch** minimum (on a simple 5-stage pipeline)
- Branches occur roughly **every 6 instructions**
- So branch overhead ≈ 1/6 ≈ ~17% of cycles lost just to branches

### CPI impact formula (general idea)
```
Actual CPI = Ideal CPI + Stalls per instruction
           = 1 + (stalls from data hazards) + (stalls from control hazards)
```
(Structural hazards are usually designed away, so they rarely appear in CPI calculations.)

---

## 14. Summary Table

| Hazard Type | Cause | Fix |
|-------------|-------|-----|
| Structural | Two instructions need the same hardware simultaneously | Add more hardware (split caches, more register ports) |
| Data (RAW) | Instruction needs a value not yet computed | Stall + bubble, or use bypassing/forwarding |
| Load-use | Load followed immediately by an instruction that uses the loaded value | 1 mandatory stall cycle even with bypassing |
| Control | Branch outcome not yet known | Stall, predict not-taken, delay slots, or branch prediction |

**RAW = Read After Write** (the most common type of data hazard — you try to read a register before the previous instruction has finished writing it)

---

## 15. Revision Checklist

- [ ] I can name and explain all 5 stages of the standard pipeline (IF, D/R, ALU, DM, RW)
- [ ] I can define a structural hazard and give the unified cache example
- [ ] I know that structural hazards are fixed by adding more hardware resources
- [ ] I can define a data hazard and explain the producer/consumer relationship
- [ ] I can draw a pipeline diagram for dependent instructions without bypassing, showing stall cycles
- [ ] I can draw a pipeline diagram for dependent instructions with bypassing, showing no stalls
- [ ] I understand what bypassing (forwarding) is and how it works
- [ ] I can identify which pipeline latch a forwarded value comes from (L3, L4, L5)
- [ ] I can work through Problem 0 (add -> add, with and without bypassing)
- [ ] I can work through Problem 1 (add -> lw) and explain why 0 stalls occur
- [ ] I can explain what a load-use hazard is and why it always needs 1 stall cycle
- [ ] I can work through Problem 2 (lw -> lw) and identify the 1 mandatory stall
- [ ] I can work through Problem 3 (lw -> sw) and explain why 0 stalls occur with bypassing
- [ ] I understand how deeper pipelines (Problem 4) affect the number of stall cycles
- [ ] I can define a control hazard and explain why it matters (branches every ~6 instructions)
- [ ] I know all 4 techniques for handling control hazards: stall, predict-not-taken, delay slot, branch prediction
- [ ] I can explain what a branch delay slot is and how it is filled
- [ ] I can show the "fill from before" strategy for branch delay slots with an example
- [ ] I can show the "fill from target" strategy for branch delay slots with an example
- [ ] I understand when fill-from-target is safe (only when branch is usually taken)
- [ ] I can calculate approximate CPI impact from data and control hazards
