---
name: test-desiderata
description: Apply Kent Beck's Test Desiderata to write higher-quality tests — covers the 12 properties (isolated, composable, deterministic, fast, writable, readable, behavioral, structure-insensitive, automated, specific, predictive, inspiring) and how to reason about tradeoffs between them
compatibility: opencode, claude-code
---

## What I do

I guide test authoring using Kent Beck's Test Desiderata — 12 properties that make tests valuable. I help you reason about which properties matter most for a given test, where tensions exist, and how to resolve them.

## The 12 properties

**Isolated** — Tests return the same results regardless of run order. No shared mutable state between tests; each test sets up and tears down its own context.

**Composable** — Different dimensions of variability can be tested separately and results combined. Enables targeted, focused tests that can be mixed and matched.

**Deterministic** — If nothing changes, the test result does not change. Eliminate sources of non-determinism: time, randomness, network, filesystem ordering.

**Fast** — Tests run quickly. Prefer in-process fakes over real I/O; reserve slow integration tests for a separate suite.

**Writable** — Tests are cheap to write relative to the cost of the code under test. Reduce boilerplate; invest in test helpers and builders where the payoff is clear.

**Readable** — Tests are comprehensible to a reader. The test should convey *why* it exists — what behavior is being verified and under what conditions.

**Behavioral** — Tests are sensitive to changes in behavior. If the behavior changes, the test should fail. Avoid testing implementation details that can vary without changing behavior.

**Structure-insensitive** — Tests do not change result when code is refactored. Couple tests to the public interface and observable behavior, not internal structure.

**Automated** — Tests run without human intervention. No manual steps, no visual inspection of output required to determine pass/fail.

**Specific** — When a test fails, the cause of failure is obvious. Prefer one logical assertion per test; give tests and assertions descriptive names.

**Predictive** — If all tests pass, the code is suitable for its intended use. Tests should cover the cases that actually matter in production.

**Inspiring** — Passing tests inspire confidence. A green suite should feel meaningful, not like a formality.

## Tradeoffs to reason about

Some properties reinforce each other:
- Automating tests also makes them faster to trigger.
- Isolated tests are easier to make deterministic.
- Specific tests are more readable.

Some properties tension each other:
- **Predictive vs. Fast**: tests that closely mirror production (real DB, real network) are slower.
- **Behavioral vs. Writable**: highly behavioral tests sometimes require more setup to exercise the full interface.
- **Composable vs. Readable**: composing many small tests can obscure the overall intent.

The resolution is often composability: test units in isolation (fast, specific) and compose them into a smaller number of integration tests that are predictive. Avoid the trap of treating all 12 as equally mandatory — choose the right tradeoff for the test layer you are writing.

## Reflection prompts

When writing a test, ask:
- Which properties does this test have? Which does it lack?
- Is that the tradeoff I want to make?
- If the tests all pass, would I feel confident deploying?

## How to use these properties when writing tests

1. **Arrange–Act–Assert**: set up state, perform one action, assert one outcome. Keep each section visually distinct.
1. **Prefer real objects over mocks** for domain logic; reserve mocks for I/O boundaries.
1. **Seed controlled data** rather than relying on pre-existing database state.
1. **Assert on outcomes visible to callers** (return values, state changes, emitted events) — not on internal calls.
1. **Delete tests that no longer inspire confidence** or that pass vacuously. One good test is better than 10 sloppy ones.

## When to load this skill

Load this skill when:
- Writing new tests from scratch
- Reviewing or critiquing existing tests
- Deciding what to test and at what level (unit / integration / end-to-end)
- Debugging a flaky or over-specified test

## Explore the space

Don't accept defaults. Question assumptions:
- "Tests just have to run in a minute or more" — why?
- "Tests just have to be non-deterministic" — change the design
- "Tests just change when code structure changes" — should they?

Take these principles. Find a test that violates them. Imagine the equivalent test that would satisfy the principles. If you can't write that test, imagine the design of the software under test that would enable a test satisfying the principles.
