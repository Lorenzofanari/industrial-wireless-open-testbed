#!/usr/bin/env python3
"""Generate figures from a canonical packets.csv.

Thin command-line entry point around ``packet_observability.plotting``.

Example
-------
    python scripts/plot_results.py --input results/demo/wifi_like/packets.csv \
        --out-dir results/demo/wifi_like/figures
"""
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401  (sets up sys.path)

from packet_observability.plotting import plot_from_csv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate figures from a packets.csv.")
    p.add_argument("--input", required=True, help="Path to packets.csv.")
    p.add_argument("--out-dir", default=None, help="Figure output directory.")
    args = p.parse_args(argv)

    produced = plot_from_csv(args.input, args.out_dir)
    for fig in produced:
        print(f"[plot] wrote {fig}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
