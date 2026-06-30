#!/usr/bin/env python3
"""Verify that fixed seeds regenerate hash-consistent synthetic traces.

Two independent checks are performed per case study:

  1. Determinism: generating the trace twice with the same seed yields an
     identical SHA-256 digest.
  2. Regression against committed canonical data: the freshly generated trace
     matches the versioned reference under ``data/synthetic_demo/<id>/packets.csv``
     (when present).

Exit code is non-zero if any check fails, so this script is suitable for CI.

Examples
--------
    python scripts/verify_reproducibility.py --all
    python scripts/verify_reproducibility.py --config configs/wifi_like.yaml
"""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import _bootstrap  # noqa: F401  (sets up sys.path)
from _bootstrap import CASE_CONFIGS, repo_root

from packet_observability.hash_utils import sha256_file
from packet_observability.io import load_config, write_packets_csv
from packet_observability.synthetic_generator import generate_packets


def _trace_digest(config_path: Path, tmp_dir: Path, tag: str) -> str:
    config = load_config(config_path)
    records = generate_packets(config)
    path = write_packets_csv(records, tmp_dir / f"{config.experiment_id}_{tag}.csv")
    return sha256_file(path)


def verify_one(config_path: Path, tmp_dir: Path) -> dict:
    config = load_config(config_path)
    exp_id = config.experiment_id

    digest_a = _trace_digest(config_path, tmp_dir, "a")
    digest_b = _trace_digest(config_path, tmp_dir, "b")
    deterministic = digest_a == digest_b

    canonical = repo_root() / "data" / "synthetic_demo" / exp_id / "packets.csv"
    if canonical.exists():
        canonical_digest = sha256_file(canonical)
        matches_reference = canonical_digest == digest_a
    else:
        canonical_digest = None
        matches_reference = None

    return {
        "experiment_id": exp_id,
        "sha256": digest_a,
        "deterministic": deterministic,
        "reference_present": canonical is not None and canonical.exists(),
        "matches_reference": matches_reference,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verify reproducibility of synthetic demo traces.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--config", help="Path to a single case-study YAML config.")
    g.add_argument("--all", action="store_true", help="Verify all four case studies.")
    args = p.parse_args(argv)

    configs_dir = repo_root() / "configs"
    if args.all:
        config_paths = [configs_dir / f"{name}.yaml" for name in CASE_CONFIGS]
    else:
        config_paths = [Path(args.config)]

    ok = True
    print(f"{'case':22} {'deterministic':14} {'matches reference':18} sha256[:16]")
    print("-" * 72)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for cp in config_paths:
            r = verify_one(cp, tmp_dir)
            det = "yes" if r["deterministic"] else "NO"
            if r["matches_reference"] is None:
                ref = "no reference"
            elif r["matches_reference"]:
                ref = "yes"
            else:
                ref = "NO"
                ok = False
            if not r["deterministic"]:
                ok = False
            print(f"{r['experiment_id']:22} {det:14} {ref:18} {r['sha256'][:16]}")

    print("-" * 72)
    if ok:
        print("[verify] PASS: all checked traces are deterministic and consistent.")
        return 0
    print("[verify] FAIL: at least one trace was non-deterministic or diverged from its reference.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
