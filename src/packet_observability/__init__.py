"""packet_observability: a safe-by-design synthetic packet-observability toolkit.

This package implements a configuration-driven, software-only ("demo mode")
workflow for generating synthetic packet-level traces, computing packet-level
observability metrics, plotting figures, and writing reproducibility manifests.

Scope and non-goals
--------------------
The synthetic demo mode emits **no** radio signal and touches **no** network
interface; it only reads YAML configuration files and writes CSV/JSON/PNG files.
It is an instrumentation and reproducibility layer for educational
cyber-physical laboratories. It is *not* a standard-conformant implementation of
Wi-Fi, BLE, IEEE 802.15.4/Zigbee, LoRa, or SDR systems, and it makes no real
radio-performance, scheduling, interference-mitigation, or certification claims.

Optional owned-device and receive-only extensions live in
``packet_observability.extensions`` and are intended for authorised laboratory
use only.
"""
from __future__ import annotations

__version__ = "0.1.1"

__all__ = [
    "__version__",
]
