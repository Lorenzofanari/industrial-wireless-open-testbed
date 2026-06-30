# Operating Instructions

## 1. Intended use

A teaching-oriented packet-observability workflow. Students configure a
technology-like traffic profile, generate a reproducible synthetic trace, compute
packet-level metrics, inspect figures and manifests, compare profiles, and
document their findings — all software-only, with no radio hardware.

## 2. Laboratory session overview

- **Suggested duration:** 90–120 minutes.
- **Audience:** undergraduate students, master students, early-stage
  researchers, and instructors.
- **Prerequisites:** basic Python, basic CSV familiarity, basic networking
  concepts. No radio hardware is required for Tier 0.

## 3. Workflow

The student will:

1. select a case profile (`configs/<case>.yaml`);
2. inspect the YAML parameters;
3. generate a synthetic trace;
4. compute metrics;
5. inspect the plots;
6. inspect the manifest and SHA-256 hashes;
7. compare two or more profiles;
8. answer the reflection questions;
9. submit the deliverables.

## 4. Commands

```bash
python scripts/run_demo.py --config configs/wifi_like.yaml --out results/demo/wifi_like
python scripts/compute_metrics.py --input results/demo/wifi_like/packets.csv
python scripts/plot_results.py --input results/demo/wifi_like/packets.csv --out-dir results/demo/wifi_like/figures
python scripts/verify_reproducibility.py --all
```

Repeat with another profile (e.g. `configs/ble_like.yaml`) to compare.

## 5. What students should observe

- **Packet count** — total number of packets in the trace.
- **Packet size** — mean and distribution of packet sizes.
- **Inter-arrival time** — spacing between globally-ordered packets.
- **Jitter proxy** — standard deviation of inter-arrival times.
- **Missing sequence identifiers** — gaps in per-node sequence ranges.
- **Duplicate sequence identifiers** — repeated per-node sequence values.
- **Capture completeness** — observed unique sequences ÷ expected span.
- **Manifest hashes** — SHA-256 digests that tie outputs to inputs.

See [`metrics.md`](metrics.md) for the precise definitions.

## 6. Synthetic vs real data

Synthetic demo-mode traces verify the **software pipeline**. They do **not**
measure real Wi-Fi, BLE, IEEE 802.15.4, Zigbee, LoRa, or SDR performance. The
`channel` and `rssi_dbm` fields in demo mode are synthetic labels, not real RF
measurements.

## 7. Deliverables

Students complete and submit [`student_worksheet.md`](student_worksheet.md).

## 8. Assessment

Work is graded against [`assessment_rubric.md`](assessment_rubric.md).

## 9. Safety boundaries

This workflow includes no jamming, flooding, deauthentication, exploitation,
unauthorised scanning, or third-party observation. Optional hardware tiers are
owned-device or receive-only and must only be used in authorised, controlled
environments. See [`safety_and_ethics.md`](safety_and_ethics.md).
