# Owned-device extension notes

These notes apply to the optional tiers that observe benign traffic on devices
and networks **you own or are explicitly authorised to use**. They are not
required for the software-only demo.

## Before you start

- Confirm you own, or are explicitly authorised to observe, every device and
  network involved.
- Set the matching config's `safety_mode` to reflect the actual setup.
- Prefer cabled or attenuated paths to reduce variability and keep experiments
  contained.

## Passive Wi-Fi observation (Tier 1)

The optional capture helper is a thin, passive wrapper around `tshark`:

```bash
# Safe default: print the command without running it.
python -m packet_observability.extensions.owned_device_capture \
    --config configs/wifi_like.yaml --interface lo --dry-run
```

It performs passive capture only. It never transmits, scans, or injects, and it
requires an explicit `--confirm-owned` flag before touching a real interface.
Convert a capture into the canonical schema with:

```bash
python -m packet_observability.extensions.pcap_to_packets_csv \
    --input results/<exp>/run01/capture.pcapng
```

## Benign telemetry between owned nodes (Tiers 2–3)

For controlled, cooperative telemetry between nodes you own, a rate-limited UDP
sender/receiver pair is provided (default destination: localhost). The sender
enforces a conservative packet-rate cap and is not a load generator:

```bash
# Receiver on the gateway node:
python -m packet_observability.extensions.owned_udp_telemetry_receiver --port 9999
# Sender on a node you own:
python -m packet_observability.extensions.owned_udp_telemetry_sender \
    --host 127.0.0.1 --port 9999 --interval-ms 50 --packet-size 128 --duration 10
```

## What these tools never do

They provide no jamming, flooding, deauthentication, exploitation, or
unauthorised scanning. They observe owned/authorised traffic only. See
[`safety_notes.md`](safety_notes.md).
