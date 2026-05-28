# Session 2: Project Management, Estimation and Scheduling

---

## 1. Why Project Management Matters

Two interdependent aspects of every software project: **Process** and **Project Management**.

| Concern | Problem | PM Solution |
|---|---|---|
| On-Time Delivery | Poor planning, unforeseen issues | Schedules, milestones, contingency plans |
| Budget Control | Scope/complexity overruns | Budgeting and scope control |
| Quality Assurance | Quality shortcuts | Planned testing, code reviews, QA standards |
| Risk Mitigation | Dependency delays, resource issues | Early risk identification and mitigation |
| Resource Optimization | Over/under-utilization | Right skills to right tasks |

---

## 2. Key Phases of Project Management

**Initiation → Planning → Execution → Monitoring → Closure**

### Initiation Phase
- **Purpose:** Define the project at a high level; validate feasibility; align stakeholders
- **Activities:** Develop business case, identify stakeholders, define scope broadly, prepare project charter
- **Deliverables:** Business case document, project charter

### Planning Phase
- **Purpose:** Break scope into manageable parts; establish timelines, costs, resources; identify risks
- **Activities:** Create WBS, develop Gantt/network schedules, budget estimation, risk management planning
- **Deliverables:** Detailed project plan, schedule and resource allocation charts, risk management plan

### Execution Phase
- **Purpose:** Carry out project work as per plan; develop actual software
- **Activities:** Assign tasks, communicate, monitor progress/quality, manage change requests
- **Tools:** Agile sprints, version control, daily standups, issue tracking

### Monitoring & Control Phase
- **Purpose:** Track against the plan; correct deviations early
- **Activities:** Use performance metrics (EV, CPI, SPI), manage scope changes, address risks, QA
- **Output:** Status reports, updated project schedule, change logs

### Closure Phase
- **Purpose:** Formally complete project; conduct post-project review
- **Activities:** Final testing and deployment, documentation handover, lessons learned analysis, release resources
- **Deliverables:** Final project report, user manuals, post-implementation review

---

## 3. Estimation in Software Projects

> "An exact estimate is an oxymoron." Estimates are based on experience (history matters) and expressed as a **range**, not a single number.

### Estimation Do's and Don'ts

- Always give a **range**, never a single number
- Always ask what the estimate will be used for
- **Estimation ≠ Commitment**
- Iteratively increase clarity (Cone of Uncertainty — uncertainty is highest at project start, narrows over time)
- First try to **measure, count, and compute**; estimate only when necessary
- Aggregate independent estimates: **"Wisdom of the Crowds"**

### Cone of Uncertainty
Variability in estimates is very high early in a project and converges as the project progresses. Early estimates can be off by 4x in either direction.

### Over- and Under-Estimation

| Type | Issues |
|---|---|
| **Over-estimation** | Project may not get funded; scope/feature creep; "double-padding" (team + manager both inflate) |
| **Under-estimation** | Quality issues (shortchanging testing); missed deadlines; team morale problems |

---

## 4. Estimation Methodologies

| Method | Description |
|---|---|
| **Top-Down** | High-level estimate based on prior projects or expert judgment |
| **Bottom-Up** | Break into tasks, estimate each, aggregate |
| **Analogous** | Use data from similar past projects |
| **Parametric / Algorithmic** | Use mathematical models (e.g., Function Point Analysis, COCOMO) |

---

## 5. Function Point Analysis (FPA)

### Why FPA?
- Measures software size by **number and complexity of functions**, not lines of code
- Analogy: LOC = square footage of a house; Function Points = number of bedrooms and bathrooms (captures both size and functionality)
- More methodical than LOC counts

### FPA Categories

```
Function Point Analysis
├── Transactional Functional Type
│   ├── External Inputs (EI)
│   ├── External Outputs (EO)
│   └── External Inquiries (EQ)
└── Data Functional Type
    ├── Internal Logical Files (ILF)
    └── External Interface Files (EIF)
```

#### External Inputs (EI)
- User/process inputs that **create or update** data
- Examples: data-entry forms ("Create Customer"), CSV imports, POST/PUT API endpoints, "Check in Book"
- Counting: DET (Data Element Types) = distinct user-recognizable fields; FTR (File Types Referenced) = files referenced/updated; classify Low/Avg/High using DET/FTR thresholds

#### External Outputs (EO)
- Outputs sent **outside** the application that contain **calculations/derived data**
- Examples: monthly sales report, invoice generation, notifications with computed values, API responses with aggregated values
- EO has **higher weight** than EI for equivalent DET/FTR counts

#### External Inquiries (EQ)
- Online queries that **retrieve data with little or no processing**
- Examples: search screens, single-record lookups, simple list displays, lightweight GET APIs
- EQ weights are **lower than EO** (minimal processing)

#### Internal Logical Files (ILF)
- Application-maintained logical data groups (within system boundary)
- Examples: Customer table, Orders, Products, User Accounts, system configurations
- Counting: DET = distinct fields stored; RET (Record Element Types) = sub-groups/record types within the file

#### External Interface Files (EIF)
- **Read-only** logical data used by the application but **maintained externally**
- Examples: external product catalog, shared user identity store, currency rates cache
- Weighted lower than ILF (not maintained by the system)
- If app reads AND writes it → treat as ILF

### FPA Process (5 Steps)

**Step 1: Identify and Classify Functions**
Count business functions per category: Inputs, Outputs, Inquiries, Logical Files, Interface Files

*Bookstore example:*
- Inputs: User Registration, Adding new books
- Outputs: Displaying order confirmation
- Inquiries: Searching for books
- Logical Files: User account details, Book details
- Interface Files: Payment gateway interface

**Step 2: Assign Complexity Weights**

| Program Characteristic | Low | Medium | High |
|---|---|---|---|
| Number of Inputs (EI) | x3 | x4 | x6 |
| Number of Outputs (EO) | x4 | x5 | x7 |
| Inquiries (EQ) | x3 | x4 | x6 |
| Logical Internal Files (ILF) | x7 | x10 | x15 |
| External Interface Files (EIF) | x5 | x7 | x10 |

**Step 3: Calculate Unadjusted Function Points (UFP)**

Sum all (count × weight) for each category.

*Example calculation:*

| Characteristic | Low | Medium | High | Subtotal |
|---|---|---|---|---|
| Inputs | 5×3=15 | 2×4=8 | 3×6=18 | 41 |
| Outputs | 6×4=24 | 6×5=30 | 0×7=0 | 54 |
| Inquiries | 0×3=0 | 2×4=8 | 4×6=24 | 32 |
| Logical internal files | 5×7=35 | 2×10=20 | 3×15=45 | 100 |
| External interface files | 8×5=40 | 0×7=0 | 2×10=20 | 60 |
| **UFP Total** | | | | **287** |

**Step 4: Compute Value Adjustment Factor (VAF) and Calculate Adjusted FP (AFP)**
- VAF = **influence multiplier** based on 14 general system characteristics (data communications, distributed functions, performance, etc.)
- Each characteristic rated 0 (no influence) to 5 (strong influence)
- VAF ranges from **0.65 to 1.35**
- **AFP = UFP × VAF**

*Example: UFP=287, VAF=1.20 → AFP = 287 × 1.20 = **344 FP***

**Step 5: Estimate Effort and Time**
- Calculate based on per-function-point effort (hours per FP, derived from historical data)

---

## 6. Wideband Delphi (Expert Consensus Estimation)

- **Group consensus approach** to estimation
- Process:
  1. Present experts with a problem and response form
  2. Conduct group discussion, collect **anonymous** opinions
  3. Share aggregated results as feedback
  4. Repeat discussion until consensus is reached

| Advantages | Disadvantages |
|---|---|
| Easy, inexpensive | Difficult to repeat |
| Utilizes expertise of several people | May fail to reach consensus |
| Does not require historical data | All experts may share the same bias |

---

## 7. Scheduling & Tracking

### Why Partition Your Project?
- Decompose into manageable chunks — **Divide & Conquer**
- Two main causes of project failure:
  1. Forgetting something critical
  2. Ballpark estimates becoming fixed targets

### How to Schedule (4 Steps)
1. **Identify "what"** needs to be done → Work Breakdown Structure (WBS)
2. **Identify "how much"** (size) → Size estimation techniques
3. **Identify dependencies** between tasks → Dependency graph / network diagram
4. **Estimate total duration** → The actual schedule

---

## 8. Work Breakdown Structure (WBS)

**Definition:** A checklist of all work that must be accomplished to meet project objectives. Lists major outputs and the team/individuals responsible.

### WBS Principles
- **Deliverable-oriented** (focus on outputs, not activities)
- **Hierarchical:** Project → Major Deliverables → Sub-deliverables → Work Packages → Tasks
- **Mutually exclusive** elements (no overlap)
- **8–80 rule:** Work packages should be 8–80 hours of effort
- Include **non-development work**: requirements, QA, deployment, training, project management

### WBS Example (Retail Website Outline)
```
0.0 Retail Web Site
1.0 Project Management
2.0 Requirements Gathering
3.0 Analysis & Design
4.0 Site Software Development
    4.1 HTML Design and Creation
    4.2 Backend Software
        4.2.1 Database Implementation
        4.2.2 Middleware Development
        4.2.3 Security Subsystems
        4.2.4 Catalog Engine
        4.2.5 Transaction Processing
    4.3 Graphics and Interface
    4.4 Content Creation
5.0 Testing and Production
```

### WBS Types

| Type | Also Called | Focus | Used By |
|---|---|---|---|
| **Process WBS** | Activity-oriented | Phases/activities (Requirements, Design, Testing) | Project Manager |
| **Product WBS** | Entity-oriented | Components/deliverables (Financial engine, DB, UI) | Engineering Manager |
| **Hybrid WBS** | — | Lifecycle phases at top, component/feature specifics within | Both |

### Work Packages (Tasks)
- Discrete tasks with definable end results
- **"One-to-two" rule:** Typically 1–2 persons for 1–2 weeks
- Basis for monitoring/reporting; tied to budget items (charge numbers) and resource assignments
- Ideally short, but not so small as to cause micro-management

### WBS Techniques
- **Top-Down:** Start from overall project, decompose downward
- **Bottom-Up:** Start from individual tasks, group upward
- **Analogy:** Base on similar past project's WBS
- **Rolling Wave:** 1st pass goes 1–3 levels deep; add more detail later as requirements clarify
- **Post-its on a wall:** Collaborative brainstorming technique

---

## 9. Scheduling Activities

Two main tools:
1. **Gantt Chart**
2. **Network Techniques** (CPM, PERT)

---

## 10. Gantt Chart

- Displays activities or events plotted against **time or cost**
- Used to show project progress or define work needed to reach an objective
- Can include: activity listing, duration, scheduled dates, progress-to-date

**Structure:** Each task shown as a horizontal bar. Parent tasks (phases) shown as summary bars. Milestones shown as diamonds.

| Advantages | Disadvantages |
|---|---|
| Easy to understand | Only a vague description of the project |
| Easy to change | Does NOT show interdependency of activities |
| | Cannot show effects of early/late start |

---

## 11. Network Techniques

**Precedence network diagram:** A graphic model showing the sequential relationships between key events/tasks in a project. Clearly communicates the plan to the team and client.

Two main network techniques:
- **CPM** – Critical Path Method
- **PERT** – Program Evaluation and Review Technique

---

## 12. Critical Path Method (CPM)

### What CPM Answers
1. What is the **total project duration**?
2. By how much will the project be delayed if any activity takes N extra days?
3. How long can certain activities be delayed **without** delaying the overall project?

### Critical Path Definition
- The **longest path** (in time) through the precedence network
- Tasks on the critical path have **zero slack** — any delay here delays the entire project
- Non-critical tasks have slack (float) — they can be delayed within limits

### Slack Time
- **Slack time = LS – ES** (or equivalently LF – EF)
- LS = Latest Start, ES = Earliest Start
- LF = Latest Finish, EF = Earliest Finish
- Tasks on the critical path have **Slack = 0**

### CPM Example

| Task | Description | Duration | Dependencies |
|---|---|---|---|
| A | Architecture & design strategy | 9 | Start |
| B | Decide on number of releases | 5 | A |
| C | Develop acceptance test plan | 7 | A |
| D | Develop customer support plan | 11 | B, C |
| E | Final sizing & costing | 8 | D |

**Network:**
```
Start → A(9) → B(5) → D(11) → E(8) → End
              ↘ C(7) ↗
```

**Paths:**
- A → B → D → E = 9+5+11+8 = **33 time units**
- A → C → D → E = 9+7+11+8 = **35 time units** ← Critical Path

**Critical Path = A – C – D – E (35 units)**
**Critical Tasks = A, C, D, E**
**Non-Critical = A – B – D – E** (Task B has 2 units of slack)

### ES/EF/LS/LF Table

| Task | Duration | Depend | ES | EF | LS | LF | Slack |
|---|---|---|---|---|---|---|---|
| A | 9 | none | 0 | 9 | 0 | 9 | 0 |
| B | 5 | A | 9 | 14 | 11 | 16 | **2** |
| C | 7 | A | 9 | 16 | 9 | 16 | 0 |
| D | 11 | B,C | 16 | 27 | 16 | 27 | 0 |
| E | 8 | D | 27 | 35 | 27 | 35 | 0 |

> Task B slack = LS – ES = 11 – 9 = **2 time units**

---

## 13. Integrating Estimation with Scheduling and Tracking

### From FP to Schedule (Example)
- FPA yields **143 FP** → 143 × 20 hrs/FP = **2860 hours** total effort
- Team of 5 devs at 150 hrs/week: 2860 / 150 ≈ **19 weeks**
- Add ~20% buffer for uncertainties → **~23 weeks total**

### Tracking with Earned Value Management (EVM)

| Metric | Definition |
|---|---|
| **PV** (Planned Value) | Budget allocated for work planned to be done by now |
| **EV** (Earned Value) | Budget allocated for work actually completed |
| **AC** (Actual Cost) | Actual money spent so far |
| **CPI** | Cost Performance Index = EV / AC (>1 = under budget) |
| **SPI** | Schedule Performance Index = EV / PV (>1 = ahead of schedule) |

**Example:** After 4 weeks, PV = $40K, EV = $35K, AC = $38K
- CPI = 35/38 ≈ 0.92 (over budget)
- SPI = 35/40 = 0.875 (behind schedule)

---

## 14. Summary

| Topic | Key Takeaway |
|---|---|
| Project Management | 5 phases: Initiation, Planning, Execution, Monitoring, Closure |
| Estimation | Always give ranges; estimation ≠ commitment; cone of uncertainty |
| Over/Under Estimation | Both cause problems — aim for calibrated estimates |
| FPA | Size by function type (EI, EO, EQ, ILF, EIF) × complexity weight × VAF |
| Wideband Delphi | Group consensus, anonymous rounds, iterative |
| WBS | Deliverable-oriented hierarchy; 8-80 hour packages |
| Gantt Chart | Visual timeline; simple but no dependency tracking |
| CPM | Find critical path (longest path); compute slack for non-critical tasks |
| EVM | Track PV, EV, AC; compute CPI and SPI to assess project health |
