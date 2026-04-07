# Week 3 — Computer Arithmetic

---

## 1. Binary Representation

Computers store everything as 1s and 0s. Each position in a binary number represents a power of 2, just like each position in a decimal number represents a power of 10.

**Analogy:** Think of binary like a light switch panel. Each switch is either ON (1) or OFF (0), and its position tells you how much it contributes to the total.

### How to read a binary number

```
Binary:  0 1 0 1 1 0 0 0   0 0 0 1 0 1 0 1   0 0 1 0 1 1 1 0   1 1 1 0 0 1 1 1
         ^                                                                      ^
   Most Significant Bit (MSB)                               Least Significant Bit (LSB)
```

The value is calculated as:

```
Value = (bit_31 × 2^31) + (bit_30 × 2^30) + ... + (bit_1 × 2^1) + (bit_0 × 2^0)
```

So the example number above equals:
`0 × 2^31 + 1 × 2^30 + 0 × 2^29 + ... + 1 × 2^0`

### Range of a 32-bit word (unsigned)

- A 32-bit word can represent **2^32 different numbers**
- Range: **0 to 2^32 - 1** (roughly 0 to 4.3 billion)
- This is called **unsigned representation** — we assume all numbers are positive

---

## 2. Why Binary and Not ASCII?

A fair question: why not just store numbers as text (ASCII characters)?

Two reasons it is a bad idea:

1. **Hardware complexity** — building circuits to do arithmetic on ASCII characters is much harder
2. **Storage inefficiency** — binary is far more compact

### Worked example: storing 1,000,000,000

| Format | How stored | Bits used |
|--------|-----------|-----------|
| Binary | Single number (2^30 > 1 billion) | **30 bits** |
| ASCII | 10 characters ("1000000000"), 8 bits each | **80 bits** |

Binary uses less than half the space. This scales up massively in real systems.

---

## 3. Negative Numbers — The Problem

With 32 bits we can represent 2^32 numbers. If we want to include negatives, we split the budget:
- **2^31 non-negative numbers** (0 to 2^31 - 1)
- **2^31 negative numbers** (-2^31 to -1)

The question is: *how* do we encode the negative ones?

---

## 4. Three Approaches to Representing Negatives

### 4a. Sign-and-Magnitude (rejected)

The leftmost bit (MSB) means + or -, and the rest of the bits give the size.

- `0 0000101` = +5
- `1 0000101` = -5

**Problem:** Two representations of zero: `0 0000000` (+0) and `1 0000000` (-0). Hardware hates ambiguity. Also requires extra conversion before doing arithmetic.

### 4b. One's Complement (rejected)

To negate a number, flip every bit.

- `00000101` = +5
- `11111010` = -5

**Problem:** Again, two zeroes: `00000000` and `11111111`. Still needs extra steps before arithmetic.

### 4c. Two's Complement (the winner — used in all modern hardware)

To negate a number: **flip all bits, then add 1**.

This gives exactly one zero, and addition/subtraction works directly without any special cases.

---

## 5. Two's Complement in Detail

### The full 32-bit picture

```
0000 0000 0000 0000 0000 0000 0000 0000  =  0
0000 0000 0000 0000 0000 0000 0000 0001  =  1
...
0111 1111 1111 1111 1111 1111 1111 1111  =  2^31 - 1    (largest positive)

1000 0000 0000 0000 0000 0000 0000 0000  = -2^31         (most negative)
1000 0000 0000 0000 0000 0000 0000 0001  = -(2^31 - 1)
1000 0000 0000 0000 0000 0000 0000 0010  = -(2^31 - 2)
...
1111 1111 1111 1111 1111 1111 1111 1110  = -2
1111 1111 1111 1111 1111 1111 1111 1111  = -1
```

**Key insight:** If the MSB is 1, the number is negative. If it is 0, positive.

### The formula for the value

```
Value = (x_31 × -2^31) + (x_30 × 2^30) + (x_29 × 2^29) + ... + (x_1 × 2^1) + (x_0 × 2^0)
```

Notice the first term uses **-2^31** (negative). That single negative bit is what makes everything work.

### Why two's complement is great for addition

You can just add the binary patterns directly — no special logic needed:

- `1 + (-2)` → add the bit patterns → you get the bit pattern for `-1`. Correct!
- `2 + (-1)` → add the bit patterns → you get the bit pattern for `+1`. Correct!

### The negation trick explained

If you take a number `x` and its bit-flipped version `x'`:

```
x + x' = all 1s = -1   (in two's complement, all 1s means -1)
```

Therefore:
```
x' + 1 = -x
```

So to find -x: **flip all bits, then add 1**.

Also: `x + (-x) = 2^n` — this is why it is called **2's complement**.

---

## 6. Worked Example: 2's Complement for 5, -5, -6

**Step 1: Write +5 in binary**
```
5  = 0000 0000 0000 0000 0000 0000 0000 0101
```

**Step 2: Get -5 by flipping all bits and adding 1**
```
+5 =  0000 0000 0000 0000 0000 0000 0000 0101
Flip: 1111 1111 1111 1111 1111 1111 1111 1010
Add 1:1111 1111 1111 1111 1111 1111 1111 1011  = -5
```

**Step 3: Get -6 (flip +6, add 1)**
```
+6 =  0000 0000 0000 0000 0000 0000 0000 0110
Flip: 1111 1111 1111 1111 1111 1111 1111 1001
Add 1:1111 1111 1111 1111 1111 1111 1111 1010  = -6
```

**Verify:** Take -5 (`1111...1011`), flip to get `0000...0100`, add 1 → `0000...0101` = 5. Correct!

---

## 7. Signed vs. Unsigned

Hardware supports two interpretations of the exact same bit pattern:

| Type | C keyword | MSB of 1 means... | Range (32-bit) |
|------|-----------|-------------------|----------------|
| Unsigned | `unsigned int` | Very large positive number | 0 to ~4.3 billion |
| Signed | `int` or `signed int` | Negative number | ~-2.1 billion to ~+2.1 billion |

**The same bit pattern can mean two completely different things** depending on which interpretation you use. The hardware does not know — *you* (the programmer or compiler) must track this.

### MIPS example: `slt` vs `sltu`

```asm
slt  $t0, $t1, $zero    ; "set $t0 to 1 if $t1 < 0" — treats $t1 as SIGNED
sltu $t0, $t1, $zero    ; "set $t0 to 1 if $t1 < 0" — treats $t1 as UNSIGNED
```

If `$t1` contains `1111 01...01` (starts with 1):

- `slt` treats this as a **negative number** → stores **1** in `$t0` (yes, it is less than zero)
- `sltu` treats this as a **very large positive number** → stores **0** in `$t0` (no, it is not less than zero)

Same bits, completely different answers. The instruction you pick must match how you intended the data.

---

## 8. Sign Extension

Sometimes you have a 16-bit number and need to convert it to 32-bit (for example, when adding an immediate value in MIPS). You need to preserve the value — this is called **sign extension**.

**Rule:** Copy the MSB (sign bit) into all the new bits on the left.

**Analogy:** Like saying "the temperature is -2 degrees" — it does not matter if you write it with 2 digits or 10 digits, the value is the same.

### Examples

**Positive number (+2):**
```
16-bit:  0000 0000 0000 0010   (MSB = 0, positive)
32-bit:  0000 0000 0000 0000   0000 0000 0000 0010
         ^^^^^^^^^^^^^^^^^ fill with 0s (copy of MSB)
```

**Negative number (-2):**
```
16-bit:  1111 1111 1111 1110   (MSB = 1, negative)
32-bit:  1111 1111 1111 1111   1111 1111 1111 1110
         ^^^^^^^^^^^^^^^^^ fill with 1s (copy of MSB)
```

The value is unchanged — just wider.

---

## 9. Addition and Subtraction

### Binary addition

Works exactly like decimal addition, just carry when you hit 2 instead of 10.

```
Example: Adding ...0011 and ...0010 (i.e., 3 + 2 = 5)

  Carries: (0)  (0)  (1)  (1)  (0)
             0    0    0    1    1
           + 0    0    0    1    0
           -------------------------
             0    0    1    0    1    = 5
```

### Binary subtraction

Don't subtract — just **add the negative**. To compute A - B:
1. Negate B (flip B's bits, add 1)
2. Add A + (-B)

This means the hardware only needs one operation (addition) to handle both add and subtract. Efficient!

---

## 10. Overflow

Overflow means the result of an arithmetic operation does not fit in the available bits — the answer is wrong because it "wrapped around".

### Overflow for unsigned numbers

Happens when a carry out of the final bit cannot be stored.

**Analogy:** Like a car odometer that rolls back to 00000 after 99999.

### Overflow for signed numbers

Happens when the MSB of the result does not match what it should be:

- **Two positives added → negative result** = overflow
- **Two negatives added → positive result** = overflow
- **One positive + one negative** = NEVER overflows (the magnitudes shrink)

### MIPS and overflow

```asm
add   $t0, $t1, $t2    ; signed add — raises exception on overflow
addu  $t0, $t1, $t2    ; unsigned add — NEVER flags overflow (you detect it yourself)
sub   $t0, $t1, $t2    ; signed subtract — raises exception on overflow
subu  $t0, $t1, $t2    ; unsigned subtract — no overflow flag
```

Use `addu`/`subu` when you know your numbers are unsigned or when you want to handle overflow detection manually.

---

## 11. Multiplication

### How it works (long multiplication in binary)

Binary multiplication is like decimal long multiplication but simpler: each multiplier bit is either 0 or 1, so you either add the multiplicand (shifted) or add nothing.

### Worked example: 1000 × 1001 (decimal: 8 × 9 = 72)

```
    Multiplicand:        1000
    Multiplier:        × 1001
                       ------
    Partial products:
      (bit 0 = 1):      1000      ← multiplicand × 1
      (bit 1 = 0):     0000       ← multiplicand × 0, shifted left 1
      (bit 2 = 0):    0000        ← multiplicand × 0, shifted left 2
      (bit 3 = 1):   1000         ← multiplicand × 1, shifted left 3
                    --------
    Product:          1001000     = 72 in decimal. Correct!
```

### The rule at each step

1. Look at the current bit of the multiplier
2. If it is 1: add the (shifted) multiplicand to the running product
3. If it is 0: add nothing
4. Shift the multiplicand left (or shift the product right, depending on implementation)
5. Move to the next multiplier bit

---

## 12. Multiplication Hardware

### Algorithm 1 (simpler but uses more space)

```
Components:
- Multiplicand register: 64-bit (starts with 32-bit number in the right half)
- Multiplier register: 32-bit (shifts right each step)
- Product register: 64-bit (accumulates the result)
- 64-bit ALU

Each step:
1. Check LSB of multiplier
2. If 1: add multiplicand to product
3. Shift multiplicand LEFT by 1
4. Shift multiplier RIGHT by 1
5. Repeat 32 times
```

### Algorithm 2 (smarter — product and multiplier share a register)

```
Components:
- Multiplicand register: 32-bit (never moves)
- Combined Product/Multiplier register: 64-bit
- 32-bit ALU

Key insight: at any point, (bits used by product) + (bits used by multiplier) = 64.
So they can share the same 64-bit register.

Each step:
1. Check LSB of the combined register (= current multiplier bit)
2. If 1: add multiplicand to the LEFT half
3. Shift the entire 64-bit register RIGHT by 1
4. Repeat 32 times
```

### Fast (parallel) algorithm

Instead of doing 32 serial steps, compute all partial products at once and add them using a tree of adders. Much faster, but uses a lot more transistors (hardware cost is high).

- No clock synchronisation needed — just wait for signals to propagate
- The delay is proportional to log2(32) instead of 32 steps

---

## 13. MIPS Multiplication Instructions

Because 32 × 32 can produce a 64-bit result, MIPS stores the product in two special registers: `hi` (upper 32 bits) and `lo` (lower 32 bits).

```asm
mult  $s2, $s3     ; signed multiply: $s2 × $s3, result goes to hi:lo
multu $s2, $s3     ; unsigned multiply: same but treats operands as unsigned

mfhi  $s0          ; "move from hi" — copy upper 32 bits into $s0
mflo  $s1          ; "move from lo" — copy lower 32 bits into $s1
```

**Note:** For numbers that fit in 32 bits, you only need `mflo`. Use `mfhi` to check if the upper half is non-zero (which would mean the result overflowed 32 bits).

---

## 14. Division

### Long division in binary

Works just like decimal long division but binary is simpler: at each step you either can or cannot subtract the divisor.

### Worked example: 1001010 ÷ 1000 (decimal: 74 ÷ 8 = 9 remainder 2)

```
        1001          ← Quotient
       ------
1000 | 1001010        ← Dividend
       -1000
       -----
          10
         101
        1010
       -1000
       -----
          10          ← Remainder
```

### The rule at each step

1. Compare divisor with current portion of dividend
2. If divisor is **larger**: quotient bit = 0, bring down next dividend bit
3. If divisor is **smaller or equal**: quotient bit = 1, subtract and bring down next bit

---

## 15. Detailed Division Example: 7 ÷ 2

Divide `0000 0111` (7) by `0010` (2). Expected: quotient = 3, remainder = 1.

The hardware starts the divisor in the left half of a 64-bit register, shifts it right each iteration, and compares with the remainder.

| Iter | Action | Quotient | Divisor | Remainder |
|------|--------|----------|---------|-----------|
| 0 | Initial values | 0000 | 0010 0000 | 0000 0111 |
| 1 | Rem = Rem - Div → negative → restore, shift 0 into Q, shift Div right | 0000 | 0001 0000 | 0000 0111 |
| 2 | Same as iter 1 (still can't subtract) | 0000 | 0000 1000 | 0000 0111 |
| 3 | Same — divisor still too big | 0000 | 0000 0100 | 0000 0111 |
| 4 | Rem = Rem - Div = 0011 → non-negative → shift 1 into Q, shift Div right | 0001 | 0000 0010 | 0000 0011 |
| 5 | Rem = Rem - Div = 0001 → non-negative → shift 1 into Q | 0011 | 0000 0001 | 0000 0001 |

**Result:** Quotient = `0011` = 3, Remainder = `0001` = 1. Correct! (7 = 3 × 2 + 1)

---

## 16. Division Hardware

Similar structure to the multiply hardware, but in reverse:

```
Components:
- Divisor register: 64-bit (starts in left half, shifts RIGHT each step)
- Quotient register: 32-bit (shifts LEFT each step, new bit added on right)
- Remainder register: 64-bit
- 64-bit ALU

Each step:
1. Subtract divisor from remainder
2. If result >= 0: keep it (new remainder), shift 1 into quotient
3. If result < 0: restore old remainder (add divisor back), shift 0 into quotient
4. Shift divisor right by 1
5. Repeat 33 times
```

**Efficient version:** Uses a 32-bit ALU (like the efficient multiply). Divisor stays fixed; the combined remainder register shifts left, saving hardware.

After completion:
- `hi` register = remainder
- `lo` register = quotient

---

## 17. Division with Negative Numbers

### The problem

The equation `Dividend = Quotient × Divisor + Remainder` has multiple valid solutions when negatives are involved.

### Worked examples: 7 and -7 divided by 2 and -2

| Operation | Quotient | Remainder |
|-----------|----------|-----------|
| +7 div +2 | +3 | +1 |
| -7 div +2 | -3 | -1 |
| +7 div -2 | -3 | +1 |
| -7 div -2 | +3 | -1 |

### Convention (used by MIPS and most systems)

- **Remainder always has the same sign as the dividend**
- **Quotient is negative if the signs of dividend and divisor disagree**

**Practical approach:** Convert both operands to positive, do the division, then fix the signs of the result based on the rules above.

### MIPS division instructions

```asm
div   $s2, $s3     ; signed divide: $s2 / $s3
divu  $s2, $s3     ; unsigned divide

mfhi  $s0          ; get remainder (stored in hi)
mflo  $s1          ; get quotient (stored in lo)
```

---

## Quick Reference: Key Formulas

| Concept | Formula |
|---------|---------|
| Value of an n-bit two's complement number | `x_(n-1) × -2^(n-1) + x_(n-2) × 2^(n-2) + ... + x_0 × 2^0` |
| Negate a number in two's complement | `-x = x' + 1` (flip all bits, add 1) |
| Property of a number and its inverse | `x + x' = -1` (all ones) |
| Why it's called 2's complement | `x + (-x) = 2^n` |
| Division identity | `Dividend = Quotient × Divisor + Remainder` |

---

## Revision Checklist

- [ ] I can explain what a binary number represents and how to calculate its decimal value
- [ ] I know the range of a 32-bit unsigned number (0 to 2^32 - 1)
- [ ] I can explain why binary is more efficient than ASCII for storing numbers (with the 1 billion example)
- [ ] I understand why sign-and-magnitude and one's complement were rejected (two zeros, extra conversion steps)
- [ ] I can explain two's complement and why it is preferred (works directly with addition, single zero)
- [ ] I can convert a positive number to its two's complement negative (flip bits, add 1)
- [ ] I know the two's complement formula: MSB has weight -2^31, all others are positive
- [ ] I understand the difference between signed and unsigned integers and when each is used
- [ ] I know how `slt` and `sltu` differ and can predict results for a given bit pattern
- [ ] I can perform sign extension correctly for both positive and negative numbers
- [ ] I understand how binary addition works including carry propagation
- [ ] I understand that subtraction is done by adding the negative (negate B, add to A)
- [ ] I can identify when overflow occurs for both signed and unsigned arithmetic
- [ ] I know which MIPS instructions cause overflow exceptions (`add`, `sub`) vs which do not (`addu`, `subu`)
- [ ] I can perform binary long multiplication step by step (shift and add)
- [ ] I understand the difference between HW Algorithm 1 (64-bit multiplicand, shifts left) and Algorithm 2 (32-bit ALU, product shifts right)
- [ ] I understand why the fast (parallel) multiplication algorithm is faster but more expensive
- [ ] I know the MIPS multiply instructions: `mult`, `multu`, `mfhi`, `mflo`
- [ ] I know that MIPS stores a 64-bit product across the `hi` and `lo` registers
- [ ] I can perform binary long division step by step (compare and subtract)
- [ ] I can trace through the divide example (7 / 2) showing quotient and remainder at each iteration
- [ ] I understand the hardware for division (divisor shifts right, quotient shifts left, remainder register)
- [ ] I know the sign convention for division with negatives (remainder sign = dividend sign; quotient negative if signs disagree)
- [ ] I know the four cases for signed division: +7/+2, -7/+2, +7/-2, -7/-2 and their results
- [ ] I know the MIPS division instructions: `div`, `divu`, `mfhi` (remainder), `mflo` (quotient)
