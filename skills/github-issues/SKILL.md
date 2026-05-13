---
name: github-issues
description: Guide for writing effective GitHub issues — what to include, what to exclude, and common mistakes
compatibility: opencode, claude-code
---

## Essential sections

**Title** — Concise, specific. "ux: make the CLI delightful" not "CLI Improvements"

**Problem** — What's broken? Who experiences it? What's the impact?

**Proposed Solution** — What needs to happen? Keep it at the *what* level, not the *how*.

## What to include vs. exclude

Include: Commands, flags, user-facing behaviors, error scenarios.

Exclude: Implementation details (libraries, frameworks, file structure), code examples, "Implementation Notes" sections.

## Good practices

- Be concise. Cut the fluff.
- Describe the *what*, not the *how*
- Focus on user experience, not architecture
- One clear problem statement
- Keep it skimmable—use lists, not paragraphs

## Common mistakes

- Adding implementation suggestions (frameworks, libraries)
- Including example output/code
- Writing "Implementation Notes" or "Technical Details"
- Too much structure (nested sections, elaborate formatting)
- Prescribing solutions instead of describing problems
- Verbose explanations of obvious things
