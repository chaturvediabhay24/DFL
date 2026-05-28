# Requirements Modeling — Session 4

## 1. Why Model Requirements?

- Converts **textual requirements** into **structured, visual models**
- Helps **validate requirements early** before design begins
- Acts as a **bridge** between business needs and system design
- Clarifies **system functionality** for all stakeholders
- Most common approaches:
  - **Use Case Modeling** — captures functional behavior
  - **Conceptual/Domain Modeling** — captures domain structure

---

## 2. Use Case Modeling

### What It Is
- A technique to **capture functional requirements from a user's perspective**
- Focuses on **what** the system does, not **how** it's implemented
- Describes an **end-to-end process**: from when a user starts using the system for a purpose until they are done

### Core Constructs

| Construct | Description | Notation |
|---|---|---|
| **Use Case** | A sequence of actions (including variants) that a system performs, interacting with actors | Oval / ellipse |
| **Actor** | A role played by an entity (person or system) that interacts with the subject | Stick figure or `<<actor>>` box |
| **System Boundary** | Represents the boundary between the system and external actors | Rectangle enclosing use cases |

### Use Case Diagram — Shopping System Example

```
[Customer] -----> ( Process Sale ) <----- [Payment Authorization Service]
[Cashier]  -----> ( Process Return )
[Manager]  -----> ( Analyze Activity ) <----- [<<actor>> Tax Calculator]
[<<actor>> Sales Activity System] ---> (Manage Users) <--- [<<actor>> HR System]
[System Administrator] --> ( ... )
```

- Actors can be human (Customer, Cashier, Manager) or external systems (Tax Calculator, HR System)
- Human actors: stick figures; System actors: boxes with `<<actor>>` stereotype

---

## 3. Identifying Actors and Use Cases

**Process:**
1. **Identify Actors** — external entities that initiate interaction
2. **Identify Goals** — what does each actor want to achieve?
3. **Define Use Cases** — one use case per goal

**ATM Example:**

| Actor | Goal | Use Case |
|---|---|---|
| Customer | Withdraw money | Withdraw Cash |
| Customer | View account balance | Check Balance |
| Bank Server | Verify account | Validate Account |

---

## 4. Use Cases as Requirements

- Use cases **capture functional requirements** — system attributes associated with a system operation are documented in a use case
- **Not all requirements** can be captured by use cases:
  - System attributes that **span use cases** (e.g., performance, security) are documented as **supplementary requirements**

---

## 5. Use Case Template (Fully-Dressed Format)

| Field | Description |
|---|---|
| **Use Case Number** | EU-xxxx (EU = Essential Use Case) |
| **Use Case Name** | Start with a Verb (e.g., "Withdraw Cash") |
| **Overview** | Brief purpose description |
| **Type** | Priority: primary / secondary / optional |
| **Actors** | List all actors; mark initiator with `[initiator]`, primary with `[primary]` |
| **Properties** | Special requirements: Performance, Security, Other |
| **Tech/Data Constraints** | Technical or data constraints and variations |
| **Pre-condition** | Condition that must be true when the use case starts |
| **Flow — Main Flow** | Numbered steps for the success path |
| **Flow — Subflows** | Breakdown of specific main flow steps |
| **Flow — Alternate Flows** | Exception/alternative paths (with post-conditions if different) |
| **Post Condition** | Condition true after successful completion |
| **Cross References** | Links to related use cases or requirements |

---

## 6. Scenarios (Use Case Instances)

- A **scenario** is a specific sequence or path through a use case
- Each use case has **multiple scenarios**:
  - **Main flow** = main success scenario
  - **Alternative / exception scenarios** = other paths

- A **use case instance** is one execution of a scenario (terms are often used interchangeably)

**Example — "Withdraw Cash":**

| Scenario | Path |
|---|---|
| Scenario 1 | Valid card and balance → Cash dispensed |
| Scenario 2 | Invalid PIN → Access denied |
| Scenario 3 | Insufficient balance → Transaction cancelled |

---

## 7. Use Case Model vs. Use Case vs. Scenario

| Concept | Description | Example |
|---|---|---|
| **Use Case Model** | Complete diagram showing all actors and use cases | ATM System Diagram |
| **Use Case** | A single functional goal | Withdraw Cash |
| **Scenario** | A specific flow of steps in that use case | Invalid PIN scenario |

---

## 8. Levels of Rigor

| Level | Description |
|---|---|
| **Brief** | One paragraph summary of functionality |
| **Casual** | Multiple paragraphs covering multiple scenarios |
| **Fully-dressed** | Structured, detailed description of all scenarios (use the template above) |

---

## 9. Essential vs. Concrete Use Cases

| Type | Description | When Used |
|---|---|---|
| **Essential** | Describes functionality in **implementation-independent** terms | Requirements phase — must always be essential |
| **Concrete** | Describes external functionality in **system-dependent** terms (e.g., refers to UI) | Design phase — documents observable behavior of subsystems |

> Requirements-level use cases MUST be essential — no UI terms, no implementation details.

---

## 10. Use Case Modeling Tips

- Use diagrams for **presentation only** — focus on text descriptions (essential use cases)
- Writing essential use cases: **focus on intent**
  - Keep user interface terms out
  - Ask "what is the goal?" not "how does the user click?"
- Write **"black-box"** use cases — do not describe internal operations (e.g., "stores to database")
- Focus only on **interactions between system and actors** — ignore interactions between actors
- A use case diagram should:
  - Contain only use cases at the **same level of abstraction**
  - Include only **required actors**

---

## 11. What Makes a Good Use Case?

- Describes an activity that yields an **observable result of value** to an actor
- Can describe an **elementary business process** — a sequence of tasks to handle a business event
- Use cases are typically **not single steps or single low-level actions**

---

## 12. Organizing Use Cases — Three Relationships

### 12.1 Generalization / Specialization

- A **specialized use case** inherits the behavior (sequence of actions) of its parent(s)
- It can **override** or **add to** parent behavior
- A specialized use case can be used **anywhere the general use case is expected**

**Example — Payments System:**
```
Cashier --> ( Make Payment )
               ^          ^
    (hollow arrow = inherits)
( Make Cash Payment )   ( Make Card Payment ) <-- [<<actor>> Card Validation System]
```
- Both "Make Cash Payment" and "Make Card Payment" specialize "Make Payment"

### 12.2 Include (`<<include>>`)

- A use case includes another use case at a **specified location** in its flow
- Used to **avoid duplicating** the same flow across multiple use cases
- The **included use case is NOT stand-alone** — it has no meaning by itself

**Example — Library System:**
```
Clerk --> ( Check Out )
              |           |
    <<includes>>    <<includes>>
              v           v
  ( Database Retrieval )  ( Check Fines ) <-- [<<actor>> Accounting System]
```
- "Check Out" always includes "Database Retrieval" and "Check Fines"

### 12.3 Extend (`<<extends>>`)

- A use case **extends a base use case** by adding optional or conditional behavior at **extension points**
- The **base use case CAN stand alone** (unlike include)
- Extension occurs only under **certain conditions**
- Used to separate **optional behavior** from mandatory behavior

**Example — Payments System:**
```
Clerk --> ( Make Payment )
               ^
          <<extends>>
               |
         ( Print Receipt )
```
- "Print Receipt" optionally extends "Make Payment" at an extension point

**Include vs. Extend — Quick Comparison:**

| | `<<include>>` | `<<extends>>` |
|---|---|---|
| Base use case standalone? | Yes | Yes |
| Included/extending standalone? | No | Yes |
| When does it happen? | Always (mandatory) | Conditionally (optional) |
| Purpose | Reuse common behavior | Add optional behavior |

---

## 13. Full Example — Caribbean Fantasy Tours (CFT)

**Problem:** CFT online booking system allows customers to book cruises, view ports, excursions, ship rooms, and facilities.

**Use Case Model (simplified):**
```
Customer --> ( Get Cruise Information )
                  ^  <<extends>>  Get Ship Room Price Packages
                  ^  <<extends>>  Get Ship Facilities Information
                  ^  <<extends>>  Get Ports Information
                                       | <<includes>>
                                  ( Get Onshore Excursion Information )
Customer --> ( Book Cruise )
                  ^  <<extends>>
             ( Book Onshore Excursion )
                       | <<includes>>
                  Get Onshore Excursion Information
Customer --> ( Get Booked Cruises )
                  ^  <<extends>>  Book Cruise (can trigger from here too)
```

**Use Case EU-0001 — Get Cruise Information:**

| Field | Content |
|---|---|
| UC Number | EU-0001 |
| Name | Get Cruise Information |
| Overview | Gets info about cruises available for booking; base use case for retrieving cruise-specific info |
| Actors | Customer [initiator, primary] |
| Precondition | System displays list of cruises by name available for booking |
| Main Flow | 1. Customer selects cruise from list. 2. System displays brief description with options for additional info. 3. <<extension point>> Get Additional Information |
| Alternate Flow | 3a. User selects option to book this cruise. 3b. User selects option to get list of available cruises. |
| Post Condition | True |
| Cross Refs | Get Ports Information, Get Ship Room Price Packages, Get Ship Facilities Information, Book Cruise |

**Use Case EU-0002 — Get Ports Information:**

| Field | Content |
|---|---|
| UC Number | EU-0002 |
| Name | Get Ports Information |
| Overview | Retrieves detailed info about ports visited on a cruise; each port provides list of onshore excursions |
| Actors | Customer [initiator, primary] |
| Precondition | Customer selected option to view cruise info consisting of a sequence of ports |
| Main Flow | 1. Customer requests ports info. 2. System displays list of ports with onshore excursion indicator. 3. Customer requests info on a specific port. 4. <<include>> Get Onshore Excursion Information. 5. Customer selects option to go back (EU-0001). |
| Alternate Flow | 6. Customer selects option to get list of available cruises |
| Post Condition | True |
| Cross Refs | Get Cruise Information, Get Onshore Excursion Information |

---

## 14. Domain / Conceptual Modeling

### From Use Cases to Domain Models

| | Use Cases | Domain Models |
|---|---|---|
| **Describes** | What happens (behavior) | What exists (structure) |
| **Language** | Verbs (actions) | Nouns (things) |
| **Diagram type** | Use case diagram | UML class diagram |

**Flow:** Use Case Models (Detailed) → Domain/Conceptual Model → Design Models

### What Is a Domain Model?

- Structuring of **domain concepts** — identifies problem concepts and their relationships
- Uses **structural models** (UML class diagrams) to depict structure
- Key questions:
  - What **concepts** exist in this domain?
  - What are their **attributes**?
  - What are their **relationships**?
- **IMPORTANT:** Domain model concepts are NOT software objects — they are a "visual dictionary" of domain concepts

### Deriving Domain Elements from Use Cases

**Example — "Withdraw Cash" use case:**

| Use Case Step | Derived Domain Concepts |
|---|---|
| Actor: Customer inserts card into ATM | Customer, Card, ATM |
| System: Validates card and PIN | Card, Account, Validation (as process) |
| Actor: Enters amount to withdraw | Amount (attribute), Transaction |
| System: Dispenses cash and updates account | Cash, Transaction, Account |
| System: Prints receipt | *(Ignore — UI detail)* |
| Postcondition: Account balance updated | Account.balance (attribute) |

---

## 15. Guidelines for Domain Modeling

1. **Extract nouns** from use cases
2. **Identify attributes** and relationships
3. **Validate** for completeness and realism

### Moving from Use Case to Conceptual Classes

From the "Process Sale" use case, key nouns extracted become conceptual classes:

```
Register | Item | Store | Sale
Sales LineItem | Cashier | Customer | Manager
Payment | Product Catalog | Product Specification
```

> Note: These are domain concepts, NOT software classes.

---

## 16. Attributes in Domain Model

- Show only **simple, primitive types** as attributes (e.g., date, time, amount, name)
- **Connections to other concepts** must be shown as **associations**, not attributes

**Example:**
```
Payment
-----------
date : Date
time : Time
amount : Money
```

### Access Modifiers (UML)

| Symbol | Meaning |
|---|---|
| `-` | Private |
| `+` | Public |
| `/` | Derived (computed) attribute |
| `[0..1]` | Optional attribute |
| `{readOnly}` | Read-only constraint |

**Examples:**
```
Sale                  Math                      Person
-----------           -----------               -----------
- dateTime : Date     + pi : Real = 3.14        firstName
- / total : Money       {readOnly}              middleName : [0..1]
                                                lastName
```

---

## 17. Associations

- A relationship between two conceptual classes
- Has an **association name** (label), often with a **direction reading arrow** (arrow has no other meaning)
- Has **multiplicity** on each end

**Example:**
```
POST  ---[1]--- Records-current ---[1]--- Sale
```

### Multiplicity Notation

| Notation | Meaning |
|---|---|
| `*` | Zero or more ("many") |
| `1..*` | One or more |
| `1..40` | One to forty |
| `5` | Exactly five |
| `3, 5, 8` | Exactly three, five, or eight |
| `0..1` | Zero or one (optional) |

**Example — Customer rents Videos:**
```
Customer [0..1] ---Rents--- [*] Video
```
- One Customer may rent zero or more Videos
- One Video may be rented by zero or one Customers

---

## 18. Domain Model — Full POS Example

Key concepts and relationships for a Point-of-Sale system:

```
Store (name, address)
  |-- Houses 1..* --> Register (id)
  |                     |-- Works-on --> Cashier (id)
  |-- Used-by * --> Product Catalog
  |                     |-- Contains 1..* --> Product Description (itemID, desc, price)
  |                                               |-- Describes * --> Item
  |-- Stocks 1 --> * Item
  |-- Records-accounts-for --> Ledger
         |-- Records-sale-of --> Sale (dateTime, /total)
                  |-- Captured-on [0..1] --> Register
                  |-- Paid-by 1 --> CashPayment (amountTendered)
                  |-- Is-for 1 --> Customer
                  |-- Contained-in (1..* SalesLineItem, quantity)
```

---

## 19. Common Pitfalls in Domain Modeling

| Mistake | Example | Fix |
|---|---|---|
| Mixing design elements | Added "Database Connector" class | Remove; stay conceptual |
| Wrong multiplicity | Transaction as many-to-many | Use appropriate multiplicity |
| Missing attributes | Transaction had no amount | Add key fields |
| Vague naming | "Info", "DataObj" | Use meaningful names |

---

## 20. Representing Domain Concepts vs. Software Classes

- A domain concept (e.g., `Payment`) and a software class (`Payment`) are **not the same thing**
- The domain concept **inspires** the naming and definition of the software class
- This reduces the **representational gap** — one of the big ideas in object technology

**Example:**
```
Domain Model:               Design Model:
Payment                     Payment
--------                    --------
amount                      o amount: Money
                              getBalance(): Money
   |                              |
   | inspires ---->               |
```

---

## Quick Reference — Use Case Relationships

| Relationship | Notation | Key Rule |
|---|---|---|
| Association (actor-UC) | Line | Actor interacts with use case |
| Generalization | Hollow arrow (child → parent) | Child inherits and may override parent |
| Include | Dashed arrow + `<<include>>` | Base always calls included UC; included is NOT standalone |
| Extend | Dashed arrow + `<<extends>>` | Extension is optional/conditional; base IS standalone |
