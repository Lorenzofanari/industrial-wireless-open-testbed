# Hardware Paper Support Tables

Ready-to-adapt tables for the MDPI *Hardware*-style artifact paper. All claims
are framed as **observability / educational fitness-for-purpose**, never as
certification.

---

## T1 — Contribution table

| # | Contribution | Evidence in repository |
|---|--------------|------------------------|
| C1 | Open-source, safe-by-design multi-technology wireless **observability** testbed | `src/`, `configs/`, `hardware/` |
| C2 | **Software-only demo mode** enabling reproducible teaching without hardware | `src/capture/synthetic_capture_generator.py` |
| C3 | Unified **capture → metrics → figures** pipeline with manifests | `src/analysis/`, `src/utils/experiment_manifest.py` |
| C4 | **Four case studies** spanning Wi-Fi, BLE, 802.15.4, LoRa/SDR | `configs/`, `experiments/` |
| C5 | **Reproducibility package** (seeds, hashes, checklist, CI) | `docs/reproducibility.md`, `.github/workflows/ci.yml` |
| C6 | **Safety/legal firewall** (no jamming/attacks; rx-only SDR; dry-run defaults) | `hardware/safety_notes.md`, `docs/limitations.md` |

---

## T2 — Case study matrix

| Case | Technology | Industrial motivation | HW (optional) | Key metrics | Duration | Reps | Safety mode |
|------|-----------|-----------------------|---------------|-------------|----------|------|-------------|
| 1 | Wi-Fi | Plant Wi-Fi latency/observability | monitor-mode adapter | rate, inter-arrival, jitter proxy, missing seq | 60 s | 5 | owned_lab_network_only |
| 2 | BLE/IIoT | Low-rate sensor telemetry health | BLE dongle | periodicity, missing samples, per-sensor count | 120 s | 5 | synthetic_or_owned_devices_only |
| 3 | IEEE 802.15.4/Zigbee | Constrained low-power sensing | 802.15.4 sniffer | low-rate observability, inter-arrival, repeatability | 180 s | 5 | synthetic_or_owned_testbed_only |
| 4 | LoRa/Sub-GHz/SDR | Long-range telemetry & occupancy | RTL-SDR (rx only) | event count, occupancy proxy, periodicity | 300 s | 3 | receive_only_or_synthetic_only |

---

## T3 — Bill of materials summary

| Tier | Items | Indicative cost (EUR) |
|------|-------|-----------------------|
| Minimal (demo) | Existing PC + Python | 0 |
| Basic capture | + Wi-Fi monitor adapter, cables, USB hub | ~50 |
| Multi-tech | + Raspberry Pi, BLE dongle, 802.15.4 dongle | ~150 |
| SDR rx | + RTL-SDR + sub-GHz antenna | ~40 |
| Contained RF | + attenuators / shielded box | ~170 |

Full detail: [`../hardware/bill_of_materials.csv`](../hardware/bill_of_materials.csv).

---

## T4 — Validation metrics table

| Metric | Definition | Fitness criterion (demo) |
|--------|------------|--------------------------|
| total_packets | count of records | > 0, matches expected steps×nodes − drops |
| packet_rate_pps | packets / duration | within expected band for configured interval |
| inter_arrival_mean_ms | mean Δt between packets | ≈ interval/nodes (ordering across nodes) |
| jitter_proxy_ms | std of inter-arrival | small and stable across runs |
| capture_completeness | unique seq / expected span | in (0, 1]; ≈ (1 − drop_probability) |
| missing_sequence_ids | gaps in per-node seq | ≈ expected from synthetic drop knob |
| duplicate_sequence_ids | repeats in per-node seq | 0 in demo |
| repeatability (mean ± std) | across repetitions | low relative std for rate/size |

> These confirm the **instrument measures what it claims**; they are **not**
> certification-grade wireless performance results.

---

## T5 — Non-goals / scope firewall table

| Forbidden in this artifact | Status |
|----------------------------|--------|
| Full cooldown-on-failure scheduler | ❌ not implemented |
| Analytical models π_on(Δ), p_loss^(K)(T_cd), χ | ❌ not implemented |
| Full ns-3 campaign | ❌ not included |
| Complete S4/S8/S9 comparative results | ❌ not included |
| Dataset reconstructing the main scheduler paper | ❌ not provided |
| Full IEEE 802.11ax PHY/MAC validation claim | ❌ not claimed |
| Anti-jamming / SIL / PROFIsafe / certified protection | ❌ not claimed |
| Advanced scheduling | ⚠️ future work / external motivation only |

---

## T6 — Reproducibility checklist (summary)

See [`../docs/reproducibility.md`](../docs/reproducibility.md) for the full list.

- [ ] Seeds documented; manifests present; output hashes recorded.
- [ ] Dependencies pinned; `pip freeze` archived.
- [ ] Repeatability report generated.
- [ ] Hardware variant + safety mode documented.
- [ ] Figures regenerated from committed CSVs.
