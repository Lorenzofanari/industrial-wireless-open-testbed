"""Convert a captured pcap/pcapng into the canonical packets.csv schema.

Uses ``tshark -T fields`` to extract a minimal, benign set of per-packet fields
(timestamp, length, addresses, ports). It deliberately extracts only the
metadata needed for the analysis workflow, not payload contents.

Safety note
-----------
Operate only on captures you are authorised to analyse. This script is
read-only with respect to the network; it parses a local file.

Usage
-----
    python -m packet_observability.extensions.pcap_to_packets_csv \
        --input results/<exp>/run01/capture.pcapng
"""
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
from pathlib import Path

from packet_observability.io import CSV_FIELDS

# tshark field names mapped onto the canonical schema.
TSHARK_FIELDS = [
    "frame.time_epoch",
    "frame.len",
    "eth.src",
    "wlan.sa",
    "ip.src",
    "udp.srcport",
    "tcp.srcport",
]


def build_tshark_export(in_pcap: Path) -> list[str]:
    cmd = ["tshark", "-r", str(in_pcap), "-T", "fields"]
    for f in TSHARK_FIELDS:
        cmd += ["-e", f]
    cmd += ["-E", "separator=,", "-E", "occurrence=f"]
    return cmd


def _node_from_row(parts: list[str]) -> str:
    eth_src, wlan_sa, ip_src = parts[2], parts[3], parts[4]
    for candidate in (wlan_sa, eth_src, ip_src):
        if candidate:
            return candidate
    return "unknown"


def parse_pcap_to_csv(in_pcap: Path, out_csv: Path) -> Path:
    """Run tshark and write a canonical packets.csv."""
    in_pcap = Path(in_pcap)
    if shutil.which("tshark") is None:
        raise RuntimeError(
            "tshark not found on PATH. Install Wireshark/tshark, or use the "
            "synthetic demo mode (synthetic_generator) instead."
        )
    if not in_pcap.exists():
        raise FileNotFoundError(f"pcap not found: {in_pcap}")

    cmd = build_tshark_export(in_pcap)
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)

    out_csv = Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    seq_by_node: dict[str, int] = {}
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for packet_id, line in enumerate(proc.stdout.splitlines()):
            parts = (line.split(",") + [""] * len(TSHARK_FIELDS))[: len(TSHARK_FIELDS)]
            ts = parts[0]
            length = parts[1]
            if not ts:
                continue
            node = _node_from_row(parts)
            seq_by_node[node] = seq_by_node.get(node, 0) + 1
            writer.writerow(
                {
                    "timestamp": ts,
                    "node_id": node,
                    "packet_id": packet_id,
                    "packet_size_bytes": length or 0,
                    "rssi_dbm": "",
                    "channel": "",
                    "sequence_id": seq_by_node[node],
                    "payload_type": "captured",
                }
            )
    return out_csv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Parse a pcap/pcapng into canonical packets.csv.")
    p.add_argument("--input", required=True, help="Path to .pcap/.pcapng file.")
    p.add_argument("--output", default=None, help="Output CSV (default: alongside input).")
    args = p.parse_args(argv)

    in_pcap = Path(args.input)
    out_csv = Path(args.output) if args.output else in_pcap.with_name("packets.csv")
    result = parse_pcap_to_csv(in_pcap, out_csv)
    print(f"[parse] Wrote {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
