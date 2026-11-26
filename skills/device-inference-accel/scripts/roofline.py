#!/usr/bin/env python3
"""Compute a roofline bound for one kernel or model pass.

Given FLOPs, bytes moved, achievable peak throughput, and memory bandwidth,
report whether the work is compute- or memory-bound and the theoretical
minimum time. This is a bound, not a measurement; compare it with bench.py.

Example:
  python3 roofline.py --flops 2e12 --bytes 8e9 --peak-tflops 40 --bw-gbps 50
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--flops", type=float, required=True, help="FLOPs for the pass")
    parser.add_argument(
        "--bytes", type=float, required=True, help="bytes moved (weights + activations + KV)"
    )
    parser.add_argument(
        "--peak-tflops", type=float, required=True, help="achievable compute peak in TFLOP/s"
    )
    parser.add_argument(
        "--bw-gbps", type=float, required=True, help="achievable memory bandwidth in GB/s"
    )
    args = parser.parse_args()

    peak = args.peak_tflops * 1e12
    bandwidth = args.bw_gbps * 1e9
    compute_time = args.flops / peak
    memory_time = args.bytes / bandwidth if bandwidth else float("inf")
    intensity = args.flops / args.bytes if args.bytes else float("inf")
    ridge = peak / bandwidth if bandwidth else float("inf")
    bound = "compute" if intensity >= ridge else "memory"

    print(f"operational intensity = {intensity:.2f} FLOP/byte")
    print(f"machine ridge         = {ridge:.2f} FLOP/byte")
    print(f"bound                 = {bound}")
    print(
        f"min time: compute {compute_time * 1e3:.3f} ms, "
        f"memory {memory_time * 1e3:.3f} ms "
        f"-> {max(compute_time, memory_time) * 1e3:.3f} ms ({bound}-bound)"
    )
    print("theoretical floor; compare with measured latency and explain the gap")


if __name__ == "__main__":
    main()
