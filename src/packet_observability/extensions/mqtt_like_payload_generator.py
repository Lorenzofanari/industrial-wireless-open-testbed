"""MQTT-like synthetic telemetry payload generator (offline, no broker).

Produces JSON-lines telemetry records resembling typical IIoT MQTT publishes
(topic, sensor id, value, units, sequence, timestamp). This is OFFLINE: it does
NOT connect to any broker or network. The output can be replayed by
``safe_trace_replay`` (on owned nodes) or used as synthetic input.

Safety note
-----------
Pure local file generation. No network connection, no broker, no publishing.

Usage
-----
    python -m packet_observability.extensions.mqtt_like_payload_generator \
        --sensors 3 --interval-ms 500 --duration 30
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from packet_observability.io import ensure_parent, results_dir

SENSOR_KINDS = [
    ("temperature", "degC", 18.0, 26.0),
    ("humidity", "pct", 30.0, 60.0),
    ("vibration", "mm_s", 0.1, 3.0),
    ("pressure", "bar", 0.9, 1.2),
]


def generate(
    *,
    sensors: int,
    interval_ms: int,
    duration_s: float,
    seed: int = 12345,
    out_path: Path | None = None,
) -> Path:
    rng = random.Random(seed)
    if out_path is None:
        out_path = results_dir() / "_traffic_logs" / "mqtt_like.jsonl"
    out_path = ensure_parent(Path(out_path))

    kinds = [SENSOR_KINDS[i % len(SENSOR_KINDS)] for i in range(sensors)]
    interval_s = interval_ms / 1000.0
    n_steps = int(duration_s / interval_s)
    base_ts = time.time()

    count = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for step in range(n_steps):
            for s in range(sensors):
                name, units, lo, hi = kinds[s]
                rec = {
                    "topic": f"factory/line1/{name}/{s + 1:02d}",
                    "sensor_id": f"{name}_{s + 1:02d}",
                    "seq": step + 1,
                    "ts": round(base_ts + step * interval_s, 6),
                    "value": round(rng.uniform(lo, hi), 3),
                    "units": units,
                    "qos": 0,
                }
                fh.write(json.dumps(rec) + "\n")
                count += 1
    print(f"[mqtt-like] wrote {count} synthetic publishes -> {out_path}")
    return out_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Offline MQTT-like synthetic telemetry generator (no broker).")
    p.add_argument("--sensors", type=int, default=3)
    p.add_argument("--interval-ms", type=int, default=500)
    p.add_argument("--duration", type=float, default=30.0)
    p.add_argument("--seed", type=int, default=12345)
    p.add_argument("--out", default=None)
    args = p.parse_args(argv)
    generate(
        sensors=args.sensors,
        interval_ms=args.interval_ms,
        duration_s=args.duration,
        seed=args.seed,
        out_path=Path(args.out) if args.out else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
