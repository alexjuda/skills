---
name: walkthrough
description: Present ideas, designs, or research findings in small chunks, one at a time, waiting for user confirmation before advancing. Use whenever the user asks to brainstorm, walk through a concept, or you're about to dump a large amount of information.
---

## What I do

I chunk complex ideas into bite-sized sections and present them one at a time. The user reads, asks questions, gives feedback, and says "continue" (or equivalent) before I move on. No walls of text. The user controls the pace.

## How I work

1. **Chunk internally first.** Before speaking, organize the full concept into logical sections (architecture, data flow, tradeoffs, edge cases, etc.). Keep each section self-contained and bounded — think 200–300 words or a few clear bullet points.

2. **Announce the scope.** Tell the user how many sections there are and what they'll cover. Ask if they want to proceed.

3. **Present one section. Then stop.** Deliver just that section. Keep each section self-contained — no teasing what's coming next. End with a short check-in so the user can pause, ask questions, or give feedback.

4. **Wait for the continuer.** The user might say "continue," "go on," "next," "move on," "this is good, go ahead," or ask a question first. Handle their feedback or question *in full* before proceeding. If they ask a question, answer it completely, then ask if they're ready to continue.

5. **Repeat until done.** After the last section, confirm the user has nothing else to add.

## Why this matters

Chunking prevents cognitive overload. When an agent dumps a large amount of information at once, the user can't meaningfully evaluate, question, or redirect — they just absorb or skim. By revealing one section at a time, the user stays engaged, can course-correct early, and the conversation stays collaborative instead of becoming a one-way broadcast. This is especially important for complex or high-stakes topics where early feedback prevents wasted effort.

## What to chunk

Every brainstorming, design, or research output should be chunked. Typical sections:

| Output type | Typical sections |
|-------------|-----------------|
| Architecture | Overview → Components → Data flow → Error handling → Deployment |
| Research summary | Context → Key findings → Implications → Recommendations |
| Design proposal | Problem → Approach → Tradeoffs → Open questions |
| Feature spec | User story → Flow → Edge cases → Acceptance criteria |

Be flexible — adapt the sections to the topic, don't force a template.

## What not to do

- **No multi-section dumps.** Even if the user didn't explicitly ask for walkthrough mode, if the output is complex enough that it'd be a wall of text, chunk it. When in doubt, ask: "Should I walk through this, or do you want it all at once?"
- **No teasing the next section.** Don't say "next I'll cover X" in the current section's message. Keep each section self-contained.
- **Don't rush through questions.** If the user asks a question, answer it fully before asking to continue. Their question *is* the continuer for the current section.
- **No skipping ahead.** The user can skip ("skip to error handling") or jump back ("go back to the data flow part"). Honor both.
