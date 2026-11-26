#!/usr/bin/env python3
"""Run a command repeatedly and report a metric's distribution.

Use for on-device inference baselines: same command, warmup, many runs, report
percentiles instead of one number. Deterministic, no third-party deps.

Examples:
  python3 bench.py --cmd "./run_infer.sh" --runs 20 --warmup 3
  python3 bench.py --cmd "./run_infer.sh" --metric "ttft_ms=([0-9.]+)" --label ttft_ms
"""

from __future__ import annotations

import argparse
import re
import statistics
import subprocess
import time


def run_once(command: str, pattern: str | None, timeout: float) -> float:
    start = time.perf_counter()
    proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if proc.returncode != 0:
        raise SystemExit(
            f"command failed ({proc.returncode}): {command}\n{proc.stderr.strip()}"
        )
    if pattern is None:
        return elapsed_ms
    match = re.search(pattern, proc.stdout + proc.stderr)
    if match is None:
        raise SystemExit(
            f"metric pattern {pattern!r} not found in command output of: {command}"
        )
    return float(match.group(1))


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return float("nan")
    position = (len(sorted_values) - 1) * p
    low = int(position)
    high = min(low + 1, len(sorted_values) - 1)
    frac = position - low
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * frac


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cmd", required=True, help="shell command to benchmark")
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument(
        "--metric",
        default=None,
        help="regex with one capture group; default: measure wall time in ms",
    )
    parser.add_argument("--timeout", type=float, default=600.0, help="per-run timeout in seconds")
    parser.add_argument("--label", default="metric")
    args = parser.parse_args()

    for _ in range(args.warmup):
        run_once(args.cmd, args.metric, args.timeout)

    values = [run_once(args.cmd, args.metric, args.timeout) for _ in range(args.runs)]
    ordered = sorted(values)
    print(f"{args.label}: n={len(ordered)}")
    print(
        f"  min={ordered[0]:.3f} p50={percentile(ordered, 0.5):.3f} "
        f"p90={percentile(ordered, 0.9):.3f} p99={percentile(ordered, 0.99):.3f} "
        f"mean={statistics.fmean(ordered):.3f} std={statistics.pstdev(ordered):.3f}"
    )
    print(f"  all={[round(value, 3) for value in values]}")


if __name__ == "__main__":
    main()
