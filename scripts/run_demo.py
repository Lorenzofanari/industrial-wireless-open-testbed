#!/usr/bin/env python3
"""Run the unified synthetic demo-mode workflow: generate -> metrics -> figures.

For each selected case-study config this script:
  1. generates a deterministic synthetic packets.csv,
  2. computes packet-level observability metrics,
  3. produces the standard figure set,
  4. writes a per-run reproducibility manifest (config, seed, git commit, hashes),
  5. aggregates the canonical artefacts under results/{metrics,figures,manifests}/.

Everything runs software-only: no radio emission and no network interface is
touched.

Examples
--------
    python scripts/run_demo.py --config configs/wifi_like.yaml --out results/demo/wifi_like
    python scripts/run_demo.py --all
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import _bootstrap  # noqa: F401  (sets up sys.path)
from _bootstrap import CASE_CONFIGS, repo_root

from packet_observability.io import load_config, write_packets_csv
from packet_observability.manifest import build_manifest, write_manifest
from packet_observability.metrics import compute_from_csv
from packet_observability.plotting import plot_from_csv
from packet_observability.synthetic_generator import generate_packets


def run_one(config_path: str | Path, out_dir: str | Path, *, seed: int | None = None,
            aggregate: bool = True) -> Path:
    """Run the full demo workflow for a single config into ``out_dir``."""
    config_path = Path(config_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(config_path)
    print(f"\n=== {config.experiment_id} ({config.technology}, {config.safety_mode}) ===")

    records = generate_packets(config, seed=seed)
    packets_csv = write_packets_csv(records, out_dir / "packets.csv")
    print(f"[generate] {len(records)} synthetic packets -> {packets_csv}")

    metric_paths = compute_from_csv(packets_csv, out_dir)
    print(f"[metrics]  -> {metric_paths['summary_json']}")

    figures = plot_from_csv(packets_csv, out_dir / "figures")
    print(f"[plot]     {len(figures)} figures -> {out_dir / 'figures'}")

    output_files = [packets_csv, metric_paths["metrics_csv"], metric_paths["summary_json"],
                    metric_paths["inter_arrival_csv"], *figures]
    manifest = build_manifest(
        experiment_id=config.experiment_id,
        config=config.raw,
        config_path=config_path,
        seed=seed if seed is not None else config.random_seed,
        mode="synthetic_demo",
        output_files=output_files,
        extra={"n_records": len(records), "n_figures": len(figures)},
    )
    manifest_path = write_manifest(manifest, out_dir / "manifest.json")
    print(f"[manifest] -> {manifest_path}")

    if aggregate:
        _aggregate(config.experiment_id, metric_paths["summary_json"], figures, manifest_path)
    return packets_csv


def _aggregate(exp_id: str, summary_json: Path, figures: list[Path], manifest_path: Path) -> None:
    """Copy canonical artefacts into results/{metrics,figures,manifests}/."""
    results = repo_root() / "results"
    (results / "metrics").mkdir(parents=True, exist_ok=True)
    (results / "manifests").mkdir(parents=True, exist_ok=True)
    fig_dir = results / "figures" / exp_id
    fig_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(summary_json, results / "metrics" / f"{exp_id}.json")
    shutil.copy2(manifest_path, results / "manifests" / f"{exp_id}.json")
    for fig in figures:
        shutil.copy2(fig, fig_dir / fig.name)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run the synthetic demo-mode workflow.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--config", help="Path to a single case-study YAML config.")
    g.add_argument("--all", action="store_true", help="Run all four case studies.")
    p.add_argument("--out", default=None, help="Output directory (single-config mode).")
    p.add_argument("--seed", type=int, default=None, help="Override the config random seed.")
    args = p.parse_args(argv)

    configs_dir = repo_root() / "configs"

    if args.all:
        for name in CASE_CONFIGS:
            run_one(configs_dir / f"{name}.yaml", repo_root() / "results" / "demo" / name, seed=args.seed)
        print("\n[done] All case studies complete. See results/demo/ and results/{metrics,figures,manifests}/.")
        return 0

    config_path = Path(args.config)
    exp_id = load_config(config_path).experiment_id
    out_dir = Path(args.out) if args.out else repo_root() / "results" / "demo" / exp_id
    run_one(config_path, out_dir, seed=args.seed)
    print(f"\n[done] {exp_id} complete. See {out_dir}/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
