# Session 6: Behavioral Modeling

**Course:** Software Systems (MDS302) | IIIT Hyderabad

---

## 1. Why Behavioral Modeling?

**SDLC flow:** Planning → Requirements → Modeling → UML (Class + Sequence) → **Behavioral Modeling**

- Structural models (class diagrams) show *what* objects exist and their relationships
- Interaction models (sequence diagrams) show *who talks to whom*
- But neither shows *how an object behaves over time* or *what states it can be in*

**The gap:** A class diagram for `Order` shows attributes and methods, but does NOT tell you:
- That `ship()` can only be called after `pay()` has been called
- That `cancel()` is invalid once the order is delivered

**Solution:** Behavioral models — specifically **State Machine Diagrams** and **Activity Diagrams**

---

## 2. Two Levels of Behavioral Modeling in UML

| Level | Diagram Type | What it shows |
|---|---|---|
| Object behavior | State Machine / Statechart | How one object changes state in response to events |
| Inter-object behavior | Interaction / Activity | How multiple objects cooperate in a process |

In UML, **all behavior results from actions of (active) objects**. Objects have internal states (modeled by statecharts) and communicate with each other (modeled by interactions).

---

## 3. State Machine Diagrams

### 3.1 Definition

A **state diagram** (also called statechart or state machine) specifies the life history of an object in terms of:
- The **states** it can be in
- The **events** that cause it to change state
- The **actions/activities** it performs during transitions or while in a state

> A state diagram describes *sequences of states* an object goes through in response to *events*.

### 3.2 Key Concepts

| Concept | Definition | Example |
|---|---|---|
| **Event** | A significant occurrence at a point in time (instantaneous on the app's timescale) | Method call request, timer expiry, button press |
| **State** | A condition of an object during its lifetime; abstraction of attribute values and links | Bank account in "Overdraft" state when balance < 0; Student in "Registered" state after registration |
| **Transition** | Movement from one (source) state to a target state when an event occurs | Student: Registered → NotRegistered on "drops out" |
| **Guard Condition** | A boolean expression that must be true for a transition to fire | `[value >= 200]` |
| **Activity** | Behavior executed in response to an event (on a transition) or while in a state | `get dial tone`, `print("on")` |

**Key rules:**
- A transition **fires** when its event occurs AND its guard (if any) is true
- Source and target states of a transition can be the same (self-transition)
- Events are instantaneous; activities on transitions execute instantaneously too
- Activities inside states (do-activities) execute while the object remains in that state

### 3.3 Object Lifecycle in a State Diagram

Every object follows:
1. **Initialize Object** → enters initial state
2. **Wait for Event** → stays in current state
3. **Handle Event** → transition fires, activity executes
4. **Terminate Object** → reaches final state

This maps directly to state diagram notation:
- **Filled circle** = initial pseudostate (object just created)
- **Filled circle inside ring** = final state (object terminates)

---

## 4. State Diagram Notation — Complete Reference

### 4.1 Basic Elements

| Element | Notation | Description |
|---|---|---|
| Initial state | Solid filled circle (●) | Entry point; no incoming events |
| State | Rounded rectangle with name | A stable condition the object can be in |
| Final state | Circle with filled dot inside (◎) | Object lifecycle ends |
| Transition | Arrow between states | Labeled with event/guard/activity |
| "Top" state | Outer enclosing rounded rectangle | Encloses all states of the machine |

### 4.2 Transition Syntax

```
Event(args) [condition] / activity ^ destination.message(params)
```

- `Event(args)` — the triggering event and its arguments
- `[condition]` — optional guard (boolean, side-effect free)
- `/ activity` — action executed during the transition (instantaneous)
- `^ destination.message(params)` — optional: send a message to another object

**Example:** `lift receiver / get dial tone`
- Event: `lift receiver`
- Activity: `get dial tone`
- No guard

**Example:** `bid [value >= 200] / sell`
- Event: `bid`
- Guard: `value >= 200`
- Activity: `sell`

### 4.3 State Internal Syntax

States can have internal compartments:

```
StateName
-----------
entry / action    ← executed when entering the state
do / activity     ← executed while in the state (ongoing)
exit / action     ← executed when leaving the state
event / action    ← internal transition (no state change)
```

**Example (Lamp):**
```
LampOn
entry / lamp.on()
```

---

## 5. Guards

- Guards are **boolean predicates** on transitions
- Must be **side-effect free** (evaluating them changes nothing)
- Allow **conditional branching** from the same source state on the same event

**Example — Selling state with three outcomes on `bid` event:**

```
Selling --[bid, value < 100]--> (self, reject)
Selling --[bid, value >= 200]--> Happy (sell)
Selling --[bid, 100 <= value < 200]--> Unhappy (sell)
```

Guards must be **mutually exclusive** if they have the same event trigger — otherwise behavior is undefined.

---

## 6. Dynamic Conditional Branching (Choice Pseudostate)

- Represented by a **hollow diamond** (choice point)
- The transition fires first (executing its action), then guards on outgoing branches are evaluated **at the instant the choice point is reached**
- Useful when the branching condition depends on a computed value

**Example:**
```
Selling --bid / gain := calculatePotentialGain(value)--> [choice point]
    [gain >= 200] / sell --> Happy
    [(gain >= 100) & (gain < 200)] / sell --> Unhappy
    [gain < 100] / reject --> Selling (self)
```

**Difference from regular guards:** With regular guards, the guard is evaluated *at the source state*. With a choice pseudostate, the guard is evaluated *after* the transitional action.

---

## 7. Hierarchical State Machines

### 7.1 Concept

- States can contain **nested submachines** (composite states)
- Reduces diagram complexity by grouping related states
- A composite state has its own initial and (optionally) final state

**Example — Lamp with flashing mode:**
```
LampOff  <--off--  LampFlashing [composite]
                        FlashOn <--> FlashOff (every 1 sec)
LampOn   <--on--   LampFlashing
```

When `flash/` event fires, the lamp enters `LampFlashing` composite state, starting at its initial substate `FlashOn`.

### 7.2 Group Transitions

A transition from a **composite state** applies to **all substates** within it.

> "When `on` occurs in *any* LampFlashing state, transition to LampOn"

This avoids drawing separate transitions from each substate to LampOn.

### 7.3 Completion Transitions

- A **completion transition** has **no trigger** (no event label)
- It fires automatically when the immediately nested state machine **terminates** (reaches its final state)
- Denoted by an arrow with no event label from the composite state

**Example:**
```
Committing [Phase1 --> Phase2 --> (final)] --[completion]--> CommitDone
```
When Phase2 completes and the final state is reached inside Committing, the completion transition to CommitDone fires automatically.

### 7.4 Triggering Rules (Priority)

When two or more transitions have the same event trigger:
- **Innermost transition takes precedence** over outer (group) transitions
- The event is **discarded** after it is processed, whether or not it triggered a transition

**Example:** In `LampFlashing`, if `FlashOff` has an `on/` inner transition to `FlashOn`, and the outer `LampFlashing` composite also has `on/` group transition to `LampOn`, the **inner** one wins (when in FlashOff).

---

## 8. Submachines and Entry/Exit Points (UML 2.0)

### 8.1 Submachines

Syntax: `StateName : SubmachineName`

A state can reference a **reusable submachine** (defined separately). This is like calling a subroutine.
- Execution enters the submachine at its initial state
- When final state of submachine is reached, parent state's exit action runs (if any)

**Example:** `Dispense cash : CashDispenser` — uses the CashDispenser state machine as a submachine.

### 8.2 Entry and Exit Points (UML 2.0)

Allow **encapsulation** of submachines — external transitions don't need to know internal structure.

- **Entry point** — small circle on the border of a composite state; external transition enters at a specific internal state (not always the default initial state)
- **Exit point** — circle with X on the border; allows leaving a submachine at a specific named exit, not just on completion

**Example (ReadAmountSM):**
- Normal entry through default initial → `selectAmount`
- Entry via `again` entry point → goes directly to `EnterAmount`
- Exit via `aborted` exit point when `abort` event occurs in `EnterAmount`

---

## 9. Orthogonality (Concurrent Regions)

### 9.1 Orthogonality Concept

An object can have **multiple simultaneous, independent aspects** of state.

**Example:** A person is simultaneously in:
- An `age` state: Child / Adult / Retiree
- A `financialStatus` state: Poor / Rich

These evolve independently.

### 9.2 Orthogonal Regions

Instead of modeling two separate state machines, combine them into **one composite state with orthogonal regions** separated by a **dashed line**.

```
[Composite State]
  region: age          | region: financialStatus
  Child --> Adult      | Poor <--> Rich
         --> Retiree   |
```

**Semantics:**
- All regions detect the same events and respond to them "simultaneously" (in practice, interleaved)
- Each region is an independent state machine running concurrently

**Example (robBank event):**
```
legalStatus region:     financialStatus region:
LawAbiding --robBank--> Outlaw    Poor --robBank--> Rich
```
Both transitions fire on the same `robBank` event.

### 9.3 Interactions Between Regions

Regions can interact via:
- **Shared variables** (e.g., `sane: Boolean`, `flying: Boolean`)
- **Change events** — transitions triggered by a guard becoming true (written as `(condition)/`)

**Example (Catch22):**
```
sanityStatus region:              flightStatus region:
Crazy (entry: sane:=false)        Flying (entry: flying:=true)
  --(flying)/--> Sane               --(~sane)/--> Grounded
Sane (entry: sane:=true)          Grounded (entry: flying:=false)
  --requestGrounding/--> Crazy      --(sane)/--> Flying
```
The `(flying)` guard means "when `flying` becomes true". Regions interact through the shared boolean variables.

### 9.4 Transition Forks and Joins

For entering/leaving orthogonal regions simultaneously:

- **Fork** (thick bar): one incoming transition splits into multiple outgoing transitions, each entering a different region
- **Join** (thick bar): multiple incoming transitions (one from each region) merge into one outgoing transition — all regions must complete before the join fires

---

## 10. Telephone State Machine — Full Example

A complete hierarchical state machine showing real-world complexity:

```
Idle --lift receiver / get dial tone--> Active [composite]
    Active initial state --> DialTone (do: play dial tone)
        DialTone --dial digit(n)--> Dialing
        DialTone --after(15 sec)--> Time-out (do: play message)
        Dialing --dial digit(n) [incomplete]--> Dialing (self)
        Dialing --after(15 sec)--> Time-out
        Dialing --dial digit(n) [invalid]--> Invalid (do: play message)
        Dialing --dial digit(n) [valid] / connect--> Connecting
        Connecting --busy--> Busy (do: play busy tone)
        Connecting --connected--> Ringing (do: play ringing tone)
        Ringing --callee answers / enable speech--> Talking
        Talking --callee answers--> Pinned
        Pinned --callee hangs up--> Talking
Active --caller hangs up / disconnect--> Idle
Active --abort--> (exit point: aborted)
Active --terminate--> (final state)
```

---

## 11. Activity Diagrams

### 11.1 From State Machines to Activity Diagrams

**State machines** model *one object's* lifecycle.  
**Activity diagrams** model *system-level workflows* involving multiple cooperating objects/actors.

| State Machine | Activity Diagram |
|---|---|
| Models states of one object | Models flow of activities across entities |
| Event-driven | Flow-driven (sequential/parallel) |
| Order states: New, Processing, Shipped, Cancelled | Order processing: Receive → Fill → Ship/Cancel |

### 11.2 What Activity Diagrams Model

- **Business processes** (workflows)
- **Data flows** (how data moves between activities)
- **Concurrent / parallel algorithms**
- Both **control flow** and **data flow** in the same diagram

### 11.3 Core Notation Elements

| Symbol | Name | Meaning | Example |
|---|---|---|---|
| Solid filled circle (●) | Initial Node | Start of flow | Workflow starts when request received |
| Filled circle in ring (◎) | Activity Final Node | End of flow | Process complete |
| Circle with X (⊗) | Flow Final Node | Terminates one flow branch, not whole diagram | Abort path ends |
| Rounded rectangle | Action / Activity | A step in the process | "Validate Login", "Process Payment" |
| Arrow | Control Flow | Sequence of execution | Order of steps |
| Diamond (◇) | Decision / Merge | Branch (decision) or merge multiple paths | "Payment successful?" |
| Thick horizontal bar | Fork / Join | Fork: split into parallel; Join: wait for all | Send email AND update database in parallel |
| Vertical swimlanes | Swimlane / Partition | Responsibility boundary (who does what) | Employee | Manager | HR |
| Rectangle (not rounded) | Object / Data | Data object passed between activities | Application, Cart, Receipt |
| «datastore» | Data Store | Persistent data source | «datastore» Courses |
| Rake symbol on activity | Sub-activity | Activity is expanded in a sub-diagram | "Deliver Order" expanded |

### 11.4 Decision vs. Merge

- **Decision** (one incoming, multiple outgoing with guards): only one branch executes — mutual exclusion
- **Merge** (multiple incoming, one outgoing): *any* arriving input triggers continuation
- **Fork** (one incoming, multiple outgoing, no guards): all branches execute in parallel
- **Join** (multiple incoming, one outgoing): waits for *all* inputs before continuing

> Key distinction: Merge = any input continues. Join = all inputs must arrive first.

---

## 12. Applications of Activity Diagrams

### 12.1 Business Process Modeling (with Swimlanes)

Swimlanes divide the diagram into columns/rows, each representing an actor or subsystem.

**Example — Leave Request Approval:**
```
[Employee] Fill Request --> Submit
[Manager]  Submit --> Manager Review
               Approved --> Update Payroll System --> Notify Employee
               Rejected --> Notify HR --> Update Team Calendar --> Notify Employee
```

Each swimlane = one actor's responsibility. Arrows crossing swimlanes = handoffs.

### 12.2 Data Flow Modeling

Activities can produce and consume **data objects** (shown as rectangles, not rounded).

**Example — Course Registration:**
```
Student: Complete Application --> [Application object]
Registration System: Check Course Availability (reads «datastore» Courses)
                     --> Check Applicant Qualification (reads «datastore» Students, Applications)
                     --> Accept/Deny Reply --> Student
```

### 12.3 Complex Activity Diagrams

- **Sub-activity diagrams**: An activity with a rake symbol is decomposed into a separate diagram
- Guards on decision branches make flow explicit
- Merge nodes collect alternative paths before continuing

**Example — Deliver Order sub-activity:**
```
[decision] --> [rush] --> Deliver Rush --> [merge] --> (final)
           --> [else] --> Deliver Regular --> [merge]
```

### 12.4 Process Sale Example (Multi-swimlane with data)

```
Customer: Shop and Fill Cart --> [Cart object]
Cashier: Enter Cart Items
NextGen POS: Calculate Taxes and Discounts
    [cash payment] --> Create Receipt
    [else] --> Submit Authorization Request
Authorization Service: Authorize Payment --> (back to merge) --> Create Receipt
POS: Create Receipt --> [Receipt object]
Cashier: Hand Over Items --> (final)
```

---

## 13. From Workflow to Architecture

Activity diagrams bridge behavioral modeling and architectural design:

| Behavioral Element | Architectural Artifact |
|---|---|
| Activity / Action | Component responsibility |
| Swimlane | Subsystem or component boundary |
| Control flow | Connector between components |

**Activity diagrams help:**
- Visualize complex processes clearly
- Expose concurrency and dependencies
- Reveal boundaries between responsibilities → candidate system components

---

## 14. Summary — State Machine vs. Activity Diagram

| Dimension | State Machine Diagram | Activity Diagram |
|---|---|---|
| Focus | Single object's lifecycle | Multi-entity workflow/process |
| Driven by | Events | Flow of control/data |
| Key elements | States, transitions, guards, events | Actions, decisions, forks/joins, swimlanes |
| Models | Object behavior over time | Business process, data flow, concurrency |
| Use when | Need to capture valid state sequences | Need to capture workflow or algorithm |

---

## 15. Quick-Reference: State Diagram Pseudostates

| Pseudostate | Symbol | Purpose |
|---|---|---|
| Initial | Filled circle (●) | Starting point of a region |
| Final | Circle in ring (◎) | Terminates the state machine |
| Choice | Hollow diamond (◇) | Dynamic conditional branch |
| Fork | Thick bar | Split into parallel regions |
| Join | Thick bar (multiple incoming) | Synchronize parallel regions |
| Entry point | Small open circle on border | Named entry into composite state |
| Exit point | Circle with X on border | Named exit from composite state |

---

## 16. Key Exam Points

1. **State diagram syntax:** `Event(args)[guard]/action` — know all parts
2. **Guard rules:** Must be side-effect free; evaluated at source state (vs. choice pseudostate evaluated at decision point)
3. **Hierarchical SM:** Inner transitions take priority over outer group transitions; completion transitions have no trigger
4. **Orthogonal regions:** Separated by dashed line; all regions respond to the same event simultaneously; interact via shared variables or change events
5. **Fork vs. Join vs. Decision vs. Merge:** Know the exact semantics (parallel vs. exclusive, all vs. any)
6. **Swimlanes:** Who is responsible for what — each lane = one actor/subsystem
7. **Completion transition:** Fires automatically when nested SM terminates — no event needed
8. **Entry/Exit points (UML 2.0):** Encapsulate submachines so external transitions don't need to know internal structure
9. **Activity diagram uses:** Business process modeling, data flow modeling, concurrent algorithm modeling
10. **Behavioral to architectural mapping:** Swimlane → subsystem; Activity → component responsibility; Control flow → connector
