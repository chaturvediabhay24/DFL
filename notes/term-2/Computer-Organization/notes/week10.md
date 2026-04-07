# Week 10: Internet Middleboxes, Firewalls, NAT, Load Balancers, WAN Accelerators, and Tunneling

---

## 1. The Internet in Practice

### The Ideal Internet (How It Was Designed)

The original vision of the internet was beautifully simple:
- Every device has a **unique, fixed IP address** that never changes
- Every device is **reachable by anyone, anywhere**
- Network nodes (like routers) **just forward packets** — they never touch, modify, or filter them

Think of it like a postal system that just delivers letters without ever opening them or changing the address.

### The Real Internet (How It Actually Works)

Reality is messier. Several problems broke the ideal model:

| Problem | What It Means |
|---|---|
| **Host mobility** | Your phone changes IP address when you move between networks |
| **IP address depletion** | IPv4 only has ~4 billion addresses. Not enough for every device |
| **Security concerns** | We need to detect and block malicious traffic |
| **Replicated services** | YouTube doesn't run on one server — load must be spread |
| **Performance concerns** | We want to cache content, allocate bandwidth smartly |
| **Incremental deployment** | New technology can't replace everything overnight |

---

## 2. What are Middleboxes?

A **middlebox** is any device that sits **between** two communicating hosts and does something to packets beyond just forwarding them.

**Analogy:** Imagine you are sending a letter, but a third party intercepts it, reads it, maybe changes the return address, and then delivers it. That middleman is the middlebox. Often, neither you nor the recipient even knows it is there.

### Why Middleboxes Are Controversial

They are seen as both a problem **and** a solution:

**The "bad" view — an abomination:**
- They **violate layering** (a router at the network layer should not be reading port numbers from the transport layer)
- They are **hard to reason about** — your app may not behave the way you expect
- They cause **subtle bugs** that are extremely difficult to debug

**The "good" view — a practical necessity:**
- They **solve real problems** that the original internet design ignored
- Those problems are not going away, so neither are middleboxes

### Types of Middleboxes

- **Address translators (NAT)** — translate IP addresses/ports
- **Firewalls** — filter packets based on rules
- **Traffic shapers** — control how much bandwidth flows
- **Intrusion detection systems** — look for signs of attacks
- **Transparent proxies** — intercept connections without client knowing
- **Application accelerators** — speed up specific apps

---

## 3. Firewalls

### What Is a Firewall?

A firewall is a middlebox that **filters packets one by one**. For every packet that arrives or wants to leave, the firewall asks: "Should I let this through?"

It makes that decision by looking at:
- **Source (SRC) and Destination (DST) IP addresses** — where is this coming from/going?
- **SRC and DST port numbers** — what service is being used (e.g., port 80 = HTTP)?
- **TCP flags** — is this the start of a connection (SYN) or a reply (ACK)?
- **ICMP message type** — what kind of network control message is this?
- **Deep Packet Inspection (DPI)** — looking inside the actual content of the packet (beyond just headers)

**Analogy:** A firewall is like a bouncer at a club. It checks your ID (packet headers) and decides if you can come in. A fancy bouncer (DPI) even checks what you are carrying in your bag.

---

### Packet Filtering Examples

**Example 1: Block all UDP traffic and Telnet**
- Rule: Block packets where IP protocol field = 17 AND port = 23
- Protocol 17 = UDP, Port 23 = Telnet
- Result: All UDP flows and all Telnet connections are blocked

**Example 2: Block external clients from connecting to internal hosts**
- Rule: Block inbound TCP packets that have **SYN set but NO ACK**
- Why this works: When you start a new TCP connection, you send a SYN packet (no ACK). When replying to an existing connection, you send ACK
- Result: Outsiders cannot start new connections inward, but internal hosts can still connect outward (because the returning SYN-ACK from outside has ACK set)

---

### Firewall Configuration

A firewall has a **list of rules** (sometimes called an Access Control List, ACL). For each packet:
1. The packet is checked against Rule 1
2. If it matches, the decision (permit or deny) is made immediately
3. If not, move to Rule 2, and so on

**Rule order matters.** This is critical. Putting rules in the wrong order can allow traffic that should be blocked, or block traffic that should be allowed.

**Worked Example from the slides:**

Setup:
- Alice's network: `222.22/16`
- Bob's network: `111.11/16` (Alice wants to allow Bob's network access to specific hosts)
- Alice's designated accessible hosts: `222.22.22/24`
- Trudy's hosts (untrusted, inside Bob's network): `111.11.11/24`
- Alice does NOT want any other internet traffic

Rules defined:
```
Rule 1: ALLOW  (SRC = 111.11/16,     DST = 222.22.22/24)  -- Allow Bob in to special hosts
Rule 2: DENY   (SRC = 111.11.11/24,  DST = 222.22/16)     -- Block Trudy
Rule 3: DENY   (SRC = 0/0,           DST = 0/0)           -- Block everyone else
```

**What order should these rules go in?**

Options given: (A) 3,1 — (B) 3,1,2 — (C) 1,3 — (D) 2,1,3

**Answer: (D) 2,1,3**

Why?
- Trudy is part of Bob's network (`111.11.11/24` is inside `111.11/16`)
- If Rule 1 (allow Bob) comes before Rule 2 (block Trudy), Trudy's packets match Rule 1 and get allowed in — wrong!
- So Trudy must be blocked **first** (Rule 2), then Bob's allowed in (Rule 1), then everyone else is blocked (Rule 3)

**Why not (C) 1,3?**
- Rule 3 (DENY all) would fire before Rule 2 (block Trudy) — but actually this doesn't matter if we apply 1 first, because Trudy matches Rule 1 too and would be allowed. So we must deny Trudy first.

---

### Stateless vs Stateful Firewalls

**Stateless Firewall:**
- Treats every packet as if it arrived from nowhere
- Does not remember previous packets
- Problem: To allow return traffic from a server, you have to explicitly write rules for it

**Stateful Firewall:**
- Keeps track of **connections**
- When an internal client connects to a server (sends SYN), the firewall notes this
- When the server sends back a SYN-ACK, the firewall recognises it as part of an existing allowed connection and lets it through automatically
- Much smarter and more secure

**Analogy:** A stateless firewall is like a bouncer who forgets everyone's face the second they walk in. A stateful firewall remembers you came in and will let your friend reply to you.

---

## 4. Load Balancers

### Why Do We Need Them?

A popular website like YouTube cannot run on a single server. One server would be overwhelmed. So there are **many identical servers** all hosting the same content.

But users all go to the same address (`www.youtube.com`). How does traffic get spread across all the servers?

Answer: A **load balancer**.

### How It Works

- The load balancer has one **virtual IP address** (e.g., `12.1.11.3`) that clients connect to
- Behind the scenes, there are multiple real servers with **dedicated IPs** (e.g., `10.0.0.1`, `10.0.0.2`, `10.0.0.3`)
- The load balancer decides which server each new connection should go to
- It applies **load balancing policies** (e.g., round-robin, least loaded, etc.)
- The load balancer is a middlebox — it modifies the destination of packets

### Failover with Load Balancers (Layer-2 Failover)

What happens when one server crashes?

- For **new TCP connections**: YES, the load balancer handles this fine. It just stops sending new connections to the dead server.
- For **existing TCP connections**: NO, these break. The connection was already established to the dead server. The load balancer cannot seamlessly migrate an existing TCP session.

**Gratuitous ARP:** When a server fails, another server can claim its IP address by broadcasting a Gratuitous ARP message saying "I am now the MAC address for IP 10.0.0.1". This helps redirect future traffic, but does not save existing connections.

---

## 5. WAN Accelerators

### What Is a WAN Accelerator?

A **WAN (Wide Area Network) accelerator** (also called a WAN optimizer or bandwidth accelerator) is a middlebox placed at the **edge** of a network, typically between two offices or data centers connected over the internet.

Its goal: **make traffic go faster** without changing anything at the end hosts.

**Analogy:** Imagine two offices sending files between them. A WAN accelerator is like a clever packing service at each end that squeezes the boxes smaller before shipping, and unpacks them on arrival.

### Key Properties

- Placed at the connection point to the internet (one appliance at each end)
- Improves end-to-end performance
- **Incrementally deployable** — no changes needed on end hosts or the rest of the internet

### Techniques Used

**1. TCP Throughput Improvement (Spoofing ACKs)**
- The local appliance sends **ACK packets quickly back to the sender** instead of waiting for the real distant ACK
- It overwrites the **receive window** with a large value (tricks sender into sending more data)
- The appliance buffers the data and sends it onward to the real destination
- Can also run a newer, improved version of TCP between the two appliances

**2. Compression**
- The sending appliance compresses each packet before sending it across the WAN
- The receiving appliance decompresses it before delivering to the real destination
- Can also compress **across multiple packets** (cross-packet compression) for even better results

**3. Caching (Deduplication)**
- The appliance caches copies of data that has been sent before
- When sending new data, it checks if any chunk has been sent before
- Instead of re-sending the same bytes, it **sends just a pointer** (like "send the same chunk as 3 packets ago")
- The receiving appliance uses its cache to reconstruct the full data
- This is extremely effective for repeated file transfers (e.g., backups, email attachments)

---

## 6. Tunneling

### What Is IP Tunneling?

An IP tunnel creates a **virtual point-to-point link** between two nodes. To everyone in between, the original packet is hidden — it looks like regular traffic going between the tunnel endpoints.

How it works technically: **encapsulation** — you wrap the original packet (with its headers and data) inside a new IP packet. The inner packet is just the "payload" of the outer packet.

**Analogy:** Imagine you are sending a sealed envelope (original packet) inside a larger envelope (outer packet). The postal service only sees the outer envelope and delivers it to the outer address. The recipient opens it and finds the inner envelope.

**Logical view:**
```
A --- B ====[tunnel]==== E --- F
```

**Physical view:**
```
A --- B --- [C] --- [D] --- E --- F
```
Nodes C and D just see outer packets going from B to E — they have no idea what is inside.

**Without tunnel:** Packet shows SRC: 1.1.1.10, DST: 2.2.2.10
**With tunnel:** Outer packet shows SRC: 1.1.1.1, DST: 2.2.2.1. Inner packet (payload) is the original with SRC: 1.1.1.10, DST: 2.2.2.10

---

### VPN (Virtual Private Network)

A commercial VPN is a tunnel from your machine to a VPN server:

1. Your machine encrypts traffic and sends it to the VPN server
2. The VPN server decrypts it and sends it on to the destination website (using NAT or a TCP proxy)
3. The destination website sees the VPN server's IP, not yours

**Benefits:**
- Traffic between you and VPN is encrypted (eavesdroppers on your network see nothing useful)
- Your IP is hidden from the destination website
- Can bypass censorship (the censorship system only sees traffic to the VPN server, not to the blocked site)

**Important caveat:** You must **fully trust your VPN provider**. You are essentially moving the "who can spy on you" from your ISP to the VPN company.

---

## 7. NAT (Network Address Translation)

### The Problem NAT Solves

IPv4 addresses are 32-bit numbers — there are about 4.3 billion of them. That sounded like enough in the 1980s. It was not.

**Problem 1:** An organisation got a block of IPs. It grew. Now it needs more. The ISP cannot give contiguous addresses. The range before and after is already taken.

**Problem 2:** Most devices in a home or office do not need internet access simultaneously. It is wasteful to assign each a permanent public IP.

**Solution:** Use **private IP addresses** internally (like `192.168.x.x`, `10.x.x.x`) and translate to public IPs at the boundary.

**NAT is a temporary workaround.** The real solution is IPv6 (128-bit addresses = basically unlimited). NAT exists because the switch to IPv6 has been slow.

---

### Port Numbers (Important for Understanding NAT)

| Port Range | Name | Description |
|---|---|---|
| 0 | Reserved | Used for IPC between programs on same OS, not internet traffic |
| 1 – 1023 | Well-known ports | Require superuser to bind. Examples: HTTP=80, SSH=22, DNS=53 |
| 1024 – 49151 | Registered ports | Assigned for specific services, no superuser needed |
| 49152 – 65535 | Ephemeral/dynamic ports | Temporary ports used by clients for outgoing connections |

---

### NAT vs PAT

Both are types of address translation, but they modify different headers:

**NAT (Network Address Translation)**
- Translates **IP address to IP address**
- Modifies the **Layer 3 (IP) header only**

**PAT (Port Address Translation)**
- Translates **IP:Port to IP:Port**
- Modifies **both Layer 3 (IP) and Layer 4 (TCP/UDP) headers**

---

### Static vs Dynamic Translation

**Static:** The admin explicitly says what the post-translation address will be. The mapping is permanent (one-to-one).

**Dynamic:** The router/device picks the post-translation address automatically when a packet arrives. The mapping is temporary (one-to-many or many-to-one).

**In all cases:** The pre-translation attributes (what to look for) are always explicitly defined. The NAT device needs to know which packets to translate in the first place.

---

### 4 Types of NAT/PAT

There are four combinations:

| Type | What gets translated | Who decides post-translation? |
|---|---|---|
| **Static NAT** | IP address only | Admin (fixed) |
| **Static PAT** | IP:Port | Admin (fixed) |
| **Dynamic PAT** | IP:Port | Router (auto-picks port) |
| **Dynamic NAT** | IP address only | Router (auto-picks IP) |

---

### Static NAT in Detail

**What it does:** Maps one private IP permanently to one public IP. Bidirectional.

**Use case:** You have a private web server at `10.2.2.33` and want it accessible from the internet as `73.8.2.33`.

**How it works:**
- Static NAT configured: `10.2.2.33 <--> 73.8.2.33`
- Outbound packet (internal to external): SRC IP `10.2.2.33` → changed to `73.8.2.33`
- Inbound packet (external to internal): DST IP `73.8.2.33` → changed to `10.2.2.33`

**Example from slides:**
```
Client (54.4.5.9) sends to 73.8.2.33:80
Router sees: DST = 73.8.2.33 → translates to 10.2.2.33:80
Server at 10.2.2.33 receives the packet
Server replies: SRC = 10.2.2.33:80
Router translates: SRC = 73.8.2.33:80
Client receives reply from 73.8.2.33:80
```

**Key observations:**
- Translation direction depends on packet direction: outbound → change SRC, inbound → change DST
- Bidirectional (works both ways)
- **Does NOT conserve IP addresses** — each private host needs its own public IP

**Without static NAT configured:** If a client at `54.4.5.9` sends to `10.2.2.33` (the private address), the packet is simply **dropped** because `10.2.2.33` is not routable on the internet.

---

### Static PAT in Detail

**What it does:** Maps one private IP:Port permanently to one public IP:Port.

**Use case 1: Multiple servers sharing one public IP**

Static NAT limitation: With one public IP and static NAT, you can only reach one internal server (the one mapped to that IP).

Static PAT solution: Map different ports to different servers. External clients hit different ports on the same public IP, and each port routes to a different internal server.

**Example from slides:**
```
Static PAT configuration:
  10.4.4.41:8080 <--> 73.8.2.44:80    (web server 1)
  10.4.4.42:443  <--> 73.8.2.44:443   (SSL server)

External client 54.4.5.7 connects to 73.8.2.44:80
  Router translates DST to 10.4.4.41:8080
  Server 10.4.4.41 receives on port 8080

External client 45.5.4.8 connects to 73.8.2.44:443
  Router translates DST to 10.4.4.42:443
  Server 10.4.4.42 receives on port 443
```

**Use case 2: Non-standard ports**

Your internal server runs HTTP on port 8080 (non-standard). Without PAT, users must type `www.site.com:8080`.

With Static PAT:
- Map `73.8.2.44:80 <--> 10.4.4.41:8080`
- Users type `www.site.com` (default port 80)
- Router automatically translates port 80 to port 8080 when forwarding inward

Also works in reverse: run a service on a non-standard external port but standard internal port. Security benefit: Attackers scan for SSH on port 22. If you forward a random port (e.g., 54321) to internal port 22, attackers scanning port 22 won't find you.

**Use case 3: Port Forwarding (selectively punching holes)**

Static NAT maps ALL ports on the public IP to ALL ports on the private IP — you cannot restrict it to just certain ports.

Static PAT lets you **selectively open only certain ports** on a public IP. Traffic to any other port is silently dropped (no translation exists for it). This is what home routers call "port forwarding."

**Static PAT is bidirectional** — both the internal and external sides can initiate the connection.

---

### Dynamic PAT in Detail

**What it does:** Maps private IP:Port to public IP:Port, but the router automatically picks the public port. Many internal hosts share ONE public IP.

**This is what your home Wi-Fi router does.** This is the most common type of NAT.

**How outbound traffic works (step by step):**

1. Internal host A (`10.6.6.61`) sends a packet with SRC `10.6.6.61:2222`, DST `82.6.4.2:443`
2. Router sees it matches the dynamic PAT rule (translate `10.6.6.0/24` to public IP `32.8.2.66`)
3. Router **randomly picks an available port** (e.g., 7777)
4. Router changes SRC to `32.8.2.66:7777`
5. Router saves this mapping in its **translation table**: `10.6.6.61:2222 <--> 32.8.2.66:7777`
6. Sends packet onward with SRC `32.8.2.66:7777`

Similarly for host B (`10.6.6.62`) sending from port 3333 → router might pick port 8888 → saves `10.6.6.62:3333 <--> 32.8.2.66:8888`

**Translation table example:**
```
10.6.6.61:2222 <--> 32.8.2.66:7777
10.6.6.62:3333 <--> 32.8.2.66:8888
10.6.6.63:3333 <--> 32.8.2.66:9999
```

**How return/response traffic works:**

Incoming packet arrives: SRC `82.6.4.2:443`, DST `32.8.2.66:7777`

Router looks up `32.8.2.66:7777` in the translation table → finds it maps to `10.6.6.61:2222` → changes DST to `10.6.6.61:2222` → delivers to internal host A.

**Why does the router re-randomize the source port?**

Multiple hosts might coincidentally pick the same source port. For example, both host B and host C might use port 3333. The router **must ensure each outbound connection has a unique port** on the public IP, otherwise it cannot tell which return packet belongs to which internal host.

Router options:
- Re-randomize ports for ALL connections (always pick a new port)
- OR re-randomize only when a conflict is detected

**Dynamic PAT is Unidirectional (Important!)**

This is a side effect, not a deliberate feature.

- An external host (D at `11.2.3.4`) tries to initiate a connection to `32.8.2.66:443`
- The router checks its translation table: is there a mapping for `32.8.2.66:443`? No.
- The router **does not know which internal host** to send this to
- It **drops the packet**

This means: only internal hosts can start connections. External hosts cannot reach internal devices through dynamic PAT unless a translation already exists (from the internal host having made a connection first).

---

### Dynamic NAT in Detail

**What it does:** Translates just the IP address (not port), but the router picks which public IP to assign — temporarily, while the connection is active.

**Use case:** Mainly used to support protocols like **Active FTP** that require the external server to make a second connection back to the client.

**How Active FTP works:**

FTP uses two channels:
1. **Control channel:** Client connects to server on TCP/21 (SRC port: random N, DST port: 21)
2. **Data channel:** Server connects BACK to client on TCP/20 (SRC port: 20, DST port: random M — the client tells the server port M via the control channel)

The problem with dynamic PAT and active FTP:
- When the server tries to make the data channel connection back, it uses a different SRC port (TCP/20 not TCP/21) and a different DST port (M not 21)
- Dynamic PAT only allows traffic back if it matches an existing translation entry
- The data channel looks like a brand new connection from outside → **Dynamic PAT drops it**

Dynamic NAT solves this:
- Each internal client gets a **dedicated public IP** (temporarily)
- The server can connect back to that public IP on any port
- The router knows all traffic to that public IP belongs to that one client → lets it through
- **Dynamic NAT allows the data channel**

**Illustration from slides:**

```
Dynamic NAT pool: 54.5.4.1, 54.5.4.2, 54.5.4.3 (3 public IPs available)
Internal hosts: 10.7.7.71 (A), 10.7.7.72 (B), 10.7.7.73 (C), 10.7.7.74 (D)

A connects → gets 54.5.4.1 (dedicated)
B connects → gets 54.5.4.2 (dedicated)
C connects → gets 54.5.4.3 (dedicated)
D tries to connect → NO IP available → packet dropped

Later, A finishes:
  54.5.4.1 becomes available again
  D connects → gets 54.5.4.1
```

**Translation table shows:**
```
10.7.7.71:1111 <--> 54.5.4.1:1111  (only IP changes, port unchanged)
10.7.7.72:2222 <--> 54.5.4.2:2222
10.7.7.73:3333 <--> 54.5.4.3:3333
10.7.7.74:4444 <--> X  no IP available
```

**Key difference from Dynamic PAT:**
- Dynamic PAT: All internal hosts share ONE public IP, distinguished by port
- Dynamic NAT: Each active internal host gets its OWN dedicated public IP (temporarily), port unchanged

**While a translation is active, Dynamic NAT is bidirectional** (external hosts can reach the internal host via its currently assigned public IP).

**Disadvantages of Dynamic NAT:**

- If more hosts want to connect than there are public IPs available → newer hosts are blocked
- Worse: if A was connected, gets disconnected (pool exhausted), and D takes A's IP, then A's old connections are broken — poor user experience
- No guarantee which public IP a host gets → unexpected behaviour
- If you need explicit, permanent mappings → use multiple static NATs instead

---

### Policy NAT

Normally, a NAT decision is made based only on the **source** of the packet. Policy NAT adds the ability to also look at the **destination** when deciding whether/how to translate.

**Use case:** You want traffic going to destination X to be translated one way, and traffic going to destination Y to be translated a different way.

**Example — Policy Dynamic PAT:**
```
Config:
  If source is 10.6.6.0/24 AND destination is 45.5.4.9 → Dynamic PAT to 32.8.2.77
  If source is 10.6.6.0/24 (any destination)           → Dynamic PAT to 32.8.2.66

Host A (10.6.6.61) connecting to 45.5.4.9:443
  → Matches first rule → SRC translated to 32.8.2.77:8888

Host B (10.6.6.62) connecting to 28.2.4.6:80
  → Matches second rule → SRC translated to 32.8.2.66:9999
```

This lets you route traffic to different public IPs based on destination.

---

### Twice NAT

Normally, NAT only translates one side of the packet (either SRC or DST). **Twice NAT translates both the SRC and the DST** in a single operation.

**Example — Policy Twice NAT:**
```
Policy: If source is 10.6.6.0/24 AND destination is 8.8.8.8
  → Dynamic PAT the SRC to 32.8.2.55
  → Static NAT the DST to 32.9.1.8 (redirect to corporate DNS instead of Google DNS)

Internal host (10.6.6.99) tries to reach Google DNS (8.8.8.8:53)
  Packet: SRC 10.6.6.99:9999, DST 8.8.8.8:53

After Twice NAT:
  SRC → 32.8.2.55:5555  (dynamic PAT)
  DST → 32.9.1.8:53     (static NAT — sent to corporate DNS, not Google)
```

This lets you silently intercept traffic and redirect it somewhere else entirely.

---

### Objections Against NAT

NAT is widely criticised by network purists:

1. **Violates layering:** Routers are network-layer devices. They should only look at IP headers. PAT forces them to also look at TCP/UDP port numbers (transport layer). This breaks the clean separation of layers.

2. **Port numbers are misused:** Port numbers were designed to identify sockets (which application is talking). NAT/PAT hijacks them to identify hosts. This causes problems for apps that embed port numbers in their payload (like FTP, SIP, etc.).

3. **Violates end-to-end argument:** The original principle was that intelligence should live at the endpoints, not in the network. NAT puts logic in the middle.

4. **IPv6 is the real answer:** IPv6 has 128-bit addresses (2^128 ≈ 3.4 × 10^38). Every device on Earth could have billions of addresses. NAT would be completely unnecessary. But IPv6 adoption has been painfully slow.

---

## Quick Comparison Table: All NAT Types

| Type | Translates | Who picks post-translation? | Bidirectional? | Use Case |
|---|---|---|---|---|
| Static NAT | IP only | Admin (fixed) | Yes | Expose private server to internet |
| Static PAT | IP:Port | Admin (fixed) | Yes | Port forwarding, hide non-standard ports |
| Dynamic PAT | IP:Port | Router auto-picks | No (unidirectional) | Home router, many hosts share one IP |
| Dynamic NAT | IP only | Router auto-picks | Yes (while active) | Active FTP, temporary dedicated public IP |
| Policy NAT | Any of above | Depends | Depends | Different translation based on DST |
| Twice NAT | Both SRC and DST | Depends | Depends | Intercept/redirect traffic |

---

## Revision Checklist

- [ ] Explain what the "ideal internet" assumed and how the real internet differs
- [ ] Define what a middlebox is and give at least 3 examples
- [ ] Explain why middleboxes are both "an abomination" and "a practical necessity"
- [ ] Describe how a firewall filters packets and what fields it can inspect
- [ ] Explain Deep Packet Inspection (DPI)
- [ ] Work through a firewall rule ordering problem (like the Alice/Bob/Trudy example)
- [ ] Explain why rule order matters in a firewall
- [ ] Distinguish between stateless and stateful firewalls with an example
- [ ] Explain what a load balancer does and how it uses a virtual IP
- [ ] Know that load balancers handle new TCP connections after failover (YES) but not existing ones (NO)
- [ ] Explain what a gratuitous ARP is and its role in load balancer failover
- [ ] Explain what a WAN accelerator is and where it sits in the network
- [ ] Describe the three WAN acceleration techniques: TCP ACK spoofing, compression, caching/deduplication
- [ ] Explain IP tunneling and how encapsulation works
- [ ] Describe how a commercial VPN works and what the trust implication is
- [ ] Explain the IPv4 address depletion problem that motivated NAT
- [ ] Know the four port ranges and their names (0, 1-1023, 1024-49151, 49152-65535)
- [ ] Distinguish NAT (IP only, L3) from PAT (IP:Port, L3+L4)
- [ ] Distinguish static (admin-defined) from dynamic (router-chosen) translation
- [ ] Explain Static NAT: how outbound and inbound packets are translated
- [ ] Work through the static NAT example (10.2.2.33 <-> 73.8.2.33)
- [ ] Explain Static PAT use cases: multiple servers on one IP, non-standard ports, port forwarding
- [ ] Explain how Dynamic PAT works, including the translation table
- [ ] Explain why Dynamic PAT re-randomizes source ports
- [ ] Explain why Dynamic PAT is unidirectional and what happens when an external host tries to connect
- [ ] Explain Dynamic NAT and how it differs from Dynamic PAT (dedicated IP vs shared IP, port untouched)
- [ ] Explain why Active FTP needs Dynamic NAT (not Dynamic PAT)
- [ ] Trace through Active FTP: control channel (TCP/21) and data channel (TCP/20)
- [ ] Know the disadvantage of Dynamic NAT (pool exhaustion, unpredictable IP assignment)
- [ ] Explain Policy NAT: matching both SRC and DST to decide translation
- [ ] Explain Twice NAT: translating both SRC and DST of a packet
- [ ] List the three main objections against NAT (violates layering, misuses ports, violates end-to-end argument)
- [ ] State why IPv6 makes NAT unnecessary
