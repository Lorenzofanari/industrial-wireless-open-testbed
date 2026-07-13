# Industrial Wireless Open Testbed

**An open-source educational workflow for reproducible wireless packet observability.**

[![Reproducibility CI](https://img.shields.io/badge/CI-reproducibility-blue)](.github/workflows/reproducibility.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey)](LICENSE)

This project lets you configure a wireless traffic profile, generate a
**synthetic** packet trace, and compute and visualise packet-observability
metrics — entirely in software, with no radio hardware. It is built for
teaching and learning reproducible measurement workflows, and it extends
optionally and safely to owned-device or receive-only observation.

- **What it is:** a software-only workflow for generating and analysing synthetic
  packet traces, with reproducible, hash-verified outputs.
- **Who it is for:** instructors, students, early-stage researchers, and artifact
  reviewers.
- **What it needs:** Python 3.9+. No radio hardware for the default (Tier 0) mode.

## Run it in 10 minutes

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

This generates, for each case study, a `packets.csv`, metrics, figures, and a
`manifest.json` with SHA-256 hashes under `results/demo/<case>/`. See
[`docs/quickstart.md`](docs/quickstart.md).

## Teach a lab with it

A self-contained 90–120 minute laboratory: students configure a profile,
generate a trace, compute metrics, inspect figures and manifests, compare
profiles, and write up their findings — no hardware required. Start with
[`docs/operating_instructions.md`](docs/operating_instructions.md) and the
[`docs/lab_activity_plan.md`](docs/lab_activity_plan.md). Documentation is indexed
in [`docs/README.md`](docs/README.md).

## What you can do with it

| Goal | Where to start |
|------|----------------|
| Reproduce the demo | [`docs/quickstart.md`](docs/quickstart.md) |
| Build it (software-only or optional hardware tiers) | [`docs/build_instructions.md`](docs/build_instructions.md) |
| Operate it in a lab session | [`docs/operating_instructions.md`](docs/operating_instructions.md) |
| Understand the metrics and data | [`docs/metrics.md`](docs/metrics.md), [`docs/packet_schema.md`](docs/packet_schema.md) |
| Check reproducibility | [`docs/validation_walkthrough.md`](docs/validation_walkthrough.md), [`docs/reproducibility_expected_outputs.md`](docs/reproducibility_expected_outputs.md) |
| Teach with it | [`docs/learning_objectives.md`](docs/learning_objectives.md), [`docs/instructor_guide.md`](docs/instructor_guide.md), [`docs/assessment_rubric.md`](docs/assessment_rubric.md) |

## Repository structure

```
configs/      one technology-like YAML profile per case study
src/packet_observability/   core library (+ optional extensions/)
scripts/      command-line entry points (run_demo, compute_metrics, ...)
data/synthetic_demo/        canonical, versioned synthetic traces
results/      regenerated metrics/figures/manifests (git-ignored)
hardware/     optional hardware tier notes (topology, BOM, safety)
docs/         quickstart, build, operating, teaching, validation docs
tests/        determinism, metrics, manifests, configs, terminology guard
```

## Case-study profiles

Four **technology-like** profiles over one common toolchain (not
standard-conformant; see [`docs/case_studies.md`](docs/case_studies.md)):
Wi-Fi-like, BLE/IIoT-like, IEEE 802.15.4/Zigbee-like, and LoRa/Sub-GHz/SDR-like.

## Build tiers

Tier 0 is software-only and is the default; it needs no radio hardware. Tiers
1–4 are optional educational extensions (owned-device Wi-Fi observation, a
BLE / IEEE 802.15.4 teaching bench, receive-only SDR, and contained RF). See
[`docs/build_instructions.md`](docs/build_instructions.md) and
[`hardware/adoption_tiers.md`](hardware/adoption_tiers.md).

## Reproducibility

Generation is seeded per config; each run writes a manifest with the config,
seed, git commit, and SHA-256 hashes of all outputs. The committed traces in
`data/synthetic_demo/` are canonical references checked by
`scripts/verify_reproducibility.py`. Synthetic demo-mode outputs verify the
software pipeline; they are not real radio measurements.

For manuscript reproduction, use the exact tagged release or commit reported in
the paper rather than the moving default branch.

## Safety

Safe by design: the default workflow is software-only and emits no RF; optional
extensions are passive or receive-only and are used only on equipment you own or
are authorised to use. Details are in
[`docs/safety_and_ethics.md`](docs/safety_and_ethics.md) and
[`hardware/safety_notes.md`](hardware/safety_notes.md); scope is summarised in
[`docs/limitations_and_non_goals.md`](docs/limitations_and_non_goals.md).

## Supplementary materials

The packaged Supplementary Material set and the release/DOI procedure are listed
in [`SUPPLEMENTARY_MATERIALS_CHECKLIST.md`](SUPPLEMENTARY_MATERIALS_CHECKLIST.md)
and [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).

## Related paper

This artifact accompanies the MDPI *Hardware* paper *An Open-Source Educational
Artifact for Wireless Packet Observability in Cyber–Physical Laboratories*
(Lorenzo Fanari, Patxi Galán, Ángel Monteagudo). The mapping from the paper to
the repository is documented in [`docs/paper_alignment.md`](docs/paper_alignment.md);
the repository is designed to be useful on its own, independent of the paper.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff).

The immutable archival DOI will be added after the `v0.1.0` GitHub release has
been deposited on Zenodo. Until then, cite the repository URL and the exact Git
commit used for the experiment.

## License

Code is under the MIT License ([`LICENSE`](LICENSE)); documentation, figures, and
synthetic data are under CC BY 4.0.
