#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""SearXNG search tool for AI agents.

Usage as a CLI:
    searxng_search.py "your query"
    uv run searxng_search.py "your query"

Usage as a module:
    from searxng_search import searx_search

    results = searx_search("what is Kubernetes?")
    for r in results:
        print(r.title, r.url, r.content)

Usage as a tool (return JSON for agent consumption):
    searxng_search.py "your query" --json

Set custom SearXNG URL:
    SEARXNG_BASE_URL="example.com" searxng_search.py "your query"
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from typing import Literal

__all__ = ["searx_search", "SearchResult", "SearXNGError"]

SafeSearch = Literal["off", "moderate", "strict"]

REQUEST_TIMEOUT = 15
DEFAULT_SEARXNG_BASE_URL = "http://sumac0:32031"
DEFAULT_MAX_RESULTS = 10


class SearXNGError(Exception):
    """Failed to reach or parse SearXNG."""


@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    engine: str | None = None
    score: float | None = None
    category: str | None = None
    published_date: str | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


def _build_params(
    query: str,
    *,
    categories: str | None = None,
    language: str | None = None,
    time_range: str | None = None,
    pageno: int = 1,
    safesearch: SafeSearch = "off",
    engines: str | None = None,
) -> str:
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "language": language,
        "pageno": str(pageno),
        "safesearch": _safesearch_value(safesearch),
    })

    if categories is not None:
        params += urllib.parse.urlencode({"categories": categories})
    if time_range is not None:
        params += urllib.parse.urlencode({"time_range": time_range})
    if engines is not None:
        params += urllib.parse.urlencode({"engines": engines})

    return params


def _safesearch_value(safesearch: SafeSearch) -> str:
    return {"off": "0", "moderate": "1", "strict": "2"}[safesearch]


def _read_base_url() -> str:
    return os.environ.get("SEARXNG_BASE_URL", DEFAULT_SEARXNG_BASE_URL)


def searx_search(
    query: str,
    *,
    categories: str | None = None,
    language: str | None = "en",
    time_range: str | None = None,
    pageno: int = 1,
    safesearch: SafeSearch = "off",
    engines: str | None = None,
    max_results: int | None = None,
    timeout: int = REQUEST_TIMEOUT,
) -> list[SearchResult]:
    """Search SearXNG and return structured results."""
    params = _build_params(
        query,
        categories=categories,
        language=language,
        time_range=time_range,
        pageno=pageno,
        safesearch=safesearch,
        engines=engines,
    )

    data = params.encode("utf-8")
    base_url = _read_base_url()
    req = urllib.request.Request(
        f"{base_url}/search",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise SearXNGError(
            f"Could not reach SearXNG at {base_url}: {exc.reason}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise SearXNGError("SearXNG returned invalid JSON") from exc

    unresponsive: list[str] = []
    for eng in body.get("unresponsive_engines", []):
        reason = eng[1] if len(eng) > 1 else "unknown"
        unresponsive.append(f"{eng[0]}: {reason}")

    if unresponsive:
        # I don't wanna pollute LLM context windows with a warning like this. It's useless most of the time.
        pass
        # print(
        #     f"\n⚠  Unresponsive engines: {', '.join(unresponsive)}",
        #     file=sys.stderr,
        # )

    results: list[SearchResult] = [
        SearchResult(
            title=r.get("title"),
            url=r.get("url"),
            content=r.get("content"),
            engine=r.get("engine"),
            score=r.get("score"),
            category=r.get("category"),
            published_date=r.get("publishedDate") or r.get("pubdate"),
        )
        for r in body.get("results", [])
    ]

    if max_results is not None:
        results = results[:max_results]

    return results


def print_results(
    results: list[SearchResult],
    *,
    json_output: bool = False,
) -> None:
    if json_output:
        print(json.dumps([r.to_dict() for r in results], indent=2))
        return

    if not results:
        print("No results found.", file=sys.stderr)
        return

    for i, r in enumerate(results, 1):
        print(f"  {i}. {r.title}")
        print(f"     {r.url}")
        if r.engine is not None:
            print(f"     engine: {r.engine}")
        if r.score is not None and r.score != 1.0:
            print(f"     score: {r.score:.4f}")
        if r.content:
            snippet = r.content[:300]
            if len(r.content) > 300:
                snippet += "…"
            print(f"     {snippet}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search SearXNG from the command line or as a module."
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Output results as JSON (for agent consumption)",
    )
    parser.add_argument(
        "--categories",
        default=None,
        help="Filter by category (e.g. 'it', 'news', 'science')",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language code (default: en)",
    )
    parser.add_argument(
        "--time-range",
        default=None,
        choices=["day", "week", "month", "year"],
        help="Filter by recency",
    )
    parser.add_argument(
        "--engines",
        default=None,
        help="Override engines (e.g. 'google,duckduckgo')",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Maximum number of results (default: {DEFAULT_MAX_RESULTS})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=REQUEST_TIMEOUT,
        help=f"Request timeout in seconds (default: {REQUEST_TIMEOUT})",
    )
    parser.add_argument(
        "--safesearch",
        default="off",
        choices=["off", "moderate", "strict"],
        help="Safe search: off, moderate, strict (default: off)",
    )

    args = parser.parse_args()

    try:
        results = searx_search(
            args.query,
            categories=args.categories,
            language=args.language,
            time_range=args.time_range,
            engines=args.engines,
            max_results=args.max_results,
            timeout=args.timeout,
            safesearch=args.safesearch,
        )
    except SearXNGError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print_results(results, json_output=args.json_output)


if __name__ == "__main__":
    main()
