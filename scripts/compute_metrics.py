#!/usr/bin/env python3
"""Compute packet-level observability metrics from a canonical packets.csv.

Thin command-line entry point around ``packet_observability.metrics``.

Example
-------
    python scripts/compute_metrics.py --input results/demo/wifi_like/packets.csv
"""
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401  (sets up sys.path)

from packet_observability.metrics import compute_from_csv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compute observability metrics from packets.csv.")
    p.add_argument("--input", required=True, help="Path to packets.csv.")
    p.add_argument("--out-dir", default=None, help="Output directory (default: alongside input).")
    args = p.parse_args(argv)

    paths = compute_from_csv(args.input, args.out_dir)
    print(f"[metrics] wrote {paths['metrics_csv']}")
    print(f"[metrics] wrote {paths['summary_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
