# Domain Pattern Library

Concrete patterns for applying design wisdom to specific software engineering contexts.

---

## API Design Patterns

### Abstraction Ladder (Flexible → Gradual → Convenient)

Every API should serve users at multiple skill levels. Stripe's framework:

1. **Flexible first** — The API is composable; operations return types that feed back in. Advanced users can build anything.
2. **Gradual second** — Complexity reveals itself progressively. Novices become experts without hitting walls.
3. **Convenient third** — Common combinations are packaged as shortcuts. But don't over-package.

**Market reality:**
- No convenience → beginners don't adopt
- No gradual → novices never become experts  
- No flexibility → power users leave

**Example (Stripe-style):**
```python
# Convenient: common case is trivial
charge = stripe.Charge.create(amount=2000, currency="usd", source=token)

# Flexible: full composition for complex flows
payment_intent = stripe.PaymentIntent.create(
    amount=2000, currency="usd",
    payment_method_types=["card"],
    metadata={"order_id": "6735"}
)
payment_intent.confirm(payment_method=pm_id, return_url=url)
```

---

### Object-First Navigation

Organize APIs around domain objects, not HTTP verbs or protocol details.

Instead of callers scanning a flat list of operations, they navigate to the object they care about, then see its operations.

```
# Flat list (hard to navigate)
GET /users
POST /users
DELETE /users/{id}
GET /orders
POST /orders
...

# Object-first (easy to navigate)
Users:
  list, create, get, update, delete, suspend, restore

Orders:
  list, create, get, cancel, fulfill, refund
```

**Rule:** The structure of your API should match the conceptual model of the domain, not the implementation structure.

---

### Error as Interface

Error handling is your most important interface. Design it with at least as much care as success responses.

**RFC 9457 (Problem Details for HTTP APIs):**
```json
{
  "type": "https://api.example.com/errors/payment-declined",
  "title": "Payment Declined",
  "status": 402,
  "detail": "The card ending in 4242 was declined. Insufficient funds.",
  "instance": "/trace/req_abc123",
  "docs_url": "https://api.example.com/docs/errors/payment-declined"
}
```

**Four principles of good errors:**
1. **Visible** — Never silent failures. Include request ID for correlation.
2. **Understandable** — Human-readable detail, not internal error codes.
3. **Actionable** — Tell the caller what to do, not just what went wrong.
4. **Stable** — Never change error shapes. Treat them as API contracts.

**Recovery patterns:**
```python
# Exponential backoff for transient failures
time.sleep(min(2 ** attempt + random.random(), 60))

# Idempotency key to make retries safe
response = client.charges.create(
    amount=2000,
    idempotency_key=f"order-{order_id}-charge"
)
```

---

### Principle of Least Astonishment

API behavior should not surprise a caller who has read only the name and signature.

**Checklist:**
- Does the function name accurately describe all of what it does? (Including side effects)
- Do consistent names signal consistent behavior? (`delete_*` should always delete, not sometimes soft-delete)
- Are defaults safe? (fail closed, not open; return empty collection, not None)
- Do return types tell the whole story? (`Optional[User]` tells you it might not find one; `User` should never return None)

**Anti-patterns:**
```python
# Astonishing: name implies read, but actually writes
def get_or_create_user(email: str) -> User: ...

# Fix: make the write explicit
def find_user(email: str) -> User | None: ...
def create_user(email: str) -> User: ...
def ensure_user_exists(email: str) -> User: ...  # name signals write is possible
```

---

### Sensible Defaults, Explicit Overrides

The most common case should require the fewest decisions.

```python
# Bad: everything explicit, no defaults — high cognitive load for common case
client = DatabaseClient(
    host="localhost",
    port=5432,
    pool_min=1,
    pool_max=10,
    timeout_seconds=30,
    retry_on_disconnect=True,
    ssl_mode="require"
)

# Good: sensible defaults, explicit overrides only when needed
client = DatabaseClient(host="localhost")  # 90% case
client = DatabaseClient(host="db.prod", pool_max=50, ssl_mode="verify-full")  # 10% case
```

**Rule:** Every required parameter is a design cost imposed on every caller, forever. Parameters should be required only when there is genuinely no sensible default and no obvious choice.

---

## CLI Design Patterns

### Progressive Disclosure in Commands

Common paths should be obvious; power should be discoverable.

```
# Layer 0 — the thing most people do, right in --help
mytool deploy

# Layer 1 — flags for the 20% cases
mytool deploy --env staging --dry-run

# Layer 2 — subcommands for complex operations
mytool deploy rollback --to v1.2.3

# Layer 3 — advanced flags that live behind --help
mytool deploy --strategy blue-green --timeout 600 --parallel 3
```

**Rule:** Don't penalize the common case to support the edge case. Hide complexity behind flags and subcommands; make them discoverable but not required.

---

### Feedback Contract

Every long-running operation should maintain a feedback contract with the user:

| Duration | Expected feedback |
|---|---|
| < 100ms | No feedback needed |
| 100ms–1s | Should feel instant; spinner optional |
| 1–10s | Progress indicator |
| > 10s | Progress + estimated time |
| > 30s | Progress + ability to cancel |

```
# Bad: silent for 2 minutes
$ mytool build
[2 minutes pass]
Done.

# Good: maintains the contract
$ mytool build
→ Resolving dependencies (12/47)...
→ Compiling (3/12 modules)...
→ Running tests (47/200)...
✓ Build complete in 2m 14s
```

**Failure feedback:** When a command fails, tell the user:
1. What failed
2. Why (if knowable)
3. How to fix it

```
# Bad
Error: exit code 1

# Good
Error: Database migration failed
  Cause: column 'user_id' in 'sessions' table has 847 non-null rows that don't
         match any row in 'users'. Migration requires referential integrity.
  Fix:   Run 'mytool db cleanup-orphan-sessions' first, then retry.
  Docs:  https://docs.example.com/migrations/fk-constraints
```

---

### Constraint Defaults for Dangerous Operations

Mutating and destructive commands should be constrained by default:

```bash
# --dry-run as universal constraint
mytool delete-env production --dry-run
# → Would delete: 14 services, 3 databases, 7 load balancers
# → Use --confirm to proceed

# --force for deliberate overrides
mytool deploy --force  # skips health checks

# Confirmation prompt for irreversible operations
mytool drop-database production
# → WARNING: This will permanently delete all data.
# → Database has 2.3M rows and 47GB of data.
# → Type the database name to confirm: ____
```

**Rule:** The default behavior of a dangerous command should be to do nothing dangerous. The dangerous path requires explicit intent.

---

## Module / Code Organization Patterns

### Domain-Aligned Structure

Module structure should match domain structure, not implementation structure.

```
# Implementation-aligned (bad) — structure reflects technical layers
app/
  models/
    user.py, order.py, payment.py, product.py  # all data models together
  services/
    user_service.py, order_service.py ...       # all services together
  handlers/
    user_handler.py, order_handler.py ...       # all handlers together

# Domain-aligned (good) — structure reflects business concerns
app/
  users/        # everything about users
    models.py, service.py, api.py, __init__.py
  orders/       # everything about orders
    models.py, service.py, api.py, __init__.py
  payments/     # everything about payments
    models.py, service.py, api.py, __init__.py
```

**Why:** When you need to change how "orders" work, everything you need is in one place. You don't need to grep across 6 directories.

---

### Dependency Direction as Design

In a well-designed codebase, dependencies flow in one direction. This is constraint design at the architectural level.

```
# The hierarchy (each layer can import from layers below, never above)
API / Handlers       ← HTTP concerns, request/response
     ↓
Services / Use Cases ← Business logic
     ↓
Domain / Models      ← Core entities, value objects
     ↓
Infrastructure       ← Database, external APIs, messaging
```

**Test:** `grep "from app.handlers import" app/domain/*.py` should return nothing. If domain imports from handlers, the dependency direction is inverted — you've coupled your core logic to a delivery mechanism.

---

### The `__init__.py` as Design Document

A module's `__init__.py` with explicit `__all__` is a design document. It defines the public interface and forces you to be deliberate about what you expose.

```python
# app/payments/__init__.py
"""
Payment processing domain.

Public interface:
  - charge(amount, payment_method) → Receipt
  - refund(receipt) → Refund
  - list_charges(account_id) → list[Receipt]
"""

from .charge import charge
from .refund import refund
from .queries import list_charges

__all__ = ["charge", "refund", "list_charges"]

# Everything else is implementation detail
# _processor, _validation, _webhook_handler are NOT exported
```

**Rule:** If you can't write a one-paragraph module docstring that accurately describes what the module does, the module has too many responsibilities.

---

### Naming as Information Scent

**Strong scent names** (communicate domain concept):
- `payment_processor`, `invoice_generator`, `user_authenticator`
- `scheduled_for`, `expires_at`, `cancelled_reason`
- `SeatReservation`, `FlightManifest`, `BoardingPass`

**Weak scent names** (communicate structure, not meaning):
- `data_handler`, `process_manager`, `item_controller`
- `flag`, `result`, `status`, `value`, `info`
- `Manager`, `Helper`, `Util`, `Base`

**Rule for weak names:** If a name could describe code in 5 different modules, it's not a name — it's a placeholder. Replace it with the specific domain concept.

```python
# "result" — communicates nothing
result = process(data)

# Domain-specific — communicates the actual thing
invoice = generate_invoice(order)
auth_token = authenticate_user(credentials)
validation_errors = validate_shipping_address(address)
```

---

## Documentation Patterns

### Diátaxis Framework

Documentation serves four distinct purposes. Mixing them produces documents that serve none well.

| Quadrant | Purpose | Form | Reader state |
|---|---|---|---|
| **Tutorial** | Learning | Guided narrative | "I'm new, teach me" |
| **How-To Guide** | Task completion | Steps | "I know what I want, show me how" |
| **Reference** | Lookup | Comprehensive catalog | "I need a specific fact" |
| **Explanation** | Understanding | Conceptual discussion | "I want to understand why" |

**Common failure:** Mixing explanation into reference docs. Reference must be complete and scannable; explanation interrupts the scan. Put the "why" in an explanation page, link to it from reference.

---

### Bottom Line Up Front

Readers scan — they decide in the first sentence whether to keep reading.

```markdown
# Bad: buries the point
The authentication system in this application uses JWT tokens, which are
signed using RS256, and it integrates with our identity provider...
[300 words later]
...so to authenticate, call POST /auth/login with email and password.

# Good: BLUF
Authenticate by calling POST /auth/login with email and password.
Returns a JWT token valid for 24 hours.

**Details:**
[depth follows for those who want it]
```

**Every heading should be informative on its own.** A reader scanning headings should be able to find what they need without reading body text.

---

### Code Examples as First-Class Content

A good code example does more work than a paragraph of prose.

**Standards for examples:**
- Syntactically correct and runnable as-is
- Uses real-looking values, not `"YOUR_VALUE_HERE"` or `"string"`
- Shows the complete happy path in the simplest case
- Shows error handling in the next example
- Includes output where output is meaningful

```python
# Bad example — reader has to fill in gaps
result = client.create(your_object)
print(result.id)

# Good example — reader can copy and adapt
from mylib import Client

client = Client(api_key="sk_test_4eC39HqLyjWDarjtT1zdp7dc")

invoice = client.invoices.create(
    customer_id="cus_NffrFeUfNV2Hib",
    amount=2000,          # amount in cents
    currency="usd",
    due_date="2025-02-01",
)

print(f"Created invoice {invoice.id}, due {invoice.due_date}")
# → Created invoice inv_1OVMyr2eZvKYlo2C8Nf5mFEB, due 2025-02-01
```

---

## Observability as Design

Operational interfaces deserve the same design attention as developer interfaces. An on-call engineer navigating an incident is a user with a goal: understand what broke and why.

> **Note:** For structured logging patterns as signifiers, see [principles-reference.md](./principles-reference.md#signifiers--extended) — covers observability signifiers, structured logging, and event naming.

### Dashboard as Hierarchy at Every Scale

A good monitoring dashboard should answer the core question at each zoom level:

- **Level 1 (system):** Is anything on fire right now?
- **Level 2 (service):** Which service has a problem?
- **Level 3 (component):** What is failing — latency, error rate, saturation?
- **Level 4 (instance):** Which specific host/pod/region?

**Anti-pattern:** A dashboard that requires level-4 reading to answer the level-1 question. If you need to read 40 graphs to know if the system is healthy, the information hierarchy is broken.
