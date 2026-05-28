# Tutorial 2 — Software Systems: Class Diagrams & Requirements Model

---

## 1. Identifying Classes

**Rule:** Look for entities (nouns) in the problem description. Keep only those that have both **data** and **behavior**.

| Candidate | Keep as | Reason |
|-----------|---------|--------|
| Price | Attribute | No behavior, no other properties — just a value field inside Room/Package (e.g., `RoomPackage.price`) |
| Payment | Class | Has data (amount, method, status) AND behavior (process(), refund()) |
| Book Cruise | Method | An action, not a thing — becomes `Customer.bookCruise()` |

**Key rules to remember:**
- Nouns = candidate classes
- If it has no behavior and is just a property of something else → make it an **attribute**
- If it is an action/verb → make it a **method**
- "Reservation" sounds like a verb but it is an **entity** created as a result of the action *reserve* — it has its own data (ID, date, status) and behavior (confirm(), cancel()) → separate class

---

## 2. Class Relationships — Summary Table

| Relationship | Arrow/Symbol | Nature | Example |
|---|---|---|---|
| Association | Solid line with open arrow | Long-term "knows about / uses" | Customer makes a Reservation |
| Inheritance | Solid line with hollow triangle | "is-a" / specialization | OnlinePayment inherits from Payment |
| Realization | Dashed line with hollow triangle | Class implements an interface | CreditCardPayment implements PaymentProcessor |
| Dependency | Dashed line with open arrow | Short-term "uses temporarily" | BookingService uses PaymentGateway |
| Aggregation | Solid line with hollow diamond | "has-a", part can exist independently | Cruise has Excursions; excursion exists without cruise |
| Composition | Solid line with filled diamond | "part-of", part cannot exist without whole | Reservation contains ReservationDetails; delete reservation → details deleted |

---

## 3. Association vs Dependency (Critical Distinction)

| | Association | Dependency |
|---|---|---|
| Duration | Long-term | Short-term / temporary |
| Mechanism | Stored reference (field/member variable) | Passed as parameter or local variable |
| Meaning | "knows" the other class | "uses" the other class momentarily |

**Code example:**
```cpp
// Association: long-term link — stored reference
class Customer {
    Reservation* reservation;  // stored reference
};

// Dependency: short-term use — passed as parameter
class BookingService {
public:
    void processPayment(PaymentGateway gateway) {  // used temporarily
        gateway.authorize();
    }
};
```

**Memory trick:** Association = stored in state. Dependency = just a method parameter.

---

## 4. Worked Example: Customer — Reservation

**Problem:** Model the relationship between Customer and Reservation.

- Both are **entities** (nouns) — both become classes
- "Reservation" sounds like a method but is actually an entity with its own data and behavior
- **Relationship type:** Association (Customer knows/uses Reservation long-term)
- **Multiplicity:** 1 Customer → 0..* Reservations; 1 Reservation → 1 Customer

**Class diagram structure:**
```
Customer                    Reservation
-----------                 -----------
customerId: int             reservationId: int
name: String      1  makes  date: Date
email: String    --------> status: String
                   0..*
makeReservation()           confirm()
                            cancel()
```

---

## 5. Problem: Cruise Service Model — Find Mistakes

**Diagram shown:** A class diagram for a cruise booking system with classes: Customer, Cruise, Port, Shipping Line, Excursion, Tour Provider, Room Package, Pending Payments, Received Payments.

**Common mistakes to spot in such diagrams:**

- **Wrong relationship type:** Using association where composition is correct (e.g., ReservationDetails should be composition with Reservation, not just association)
- **Attributes as classes:** Things like "Price" or "Location" modeled as separate classes when they should be attributes
- **Missing multiplicity:** Relationships without multiplicity annotations
- **Wrong multiplicity:** e.g., a Cruise stopping at 0 ports makes no sense — should be 1..*
- **Inheritance misuse:** Using inheritance where association is correct
- **Pending Payments becoming Received Payments:** This should be a **state change** (status attribute), not a separate class connected by "Becomes" — having two separate classes for the same entity in different states is a design smell. Better: one Payment class with a `status` attribute.
- **Customer has "Planned Cruises", "Booked Cruises", "Pending Payments" as attributes** — these are actually associations to other classes, not simple attributes

---

## 6. Problem: Use Case Diagram — Find Mistakes

**System:** CFT Online Booking System  
**Actors shown:** Customer, CFT Booking System (external system), Online Payment Service

**Use cases shown:** Plan Cruise, Edit Saved Cruise, Edit Rooms, Edit Excursions, Get Information, Book Cruise, Book Additional Excursions

**Mistakes to find in such diagrams:**

- **System as actor:** "CFT Booking System" is shown as an actor but it is the system itself — external systems can be actors, but this must be clearly an *external* system, not the system under design
- **Include vs Extend misuse:** "Book Additional Excursions" appears to extend "Book Cruise" — the arrow direction matters. `<<extend>>` points from the extending use case to the base; `<<include>>` points from the base to the included
- **Wrong relationship arrow direction:** If "Book Additional Excursions" uses a generalization (hollow triangle) instead of extend/include, that is wrong
- **Actors not connected:** An actor (Online Payment Service) that has no connection to any use case, or is connected to the wrong use cases
- **Use cases inside system boundary vs outside:** All use cases must be inside the system rectangle; actors must be outside

---

## 7. Problem: Detailed Use Case — Find Mistakes

**Use Case:** Book Cruise

| Element | Given Description | Problem/Mistake |
|---|---|---|
| Actors | Customer, **System** | "System" is NOT an actor — the system is the subject of the use case, not an external participant. Only external entities are actors. |
| Preconditions | Customer is logged in. Cruise availability has been verified. | OK |
| Main Flow | 1. Customer selects cruise. 2. System shows rooms. 3. Customer chooses room and confirms. 4. System **books cruise and charges card automatically**. 5. System sends confirmation. | Step 4 combines two distinct actions — booking and payment should be separate steps. Also "charges card automatically" without customer confirmation is a business logic error. |
| Alternate Flow | If payment fails, system cancels booking and exits. | "exits" is vague — should specify what state the system returns to. |
| Postconditions | **TRUE** | Postcondition must be a meaningful state, not just "TRUE". Should be: "Reservation is confirmed and payment is recorded." |

---

## 8. Key Exam Patterns to Remember

### Identifying what something should be:
1. Does it have **multiple attributes** AND **behavior (methods)**? → **Class**
2. Does it have only a value, no behavior? → **Attribute** of another class
3. Is it an action/verb? → **Method** of some class

### Choosing the right relationship:
- "is-a" → Inheritance
- "implements interface" → Realization
- "has-a, part lives independently" → Aggregation
- "part cannot live without whole" → Composition
- "knows / long-term link" → Association
- "uses temporarily in a method" → Dependency

### Multiplicity notation:
| Notation | Meaning |
|---|---|
| 1 | Exactly one |
| 0..1 | Zero or one (optional) |
| 1..* | One or more (at least one) |
| 0..* or * | Zero or more (any number) |
| m..n | Between m and n |

### Common class diagram mistakes:
- "System" listed as an actor in a use case
- Postcondition left as "TRUE" instead of a concrete state
- Combining two distinct steps into one main flow step
- Using separate classes for states of the same entity (use a status attribute instead)
- Attributes that are actually associations to other classes
- Wrong arrow direction for include/extend in use case diagrams
- Missing or incorrect multiplicity on associations
