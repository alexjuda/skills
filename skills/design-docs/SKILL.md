---
name: design-docs
description: Guide for writing effective software design documents — covers structure, good practices, what to include/exclude, and common mistakes
compatibility: opencode, claude-code
---

## Essential sections

**Problem Statement** — Why are we doing this? Who experiences it? What's the impact?

**Scope** — In and out of scope. Explicit boundaries prevent creep.

**Architecture** — Components, relationships, data flow. ASCII/Mermaid diagrams work well in Markdown.

**API Contracts** — Wire formats, protocols, data models. What reviewers need to evaluate the interface.

**Alternatives** — What else was considered and why it was rejected. Shows you've thought it through.

**Security & Performance** — Auth model, data sensitivity, latency, scale expectations.

## What to include vs. exclude

Include: API schemas, message formats, data models, protocol choices.

Exclude: file names, directory structure, class names, function signatures, DB schemas, config formats.

## Good practices

- Be concise. Keep high signal-to-noise ratio. Avoid repeated information. One, good sentence is better than 10 verbose ones.
- Write for reviewers and future devs, not yourself
- One-page for quick review, link deep-dives
- Update or delete stale docs

## Common mistakes

- Skipping the "why" (jumping to solutions)
- No alternatives considered
- Implementation details (file structure, class names)
- Vague requirements
