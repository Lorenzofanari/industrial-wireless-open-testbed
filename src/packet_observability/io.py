"""Input/output helpers: configuration loading, packet CSV I/O, and paths.

This module centralises reading the YAML case-study configurations and the
canonical packet-level CSV traces, plus a few defensive path utilities that keep
all generated artefacts inside the repository tree.

Safety note: configuration files describe synthetic demo-mode profiles (or
optional owned-device / receive-only extensions). The ``safety_mode`` field is
mandatory and is surfaced to the user by every tool that consumes a config.
This module performs no network or radio operations.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# --- canonical packet schema -------------------------------------------------

# The canonical per-packet CSV schema used throughout the toolkit. See
# docs/packet_schema.md for the full definition.
CSV_FIELDS: list[str] = [
    "timestamp",
    "node_id",
    "packet_id",
    "packet_size_bytes",
    "rssi_dbm",
    "channel",
    "sequence_id",
    "payload_type",
]

# Recognised, explicitly-safe operating modes.
ALLOWED_SAFETY_MODES = {
    "synthetic_only",
    "synthetic_or_owned_devices_only",
    "synthetic_or_owned_testbed_only",
    "owned_lab_network_only",
    "receive_only_or_synthetic_only",
}

REQUIRED_KEYS = (
    "experiment_id",
    "technology",
    "number_of_nodes",
    "packet_size_bytes",
    "packet_interval_ms",
    "experiment_duration_s",
    "repetitions",
    "random_seed",
    "safety_mode",
)


@dataclass
class CaseStudyConfig:
    """Typed view over a technology-like case-study configuration."""

    experiment_id: str
    technology: str
    number_of_nodes: int
    packet_size_bytes: list[int]
    packet_interval_ms: list[int]
    experiment_duration_s: float
    repetitions: int
    random_seed: int
    safety_mode: str
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def default_packet_size(self) -> int:
        return self.packet_size_bytes[0]

    @property
    def default_interval_ms(self) -> int:
        return self.packet_interval_ms[0]

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)


def _as_list(value: Any) -> list:
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def load_config(path: str | Path) -> CaseStudyConfig:
    """Read, validate, and return a :class:`CaseStudyConfig`."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"Config {path} is missing required keys: {missing}")

    safety_mode = str(data["safety_mode"])
    if safety_mode not in ALLOWED_SAFETY_MODES:
        raise ValueError(
            f"Config {path} has unrecognised safety_mode {safety_mode!r}. "
            f"Allowed: {sorted(ALLOWED_SAFETY_MODES)}"
        )

    return CaseStudyConfig(
        experiment_id=str(data["experiment_id"]),
        technology=str(data["technology"]),
        number_of_nodes=int(data["number_of_nodes"]),
        packet_size_bytes=[int(x) for x in _as_list(data["packet_size_bytes"])],
        packet_interval_ms=[int(x) for x in _as_list(data["packet_interval_ms"])],
        experiment_duration_s=float(data["experiment_duration_s"]),
        repetitions=int(data["repetitions"]),
        random_seed=int(data["random_seed"]),
        safety_mode=safety_mode,
        raw=data,
    )


# --- packet CSV I/O ----------------------------------------------------------

def write_packets_csv(records: list[dict[str, Any]], path: str | Path) -> Path:
    """Write packet records to ``path`` using the canonical schema."""
    path = ensure_parent(Path(path))
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r.get(k, "") for k in CSV_FIELDS})
    return path


def read_packets_csv(path: str | Path):
    """Read a canonical packets.csv into a pandas DataFrame.

    Imported lazily so that lightweight callers (e.g. config validation) do not
    pull in pandas.
    """
    import pandas as pd

    return pd.read_csv(path)


# --- path helpers ------------------------------------------------------------

def project_root() -> Path:
    """Return the repository root (three levels up from this file)."""
    return Path(__file__).resolve().parents[2]


def results_dir() -> Path:
    """Return the ``results/`` directory, creating it if necessary."""
    d = project_root() / "results"
    d.mkdir(parents=True, exist_ok=True)
    return d


def data_dir() -> Path:
    """Return the ``data/`` directory, creating it if necessary."""
    d = project_root() / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensure_dir(path: str | Path) -> Path:
    """Ensure ``path`` exists as a directory; return it."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: str | Path) -> Path:
    """Ensure the parent directory of ``path`` exists; return ``path``."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
