"""Build publication report data: metrics, repeatability, performance, determinism.

Aggregates existing per-case outputs under results/ and measures:
  * runtime of the generate -> metrics -> plot pipeline (representative timing),
  * storage footprint of generated logs/figures,
  * determinism (same seed -> identical SHA-256 of packets.csv).

Outputs:
  * paper_assets/report_data.json         (machine-readable)
  * paper_assets/tables/auto_tables.md    (rendered Markdown tables)

SAFETY NOTE: offline aggregation/measurement only; no network or radio access.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from src.analysis import compute_metrics, make_plots
from src.capture import synthetic_capture_generator as gen
from src.utils.config_loader import load_config

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CONFIGS = ROOT / "configs"
PAPER = ROOT / "paper_assets"

CASES = [
    ("case_wifi_latency", "Wi-Fi-like"),
    ("case_ble_telemetry", "BLE-like"),
    ("case_802154_sensing", "802.15.4-like"),
    ("case_lora_sdr_observability", "LoRa/SDR-like"),
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _dir_size_bytes(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def measure_runtime(config_path: Path) -> dict:
    """Time generate -> metrics -> plots for a single run (representative)."""
    cfg = load_config(config_path)
    t0 = time.perf_counter()
    csv_path = gen.run(config_path, run_label="_bench", seed=777, drop_probability=0.01)
    t1 = time.perf_counter()
    compute_metrics.run(csv_path)
    t2 = time.perf_counter()
    make_plots.run(csv_path, out_dir=csv_path.parent / "figures")
    t3 = time.perf_counter()
    n_packets = sum(1 for _ in csv_path.open()) - 1
    bench_dir = csv_path.parent
    return {
        "n_packets": n_packets,
        "generate_s": round(t1 - t0, 4),
        "metrics_s": round(t2 - t1, 4),
        "plots_s": round(t3 - t2, 4),
        "total_s": round(t3 - t0, 4),
        "_bench_dir": str(bench_dir),
    }


def check_determinism(config_path: Path) -> dict:
    """Generate twice with the same seed; confirm identical packets.csv hash."""
    a = gen.run(config_path, run_label="_det_a", seed=4242, drop_probability=0.0)
    b = gen.run(config_path, run_label="_det_b", seed=4242, drop_probability=0.0)
    ha, hb = _sha256(a), _sha256(b)
    # cleanup determinism scratch dirs
    for p in (a.parent, b.parent):
        for f in p.rglob("*"):
            if f.is_file():
                f.unlink()
        p.rmdir()
    return {"seed": 4242, "sha256": ha, "match": ha == hb}


def main() -> int:
    report: dict = {"cases": {}, "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    for exp_id, label in CASES:
        exp_dir = RESULTS / exp_id
        run01 = load_json(exp_dir / "run01" / "metrics_summary.json")
        rep = load_json(exp_dir / "repeatability_summary.json")
        cfg = load_config(CONFIGS / f"{exp_id}.yaml")

        runtime = measure_runtime(CONFIGS / f"{exp_id}.yaml")
        determinism = check_determinism(CONFIGS / f"{exp_id}.yaml")

        # storage: size of the per-case results dir (excludes scratch bench/det dirs after cleanup)
        bench_dir = Path(runtime.pop("_bench_dir"))
        # remove the bench scratch dir from storage accounting
        if bench_dir.exists():
            for f in bench_dir.rglob("*"):
                if f.is_file():
                    f.unlink()
            for d in sorted(bench_dir.rglob("*"), reverse=True):
                if d.is_dir():
                    d.rmdir()
            bench_dir.rmdir()

        storage_bytes = _dir_size_bytes(exp_dir)
        # representative single-run CSV size
        run01_csv = exp_dir / "run01" / "packets.csv"
        run01_csv_kb = round(run01_csv.stat().st_size / 1024, 1)

        report["cases"][exp_id] = {
            "label": label,
            "technology": cfg.technology,
            "safety_mode": cfg.safety_mode,
            "n_nodes": cfg.number_of_nodes,
            "packet_size_bytes": cfg.packet_size_bytes,
            "packet_interval_ms": cfg.packet_interval_ms,
            "duration_s": cfg.experiment_duration_s,
            "repetitions": cfg.repetitions,
            "seed": cfg.random_seed,
            "run01_metrics": run01,
            "repeatability": rep,
            "runtime": runtime,
            "determinism": determinism,
            "storage_bytes": storage_bytes,
            "run01_csv_kb": run01_csv_kb,
        }

    out_json = PAPER / "report_data.json"
    with out_json.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"[report] wrote {out_json}")

    render_tables(report)
    return 0


def render_tables(report: dict) -> None:
    lines: list[str] = []
    lines.append("<!-- AUTO-GENERATED by scripts/build_report.py. Do not edit by hand. -->")
    lines.append(f"<!-- generated: {report['generated_utc']} -->\n")

    # Table: per-case demo metrics (run01)
    lines.append("## Auto Table A1 - Per-case demonstration metrics (run01, synthetic)\n")
    lines.append("| Case | Tech-like | Packets | Rate (pps) | Mean size (B) | IA mean (ms) | Jitter proxy (ms) | Missing seq | Completeness |")
    lines.append("|------|-----------|---------|------------|---------------|--------------|-------------------|-------------|--------------|")
    for exp_id, c in report["cases"].items():
        m = c["run01_metrics"]
        lines.append(
            f"| {exp_id} | {c['label']} | {m['total_packets']} | {m['packet_rate_pps']} | "
            f"{m['mean_packet_size_bytes']} | {m['inter_arrival_mean_ms']} | {m['jitter_proxy_ms']} | "
            f"{m['missing_sequence_ids']} | {m['capture_completeness']} |"
        )
    lines.append("")

    # Table: repeatability (packet_rate_pps + completeness)
    lines.append("## Auto Table A2 - Repeatability across runs (mean +/- std)\n")
    lines.append("| Case | Runs | Rate mean (pps) | Rate std | Completeness mean | Completeness std | Jitter proxy mean (ms) | Jitter proxy std |")
    lines.append("|------|------|-----------------|----------|-------------------|------------------|------------------------|------------------|")
    for exp_id, c in report["cases"].items():
        rm = c["repeatability"]["metrics"]
        rate = rm.get("packet_rate_pps", {})
        comp = rm.get("capture_completeness", {})
        jit = rm.get("jitter_proxy_ms", {})
        lines.append(
            f"| {exp_id} | {c['repeatability']['n_runs']} | {rate.get('mean')} | {rate.get('std')} | "
            f"{comp.get('mean')} | {comp.get('std')} | {jit.get('mean')} | {jit.get('std')} |"
        )
    lines.append("")

    # Table: performance (runtime + storage)
    lines.append("## Auto Table A3 - Usability: runtime and storage (single run)\n")
    lines.append("| Case | Packets | Generate (s) | Metrics (s) | Plots (s) | Total (s) | run01 CSV (KB) | Case dir (KB) |")
    lines.append("|------|---------|--------------|-------------|-----------|-----------|----------------|---------------|")
    for exp_id, c in report["cases"].items():
        r = c["runtime"]
        lines.append(
            f"| {exp_id} | {r['n_packets']} | {r['generate_s']} | {r['metrics_s']} | {r['plots_s']} | "
            f"{r['total_s']} | {c['run01_csv_kb']} | {round(c['storage_bytes']/1024,1)} |"
        )
    lines.append("")

    # Table: determinism
    lines.append("## Auto Table A4 - Determinism (same seed -> identical packets.csv)\n")
    lines.append("| Case | Seed | SHA-256 (packets.csv, first 16) | Match |")
    lines.append("|------|------|---------------------------------|-------|")
    for exp_id, c in report["cases"].items():
        d = c["determinism"]
        lines.append(f"| {exp_id} | {d['seed']} | `{d['sha256'][:16]}...` | {'yes' if d['match'] else 'NO'} |")
    lines.append("")

    out_md = PAPER / "tables" / "auto_tables.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] wrote {out_md}")


if __name__ == "__main__":
    raise SystemExit(main())
