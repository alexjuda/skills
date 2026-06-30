---
name: design-theory-for-software
description: Use when designing APIs, modules, CLIs, or system architecture — and when reviewing existing code for structural quality. Applies design wisdom from graphic, industrial, and UX design to software engineering decisions. Not for UI pixel work; for the shape of interfaces, abstractions, and systems.
---

# Design Wisdom for Software

Good software design and good industrial/graphic design share deep structure. This skill transplants that structure — the principles, vocabulary, and *process* of traditional design — into software engineering.

**Scope:** APIs, module interfaces, CLIs, system architecture, code organization, developer experience. Not UI pixels or visual styling.

---

## Companion Files — Load Before Using

This skill has two companion files with extended content. Load them now with `Read`:

- **[principles-reference.md](./principles-reference.md)** — Full citations, extended examples, negative transfer warnings for every lens
- **[patterns-library.md](./patterns-library.md)** — Concrete patterns for APIs, CLIs, module organization, documentation, and observability

Inline references below point to relevant sections in these files.

---

## When to Invoke

- Designing a new API, module interface, or CLI command surface
- Naming abstractions, choosing what to expose vs. hide
- Reviewing code for structural quality (not just correctness)
- Something feels off about a design but you can't articulate why
- Deciding what NOT to build

---

## Core Insight: Design Is a Process, Not a Checklist

The deepest transplant from design practice is not any single principle — it's the **process**:

1. **Frame before solving** — Designers restate the problem before touching a solution. "We're not designing a button; we're designing a way for users to commit." What is the human need, not the technical requirement?

2. **Sketch alternatives before committing** — Designers produce 10–20 rough variations before refining one. For software: sketch 3 different calling conventions, 3 different module boundaries, 3 different names — on paper or in pseudocode — before writing real code. The first idea is rarely the best one.

3. **Critique separately from execution** — Design critique asks "does this solve the problem?" before "is it executed well?" In code review, these collapse. Separate them: first evaluate the interface shape and conceptual model, then evaluate the implementation.

4. **Treat early designs as hypotheses** — All interesting software problems are wicked problems (Rittel & Webber, 1973): you can't fully understand the problem until you've started solving it. Release a minimal surface, observe real usage, iterate. API design is hypothesis, not prophecy.

---

## The Design Lenses

Apply these as questions, not rules. Each lens reveals a different dimension of quality.

### 1. Affordances — Does the shape communicate use?

An affordance is a property that suggests how something should be used (Norman, *The Design of Everyday Things*). In code, the shape of a function, the name of a parameter, the structure of a type — these communicate what the caller should do.

**Ask:** Can a caller understand correct usage from the signature alone, without reading the body or docs?

```python
# Weak affordances — shape communicates nothing
process(data, True, None, "", False, -1)

# Strong affordances — shape communicates intent
query.filter(status="active").order_by("created_at").limit(50)
create_user(*, name: str, email: Email, role: Role) -> User
```

**Red flag:** If correct usage requires reading the implementation.

> See [principles-reference.md](./principles-reference.md) for the critical affordance/signifier distinction and negative transfer warnings.

---

### 2. Signifiers — Does the design guide toward correct usage?

Affordances exist whether perceived or not. Signifiers *make affordances visible* (Norman, 2013). Type hints, names, docstrings, error messages — these are signifiers that guide the caller.

**Ask:** When someone misuses this, do they get an immediate, helpful signal pointing to the fix?

```python
# No signifier — silent wrong behavior
def schedule(start=None, end=None): ...

# Strong signifier — error is the guide
@dataclass
class DateRange:
    start: datetime
    end: datetime
    def __post_init__(self):
        if self.end < self.start:
            raise ValueError(f"end ({self.end}) must be after start ({self.start})")
```

**CLI signifier:** `Error: --config is required. Run 'mytool init' to generate one.` — not just "missing flag."

> See [principles-reference.md](./principles-reference.md) for the four levels of signifiers and observability as signifier patterns.

---

### 3. Constraint Design — Are invalid states unrepresentable?

Constraints reduce available actions, making errors impossible or difficult rather than merely documented (Norman, ch. 4). The best constraint is one the user never encounters because the type system or API shape prevents the mistake.

**Ask:** What invalid states does this interface allow that it shouldn't?

```python
# Allows invalid state — str could be anything
def send_email(to: str, subject: str, body: str): ...

# Constrains invalid state at the type level
def send_email(to: EmailAddress, subject: Subject, body: str): ...

# Closed enumeration — can't pass unsupported values
Action = Literal["create", "update", "delete"]
```

**Infrastructure:** Circuit breakers, `--dry-run`, confirmation prompts for destructive actions. Fail closed, not open.

> See [principles-reference.md](./principles-reference.md) for Norman's constraint taxonomy and the "make invalid states unrepresentable" ladder.

---

### 4. Conceptual Model — What picture forms in the caller's mind?

The conceptual model is the mental representation a user builds about how a system works (Norman; Lakoff & Johnson, *Metaphors We Live By*). The best designs present a simple, consistent, predictable model — even if the implementation is complex.

**Ask:** If a new caller explains this API back to you after 5 minutes, what would they say? Is that accurate?

```python
# Good: requests.Session() — presents "persistent stateful connection" model.
# The metaphor is consistent with how browsers work. It holds up under use.

# Bad: A "connection pool" where connections silently expire.
# The implementation model leaks through — caller must understand internals to debug.
```

**Rule:** The abstraction should never force the caller to reason about the implementation. When the abstraction leaks, the conceptual model is broken.

> See [principles-reference.md](./principles-reference.md) for the three-layer model test and metaphor selection guidance.

---

### 5. Information Scent — Can someone find the right thing without reading everything?

Information scent is the cue density that tells a person they're getting closer to their goal in an information space (Pirolli & Card, 1999). Strong scent = efficient navigation. Weak scent = random search.

**Ask:** Given only the names visible from outside, can a new engineer guess where to look?

```python
# Strong scent — every token narrows the target
from app.api.v2.users import create_user

# Scent void — dead end, forces reading internals
from utils import helpers
```

**Graveyard names:** `utils/`, `helpers/`, `common/`, `misc/`, `lib/` — these are where scent goes to die. Names like these signal that the author deferred the design decision.

> See [principles-reference.md](./principles-reference.md) for the renaming test and API endpoint scent patterns.

---

### 6. Signal-to-Noise — Is every element earning its place?

Tufte's data-ink ratio applied to code: maximize the proportion of content that carries meaning; minimize ceremony, boilerplate, and scaffolding that obscures intent (Tufte, *The Visual Display of Quantitative Information*, 1983).

**Ask:** If you removed this, would anything important be lost? Does each parameter, method, and abstraction layer earn its presence?

```python
# High noise — ceremony obscures a simple intent
client.NewRequest(ctx).WithEndpoint("/users").WithMethod("POST") \
      .WithBody(serialize(user)).WithTimeout(30).Execute()

# High signal — intent is immediate
client.create_user(user)
```

**For CLIs:** Does every line of default output carry information? Verbose-by-default is a noise problem.

> See [patterns-library.md](./patterns-library.md) for the CLI Feedback Contract pattern (timing table, failure feedback).

---

### 7. Negative Space — What are you explicitly not doing?

In design, negative space is as intentional as positive space. What you *exclude* shapes the design as much as what you include. "As little design as possible" (Dieter Rams) — not no design, but removing everything that doesn't serve the user's goal.

**Ask:** Is this addition earning its place, or is it there because it was easy to add? What deliberate boundaries does this design have?

```python
# Good — explicit boundary, coherent surface
class PaymentProcessor:
    def charge(self, amount: Money, card: Card) -> Receipt: ...
    def refund(self, receipt: Receipt) -> Refund: ...
    # Does NOT send emails, does NOT log to Slack, does NOT update inventory

# Bad — scope creep erodes the model
class PaymentProcessor:
    def charge(...): ...
    def send_confirmation_email(...): ...   # why is this here?
    def log_to_slack(...): ...              # now what is this class?
```

**The discipline:** Every feature added to a surface is a feature the caller must learn, remember, and reason about forever.

---

### 8. Cognitive Load — Can a human hold this in mind?

Working memory is limited to ~4±1 chunks (Cowan, 2005). Every concept, parameter, abstraction layer, and edge case the caller must track consumes a slot.

**Ask:** Can a competent engineer understand this from the public interface in one sitting, without notes?

- Functions with > 4 parameters almost always hide a missing abstraction
- Classes where you need to read 3 parent classes to understand one method are too deep
- A module you can't summarize in one sentence probably has two responsibilities

**Gestalt:** Related things should *look* related. Code that belongs together should be near each other, named similarly, and visually grouped. The human eye organizes by proximity and similarity before it reads — design with this, not against it.

> See [principles-reference.md](./principles-reference.md) for the full Gestalt-to-code mapping table.

---

## Design Critique Workflow

When reviewing existing code through a design lens (separate from correctness review):

```
1. FRAME: What is this interface for? Who calls it? What is their goal?

2. CONCEPTUAL MODEL TEST: Without reading the implementation, what model
   does the public interface present? Is it accurate? Is it simple enough?

3. LENS SWEEP: Run each lens as a question:
   - Affordances: shape communicates use?
   - Signifiers: errors/types guide correct usage?
   - Constraints: invalid states prevented, not just documented?
   - Scent: names lead to the right place?
   - Signal/Noise: every element earning its place?
   - Negative Space: deliberate exclusions visible?
   - Cognitive Load: holdable in working memory?

4. PRIORITIZE: Which lens violations actually matter for this context?
   Not every issue is worth fixing. Name the top 1-3.

5. SUGGEST: Ground suggestions in the principle, not personal preference.
   "This parameter adds cognitive load without enabling a use case that
   couldn't be handled by X" is better than "I'd simplify this."
```

---

## Applying Before Implementation

When *designing* something new, use this sequence:

1. **Frame the problem** — What is the human need? What is the caller's goal? (Not: what function do I need to write?)

2. **Sketch alternatives** — Produce 2–3 rough calling conventions in pseudocode. Don't refine any of them yet.

3. **Apply the lenses** — Which sketch has the strongest affordances? The cleanest conceptual model? The least cognitive load?

4. **Choose and articulate the model** — Before writing implementation, be able to state: "The mental model this API presents is ___." If you can't state it simply, the design isn't ready.

5. **Implement** — Now write the real code. The design is a hypothesis; plan to iterate.

---

For deeper treatment of any lens, see [principles-reference.md](./principles-reference.md) and [patterns-library.md](./patterns-library.md).
