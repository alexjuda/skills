---
name: tdd
description: Apply Test-Driven Development — red/green/refactor cycle to drive code and design
compatibility: opencode, claude-code
---

## Step 0: Plan the Approach

Read the codebase to understand the structure. Then:
- Identify what modules/classes need unit tests
- Decide where integration tests are warranted
- List test scenarios before writing any code (see below)
- Determine testing priority

Ask the human for input on genuinely ambiguous decisions (e.g., "should X be a unit test or integration test?"). Propose alternatives and tradeoffs.

### List Test Scenarios First

Before entering the red/green/refactor cycle, write out an initial list of test cases for the feature:
- What's the happy path?
- What edge cases exist?
- What error conditions should be handled?
- What if a service times out? What if data doesn't exist?

This is not a complete plan—it's a starting point. As you implement and learn, add missing cases to the list. Don't try to envision the whole implementation upfront; that would be waterfall. Start with the simplest case to establish the basic interface, then add progressively more complex scenarios.

## The Cycle (One Test at a Time)

For each element in the plan:

1. **Red** — Write a SINGLE failing test. One behavior, one assertion.
2. **Green** — Write minimal code to make it pass.
3. **Refactor** — Clean up while keeping tests green.
4. **Ask for feedback** — Wait for human input before proceeding to the next test.

Repeat for each test case.

## Principles

- Tests drive design: hard to test = design problem
- Minimal implementation: only what's needed now
- Fast feedback: run tests every few minutes
- One test at a time: write one, not multiple

## Connecting to Test Desiderata

See [test-desiderata skill](/skills/test-desiderata/SKILL.md). TDD works best with tests that are isolated, fast, readable, behavioral, and specific.

## Common Mistakes

- Skipping the planning step
- Writing multiple tests at once (the main TDD failure mode)
- Skipping red (tests after implementation defeats TDD)
- Green-slopping (ugly code that passes, no refactor)
- Not asking for feedback before continuing

## When to Load

- New code or features
- Fixing bugs (test first to reproduce)
- Refactoring (tests provide safety)
