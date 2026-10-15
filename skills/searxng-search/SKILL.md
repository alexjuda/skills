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
| `--max-results N` | Maximum number of results (default: 10) |
| `--categories CAT` | Filter by category (e.g. `'it'`, `'news'`, `'science'`) |
| `--language LANG` | Language code (default: `'en'`) |
| `--time-range RANGE` | Filter by recency: `'day'`, `'week'`, `'month'`, `'year'` |
| `--engines ENGINES` | Override engines (e.g. `'google,duckduckgo'`) |
| `--timeout SECS` | Request timeout in seconds (default: 15) |
| `--safesearch LEVEL` | Safe search level: `'off'`, `'moderate'`, `'strict'` (default: `'off'`) |

Use `--json` for structured output when you need to parse results programmatically (ideally, with `jq`). Use `--max-results 10` as a starting point, reduce for focused queries.

## Examples

```bash
cd <path-to-skill-dir>

# Basic search
./searxng_search.py "kubernetes networking basics"

# Limit results
./searxng_search.py "python asyncio patterns" --max-results 3

# JSON output — note: results are wrapped in a "results" key, so use .results[]
./searxng_search.py "Kubernetes vs Docker Swarm" --max-results 5 --json | jq '.results[] | {title, url, content: .content[:500]}'

# Search recent news (last week)
./searxng_search.py "AI regulation" --time-range week --max-results 5 --json

# Search with specific engines
./searxng_search.py "Rust async best practices" --engines "google,bing" --max-results 5 --json

# Search in a specific category
./searxng_search.py "climate change solutions" --categories science --max-results 5 --json
```

## JSON Output Structure

When using `--json`, the output is:

```json
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "content": "...",
      "engine": "...",
      "score": 0.5,
      "category": "general",
      "published_date": "..."
    }
  ],
  "unresponsive_engines": ["engine1: reason", ...]
}
```

Use `.results[]` in `jq` to iterate results. `unresponsive_engines` is optional and only present if some search engines failed.

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

- Powered by your self-hosted SearXNG instance (default: `http://sumac0:32031`)
- Override the instance URL via `SEARXNG_BASE_URL` environment variable
