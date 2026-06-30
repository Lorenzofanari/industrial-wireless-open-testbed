# Paper alignment

This table maps the paper's contributions (C1–C6) to concrete evidence in the
repository, so a reviewer can locate the support for each claim quickly.

| ID | Contribution | Repository evidence |
|----|--------------|---------------------|
| **C1** | Safe-by-design wireless packet-observability workflow. | `src/packet_observability/` (synthetic generator, metrics, plotting, manifest, hashing, I/O); default-safe extensions in `src/packet_observability/extensions/`; `docs/safety_and_ethics.md`; `hardware/safety_notes.md`. |
| **C2** | Tiered adoption from software-only to owned-device and receive-only extensions. | `hardware/adoption_tiers.md`; `hardware/bill_of_materials.md`; `hardware/owned_devices_notes.md`; `hardware/receive_only_sdr_notes.md`; `src/packet_observability/extensions/`. |
| **C3** | Software-only demonstration mode (no radio hardware), suitable for teaching, artifact checking, and CI. | `scripts/run_demo.py`, `scripts/generate_traces.py`; `configs/*.yaml`; `data/synthetic_demo/`; `.github/workflows/reproducibility.yml`. |
| **C4** | Unified capture-to-metrics-to-figures workflow with per-run manifests. | `scripts/run_demo.py`; `src/packet_observability/metrics.py`, `plotting.py`, `manifest.py`; `results/` layout; `docs/reproducibility_protocol.md`. |
| **C5** | Four technology-like case-study profiles (Wi-Fi-like, BLE/IIoT-like, IEEE 802.15.4/Zigbee-like, LoRa/Sub-GHz/SDR receive-only). | `configs/wifi_like.yaml`, `ble_like.yaml`, `ieee802154_like.yaml`, `lora_sdr_like.yaml`; `docs/case_studies.md`; `data/synthetic_demo/<case>/`. |
| **C6** | Explicit scope and safety boundaries (educational artifact; no offensive functionality, interference mitigation, wireless algorithms, or standard validation). | `docs/limitations_and_non_goals.md`; `claims_included.md`; `claims_excluded.md`; `docs/safety_and_ethics.md`; `SECURITY.md`; `tests/test_no_unsafe_terminology.py`. |

## How to verify the mapping

- Reproduce the artefacts: `python scripts/run_demo.py --all` (C3, C4, C5).
- Confirm determinism: `python scripts/verify_reproducibility.py --all` (C4).
- Run the guardrail tests: `pytest tests/test_no_unsafe_terminology.py` (C6).
- Read the scope statement: `docs/limitations_and_non_goals.md` (C6).

Synthetic demo-mode outputs are not real radio measurements; see
[`limitations_and_non_goals.md`](limitations_and_non_goals.md).
