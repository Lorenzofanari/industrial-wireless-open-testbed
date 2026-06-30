"""Deterministic synthetic packet-trace generator (demo mode).

Reads a technology-like case-study YAML configuration and produces a
reproducible synthetic packet trace that mimics the *shape* of an observed
packet stream (timestamps, sizes, per-node sequence identifiers, optional
signal/channel metadata). This lets the whole analysis-to-figures workflow run
with zero hardware and zero radio emission.

Safety note
-----------
This generator emits NO radio signal and touches NO network interface. It only
reads a YAML file and returns / writes synthetic records. The optional
missing-sample model merely omits rows in a synthetic trace so that downstream
analysis can exercise its "missing sequence id" logic; it does not correspond to
any real-world phenomenon.
"""
from __future__ import annotations

import random
from typing import Any

from packet_observability.io import CaseStudyConfig

# Per-technology presentation hints for the synthetic trace. These are cosmetic
# labels for a technology-like profile, NOT standard-conformant parameters.
_NODE_PREFIX = {
    "wifi": "sta",
    "ble": "sensor",
    "ieee802154": "node",
    "lora_sdr": "emitter",
}
_SYNTHETIC_CHANNEL = {
    "wifi": 36,
    "ble": 37,
    "ieee802154": 15,
    "lora_sdr": 868,
}
_TECH_WITH_RSSI = {"wifi", "ble", "ieee802154"}


def _node_names(config: CaseStudyConfig) -> list[str]:
    """Build logical sender/sensor node identifiers from the config."""
    roles = config.get("roles", {}) or {}
    senders = (
        roles.get("senders")
        or roles.get("sensors")
        or roles.get("emitters_synthetic")
        or max(config.number_of_nodes - 1, 1)
    )
    senders = int(senders)
    prefix = _NODE_PREFIX.get(config.technology, "node")
    return [f"{prefix}_{i + 1:02d}" for i in range(senders)]


def _drop_probability_from_config(config: CaseStudyConfig) -> float:
    """Read the synthetic missing-sample probability from the config, if any."""
    model = config.get("missing_sample_model", {}) or {}
    if isinstance(model, dict):
        return float(model.get("drop_probability", 0.0) or 0.0)
    return 0.0


def generate_packets(
    config: CaseStudyConfig,
    *,
    packet_size: int | None = None,
    interval_ms: int | None = None,
    seed: int | None = None,
    drop_probability: float | None = None,
    jitter_fraction: float = 0.05,
) -> list[dict[str, Any]]:
    """Generate a deterministic list of synthetic packet records.

    Parameters
    ----------
    drop_probability:
        Synthetic missing-sample fraction (0..1). Omits rows while still
        advancing the per-node sequence id, so analysis can detect a "missing
        sequence id". When ``None`` the value is taken from the config's
        ``missing_sample_model`` (default 0.0).
    jitter_fraction:
        Random timing perturbation as a fraction of the nominal interval, used to
        produce a realistic inter-arrival distribution.
    """
    rng = random.Random(seed if seed is not None else config.random_seed)

    packet_size = packet_size or config.default_packet_size
    interval_ms = interval_ms or config.default_interval_ms
    interval_s = interval_ms / 1000.0
    duration_s = config.experiment_duration_s
    if drop_probability is None:
        drop_probability = _drop_probability_from_config(config)

    nodes = _node_names(config)
    channel_band = str(config.get("channel_or_band", ""))
    channel = _SYNTHETIC_CHANNEL.get(config.technology, 0)
    has_rssi = config.technology in _TECH_WITH_RSSI

    records: list[dict[str, Any]] = []
    packet_id = 0
    seq_by_node = {n: 0 for n in nodes}

    n_steps = int(duration_s / interval_s)
    for step in range(n_steps):
        nominal_t = step * interval_s
        for node in nodes:
            seq_by_node[node] += 1
            seq_id = seq_by_node[node]

            if rng.random() < drop_probability:
                continue

            jitter = rng.uniform(-jitter_fraction, jitter_fraction) * interval_s
            ts = max(0.0, nominal_t + jitter)
            size = max(1, int(rng.gauss(packet_size, packet_size * 0.05)))
            rssi = round(rng.uniform(-75, -45), 1) if has_rssi else ""

            records.append(
                {
                    "timestamp": round(ts, 6),
                    "node_id": node,
                    "packet_id": packet_id,
                    "packet_size_bytes": size,
                    "rssi_dbm": rssi,
                    "channel": channel if channel_band else "",
                    "sequence_id": seq_id,
                    "payload_type": "synthetic_telemetry",
                }
            )
            packet_id += 1

    records.sort(key=lambda r: r["timestamp"])
    return records
