# Computer Organization — Full Syllabus Index

> All notes are in simple language with worked examples and revision checklists.

---

## [Week 1 — Introduction & MIPS Basics](week1.md)

- Why study hardware (Moore's Law, multi-core, new platforms)
- Motivating example: 200x speedup via hardware-aware coding
- Microprocessor performance trends
- Dynamic power formula and the power wall
- Performance equation: Execution Time = Cycles × Cycle Time
- MIPS ISA design principles (simple + regular)
- Registers: 32 MIPS registers, `$s`, `$t`, `$zero`
- Load/Store instructions (`lw`, `sw`)
- Memory layout: Text → Globals → Heap → Stack
- Base + offset addressing, array access
- Immediate operands (`addi`, `$zero`)
- Number systems: Binary, Hex, memory sizing

---

## [Week 2 — MIPS Instruction Set (Deep Dive)](week2.md)

- R-type and I-type instruction formats (fields decoded)
- Logical operations: `sll`, `srl`, `and`, `or`, `nor`
- Control instructions: `beq`, `bne`, `slt`, `j`, `jr`
- If-else and while loops in assembly
- Procedure calls — 6-step process
- Full MIPS register table (all 32 registers)
- `jal`, Program Counter (PC), nested calls
- The Stack — `$sp`, push/pop, activation records
- Caller vs callee-saved registers
- Leaf function example (leaf_example)
- Recursive function example (factorial)
- Character handling: `lb`, `sb`, ASCII, null terminator
- `strcpy` in assembly
- Large constants: `lui` + `ori`
- CISC vs RISC comparison
- Big Endian vs Little Endian
- How a program starts: Assembler → Linker → Loader

---

## [Week 3 — Binary Arithmetic](week3.md)

- Binary representation: MSB, LSB, unsigned range
- ASCII vs binary storage (space comparison)
- Why negative numbers are tricky
- Sign-and-magnitude (and why it was rejected)
- One's complement (and why it was rejected)
- Two's complement — the standard, the formula, negation trick
- Worked examples: 5, -5, -6 in two's complement
- Signed vs unsigned: `slt` vs `sltu`
- Sign extension
- Addition and subtraction in binary
- Overflow — conditions, MIPS `add` vs `addu`
- Multiplication — long multiply, hardware algorithm, MIPS `mult`, `mfhi`, `mflo`
- Division — long division, 7÷2 traced step by step
- Division hardware (basic and efficient)
- Negative division — all four sign cases

---

## [Week 4 — Floating Point & Subword Parallelism](week4.md)

- Why floating point exists (very large/small numbers)
- IEEE 754 single precision: 1 sign + 8 exponent + 23 mantissa bits
- Implicit leading 1, normalized form
- Biased exponent (bias = 127), how to convert
- Range: largest (~10³⁸), smallest (~10⁻³⁸), overflow, underflow
- Double precision: 1 + 11 + 52 bits
- Special values: zero, denormals, infinity, NaN
- Worked encoding: -0.75 in single and double precision
- Worked decoding: `1 1000 0001 0100...` → -5.0
- FP Addition — 6 steps with `9.999×10¹ + 1.610×10⁻¹` example
- FP Multiplication — steps, exponent bias trap
- MIPS FP instructions: arithmetic, comparison (`c.lt.s`, `bc1t/bc1f`), load/store
- Double-precision register pairs
- Fahrenheit-to-Celsius code example traced
- Fixed point — concept, worked example, speed vs precision trade-off
- Subword parallelism — 64-bit ALU as 8× 8-bit adders, pixel/audio use cases

---

## [Week 5 — Von Neumann, Amdahl's Law & Pipelining Intro](week5.md)

- Von Neumann architecture (1945): stored program concept
- 5 components: CU, ALU, Registers, Memory, I/O
- All 5 registers: MAR, MDR, AC, PC, CIR
- Buses: Address, Data, Control
- RAM vs hard drive
- Amdahl's Law — formula + web server example (1.56x actual, 1.66x max)
- Common principles: 90-10 rule, temporal/spatial locality, energy leakage
- Clocks and latches: combinational vs sequential circuits
- Single-cycle vs multi-cycle design
- Pipelining — assembly line analogy, ideal speedup formula
- 5-Stage MIPS pipeline: IF → RR → ALU → DM → RW
- Pipeline timing diagram
- Stage summary table for ADD/BEQ/LD/ST
- Conflicts: I-cache/D-cache, register read/write, branch timing
- Three hazard types: structural, data, control

---

## [Week 6 — Pipeline Hazards (Deep Dive)](week6.md)

- 5-stage pipeline recap
- Structural hazards — unified cache problem, fix: add hardware
- Data hazards — producer/consumer concept
- No-bypass approach: 2 stall cycles shown with pipeline diagram
- Bypassing/forwarding — input latches L3/L4/L5, which latch forwards what
- Problem 0: add→add (no-bypass and bypass)
- Problem 1: add→lw (0 stalls with bypassing)
- Problem 2: lw→lw — load-use hazard, 1 mandatory stall
- Problem 3: lw→sw — DM-to-DM forwarding, 0 stalls
- Problem 4: deeper pipeline (7/9 stages) implications
- Control hazards — 4 techniques: stall, predict-not-taken, delay slot, branch prediction
- Branch delay slots — "from before" and "from target" strategies
- Key formulas: stall count, branch penalty, CPI
- Summary table: hazard → cause → fix

---

## [Week 7 — Branch Prediction, Out-of-Order Execution & Caches](week7.md)

- Control hazards recap — all 4 techniques
- Bimodal branch predictor: 14-bit index, 16K entries, 2-bit saturating counters
- 4-state state machine (ST, WT, WNT, SNT)
- Why 2-bit beats 1-bit for loops
- Context switch weakness, combination predictors
- Multicycle instructions causing out-of-order completion
- 4 execution units and their stage counts
- Out-of-order processor: Fetch Queue, Decode/Rename, ROB, IQ, ALUs
- Register renaming — example: R1→T1, why it removes false dependencies
- Reorder Buffer (ROB) and Instruction Queue (IQ)
- Worked example: in-order vs OoO completion time with `LW R9`
- DRAM vs SRAM trade-off
- Memory hierarchy: Registers → L1 → L2 → L3 → DRAM → Disk
- Temporal and spatial locality
- AMAT formula: `AMAT = Hit Time + Miss Rate × Miss Penalty`
- Worked AMAT example: 300 cycles → 16 cycles (~19x speedup)

---

## [Week 8 — How the Internet Works](week8.md)

- ARPANET history (1969), first host-to-host message
- Network of networks, packet switching, best-effort delivery
- End-to-end principle
- Protocol layering — 4-layer model
- IP hourglass model
- HTTP request/response with real examples
- Layer encapsulation
- Sockets, IP addresses, port numbers
- URI/URL/URN syntax with worked example
- DNS hierarchy — how names resolve (ucla.edu tree)
- DHCP — how devices get IP addresses
- ARP — how IP maps to MAC address (3-device example)
- Complete step-by-step: what happens when you open a browser
  - DNS lookup (11 sub-steps)
  - TCP 3-way handshake
  - NAT at each step
  - HTTP GET and response

---

## [Week 9 — Network Devices & Routing](week9.md)

- Device comparison: Repeater / Hub / Bridge / Switch / Router
- Repeaters — signal attenuation fix
- Hubs — half-duplex, 1 collision domain, security risks
- Bridges — LAN segmentation
- Switches — self-learning, MAC table evolution (step-by-step)
- Traffic isolation
- Routers — 5-step operation, internal architecture
- Line cards, switching fabric, control plane vs data plane
- Longest Prefix Matching (LPM) — why it exists, 4 examples worked
- Binary trie — traced examples (1011→C, 1000→B)
- Direct trie trade-offs
- CAM and TCAM — wildcard explanation, sorted-table trick
- Switching fabric — shared bus vs crossbar
- Head-of-Line (HOL) blocking — car queue analogy
- Virtual Output Queues (VOQ) — solution to HOL blocking
- Broadcast vs collision domains
- Hub vs switch vs router behaviour
- Full-duplex and Wi-Fi in modern networks

---

## [Week 10 — Middleboxes, Firewalls & NAT](week10.md)

- Ideal vs real internet — 6 real-world problems
- Middleboxes — what they are, why controversial
- 6 types of middleboxes
- Firewalls — packet filtering fields (SRC/DST IP, ports, TCP flags, ICMP, DPI)
- Two filtering examples
- Rule-ordering worked example (Alice/Bob/Trudy → answer D = 2,1,3)
- Stateless vs stateful firewalls
- Load balancers — virtual IP, failover behaviour, gratuitous ARP
- WAN Accelerators — TCP ACK spoofing, compression, caching/deduplication
- Tunneling — encapsulation, logical vs physical view, VPN
- NAT — motivation, terminology (NAT vs PAT, static vs dynamic)
- All 4 NAT types with worked examples
- Policy NAT and Twice NAT
- Arguments against NAT

---

## Quick Revision Order (Recommended)

1. **Week 1 → 2 → 3 → 4** — Hardware fundamentals + MIPS + Math
2. **Week 5 → 6 → 7** — Architecture, Pipelining, Out-of-Order, Caches
3. **Week 8 → 9 → 10** — Networking end-to-end
