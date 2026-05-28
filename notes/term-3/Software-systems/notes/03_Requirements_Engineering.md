# Requirements Engineering — Revision Notes
**Software Systems | Session 3 | Y. Raghu Reddy, IIIT Hyderabad**

---

## 1. Why Requirements Engineering?

**Requirement**: A statement that specifies what a system must do or qualities it must possess to satisfy stakeholder needs.

### Project Failure Causes (by % contribution)
| Factor | Contribution |
|---|---|
| Requirements / Planning | 30–40% |
| Project Management / Estimation | 20–30% |
| People & Organization | 15–25% |
| Technical / Design | 10–20% |
| Testing / Quality Assurance | 5–15% |
| Change Management / Org. Adoption | 5–15% |

> Requirements failures are the **single largest cause** of project failure.

---

## 2. Sources of Requirements

- Stakeholders
- Existing systems / artifacts
- External constraints / regulations
- Market research
- Technical & organizational sources

The **environment** for the requirements definition process varies by system type:
- Highly constrained systems (e.g., Missile Guidance) → fewer requirements come from stakeholders
- Unconstrained systems (e.g., Online Ordering System) → most requirements gathered from stakeholders

---

## 3. Defining the Scope

- Narrow the scope by defining a more precise problem
  - List everything the system might do
  - Exclude items if too broad → narrow scope
  - Add high-level goals if too narrow

**Example (University Registration System):**
- Broad scope: browsing courses + registering + fee payment + room allocation + exam scheduling
- Narrowed scope: browsing courses + registering + fee payment (room allocation and exam scheduling become a separate system)

---

## 4. Starting Points for Software Projects

|  | Requirements must be determined | Clients have produced requirements |
|---|---|---|
| **New development** | A | B |
| **Evolution of existing system** | C | D |

---

## 5. Types of Requirements

Two broad categories:
1. **Functional Requirements (FR)**
2. **Non-Functional Requirements (NFR)**

There may also be: Domain, Business, Transition requirements.

---

## 6. Functional Requirements

- Specify **behaviours / services** — describe *what* the system should do
- Written as: "The system shall ..."
- Clearly specifying FRs helps **reduce scope creep**

**Examples (e-commerce):**
- "The system shall allow users to add items to their shopping cart."
- "The system shall process refunds when requested by authorised personnel."

**Example (library system) — f1: findBooks**
- Input: borrower's id
- Output: list of books the borrower has currently checked out

---

## 7. Non-Functional Requirements (NFR)

- Characteristics that **cannot be expressed as functions** — specifies **qualities / constraints**
- Clearly specifying NFRs helps **measure** how well the system is doing what it's supposed to do

**Categories:**
- Quality attributes: Performance, Security, Usability, Reliability, etc.
- Constraints: Technical, Business, Process

**Examples (e-commerce):**
- "The system shall support at least 100,000 concurrent users." (Performance)
- "The website shall be available 99.99% of the time." (Availability)

---

## 8. Requirements Engineering Activities

```
Requirements Engineering
├── Requirements Development
│   ├── Elicitation
│   ├── Analysis
│   ├── Negotiation
│   ├── Documentation
│   └── Validation
└── Requirements Management
    ├── Change control
    ├── Version control
    ├── Status tracking
    └── Tracing
```

---

## 9. Requirements Elicitation (Gathering)

### 9.1 Interviews
- **Structured** (fixed questions) vs **Unstructured** (open-ended)
- Ask about: specific details, stakeholder's vision, alternative ideas, other sources, diagrams
- Example: Interview product owner and lead developer to capture API requirements.

### 9.2 Observation / Contextual Inquiry
- Ethnographic methods, task analysis, capturing **tacit knowledge**
- Techniques:
  - Read documents and discuss requirements with users
  - **Shadowing**: follow users as they do their work
  - Session videotaping
- Example: Observe staff using legacy LMS to identify pain points for migration.

### 9.3 Workshops / Joint Application Development (JAD)
- Facilitated sessions; experienced **moderator** resolves conflicting requirements
- Process:
  1. Appoint an experienced moderator
  2. Arrange attendees around a table
  3. Decide on a "trigger question"
  4. Each participant writes an answer and passes it to their neighbour
- Example: Cross-functional workshop to define semester grading workflow.

### 9.4 Prototyping
- **Paper prototype** (simplest): sequence of pictures shown to users to explain system flow
- **UI mock-up** (most common): mock-up of the system's UI
  - Written in a rapid prototyping language
  - Does NOT perform computations, access databases, or interact with other systems
  - May prototype just one specific aspect of the system

### Example: Requirements Gathering Table Structure

| Req ID | Title | Description | Priority | Type | Source | Acceptance Criteria | Notes/Dependencies |
|---|---|---|---|---|---|---|---|
| R-001 | User Registration | Allow users to create account via email + password, with email verification | H | Functional | Product Owner | User can register, receive verification email, activate account | Depends on SMTP; GDPR checkbox |
| R-002 | User Login | Authenticate via email/password; support "Forgot Password" | H | Functional | Product Owner | Login with valid credentials; password reset within 5 min | Rate-limit login attempts |

---

## 10. Requirements Analysis

**Purpose:**
- Clearly understand user requirements
- Detect **inconsistencies**, **ambiguities**, and **incompleteness**

Incompleteness and inconsistencies → resolved through further discussion with end-users and customers.

### 10.1 Inconsistent Requirements
Some part of the requirement **contradicts** another part.

**Example (e-commerce — Product Availability):**
- Req A: Products displayed as available even if only 1 left (to create urgency)
- Req B: Users cannot add to cart if stock < 5
→ These directly contradict each other.

### 10.2 Incomplete Requirements
Some requirements have been **omitted** — possibly due to oversight.

**Example (e-commerce — Authentication):**
- Vague: "Implement user authentication."
- Complete: "Users log in with email/password. After 3 failed attempts, account locked for 30 minutes. Password reset link sent to registered email."

---

## 11. Requirements Quality Control

**Goal:** Check that identified requirements represent all stakeholder expectations and do not contradict each other.

**Process:** Validation and Verification (V&V) activities; metrics can be used.

**Benefits of good quality requirements:**
- Less rework
- Fewer unnecessary features
- Lower cost
- Faster development
- Fewer miscommunications
- Reduced scope creep
- Better deliverables
- Minimised change control

---

## 12. Verification vs Validation

| | Validation | Verification |
|---|---|---|
| Question | "Am I building the **right product**?" | "Am I **building** the product right?" |
| Checks against | Higher-level work products / stakeholder authorities | Standards and conditions for this type of product |
| Focus | Requirement qualities that affect the **product** | Requirement qualities that affect the **development process** |
| Done by | **Stakeholders** | **Analysts** (mainly) |

### V&V Flow in Requirements Engineering
1. **Elicitation** → Analysis & Specification → **Validation**
2. At each stage, if verification fails → Reviews & Inspections → Requirements Document (Verified)
3. If validation fails → Prototypes & User Feedback → Requirements Document (Validated)
4. Central step: **Negotiation & Prioritisation**

---

## 13. Desired Qualities in Requirements

### Checked by Validation (stakeholder-focused):
- **Correct** — only user representative can determine
- **Feasible** — reality check on what can/cannot be done technically or within cost
- **Necessary** — each requirement traceable back to its origin
- **Prioritised** — function of value provided to the customer

### Checked by Both V&V:
- **Complete** — no missing requirements
- **Consistent** — no contradictions
- **Unambiguous** — one interpretation only

### Checked by Verification (analyst-focused):
- **Concise**
- **Traceable**
- **Non-redundant**
- **Organised**
- **Conformant to standards**
- **Verifiable** — how do you know if the requirement was implemented properly?

> Look at requirements **as a whole** AND at a **statement level**.

---

## 14. Bad Requirements — Examples and Fixes

### Bad Requirement #1
> *"The product shall provide status messages at regular intervals not less than every 60 seconds."*

Problems:
- **Incomplete** — what are the status messages? How displayed?
- **Ambiguous** — what part of the product? What is a "regular interval"?
- **Not verifiable**

Fixed version:
- 1.1: The Background Task Manager shall display status messages in a designated UI area at intervals of 60 ±10 seconds.
- 1.2: If processing normally, display percentage completed.
- 1.3: Display a message when the background task is completed.
- 1.4: Display an error message if the background task stalls.

### Bad Requirement #2
> *"The product shall switch between displaying and hiding non-printing characters instantaneously."*

Problems:
- **Not feasible** — computers cannot do anything instantaneously
- **Incomplete** — conditions which trigger state switch are missing
- **Ambiguous** — "non-printing character" undefined

Fixed version:
> "The user shall be able to toggle between displaying and hiding all HTML markup tags in the document being edited with the activation of a specific triggering condition."
(Note: "triggering condition" is left for design — not over-specified)

### The Specification Trap
Overly complex language (e.g., British Airways pilot role memo) leads to ambiguity. Keep requirements **simple and atomic**.

---

## 15. Quantifying Requirements

NFRs must be **measurable**. Process:
1. **Quality Concept** (abstract, e.g., reliability)
2. **Measurable Quantity** (define metric, e.g., mean time to failure)
3. **Count from Design** (realization, e.g., count crashes per hour)

### Quantifiable NFR Properties:
- Auditability, Capacity, Configurability (Internationalisation, Personalisation, Variability)
- Correctness (Accuracy, Precision, Currency)
- Dependability (Availability, Reliability, Robustness, Safety, Security, Survivability)
- Efficiency, Interoperability
- Performance (Response time, Latency, Throughput, Schedulability)

### Example Quantification Table

| Quality | Metric |
|---|---|
| Speed | Transactions/sec, response time, screen refresh time |
| Size | Kbytes, number of RAM chips |
| Ease of Use | Training time, number of help frames |
| Reliability | Mean-time-to-failure, probability of unavailability, rate of failure |
| Robustness | Time to restart after failure, % events causing failure |
| Portability | % target-dependent statements, number of target systems |

---

## 16. Difficulties and Risks in Requirements Analysis

| Problem | Mitigation |
|---|---|
| Requirements change rapidly | Incremental development; build flexibility; regular reviews |
| Attempting to do too much | Document problem boundaries early; estimate time carefully |
| Conflicting sets of requirements | Brainstorming, JAD sessions, competing prototypes |
| Hard to state requirements precisely | Break into simple sentences; review carefully; early prototypes |

---

## 17. Software Requirements Specification (SRS)

**Purpose:**
- Systematically organise requirements arrived at during analysis
- Document requirements properly

**SRS = Black-Box Specification:**
- System treated as a black box — internal details unknown
- Only external (input/output) behaviour documented
- Focuses on **WHAT** needs to be done, not HOW
- Serves as a **contract** between the development team and the customer

### Forms of SRS Documentation:
1. **Natural Language**
2. **Structured Natural Language**
3. **Formal Specifications**

---

## 18. Properties of a Good SRS Document

- Correctness
- Completeness
- Consistency
- Unambiguous / Precise
- Verifiable / Testable
- Modifiable / Maintainable
- Traceable
- Ranked for priority
- Understandable by stakeholders
- Feasible / Realistic
- Concise / Organised
- Uniform terminology and style
- Include functional and non-functional requirements
- Include acceptance criteria and success metrics
- Versioning and change history

---

## 19. Types of SRS Documentation

### 19.1 Natural Language SRS

Simple prose statements. Easy to write but can be vague.

| Field | Content |
|---|---|
| System | Online Bookstore — Customer Purchasing |
| Scope | Customers can browse, search, add books to cart, and checkout |
| N-L1 | The system shall allow customers to create an account using email and password |
| N-L2 | Customers should be able to search for books by title, author, or ISBN; results sorted by relevance |
| N-L3 | The system shall process payments via credit card and display order confirmation |
| N-L4 | The system should be fast and user friendly |

> N-L4 is an example of a **bad NFR** — "fast" and "user friendly" are not measurable.

### 19.2 Structured Natural Language SRS

Uses fixed fields for each requirement — improves clarity, testability, traceability.

**User Story template:**
> As a [Type of USER], [Function to Perform (some goal)] so that [Business Value (some reason)]

Example:
> "As a user, I can indicate folders not to backup so that my backup isn't filled up with things I don't need saved."

**Structured field template:**

| Field | Content |
|---|---|
| System | Online Bookstore — Customer Purchasing |
| ID | R-001 |
| Title | User Registration |
| Statement | The system shall allow a new customer to register using a unique email and password |
| Preconditions | None |
| Postconditions | A customer account record is created; verification email queued |
| Priority | High |
| Acceptance Criteria | Given valid unused email + password meeting policy, when user submits, account created and verification email sent within 30 seconds; duplicate emails rejected with HTTP 409 |
| Notes | Structured fields improve clarity, testability, and traceability |

**Specification templates:**
- `The <System_name> shall <behavior> if <conditions>, where <quality factor>.`
- `Upon <conditions>, the <System_name> shall <behavior> where <quality factor>.`
- Example: "The ATM shall reject withdrawal requests if the amount requested is not divisible by 20."
- `The system_name shall produce <output> for use by <nodes>, if <conditions>, using <inputs/outputs> where <quality factor>.`
- Example: "The ATM shall produce a receipt for use by bank patrons if a transaction is completed. The receipt will include a unique transaction code, amount, date, time and location."

### 19.3 Formal SRS

Mathematical/logical notation. Most precise, least ambiguous.

**Example (Online Bookstore — Shopping Cart Module):**

| Field | Specification |
|---|---|
| Types | BOOK = {isbn: String, title: String, price: Real}; CART = sequence of BOOK |
| State | cart: CART; total: Real; Invariant: total = Σ{b ∈ cart} b.price |
| Operation: AddBook | Precondition: true; Input: b: BOOK; Postcondition: cart' = cart++[b] ∧ total' = total + b.price |
| Operation: GetTotal | Precondition: true; Output: total = Σ{b ∈ cart} b.price |
| Error Handling | AddBook: if b.price < 0 → error BAD_PRICE |
| Invariants | ∀b ∈ cart: b.price ≥ 0 |

---

## 20. Formal Specification Techniques (FSTs)

**Definition:** A FST consists of a formal specification language and mechanisms for deriving consequences from statements in the language.

**FSTs can be used to:**
- Prove that a specification is implementable
- Prove that an implementation satisfies its specification
- Prove properties of a system without executing it

### Properties FSTs can investigate:
| Property | Meaning |
|---|---|
| **Correctness** | Model captures desired functionality; refinement consistent with spec |
| **Safety** | Model does not allow undesired behaviour |
| **Liveness** | Model will eventually do certain desired things |
| **Security** | Unauthorised access to sensitive data not permitted by model |
| **Timeliness** | Modelled behaviour consistent with timing constraints |

### Levels of Rigor

| Level | Description | When to use |
|---|---|---|
| **0** | No use of FSTs — plain natural language | Routine, well-understood applications |
| **1** | Use of concepts and notation from discrete mathematics | Documentation only |
| **2** | Formalized specification languages with some supporting tools | Gaining insight into problem/solution |
| **3** | Full formal languages with animators, theorem proving, proof checking tools | Critical systems requiring design justification |

**Level 1 Example** (Calculate mean salary):
- input: empsals: list of N
- output: avg: R
- Pre-condition: empsals ≠ emptylist
- Post-condition: avg = (Σ empsals(i)) div #empsals

**Level 2 Example** uses Z notation (formal schema boxes with types, state, and operations).

### Types of FSTs (dimensions of classification):
- **Presentation mode**: textual, visual
- **Specification approach**: model-oriented, property-oriented
- **Specification perspective**: process-oriented, state-oriented, object-oriented
- **Semantic basis**: operational semantics, denotational semantics, formal logic
- **Analysis approach**: model checking, theorem proving, animation/simulation
- **Applicable system types**: transformational, reactive

### Proof Obligations
- **What they depend on:** problem being tackled, expressive power of formal language, structure of solution
- **Discharge depends on:** analytical power of the FST, structure of the solution

---

## 21. Summary

| Key Takeaway | Detail |
|---|---|
| Requirements define system needs | Both what it does (FR) and how well (NFR) |
| Gathering techniques | Interviews, Observation, JAD workshops, Prototyping |
| Analysis goals | Find inconsistencies, ambiguities, incompleteness |
| Quality via V&V | Validation = right product; Verification = built right |
| SRS = contract | Between dev team and customer; black-box spec |
| SRS formats | Natural language → Structured NL → Formal spec |
| Formal specs | Used to prove correctness, safety, liveness, security, timeliness |
| Quantify NFRs | Abstract quality → measurable metric → count from design |
