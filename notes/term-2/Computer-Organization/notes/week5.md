# Week 5: Von Neumann Architecture, Single/Multi-Cycle Design & Basic Pipelining

---

## Part 1: Von Neumann Architecture

### What Is It?

Published by John von Neumann in **1945**, this is the blueprint that almost every modern computer follows.

The big idea: **store both the program instructions AND the data in the same memory**. The CPU reads instructions from that memory, one at a time, and executes them.

**Analogy:** Think of it like a recipe book (program) sitting on the same kitchen shelf as the ingredients (data). The chef (CPU) reads the recipe and uses the ingredients from the same place.

---

### Stored Program vs Fixed Program Computers

| Type | What it means | Example |
|---|---|---|
| **Stored Program** | Instructions and data live in the same memory; the program can be changed | Modern computers, laptops, phones |
| **Fixed Program** | Hard-wired to do one thing; cannot be reprogrammed | Old calculators |

---

### The Five Components of Von Neumann Architecture

```
Input Device --> [Central Processing Unit] --> Output Device
                   |  Control Unit        |
                   |  ALU                 |
                   |  Registers (PC, CIR, |
                   |   AC, MAR, MDR)      |
                        |
                   [Memory Unit (RAM)]
```

1. **Control Unit (CU)**
2. **Arithmetic and Logic Unit (ALU)**
3. **Registers**
4. **Memory Unit**
5. **Input/Output devices**

---

### Central Processing Unit (CPU)

- The electronic circuit that actually **runs your program**
- Also called the **microprocessor** or **processor**
- Contains: ALU + Control Unit + Registers

**Analogy:** The CPU is the brain of the computer. Everything has to go through it.

---

### Control Unit (CU)

- Acts like a **manager/coordinator**
- Reads instructions from memory, figures out what they mean, then tells the ALU, memory, and I/O devices what to do
- Also sends **timing and control signals** to keep everything in sync

**Analogy:** The CU is like a conductor in an orchestra — it doesn't play any instrument itself, but it tells every section when to play and how.

---

### Arithmetic and Logic Unit (ALU)

- Does all the **actual computation**
- **Arithmetic operations:** add, subtract, multiply, divide
- **Logic operations:** AND, OR, NOT, comparisons

**Analogy:** The ALU is the calculator inside the CPU.

---

### Registers

Registers are **tiny, ultra-fast storage slots** inside the CPU. Before the CPU can process any data, that data must first be loaded into a register.

**Analogy:** Registers are like your hands — you can only work with what you're currently holding. RAM is like the table in front of you.

| Register | Full Name | What it holds |
|---|---|---|
| **MAR** | Memory Address Register | The **address** (location) in memory where data needs to be read from or written to |
| **MDR** | Memory Data Register | The actual **data** being moved to or from memory |
| **AC** | Accumulator | Holds **intermediate results** from the ALU (like a running total) |
| **PC** | Program Counter | Holds the **address of the NEXT instruction** to execute |
| **CIR** | Current Instruction Register | Holds the **current instruction** being decoded and executed |

---

### Buses

Buses are the **wires/pathways** that carry data between parts of the computer. Think of them like roads connecting different buildings in a city.

A standard CPU system has **three buses**:

| Bus | What it carries | Direction |
|---|---|---|
| **Address Bus** | Memory addresses (where to look), NOT actual data | One-way: CPU to memory |
| **Data Bus** | The actual data being transferred | Two-way: between CPU, memory, and I/O |
| **Control Bus** | Control signals and commands from the CPU; status signals from devices | Both ways |

**Analogy:**
- Address bus = the street address you write on an envelope
- Data bus = the letter inside the envelope
- Control bus = the postal instructions (fragile, priority, return receipt)

---

### Memory Unit

- The memory unit is **RAM** (Random Access Memory) — this is primary/main memory
- RAM is **fast** and **directly accessible** by the CPU (unlike a hard drive which is slow)
- RAM is split into **partitions (cells)**. Each cell has:
  - An **address** (like a house number, in binary)
  - **Contents** (the data stored there, also in binary)
- Every location in memory has a **unique address**

**Why not just use the hard drive?**
The hard drive is permanent storage but very slow. When you open a program, it gets loaded from the hard drive into RAM so the CPU can access it quickly.

**Analogy:** RAM is your desk workspace. The hard drive is a filing cabinet across the room. You bring files from the cabinet to your desk to work on them faster.

---

## Part 2: Amdahl's Law

### The Core Idea

Computer architecture is all about finding and fixing **bottlenecks**. The rule is:
> **Make the common case fast.** Don't waste resources on something that barely affects overall performance.

### Amdahl's Law (The Formula Concept)

> Performance improvements from an enhancement are **limited by the fraction of time** that enhancement is actually being used.

In plain English: if only part of your program benefits from an upgrade, you can only speed up that part — the rest stays the same.

**Formula for Speedup:**

```
Speedup = 1 / [(1 - fraction_enhanced) + (fraction_enhanced / speedup_of_part)]
```

Where:
- `fraction_enhanced` = the fraction of time the improved part is used
- `speedup_of_part` = how much faster that part now runs

### Worked Example from the Slides

**Scenario:** A web server spends:
- 40% of time in the CPU
- 60% of time doing I/O

A new processor is **10x faster**. What is the overall speedup?

**Applying the formula:**
```
Speedup = 1 / [(1 - 0.40) + (0.40 / 10)]
        = 1 / [0.60 + 0.04]
        = 1 / 0.64
        = 1.5625  (~1.56)
```

So execution time drops by about **36%**, giving a speedup of **1.56**.

**What is the MAXIMUM possible speedup** (if the CPU was infinitely fast)?
```
Max speedup = 1 / (1 - 0.40) = 1 / 0.60 = 1.66
```

So no matter how fast you make the CPU, the maximum speedup is **1.66** because 60% of the time is spent on I/O which you didn't improve.

**Key takeaway:** There's always a ceiling on how much improvement you can get from speeding up just one part of a system.

---

## Part 3: Common Principles in Architecture Design

1. **Amdahl's Law** — Speedup is limited by the unimproved fraction
2. **Energy leakage** — Systems consume energy even when idle (just sitting there doing nothing)
3. **Performance and energy are linked** — Faster, more efficient systems usually also use less energy (less leakage time)
4. **90-10 Rule** — 10% of the code accounts for 90% of the execution time. Focus your optimisations on that 10%.
5. **Principle of Locality** — Programs tend to reuse the same data/code:
   - **Temporal locality:** If you used something recently, you'll probably use it again soon (e.g., a loop variable)
   - **Spatial locality:** If you accessed one memory location, you'll probably access nearby locations soon (e.g., reading an array)

**Why does locality matter?** It's the reason **caches** work so well — the cache holds recently/nearby used data so the CPU doesn't have to go all the way to RAM every time.

---

## Part 4: Single-Cycle and Multi-Cycle Design

### Clocks

A microprocessor has many circuits all running at the same time. To keep them coordinated, they all share a **clock signal** — a repeating square wave (like a heartbeat).

```
Clock signal:
   ___   ___   ___   ___
  |   | |   | |   | |   |
__|   |_|   |_|   |_|   |__
```

The clock tells every circuit:
- **When** to accept new inputs (rising edge)
- **How long** they have to do their work (one clock period)
- **When** they must produce their output (next rising/falling edge)

**Analogy:** The clock is like a starter pistol at a relay race — every runner (circuit) knows exactly when to start and when to hand off the baton.

---

### Combinational vs Sequential Circuits

**Combinational circuit:** Output changes whenever input changes (after a short delay). No memory of past states.

```
Inputs ---> [Combinational Circuit] ---> Outputs
```

**Problem:** In a CPU with many chained circuits, outputs from one circuit become inputs to the next. Without control, things can go haywire mid-cycle.

**Solution: Latches**

A **latch** is a storage device placed between circuits. It holds the value steady and only updates when the clock tells it to.

```
           Clock                    Clock
             |                        |
Inputs --> [Latch] --> [Circuit] --> [Latch] --> [Circuit] --> ...
```

This creates a **sequential circuit** — the behaviour depends on the clock, not just the current inputs. Data flows through one stage per clock cycle, in an orderly way.

---

### Basic MIPS Architecture

We design a simple CPU to execute these instruction types:

```
Basic math:       add, sub, and, or, slt
Memory access:    lw (load word), sw (store word)
Control flow:     beq (branch if equal), j (jump)
```

**What every instruction needs:**
1. Use the **Program Counter (PC)** to fetch the next instruction from instruction memory
2. **Read register values** needed by the instruction

---

### Single-Cycle Design

In a single-cycle design, the **entire instruction executes in one clock cycle**.

The pipeline of components looks like this:

```
PC --> [Instr Memory] --> [Reg File] --> [ALU] --> [Addr] --> [Data Memory]
 ^(rising edge)             ^(rising edge)          ^(falling edge)
```

- **Green blocks (latches):** PC, Register File, Address register
- **At the rising edge:** New PC is recorded; result from previous cycle is stored in register file
- **At the falling edge:** Address for Load/Store is recorded so data memory can be accessed in the second half of the cycle

**Problem with single-cycle:** The clock period must be long enough for the **slowest possible instruction** (e.g., a load word that goes through every stage). Simpler instructions like `add` have to wait just as long — wasteful.

---

### Multi-Stage (Multi-Cycle) Design

Instead of one big stage, break the instruction execution into **multiple smaller stages**, each separated by a latch.

```
PC --> [Instr Mem] --> L2 --> [Reg File] --> L3 --> [ALU] --> L4 --> [Data Mem] --> L5
                              [Reg File] <-----------------------------------------(feedback)
```

- Each stage takes **one clock cycle**
- Stages are separated by **latches (L2, L3, L4, L5)**
- The result from the last stage (Data Memory / L5) feeds back into the Register File for write-back

**Advantage:** Each stage can now have a shorter clock period (tuned to the slowest *stage*, not the slowest *instruction*).

---

## Part 5: Pipelining

### The Assembly Line Analogy

Imagine building cars. You could:

**Unpipelined (sequential):**
- Build car 1 completely (A→B→C), then start car 2
- One car finishes at a time
- Very slow overall throughput

**Pipelined:**
- While car 1 is in stage B, start car 2 in stage A
- While car 1 is in stage C, car 2 is in B, car 3 starts in A
- Much higher throughput — many cars moving simultaneously

```
Unpipelined:
Job 1:  [  A  ][  B  ][  C  ]
Job 2:                        [  A  ][  B  ][  C  ]
Job 3:                                             [  A  ][  B  ][  C  ]

Pipelined:
Job 1:  [  A  ][  B  ][  C  ]
Job 2:         [  A  ][  B  ][  C  ]
Job 3:                [  A  ][  B  ][  C  ]
Job 4:                       [  A  ][  B  ][  C  ]
```

The key insight: **each individual job takes the same time**, but you finish many more jobs per unit time.

---

### Quantitative Effects of Pipelining

| Metric | Effect of pipelining |
|---|---|
| Time per instruction (ns) | Goes **UP** (more stages = more overhead per instruction) |
| Cycles per instruction (CPI) | Stays **roughly the same** on average |
| Clock speed | Goes **UP** (shorter cycle time per stage) |
| Total execution time | Goes **DOWN** |
| Average time per instruction | Goes **DOWN** (more instructions complete per second) |

**Speedup formula (ideal conditions):**

```
Speedup = Number of pipeline stages = Increase in clock speed
```

So a 5-stage pipeline ideally gives a **5x speedup** over a single-cycle design.

**Important caveats:** This is the *ideal* case assuming no stalls or hazards. Real-world speedup is less due to hazards (covered below).

---

### The Classic 5-Stage MIPS Pipeline

The standard 5-stage pipeline used in MIPS processors:

```
Stage 1: IF  - Instruction Fetch
Stage 2: RR  - Register Read (also called ID - Instruction Decode)
Stage 3: ALU - Execute (ALU operation or address calculation)
Stage 4: DM  - Data Memory access
Stage 5: RW  - Register Write-back
```

**What happens in each stage:**

| Stage | Full Name | What happens |
|---|---|---|
| **IF** | Instruction Fetch | Use the PC to read the instruction from the instruction cache (I-cache); increment PC by 4 |
| **RR** | Register Read | Read the required register values; for branches: compare registers and compute branch target address |
| **ALU** | Execute | Run the ALU operation (e.g., addition); for load/store: compute the effective memory address |
| **DM** | Data Memory | For loads: read data from data cache; for stores: write data to data cache; stores finish here (4 cycles total) |
| **RW** | Register Write | Write the result (from ALU or from a load) back into the register file |

**Visualising the 5-stage pipeline over time (clock cycles CC1 to CC6):**

```
         CC1   CC2   CC3   CC4   CC5   CC6
Instr 1:  IF    RR   ALU    DM    RW
Instr 2:        IF    RR   ALU    DM    RW
Instr 3:              IF    RR   ALU    DM
Instr 4:                    IF    RR   ALU
Instr 5:                          IF    RR
```

Every clock cycle, a new instruction enters the pipeline. At steady state, **5 instructions are in flight simultaneously**.

---

### Pipeline Summary Table (What Each Instruction Does Per Stage)

| Instruction | RR (Read Regs) | ALU (Execute) | DM (Memory) | RW (Write Back) |
|---|---|---|---|---|
| `ADD R1, R2 -> R3` | Read R1, R2 | Compute R1+R2 | -- (no memory) | Write result to R3 |
| `BEQ R1, R2, 100` | Read R1, R2; Compare; Set PC | -- | -- | -- |
| `LD 8[R3] -> R6` | Read R3 | Compute R3+8 (address) | Get data from memory | Write data to R6 |
| `ST 8[R3] <- R6` | Read R3 and R6 | Compute R3+8 (address) | Write R6 to memory | -- (nothing to write back) |

**Note:** BEQ (branch if equal) is handled in the RR stage — it compares registers and sets the PC early to minimise disruption.

---

### Conflicts and Problems in the Pipeline

Even with a clean 5-stage design, some conflicts arise:

1. **I-cache and D-cache accessed in the same cycle**
   - Instruction Fetch (stage 1) reads from I-cache
   - Data Memory (stage 4) reads/writes D-cache
   - Since different instructions can be in stages 1 and 4 at the same time, having separate I-cache and D-cache avoids a conflict

2. **Registers read and written in the same cycle**
   - Stage 2 (RR) reads registers; Stage 5 (RW) writes registers
   - Different instructions will be doing both at the same time
   - **Solution:** Design the register file so that the read/write time equals half the clock cycle — read in the second half of the cycle, write in the first half (or vice versa)

3. **Branch target not known until end of stage 2 (RR)**
   - After fetching a branch instruction, the CPU has already started fetching the next instruction
   - But it doesn't know yet whether the branch will be taken and where to jump to
   - **What to do in the meantime?** This leads us to hazards...

---

### Hazards

Hazards are situations where the pipeline cannot proceed smoothly. There are three types:

#### 1. Structural Hazard
**What it is:** Two instructions (in different pipeline stages) are competing for the **same hardware resource** at the same time.

**Example:** If there was only one memory unit (not separate I-cache and D-cache), then when instruction 1 is in stage 4 (reading data memory) and instruction 5 is in stage 1 (fetching from instruction memory), they'd both want memory at the same time.

**Fix:** Duplicate resources (e.g., separate instruction and data caches).

#### 2. Data Hazard
**What it is:** An instruction needs a value that a previous instruction **hasn't finished computing yet**.

**Example:**
```asm
ADD R1, R2 -> R3     # R3 = R1 + R2  (stage 5 writes R3)
SUB R3, R4 -> R5     # Needs R3! But R3 isn't written until 3 cycles later
```
The SUB instruction tries to read R3 in stage 2, but ADD hasn't written R3 yet (it's still in the pipeline).

**Fixes:**
- **Stalling (bubbles):** Pause the pipeline until the data is ready (wastes cycles)
- **Forwarding/Bypassing:** Route the result directly from one stage to another without waiting for it to be written to a register

#### 3. Control Hazard
**What it is:** The CPU has fetched the next instruction(s) but then a branch changes the PC — those fetched instructions are now wrong.

**Example:**
```asm
BEQ R1, R2, 100    # If R1 == R2, jump to address 100
ADD R3, R4 -> R5   # Already fetched! But should we execute it?
```
By the time we know whether the branch is taken, we've already fetched one or more wrong instructions.

**Control hazard is a special case of data hazard** (we're waiting for the PC value to be computed), but it's treated separately because the solutions are different:
- **Stalling:** Wait until the branch outcome is known
- **Branch prediction:** Guess whether the branch will be taken and continue fetching — if wrong, flush the pipeline
- **Delayed branching:** Always execute the instruction(s) after the branch (the "delay slot"), useful when the instruction after a branch is harmless

---

## Revision Checklist

- [ ] I can explain what Von Neumann architecture is and why it was important (stored program concept)
- [ ] I know the difference between stored program computers and fixed program computers
- [ ] I can name and describe all 5 components of Von Neumann architecture (CU, ALU, Registers, Memory Unit, I/O)
- [ ] I understand what the CPU is and what it contains
- [ ] I can explain what the Control Unit does (coordinates, sends timing/control signals)
- [ ] I can explain what the ALU does (arithmetic and logic operations)
- [ ] I know all 5 key registers and what each one holds: MAR, MDR, AC, PC, CIR
- [ ] I understand the three buses: Address Bus, Data Bus, Control Bus — and what each carries
- [ ] I understand why RAM is used instead of just a hard drive (speed, direct CPU access)
- [ ] I can state and apply Amdahl's Law (including the formula and what it means)
- [ ] I can work through the web server speedup example (40% CPU, 60% I/O, 10x faster CPU → 1.56 speedup, max 1.66)
- [ ] I understand the 90-10 rule and the principle of locality (temporal and spatial)
- [ ] I know why clocks are needed in a CPU and what a clock signal looks like
- [ ] I can explain what a latch is and why it is used between circuit stages
- [ ] I understand the difference between a combinational circuit and a sequential circuit
- [ ] I can describe single-cycle design and why the clock cycle length is a problem
- [ ] I can describe multi-stage (multi-cycle) design and how latches separate stages
- [ ] I can explain pipelining using the assembly line analogy
- [ ] I know the quantitative effects of pipelining (CPI stays same, clock speed up, total time down)
- [ ] I know the ideal speedup formula: speedup = number of pipeline stages
- [ ] I can name and describe all 5 stages of the MIPS pipeline: IF, RR, ALU, DM, RW
- [ ] I know what happens in each pipeline stage (fetch, decode/read regs, execute, memory, write-back)
- [ ] I can fill in the pipeline summary table for ADD, BEQ, LD, and ST instructions
- [ ] I understand the conflicts in the 5-stage pipeline (I-cache vs D-cache, register read/write, branch target)
- [ ] I can define and give an example of all three types of hazards: structural, data, and control
- [ ] I understand why control hazards are treated separately from data hazards
