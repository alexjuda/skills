---
name: exa-search-cli
description: "Use whenever the user or agent needs to search online, research web sources, find current information, or retrieve documentation. Provides an Exa Search CLI for semantic web retrieval."
---
# Exa Search CLI

This skill provides a CLI tool for Exa Search using a Python script with uv inline dependencies. It's self-contained and requires no separate installation.

## Quick Start

The script is located at `./exa-search` in the same directory as this SKILL.md file and can be run directly. It's self-contained: uv auto-installs any dependencies on first run, and the script itself validates required environment variables and prerequisites, reporting clear errors when anything is missing. The script uses a shebang (`#!/usr/bin/env -S uv run --script`) making it directly executable.

**Location**: The script and SKILL.md file are in the same directory, so `./exa-search` will work when run from this directory.

### Basic Search

```bash
cd <skill-dir>
./exa-search "kubernetes architecture" --type auto --num-results 5
```

### With Highlights

```bash
cd <skill-dir>
./exa-search "kubernetes components" --contents-highlights
```

### With Filters

```bash
cd <skill-dir>
./exa-search "AI regulation policy updates" --category news --start-date "2025-01-01"
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `query` | Search query (required positional argument) |
| `--type` | Search method: auto, fast, instant, deep-lite, deep, deep-reasoning |
| `--num-results` | Number of results to return (default: 10) |
| `--category` | Specialized result type: company, people, research paper, news, personal site, financial report |
| `--include-domains` | Comma-separated domains to include |
| `--exclude-domains` | Comma-separated domains to exclude |
| `--start-date` | Start date for publication filtering (ISO 8601) |
| `--end-date` | End date for publication filtering (ISO 8601) |
| `--contents-highlights` | Include highlights in results (flag) |
| `--contents-text` | Include full text in results (flag) |
| `--contents-summary` | Include summaries in results (flag) |

## Examples

```bash

cd <skill-dir>

# Basic search
./exa-search "kubernetes components" --type auto --num-results 3

# Search with highlights
./exa-search "kubernetes nodes" --contents-highlights

# Search with date range
./exa-search "kubernetes architecture" --start-date "2025-01-01" --end-date "2025-12-31"

# Deep search with text extraction
./exa-search "compare sodium-ion batteries" --type deep --contents-text
```

## Usage Guidelines

This skill should be used whenever the agent or the user needs to search for information online. Use it for:

- General web searches for knowledge and facts
- Researching topics, concepts, or technical documentation
- Finding current information, news, or recent updates
- Searching for examples, tutorials, or guides
- Finding official documentation or authoritative sources
- Any situation where web search would help answer questions

**Not appropriate for:** Personal/proprietary data, internal company information, or sensitive queries that shouldn't be publicly accessible.

## Implementation

The tool is a self-contained Python script using `uv` inline dependencies (requests, click). The shebang `#!/usr/bin/env -S uv run --script` makes it directly executable with automatic dependency management.
