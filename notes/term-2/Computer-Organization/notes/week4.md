# Week 4: Floating Point

---

## 1. What is Floating Point?

Computers need to represent decimal numbers like 0.75 or very large/very small numbers like 0.000000001. Integers alone can't do this. Enter **floating point** — the computer's way of storing numbers with decimal points.

### Normalized Scientific Notation

Think of how scientists write big numbers: **3.5 x 10^9** (3.5 billion). There's always exactly one non-zero digit before the decimal point. That's "normalized" form.

Computers do the same thing, but in **binary**:

```
1.010001 x 2^(-5)
```

This means: `(1 + 0x2^-1 + 1x2^-2 + ... + 1x2^-6) x 2^-5`

The rule: **always exactly one `1` before the binary point**.

### Why a Standard?

Without a standard, a number saved on one computer might mean something different on another. The **IEEE 754 standard** was created so all computers agree on how floating point numbers are stored. It also makes hardware design simpler.

---

## 2. The IEEE 754 Format (Sign and Magnitude Representation)

A floating point number is split into **3 fields** stored in a 32-bit register (single precision):

```
| S |    E (8 bits)    |         F (23 bits)          |
  1        8                        23
Sign    Exponent                 Fraction
```

- **S (Sign)** — 1 bit: `0` = positive, `1` = negative
- **E (Exponent)** — 8 bits: controls the range (how big or small the number can be)
- **F (Fraction)** — 23 bits: controls the precision (how many significant digits)

### The Key Insight: The Implicit Leading 1

Since normalized binary numbers always start with `1.xxxx`, there's no need to actually store that `1` — it's **always assumed to be there**. This gives us one free extra bit of precision!

So the value of a register is:

```
Value = (-1)^S  x  (1 + F)  x  2^E
```

Without the implicit 1, it would just be `(-1)^S x F x 2^E`.

### Trade-offs

| More bits in... | Gives you... |
|---|---|
| Exponent | Wider **range** (bigger/smaller numbers) |
| Fraction | Higher **precision** (more decimal digits) |

Think of it like this: the exponent is the zoom level on a map, the fraction is the detail at that zoom level.

---

## 3. Range of Single-Precision Numbers

With 8 exponent bits and 23 fraction bits:

- **Largest number**: `2.0 x 2^128 ≈ 2.0 x 10^38`
- **Smallest (positive) number**: `1.0 x 2^-127 ≈ 2.0 x 10^-38`

### What happens when you go out of range?

- **Overflow**: your result is **bigger than the max** — the computer can't store it
- **Underflow**: your result is **smaller than the min** (too close to zero) — again, can't store it

Analogy: overflow is like trying to write a number on a sticky note that's too big to fit. Underflow is like trying to write a number so tiny it just rounds down to zero.

---

## 4. Double Precision Format

When you need more range and precision, use **double precision** — it takes up **two 32-bit registers** (64 bits total):

```
| S |      E (11 bits)      |              F (52 bits)              |
  1           11                               52
```

- **11 exponent bits** → much wider range
- **52 fraction bits** → much higher precision

Double precision is what most programming languages use by default when you write `double` in C/Java.

---

## 5. Biased Exponent Representation

Here's a problem: if the exponent can be negative (like -5), how do we store it in bits without using a separate sign bit for it?

### The Solution: Biased Notation

We store a **biased** version of the exponent. To get the true exponent, you **subtract the bias** from what's stored.

```
True exponent = (Exponent stored in register) - Bias
```

- **Single precision bias = 127**
- **Double precision bias = 1023**

### Why bias = 127?

Because the exponent needs to range from **-127 to +128**. By adding 127 to everything, we shift this range to **0 to 255** — which fits perfectly in 8 bits, all positive, easy to compare.

Analogy: it's like a thermometer that always adds 40 degrees to avoid negative numbers. If the thermometer reads 37, the real temperature is 37 - 40 = -3.

### The Final Formula

```
Value = (-1)^S  x  (1 + Fraction)  x  2^(Exponent - Bias)
```

This is the complete IEEE 754 formula. Learn this by heart.

**Diagram to remember:**
```
True exponent  <---(-127)---  Exponent stored in register
True exponent  ---(+127)--->  Exponent stored in register
```

---

## 6. Special Values in IEEE 754

The format reserves some bit patterns for special purposes:

| Exponent field | Fraction field | Meaning |
|---|---|---|
| All 0s | All 0s | **Zero** (special code, implicit 1 is NOT added) |
| All 0s | Non-zero | **Denormalized number** (denorm) — very tiny numbers near zero |
| All 1s | All 0s | **+/- Infinity** (e.g., 1/0) |
| All 1s | Non-zero | **NaN** (Not a Number) — e.g., 0/0 or infinity - infinity |

These reserved patterns slightly reduce the range of representable numbers, but they are essential for handling edge cases in real programs.

---

## 7. Worked Examples

### Formula reminder:
```
Value = (-1)^S  x  (1 + Fraction)  x  2^(Exponent - Bias)
```

---

### Example 1: Encode -0.75 in Single Precision

**Step 1: Convert -0.75 to binary**

- 0.75 in binary: `0.75 = 0.5 + 0.25 = 2^-1 + 2^-2 = 0.11` in binary
- Normalized: `1.1 x 2^-1`

**Step 2: Fill in the fields**

- **Sign S = 1** (negative)
- **True exponent = -1**; stored exponent = -1 + 127 = **126 = 0111 1110** in binary
- **Fraction = 1000...000** (the `.1` after the implicit leading 1, padded with zeros to fill 23 bits)

**Single-precision result:**
```
1  0111 1110  1000 0000 0000 0000 0000 000
S  Exponent   Fraction
```

**Double-precision result** (bias = 1023, exponent = -1 + 1023 = 1022 = 011 1111 1110):
```
1  011 1111 1110  1000 0000 ... 0000
S    Exponent        Fraction (52 bits)
```

---

### Example 2: Decode a Single-Precision Number

**Given:** `1  1000 0001  0100 0000 0000 0000 0000 000`

**Step 1: Extract fields**
- S = `1` → negative
- Exponent = `1000 0001` = 129 (in decimal)
- Fraction = `0100 0000...` = 0.25 (= 0 x 2^-1 + 1 x 2^-2)

**Step 2: Apply formula**
- True exponent = 129 - 127 = **2**
- Significand = 1 + 0.25 = **1.25**
- Value = (-1)^1 x 1.25 x 2^2 = **-1.25 x 4 = -5.0**

**Answer: -5.0**

---

## 8. Floating Point Addition

Adding floating point numbers is not as simple as adding integers. You can't just add the fractions if the exponents are different — it's like trying to add metres and kilometres without converting first.

### Steps for FP Addition:

1. **Match exponents** — convert the smaller-exponent number to use the larger exponent (shift the fraction right)
2. **Add the fractions**
3. **Normalize** the result (get back to `1.xxxx` form)
4. **Check for overflow/underflow**
5. **Round** to fit in the available fraction bits
6. **Re-normalize** if rounding changed the form

### Worked Example (4 decimal digits, 2 exponent digits):

**Problem:** `9.999 x 10^1 + 1.610 x 10^-1`

```
Step 1 - Match exponents (convert to larger: 10^1):
    9.999 x 10^1
  + 0.016 x 10^1    ← 1.610 x 10^-1 shifted right by 2 places

Step 2 - Add:
    10.015 x 10^1

Step 3 - Normalize:
    1.0015 x 10^2

Step 4 - Check overflow/underflow: OK

Step 5 - Round (only 4 digits allowed):
    1.002 x 10^2    ← the '5' caused rounding up

Step 6 - Re-normalize: already normalized
```

**Final answer: 1.002 x 10^2**

> Note: The true answer is 100.161, but we got 100.2. There's a small error because we had limited fraction bits. More fraction bits = less rounding error.

---

## 9. Floating Point Multiplication

### Steps for FP Multiplication:

1. **Compute the new exponent** — add the two exponents (and be careful: because of bias, you must subtract one bias from the sum, otherwise you double-count it)
2. **Multiply the significands** (the `1.xxxx` parts), then place the binary point correctly
3. **Normalize** the result
4. **Round** (and potentially re-normalize)
5. **Assign the sign** — XOR the two sign bits (positive x positive = positive, positive x negative = negative)

> The "careful!" note on the exponent: if both exponents are stored with bias added, adding them gives you `(E1 + bias) + (E2 + bias) = E1 + E2 + 2*bias`. You only want one bias in the result, so subtract one bias back.

---

## 10. MIPS Floating Point Instructions

MIPS has a **separate set of registers** just for floating point: `$f0` through `$f31`.

### Arithmetic Instructions

```
add.s  $f0, $f1, $f2    # single-precision add: $f0 = $f1 + $f2
add.d  $f0, $f2, $f4    # double-precision add
sub.s  $f0, $f1, $f2    # subtract (single)
mul.s  $f0, $f1, $f2    # multiply (single)
div.s  $f0, $f1, $f2    # divide (single)
```

### Comparison Instructions

FP comparisons don't use branch conditions directly. They **set an internal hardware bit**, which is then read by a branch instruction.

```
c.eq.s  $f1, $f2    # set flag if $f1 == $f2
c.lt.s  $f1, $f2    # set flag if $f1 < $f2
c.neq.s $f1, $f2    # set flag if $f1 != $f2

bc1t  label         # branch if flag is TRUE
bc1f  label         # branch if flag is FALSE
```

### Load/Store

```
lwc1  $f0, address($t0)    # load word into FP register
swc1  $f0, address($t0)    # store word from FP register
```

Important: **the address is still computed using integer registers** (`$t0` here), not FP registers.

### Double Precision Storage

A double takes 64 bits, so it uses **two adjacent FP registers**. For example, a double stored in `$f4-$f5` is referred to by just `$f4`.

---

## 11. Code Example: Fahrenheit to Celsius

Here's a complete example converting the C formula `(5.0/9.0) * (fahr - 32.0)` to MIPS assembly.

### C code:

```c
float f2c(float fahr) {
    return ((5.0 / 9.0) * (fahr - 32.0));
}
```

### MIPS Assembly:

```
# fahr is passed in $f12 (convention: first FP argument goes in $f12)

lwc1  $f16, const5       # load constant 5.0 into $f16
lwc1  $f18, const9       # load constant 9.0 into $f18
div.s $f16, $f16, $f18   # $f16 = 5.0 / 9.0

lwc1  $f18, const32      # load constant 32.0 into $f18
sub.s $f18, $f12, $f18   # $f18 = fahr - 32.0

mul.s $f0, $f16, $f18    # $f0 = (5/9) * (fahr - 32)  ← return value goes in $f0

jr    $ra                 # return to caller
```

**Line by line:**
- We load `5.0` and `9.0` from memory (constants can't be embedded directly in FP instructions the same way as integers)
- We divide them: `$f16 = 5/9 ≈ 0.5556`
- We load `32.0`, subtract from the input temperature
- We multiply to get the Celsius result
- Result is returned in `$f0` (by MIPS calling convention)

---

## 12. Fixed Point Arithmetic

Floating point is flexible but **slow** — the hardware is complex. Sometimes we don't need that flexibility.

**Fixed point** is a trick: use integers, but secretly agree that all numbers represent values **scaled by a fixed factor**.

### How it works:

Pick a factor, say `1/1000`. Now:
- Instead of storing `1.46`, store the integer `1460`
- Instead of storing `1.7198`, store `1720` (rounded)
- Instead of storing `5624`, store `5624000`

To get the real value: divide the integer by 1000.

### Trade-offs:

| Property | Fixed Point | Floating Point |
|---|---|---|
| Speed | Faster (uses integer ALU) | Slower |
| Flexibility | Less flexible | More flexible |
| Precision | Can be lower | Higher |
| Programming effort | More (you manage the scale) | Less |

Fixed point is used in embedded systems, audio DSPs, and anywhere speed matters more than flexibility.

---

## 13. Subword Parallelism

Modern CPUs have wide ALUs — often 64-bit or 128-bit. But sometimes the data you're working with is much smaller, like:

- **8-bit values** (bytes): pixel RGB colour values in image processing
- **16-bit values** (half-words): audio samples

It would be wasteful to use a 64-bit adder on an 8-bit value. Instead, we can **split the ALU** into multiple smaller adders by partitioning the carry chains inside.

### Example:

One 64-bit adder can be re-used as:
- **4 independent 16-bit adders** (for audio processing), or
- **8 independent 8-bit adders** (for pixel processing)

### The benefit:

- A single `load` instruction can load 8 pixel values at once
- A single `add` instruction can add 8 pairs of pixels simultaneously

This is called **subword parallelism** (also known as SIMD — Single Instruction, Multiple Data, at a small scale). It's a cheap way to get parallel speedup without extra cores.

---

## Revision Checklist

- [ ] I understand what normalized scientific notation means and can write a binary number in that form
- [ ] I know the IEEE 754 standard exists to make floating point consistent across machines
- [ ] I can draw the single-precision layout: 1 sign bit, 8 exponent bits, 23 fraction bits
- [ ] I understand why the leading 1 is implicit and how this gives a free extra bit
- [ ] I know the formula: `Value = (-1)^S x (1 + Fraction) x 2^(Exponent - Bias)`
- [ ] I can state the single-precision range: largest ~2 x 10^38, smallest ~2 x 10^-38
- [ ] I understand what overflow and underflow mean
- [ ] I can describe the double-precision format: 1 + 11 + 52 bits
- [ ] I understand biased notation and can explain why bias = 127 for single precision
- [ ] I can convert between true exponent and stored exponent using the bias
- [ ] I know the special values: zero (all 0s), infinity (max exponent + zero fraction), NaN (max exponent + non-zero fraction), denorms (zero exponent + non-zero fraction)
- [ ] I can encode a decimal number (like -0.75) into IEEE 754 single-precision bit pattern
- [ ] I can decode an IEEE 754 bit pattern (like `1 1000 0001 0100...`) back to a decimal number
- [ ] I can walk through the 6 steps of FP addition: match exponents, add, normalize, check overflow, round, re-normalize
- [ ] I understand that rounding errors come from limited fraction bits
- [ ] I can list the steps for FP multiplication, including the exponent bias trick
- [ ] I know the MIPS FP register file: $f0 to $f31
- [ ] I know the MIPS FP instructions: `add.s`, `add.d`, `sub.s`, `mul.s`, `div.s`
- [ ] I understand how FP comparison works in MIPS: `c.lt.s` sets a flag, then `bc1t`/`bc1f` branches on it
- [ ] I know that `lwc1`/`swc1` load/store FP values but still use integer registers for addresses
- [ ] I can trace through the Fahrenheit-to-Celsius MIPS assembly code
- [ ] I can explain fixed point arithmetic and give an example with a scale factor
- [ ] I know the trade-off: fixed point is faster but less flexible than floating point
- [ ] I understand subword parallelism: splitting a wide ALU to do multiple small additions in parallel
- [ ] I can give real-world examples of where subword parallelism is used (pixels, audio samples)
