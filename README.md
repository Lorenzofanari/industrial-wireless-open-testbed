# An Open-Source Educational Artifact for Wireless Packet Observability in Cyber–Physical Laboratories

[![Reproducibility CI](https://img.shields.io/badge/CI-reproducibility-blue)](.github/workflows/reproducibility.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey)](LICENSE)

## Summary

This repository is an open-source **educational hardware/software artifact** for
teaching reproducible wireless packet observability in cyber–physical
laboratories. From human-editable YAML profiles it generates deterministic
**synthetic** packet traces, computes packet-level metrics, produces figures, and
writes per-run manifests with SHA-256 hashes — entirely software-only, with no
radio hardware. It accompanies the MDPI *Hardware* paper of the same title and is
intended for public release and Supplementary Material.

## What this artifact teaches

- Configuring a wireless traffic profile with YAML.
- Generating a reproducible synthetic packet trace.
- Computing and interpreting packet-observability metrics (rate, inter-arrival,
  jitter proxy, missing/duplicate sequence ids, completeness).
- Documenting configuration, results, manifests, and hashes.
- Understanding why synthetic traces do not prove real radio performance.
- Extending cautiously to owned-device or receive-only observation.

See [`docs/learning_objectives.md`](docs/learning_objectives.md).

## Quickstart

```bash
git clone https://github.com/Lorenzofanari/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

See [`docs/quickstart.md`](docs/quickstart.md) and
[`docs/build_instructions.md`](docs/build_instructions.md).

## Repository structure

```
.
├── configs/        # one technology-like YAML profile per case study
├── src/packet_observability/   # core library (+ optional extensions/)
├── scripts/        # thin command-line entry points
├── data/synthetic_demo/        # canonical, versioned synthetic traces
├── results/        # regenerated metrics/figures/manifests (git-ignored)
├── hardware/       # optional hardware tier notes (topology, BOM, safety)
├── docs/           # build, operating, educational, validation, design docs
├── tests/          # determinism, metrics, manifests, configs, terminology guard
└── .github/workflows/reproducibility.yml   # hardware-free CI
```

## Case-study profiles

Four **technology-like** profiles over one common toolchain (not
standard-conformant; see [`docs/case_studies.md`](docs/case_studies.md)):

- **Wi-Fi-like** — packet observability of short-range benign traffic.
- **BLE/IIoT-like** — low-rate telemetry periodicity and gateway logging.
- **IEEE 802.15.4/Zigbee-like** — low-power, constrained-payload sensing.
- **LoRa/Sub-GHz/SDR-like** — long-range event logging; optional receive-only SDR.

## Build tiers

- **Tier 0 — software-only:** needs no radio hardware; this is the default.
- **Tiers 1–4 — optional:** owned-device Wi-Fi observation, BLE / IEEE 802.15.4
  teaching bench, receive-only SDR, and contained RF. All optional tiers are
  owned-device or receive-only. See
  [`docs/build_instructions.md`](docs/build_instructions.md) and
  [`hardware/adoption_tiers.md`](hardware/adoption_tiers.md).

## Operating instructions

A 90–120 minute teaching session: select a profile, inspect the YAML, generate a
trace, compute metrics, inspect figures and manifests, compare profiles, and
submit deliverables. See [`docs/operating_instructions.md`](docs/operating_instructions.md),
[`docs/lab_activity_plan.md`](docs/lab_activity_plan.md),
[`docs/student_worksheet.md`](docs/student_worksheet.md),
[`docs/instructor_guide.md`](docs/instructor_guide.md), and
[`docs/assessment_rubric.md`](docs/assessment_rubric.md).

## Reproducibility

Generation is seeded per config. Each run writes a `manifest.json` with config,
seed, git commit, and SHA-256 hashes of all outputs. The committed traces in
`data/synthetic_demo/` are canonical references checked by
`scripts/verify_reproducibility.py`. See
[`docs/reproducibility_protocol.md`](docs/reproducibility_protocol.md),
[`docs/validation_walkthrough.md`](docs/validation_walkthrough.md), and
[`docs/reproducibility_expected_outputs.md`](docs/reproducibility_expected_outputs.md).

Synthetic demo-mode outputs are not real measurements; this is a teaching
artifact.

## Safety and ethics

Safe by design: synthetic mode emits no RF signal and touches no network
interface; optional extensions are passive / receive-only and default to a
dry-run; owned-device observation applies only in authorised, controlled
environments. The artifact provides no jamming, flooding, deauthentication,
exploitation, or unauthorised scanning. See
[`docs/safety_and_ethics.md`](docs/safety_and_ethics.md),
[`SECURITY.md`](SECURITY.md), and [`hardware/safety_notes.md`](hardware/safety_notes.md).

This artifact does not implement wireless algorithms, interference mitigation,
offensive cybersecurity functionality, or radio-standard validation; its purpose
is to teach reproducible packet-observability workflows
([`claims_included.md`](claims_included.md), [`claims_excluded.md`](claims_excluded.md),
[`docs/limitations_and_non_goals.md`](docs/limitations_and_non_goals.md)).

## Supplementary materials

The Supplementary Material set and the release/DOI procedure are listed in
[`SUPPLEMENTARY_MATERIALS_CHECKLIST.md`](SUPPLEMENTARY_MATERIALS_CHECKLIST.md) and
[`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).

## Citation

If you use this artifact, please cite it (Lorenzo Fanari, Patxi Galán, Ángel
Monteagudo). Metadata is in [`CITATION.cff`](CITATION.cff); the archival DOI will
be added after the Zenodo release.

## License

- **Code:** MIT (see [`LICENSE`](LICENSE)).
- **Documentation, figures, and synthetic data:** CC BY 4.0.
