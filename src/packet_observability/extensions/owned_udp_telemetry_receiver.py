"""Benign UDP telemetry receiver/logger (owned lab nodes only).

Listens for the datagrams produced by ``owned_udp_telemetry_sender`` and logs
the receive timestamp, sequence id, and size. Combined with the sender log this
yields a latency proxy (recv_ts - send_ts) and packet-loss indicators (missing
sequence ids).

Safety note
-----------
Passive listener bound to a local port you control. It does not reply, scan, or
forward anything.

Usage
-----
    python -m packet_observability.extensions.owned_udp_telemetry_receiver \
        --port 9999 --duration 12
"""
from __future__ import annotations

import argparse
import socket
import time
from pathlib import Path

from packet_observability.io import ensure_parent, results_dir


def _parse_payload(data: bytes) -> tuple[int, float]:
    """Extract (sequence_id, send_ts) from a sender payload; tolerant of noise."""
    seq = -1
    send_ts = float("nan")
    try:
        text = data.split(b"\x00", 1)[0].decode("ascii", errors="ignore")
        for field in text.split(";"):
            if field.startswith("seq="):
                seq = int(field[4:])
            elif field.startswith("ts="):
                send_ts = float(field[3:])
    except (ValueError, UnicodeDecodeError):
        pass
    return seq, send_ts


def run(port: int, *, duration_s: float, host: str = "0.0.0.0", log_path: Path | None = None) -> Path:
    print(f"[receiver] listening on {host}:{port} for {duration_s}s (owned-network use only)")

    if log_path is None:
        log_dir = results_dir() / "_traffic_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "udp_receiver_log.csv"
    else:
        log_path = ensure_parent(log_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.settimeout(0.5)

    end_t = time.time() + duration_s
    received = 0
    with Path(log_path).open("w", encoding="utf-8") as log:
        log.write("recv_timestamp,send_timestamp,sequence_id,packet_size_bytes,latency_proxy_ms,src_ip\n")
        while time.time() < end_t:
            try:
                data, addr = sock.recvfrom(65535)
            except socket.timeout:
                continue
            recv_ts = time.time()
            seq, send_ts = _parse_payload(data)
            latency_ms = (recv_ts - send_ts) * 1000.0 if send_ts == send_ts else ""  # NaN check
            latency_str = f"{latency_ms:.3f}" if latency_ms != "" else ""
            log.write(f"{recv_ts:.6f},{send_ts:.6f},{seq},{len(data)},{latency_str},{addr[0]}\n")
            received += 1
    sock.close()
    print(f"[receiver] received {received} datagrams; log -> {log_path}")
    return Path(log_path)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Benign UDP telemetry receiver/logger (owned nodes only).")
    p.add_argument("--port", type=int, default=9999)
    p.add_argument("--host", default="0.0.0.0", help="Bind address (default: all local interfaces).")
    p.add_argument("--duration", type=float, default=12.0)
    p.add_argument("--log", default=None)
    args = p.parse_args(argv)
    run(
        args.port,
        duration_s=args.duration,
        host=args.host,
        log_path=Path(args.log) if args.log else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
