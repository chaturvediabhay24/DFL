# Week 8 — The Internet

> **Lecturer:** Prof. Ankit Gangwal, IIIT-H
> **Topic:** Internet — what it is, key networking concepts, and how it actually works step by step

---

## Table of Contents
1. [Origins of the Internet](#1-origins-of-the-internet)
2. [What is the Internet?](#2-what-is-the-internet)
3. [Key Concepts in Networking](#3-key-concepts-in-networking)
4. [How Does the Internet Work? — Step by Step](#4-how-does-the-internet-work--step-by-step)
5. [Revision Checklist](#revision-checklist)

---

## 1. Origins of the Internet

The Internet started as **ARPANET** — a US military/academic research project in the late 1960s.

- The very first message ever sent over a network was on **29 October 1969** at 2100 hours
  - The log book entry reads: *"Talked to SRI host to host"* — the first ever host-to-host communication
  - The program was running after sending a "host dead message to IMP" (Interface Message Processor)
- The **IMP (Interface Message Processor)** was the special hardware box used to connect computers to the early network — think of it as the world's first router

By **May 1973**, ARPANET had grown to a full logical map connecting universities, research labs, and military sites across the USA — Stanford, UCLA, MIT, Harvard, Carnegie Mellon, and many more were all connected.

> **Analogy:** ARPANET was like the first highway — built for a small number of government vehicles, but it laid the foundation for the massive road network (the Internet) we use today.

---

## 2. What is the Internet?

### The simple definition

The Internet is a **publicly accessible network of interconnected computer networks**.

- It transmits data using **packet switching** and standard **Internet Protocols (IP)**
- It is literally a **network of networks** — many smaller networks (home, university, business, government) all connected together
- These networks carry all kinds of information and services — web pages, emails, video calls, etc.

### Best-effort delivery

The Internet is a **best-effort packet delivery service**.

- This means: the Internet will *try its best* to deliver your data packets to the destination
- But it gives **no guarantees** — packets can be lost, delayed, or arrive out of order
- Think of it like regular post: you put a letter in the box and it *usually* arrives, but there are no promises

> **Analogy:** If you drop 100 identical envelopes in a post box at the same time and send them to the same address, some might arrive early, some late, and a few might get lost entirely. The postal service does its best — that is exactly what the Internet does with your data packets.

### Power at the Edge

A core design philosophy of the Internet:

- **End-to-end principle:** Complicated communication logic (checking if data arrived, re-sending lost data, etc.) should happen at the **endpoints** (your computer, the server) — NOT in the middle of the network
  - This keeps the core network simple and fast
  - The "smart" work happens at the edges

- **Programmability:** Because the end hosts handle the smart stuff, anyone can build new services on top of the Internet without changing the network itself
  - You don't need to "ask" the Internet to support your new app — you just write the code and your computer handles it
  - This is why new apps and services can appear overnight

- Over time, end hosts (your laptop, phone, etc.) became **powerful and everywhere** — which makes this approach work perfectly

### Routing: How does traffic find its way?

The Internet is a network of many smaller networks (shown as clouds/trees in the slides).

- **Announcing a route:** Each network tells its neighbours *"IIIT's computers are reachable via me"* — like putting up signposts
- **Forwarding traffic:** Routers read these signposts and pass your data in the right direction — the red dashed line in the slides shows the actual path a packet travels
- **Withdrawing a route:** If a network goes down, it broadcasts *"IIIT is NOT reachable this way anymore"* — routers update their maps and find alternative paths

> **Analogy:** Think of the Internet like a city road network. Each junction (router) has a map of which direction to go for each destination. If a road closes, the map gets updated and traffic is rerouted.

---

## 3. Key Concepts in Networking

### 3.1 Protocol Layering (Abstraction)

Networks are too complex to manage all at once, so we break them into **layers**. Each layer has one job.

**The rules of layering:**
- Each layer **only** uses services from the layer directly below it
- Each layer **only** provides services to the layer directly above it
- The **interface** between layers hides the details — one layer does not need to know how the layer below works
- You can change one layer (e.g., upgrade physical cables to fibre) without breaking the others

**The four layers (simplified model shown in slides):**

| Layer | What it does | Example |
|---|---|---|
| **Application** | The actual app/service | Web browser, email |
| **App-to-App Channels** | Connecting two applications | TCP, UDP |
| **Host-to-Host Connectivity** | Getting data from one machine to another | IP |
| **Link Hardware** | The physical wire/wifi | Ethernet, WiFi |

> **Analogy:** Think of a company sending a physical parcel. The person who writes the letter does not care how the van is driven. The van driver does not care what is in the parcel. Each layer does its job without worrying about the others.

### 3.2 The IP Suite and the Hourglass Model

The Internet Protocol (IP) suite shows exactly how protocols stack up. The key insight is the **hourglass shape**:

```
  FTP  HTTP  NV  TFTP     <-- Many applications on top
       TCP   UDP          <-- Transport layer
          IP              <-- THE NARROW WAIST (just one protocol!)
   NET1  NET2  ... NETn   <-- Many physical network types below
```

- **IP is the "thin waist"** — everything above (applications) speaks to IP, and everything below (physical networks) is spoken to by IP
- This is why IP is the universal glue of the Internet — any application can run over it, and it can run over any physical network
- IP **facilitates interoperability** — your packet can travel over Ethernet at home, then over fibre optic cable, then over WiFi at a coffee shop, all in one journey

### 3.3 HTTP — HyperText Transfer Protocol

This is the application-layer protocol your browser uses to ask for and receive web pages.

**A real HTTP request:**
```
GET /path/to/resource/HTTP/1.1
Host: www.cs.xyz.edu
User-Agent: Mozilla/5.0
CRLF
```
- `GET` = "please give me this resource"
- `Host` = which website you are asking
- `User-Agent` = what software is making the request
- `CRLF` = blank line signalling end of headers

**A real HTTP response:**
```
HTTP/1.1 200 OK
Date: Wed, 11 Aug 2021 09:28:28 GMT
Server: Apache/2.4.41
Last-Modified: Fri, 06 Aug 2021 04:46:59 GMT
Content-Length: 23
CRLF
Site under construction
```
- `200 OK` = success
- The body (`Site under construction`) is the actual content of the page

### 3.4 Layer Encapsulation

When you send an HTTP request, each layer **wraps** the data with its own header before passing it down. At the receiving end, each layer **unwraps** its header. This is called encapsulation.

**Example — User A sends "Get index.html" to User B:**

```
Application layer:    [Get index.html]
App-to-App layer:     [Connection ID] [Get index.html]
Host-to-Host layer:   [Src/Dst IP] [Connection ID] [Get index.html]
Link Hardware layer:  [Link Address] [Src/Dst IP] [Connection ID] [Get index.html]
```

Each layer adds information needed at that level. The network in the middle only looks at what it needs (IP addresses) and does not open the rest.

### 3.5 End Hosts vs Routers

- **End hosts** (your computer, a web server) run **all** layers: HTTP, TCP, IP, and Ethernet
- **Routers** in the middle only run the **lower layers**: IP and Ethernet
  - Routers do NOT look at TCP or HTTP — they only care about IP addresses to decide where to send the packet next

> **Analogy:** A delivery courier only cares about the address on the parcel, not what is inside. Routers are the couriers of the Internet.

### 3.6 Sockets and Process Communication

When two programs on different computers want to talk:

- **Socket** = the interface that the Operating System gives to a program so it can send/receive data over the network
  - Think of a socket as the "plug socket" a program plugs into to access the network

**How does a message find the right program?**

Two pieces of information are needed:

1. **IP Address (32-bit)** — finds the right **machine**
   - Written as four numbers: `1.2.3.4`
   - Identifies which computer on the Internet

2. **Port Number (16-bit)** — finds the right **program** on that machine
   - Written as a single number: `80` (web), `53` (DNS), `22` (SSH)
   - One machine can run many programs, each listening on a different port
   - Range: 0 to 65535

> **Analogy:** The IP address is like a building's street address. The port number is like the flat/apartment number. Both together tell the postman exactly where to deliver the letter.

### 3.7 URI — Uniform Resource Identifier

A URI is a unique string of characters that **identifies** a resource — either a real-world thing (a person, a book) or an information resource (a web page).

**URI syntax:**
```
URI = scheme:[//authority]path[?query][#fragment]
authority = [userinfo@]host[:port]
```

**Real example broken down:**
```
https://john.doe@www.example.com:123/forum/questions/?tag=networking&order=newest#top

scheme    = https
authority = john.doe@www.example.com:123
  userinfo  = john.doe
  host      = www.example.com
  port      = 123
path      = /forum/questions/
query     = tag=networking&order=newest
fragment  = top
```

**There are two types of URI:**

| Type | Full Name | What it does | Example |
|---|---|---|---|
| **URN** | Uniform Resource Name | Gives a unique *name* only — does not help you find it | ISBN of a book |
| **URL** | Uniform Resource Locator | Gives a *name AND a way to find/retrieve it* | A web address |

- A **URN** is like a person's national ID number — uniquely identifies them, but does not tell you where they live
- A **URL** is like a full postal address — uniquely identifies a place AND tells you how to get there

### 3.8 URL — Uniform Resource Locator

A URL is the most common type of URI — it gives you both the name and the method to retrieve a resource.

**URL example broken down:**
```
https :// www. mywebsite .com /info/ index.html
  |         |       |        |      |        |
Transfer  Sub    Second-  Top-   Dir   Filename
protocol domain  Level   Level  path  with ext
              Domain   Domain
              (SLD)    (TLD)
```

- **Transfer protocol** (`https`): how to communicate (HTTP, HTTPS, FTP etc.)
- **Subdomain** (`www`): optional prefix for a sub-part of the domain
- **SLD** (`mywebsite`): the main name you registered
- **TLD** (`.com`): the top-level category (`.com`, `.org`, `.edu`, `.in` etc.)
- **Directory path** (`/info/`): the folder on the server
- **Filename** (`index.html`): the specific file — this part is **case sensitive**
- Together, **SLD + TLD = the domain name** = `mywebsite.com`

### 3.9 DNS — Domain Name System

**The problem:** Computers use IP addresses (like `143.75.19.3`). Humans prefer names (like `www.iis.se`). Something needs to translate between them.

**The solution:** DNS — the "phone book" of the Internet. It translates human-friendly hostnames into IP addresses.

**DNS is a hierarchy — like a tree:**

```
                    .               <-- Root (the top of everything)
          /    /    |    \
        com   org  edu   net        <-- Top-Level Domains (TLDs)
       /   \        |
     abc   imdb    ucla             <-- Second-Level Domains (SLDs)  e.g. ucla.edu
                  / | \
                cs mail www         <-- Subdomains  e.g. cs.ucla.edu
               /
             pc15                   <-- Individual host  e.g. pc15.cs.ucla.edu
```

- You read domain names from right to left in the hierarchy
- `pc15.cs.ucla.edu` means: host `pc15`, in subdomain `cs`, in domain `ucla`, under TLD `edu`

### 3.10 DHCP — Dynamic Host Configuration Protocol

**The problem:** Every device on a network needs a unique IP address. Typing one in manually every time is impractical.

**The solution:** DHCP — a server that automatically gives out ("leases") IP addresses.

When your laptop joins a WiFi network, it asks the DHCP server: *"Can I have an address please?"* The DHCP server gives it:
- A unique **IP address** (e.g. `192.168.1.5`)
- A **Subnet mask** (e.g. `255.255.255.0`) — tells your computer which other addresses are on the same local network
- A **Default gateway** (e.g. `192.168.1.1`) — the router's address, where to send traffic going outside your local network
- **DNS server addresses** (e.g. `192.168.1.1` or `8.8.4.4`) — where to ask for hostname-to-IP translations

> **Analogy:** DHCP is like a hotel receptionist who assigns you a room number when you check in, gives you a key, tells you where the restaurant is (default gateway), and tells you where the information desk is (DNS server).

### 3.11 Link-Local Addresses

**What if DHCP fails?**

If a device cannot get an IP address from DHCP and no one has manually assigned one, it assigns itself a **link-local address**:

- Range: `169.254.0.0` to `169.254.255.255` (that is 65,536 possible addresses)
- Written in CIDR notation as `169.254.0.0/16`

**Key properties of link-local addresses:**
- **Non-routable** — packets with these addresses cannot travel beyond your local network segment
- They allow two devices on the same physical link to communicate even when there is no DHCP or router
- Assigned automatically via **APIPA (Automatic Private IP Addressing)**

**Validation with ARP:** Before using a link-local address, the device sends an ARP broadcast to check that no other device on the network is already using it.

> **Analogy:** If no one has given you an official room number at the hotel, you just write your name on a piece of paper and stick it to a spare room — but you can only receive visitors who are already in the same building.

### 3.12 ARP — Address Resolution Protocol

**The problem:** IP works with IP addresses, but to actually send a packet on a local network (Ethernet, WiFi), you need the **MAC address** (the hardware address). How do you find out what MAC address corresponds to a given IP address?

**The solution:** ARP — it broadcasts a question to everyone and waits for the right device to answer.

**How ARP works (example from slides):**

Three devices on a network:
- Laptop: MAC `71-65-F7-2B-08-53`, IP `1.2.3.4`
- Phone: MAC `0C-C4-11-6F-E3-98`, IP `1.2.3.6`
- Access Point: MAC `1A-2F-BB-76-09-AD`, IP `1.2.3.5`

The laptop wants to send something to IP `1.2.3.6` but does not know the MAC address:

1. **Laptop broadcasts:** *"Who has IP address 1.2.3.6? Respond with your MAC address!"*
   - Destination MAC in this broadcast = `FF:FF:FF:FF:FF:FF` (the broadcast address — everyone reads it)

2. **Phone responds:** *"I have IP 1.2.3.6! My MAC address is 0C-C4-11-6F-E3-98"*

3. **Laptop saves this** in its ARP table (a local cache of IP → MAC mappings) so it does not have to ask again

> **Analogy:** ARP is like standing in a room and shouting: "Who is called John Smith?" — the person with that name replies, and now you know what they look like (their MAC address).

---

## 4. How Does the Internet Work? — Step by Step

This is a detailed walkthrough of what happens when you type `http://www.iis.se` in your browser. The slides walk through this as a numbered example.

### The Setup (from the slides)

| Device | IP Address | MAC Address | Notes |
|---|---|---|---|
| Your computer | `192.168.1.5` | `00:19:a7:51:cd:9f` | Subnet: `255.255.255.0`, Gateway: `192.168.1.1`, DNS: `192.168.1.1` |
| Home Router (LAN side) | `192.168.1.1` | `00:13:fe:19:c7:9e` | |
| Home Router (WAN side) | `115.20.97.114` | `00:27:9c:11:fa:1a` | |
| ISP's Router | `115.20.97.113` | `00:a5:33:8b:6c:cd` | |
| DNS Server | `8.8.4.4` | — | |
| Web Server (www.iis.se) | `143.75.19.3` | — | |

---

### Step 1 — Browser Asks the OS to Set Up a Connection

```
Web Browser → OS: "Dear OS, set up a TCP session for me to www.iis.se on port 80"
OS → Web Browser: "OK, I will set up a session for you!"
```

The application (browser) does not deal with network details itself — it asks the OS.

---

### Step 2 — DNS Resolution (Finding the IP Address of www.iis.se)

This is the longest part, involving many sub-steps.

#### Step 2a — Check the Local DNS Cache

Before asking anyone, the computer checks its **DNS cache** (a local memory of recent hostname lookups):

```
DNS Cache on Computer:
DNS name     | IP address
(empty)      | (empty)

Result: Cache miss — need to ask a DNS server!
```

#### Step 2b — Build the DNS Query Packet

The computer prepares a packet to send to the DNS server:

```
Source MAC:       00:19:a7:51:cd:9f      (computer's MAC)
Destination MAC:  ???                     (don't know yet!)
Source IP:        192.168.1.5
Destination IP:   192.168.1.1            (the DNS server = home router)
Source Port:      21874/UDP              (random high port)
Destination Port: 53/UDP                (DNS always uses port 53)

DNS Query: What is the IP address of www.iis.se?
```

Note: DNS uses **UDP port 53** — UDP because DNS queries are small and fast, and TCP's handshake overhead is not worth it for a short question.

#### Step 2c — Check the ARP Table

The computer needs the router's MAC address to send the packet. It checks its ARP table:

```
ARP Table on Computer:
MAC address  | IP address
(empty)      | (empty)

Result: ARP table empty — must use ARP to find router's MAC!
```

The DNS packet is held in memory (a "packet queue") while the MAC address is found.

#### Step 2d — ARP Broadcast to Find the Router

The computer broadcasts an ARP request to every device on the local network:

```
Source MAC:       00:19:a7:51:cd:9f
Destination MAC:  FF:FF:FF:FF:FF:FF    (broadcast — everyone reads this)

Message: ARP Query — "Whoever has IP 192.168.1.1, reply with your MAC address"
```

#### Step 2e — ARP Reply from the Router

The home router sees the broadcast and replies directly to the computer:

```
Source MAC:       00:13:fe:19:c7:9e    (router's LAN MAC)
Destination MAC:  00:19:a7:51:cd:9f   (computer's MAC)

Message: ARP Reply — "I have IP 192.168.1.1 and my MAC is 00:13:fe:19:c7:9e"
```

The computer saves this in its ARP table:

```
ARP Table (updated):
MAC address          | IP address
00:13:fe:19:c7:9e    | 192.168.1.1
```

Now the waiting DNS packet can have its destination MAC filled in.

#### Step 2f — Send the DNS Query to the Router

The DNS packet is now complete and sent to the home router:

```
Source MAC:       00:19:a7:51:cd:9f
Destination MAC:  00:13:fe:19:c7:9e
Source IP:        192.168.1.5
Destination IP:   192.168.1.1
Source Port:      21874/UDP
Destination Port: 53/UDP

DNS Query: IP address of www.iis.se?
```

#### Step 2g — Home Router Checks Its Own DNS Cache

The home router checks if it already knows the answer:

```
Home Router DNS Cache:
DNS name  | IP address
(empty)   | (empty)

Result: Cache miss — must forward to the real DNS server (8.8.4.4)
```

#### Step 2h — Home Router Forwards DNS Query to Internet DNS Server

The home router now prepares its own DNS query and sends it out to the Internet. Notice how the IPs and MACs change — the router swaps in its WAN (public) IP:

```
Source MAC:       00:27:9c:11:fa:1a    (router's WAN MAC)
Destination MAC:  00:a5:33:8b:6c:cd   (ISP router's MAC)
Source IP:        115.20.97.114        (router's WAN/public IP)
Destination IP:   8.8.4.4             (DNS server on the Internet)
Source Port:      9735/UDP
Destination Port: 53/UDP

DNS Query: IP address of www.iis.se?
```

#### Step 2i — DNS Query Travels Across the Internet

The query is routed hop-by-hop across the Internet (through multiple routers) until it reaches the DNS server at `8.8.4.4`. At this stage, only the IP headers matter — MAC addresses change at every hop.

#### Step 2j — DNS Server Responds

The DNS server at `8.8.4.4` knows the answer and sends a response:

```
Source IP:        8.8.4.4
Destination IP:   115.20.97.114
Source Port:      53/UDP
Destination Port: 9735/UDP

DNS Reply: www.iis.se has IP address 143.75.19.3
```

The home router receives this and saves it in its DNS cache:

```
Home Router DNS Cache (updated):
DNS name   | IP address
www.iis.se | 143.75.19.3
```

#### Step 2k — Home Router Sends DNS Reply to Your Computer

The router forwards the DNS answer back to your computer:

```
Source IP:        192.168.1.1
Destination IP:   192.168.1.5
Source Port:      53/UDP
Destination Port: 21874/UDP

DNS Reply: www.iis.se has IP address 143.75.19.3
```

Your computer saves this in its DNS cache too:

```
Computer DNS Cache (updated):
DNS name   | IP address
www.iis.se | 143.75.19.3
```

**DNS resolution is complete!** Your computer now knows that `www.iis.se = 143.75.19.3`.

---

### Step 3 — TCP 3-Way Handshake (Setting Up a Connection)

Before sending the HTTP request, TCP must establish a reliable connection. This takes exactly **three messages** — hence "3-way handshake".

> **Analogy:** Like calling someone on the phone. You call (SYN), they pick up and say "hello?" (SYN-ACK), you say "hello, it's me" (ACK). Now you are both ready to talk.

#### Step 3a — Computer sends TCP SYN

The computer sends a "synchronise" message to the web server, saying "I want to connect":

```
From computer to home router:
Source MAC:       00:19:a7:51:cd:9f
Destination MAC:  00:13:fe:19:c7:9e
Source IP:        192.168.1.5
Destination IP:   143.75.19.3
Source Port:      14756/TCP
Destination Port: 80/TCP          (port 80 = HTTP)

Message: TCP SYN
```

The home router applies **NAT (Network Address Translation)** when forwarding this to the internet — it replaces the private IP `192.168.1.5` with the public IP `115.20.97.114`:

```
NAT: Translate 192.168.1.5 → 115.20.97.114
(and keeps a table so it can reverse this when the reply comes back)
```

The packet continues to the web server at `143.75.19.3`.

#### Step 3b — Web Server Replies with TCP SYN-ACK

The web server says "yes, I am ready to connect":

```
Source IP:        143.75.19.3
Destination IP:   115.20.97.114
Source Port:      80/TCP
Destination Port: 14756/TCP

Message: TCP SYN-ACK
```

The home router receives this, applies **NAT in reverse** (translates `115.20.97.114` back to `192.168.1.5`), and forwards it to the computer.

#### Step 3c — Computer Sends TCP ACK

The computer confirms: "Got it, connection is established":

```
Source IP:        192.168.1.5
Destination IP:   143.75.19.3
Source Port:      14756/TCP
Destination Port: 80/TCP

Message: TCP ACK
```

Again, NAT translates the private IP to public before it goes onto the Internet.

**TCP connection is now established!** The "three-way handshake" is done.

---

### Step 4 — The Browser Talks to the Web Server (HTTP GET)

Now that a TCP connection is set up, the browser can ask for the web page using HTTP:

```
Source IP:        192.168.1.5
Destination IP:   143.75.19.3
Source Port:      14756/TCP
Destination Port: 80/TCP

Message: HTTP GET www.iis.se
```

(After NAT, the Source IP becomes `115.20.97.114` when it goes over the Internet.)

The web server at `143.75.19.3` receives this HTTP GET request and sends back the HTML content of the page. The browser renders it and you see the website!

---

### The Complete Journey — Summary

```
[1] Browser asks OS: "Connect me to www.iis.se:80"
[2] DNS: Translate "www.iis.se" → 143.75.19.3
    [2a] Check DNS cache → miss
    [2b] Build DNS query (port 53/UDP)
    [2c] Check ARP table for router MAC → miss
    [2d] ARP broadcast: "Who has 192.168.1.1?"
    [2e] Router replies with its MAC
    [2f] Send DNS query to router
    [2g] Router checks its DNS cache → miss
    [2h] Router sends DNS query to 8.8.4.4 over Internet
    [2i] Query routed across Internet to DNS server
    [2j] DNS server replies: "www.iis.se = 143.75.19.3"
    [2k] Router forwards DNS reply to computer
[3] TCP 3-Way Handshake with 143.75.19.3
    [3a] Computer → Server: SYN (via NAT)
    [3b] Server → Computer: SYN-ACK (via NAT)
    [3c] Computer → Server: ACK (via NAT)
[4] HTTP GET request → Web server sends back the page
```

---

## Key Formulas and Numbers to Remember

| Thing | Value |
|---|---|
| IP address size | 32 bits (IPv4), written as `a.b.c.d` |
| Port number size | 16 bits (range: 0 to 65535) |
| DNS port | 53 (UDP) |
| HTTP port | 80 (TCP) |
| HTTPS port | 443 (TCP) |
| MAC address format | 6 bytes, e.g. `00:19:a7:51:cd:9f` |
| ARP broadcast address | `FF:FF:FF:FF:FF:FF` |
| Link-local address range | `169.254.0.0 – 169.254.255.255` |
| Link-local CIDR | `169.254.0.0/16` (65,536 addresses) |

---

## Revision Checklist

- [ ] I can explain what the Internet is in plain English (network of networks, packet switching, publicly accessible)
- [ ] I know what ARPANET was and roughly when the first host-to-host communication happened (1969)
- [ ] I understand what "best-effort delivery" means and why the Internet offers no guarantees
- [ ] I can explain the end-to-end principle — why complex logic lives at the endpoints, not the network core
- [ ] I understand why the Internet's programmability allowed new services to emerge freely
- [ ] I can explain route announcing, forwarding, and withdrawing with an analogy
- [ ] I understand protocol layering — each layer uses only the layer below and serves only the layer above
- [ ] I know the four layers: Application, App-to-App (Transport), Host-to-Host (Network), Link Hardware
- [ ] I can explain the hourglass model — IP is the narrow waist that connects many apps above and many networks below
- [ ] I know what an HTTP GET request looks like and what a 200 OK response contains
- [ ] I understand layer encapsulation — how each layer wraps data with a header
- [ ] I know the difference between end hosts (run all layers) and routers (run only lower layers)
- [ ] I can explain what a socket is and why it is needed
- [ ] I know that IP addresses (32-bit) identify machines and port numbers (16-bit) identify processes
- [ ] I can write and parse a URI using the syntax: `scheme://[userinfo@]host[:port]/path[?query][#fragment]`
- [ ] I know the difference between a URN (name only, e.g. ISBN) and a URL (name + how to find it)
- [ ] I can label all parts of a URL: protocol, subdomain, SLD, TLD, path, filename
- [ ] I understand DNS as a hierarchical phone book: Root → TLDs → SLDs → Subdomains → Hosts
- [ ] I can trace a full DNS resolution: cache miss → ARP → ARP reply → DNS query over UDP/53 → DNS reply
- [ ] I know what DHCP gives to each client: IP address, subnet mask, default gateway, DNS server
- [ ] I know what link-local addresses are (`169.254.0.0/16`), when they are used, and that they are non-routable
- [ ] I know what APIPA stands for and that ARP is used to validate a link-local address before using it
- [ ] I can describe ARP step by step: broadcast with `FF:FF:FF:FF:FF:FF`, unicast reply, save to ARP table
- [ ] I can walk through all 4 steps of "how the Internet works" in the slide example (DNS + ARP + TCP handshake + HTTP GET)
- [ ] I understand the TCP 3-way handshake: SYN → SYN-ACK → ACK
- [ ] I know what NAT does — translates private IPs (`192.168.x.x`) to a public IP when going to the Internet
- [ ] I know DNS runs on UDP port 53 and HTTP runs on TCP port 80
