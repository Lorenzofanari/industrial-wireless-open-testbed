"""Packet-level observability metrics computed from canonical CSV traces.

Per-run metrics (see docs/metrics.md):
  * total_packets, duration_s, packet_rate_pps
  * mean_packet_size_bytes
  * inter_arrival_mean_ms / inter_arrival_std_ms (jitter proxy = std)
  * missing_sequence_ids, duplicate_sequence_ids
  * capture_completeness
  * per_node_packet_counts

Outputs written by :func:`write_outputs`:
  * metrics.csv          - one row per scalar metric (long form)
  * metrics_summary.json - structured summary including per-node counts
  * inter_arrival.csv    - per-packet inter-arrival series (for plotting)

Safety note: this is pure offline analysis of a local CSV. No network or radio
access.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

SCALAR_METRICS = [
    "total_packets",
    "duration_s",
    "packet_rate_pps",
    "mean_packet_size_bytes",
    "inter_arrival_mean_ms",
    "inter_arrival_std_ms",
    "jitter_proxy_ms",
    "missing_sequence_ids",
    "duplicate_sequence_ids",
    "capture_completeness",
]


def _missing_and_duplicate_sequences(df: pd.DataFrame) -> tuple[int, int]:
    """Count missing and duplicate per-node sequence identifiers.

    Missing  = gaps in the per-node sequence range (max-min+1 - unique observed).
    Duplicate = observed count - unique count, per node.
    """
    missing = 0
    duplicate = 0
    if "sequence_id" not in df.columns:
        return missing, duplicate
    for _, group in df.groupby("node_id"):
        seqs = pd.to_numeric(group["sequence_id"], errors="coerce").dropna().astype(int)
        if seqs.empty:
            continue
        observed = len(seqs)
        unique = seqs.nunique()
        expected = int(seqs.max() - seqs.min() + 1)
        missing += max(0, expected - unique)
        duplicate += max(0, observed - unique)
    return missing, duplicate


def compute_metrics(df: pd.DataFrame) -> dict[str, Any]:
    """Compute the metrics dictionary from a packets DataFrame."""
    if df.empty:
        raise ValueError("packets.csv contains no rows")

    df = df.copy()
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    df["packet_size_bytes"] = pd.to_numeric(df["packet_size_bytes"], errors="coerce")

    total_packets = int(len(df))
    duration_s = float(df["timestamp"].max() - df["timestamp"].min())
    packet_rate_pps = total_packets / duration_s if duration_s > 0 else float("nan")
    mean_size = float(df["packet_size_bytes"].mean())

    inter_arrival_ms = df["timestamp"].diff().dropna() * 1000.0
    ia_mean = float(inter_arrival_ms.mean()) if not inter_arrival_ms.empty else float("nan")
    ia_std = float(inter_arrival_ms.std(ddof=0)) if not inter_arrival_ms.empty else float("nan")

    missing, duplicate = _missing_and_duplicate_sequences(df)

    expected_total = 0
    observed_unique_total = 0
    for _, group in df.groupby("node_id"):
        seqs = pd.to_numeric(group["sequence_id"], errors="coerce").dropna().astype(int)
        if seqs.empty:
            continue
        expected_total += int(seqs.max() - seqs.min() + 1)
        observed_unique_total += int(seqs.nunique())
    completeness = (observed_unique_total / expected_total) if expected_total > 0 else float("nan")

    per_node_counts = {str(k): int(v) for k, v in df.groupby("node_id").size().to_dict().items()}

    return {
        "total_packets": total_packets,
        "duration_s": round(duration_s, 6),
        "packet_rate_pps": round(packet_rate_pps, 4),
        "mean_packet_size_bytes": round(mean_size, 3),
        "inter_arrival_mean_ms": round(ia_mean, 4),
        "inter_arrival_std_ms": round(ia_std, 4),
        "jitter_proxy_ms": round(ia_std, 4),
        "missing_sequence_ids": int(missing),
        "duplicate_sequence_ids": int(duplicate),
        "capture_completeness": round(completeness, 4),
        "n_nodes": int(df["node_id"].nunique()),
        "per_node_packet_counts": per_node_counts,
        "_inter_arrival_ms_series": inter_arrival_ms.tolist(),
        "_packet_size_series": df["packet_size_bytes"].dropna().tolist(),
        "_timestamp_series": df["timestamp"].tolist(),
    }


def write_outputs(metrics: dict[str, Any], out_dir: str | Path) -> dict[str, Path]:
    """Write metrics.csv, inter_arrival.csv, and metrics_summary.json."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    scalar_rows = [
        {"metric": k, "value": v}
        for k, v in metrics.items()
        if not k.startswith("_") and k != "per_node_packet_counts"
    ]
    metrics_csv = out_dir / "metrics.csv"
    pd.DataFrame(scalar_rows).to_csv(metrics_csv, index=False)

    ia_csv = out_dir / "inter_arrival.csv"
    pd.DataFrame({"inter_arrival_ms": metrics["_inter_arrival_ms_series"]}).to_csv(ia_csv, index=False)

    summary = {k: v for k, v in metrics.items() if not k.startswith("_")}
    summary_json = out_dir / "metrics_summary.json"
    with summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    return {"metrics_csv": metrics_csv, "inter_arrival_csv": ia_csv, "summary_json": summary_json}


def compute_from_csv(input_csv: str | Path, out_dir: str | Path | None = None) -> dict[str, Path]:
    """Read a packets.csv, compute metrics, and write outputs."""
    input_csv = Path(input_csv)
    df = pd.read_csv(input_csv)
    metrics = compute_metrics(df)
    out_dir = Path(out_dir) if out_dir else input_csv.parent
    return write_outputs(metrics, out_dir)


def repeatability(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate mean/std/min/max of scalar metrics across run summaries."""
    df = pd.DataFrame(summaries)
    out: dict[str, Any] = {"n_runs": int(len(df)), "metrics": {}}
    for m in SCALAR_METRICS:
        if m not in df.columns:
            continue
        col = pd.to_numeric(df[m], errors="coerce").dropna()
        if col.empty:
            continue
        out["metrics"][m] = {
            "mean": round(float(col.mean()), 4),
            "std": round(float(col.std(ddof=0)), 4),
            "min": round(float(col.min()), 4),
            "max": round(float(col.max()), 4),
        }
    return out
