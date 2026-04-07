# Week 1 - Computer Organization

---

## Why Study Hardware?

Computers are no longer getting faster on their own like they used to. So if you want fast programs, you need to understand the hardware yourself.

Three big reasons:
- **Moore's Law is slowing down** — chips aren't doubling in speed every 2 years anymore
- **Multi-core chips** — modern CPUs have multiple cores; you need to write code that uses all of them
- **New hardware types** — GPUs, mobile chips, etc. work differently

**Real example:** A matrix multiplication program got **200x faster** just by using hardware smartly:
- Using SIMD (data parallelism): 3.8x faster
- Loop unrolling + out-of-order tricks: 2.3x faster
- Cache blocking: 2.5x faster
- Using multiple threads: 14x faster

---

## How Fast Are Processors?

Processors got **~52% faster every year** from 1986 to 2003. After that, growth slowed to ~22%/year because of heat and power problems.

---

## Power & Heat Problem

More transistors = more power = more heat.

**Dynamic Power formula:**
```
Power = activity × capacitance × voltage² × frequency
```

- Voltage and frequency can't keep increasing (chips would melt)
- So the industry moved to **more cores** instead of faster single cores
- **Leakage power** is also a problem — transistors leak electricity even when idle

---

## Clocks and Performance

Every processor has a **clock** that ticks billions of times per second.

```
Execution Time = Number of Clock Cycles × Time per Cycle
Time per Cycle = 1 / Clock Frequency
```

**Examples:**
- Program runs 10 sec on 3 GHz CPU → **30 billion cycles** used
- Program takes 2 billion cycles on 1.5 GHz CPU → **1.33 seconds**

---

## What is an Instruction Set (ISA)?

When you write `a = b + c` in C, the CPU doesn't understand that directly. It needs simple instructions in its own language — this is called **assembly language**.

```
C code:       a = b + c
Assembly:     add a, b, c
Machine code: 00000010001100100100000000100000
```

The set of all such instructions a CPU understands is called its **Instruction Set Architecture (ISA)**.

Two design rules for a good ISA:
1. **Keep hardware simple** — basic operations only, runs fast
2. **Keep instructions regular** — same format everywhere, easy to decode

---

## MIPS — The ISA We Study

MIPS is a simple, clean ISA used for teaching. Every instruction does exactly ONE thing.

**Example:** `a = b + c + d + e` in assembly:
```
add a, b, c      # a = b + c
add a, a, d      # a = a + d
add a, a, e      # a = a + e
```
One C line = multiple assembly lines. That's normal.

**Subtraction example:** `f = (g + h) - (i + j)`
```
add t0, g, h
add t1, i, j
sub f, t0, t1
```

> Important: floating-point math is not always associative. `(a+b)+c` may not equal `a+(b+c)` in a computer. Different instruction orders can give different results.

---

## Registers — The CPU's Scratchpad

The CPU can't do math directly on memory — it's too slow. So it first copies values into tiny, super-fast storage called **registers**.

Think of registers as the CPU's notepad — only a few slots, but very fast.

**MIPS has 32 registers**, each 32 bits (4 bytes) wide.

Named registers:
| Name | Purpose |
|---|---|
| `$s0–$s7` | Your program's main variables |
| `$t0–$t9` | Temporary values |
| `$zero` | Always 0, can't be changed |

```
add $s0, $s1, $s2    # $s0 = $s1 + $s2
```

Why not more registers? More registers = bigger chip = slower access. 32 is a sweet spot.

---

## Loading from Memory

Since registers are limited, most data lives in RAM. You load it into a register before using it, then store the result back.

```
lw $t0, address     # Load: copy from memory into register
sw $t0, address     # Store: copy from register into memory
```

---

## Memory Sizes (Quick Reference)

| Unit | Size |
|---|---|
| 1 byte | 8 bits |
| 1 word | 32 bits = 4 bytes |
| 1 KB | 1024 bytes = 2¹⁰ bytes |
| 1 MB | 2²⁰ bytes |
| 1 GB | 2³⁰ bytes |

A 32-bit address can point to any of **4 GB** of memory (2³² bytes).

---

## How Memory is Organized

Memory is split into sections:

```
High address  ┌─────────────┐
              │   Stack     │  ← local variables, function calls (grows down)
              │     ↓       │
              │     ↑       │
              │    Heap     │  ← dynamic memory (malloc), grows up
              ├─────────────┤
              │   Globals   │  ← global variables
              ├─────────────┤
Low address   │ Instructions│  ← your program's code
              └─────────────┘
```

Important pointers:
- **`$sp`** — Stack Pointer: points to top of the stack
- **`$fp`** — Frame Pointer: points to start of the current function's local data
- **`$gp`** — Global Pointer: points to global variables

When a function is called, it gets a **stack frame** (activation record) — a block of stack space for its local variables.

---

## Addressing: Base + Offset

The compiler knows where every variable is in memory and uses **base address + offset** to access it.

```c
int a, b, c, d[10];
// a is at offset 0, b at 4, c at 8, d[] starts at 12
```

```
addi $gp, $zero, 1000   # set base address to 1000
lw   $s2, 4($gp)        # load b  (address = 1000 + 4)
lw   $s3, 8($gp)        # load c  (address = 1000 + 8)
add  $s1, $s2, $s3      # $s1 = b + c
sw   $s1, 0($gp)        # store result into a
```

**Array access example:** `d[3] = d[2] + a`
```
lw  $t0, 8($s4)     # load d[2]   → offset = 2 × 4 = 8
add $t0, $t0, $s1   # add a
sw  $t0, 12($s4)    # store d[3]  → offset = 3 × 4 = 12
```

Each `int` is 4 bytes, so multiply the index by 4 to get the byte offset.

---

## Immediate Values (Constants in Instructions)

Sometimes you want to use a number directly in an instruction instead of loading it from memory.

```
addi $s0, $s1, 10       # $s0 = $s1 + 10
addi $s0, $zero, 1000   # $s0 = 0 + 1000  → load constant 1000
```

`$zero` always holds 0. It's used to load constants since every instruction needs at least one register.

---

## Number Systems

| System | Example | How it works |
|---|---|---|
| Decimal | 35 | 3×10 + 5×1 |
| Binary | 00100011 | 1×32 + 1×2 + 1×1 = 35 |
| Hex | 0x23 | 2×16 + 3×1 = 35 |

- Hex is just a compact way to write binary: 4 bits = 1 hex digit
- A 32-bit number = 8 hex digits
- Digits: `0–9` then `a=10, b=11, c=12, d=13, e=14, f=15`

---

## Revision Checklist

- [ ] Why hardware matters (Moore's Law ending, multi-core era)
- [ ] Performance = cycles × cycle time; can calculate from clock speed
- [ ] Dynamic power formula; why we can't just increase clock speed
- [ ] ISA = set of instructions a CPU understands
- [ ] MIPS: 32 registers, `$s`, `$t`, `$zero`, each 32 bits
- [ ] `lw` = load from memory; `sw` = store to memory
- [ ] Memory layout: Instructions → Globals → Heap → Stack
- [ ] `$sp`, `$fp`, `$gp` — what each pointer does
- [ ] Base + offset addressing; array index × 4 = byte offset
- [ ] `addi` with `$zero` to load constants
- [ ] Binary, Hex — how to convert and why hex is used
