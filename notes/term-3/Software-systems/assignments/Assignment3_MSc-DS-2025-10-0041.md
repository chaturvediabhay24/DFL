# Software Systems — Assignment 3
**Name:** Abhay Chaturvedi  
**Roll Number:** MSc-DS-2025-10-0041

---

# SkyHigh Booking System — Design Pattern Solutions

## Selected Problems

| # | Problem | Pattern | Category |
|---|---------|---------|----------|
| 1 | Problem 2 — Monster Constructor for Orders | Builder | Creational |
| 2 | Problem 3 — Integration Nightmare | Adapter | Structural |
| 3 | Problem 4 — All-Powerful Payment Class | Strategy | Behavioral |

---

## Solution 1 — Problem 2: The "Monster Constructor" for Orders

### 1. The Problem

The `Order` class currently uses a single large constructor with around a dozen parameters, most of which are optional (e.g., travel insurance, extra baggage, meal preference). Callers are forced to pass `null` for every optional parameter they don't need, resulting in calls like `new Order(customer, flights, null, 2, null, ...)`. This is fragile: the parameter order is easy to get wrong, the intent of each positional argument is unclear at the call site, and adding a new optional field forces every existing call site to be updated.

### 2. Chosen Design Pattern and Category

**Pattern:** Builder  
**Category:** Creational

### 3. Justification

The Builder pattern separates the construction of a complex object from its representation. Instead of one overloaded constructor, a dedicated `OrderBuilder` class exposes named setter methods — one per field — and a terminal `build()` method that validates and produces the final `Order`.

This directly addresses the pain points:

- **High cohesion**: The `Order` class itself only holds data; all construction logic lives in `OrderBuilder`.
- **Low coupling**: Callers depend on fluent setter names (`withTravelInsurance()`, `withExtraBaggage()`) rather than positional slot numbers, so adding a new optional field does not break any existing call site.
- **Open/Closed Principle**: New optional attributes (e.g., priority boarding) can be added to `OrderBuilder` without modifying `Order` or any existing client code.
- **Separation of concerns**: Validation (e.g., "a meal choice requires a flight") is centralised in `build()`, not scattered across callers.

The Telescoping Constructor anti-pattern (what currently exists) and the Builder pattern are a canonical pair in creational design; this is the textbook fix for an object with many optional fields.

### 4. Solution Sketch

#### UML Class Diagram

```
+-------------------+          +----------------------------+
|      Order        |<-builds--|        OrderBuilder        |
+-------------------+          +----------------------------+
| - customer        |          | - customer: Customer       |
| - flights         |          | - flights: List<Flight>    |
| - numBaggage: int |          | - numBaggage: int = 0      |
| - hasTravelIns.   |          | - hasTravelInsurance: bool |
| - mealChoice      |          | - mealChoice: String       |
| - seatUpgrade     |          | - seatUpgrade: bool        |
|                   |          | - priorityBoarding: bool   |
+-------------------+          +----------------------------+
                               | + withCustomer(c): Builder |
                               | + withFlights(f): Builder  |
                               | + withExtraBaggage(n):     |
                               |     Builder                |
                               | + withTravelInsurance():   |
                               |     Builder                |
                               | + withMealChoice(m):       |
                               |     Builder                |
                               | + withSeatUpgrade():       |
                               |     Builder                |
                               | + withPriorityBoarding():  |
                               |     Builder                |
                               | + build(): Order           |
                               +----------------------------+
```

#### Pseudo-code

```
// BEFORE (fragile — what is null at position 3? position 5?)
Order o = new Order(customer, flights, null, 2, null, false, "vegetarian", null, ...)

// AFTER (readable, safe, extensible)
Order o = new OrderBuilder()
    .withCustomer(customer)
    .withFlights(flights)
    .withExtraBaggage(2)
    .withMealChoice("vegetarian")
    .build()

// ----------------------------------------------------------
class OrderBuilder:
    customer, flights       // mandatory
    numBaggage = 0          // optional, defaults
    hasTravelInsurance = false
    mealChoice = null
    seatUpgrade = false

    withCustomer(c)         -> set customer;          return this
    withFlights(f)          -> set flights;           return this
    withExtraBaggage(n)     -> set numBaggage = n;    return this
    withTravelInsurance()   -> set hasTravelInsurance = true; return this
    withMealChoice(m)       -> set mealChoice = m;    return this
    withSeatUpgrade()       -> set seatUpgrade = true; return this

    build():
        if customer == null OR flights is empty:
            throw IllegalStateException("Customer and flights are mandatory")
        return new Order(this)   // Order has a package-private constructor
                                 // that accepts only an OrderBuilder

// Order constructor (package-private — only OrderBuilder may call it)
class Order:
    Order(builder: OrderBuilder):
        this.customer           = builder.customer
        this.flights            = builder.flights
        this.numBaggage         = builder.numBaggage
        this.hasTravelInsurance = builder.hasTravelInsurance
        this.mealChoice         = builder.mealChoice
        this.seatUpgrade        = builder.seatUpgrade
```

### 5. Assumptions

- `customer` and at least one `flight` are treated as mandatory; all other fields are optional with sensible defaults.
- The `Order` class constructor is made package-private (or the `OrderBuilder` is a static inner class of `Order`) so that callers cannot bypass the builder.
- No existing persistent storage schema needs to be changed; only the in-memory construction API changes.

---

## Solution 2 — Problem 3: The Integration Nightmare

### 1. The Problem

The `ScheduledFlight` class needs to know the passenger capacity of whichever aircraft it is assigned. The three aircraft types expose this information in completely incompatible ways:
- `PassengerPlane` uses a public field: `passengerCapacity`
- `Helicopter` uses a method: `getPassengerCapacity()`
- `PassengerDrone` has no capacity API at all — the number (4) is hardcoded in the caller

Because none of these expose a common interface, `ScheduledFlight` is riddled with `instanceof` checks. Every new aircraft type added to the fleet forces a change inside `ScheduledFlight`, violating the Open/Closed Principle.

### 2. Chosen Design Pattern and Category

**Pattern:** Adapter  
**Category:** Structural

### 3. Justification

The Adapter pattern converts the interface of a class into another interface that the client expects. Here, we define a single `Aircraft` interface with one method — `getPassengerCapacity()` — and create a thin adapter wrapper for each existing aircraft type that implements this interface.

This achieves:

- **Open/Closed Principle**: `ScheduledFlight` is closed for modification. To support a new aircraft (e.g., `Airship`), we only add a new `AirshipAdapter` without touching any existing code.
- **Low coupling**: `ScheduledFlight` depends only on the `Aircraft` interface, not on concrete manufacturer classes. This decouples the booking system from third-party aircraft software.
- **High cohesion**: Each adapter has one job — translating one manufacturer's API into the common interface. The messy `instanceof` logic in `ScheduledFlight` disappears entirely.
- **Separation of concerns**: The translation details (field access vs. method call vs. hardcoded constant) are encapsulated inside the adapters, not leaked into business logic.

### 4. Solution Sketch

#### UML Class Diagram

```
           <<interface>>
         +---------------+
         |    Aircraft   |
         +---------------+
         | + getPassenger|
         |   Capacity()  |
         |   : int       |
         +---------------+
                 ^
                 | implements
    _____________|_____________________________
    |                    |                    |
+------------------+ +-----------------+ +------------------+
|PassengerPlane    | |  HelicopterAd-  | |PassengerDroneAd- |
|    Adapter       | |     apter       | |     apter        |
+------------------+ +-----------------+ +------------------+
| - plane:         | | - heli:         | | FIXED_CAP = 4    |
|  PassengerPlane  | |  Helicopter     | |                  |
+------------------+ +-----------------+ +------------------+
| +getPassenger    | | +getPassenger   | | +getPassenger    |
|  Capacity():     | |  Capacity():    | |  Capacity():     |
|  return          | |  return heli.   | |  return 4        |
|  plane.passenger | |  getPassenger   | |                  |
|  Capacity        | |  Capacity()     | |                  |
+------------------+ +-----------------+ +------------------+

  [Third-party / legacy classes — NOT modified]
  +-------------------+  +--------------+  +------------------+
  |  PassengerPlane   |  | Helicopter   |  | PassengerDrone   |
  +-------------------+  +--------------+  +------------------+
  | + passengerCapacity|  | + getPassenger|  | (no capacity API)|
  |   : int            |  |   Capacity() |  |                  |
  +-------------------+  +--------------+  +------------------+

  +---------------------+
  |   ScheduledFlight   |
  +---------------------+
  | - aircraft: Aircraft|   <-- depends only on the interface
  +---------------------+
  | + getCapacity():    |
  |   aircraft          |
  |   .getPassenger     |
  |   Capacity()        |
  +---------------------+
```

#### Pseudo-code

```
// Common interface — the only thing ScheduledFlight knows about
interface Aircraft:
    getPassengerCapacity(): int

// Adapter for PassengerPlane (field access -> method call)
class PassengerPlaneAdapter implements Aircraft:
    plane: PassengerPlane
    PassengerPlaneAdapter(plane) -> this.plane = plane
    getPassengerCapacity(): return plane.passengerCapacity

// Adapter for Helicopter (already has a method, just rename/wrap)
class HelicopterAdapter implements Aircraft:
    heli: Helicopter
    HelicopterAdapter(heli) -> this.heli = heli
    getPassengerCapacity(): return heli.getPassengerCapacity()

// Adapter for PassengerDrone (hardcoded knowledge lives here, not in ScheduledFlight)
class PassengerDroneAdapter implements Aircraft:
    FIXED_CAPACITY = 4
    getPassengerCapacity(): return FIXED_CAPACITY

// ScheduledFlight — no instanceof, no coupling to concrete types
class ScheduledFlight:
    aircraft: Aircraft

    ScheduledFlight(aircraft: Aircraft):
        this.aircraft = aircraft

    getAvailableSeats():
        return aircraft.getPassengerCapacity() - bookedSeats

// Usage — adding an Airship later only requires AirshipAdapter, nothing else changes
flight = new ScheduledFlight(new PassengerPlaneAdapter(myBoeing747))
flight = new ScheduledFlight(new HelicopterAdapter(myBell412))
flight = new ScheduledFlight(new PassengerDroneAdapter())
```

### 5. Assumptions

- The third-party aircraft classes (`PassengerPlane`, `Helicopter`, `PassengerDrone`) cannot be modified, which is why Adapter is preferred over simply adding a common interface to them directly.
- The fixed capacity of `PassengerDrone` (4) is a stable, documented specification from the manufacturer. It is encapsulated inside `PassengerDroneAdapter` rather than derived from any live API.
- An `AircraftAdapterFactory` (or similar) is assumed to be responsible for instantiating the correct adapter at fleet-setup time, so the rest of the system never deals with the concrete aircraft types.

---

## Solution 3 — Problem 4: The All-Powerful Payment Class

### 1. The Problem

The `FlightOrder` class contains a single large method that uses a long `if-else` chain to handle different payment types (`CreditCard`, `PayPal`, etc.). The business team now wants to add `CryptoWallet` and `BankTransfer`. Each addition means touching the `FlightOrder` class, making it larger, harder to test, and increasingly risky to change — the definition of a "God Class." Payment processing logic is unrelated to order management, yet the two are fused together.

### 2. Chosen Design Pattern and Category

**Pattern:** Strategy  
**Category:** Behavioral

### 3. Justification

The Strategy pattern defines a family of algorithms (in this case, payment processing algorithms), encapsulates each in its own class, and makes them interchangeable. The `FlightOrder` class holds a reference to a `PaymentStrategy` interface and delegates payment processing to whichever concrete strategy is injected at runtime.

This addresses the problem on multiple fronts:

- **Open/Closed Principle**: Adding `CryptoWalletStrategy` requires creating one new class. `FlightOrder` is never modified — it stays closed to modification but open to extension through new strategies.
- **Single Responsibility Principle / High Cohesion**: `FlightOrder` is responsible for managing booking state. Payment processing is the responsibility of the strategy objects. Each class now has one clearly defined job.
- **Low coupling**: `FlightOrder` depends only on the `PaymentStrategy` interface, not on any payment provider's SDK or API.
- **Testability**: Each strategy can be unit-tested in isolation. `FlightOrder` can be tested with a mock `PaymentStrategy`, free from any payment-provider dependency.
- **Separation of concerns**: Provider-specific logic (API keys, retry policies, response parsing) lives inside each strategy, not in the order-management class.

### 4. Solution Sketch

#### UML Class Diagram

```
         <<interface>>
       +------------------+
       | PaymentStrategy  |
       +------------------+
       | + pay(amount:    |
       |   double): bool  |
       +------------------+
               ^
               | implements
    ___________|_________________________________
    |              |              |             |
+----------+ +-----------+ +-----------+ +------------+
|CreditCard| |  PayPal   | |CryptoWallet| |BankTransfer|
| Strategy | | Strategy  | | Strategy  | | Strategy   |
+----------+ +-----------+ +-----------+ +------------+
| +pay()   | | +pay()    | | +pay()    | | +pay()     |
| // charge| | // call   | | // sign   | | // initiate|
| // card  | | // PayPal | | // TX     | | // transfer|
|   API    | |   API     | |           | |            |
+----------+ +-----------+ +-----------+ +------------+

+---------------------------+
|       FlightOrder         |
+---------------------------+
| - bookingDetails          |
| - paymentStrategy:        |
|   PaymentStrategy         |
+---------------------------+
| + setPaymentStrategy(s):  |
|   void                    |
| + processPayment(amount): |
|   bool                    |
|   // delegates to         |
|   // paymentStrategy.pay()|
+---------------------------+
```

#### Sequence Diagram (checkout flow)

```
  Client          FlightOrder         CreditCardStrategy
    |                  |                      |
    |--setPaymentStrategy(creditCardStrategy)->|
    |                  |                      |
    |--processPayment(totalAmount)----------->|
    |                  |--pay(totalAmount)--->|
    |                  |                      |--[calls Credit Card API]
    |                  |                      |--returns true/false
    |                  |<--result-------------|
    |<--confirmation---|
```

#### Pseudo-code

```
// Strategy interface
interface PaymentStrategy:
    pay(amount: double): boolean

// Concrete strategies — each encapsulates one provider
class CreditCardStrategy implements PaymentStrategy:
    cardNumber, cvv, expiry
    pay(amount):
        // call credit card processing API
        return chargeCard(cardNumber, cvv, expiry, amount)

class PayPalStrategy implements PaymentStrategy:
    email, accessToken
    pay(amount):
        // call PayPal REST API
        return paypalClient.charge(email, accessToken, amount)

class CryptoWalletStrategy implements PaymentStrategy:
    walletAddress, privateKey
    pay(amount):
        // sign and broadcast blockchain transaction
        return cryptoGateway.send(walletAddress, privateKey, amount)

class BankTransferStrategy implements PaymentStrategy:
    accountNumber, routingCode
    pay(amount):
        // initiate ACH / SWIFT transfer
        return bankGateway.transfer(accountNumber, routingCode, amount)

// FlightOrder — no if-else, no provider knowledge
class FlightOrder:
    bookingDetails: BookingDetails
    paymentStrategy: PaymentStrategy

    setPaymentStrategy(strategy: PaymentStrategy):
        this.paymentStrategy = strategy

    processPayment(amount: double): boolean:
        if paymentStrategy == null:
            throw IllegalStateException("No payment method selected")
        return paymentStrategy.pay(amount)

// Usage
order = new FlightOrder(bookingDetails)
order.setPaymentStrategy(new CreditCardStrategy("4111...", "123", "12/27"))
success = order.processPayment(order.getTotalPrice())
```

### 5. Assumptions

- The `PaymentStrategy` is selected by the customer at checkout and injected into `FlightOrder` before `processPayment()` is called. A factory or service layer is responsible for instantiating the correct strategy based on the user's selection.
- Each strategy handles its own error handling and retry logic internally; `FlightOrder` only observes the boolean result.
- All payment strategies are assumed to be stateless with respect to the order (i.e., they do not need to read `FlightOrder` fields directly). If provider-specific data needs order context, the `pay()` signature can be extended to pass an `OrderContext` object.

---

## Summary Table

| Problem | Design Pattern | Category | Principle Addressed |
|---------|---------------|----------|---------------------|
| Monster Constructor (Order) | Builder | Creational | High Cohesion, Low Coupling, OCP |
| Integration Nightmare (Aircraft) | Adapter | Structural | OCP, Low Coupling, Separation of Concerns |
| All-Powerful Payment Class | Strategy | Behavioral | OCP, SRP, High Cohesion, Testability |
