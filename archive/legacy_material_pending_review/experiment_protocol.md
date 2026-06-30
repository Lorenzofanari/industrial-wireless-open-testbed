# Experiment Protocol

This protocol covers both **demo mode** (synthetic) and **Phase 2 real-hardware**
experiments. Follow the safety checklist before any radio/network activity.

> ⚠️ Read [`../hardware/safety_notes.md`](../hardware/safety_notes.md) first.
> Only use owned/authorised devices and networks. SDR is **receive-only**.

## 0. Pre-experiment safety checklist

- [ ] I own or am authorised to use every device/network involved.
- [ ] No experiment transmits interference or targets third-party networks.
- [ ] SDR (if used) is configured **receive-only** on a legally observable band.
- [ ] Cabled/attenuated/shielded setup used where practical.
- [ ] `safety_mode` in the config matches the actual setup.

## 1. Choose and review a config

Each case study has a YAML config under `configs/`. Confirm:
- `experiment_id`, `technology`, `safety_mode`
- `packet_size_bytes`, `packet_interval_ms`, `experiment_duration_s`
- `repetitions`, `random_seed`, `metrics_to_compute`

## 2. Demo-mode run (always available)

```bash
python -m src.capture.synthetic_capture_generator --config configs/<case>.yaml --run-label run01
python -m src.analysis.compute_metrics --input results/<exp>/run01/packets.csv
python -m src.analysis.make_plots --input results/<exp>/run01/packets.csv --out-dir results/<exp>/figures
```

Repeat for `repetitions` runs (vary `--seed`), then:

```bash
python -m src.analysis.repeatability_report --experiment-id <exp>
```

## 3. Real-capture run (Phase 2, owned interface)

### 3.1 Dry-run first (safe default)

```bash
python -m src.capture.capture_tshark --config configs/case_wifi_latency.yaml \
    --interface lo --dry-run
```

### 3.2 Capture (after confirming ownership)

```bash
python -m src.capture.capture_tshark --config configs/case_wifi_latency.yaml \
    --interface <owned_iface> --duration 60 --confirm-owned
```

### 3.3 Parse to canonical CSV

```bash
python -m src.capture.parse_pcap --input results/<exp>/run01/capture.pcapng
python -m src.analysis.compute_metrics --input results/<exp>/run01/packets.csv
```

## 4. Generating controlled benign traffic (owned nodes)

```bash
# Receiver on the gateway node:
python -m src.traffic.udp_telemetry_receiver --port 9999 --duration 65

# Sender on a sensor node (rate-limited):
python -m src.traffic.udp_telemetry_sender --host <gateway_ip> --port 9999 \
    --interval-ms 50 --packet-size 128 --duration 60
```

> The sender enforces a conservative rate cap and is **not** a load/flood tool.

## 5. Per-case-study parameters (conservative defaults)

| Case | Nodes | Sizes (B) | Interval (ms) | Duration (s) | Reps |
|------|-------|-----------|---------------|--------------|------|
| 1 Wi-Fi | 2 senders + 1 rx (+1 monitor) | 128/256/512 | 20/50/100 | 60 | 5 |
| 2 BLE | 3 sensors + 1 gateway | 20/32/64 | 250/500/1000 | 120 | 5 |
| 3 802.15.4 | 4 sensors + 1 sink | 32/64/96 | 500/1000/2000 | 180 | 5 |
| 4 LoRa/SDR | synthetic / rx-only | 12/24/51 | 1000/5000/10000 | 300 | 3 |

## 6. Post-experiment

- [ ] Verify a `manifest.json` exists for each run.
- [ ] Archive `results/<exp>/` (do **not** commit raw `.pcap`).
- [ ] Record any deviations from the config in your lab notebook.
- [ ] Power down radios; detach antennas safely.
