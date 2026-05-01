---
name: agent-memory
description: Manage long-term memory across OpenCode sessions. Use when asked to remember something, when running /remember or /recall, or when you notice the user correcting you on something you should retain.
---

# Agent Memory

You have a persistent memory system that survives across sessions. Memory is stored in plain markdown files that you read at session start and update when asked.

## Memory Locations

There are two tiers of memory:

1. **Global memory**: `~/.config/opencode/memory/MEMORY.md` -- preferences, habits, and knowledge that apply across all projects.
1. **Project memory**: `.opencode/memory/MEMORY.md` (relative to project root) -- project-specific knowledge like build commands, architecture decisions, debugging insights, and conventions.

If a project memory file or directory doesn't exist yet, create it when first needed.

## What to Save

Save information that would be useful in a future session:

- Build, test, lint commands and their quirks
- Debugging insights (e.g., "service X requires Y env var to run locally")
- Architecture decisions and their rationale
- User corrections (e.g., "always use pnpm, not npm")
- Code style preferences the user has expressed
- Project-specific conventions not captured in AGENTS.md
- Common pitfalls and how to avoid them
- Tool/dependency version constraints

## What NOT to Save

- Conversation-specific context (temporary debugging steps, one-off questions)
- Information already in AGENTS.md, README, or other committed docs
- Sensitive data (API keys, passwords, tokens)
- Opinions or speculation -- only save facts and observed preferences

## Memory File Format

Keep memory files concise. Target under 150 lines to leave headroom under the 200-line practical limit.

Structure:

```markdown
# Memory

## Quick Reference
<!-- Most frequently needed facts: build commands, key preferences -->

## Architecture & Conventions
<!-- Project structure insights, naming conventions, patterns -->

## Debugging & Gotchas
<!-- Known issues, workarounds, environment setup notes -->

## Preferences
<!-- User's coding style preferences, tool choices, workflow habits -->
```

## Writing Memory

When updating memory:

1. Read the existing memory file first.
1. Merge new information with existing content. Don't duplicate.
1. If a fact has changed, update it in place rather than appending.
1. If the file is approaching 150 lines, consolidate: remove stale entries, merge related items, and tighten wording.
1. Write the updated file.
1. Report what you saved and where.

## Reading Memory

When reading memory at session start:

1. Read both global and project memory files (if they exist).
1. Don't announce the contents unprompted -- just use the knowledge naturally.
1. If a memory entry conflicts with AGENTS.md or explicit user instructions, the user's instructions win.

## When to Suggest Remembering

If the user corrects you on something that would apply to future sessions, suggest: "Want me to remember this for next time? You can run `/remember`."

Don't be pushy about it. Once per session is enough.
