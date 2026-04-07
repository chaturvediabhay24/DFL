# Week 2: Control Instructions — Revision Notes

---

## 1. Instruction Formats

Every MIPS instruction is exactly **32 bits** (one word). Those 32 bits are split into **6 fields** that tell the hardware what to do and which data to use.

Think of it like a form with different boxes to fill in: one box for the operation, others for which registers to use, and so on.

### R-type Instructions (Register-type)

Used for operations where everything is in registers (add, subtract, shift, etc.).

```
| op     | rs    | rt    | rd    | shamt | funct  |
| 6 bits | 5bits | 5bits | 5bits | 5bits | 6 bits |
```

| Field   | Meaning                        |
|---------|-------------------------------|
| `op`    | Opcode — what kind of instruction (always 000000 for R-type) |
| `rs`    | First source register          |
| `rt`    | Second source register         |
| `rd`    | Destination register (result goes here) |
| `shamt` | Shift amount (only used for shift instructions, 0 otherwise) |
| `funct` | Function code — specifies the exact operation (e.g. add, sub) |

**Example: `add $t0, $s1, $s2`**

```
000000  10001  10010  01000  00000  100000
  op      rs     rt     rd   shamt  funct
```

- `rs` = 10001 = register 17 = `$s1`
- `rt` = 10010 = register 18 = `$s2`
- `rd` = 01000 = register 8 = `$t0`
- `funct` = 100000 = add

So in plain English: "Add the value in `$s1` to the value in `$s2`, and put the result in `$t0`."

---

### I-type Instructions (Immediate-type)

Used when one of the values is a constant (immediate) rather than a register, or for memory access (load/store) and branches.

```
| op     | rs    | rt    | constant/offset |
| 6 bits | 5bits | 5bits | 16 bits         |
```

| Field      | Meaning                                      |
|------------|----------------------------------------------|
| `op`       | Opcode — specifies the operation             |
| `rs`       | Source register (base address for memory ops)|
| `rt`       | Target register (destination or second source)|
| `constant` | A 16-bit number baked into the instruction   |

**Example: `lw $t0, 32($s3)`**

- Load the word from memory at address (`$s3` + 32) into `$t0`
- `rs` = `$s3` (base), `rt` = `$t0` (destination), constant = 32

> **Analogy:** The instruction format is like a post office parcel form. The opcode is the "service type" box, the register fields are the "sender" and "recipient" addresses, and the constant field is any special instructions written in the notes box. Everything has a fixed size so the hardware can read it instantly.

---

## 2. Logical Operations

These work on individual bits. Useful for masking, testing bits, and packing/unpacking data.

| Operation      | C / Java | MIPS Instruction |
|----------------|----------|-----------------|
| Shift Left     | `<<`     | `sll`           |
| Shift Right    | `>>`/`>>>`| `srl`          |
| Bit-by-bit AND | `&`      | `and`, `andi`   |
| Bit-by-bit OR  | `\|`      | `or`, `ori`     |
| Bit-by-bit NOT | `~`      | `nor`           |

### What do these actually do?

- **Shift Left (`sll`):** Move all bits to the left by N positions, filling the right with 0s. Shifting left by 1 is the same as multiplying by 2. Shifting left by 2 = multiply by 4, etc.
  - Example: `0000 0011` shifted left 2 = `0000 1100` (3 became 12)

- **Shift Right (`srl`):** Move all bits right by N positions. Shifting right by 1 = divide by 2 (integer).

- **AND (`and`, `andi`):** Each bit of result is 1 only if BOTH input bits are 1. Used to **mask** (isolate) specific bits.
  - Example: `1010 AND 1100 = 1000`

- **OR (`or`, `ori`):** Each bit is 1 if EITHER input bit is 1. Used to **set** specific bits.
  - Example: `1010 OR 1100 = 1110`

- **NOT via NOR:** MIPS has no dedicated NOT instruction. Instead it uses NOR (NOT-OR). `NOR $rd, $rs, $zero` gives you NOT of `$rs`, because OR-ing anything with 0 leaves it unchanged, and then NOR flips all bits.

> **Analogy for AND:** Imagine a bouncer who only lets you in if you have BOTH a ticket AND an ID. AND only outputs 1 when both inputs are 1.

> **Analogy for OR:** A door that opens if you have a key OR a keycard. Only stays shut if you have neither.

---

## 3. Control Instructions

By default, the CPU runs instructions one after another in order. Control instructions let you **jump around** — skipping code, repeating it (loops), or choosing between options (if/else). This is how we get decisions and loops.

### 3.1 Conditional Branches

Jump to a label **only if** a condition is true. Otherwise, keep going to the next instruction.

```
beq register1, register2, L1   # Branch if Equal
bne register1, register2, L1   # Branch if Not Equal
slt rd, rs, rt                  # Set on Less Than: rd = 1 if rs < rt, else 0
```

- **`beq`**: "If register1 == register2, jump to L1"
- **`bne`**: "If register1 != register2, jump to L1"
- **`slt`**: Doesn't branch directly — sets a register to 1 or 0, which you can then use with `beq`/`bne`

### 3.2 Unconditional Branches (Jumps)

Always jump, no condition needed.

```
j L1         # Jump to label L1 unconditionally
jr $s0       # Jump to the address stored in register $s0
```

- **`j L1`**: Like a `goto` — always go to that label
- **`jr $s0`**: Jump to whatever address is in `$s0`. Useful for large `switch` statements and for returning from procedures (using `jr $ra`).

---

### 3.3 Example: if-else in Assembly

**C code:**
```c
if (i == j)
    f = g + h;
else
    f = g - h;
```

Assume: `f=$s0`, `g=$s1`, `h=$s2`, `i=$s3`, `j=$s4`

**Version 1 — using `bne` (branch to else):**

```assembly
        bne  $s3, $s4, Else   # if i != j, skip to Else
        add  $s0, $s1, $s2    # f = g + h  (the "then" part)
        j    Exit              # skip the else block
Else:   sub  $s0, $s1, $s2    # f = g - h  (the "else" part)
Exit:
```

Step by step:
1. Check if `i != j`. If yes, jump straight to `Else`.
2. If we didn't jump, do `f = g + h`, then jump past the else block.
3. `Else:` does `f = g - h`.

**Version 2 — using `beq` (branch to then):**

```assembly
        beq  $s3, $s4, Then   # if i == j, jump to Then
        sub  $s0, $s1, $s2    # f = g - h  (else part comes first)
        j    Exit
Then:   add  $s0, $s1, $s2    # f = g + h
Exit:
```

> Both versions are correct — it's just two different ways to structure the branching logic. The first one is more natural (mirrors the code structure). The second one inverts it.

---

### 3.4 Example: while loop in Assembly

**C code:**
```c
while (save[i] == k)
    i += 1;
```

Registers: `i = $s3`, `k = $s5`, base address of `save[]` = `$s6`

**Version 1 (straightforward):**

```assembly
Loop:   sll  $t1, $s3, 2       # $t1 = i * 4  (byte offset; each int = 4 bytes)
        add  $t1, $t1, $s6     # $t1 = address of save[i]
        lw   $t0, 0($t1)       # $t0 = save[i]  (load the value)
        bne  $t0, $s5, Exit    # if save[i] != k, exit loop
        addi $s3, $s3, 1       # i = i + 1
        j    Loop              # go back to top
Exit:
```

**Why `sll $t1, $s3, 2`?**
- Array elements are 4 bytes each (32-bit integers).
- To get the byte address of element `i`, you need `i * 4`.
- Shifting left by 2 is the same as multiplying by 4 (2^2 = 4). It's faster than a multiply instruction.

**Version 2 (optimised — avoids recalculating address from scratch every iteration):**

```assembly
        sll  $t1, $s3, 2       # compute initial address of save[i] BEFORE loop
        add  $t1, $t1, $s6
Loop:   lw   $t0, 0($t1)       # load save[i]
        bne  $t0, $s5, Exit    # exit if not equal
        addi $s3, $s3, 1       # i += 1
        addi $t1, $t1, 4       # advance pointer by 4 bytes (next element)
        j    Loop
Exit:
```

This is more efficient because the `sll` and `add` to compute the address only happen once, and then we just increment the pointer by 4 bytes each time.

---

## 4. Procedure Calls

A procedure (function/subroutine) is a block of code you can call from different places. The calling code is the **caller**, and the procedure being called is the **callee**.

Think of it like calling a plumber. You (caller) give them the job details (arguments), they do the work (execute), and then they give you the result and leave your house the way they found it (return value + restore state).

### The 6 Steps of a Procedure Call

1. Put arguments where the callee can see them (`$a0`-`$a3`)
2. Transfer control to the callee (`jal`)
3. Callee acquires storage (makes space on the stack)
4. Callee executes
5. Callee puts result in `$v0`/`$v1` where caller can access it
6. Return control to caller (`jr $ra`)

---

## 5. MIPS Registers — Full Map

MIPS has **32 registers** (each 32 bits wide), each with a specific role:

| Register(s)  | Name       | Purpose                                     |
|-------------|------------|---------------------------------------------|
| `$0`        | `$zero`    | Always 0. You can't change it. Useful as a constant. |
| `$2-$3`     | `$v0-$v1`  | Return values from a procedure              |
| `$4-$7`     | `$a0-$a3`  | Input arguments to a procedure              |
| `$8-$15`    | `$t0-$t7`  | Temporaries — caller must save if needed    |
| `$16-$23`   | `$s0-$s7`  | Saved variables — callee must restore       |
| `$24-$25`   | `$t8-$t9`  | More temporaries                            |
| `$28`       | `$gp`      | Global pointer (points to global data)      |
| `$29`       | `$sp`      | Stack pointer (top of the stack)            |
| `$30`       | `$fp`      | Frame pointer (base of current stack frame) |
| `$31`       | `$ra`      | Return address (saved by `jal`)             |

> **Analogy:** Think of registers like named slots on a whiteboard. `$zero` is a slot that always reads 0 no matter what you write on it. `$ra` is a sticky note that says "come back here when you're done."

---

## 6. Jump-and-Link (jal) and the Program Counter (PC)

### The Program Counter (PC)

- A special register (not in the 32 general-purpose registers) that holds the **address of the currently executing instruction**.
- After each instruction, PC automatically increments by 4 (to the next instruction).

### How `jal` Works

```assembly
jal  NewProcedureAddress
```

- Saves `PC + 4` (the address of the next instruction — the return address) into `$ra`
- Jumps to `NewProcedureAddress` by updating the PC

**Why PC+4 and not just PC?** Because by the time we want to return, we want to execute the instruction AFTER the `jal`, not the `jal` itself again.

### Returning from a procedure

```assembly
jr  $ra    # jump to the address stored in $ra
```

This sends control back to wherever the caller was.

### The problem with nested calls

If `jal` overwrites `$ra`, and inside your procedure you call another procedure with another `jal`, the original `$ra` is lost. You must **save `$ra` to the stack** before calling another procedure.

---

## 7. The Stack

The stack is a region of memory used to save and restore values when procedures call other procedures. It grows **downward** (from high addresses toward low addresses).

```
High address
+--------------+
| Proc A data  |
+--------------+
| Proc B data  |
+--------------+
| Proc C data  |
+--------------+
      ...
Low address   <-- $sp points here (top of stack)
```

- `$sp` (stack pointer) always points to the **top** of the stack (the lowest used address).
- To push (make space): `addi $sp, $sp, -N` (subtract N bytes — moves pointer down)
- To pop (free space): `addi $sp, $sp, N` (add N bytes — moves pointer up)

> **Analogy:** The stack is like a pile of trays in a cafeteria. Each procedure puts its tray on top when it starts and takes it off when it leaves. `$sp` always points to the topmost tray.

---

## 8. Storage Management on a Call/Return

### Full sequence of events:

**Before calling (caller's job):**
1. Put arguments in `$a0`-`$a3`
2. Save any temp registers (`$t0`-`$t9`) you still need
3. Save `$ra` if this caller will itself make another call
4. Execute `jal ProcedureName`

**Inside the callee:**
1. Make stack space: `addi $sp, $sp, -N`
2. Save any `$s0`-`$s7` registers it will use
3. Do the work
4. Put result in `$v0` (or `$v1` if two return values)
5. Restore saved `$s` registers from stack
6. Free stack space: `addi $sp, $sp, N`
7. `jr $ra` to return

---

## 9. Example 1 — Leaf Procedure (no nested calls)

A "leaf" procedure is one that doesn't call any other procedures — like a leaf on a tree (no children).

**C code:**
```c
int leaf_example(int g, int h, int i, int j) {
    int f;
    f = (g + h) - (i + j);
    return f;
}
```

Arguments: `g=$a0`, `h=$a1`, `i=$a2`, `j=$a3`

**Assembly:**
```assembly
leaf_example:
    addi $sp, $sp, -12   # make room for 3 values on the stack (3 x 4 bytes)
    sw   $t1, 8($sp)     # save $t1 at stack+8
    sw   $t0, 4($sp)     # save $t0 at stack+4
    sw   $s0, 0($sp)     # save $s0 at stack+0

    add  $t0, $a0, $a1   # $t0 = g + h
    add  $t1, $a2, $a3   # $t1 = i + j
    sub  $s0, $t0, $t1   # $s0 = (g+h) - (i+j) = f

    add  $v0, $s0, $zero # return value = f  ($zero is always 0, so this just copies $s0 to $v0)

    lw   $s0, 0($sp)     # restore $s0
    lw   $t0, 4($sp)     # restore $t0
    lw   $t1, 8($sp)     # restore $t1
    addi $sp, $sp, 12    # free stack space
    jr   $ra             # return to caller
```

**Key notes:**
- The **callee** saved the registers it needed (`$t0`, `$t1`, `$s0`)
- The **caller** was responsible for saving its own `$ra` and `$a0`-`$a3` before calling this
- We could have skipped the stack entirely here and just used `$t` registers directly (they're temporaries and the callee isn't expected to preserve them). The stack save/restore is shown here for completeness.

---

## 10. Example 2 — Recursive Procedure

**C code:**
```c
int fact(int n) {
    if (n < 1) return 1;
    else return n * fact(n - 1);
}
```

This calls itself — so we MUST save `$ra` to the stack (otherwise the recursive `jal` would overwrite it).

**Assembly:**
```assembly
fact:
    slti $t0, $a0, 1      # $t0 = 1 if n < 1, else 0
    beq  $t0, $zero, L1   # if $t0 == 0 (n >= 1), jump to L1 for recursion
    addi $v0, $zero, 1    # base case: return 1
    jr   $ra              # return

L1:
    addi $sp, $sp, -8     # make room for 2 values
    sw   $ra, 4($sp)      # save return address
    sw   $a0, 0($sp)      # save n (we need it after the recursive call)

    addi $a0, $a0, -1     # argument for recursive call: n - 1
    jal  fact             # call fact(n-1) — result goes into $v0

    lw   $a0, 0($sp)      # restore n
    lw   $ra, 4($sp)      # restore return address
    addi $sp, $sp, 8      # free stack space

    mul  $v0, $a0, $v0    # return n * fact(n-1)
    jr   $ra              # return to caller
```

**Walk-through for `fact(3)`:**
1. `n=3`: not < 1, so jump to L1. Save `$ra` and `n=3`, call `fact(2)`
2. `n=2`: save `$ra` and `n=2`, call `fact(1)`
3. `n=1`: save `$ra` and `n=1`, call `fact(0)`
4. `n=0`: 0 < 1, return 1
5. Unwind: `1 * 1 = 1`, then `2 * 1 = 2`, then `3 * 2 = 6`. Returns 6.

**Note:** `$t0` is a temporary and is never saved — this is fine because temp registers are caller-saved, and the recursive call is free to clobber them.

---

## 11. Dealing with Characters

Characters aren't always 32 bits. MIPS provides special instructions for smaller data:

| Instruction | Meaning          |
|-------------|------------------|
| `lb`        | Load byte (8 bits)  |
| `sb`        | Store byte       |
| `lh`        | Load half-word (16 bits) |
| `sh`        | Store half-word  |

### ASCII

- C stores characters as **ASCII** — each character is 8 bits (1 byte)
- `'A'` = 65, `'a'` = 97
- A string ends with a **null character** — a byte with value 0 (`'\0'`)
- This is how the computer knows where the string ends

---

## 12. Example 3 — String Copy (strcpy)

**C code:**
```c
void strcpy(char x[], char y[]) {
    int i = 0;
    while ((x[i] = y[i]) != '\0')
        i += 1;
}
```

Registers: `x = $a0` (destination array), `y = $a1` (source array)

**Assembly:**
```assembly
strcpy:
    addi $sp, $sp, -4     # make room to save $s0
    sw   $s0, 0($sp)      # save $s0 (callee-saved)
    add  $s0, $zero, $zero # i = 0

L1: add  $t1, $s0, $a1    # $t1 = address of y[i]
    lb   $t2, 0($t1)       # $t2 = y[i]  (load one byte)
    add  $t3, $s0, $a0    # $t3 = address of x[i]
    sb   $t2, 0($t3)       # x[i] = y[i]  (store one byte)
    beq  $t2, $zero, L2   # if y[i] == '\0', we're done
    addi $s0, $s0, 1      # i += 1
    j    L1                # loop back

L2: lw   $s0, 0($sp)      # restore $s0
    addi $sp, $sp, 4      # free stack
    jr   $ra              # return
```

**Notes:**
- We use `lb`/`sb` because characters are 1 byte, not 4 bytes.
- Since the index `i` goes up by 1 (not by 4), we don't need to shift by 2 as we did with int arrays.
- Temp registers (`$t1`, `$t2`, `$t3`) are not saved — they're caller-saved temporaries.
- `$s0` IS saved because it's a callee-saved register.

---

## 13. Saving Conventions (Who Saves What)

This is a formal agreement between callers and callees about register responsibilities.

| Who Saves | Registers | Why |
|-----------|-----------|-----|
| **Caller** saves | `$t0`-`$t9` | The callee may freely overwrite these. If the caller needs them after the call, it must save them first. |
| **Caller** saves | `$ra` | `jal` will overwrite `$ra`. Save it if you're going to call again. |
| **Caller** saves | `$a0`-`$a3` | The callee may change these. If caller needs original args later, save them. |
| **Callee** saves | `$s0`-`$s7` | These are "precious" variables. The callee must save and restore them if it uses them. |

> **Analogy:** Think of `$t` registers as a shared whiteboard in a meeting room — anyone can erase it. `$s` registers are your personal notebook — if someone borrows it, they must return it exactly as they found it.

---

## 14. Large Constants

### Problem
I-type instructions only have a **16-bit** field for constants. What if you need a bigger number?

### Solution: `lui` + `ori`

`lui` = Load Upper Immediate

```assembly
lui  $t0, 0x1234      # puts 0x1234 into the UPPER 16 bits of $t0
                      # lower 16 bits become 0
ori  $t0, $t0, 0x5678 # OR in the lower 16 bits
                      # $t0 now = 0x12345678
```

This two-instruction combo loads any 32-bit constant into a register.

### Branch target addresses

- `beq`/`bne` branch destinations are 16-bit **offsets** relative to the current PC (not absolute addresses)
- Formula: `Target address = PC + 4 + (offset × 4)`
- This means branches can only reach instructions that are within about ±32K instructions of the current one

### Jump addresses

- `j` instruction uses a **26-bit** field for the target address
- If you need to jump to an address that doesn't fit in 26 bits, load the address into a register and use `jr` instead

---

## 15. IA-32 Instruction Set (Intel x86)

This is a brief look at Intel's architecture for comparison with MIPS.

| Feature | MIPS (RISC) | IA-32 / x86 (CISC) |
|---------|-------------|---------------------|
| Instruction size | Fixed 32 bits | Variable size |
| General-purpose registers | 32 registers | Only 8 registers |
| Operand locations | Always registers (except load/store) | Can be in registers OR memory |
| Instruction complexity | Simple, uniform | Complex, varied |
| Performance | High (easier to pipeline) | Lower (harder to pipeline) |
| Compatibility | Clean design | 20+ years of legacy features preserved |

- **CISC** = Complex Instruction Set Computer (IA-32)
- **RISC** = Reduced Instruction Set Computer (MIPS)

Modern Intel processors deal with the complexity of IA-32 by internally **converting complex IA-32 instructions into simpler micro-operations** (similar to RISC internally), then executing those. Best of both worlds in practice.

---

## 16. Endian-ness

When you load multi-byte data from memory into a register, which byte goes where?

**Memory layout example:**
```
low address --> 45  7b  87  7f --> high address
```

### Big-endian (MIPS, IBM)
- First byte read goes into the **most significant** (big/left) end of the register
- Register looks like: `45 7b 87 7f`
- The data appears in memory in the same order as in the register
- "What you see is what you get"

### Little-endian (x86 / Intel)
- First byte read goes into the **least significant** (small/right) end of the register
- Register looks like: `7f 87 7b 45`
- The bytes appear reversed compared to memory

> **Analogy:** Imagine reading a 4-digit number written across 4 boxes in memory: "4", "5", "7", "b". Big-endian reads it naturally left-to-right: 457b. Little-endian reverses it: the first box goes to the rightmost position.

This matters a lot when sharing binary data between different computer architectures (e.g., network communication between x86 and MIPS machines).

---

## 17. Starting a Program — From C to Running

Here is the full journey from source code to running program:

```
x.c  (C source file)
  |
  | [Compiler]
  v
x.s  (Assembly language file)
  |
  | [Assembler]
  v
x.o  (Object file — machine code, but with unresolved references)
  |
  | [Linker] <--- also links in library routines (x.a, x.so)
  v
a.out  (Executable — complete machine language program)
  |
  | [Loader]
  v
Memory  (program is loaded and begins running)
```

### Role of the Assembler
- Converts **pseudo-instructions** into real hardware instructions
  - Pseudo-instructions are shortcuts that don't exist in hardware but make programming easier: e.g., `move $t0, $t1` (no such hardware instruction, assembled as `add $t0, $t1, $zero`)
  - Other examples: `blt` (branch-less-than), loading 32-bit immediates, labels
- Converts assembly instructions into binary machine code
- Creates a separate `.o` file for each `.c` file
- Calculates actual numeric values for instruction labels
- Records which labels are referenced from other files (external references) and debug info

### Role of the Linker
- Stitches all `.o` files together into one executable
- Patches up all cross-references between files (where one file calls a function defined in another)
- Determines final memory addresses for all code and data labels
- Organises the code and data sections in memory

**Dynamic Linking (DLLs):**
- Some libraries (`.dll` on Windows, `.so` on Linux) are linked at run time, not compile time
- The executable contains stub/dummy routines
- When the stub is called, it invokes the dynamic linker which finds the real library function and updates the executable to call it directly next time

### Role of the Loader
- Copies the executable from disk into memory
- Sets up the stack and initialises registers
- Starts execution (jumps to the program entry point)

---

## Revision Checklist

- [ ] I can describe the R-type instruction format and name all 6 fields
- [ ] I can describe the I-type instruction format and its 4 fields
- [ ] I can decode a binary R-type instruction (e.g. identify op, rs, rt, rd, shamt, funct)
- [ ] I know all 5 logical operations (shift left, shift right, AND, OR, NOT/NOR) and their MIPS instructions
- [ ] I understand why `sll` by 2 is the same as multiplying by 4
- [ ] I can explain what `beq`, `bne`, and `slt` do
- [ ] I can explain what `j`, `jr` do and when to use `jr` instead of `j`
- [ ] I can convert a simple if-else C block into MIPS assembly (both bne and beq versions)
- [ ] I can convert a while loop into MIPS assembly, including computing the array address with `sll`
- [ ] I know the 6 steps of a procedure call
- [ ] I can list all 32 MIPS registers, their names, and their purposes
- [ ] I understand what the Program Counter (PC) is
- [ ] I know exactly what `jal` does (saves PC+4 into $ra, jumps to procedure)
- [ ] I understand why nested calls require saving `$ra` to the stack
- [ ] I understand the stack — direction of growth, role of `$sp`, push/pop using `addi`
- [ ] I can explain the full call/return process including stack management
- [ ] I can trace through Example 1 (leaf_example) and explain each instruction
- [ ] I can trace through Example 2 (recursive factorial) and explain why `$ra` and `$a0` are saved
- [ ] I know what `lb`, `sb`, `lh`, `sh` are used for
- [ ] I know how ASCII encodes characters ('A'=65, 'a'=97, null terminator=0)
- [ ] I can trace through Example 3 (strcpy) and explain why `lb`/`sb` are used
- [ ] I know the saving conventions: caller saves `$t`, `$ra`, `$a`; callee saves `$s`
- [ ] I can explain how to load a 32-bit constant using `lui` + `ori`
- [ ] I understand how branch target addresses are calculated (PC-relative, 16-bit offset)
- [ ] I know the difference between RISC and CISC and can compare MIPS vs IA-32
- [ ] I can explain big-endian vs little-endian with an example, and name which architecture uses which
- [ ] I can draw the full C-to-execution pipeline: Compiler → Assembler → Linker → Loader
- [ ] I know what the assembler does (converts pseudo-instructions, creates .o files)
- [ ] I know what the linker does (patches references, creates executable)
- [ ] I know what the loader does (puts executable in memory, starts execution)
- [ ] I understand dynamic linking (DLLs) and how stub routines work
