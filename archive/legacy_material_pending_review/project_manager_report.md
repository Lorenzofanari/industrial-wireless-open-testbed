# Project Manager Report

## 1. Objective

Deliver a **separate, open-source companion artifact** supporting an MDPI
*Hardware*-style paper about an **industrial wireless instrumentation testbed**:
packet capture, reproducibility, and educational cyber-physical experiments.

This artifact is **independent** of the main scheduler paper. It must not
disclose or reproduce the main paper's scheduling contributions (see the
contribution firewall in `paper_assets/hardware_paper_tables.md` and
`docs/limitations.md`).

## 2. Repository status

| Area | Status |
|------|--------|
| Repository scaffold | ✅ complete |
| Case-study configs (×4) | ✅ complete |
| Synthetic data generator (demo mode) | ✅ complete |
| Benign traffic tools (UDP, MQTT-like, safe replay) | ✅ complete |
| Capture helpers (tshark wrapper, pcap parser) | ✅ complete (dry-run default) |
| Analysis + repeatability + plotting | ✅ complete |
| Experiment runner scripts (×4) | ✅ complete |
| Bill of materials, topology, safety notes | ✅ complete |
| Documentation suite | ✅ complete |
| Paper support assets | ✅ complete |
| Unit tests + CI workflow | ✅ complete |
| Demo verified end-to-end | ✅ verified |

## 3. Case studies

1. **Wi-Fi** — packet capture & latency observability (owned lab network).
2. **BLE / IIoT** — sensor telemetry periodicity & gateway logging.
3. **IEEE 802.15.4 / Zigbee** — low-power constrained sensing.
4. **LoRa / Sub-GHz / SDR** — receive-only spectrum/traffic observability.

Each ships a config, runner script, and produces metrics + figures.

## 4. Parameter summary (conservative defaults)

| Case | Nodes | Sizes (B) | Interval (ms) | Duration (s) | Reps |
|------|-------|-----------|---------------|--------------|------|
| 1 | 4 | 128/256/512 | 20/50/100 | 60 | 5 |
| 2 | 4 | 20/32/64 | 250/500/1000 | 120 | 5 |
| 3 | 5 | 32/64/96 | 500/1000/2000 | 180 | 5 |
| 4 | 3 | 12/24/51 | 1000/5000/10000 | 300 | 3 |

## 5. Validation plan (minimal, fitness-for-purpose)

- **Demo determinism:** identical seed → identical `packets.csv` (hash-checked).
- **Repeatability:** mean/std of key metrics across repetitions.
- **Sanity bounds:** inter-arrival mean ≈ configured interval; completeness in
  (0,1]; per-node counts balanced for symmetric configs.
- **Pipeline integrity:** every run emits a `manifest.json`.

These validate **fitness for purpose** (the testbed faithfully measures what it
claims), not certification-grade wireless performance.

## 6. Non-burning policy (firewall)

The artifact **must not**:
- implement a full cooldown-on-failure scheduler;
- implement/reproduce the analytical models (π_on(Δ), p_loss^(K)(T_cd), χ);
- run the full ns-3 campaign or reproduce S4/S8/S9 comparative results;
- ship a dataset that reconstructs the main scheduler paper;
- claim full IEEE 802.11ax PHY/MAC validation;
- claim deployment-ready anti-jamming/safety/SIL/PROFIsafe protection.

Advanced scheduling may appear **only** as future work / external motivation.

## 7. Next implementation steps

1. Add real-hardware capture notes per lab (fill `hardware/setup_photos_placeholder/`).
2. Produce architecture/pipeline diagrams (F1–F2) for the paper.
3. Tag a `v0.1.0` release and mint a DOI (e.g. Zenodo).
4. Expand tests with golden-hash fixtures for each case study.
5. Draft the paper sections using `docs/hardware_paper_outline.md`.
