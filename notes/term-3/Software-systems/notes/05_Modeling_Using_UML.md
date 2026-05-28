# Session 5: Modeling Using UML — Revision Notes

---

## 1. Context: Where UML Fits in the SDLC

| Phase | Purpose | UML Artifact |
|---|---|---|
| SDLC | Establishes lifecycle and processes | — |
| Project Planning | Defines "when" and "who" | — |
| Requirements Engineering | Defines **what** the system must do | Use Case Diagrams |
| Requirements Modeling | Structures and validates "what" | Class Diagrams (analysis) |
| **UML Modeling** | Defines **how** the system will be structured and behave | Class, Sequence, State Diagrams |
| Implementation | Maps UML to code | — |
| Testing | Traces test cases | From sequence diagrams |

---

## 2. What is a Model?

- A model is a **description** of something — "a pattern for something to be made" (Merriam-Webster)
- A model is **not** the thing it models: "The Map is Not The Territory"
- **Engineering model**: a reduced representation of a system that highlights properties of interest **from a given viewpoint**
  - We don't see everything at once
  - Use representations (notations) easily understood for the purpose at hand

### Modeling Maturity Levels

| Level | Description |
|---|---|
| 0 | No specification |
| 1 | Textual |
| 2 | Text with Diagrams |
| 3 | Models with Text |
| 4 | Precise Models |

---

## 3. Modeling Languages

| Type | Description | Examples |
|---|---|---|
| **DSL** (Domain-Specific Language) | Designed for a specific domain | HTML, SQL |
| **GPL** (General Purpose Modeling Language) | Applicable to any domain | **UML**, XML |

---

## 4. UML — Unified Modeling Language

### Brief History
- No common modeling language existed until 1996
- GPL developed by industry consortium in **1997**
- Standardized by **OMG** (Object Management Group)
- Created by the **Three Amigos**: Grady Booch, Ivar Jacobson, James Rumbaugh
- Based on multiple prior visual modeling languages
- Goal: single language covering a large number of SE tasks
- Current version: **UML 2.5.1** (Dec 2017)

### What UML is
- Notation for **OO (Object-Oriented) Modeling**
- Models a system as a collection of **objects that interact with each other**
- Uses **graphical diagrams** — clearer than natural language, independent of programming language/technology

### What UML is NOT
- Not an OO method or process
- Not a visual programming language
- Not a tool specification

---

## 5. Models and Meta-Models

Three levels:

| Level | Name | Example |
|---|---|---|
| M0 | **Objects** (instances) | `<Ben&Jerry's>`, `<lard, 5 tons>` |
| M1 | **Model** (class diagram) | `Customer`, `CustomerOrder` |
| M2 | **Meta-Model** | `Class`, `Association` |

Meta-models are simply **models of models**.

---

## 6. Domain Concept vs. Design vs. Code

- **Domain concept**: real-world thing (e.g., a Boeing 737 airplane)
- **Design representation**: UML class box showing `Plane` with attribute `tailNumber`
- **Code representation**: Java class `public class Plane { private String tailNumber; public List getFlightHistory() {...} }`

---

## 7. UML Diagram Types (14 total)

### Structure Diagrams (static aspects)
- Class Diagram
- Package Diagram
- Object Diagram
- Component Diagram
- Profile Diagram
- Composition Structure Diagram
- Deployment Diagram

### Behavior Diagrams (dynamic aspects)
- State Machine Diagram
- Use Case Diagram
- Activity Diagram
- Interaction Diagram
  - Sequence Diagram
  - Communication Diagram
  - Interaction Overview Diagram
  - Timing Diagram

---

## 8. UML in a Full Process

### Full Process layers:
1. **Business Models**: Business Use Cases → Activity Diagrams, Domain Object State Diagrams, Domain Model
2. **Analysis Models**: Analysis Use Cases → Activity Diagrams, State Diagrams; Analysis Class Diagram
3. **System Architectural Models**: Interaction Diagrams, Component/Deployment Diagrams, System Architecture, Design Class Diagrams, State Diagrams

### UltraLite Process (simplified — what this course focuses on):
```
Business Use Cases
       ↓ (refine)
Analysis Use Cases  <--trace-->  Requirements Class Diagram
       ↓ (refine)                         ↓ (refine)
Interaction Diagrams  <--trace-->  Design Class Diagrams
       ↓ (refine)                         ↓ (refine)
                        code
```

---

## 9. Static vs. Dynamic Models

| Type | Describes | Main Diagram |
|---|---|---|
| **Static Model** | Static structure of a system | Class Diagram |
| **Dynamic Model** | Dynamic behavior of a system | State chart, Sequence Diagram |

**This unit covers: Class Diagram (static) + Sequence Diagram (dynamic)**

---

## 10. Object-Oriented Modeling

- Uses object-orientation as the basis of modeling
- Models a system as **a set of objects that interact with each other**
- **No semantic gap** (no impedance mismatch) between real world and model
- Enables **seamless development**

### Key OO Ideas
- **Abstraction**: capture essential properties, ignore details
- **Encapsulation**: hide internal state, expose interface
- **Relationship**:
  - *Association*: relationship between objects
  - *Inheritance*: mechanism to represent similarity among objects
- **OO formula**: `object (class) + inheritance + message send`

---

## 11. Objects vs. Classes

| | Real World Interpretation | Model Representation |
|---|---|---|
| **Object** | Anything distinctly identifiable | Has an identity, a state, and a behavior |
| **Class** | A set of objects with similar characteristics/behavior; objects are *instances* | Characterizes the structure of states and behaviors shared by all instances |

---

## 12. UML Class Diagram

- Most common diagram in OO modeling
- Describes the **static structure** of a system
- Consists of:
  - **Nodes** representing classes
  - **Links** representing relationships:
    - Inheritance
    - Association (including Aggregation and Composition)
    - Dependency

### Notation for a Class

```
+-------------------+
|    ClassName      |   <- Top: class name (bold if concrete)
+-------------------+
|  field1           |   <- Middle: attributes
|  field2           |
+-------------------+
|  method1()        |   <- Bottom: methods
|  method2()        |
+-------------------+
```

**Example:**
```
+---------------------------+
|          Point            |
+---------------------------+
|  - x: int                 |
|  - y: int                 |
+---------------------------+
|  + move(dx: int, dy: int): void |
+---------------------------+
```

### Field Declaration Syntax
```
[visibility] name [multiplicity]: type [= default]
```
Examples:
- `birthday: Date`
- `+duration: int = 100`
- `-students[1..MAX_SIZE]: Student`

### Method Declaration Syntax
```
[visibility] name(param: type, ...): returnType
```
Examples:
- `+move(dx: int, dy: int): void`
- `+getSize(): int`

### Visibility Notation

| Visibility | Symbol |
|---|---|
| public | `+` |
| protected | `#` |
| package | `~` |
| private | `-` |

### Abstract Classes
- Marked with `{abstract}` in the class name compartment
- Example: `Student {abstract}`

---

## 13. Notation for Objects

```
+---------------------------+
|  objectName: ClassName    |   <- underlined
+---------------------------+
|  field1 = value1          |
|  field2 = value2          |
+---------------------------+
```

Example:
```
+-------------+     +-------------+
|  p1: Point  |     |  p2: Point  |
+-------------+     +-------------+
|  x = 10     |     |  x = 20     |
|  y = 20     |     |  y = 30     |
+-------------+     +-------------+
```

---

## 14. UML Interfaces

Two notations:

**Notation 1 (stereotype):**
```
+----------------------------+
|  <<interface>>             |
|     Drawable               |
+----------------------------+
|  + draw(g: Graphics): void |
+----------------------------+
```

**Notation 2 (lollipop — abbreviated):**
```
Drawable
+ draw(g: Graphics): void
```
(class name in italics)

---

## 15. Inheritance (Generalization / Specialization)

Three kinds in Java → three notations in UML:

| Java Relationship | UML Name | Notation |
|---|---|---|
| Class `extends` Class | Specialization / Generalization | Solid line + hollow triangle arrow (pointing to superclass) |
| Interface `extends` Interface | Extension of interfaces | Solid line + hollow triangle (pointing to superinterface) |
| Class `implements` Interface | Realization | Dashed line + hollow triangle (pointing to interface) |

**Arrow direction**: always points **from child to parent** (subclass to superclass).

### Example: Student Hierarchy
```
          Student {abstract}
         /    |       \
Nondegree  Undergraduate  Graduate {abstract}
                          /        \
                       Master      PhD
```

---

## 16. Association

- General **binary relationship** between classes
- Represented as direct/indirect references between classes
- Drawn as a **solid line**
- Optional **label** with a direction arrow (solid arrowhead, no tail) showing direction of association name
- Optional **navigation arrow** (open arrowhead at end of path) indicating direction of traversal

**Example:**
```
Student ——— enroll ► ——— Course
```

### Role Names and Multiplicity

Association ends can have:
- A **role name** (e.g., `advisee`, `advisor`)
- A **multiplicity** specification

**Multiplicity Notation:**

| Notation | Meaning |
|---|---|
| `1` | Exactly one |
| `0..1` | Zero or one |
| `m..n` | Between m and n (inclusive) |
| `0..*` or `*` | Zero or more |
| `1..*` | One or more |

**Example:**
```
Student ——0..* advisee ——— advisor 1—— Faculty
```
(Each student has exactly 1 advisor; each faculty advises 0 or more students)

### Course Enrollment Example
```
Student —6..* — enroll ► — 0..* — Course
   |                                 |
advisee 0..*              1..* teach |
   |                                 |
   ——————————— 1 advisor ——————— Faculty
```

---

## 17. Aggregation

- Special form of association representing **has-a** or **part-whole** relationship
- Distinguishes the **whole** (aggregate class) from its **parts** (component class)
- Parts can **exist independently** of the whole (no lifetime dependency)
- Notation: **hollow diamond** on the aggregate side

```
Aggregate ◇————— Component
```

**Example:** Department ◇————— Student (students can exist without the department)

---

## 18. Composition

- **Stronger form of aggregation**
- Implies **exclusive ownership**: component belongs to exactly one aggregate
- Component **cannot exist without** its aggregate (lifetime of component is within lifetime of aggregate)
- Notation: **filled diamond** on the aggregate side

```
Composition ◆————— Component
```

**Example:** University ◆————— College (a college cannot exist without the university)

### Aggregation vs. Composition Summary

| Feature | Aggregation | Composition |
|---|---|---|
| Symbol | Hollow diamond ◇ | Filled diamond ◆ |
| Ownership | Shared / weak | Exclusive / strong |
| Lifetime | Parts can outlive whole | Parts destroyed with whole |
| Example | Department ◇— Student | University ◆— College |

### Full University Example
```
University ◆—1—— 1..* ——College ◆—1—— 1..* ——Department
                                              ◇ 1         ◇ 1
                                          0..*            member-of 1..*
                                         Student ——— Faculty
                                                    chair-of 1
```

---

## 19. Dependency

- Relationship where proper operation of one entity depends on the **presence or correctness of another**
- Changes in one entity affect the other
- Most common form: **use** relation among classes
- Notation: **dashed arrow** with `<<use>>` stereotype

```
Class1 - - - - - <<use>> ——> Class2
```

**Key rule:** Dependencies are most often **omitted** from diagrams unless they convey significant information.

**Example:** `Registrar` class depends on `CourseSchedule`, `Course`, and `Student` (uses them in method parameters).

---

## 20. OO Modeling Process (How to Build a Class Diagram)

1. **Identify classes** — represent physical objects, people, organizations, places, events, or concepts. Class names should be **noun phrases**.
2. **Identify fields and methods** — actions are modeled as methods. Method names should be **verb phrases**.
3. **Identify inheritance relationships** — draw generalization/specialization hierarchy.
4. **Identify association relationships** — draw with multiplicity and role names.
5. **Identify aggregation and composition relationships**.
6. **Add dependency relationships** if significant.

---

## 21. Interaction Models (Sequence Diagrams)

### What is an Interaction Model?
- Shows interactions (messages exchanged) between **objects** in a system
- Definition: "a behavior that comprises a set of messages exchanged among a set of objects within a context to accomplish a purpose" (UML user guide)
- Provides a **view of system behavior** (dynamic model)

### Sequence Diagram
- Captures **dynamic behavior** (time-oriented)
- Purpose: model flow of control, illustrate typical scenarios
- Time flows **top to bottom**

### Key Elements

| Element | Description |
|---|---|
| **Object/Actor** | Box at top: `objectName : ClassName` |
| **Lifeline** | Dashed vertical line below object |
| **Focus of control** | Thin rectangle on lifeline — period of activity |
| **Message** | Horizontal arrow between lifelines with label |
| **Return** | Dashed horizontal arrow |
| **Creation** | `<<create>>` message to new object |
| **Destruction** | `<<destroy>>` with X at end of lifeline |
| **Sequence label** | Label on message like `a1: run(3)` |

### Message Types

| Type | Description | Notation |
|---|---|---|
| **Synchronous** | Sender waits for return before continuing | Solid arrowhead `——►` |
| **Asynchronous** | Sender does not wait for response | Open arrowhead `——>` |
| **Response/Return** | Return value (not mandatory in obvious cases) | Dashed arrow `- - -►` |

### Combined Fragments (Control Structures)
Used to model control structures explicitly. 12 operators in 3 groups:

| Operator | Keyword | Use |
|---|---|---|
| Alternative | `alt` | if-else (alternative execution) |
| Optional | `opt` | if (execute if guard condition true) |
| Break | `break` | Execute fragment when break condition met |
| Loop | `loop` | Repeated execution |
| Sequential | `seq` | Weak ordering (default) |
| Strict | `strict` | Strict ordering |
| Parallel | `par` | Concurrent execution of sub-scenarios |
| Critical | `critical` | Atomic — no other interactions can intervene |
| Ignore | `ignore` | Irrelevant messages at runtime |
| Consider | `consider` | Important messages of the interaction |
| Negate | `neg` | Invalid/undesirable interactions |
| Assert | `assert` | Mandatory interactions |

**Fragment notation:** A rectangle with the operator name in the top-left corner and a condition `[guard]`.

### Sequence Diagram Example (Course Registration)
```
:StudentManager  :CoursePortal  :Admin  :CourseDataManager

     |                |              |            |
     |—register(courseId, studId)——>|             |
     |                |—approve(courseId, studId)—>|
     |                |              |—checkSeatStatus(courseId)—>|
     |                |              |<—————status——————————————|
     |        alt [status=full]      |
     |<——NotAllocated————————————————|
     |        [else]                 |
     |                |              |—allotCourse(courseId, studId)—>|
     |                |              |<————success————————————————|
     |<——success——————|              |
```

### Interaction Modeling Tips
- Set the **context** for the interaction
- Flow runs **left to right** and **top to bottom**
- Put **active objects** on the left/top; **passive objects** on the right/bottom
- Use sequence diagrams to show **explicit ordering** between stimuli or when modeling **real-time** interactions

---

## 22. UML in SDLC — Summary

| SDLC Phase | UML Diagrams Used |
|---|---|
| Requirements | Use Case Diagrams |
| Design | Class Diagrams, Sequence Diagrams, State Diagrams |
| Implementation | Map UML to code |
| Testing | Trace test cases from sequence diagrams |

---

## Quick Reference: Relationship Notation Cheat Sheet

| Relationship | Line Style | Arrowhead | Symbol |
|---|---|---|---|
| Association | Solid | Open arrow (optional) | `———` |
| Directed Association | Solid | Open arrowhead at target | `———►` |
| Aggregation (has-a, weak) | Solid | Hollow diamond at whole | `◇———` |
| Composition (owns, strong) | Solid | Filled diamond at whole | `◆———` |
| Generalization / Inheritance | Solid | Hollow triangle at parent | `———▷` |
| Realization (implements) | Dashed | Hollow triangle at interface | `- - -▷` |
| Dependency (use) | Dashed | Open arrowhead | `- - -►` |

---

## Key Exam Points

- **UML is not** a programming language, OO method, or tool spec — it is a **notation**
- Class diagram = static model; Sequence diagram = dynamic model
- **Composition** = strong ownership, parts die with whole; **Aggregation** = weak, parts can live independently
- Arrow in inheritance always points **from subclass to superclass**
- **Realization** (class implements interface) = dashed line + hollow triangle
- Multiplicity is placed **near the target end** of an association
- `0..*` means zero or more; `1..*` means one or more; `1` means exactly one
- Dependencies are often **omitted** unless significant
- Sequence diagram: time flows **top to bottom**; synchronous = solid arrowhead, return = dashed arrow
- Combined fragment operators: `alt` = if-else, `opt` = if, `loop` = loop, `par` = parallel
