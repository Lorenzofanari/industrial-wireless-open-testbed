"""Figure generation from canonical packet traces (offline, headless).

Figures (one plot per figure, matplotlib only, default styling):
  1. packet_count_over_time.png      - packets per time bin
  2. inter_arrival_distribution.png  - histogram of inter-arrival times
  3. packet_size_distribution.png    - histogram of packet sizes
  4. per_node_packet_count.png       - bar chart of packets per node
  5. repeatability_summary.png       - per-run metric with across-run mean

Safety note: offline plotting of local CSV/JSON. No network or radio access.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless / reproducible rendering
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402


def _save(fig, out_dir: Path, name: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_packet_count_over_time(df: pd.DataFrame, out_dir: Path, bin_s: float = 1.0) -> Path:
    t = pd.to_numeric(df["timestamp"], errors="coerce").dropna()
    t = t - t.min()
    bins = pd.cut(t, bins=max(1, int((t.max() + bin_s) / bin_s)))
    counts = t.groupby(bins, observed=False).count()
    centers = [interval.mid for interval in counts.index]

    fig, ax = plt.subplots()
    ax.plot(centers, counts.values, marker="o")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"Packets per {bin_s:g} s bin")
    ax.set_title("Packet count over time (synthetic demo-mode)")
    ax.grid(True, alpha=0.3)
    return _save(fig, out_dir, "packet_count_over_time.png")


def plot_inter_arrival(df: pd.DataFrame, out_dir: Path) -> Path:
    t = pd.to_numeric(df["timestamp"], errors="coerce").dropna().sort_values()
    ia_ms = t.diff().dropna() * 1000.0

    fig, ax = plt.subplots()
    ax.hist(ia_ms, bins=40)
    ax.set_xlabel("Inter-arrival time (ms)")
    ax.set_ylabel("Count")
    ax.set_title("Inter-arrival time distribution (synthetic demo-mode)")
    ax.grid(True, alpha=0.3)
    return _save(fig, out_dir, "inter_arrival_distribution.png")


def plot_packet_size(df: pd.DataFrame, out_dir: Path) -> Path:
    sizes = pd.to_numeric(df["packet_size_bytes"], errors="coerce").dropna()

    fig, ax = plt.subplots()
    ax.hist(sizes, bins=30)
    ax.set_xlabel("Packet size (bytes)")
    ax.set_ylabel("Count")
    ax.set_title("Packet size distribution (synthetic demo-mode)")
    ax.grid(True, alpha=0.3)
    return _save(fig, out_dir, "packet_size_distribution.png")


def plot_per_node(df: pd.DataFrame, out_dir: Path) -> Path:
    counts = df.groupby("node_id").size().sort_index()

    fig, ax = plt.subplots()
    ax.bar([str(i) for i in counts.index], counts.values)
    ax.set_xlabel("Logical node")
    ax.set_ylabel("Packet count")
    ax.set_title("Per-node packet count (synthetic demo-mode)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, axis="y", alpha=0.3)
    return _save(fig, out_dir, "per_node_packet_count.png")


def plot_repeatability(rep_csv: Path, out_dir: Path) -> Path | None:
    if not rep_csv.exists():
        return None
    df = pd.read_csv(rep_csv)
    if df.empty:
        return None
    metric = "packet_rate_pps" if "packet_rate_pps" in df.columns else df.columns[1]
    vals = pd.to_numeric(df[metric], errors="coerce")

    fig, ax = plt.subplots()
    ax.bar(df["run"].astype(str), vals)
    if vals.notna().any():
        ax.axhline(vals.mean(), linestyle="--", label=f"mean = {vals.mean():.3f}")
        ax.legend()
    ax.set_xlabel("Run")
    ax.set_ylabel(metric)
    ax.set_title(f"Repeatability across runs ({metric})")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, axis="y", alpha=0.3)
    return _save(fig, out_dir, "repeatability_summary.png")


def plot_from_csv(
    input_csv: str | Path,
    out_dir: str | Path | None = None,
    repeatability_csv: str | Path | None = None,
) -> list[Path]:
    """Generate the standard figure set from a packets.csv."""
    input_csv = Path(input_csv)
    df = pd.read_csv(input_csv)
    out_dir = Path(out_dir) if out_dir else input_csv.parent / "figures"

    produced = [
        plot_packet_count_over_time(df, out_dir),
        plot_inter_arrival(df, out_dir),
        plot_packet_size(df, out_dir),
        plot_per_node(df, out_dir),
    ]

    rep_csv = Path(repeatability_csv) if repeatability_csv else input_csv.parent.parent / "repeatability.csv"
    rep_fig = plot_repeatability(rep_csv, out_dir)
    if rep_fig:
        produced.append(rep_fig)
    return produced
