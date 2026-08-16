---
name: searxng-search
description: "Use whenever the user or agent needs to search online, research web sources, find current information, or retrieve documentation."
---

# SearXNG Search

Use this skill whenever you need to search the web for information, facts, current events, documentation, or any other topic. Provides a self-contained SearXNG CLI tool with uv inline dependencies.

## Quick Start

The search script lives in the same directory as this SKILL.md. Change into that directory, then run the script.

```bash
cd <path-to-skill-dir>
./searxng_search.py "your search query"
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `query` | Search query (required positional argument) |
| `--json` | Output as structured JSON instead of human-readable text |
| `--max-results` | Number of results to return (default: 10) |

## Examples

```bash
cd <path-to-skill-dir>

# Basic search
./searxng_search.py "kubernetes networking basics"

# Limit results
./searxng_search.py "python asyncio patterns" --max-results 3

# JSON output for analysis
./searxng_search.py "Kubernetes vs Docker Swarm" --json --max-results 5 2>/dev/null
```

## Usage Guidelines

Use this for:

- Answering questions that require up-to-date or verified information
- Researching topics before providing detailed answers
- Finding documentation, tutorials, or authoritative sources
- Checking current events, news, or recent updates
- Verifying facts or finding specific data
- Any situation where "let me search for that" would be appropriate

**Not appropriate for:** Personal/proprietary data, internal company information, or sensitive queries that shouldn't go through a public search endpoint.

## Notes

- Powered by your self-hosted SearXNG instance
- Unresponsive engines are silently filtered — you only get working results
