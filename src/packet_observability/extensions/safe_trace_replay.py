"""Safe CSV-driven trace replay (owned lab nodes only).

Replays the *timing* of a recorded/synthetic packets.csv by sending benign,
rate-limited UDP datagrams to a destination YOU control (default localhost).
Only the inter-arrival timing and packet sizes are reproduced; original payload
contents are NOT reconstructed or replayed.

Safety / legal note
-------------------
* Replay ONLY toward devices you own / are authorised to test.
* The same hard rate cap as the telemetry sender applies; bursts faster than the
  cap are throttled rather than reproduced. This makes the tool unsuitable for
  stress use, by design.
* This is NOT a traffic-injection tool.

Usage
-----
    python -m packet_observability.extensions.safe_trace_replay \
        --input results/demo/wifi_like/packets.csv \
        --host 127.0.0.1 --port 9999 --speed 1.0 --dry-run
"""
from __future__ import annotations

import argparse
import csv
import socket
import time
from pathlib import Path

MIN_INTERVAL_S = 1.0 / 200.0  # mirror MAX_PPS = 200 in the sender


def load_trace(path: Path) -> list[tuple[float, int]]:
    """Return a list of (timestamp, size_bytes) sorted by timestamp."""
    rows: list[tuple[float, int]] = []
    with Path(path).open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            try:
                ts = float(r["timestamp"])
                size = int(float(r.get("packet_size_bytes", 64) or 64))
            except (KeyError, ValueError):
                continue
            rows.append((ts, size))
    rows.sort(key=lambda x: x[0])
    return rows


def replay(
    rows: list[tuple[float, int]],
    *,
    host: str,
    port: int,
    speed: float = 1.0,
    dry_run: bool = True,
) -> int:
    if not rows:
        print("[replay] empty trace; nothing to do.")
        return 0

    print("[safety] Safe trace replay: benign, rate-capped, owned nodes only.")
    if dry_run:
        print(f"[dry-run] Would replay {len(rows)} packets to {host}:{port} at speed {speed}x")
        return 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t0 = rows[0][0]
    wall_start = time.time()
    sent = 0
    try:
        for ts, size in rows:
            target_offset = (ts - t0) / max(speed, 1e-6)
            now_offset = time.time() - wall_start
            sleep_for = target_offset - now_offset
            if sleep_for < MIN_INTERVAL_S and sent > 0:
                sleep_for = MIN_INTERVAL_S
            if sleep_for > 0:
                time.sleep(sleep_for)
            payload = b"replay" + b"\x00" * max(0, size - 6)
            sock.sendto(payload[:size] if size > 0 else b"replay", (host, port))
            sent += 1
    finally:
        sock.close()
    print(f"[replay] sent {sent} datagrams to {host}:{port}")
    return sent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Safe CSV trace replay (owned nodes only).")
    p.add_argument("--input", required=True, help="packets.csv to replay (timing + sizes only).")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=9999)
    p.add_argument("--speed", type=float, default=1.0, help="Playback speed multiplier.")
    p.add_argument("--dry-run", action="store_true", help="Print plan without sending (default-safe).")
    p.add_argument("--confirm-owned", action="store_true", help="Affirm destination is owned/authorised.")
    args = p.parse_args(argv)

    rows = load_trace(Path(args.input))
    do_dry = args.dry_run or not args.confirm_owned
    if not args.confirm_owned and not args.dry_run:
        print("Refusing to send: pass --confirm-owned to affirm the destination is yours.")
    replay(rows, host=args.host, port=args.port, speed=args.speed, dry_run=do_dry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
