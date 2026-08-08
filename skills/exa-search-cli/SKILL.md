---
name: exa-search-cli
description: "CLI tool for Exa Search using a Python script with uv inline dependencies for semantic web retrieval"
---
# Exa Search CLI

This skill provides a CLI tool for Exa Search using a Python script with uv inline dependencies. It's self-contained and requires no separate installation.

## Quick Start

The script is located at `/home/alex/.config/opencode/skills/exa-search-cli/exa-search` and can be run directly. It's self-contained: uv auto-installs any dependencies on first run, and the script itself validates required environment variables and prerequisites, reporting clear errors when anything is missing.

### Basic Search

```bash
exa-search "kubernetes architecture" --type auto --num-results 5
```

### With Highlights

```bash
exa-search "kubernetes components" --contents-highlights
```

### With Filters

```bash
exa-search "AI regulation policy updates" --category news --start-date "2025-01-01"
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
# Basic search
exa-search "kubernetes components" --type auto --num-results 3

# Search with highlights
exa-search "kubernetes nodes" --contents-highlights

# Search with date range
exa-search "kubernetes architecture" --start-date "2025-01-01" --end-date "2025-12-31"

# Deep search with text extraction
exa-search "compare sodium-ion batteries" --type deep --contents-text
```

## Implementation

The tool is a self-contained Python script using `uv` inline dependencies (requests, click). The shebang `#!/usr/bin/env -S uv run --script` makes it directly executable with automatic dependency management.
