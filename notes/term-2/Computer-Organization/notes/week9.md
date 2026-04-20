# Week 9 - Internet Devices

> Lecture by Prof. Ankit Gangwal, IIIT-H

---

## Table of Contents

1. [Overview of Network Devices](#1-overview-of-network-devices)
2. [Repeaters and Hubs](#2-repeaters-and-hubs)
3. [Bridges and Switches](#3-bridges-and-switches)
4. [Routers](#4-routers)
5. [Longest Prefix Match (LPM)](#5-longest-prefix-match-lpm)
6. [LPM Lookup Techniques](#6-lpm-lookup-techniques)
7. [Switching Fabric and Crossbar Switching](#7-switching-fabric-and-crossbar-switching)
8. [Broadcast and Collision Domains](#8-broadcast-and-collision-domains)
9. [Revision Checklist](#9-revision-checklist)

---

## 1. Overview of Network Devices

Think of network devices as traffic controllers at different levels of intelligence:

| Device | Layer | How it forwards traffic |
|---|---|---|
| Repeater / Hub | Layer 1 (Physical) | Broadcasts to ALL ports |
| Bridge / Switch | Layer 2 (Data Link) | Forwards to the right port using MAC address |
| Router | Layer 3 (Network) | Forwards to the right port using IP address |

**Analogy:** A hub is like a person shouting in a room (everyone hears it). A switch is like a phone call (only the right person hears it). A router is like a postal sorting office (it reads the address and sends it to the right city).

---

## 2. Repeaters and Hubs

### Repeaters

The problem: electrical signals get weaker the further they travel down a wire — like how your voice fades if you shout across a big room. This limits how long a LAN cable can be.

**What a repeater does:**
- Sits in the middle of a cable run
- Continuously monitors the electrical signal coming in
- Sends out an amplified (boosted) copy on the other side
- It is a **Layer 1 device** — it has absolutely no idea what the data means, it just boosts the signal

**Analogy:** A repeater is like a megaphone relay — it doesn't understand what is being said, it just makes the sound louder and passes it on.

### Hubs

A hub is basically a **multiport repeater** — it has many ports and shouts everything it receives out of every other port.

**Key properties of a hub:**
- **Layer 1 device** — no knowledge of MAC addresses or IP addresses
- **Half-duplex** — a device connected to a hub cannot send and receive at the same time. If two devices transmit at once, the signals collide
- **1 collision domain** — every device connected to the hub is in the same collision domain. A collision anywhere affects everyone
- **Security risk** — since every frame goes to every port, anyone connected can snoop on all traffic
- **Wasted bandwidth** — even if only PC-A wants to talk to PC-B, PC-C and PC-D also receive the data and have to throw it away
- Hubs have been **replaced by switches** in modern networks

### Limitations of Repeaters and Hubs

- **One big shared link**: because every bit goes to everyone, only one conversation can happen at a time — the total bandwidth (aggregate throughput) is limited
- **Cannot mix LAN technologies**: a repeater/hub cannot connect a 10 Mbps network to a 100 Mbps network because it does not buffer or understand frames — it just amplifies raw electrical signals

---

## 3. Bridges and Switches

### Bridges

A bridge is smarter than a hub. It actually reads frame headers to learn MAC addresses.

**Key properties:**
- **Layer 2 device** — understands MAC addresses
- **Segments the LAN** — splits the network into separate sections. Traffic on one segment stays there unless it needs to cross
- **Usually only 2 ports** — it sits between two LAN segments
- Creates **2 collision domains** (one per side)
- Has been **replaced by switches** (which do the same thing but with many ports)

**Analogy:** A bridge is like a receptionist between two offices. Instead of shouting everything to both sides, they look at who the message is for and only pass it to the right side.

### Switches

A switch is basically **Hub + Bridge** combined, with many ports.

**Key properties:**
- **Layer 2 device**
- **Full-duplex** — devices can send and receive at the same time because each port is its own dedicated connection
- **Multiple collision domains** — each port is its own collision domain, so a collision on one port does not affect others
- **Saves bandwidth** — traffic only goes where it needs to go
- **Better security** — devices only see traffic meant for them (usually)

#### Switch Self-Learning (How a Switch Builds Its MAC Table)

The switch starts with an **empty MAC address table**. It learns by watching traffic:

**Step 1 — A sends data to C (miss):**
- The switch sees a frame from A on Port 1
- It does not know where C is yet, so it **broadcasts** the frame to all other ports
- But it **records** that A is on Port 1 in its table

```
MAC Address Table after Step 1:
+-------------------+------+
| MAC Address       | Port |
+-------------------+------+
| AA-AA-AA-AA-AA-AA |  1   |
+-------------------+------+
```

**Step 2 — C replies to A (hit for A, miss for C):**
- The switch sees a frame from C on Port 3
- It knows A is on Port 1, so it sends the reply **only to Port 1** (no broadcast needed)
- It records that C is on Port 3

```
MAC Address Table after Step 2:
+-------------------+------+
| MAC Address       | Port |
+-------------------+------+
| AA-AA-AA-AA-AA-AA |  1   |
| CC-CC-CC-CC-CC-CC |  3   |
| ...               | ...  |
+-------------------+------+
```

Over time, the table fills up completely and the switch can deliver every frame directly.

#### Traffic Isolation

Once the MAC table is populated, frames are only forwarded to the correct port. This means multiple pairs of devices can communicate simultaneously across different ports — like multiple private phone conversations happening at the same time in the same building.

---

## 4. Routers

### What is a Router?

A router is a **Layer 3 device** that routes traffic **between different networks** (not just within one LAN). It uses **IP addresses** to make decisions.

**Key properties:**
- Usually has fewer ports than a switch
- Has a **forwarding table** that maps destination IP addresses to outgoing network interfaces
- Sits at the boundary between your internal network and the outside internet

### Basic Router Operation (step by step)

When a packet arrives at a router:

1. **Receive** the packet
2. **Read the header** to find the destination IP address
3. **Look up** the forwarding table to find which output interface matches
4. **Modify the header** — decrease TTL (Time to Live) by 1, recalculate the checksum
5. **Send** the packet out through the correct interface

**Internally**, each router has:
- **Line Cards** — handle actual I/O (receive and send packets). Each line card has its own copy of the forwarding table
- **Switching Fabric** — the internal highway that moves packets from an input line card to the correct output line card
- **Processor (Control Plane)** — runs routing protocols, builds the forwarding tables, but is NOT in the path of every packet

### Lookup Algorithm — Depends on Protocol

Different protocols use different matching strategies:

| Protocol | Mechanism | Techniques Used |
|---|---|---|
| Ethernet (48-bit MAC), MPLS, ATM | Exact match | Direct lookup, Associative lookup, Hashing, Binary tree |
| IPv4 (32-bit), IPv6 (128-bit) | Longest-prefix match | Radix trie, Compressed trie, TCAM |

---

## 5. Longest Prefix Match (LPM)

### Why Not Exact Match for IP?

With IP addresses, storing an exact entry for every possible host address would be impractical — there are over 4 billion IPv4 addresses. Instead, routers store **network prefixes** (e.g., "all addresses starting with 192.168.20..." go to interface 1).

The challenge: a destination address might match **multiple prefixes** of different lengths. The rule is: **always use the longest matching prefix** because that is the most specific route.

**Analogy:** Your postal code system. If a router has rules for "India" and also "Delhi" and also "Delhi 110001", and a packet is going to Delhi 110001, the router uses the "Delhi 110001" rule because it is the most specific.

### LPM Examples from the Slides

#### Example 1 (Binary addresses)

Forwarding table:
```
Destination Prefix                         | Output
11001000 00010111 00010*** *********       |   1
11001000 00010111 00011000 *********       |   2
11001000 00010111 00011*** *********       |   3
```

Destination address: `11001000 00010111 00010110 10100001`

Matching analysis:
- Row 1: `11001000 00010111 00010` matches (21 bits match) -> Output 1
- Row 2: `11001000 00010111 00011000` does NOT match (third byte differs)
- Row 3: `11001000 00010111 00011` does NOT match

**Answer: Output 1** (Row 1 is the only match and also the longest match)

#### Example 2 (Binary addresses)

Same table, different destination: `11001000 00010111 00011000 10101010`

- Row 1: `11001000 00010111 00010` — NO (third byte `00011` vs `00010`)
- Row 2: `11001000 00010111 00011000` — YES, 24 bits match
- Row 3: `11001000 00010111 00011` — YES, 21 bits match

Both rows 2 and 3 match, but Row 2 is longer (24 bits vs 21 bits).

**Answer: Output 2** (Row 2 is the longest match)

#### Example 3 (CIDR notation)

Forwarding table:
```
Prefix              | Output
192.168.20.16/28    |   1
192.168.0.0/16      |   2
```

Destination: `192.168.20.191`

Convert to binary to compare:
```
192.168.20.16/28  -> 11000000.10101000.00010100.00010000  (first 28 bits matter)
192.168.0.0/16    -> 11000000.10101000.00000000.00000000  (first 16 bits matter)
192.168.20.191    -> 11000000.10101000.00010100.10111111
```

- Does `192.168.20.191` fall in `192.168.20.16/28`? The /28 block covers `192.168.20.16` to `192.168.20.31`. 191 is NOT in that range.
- Does it fall in `192.168.0.0/16`? The /16 block covers all of `192.168.x.x`. 192.168.20.191 IS in this range.

**Answer: Output 2** (`192.168.0.0/16` is the only match)

#### Example 4 (CIDR notation)

Forwarding table:
```
Prefix              | Output
68.208.0.0/12       |   1
68.211.0.0/17       |   1
68.211.128.0/19     |   2
68.211.160.0/19     |   2
68.211.192.0/18     |   1
```

Destination: `68.211.6.120`

Convert to binary:
```
68.211.0.0/17    -> 01000100.11010011.00000000.00000000  (first 17 bits: 01000100.1101001 1 .0...)
68.211.6.120     -> 01000100.11010011.00000110.01111000
```

- `68.208.0.0/12`: first 12 bits of 68.208 = `01000100.1101`. First 12 bits of 68.211 = `01000100.1101`. Match! (12 bits)
- `68.211.0.0/17`: third byte of 68.211.0.0 starts with `0` (for the 17th bit position). 68.211.6 also has `0` in that position. Match! (17 bits — longer)
- `68.211.128.0/19`, `68.211.160.0/19`, `68.211.192.0/18`: third byte is 6 in binary = `00000110`, which does not match 128, 160, or 192

**Answer: Output 1** (`68.211.0.0/17` is the longest match at 17 bits)

---

## 6. LPM Lookup Techniques

### Binary Trie (Software LPM)

A **trie** is a tree where each edge represents a bit (0 or 1). To look up an address, you follow the path bit by bit from the root.

Example routing table:
```
Prefix  | Router
0*      |   A
10*     |   B
101*    |   C
```

The trie looks like:
```
         [root]
        /       \
       0         1
      [A]         \
                   1
                  /  \
                 0    1
                [B]  [?]
               /   \
              0     1
                   [C]
```

**Lookup: input = `1011`**
- Bit 1 = `1` → go right
- Bit 2 = `0` → go left, reach B (note B as last known match)
- Bit 3 = `1` → go right, reach C (update last known match)
- Bit 4 = `1` → no child exists, stop
- **Output: C** (last valid match found)

**Lookup: input = `1000`**
- Bit 1 = `1` → go right
- Bit 2 = `0` → go left, reach B (record B)
- Bit 3 = `0` → go left, no node exists — stop
- **Output: B** (B was the last valid match before we ran out of path)

**Advantage:** Fast lookup concept
**Disadvantage:** Up to 32 memory accesses for a 32-bit IPv4 address (one per bit level) — each memory access takes time

### Direct Trie (Multi-bit Trie)

Instead of processing 1 bit at a time, process **multiple bits** at once (e.g., 2 bits per level). This reduces the depth of the tree.

- Example: 2 bits per node means edges labelled `00`, `01`, `10`, `11`
- The tree is shallower → fewer memory accesses needed
- **Tradeoff:** Each node needs more memory (has more children slots, many of which may be empty/wasted)

### Hardware: CAM and TCAM

#### Content-Addressable Memory (CAM)

Normal RAM: you give an address, you get back data. CAM works the opposite way:
- You give a **value (tag/address)** as input
- Hardware **searches all entries simultaneously** and returns which row matches
- **Exact match only**
- Operates in **O(1)** because all comparisons happen in parallel in hardware

#### Ternary Content-Addressable Memory (TCAM)

TCAM extends CAM by adding a third state — a **wildcard / don't-care bit (X)**.

Each TCAM cell can store:
- `0` — match only if the incoming bit is 0
- `1` — match only if the incoming bit is 1
- `X` — match either 0 or 1 (don't care)

**Example:** Stored word = `10XX0`
This will match any of these four inputs: `10000`, `10010`, `10100`, `10110`

**How LPM is done with TCAM:**
- All prefixes are stored in TCAM format (trailing bits become `X`)
- Prefixes are sorted from longest to shortest in the table

```
Prefix | TCAM format
101/3  |   101X
111/3  |   111X
10/2   |   10XX
0/0    |   XXXX     <- matches everything (default route)
```

- When a lookup is done, **all rows are searched in parallel simultaneously**
- **Multiple rows may match**
- Because rows are sorted longest-first, the **first match** is automatically the longest match
- This is O(1) in hardware — all comparisons happen at the same time

### Forwarding Tables on Line Cards

Rather than having one central forwarding table that all line cards must query (which would create a bottleneck), each line card has **its own copy** of the forwarding table. The central processor (control plane) updates all copies when routes change.

---

## 7. Switching Fabric and Crossbar Switching

The **switching fabric** is the internal mechanism that moves a packet from an input line card to the correct output line card inside a router.

### Option 1: Shared Bus

- All line cards share a single internal bus
- Only **one input can send to one output at a time**
- Simple but creates a bottleneck

### Option 2: Crossbar Switch (Switched Backplane)

- **Every input port has a direct connection to every output port**
- Multiple input-output pairs that do NOT compete can transfer data **simultaneously** in the same time slot
- Provides good parallelism
- Requires a **scheduler** to decide which connections to activate each time slot

**Example:** Input 1 → Output 4 and Input 2 → Output 5 can happen at the same time (no shared resource). But Input 1 → Output 4 and Input 3 → Output 4 would conflict (both want output 4 at the same time).

### Head-of-Line (HoL) Blocking

This is a nasty problem with crossbar switching.

**The problem:** Each input port has a queue of packets waiting to be sent. If the packet at the **front of the queue** (the "head") is waiting for a busy output port, it **blocks all the packets behind it** — even if those back-of-queue packets want to go to output ports that are currently free.

**Analogy:** Imagine a single-lane road with a queue of cars. The car at the front wants to turn left but oncoming traffic is blocking it. All the cars behind it — even those wanting to turn right (which is free) — are stuck waiting.

**Solution: Virtual Output Queues (VOQ)**

Instead of one single queue per input port, maintain **N separate queues per input port** — one for each output port.

- Input 1's queue for Output 1 (waiting for Output 1 to be free)
- Input 1's queue for Output 2 (waiting for Output 2 to be free)
- Input 1's queue for Output 3 (waiting for Output 3 to be free)
- etc.

Now packets destined for free outputs are not blocked by packets waiting for busy outputs. Each virtual queue can be served independently.

---

## 8. Broadcast and Collision Domains

### Definitions

**Broadcast Domain:**
The set of all devices that will receive a broadcast frame sent by any one device. If PC-A sends a broadcast, every device in its broadcast domain gets it.

**Collision Domain:**
The section of network where two devices sending at the same time will cause a collision (their electrical signals will interfere). Only relevant in shared-medium or half-duplex connections.

### Hub — Both Domains Span Everything

With a hub connecting 4 PCs:
- **1 broadcast domain** — the whole network (all 4 PCs receive every broadcast)
- **1 collision domain** — the whole network (any two PCs sending at the same time causes a collision)

### Switch — One Broadcast Domain, Many Collision Domains

With a switch connecting 4 PCs:
- **1 broadcast domain** — the switch still forwards broadcast frames to all ports (by design — it must, since Layer 2 cannot filter broadcasts)
- **Multiple collision domains** — each switch port is its own separate collision domain. A collision between the switch and PC-A does not affect PC-B, PC-C, or PC-D

**Why do we still care about collision domains even with switches?**
- If a **hub is plugged into a switch port**, that port operates in half-duplex mode, and CSMA/CD is active on that segment — so collisions can still happen on that segment
- A **defective NIC** sending garbage data can cause collisions on its segment
- In such cases, the switch limits damage to only the affected port

**Summary for Switch:**
- Switch is a **collision domain separator** — each port = one collision domain
- Switch is **NOT a broadcast domain separator** — all ports are still in one broadcast domain

### Router — Breaks BOTH Domains

A router creates a **hard boundary**:
- **Breaks broadcast domains** — a broadcast from one side of the router stays on that side and never reaches the other network
- **Breaks collision domains** — each router interface is its own collision domain

### Combined Switch + Router Example

Network topology: Router at top → two switches → PCs under each switch

**Broadcast domains:** 2 (one on each side of the router)

**Collision domains:** One per switch port (each PC-to-switch link is its own collision domain, plus the switch-to-router links)

### Summary Table

| Device | Broadcast Domain | Collision Domain |
|---|---|---|
| Hub | Does NOT separate | Does NOT separate (1 big domain) |
| Switch | Does NOT separate | Separates (1 per port) |
| Router | Separates | Separates |

### Modern Networks

- Wired networks today use switches everywhere — hubs are obsolete
- **Half-duplex switch links**: each switch port is its own collision domain
- **Full-duplex switch links**: collisions are **impossible** — CSMA/CD is disabled entirely
- **Gigabit Ethernet and faster**: only full-duplex exists. No hubs, no repeaters
- Collision domains still matter in **Wi-Fi (wireless networks)** — because all devices share the same radio channel (a shared medium), collisions can still happen

---
| Feature           | Hub     | Switch          | Router  |
| ----------------- | ------- | --------------- | ------- |
| OSI Layer         | Layer 1 | Layer 2         | Layer 3 |
| Data Unit         | Bits    | Frames          | Packets |
| Address Used      | None    | MAC             | IP      |
| Intelligence      | ❌ None  | ✅ Medium        | ✅ High  |
| Collision Domains | 1       | Many (per port) | Many    |
| Broadcast Domains | 1       | 1 (default)     | Many    |
| Duplex            | Half    | Full            | Full    |
| Speed             | Slow    | Fast            | Depends |

---
## 9. Revision Checklist

- [ ] Can explain the difference between a repeater, hub, bridge, switch, and router in plain English
- [ ] Know which OSI layer each device operates at (Layer 1, 2, or 3)
- [ ] Understand why repeaters are needed (signal attenuation over distance)
- [ ] Understand why hubs are problematic (half-duplex, 1 collision domain, security risk)
- [ ] Understand the limitations of repeaters/hubs (cannot mix LAN technologies, limited throughput)
- [ ] Understand how a bridge segments a LAN and creates 2 collision domains
- [ ] Know that a switch = Hub + Bridge, operates full-duplex, each port is its own collision domain
- [ ] Can walk through switch self-learning step-by-step (empty table → miss → broadcast + learn → hit → forward directly)
- [ ] Understand traffic isolation in switches/bridges
- [ ] Know the 5 steps of basic router operation (receive → read header → lookup table → modify header → send)
- [ ] Know the two-part internal architecture of a router: data plane (line cards + switching fabric) and control plane (processor)
- [ ] Know the difference between exact match (Ethernet/MPLS) and longest-prefix match (IPv4/IPv6)
- [ ] Understand WHY longest-prefix match is used for IP (too many addresses for exact match)
- [ ] Can work through LPM examples in binary (find the longest matching prefix)
- [ ] Can work through LPM examples in CIDR notation (e.g., /28 vs /16)
- [ ] Understand binary trie structure and how to trace a lookup through it
- [ ] Know the limitation of binary trie (up to 32 memory accesses for IPv4)
- [ ] Understand the direct (multi-bit) trie tradeoff: fewer memory accesses but more memory usage
- [ ] Can explain how CAM works (give value, get matching address, O(1) exact match)
- [ ] Can explain how TCAM works (three states: 0, 1, X; wildcards enable prefix matching)
- [ ] Know how TCAM achieves LPM (sort by prefix length longest-first, take first match)
- [ ] Know the TCAM format for a prefix (e.g., `101/3` becomes `101X`, `10/2` becomes `10XX`)
- [ ] Understand why forwarding tables are distributed to each line card (avoid central bottleneck)
- [ ] Know the difference between shared bus and crossbar switching fabric
- [ ] Can explain Head-of-Line (HoL) blocking with an analogy
- [ ] Know the solution to HoL blocking: Virtual Output Queues (one queue per output port per input)
- [ ] Can define broadcast domain and collision domain clearly
- [ ] Can identify the number of broadcast and collision domains in a network diagram with hubs, switches, and routers
- [ ] Know that a switch separates collision domains but NOT broadcast domains
- [ ] Know that a router separates BOTH collision and broadcast domains
- [ ] Understand why collision domains still matter even with switches (hubs connected to switch ports, defective NICs)
- [ ] Know that full-duplex links eliminate collisions entirely (CSMA/CD disabled)
- [ ] Know that Gigabit Ethernet requires full-duplex (no hubs allowed)
- [ ] Know that Wi-Fi is still a shared medium and has collision domains
