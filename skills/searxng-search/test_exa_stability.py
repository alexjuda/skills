#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Test Exa engine stability on your SearXNG instance.

Run repeatedly to catch intermittent Exa API timeouts.
Usage: uv run test_exa_stability.py [--iterations N] [--query "q"]

Example:
    uv run test_exa_stability.py --iterations 50 --query "LLM agents"
"""

import argparse
import json
import subprocess
import time

def main():
    parser = argparse.ArgumentParser(description="Test Exa engine stability")
    parser.add_argument("--iterations", type=int, default=20, help="Number of iterations to run (default: 20)")
    parser.add_argument("--query", default="kubernetes")
    args = parser.parse_args()

    # Use a base pool of queries so each iteration is unique,
    # avoiding cached responses that mask cold-start latency.
    base_queries = [
        "kubernetes",
        "python web frameworks",
        "LLM agent patterns",
        "rust async runtime",
        "go concurrency model",
        "webassembly use cases",
        "database indexing strategies",
        "serverless cold start",
        "microservices anti patterns",
        "graphene crystal structure",
    ]

    ok = 0
    fail = 0
    times = []

    queries = [f"{q} #{i}" for i, q in enumerate(base_queries, 1)]
    # If we need more iterations than base queries, cycle with suffixes
    while len(queries) < args.iterations:
        extra = len(queries) + 1
        queries.append(f"{base_queries[(extra - 1) % len(base_queries)]} #{extra}")

    print(f"=== Exa API Stability Test ===")
    print(f"Iterations: {args.iterations} | Unique queries (no cache warmup)")
    print("---")

    for i in range(1, args.iterations + 1):
        query = queries[i - 1]
        start = time.time()
        r = subprocess.run(
            ["./searxng_search.py", query, "--max-results", "3", "--json"],
            capture_output=True, text=True,
        )
        elapsed_ms = int((time.time() - start) * 1000)
        times.append(elapsed_ms)

        try:
            parsed = json.loads(r.stdout)
        except json.JSONDecodeError:
            parsed = {}

        results = parsed if isinstance(parsed, list) else parsed.get("results", [])
        exa_count = sum(1 for item in results if isinstance(item, dict) and item.get("engine") == "exaapi")
        has_exa = exa_count > 0

        if has_exa:
            ok += 1
            status = "OK"
        else:
            fail += 1
            status = "FAIL"

        print(
            f"  {i:3d}/{args.iterations} | {elapsed_ms:5d} ms | {status} (exa={exa_count})"
        )

    print("---")
    print(f"Summary:")
    print(f"  OK:        {ok}/{args.iterations} ({ok * 100 // args.iterations}%)")
    print(f"  FAIL:      {fail}/{args.iterations} ({fail * 100 // args.iterations}%)")
    if times:
        print(f"  Avg time:  {sum(times) // len(times)} ms")
        print(f"  Slowest:   {max(times)} ms")
        p95 = sorted(times)[int(len(times) * 0.95)]
        print(f"  P95 time:  {p95} ms")
    if fail > 0:
        print(f"  ⚠ Exa engine failed {fail}/{args.iterations} times")
        print("  → Check SearXNG config: 'exaapi' may be suspended or the API key may be expired.")


if __name__ == "__main__":
    main()
