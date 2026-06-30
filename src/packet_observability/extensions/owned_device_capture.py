"""Thin, passive wrapper around tshark for capture on OWNED interfaces.

Safety / legal note
-------------------
* Capture ONLY on interfaces and networks you own or are explicitly authorised
  to observe.
* This tool performs PASSIVE capture only. It does not transmit, deauthenticate,
  scan, or inject anything.
* Passive capture of third-party traffic may be unlawful in your jurisdiction.
  You are responsible for compliance.
* The default mode is ``--dry-run``: it only prints the command it would run.

Usage
-----
    # Show the command without running it (safe default):
    python -m packet_observability.extensions.owned_device_capture \
        --config configs/wifi_like.yaml --interface lo --dry-run

    # Capture (requires tshark and appropriate permissions on an owned iface):
    python -m packet_observability.extensions.owned_device_capture \
        --config configs/wifi_like.yaml --interface lo --duration 10 --confirm-owned
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from packet_observability.io import ensure_dir, load_config, results_dir

SAFETY_BANNER = (
    "=" * 70
    + "\n SAFETY: Passive capture on OWNED/AUTHORISED interfaces only.\n"
    + " This tool never transmits. You are responsible for legal compliance.\n"
    + "=" * 70
)


def build_tshark_command(interface: str, duration: int, out_pcap: Path) -> list[str]:
    """Build a passive tshark capture command (capture to pcapng)."""
    return ["tshark", "-i", interface, "-a", f"duration:{int(duration)}", "-w", str(out_pcap)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Passive tshark capture wrapper (owned interfaces only).",
    )
    p.add_argument("--config", required=True, help="Case-study YAML config.")
    p.add_argument("--interface", required=True, help="Interface to capture on (e.g. lo, eth0).")
    p.add_argument("--duration", type=int, default=None, help="Capture duration (s). Defaults to config.")
    p.add_argument("--run-label", default="run01")
    p.add_argument("--dry-run", action="store_true", help="Print the command without executing (default-safe).")
    p.add_argument(
        "--confirm-owned",
        action="store_true",
        help="Affirm you own / are authorised to observe this interface. Required to actually run.",
    )
    args = p.parse_args(argv)

    print(SAFETY_BANNER)
    config = load_config(args.config)
    duration = args.duration or int(config.experiment_duration_s)
    out_dir = ensure_dir(results_dir() / config.experiment_id / args.run_label)
    out_pcap = out_dir / "capture.pcapng"

    cmd = build_tshark_command(args.interface, duration, out_pcap)
    printable = " ".join(cmd)

    if args.dry_run or not args.confirm_owned:
        print("[dry-run] Would execute:")
        print(f"    {printable}")
        if not args.confirm_owned:
            print("\nRefusing to capture: pass --confirm-owned to affirm ownership/authorisation.")
        return 0

    if shutil.which("tshark") is None:
        print("ERROR: tshark not found on PATH. Install Wireshark/tshark to capture.")
        print(f"(Would have run: {printable})")
        return 1

    print(f"[capture] Running: {printable}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: tshark exited with status {exc.returncode}")
        return exc.returncode
    print(f"[capture] Saved -> {out_pcap}")
    print("Next: python -m packet_observability.extensions.pcap_to_packets_csv --input", out_pcap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
