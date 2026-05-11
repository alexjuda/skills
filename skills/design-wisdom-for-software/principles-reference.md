# Principles Reference

Full citations, extended examples, and negative-transfer warnings for each lens in the design-wisdom-for-software skill.

---

## Source Bibliography

| Principle | Primary Source |
|---|---|
| Affordances, Signifiers, Conceptual Models, Constraint Design | Norman, *The Design of Everyday Things* (1988, rev. 2013) |
| Cognitive Load | Sweller, "Cognitive Load During Problem Solving" (1988); Cowan, "The Magical Number 4" (2001) |
| Signal-to-Noise / Data-Ink | Tufte, *The Visual Display of Quantitative Information* (1983) |
| Information Scent | Pirolli & Card, "Information Foraging" (1999) |
| Negative Space / Less is More | Mies van der Rohe (attributed); Dieter Rams, Ten Principles of Good Design (1970s) |
| Atomic Composition | Alexander, *The Timeless Way of Building* (1979); Brad Frost, *Atomic Design* (2013) |
| Hierarchy at Every Scale | Alexander, *Notes on the Synthesis of Form* (1964); Tufte (1983) |
| Wicked Problems | Rittel & Webber, "Dilemmas in a General Theory of Planning" (1973) |
| Gestalt | Wertheimer, Köhler, Koffka (1920s); applied to code in Henney (2010s) |
| Metaphors as Conceptual Models | Lakoff & Johnson, *Metaphors We Live By* (1980) |

---

## Affordances — Extended

**Origin:** James J. Gibson (1977, ecological psychology) coined the term. Donald Norman adapted it for designed objects and UX.

**The critical distinction:** Affordances exist whether or not they're perceived. A glass door *affords* pushing, even if you try to pull it. The problem isn't missing affordance — it's missing **signifier** (see below). In software: the affordance is the capability; the signifier is what makes the capability discoverable.

**Software-specific applications:**

*Type system affordances:*
```python
# No affordances — raw primitives communicate nothing about valid use
def reserve_seat(flight_id: int, seat: str, passenger: str) -> bool: ...

# Strong affordances — types encode valid usage
def reserve_seat(flight: FlightId, seat: SeatCode, passenger: PassengerId) -> Reservation: ...
```

*Method chaining affords composition (fluent interface pattern):*
```python
# Shape affords sequential refinement
results = (
    db.query(User)
      .filter(User.active == True)
      .order_by(User.created_at.desc())
      .limit(20)
      .all()
)
```

*Keyword-only arguments afford safe future extension:*
```python
# Forces callers to name args — adding params later won't silently break callers
def create_event(*, title: str, starts_at: datetime, location: str | None = None) -> Event: ...
```

**Negative transfer warning:** Affordances in physical design are often about preventing accidents (a knife handle affords gripping, not cutting). In software, over-engineering affordances into the type system creates its own cognitive load. Don't model every constraint as a newtype — reserve it for constraints where violation would cause serious, hard-to-debug problems.

---

## Signifiers — Extended

**The distinction from affordances:** Affordances are relational properties. Signifiers are communication. A "PUSH" sign is a signifier for the affordance of a door. Without it, users pull.

**Four levels of signifiers in code:**

1. **Names** — function name, parameter name, module name. The first and cheapest signifier.
2. **Types** — type annotations communicate valid inputs, return shapes, side effects (Result type, Optional).
3. **Docstrings** — especially valuable for *why* something behaves as it does, and for exceptional cases.
4. **Error messages** — the most neglected signifier. An error is a signifier about what went wrong and how to fix it. A good error is a mini design document.

**Error as signifier example:**
```
# Weak — tells you what broke, not where to go
ValidationError: invalid value

# Strong — points toward the fix
ValidationError: 'expires_at' must be in the future.
  Got: 2024-01-01T00:00:00Z (1 year ago)
  Tip: Use datetime.utcnow() + timedelta(days=30) for a 30-day expiry.
```

**Observability as signifiers:** Structured logs, named metrics, correlation IDs — these are signifiers for the operational interface. An operator navigating an incident is a user navigating an information space. Name metrics and log fields for *that* user, not for the implementation.

```
# Weak observability signifier
log.error("error occurred")

# Strong — operator can navigate to the cause
log.error("payment_charge_failed",
    charge_id=charge.id,
    amount_cents=charge.amount,
    gateway_error=e.code,
    retry_count=attempt,
    correlation_id=request.id)
```

---

## Constraint Design — Extended

**Norman's constraint taxonomy:**

| Type | Physical design | Software analog |
|---|---|---|
| Physical | Shape prevents wrong assembly | Type system prevents invalid inputs |
| Logical | Only one piece fits here | Exactly one valid state transition from here |
| Cultural | Green=go, Red=stop | Return `None` means "not found", raise means "error" |
| Semantic | This is a library, not a shelter | Module boundaries encode domain rules |

**Make invalid states unrepresentable** (Yaron Minsky's formulation): The best constraint is one that makes wrong code fail to compile or instantiate. Second best: fail at construction time. Third: fail at call time with a clear error. Last resort: document it.

```python
# Level 4 (worst) — runtime surprise, hard to trace
def transfer(from_id, to_id, amount):
    # documented: amount must be positive
    ...

# Level 3 — fails at call time
def transfer(from_id: AccountId, to_id: AccountId, amount: Decimal):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")

# Level 2 — fails at construction
@dataclass
class TransferAmount:
    value: Decimal
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(...)

# Level 1 (best for critical invariants) — compile-time via type
PositiveDecimal = NewType("PositiveDecimal", Decimal)
# construction validated by a smart constructor that returns PositiveDecimal only if valid
```

**Constraint design in system architecture:**
- Read-only replicas by default; write access requires explicit opt-in
- `--dry-run` as a universal constraint on mutating CLI commands
- Blast-radius bounding: infrastructure that fails closed, not open
- Circuit breakers as runtime constraints on dependency failure propagation

**Negative transfer warning:** Constraints have a cost — they reduce flexibility and increase implementation complexity. The value of a constraint is proportional to how hard the error is to find when the constraint is violated. Invest constraints where violations would cause production incidents or data loss. Don't constrain everything.

---

## Conceptual Model — Extended

**Three-layer model test (from Lakoff & Johnson):**

1. **Language layer:** Do the labels match domain terms users already use? If users say "subscription" and the API says "billing_plan_instance", the conceptual model is already fractured.

2. **Behavior layer:** Does the system do what it looks like it will do? If `delete_user` also deletes their orders, invoices, and audit logs without warning, the behavior layer breaks the model.

3. **Feedback layer:** Does the system report what just happened and what happens next? The model holds up only if the system confirms its own behavior.

**Leaky abstraction test:** If a caller must understand the implementation to debug or correctly use the interface, the abstraction is leaking. The implementation model is bleeding through.

```python
# Leaky: caller must understand connection pooling internals to use correctly
pool = ConnectionPool(host="db", max_connections=10)
conn = pool.get()  # what happens if pool is exhausted? if connection is stale?

# Non-leaky: pool manages its own lifecycle, caller just uses connections
with pool.connection() as conn:
    result = conn.execute(query)
# connection is returned/recycled transparently
```

**Metaphor selection matters:** The metaphor you choose for an abstraction constrains what users will expect from it. Choose metaphors from domains your callers already understand:
- `Session` → web browsing (stateful, closeable, reusable)
- `Stream` → water (flows in one direction, can be piped)
- `Queue` → waiting in line (FIFO, add to back, take from front)
- `Pool` → swimming pool (borrow a lane, return it, lanes are shared)

When your implementation violates the chosen metaphor, users' predictions will be wrong.

---

## Information Scent — Extended

**Origin:** Pirolli & Card's information foraging theory draws on animal foraging behavior — organisms follow "patches" of food by following scent. In information spaces, users follow cues (scent) that suggest they're getting warmer.

**Code-level scent:**

Strong scent names communicate *domain* not *mechanism*:
```
app/payments/charge.py       ← strong scent (domain concept)
app/handlers/payment_v2.py   ← weak scent (mechanism + version)
app/services/service3.py     ← no scent (pure structure, no meaning)
```

**The graveyard of scent:** `utils/`, `helpers/`, `common/`, `shared/`, `misc/` — these names contain every kind of scent, so they contain no scent at all. They are the design equivalent of a room labeled "stuff." Anything placed there becomes unfindable.

**Renaming test:** If you had to rename a module to make a new engineer find it on their first try, what would you call it? That's the right name.

**Import path as scent trail:**
```python
# Every token narrows the search — strong scent trail
from app.billing.invoices.line_items import calculate_tax

# Trail goes cold — "what kind of util? what does it help with?"
from utils.helpers import calculate_tax
```

**API endpoint scent:**
- `GET /users/{id}/orders` — strong scent, navigable hierarchy
- `POST /process` — no scent, what gets processed? in what way?

---

## Signal-to-Noise — Extended

**Tufte's data-ink ratio:** In statistical graphics, "data-ink" is ink that encodes data. Everything else is noise. Maximize the ratio.

**Software mapping:**
- **Signal:** lines that express domain logic, business rules, meaningful computation
- **Noise:** boilerplate, adapter code, scaffolding, ceremony, comments explaining what (not why)

**Code noise patterns:**
```python
# Noise: comment explains what the code already says
# Increment counter by 1
counter += 1

# Noise: method that only delegates, adds no value
def get_user(self, user_id):
    return self._user_repository.get_user(user_id)

# Noise: builder pattern wrapping a simple constructor
user = UserBuilder() \
    .set_name("Alice") \
    .set_email("alice@example.com") \
    .set_role(Role.ADMIN) \
    .build()

# Signal version
user = User(name="Alice", email="alice@example.com", role=Role.ADMIN)
```

**When noise is necessary:** Some noise is unavoidable (imports, type boilerplate in some languages, framework wiring). The question is whether it's in the right place — aggregated and isolated, not scattered through domain logic.

**CLI output signal-to-noise:**
- Progress output: every line should tell the user something they didn't know. If 95% of lines are "processing file X...", that's noise.
- Errors: the error message is the entire signal. Avoid stack traces by default; surface them only on `--verbose`.

---

## Negative Space — Extended

**Design precedents:**
- Mies van der Rohe: "Less is more" — restraint as a positive design act
- Dieter Rams: "Good design is as little design as possible" — remove everything not serving the user's goal
- Japanese *ma* (間): the meaningful pause, the deliberate emptiness

**In software, negative space takes these forms:**

*API surface exclusion:*
```python
# Adding XML support because someone might want it → positive space bloat
# Explicitly not supporting XML → negative space, deliberate boundary
# The exclusion is a design decision that keeps everything else simpler
```

*Dependency refusal:*
```python
# app/payments/ deliberately does not import from app/notifications/
# That boundary is the design. The absence is the feature.
```

*Feature restraint:* Not adding a flag because the use case is rare, even though it would be easy to add. The flag-you-didn't-add is negative space.

**How to exercise it:** Before adding any parameter, method, or endpoint, ask: "What does this NOT do that it might be expected to do?" Name the exclusion. Make it deliberate. If you can't articulate why it's excluded, you haven't finished the design.

**Negative transfer warning:** "As little as possible" is not an excuse to skip error handling, observability, or safety checks. Those aren't excess design — they're core to the product. Negative space is for features and surface area, not for operational correctness.

---

## Gestalt Principles Applied to Code — Extended

**Origin:** Gestalt psychology (Wertheimer, Köhler, Koffka, 1920s Germany). The mind organizes sensory input into coherent patterns before conscious analysis.

| Gestalt Principle | Code Application |
|---|---|
| **Proximity** | Code that belongs together should be near each other. Related functions in a class, related constants near their usage, related tests adjacent to the code they test. |
| **Similarity** | Things that look alike should behave alike. Consistent naming, consistent parameter order, consistent return conventions. If two functions have similar names, callers will assume similar behavior. |
| **Common Region** | Enclosure groups elements. Module boundaries, class bodies, and file organization signal "these things belong to the same concern." |
| **Continuity** | The eye follows smooth paths. Control flow should read top-to-bottom, left-to-right, without surprising jumps. Avoid early returns buried deep in functions; avoid goto-like constructs. |
| **Figure/Ground** | Important elements stand out from the background. Domain logic should be the figure; infrastructure, error handling, and logging should recede into the ground. |
| **Closure** | The mind completes familiar patterns. Consistent structure allows readers to fill in what they haven't read. If all your service classes follow the same shape, readers understand new ones faster. |

**Practical implication:** Inconsistency is noise that forces conscious attention. When naming conventions, parameter order, and error conventions are inconsistent, readers must consciously parse each new instance instead of pattern-completing. Consistency is a cognitive load reduction strategy.

---

## Wicked Problems — Extended

**Rittel & Webber (1973):** Wicked problems are problems that can't be fully specified before solving begins, where solving changes the problem, where there's no definitive solution, and where every attempt has consequences.

**This is the normal state for API design.** You cannot know the full API surface before you've built anything on it. The first version will be wrong. The question is how wrong, and how recoverable.

**Design implications:**

1. *Ship a minimal surface.* Every exposed API method is a permanent commitment. Things you don't expose today can always be added. Things you expose today must be supported forever (or versioned at significant cost).

2. *Treat v1 as an explicit learning exercise.* The purpose of v1 is to discover what v2 should be. Design for versioning from day one.

3. *ADRs as hypothesis records.* Architecture Decision Records document not just decisions but the assumptions behind them. When assumptions change, you know exactly which decisions to revisit.

4. *Progressive disclosure in versions.* Start with the common case. Add power-user paths in v2 based on observed needs, not anticipated ones.

**Anti-pattern:** A 40-page API specification written before any implementation. By the time implementation reveals what the data model actually requires, the spec is fiction and the author must either defend the fiction or start over.

---

## Atomic Composition — Extended

**Alexander's insight (The Timeless Way of Building):** Complex, living systems emerge from simple, stable, composable parts — not from top-down imposition of a total design. Each pattern is a solution to a recurring problem in context. Patterns connect to each other, forming languages.

**Software expression:**

*Unix philosophy:* Small tools that do one thing well, composable via pipes. The composition surface is the interface (stdin/stdout).

*Functional composition:* Pure functions that transform values. Composition surface is type compatibility.

*React/component model:* Atomic components that compose into molecules, organisms, pages. Composition surface is props interface.

*Terraform modules:* Composable infrastructure blocks. Composition surface is input/output variables.

**The failure mode:** Monolithic designs that try to do everything in one abstraction. The `UserManager` that handles CRUD, email notifications, audit logging, CSV export, and permission checking. When a class or module has no coherent composition surface — when it can only be used as a whole, never as a part — it's not atomic.

**Test for atomicity:** Can this module/class/function be used in isolation, without pulling in unrelated concerns? If `import payments` also brings in `notifications`, `audit`, and `reporting`, it's not atomic — it's a dependency web masquerading as a module.
