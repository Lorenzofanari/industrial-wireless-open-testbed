"""Make the ``src/`` package importable when running scripts directly.

Importing this module (``import _bootstrap``) prepends the repository ``src/``
directory to ``sys.path`` so that ``import packet_observability`` works without
installing the package or setting ``PYTHONPATH`` manually.
"""
from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parents[1]


# Canonical case-study configs, in presentation order.
CASE_CONFIGS = [
    "wifi_like",
    "ble_like",
    "ieee802154_like",
    "lora_sdr_like",
]

# Neutral scientific-facing workload identifiers (W1-W4) for each legacy config
# name. The YAML filenames and experiment_id values are kept unchanged for
# backward compatibility; see docs/case_studies.md.
WORKLOAD_LABELS = {
    "wifi_like": "W1",
    "ble_like": "W2",
    "ieee802154_like": "W3",
    "lora_sdr_like": "W4",
}


def workload_label(experiment_id: str) -> str:
    """Return ``"W1 (wifi_like)"``-style label, or the bare id if unmapped."""
    label = WORKLOAD_LABELS.get(experiment_id)
    return f"{label} ({experiment_id})" if label else experiment_id
