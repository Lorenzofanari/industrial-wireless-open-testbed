"""Benign periodic UDP telemetry sender (owned lab nodes only).

Sends small, rate-limited UDP datagrams carrying a sequence id and a send
timestamp to a destination YOU control. Defaults to localhost.

Safety / legal note
-------------------
* Send ONLY to IP/ports of devices you own or are authorised to test.
* This is cooperative telemetry, not a load/flood tool. A hard rate cap is
  enforced (see ``MAX_PPS``) to prevent accidental network stress.
* There is no broadcast/multicast convenience and no high-rate mode, by design.

Usage
-----
    # Terminal A (receiver):
    python -m packet_observability.extensions.owned_udp_telemetry_receiver --port 9999
    # Terminal B (sender):
    python -m packet_observability.extensions.owned_udp_telemetry_sender \
        --host 127.0.0.1 --port 9999 --interval-ms 50 --packet-size 128 --duration 10
"""
from __future__ import annotations

import argparse
import socket
import time
from pathlib import Path

from packet_observability.io import ensure_parent, results_dir

# Conservative safety cap: refuse configurations above this packet rate.
MAX_PPS = 200

SAFETY_BANNER = (
    "[safety] Benign telemetry sender. Send ONLY to devices you own/authorised. "
    "Rate-limited; not a load generator."
)


def _build_payload(seq_id: int, target_size: int) -> bytes:
    header = f"seq={seq_id};ts={time.time():.6f};".encode("ascii")
    if len(header) >= target_size:
        return header[:target_size]
    return header + b"\x00" * (target_size - len(header))


def run(
    host: str,
    port: int,
    *,
    interval_ms: int,
    packet_size: int,
    duration_s: float,
    log_path: Path | None = None,
) -> Path:
    pps = 1000.0 / max(interval_ms, 1)
    if pps > MAX_PPS:
        raise SystemExit(
            f"Refusing to send at ~{pps:.0f} pps (interval {interval_ms} ms). "
            f"Max allowed is {MAX_PPS} pps. Increase --interval-ms."
        )

    print(SAFETY_BANNER)
    print(f"[sender] -> {host}:{port} every {interval_ms} ms, size {packet_size} B, {duration_s}s")

    if log_path is None:
        log_dir = results_dir() / "_traffic_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "udp_sender_log.csv"
    else:
        log_path = ensure_parent(log_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interval_s = interval_ms / 1000.0
    end_t = time.time() + duration_s
    seq = 0
    sent = 0
    with Path(log_path).open("w", encoding="utf-8") as log:
        log.write("send_timestamp,sequence_id,packet_size_bytes,dest_host,dest_port\n")
        try:
            while time.time() < end_t:
                seq += 1
                payload = _build_payload(seq, packet_size)
                send_ts = time.time()
                sock.sendto(payload, (host, port))
                sent += 1
                log.write(f"{send_ts:.6f},{seq},{len(payload)},{host},{port}\n")
                sleep_for = interval_s - (time.time() - send_ts)
                if sleep_for > 0:
                    time.sleep(sleep_for)
        finally:
            sock.close()
    print(f"[sender] sent {sent} datagrams; log -> {log_path}")
    return Path(log_path)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Benign periodic UDP telemetry sender (owned nodes only).")
    p.add_argument("--host", default="127.0.0.1", help="Destination IP (default: localhost).")
    p.add_argument("--port", type=int, default=9999)
    p.add_argument("--interval-ms", type=int, default=50)
    p.add_argument("--packet-size", type=int, default=128)
    p.add_argument("--duration", type=float, default=10.0, help="Duration in seconds.")
    p.add_argument("--log", default=None, help="Path to sender CSV log.")
    args = p.parse_args(argv)
    run(
        args.host,
        args.port,
        interval_ms=args.interval_ms,
        packet_size=args.packet_size,
        duration_s=args.duration,
        log_path=Path(args.log) if args.log else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
