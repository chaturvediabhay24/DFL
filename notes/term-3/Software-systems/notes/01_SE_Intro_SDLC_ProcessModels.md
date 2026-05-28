# Software Systems — Session 1: SE Intro, SDLC & Process Models

**Course:** MDS302 | IIIT Hyderabad | Instructors: Y. Raghu Reddy & Karthik Vaidhyanathan

---

## 1. Course Overview

By the end of this course you should be able to:
- Understand the lifecycle of software and various process models
- Model and build software using a specific development lifecycle
- Assess and improve software quality
- Understand the use of AI in software development

**Topics covered:** Requirements, Modeling, Architecture & Patterns, Low-Level Design & Patterns, Refactoring, Testing, Deployment & Maintenance, Engineering AI Systems

---

## 2. Exploratory (Build-and-Fix) Programming

- Early programmers used a **build-and-fix** (exploratory) style:
  - Write initial code quickly
  - Test it; if not satisfactory, fix and repeat
  - Stop when satisfied

**Flow:** Initial Coding → Build/Testing → [Not satisfied] → Modify/Fix Code → (loop back) → [Satisfied] → Done

### Problems with Exploratory Style

- Works only for very small programs
- Large programs become unmaintainable
- Time and effort grow **exponentially** with program size
- Engineering approach scales much better than exploratory for large/complex systems

---

## 3. Programs vs. Software Products

| **Programs** | **Software Products** |
|---|---|
| Usually small | Large |
| Author is sole user | Large number of users |
| Single developer | Team of developers |
| Lacks proper UI | Well-designed interface |
| Lacks documentation | Well documented, user manual prepared |
| Ad hoc / exploratory development | Systematic development |

---

## 4. Why Engineer Software Systems?

- Ad hoc approach breaks down as software size increases
- Large complex systems require a **systematic approach** because:
  - Complexity and difficulty grow exponentially with size
  - No single person can understand the entire system
  - Requires teamwork
  - Must achieve sufficient quality (maintainability, usability, etc.)

**Engineering principles needed:**
- **Decomposition** — break the system into smaller parts
- **Abstraction** — hide irrelevant details

**Tools and methods:** specification, design, UI development, testing, project management

### Scale Example
- Boeing 777: 5,000,000+ lines of code
- Top-level game (e.g., WoW): 1,000,000+ SLOC
- 1 SE writes ~120,000 SLOC/year → a 2M SLOC game needs ~17 SEs

**Key insight:** Large software requires **Design**, **Teamwork**, **Communication**, and **Process**.

---

## 5. Fundamental Principles in Engineering Software Systems

### 5.1 Decomposition

**Definition:** Break a complex system into smaller, manageable parts (modules, components, functions) that can be developed, understood, and maintained independently.

**Purpose:** Reduce complexity, enable parallel work, improve testability and reuse.

**Types:**
- **Functional decomposition:** Split by features/behaviors (e.g., auth, billing)
- **Layered decomposition:** Separate concerns by layer (UI, business logic, data)
- **Modular/component decomposition:** Self-contained modules or services

### 5.2 Abstraction

**Definition:** Hide irrelevant details and expose only the essential features needed at a particular level of reasoning.

**Purpose:** Manage complexity, improve readability, enable reuse, reduce coupling.

**Structure:**
```
High Level View (WHAT, not HOW)
        |
  [Abstraction Barrier: Interface/API]
        |
Low Level View (implementation details — hidden from user)
```

**Examples:**
- Functions/methods: expose behavior, hide implementation
- Classes/objects: public API vs. private fields/methods
- Modules/APIs: services with well-defined contracts
- Abstract data types: stacks, queues (what they do, not how)

---

## 6. The Software Engineer's Role

**Daily questions a software engineer must answer:**
- What does the customer need?
- How will users interact with the system?
- What OS, language, hardware to use?
- What is the overall system structure?
- What code to write?
- How to organise the team effectively?
- Can we deliver on time?

**Must work with:** customers, end users, domain experts, engineers from other disciplines, and fellow software engineers.

**Key skill:** Communication

**Technical breadth:** Programming languages (Java, C++, Python, Ruby, PHP), UML, SQL, design patterns, testing, software architecture, Agile/SCRUM, version control (SVN, CVS), GUI, databases, networks, concurrency, etc.

### Real-World Process Failure: Knight Capital Group (Aug 2012)
- **What happened:** Faulty software deployment — configuration error in trading application, poor release management
- **Impact:** $440 million loss in 45 minutes; company sold
- **Lesson:** Even a "small upgrade" in a financial-critical system requires rigorous understanding of **configuration and release process**. Process matters.

---

## 7. Software Development Lifecycle (SDLC)

**Definition:** A framework that formalizes programming, design, teamwork, communication, and process across all phases of software development.

**Why SDLC?**
- Without coordination, engineers work in different directions (one codes, another writes test docs, another defines file structure) — project fails
- Adherence enables accurate status reports

### 7.1 SDLC Phases

| Phase | Key Activities | Keywords |
|---|---|---|
| Feasibility Study | Business case, go/no-go decision | Process |
| Requirements Engineering | Gather, specify, validate needs | Teamwork, Communication |
| Design | Architecture and component plans | Design principles |
| Implementation | Convert design to code | Programming, coding standards |
| Integration & Testing | Integrate modules, run tests | Process, Teamwork |
| Deployment & Maintenance | Release, monitor, improve | Process, Communication, Teamwork |

### 7.2 SDLC Relative Effort (approximate %)

| Phase | Effort |
|---|---|
| Feasibility Study | ~5% |
| Requirements Analysis & Specification | ~10% |
| Design | ~10% |
| Implementation | ~15% |
| Testing | ~20% |
| **Maintenance** | **~45%** |

> **Key point:** Maintenance is the most effort-intensive phase — it costs more than building the product.

---

## 8. SDLC Phases — Details

### 8.1 Feasibility Study
**Aim:** Determine whether the proposed system is viable and worth pursuing.

**Key Activities:**
- Stakeholder interviews & requirements scoping
- Technical feasibility
- Economic (cost-benefit) analysis
- Schedule feasibility & preliminary estimation
- Operational feasibility
- Legal/compliance & risk assessment
- Go/no-go decision

**Types of feasibility:**
- **Technical:** Can it be built with available tech?
- **Economic:** Is it cost-effective?
- **Schedule:** Can it be delivered on time?
- **Legal:** Are there regulatory/IP issues?
- **Operational:** Will it work in the target environment?

### 8.2 Requirements Engineering
**Definition:** Elicit, analyze, specify, validate, and manage stakeholder needs so the system meets its intended purpose and constraints.

**Activities:**
- **Requirements gathering and analysis** — interviews, observation, workshops
- **Requirements specification** — document functional and non-functional requirements (SRS)
- **Verification & validation** — are we building the right thing correctly?
- **Requirements management & change control** — handle changing requirements

### 8.3 Design
**Purpose:** Transform validated requirements into a robust, maintainable, and implementable architecture and detailed design.

**High-level design:**
- Decompose the system into modules/components
- Represent invocation relationships among modules
- Specify constraints

**Detailed design (Low-level design):**
- Data structures, interfaces, and algorithms for each module
- API contracts, sequence/collaboration diagrams, database schemas

### 8.4 Implementation — Building the System
**Goal:** Convert design modules into codified components/classes following coding standards.

**Coding Standards:** Enforce team-wide naming, layout, function size conventions.
- Consistency boosts readability, maintainability, and good practices

**Standard examples:** Python PEP 8, Google Java Style Guide, Microsoft .NET/C# Guidelines, CERT Secure Coding

**End product:** Code modules that can be individually tested (unit testing)

### 8.5 Integration and Testing
- Modules are never integrated all at once ("big bang")
- Integration is done **incrementally in steps**
- After each integration step, the integrated system is tested

**V-Model** — maps development phases to test phases:
```
Requirements          <---->  Acceptance Testing
High-level Design     <---->  System Testing
Low-level Design      <---->  Integration Testing
Implementation        <---->  Unit Testing
```
(Left side = development; Right side = corresponding test; dashed arrows show the relationship)

### 8.6 Maintenance
**Key fact:** Maintenance requires **more effort** than developing the product itself (~45% of total effort).

**Types of maintenance:**
| Type | Description |
|---|---|
| **Preventive** | Defect prevention (code cleanup, refactoring) |
| **Corrective** | Bug fixes |
| **Perfective** | Improvements / enhancements |
| **Adaptive** | Port software to a new environment/OS/platform |

---

## 9. Software Lifecycle — Process Flows

Four types of process flow:

| Flow | Description |
|---|---|
| **(a) Linear** | Sequential: Communication → Planning → Modeling → Construction → Deployment |
| **(b) Iterative** | Phases can loop back (revisit previous phases) |
| **(c) Evolutionary** | Each increment releases a deployable product; repeats the full cycle |
| **(d) Parallel** | Multiple activities happen simultaneously (time-based) |

---

## 10. Process Models — Overview

### Traditional (Plan-Driven) Models
- Classical Waterfall
- Iterative Waterfall
- Evolutionary (Incremental)
- Prototyping
- Spiral
- Rational Unified Process (RUP)

### Agile Models
- eXtreme Programming (XP)
- Scrum
- Crystal
- Feature-Driven Development (FDD)

---

## 11. Traditional SDLC — Waterfall Process

**Flow:** Planning → Requirements → Analysis/Design → Implementation → Test → Release

**Artifacts produced at each phase:**
- Planning: Project Plan, Estimates, Schedule, Risk Mgmt, SRS
- Analysis/Design: GUI Prototypes, Design Document (Structural and Behavioral Diagrams)
- Implementation: Code
- Test: Inspections, Post Mortem
- Release: Deployed product

### Challenges with Waterfall Model

- Heavyweight process for lightweight applications
- Document intensive
- Less flexible design — hard to accommodate changes
- Big bang approach to coding/integration
- Testing short-shifted (often squeezed at the end)
- One-shot delivery opportunity — no incremental feedback
- Limited opportunity for process improvement

---

## 12. Prototyping Process Model

**Idea:** Before full development, build a working prototype to clarify requirements.

**Prototype characteristics:**
- Limited functional capabilities
- Low reliability
- Inefficient performance (it's a "toy implementation")

**Flow:**
```
Requirements Gathering → Quick Design → Build Prototype
                                              ↓
                                  Customer Evaluation of Prototype
                                              ↓
                                  [Not satisfied] → Refine Requirements → (loop)
                                  [Satisfied] → Design → Implement → Test → Maintain
```

**When to use:** When user requirements or technical aspects are not well understood.

---

## 13. Evolutionary Process Model (Incremental Model)

**Also called:** Successive Versions / Incremental Model

**Key idea:**
- System is broken into modules that can be implemented and delivered incrementally
- First develop the **core modules**
- Initial product skeleton is refined by adding new functionalities in successive versions

**Iterative Incremental variant:**
- Each new release may add new functionality AND modify existing functionality
- Characteristics: Incremental Building, User Feedback Driven, Adapts to Change, Continuous new versions

**When to use:** Large problems that can be decomposed into modules; when incremental delivery is acceptable to the customer.

---

## 14. Spiral Model

**Proposed by:** Boehm, 1988

**Key idea:** Each loop of the spiral represents a phase of the software process.

**Four quadrants per loop:**
1. **Determine Objectives** — goals, constraints, alternatives
2. **Identify & Resolve Risks** — risk analysis and prototyping
3. **Develop Next Level of Product** — design, code, test
4. **Customer Evaluation of Prototype** — plan next iteration

**Innermost loop:** System feasibility
**Next loop:** Requirements definition
**Next:** System design, and so on

**No fixed phases** — the phases shown are examples; adapt as needed.

**When to use:** Technically challenging software subject to several kinds of risks.

---

## 15. Comparison of Plan-Driven Process Models

| Model | Best Suited For |
|---|---|
| Iterative Waterfall | Most widely used; suitable only for well-understood problems |
| Prototype | Projects not well understood (user requirements or technical aspects unclear) |
| Evolutionary | Large problems that can be decomposed; incremental delivery acceptable |
| Spiral | Technically challenging products subject to multiple risks |

---

## 16. Plan-Driven vs. Agile Models

| Aspect | Traditional (Plan-Driven) | Agile |
|---|---|---|
| Structure | Sequential, rigid phases | Iterative & Incremental |
| Planning | Detailed upfront planning | Planning based on user stories per sprint |
| Flexibility | Less flexible to changes | Flexible/Adaptive |
| Documentation | Formal, heavy documentation | Working software over documentation |
| Feedback | Limited, at end | Continuous feedback & collaboration |
| Delivery | One-shot or phased big releases | Frequent, incremental releases |
| Change | Difficult to accommodate | Responds to change |

---

## 17. Agile Software Development

**Origin:** Late 1990s — multiple methodologies emerged emphasizing:
- Close collaboration between developers and business experts
- Face-to-face communication (more efficient than written docs)
- Frequent delivery of new deployable business value
- Tight, self-organizing teams
- Handling requirements churn without crisis

**2001:** Snowbird, Utah — practitioners coined "agile" and created the **Agile Manifesto**.

### Applying Agility
- Effective rapid and adaptive response to change
- Effective communication among all stakeholders
- Drawing the customer onto the team
- Team in control of work performed

**Result:** Rapid, incremental delivery of software

**Each iteration (release cycle) covers:** User Stories → Test Plan → Implement → Test → Demo/Deliver → Reflect

### Agile Characteristics
- Incremental development — several releases
- Planning based on user stories
- Each iteration touches **all** lifecycle activities
- Testing: unit testing for deliverables; acceptance tests for each release
- Flexible design — evolution vs. big upfront effort
- Reflection after each release cycle
- Multiple customer-facing presentation opportunities

---

## 18. Agile Process Models

### 18.1 eXtreme Programming (XP)

**Evolution from Waterfall:** Waterfall is sequential/rigid/documentation-heavy → XP is iterative/flexible/customer-collaborative.

**XP cycle (iterative, weeks):**
1. Planning (User Stories)
2. Listening (Feedback)
3. Coding (with TDD)
4. Testing/Review

**Key changes vs. Waterfall:** Structure, Feedback, and Collaboration

### 18.2 Scrum

**Roles:**
- **Product Owner** — defines and prioritizes the product backlog
- **Development Team** — self-organizing team that builds the product
- **Scrum Master** (implied) — facilitates the process

**Artifacts:**
- **Product Backlog** — ordered list of everything the product needs

**The Sprint (time-boxed: 1–4 weeks):**
- Product Planning → Select Items from Backlog
- Sprint Development Work (with Daily Scrum stand-ups)
- → Increment (Shippable Product)
- → Sprint Review + Sprint Retrospective

**Key ceremonies:** Daily Stand-up, Sprint Planning, Sprint Review, Sprint Retrospective

---

## 19. Key Agile Components

| Component | Description |
|---|---|
| **User Stories** | Requirements elicitation tool; used for planning scope |
| **Evolutionary Design** | Design emerges iteratively; allows course correction |
| **Test-Driven Development (TDD)** | Tests written before code; testing is not an end-of-cycle activity |
| **Refactoring** | Small code changes to maintain design quality (reduce design entropy) |
| **Continuous Integration** | Frequent small merges vs. big bang integration |
| **Pair Programming** | Two developers work together; collaborative development |
| **Reflections** | Retrospectives for process improvement |
| **Shared Ownership** | All team members interact with customer and each other |

### Test-Driven Development (TDD) — Red-Green-Refactor Cycle

**Process:**
1. **RED** — Write a failing test (test case for functionality that doesn't exist yet)
2. **GREEN** — Write minimal code to make the test pass
3. **REFACTOR** — Improve the code while keeping tests passing; then repeat

**Example:**
```java
// Step 1: Write failing test
@Test
public void testAddition() {
    Calculator calc = new Calculator();
    assertEquals(7, calc.add(3, 4));  // FAILS — add() doesn't exist yet
}

// Step 2: Write code to make it pass
public int add(int a, int b) { return a + b; }  // PASSES

// Step 3: Refactor — e.g., extract Operation interface for extensibility
public interface Operation { int apply(int a, int b); }
public class Addition implements Operation { public int apply(int a, int b) { return a+b; } }
public class Calculator {
    private final Operation operation;
    public Calculator(Operation op) { this.operation = op; }
    public int calculate(int a, int b) { return operation.apply(a, b); }
}
```

---

## 20. The Process Methodology Spectrum

The spectrum ranges from **More Agile** to **Less Agile (More Plan-Driven)**:

```
More Agile ←————————————————————————————→ Less Agile
Kanban | Scrum | Crystal/Lean | BDD | XP | FDD/DSDM | TSP | RUP | SW-CMM | PSP | Cleanroom | Inch-Pebble
```

> "It's not black and white — the process spectrum spans a range of grey."

---

## 21. CI/CD — Continuous Integration / Continuous Deployment

**Continuous Integration (CI):**
- Developers merge code into the central repository regularly
- Automated builds and testing triggered on every merge

**Continuous Delivery vs. Continuous Deployment:**
- **Continuous Delivery:** Deploy to staging automatically; production deploy is **manual** (requires approval)
- **Continuous Deployment:** Everything is automated — code goes to production automatically after passing tests

**Pipeline:** Source Control → Build (automated) → Staging (integration tests) → Production

---

## 22. DevOps

**Problem:** Developers and Operations teams work in silos, causing friction when moving code to production.

**Solution — DevOps:** Culture and practice of unifying development and operations.

**Developers do:** Designing, coding, testing, bug tracking, code reviews, CI

**Operations do:** Hardware/OS management, monitoring (load, performance, crashes), backups, rollback releases

**Goals of DevOps:**
- Better coordination between Dev and Ops
- Reduce issues when moving changes from development to production
- Configurations as code
- Automation of delivery and monitoring

**DevOps Common Practices:**
- Continuous Integration
- Continuous Delivery
- Infrastructure as Code — test and deploy in containers
- Monitoring and logging
- Microservice architecture
- Communication and Collaboration

---

## Quick Reference: Key Definitions

| Term | Definition |
|---|---|
| SDLC | Framework formalizing all phases of software development |
| Decomposition | Breaking a complex system into smaller, manageable, independent parts |
| Abstraction | Hiding implementation details; exposing only necessary interface |
| SRS | Software Requirements Specification document |
| V-Model | Lifecycle view mapping each development phase to a corresponding test phase |
| TDD | Write tests first, then code to pass them; Red-Green-Refactor cycle |
| Refactoring | Restructuring existing code without changing external behavior |
| CI | Continuous Integration — frequent merges with automated build/test |
| CD | Continuous Delivery (manual deploy) or Continuous Deployment (automated) |
| DevOps | Culture unifying development and operations for faster, reliable delivery |
| Sprint | Time-boxed iteration (1–4 weeks) in Scrum |
| User Story | Short, informal description of a feature from the user's perspective |
