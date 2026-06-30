#!/usr/bin/env python3
"""Generate a synthetic demo-mode packet trace from a case-study config.

This is a thin command-line entry point; the logic lives in
``packet_observability.synthetic_generator`` and ``packet_observability.io``.

Example
-------
    python scripts/generate_traces.py --config configs/wifi_like.yaml \
        --out results/demo/wifi_like/packets.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401  (sets up sys.path)

from packet_observability.io import load_config, write_packets_csv
from packet_observability.synthetic_generator import generate_packets


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a synthetic demo-mode packet trace.")
    p.add_argument("--config", required=True, help="Path to a case-study YAML config.")
    p.add_argument("--out", required=True, help="Output packets.csv path.")
    p.add_argument("--seed", type=int, default=None, help="Override the config random seed.")
    p.add_argument("--packet-size", type=int, default=None, help="Override packet size (bytes).")
    p.add_argument("--interval-ms", type=int, default=None, help="Override packet interval (ms).")
    p.add_argument(
        "--drop-probability",
        type=float,
        default=None,
        help="Synthetic missing-sample fraction [0,1). Defaults to the config value.",
    )
    args = p.parse_args(argv)

    if args.drop_probability is not None and not (0.0 <= args.drop_probability < 1.0):
        raise SystemExit("--drop-probability must be in [0, 1).")

    config = load_config(args.config)
    records = generate_packets(
        config,
        packet_size=args.packet_size,
        interval_ms=args.interval_ms,
        seed=args.seed,
        drop_probability=args.drop_probability,
    )
    out_path = write_packets_csv(records, Path(args.out))
    print(f"[generate] {config.experiment_id}: wrote {len(records)} synthetic packets -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
