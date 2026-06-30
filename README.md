# Open-Source Instrumentation for Reproducible Industrial Wireless Packet Observability

[![Reproducibility CI](https://img.shields.io/badge/CI-reproducibility-blue)](.github/workflows/reproducibility.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey)](LICENSE)

An open-source **instrumentation and reproducibility workflow** for packet-level
observability in educational cyber–physical laboratories. It accompanies the
paper *Open-Source Instrumentation for Reproducible Industrial Wireless Packet
Observability in Educational Cyber–Physical Laboratories* and is intended as a
public, reviewable, reusable scientific artifact in the style of open scientific
hardware/software documentation.

## Scope

The repository provides a configuration-driven, **software-only synthetic demo
mode**: from YAML configurations it generates deterministic synthetic packet
traces, computes packet-level metrics, produces figures, and writes per-run
manifests with SHA-256 hashes. It also ships documentation and optional notes
for extending to owned-device and receive-only observation. Concretely it
includes synthetic demo-mode traces, YAML configurations, metrics, figures,
manifests, hashes, documentation, and optional hardware notes.

## Non-goals

> - This is **not** an anti-jamming tool.
> - This is **not** an offensive cybersecurity framework (no jamming, flooding,
>   deauthentication, exploitation, or unauthorised scanning).
> - This is **not** a wireless scheduler.
> - This is **not** a full implementation or validation of Wi-Fi, BLE,
>   IEEE 802.15.4, Zigbee, LoRa, or SDR systems; the case studies are
>   technology-like profiles, **not** standard-conformant implementations.
> - Synthetic demo-mode outputs are **not** real radio measurements.

See [`docs/limitations_and_non_goals.md`](docs/limitations_and_non_goals.md).

## Quickstart

```bash
# 1. Clone
git clone <repository-url>
cd industrial-wireless-open-testbed

# 2. Create an environment
python -m venv .venv && source .venv/bin/activate     # or: conda env create -f environment.yml

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Run the synthetic demo (all four case studies)
python scripts/run_demo.py --all

# 5. Compute metrics / generate figures for a single case (also done by run_demo)
python scripts/compute_metrics.py --input results/demo/wifi_like/packets.csv
python scripts/plot_results.py   --input results/demo/wifi_like/packets.csv --out-dir results/demo/wifi_like/figures

# 6. Verify reproducibility
python scripts/verify_reproducibility.py --all
```

See [`docs/quickstart.md`](docs/quickstart.md) for a guided walkthrough.

## Repository structure

```
.
├── configs/        # one technology-like YAML profile per case study
├── src/
│   └── packet_observability/   # core library (generator, metrics, plotting, manifest, hashing, io)
│       └── extensions/         # optional owned-device / receive-only tools
├── scripts/        # thin command-line entry points
├── data/
│   └── synthetic_demo/         # canonical, versioned synthetic traces (one per case)
├── results/        # regenerated metrics, figures, manifests (not version-controlled)
├── hardware/       # optional hardware extension notes (BOM, adoption tiers, safety)
├── docs/           # overview, quickstart, reproducibility, schema, metrics, limits, ethics
├── tests/          # determinism, metrics, manifest hashes, configs, terminology guard
├── archive/        # superseded legacy material kept for traceability
└── .github/workflows/reproducibility.yml   # hardware-free CI
```

## Case studies

Four **technology-like** profiles over one common toolchain (not
standard-conformant; see [`docs/case_studies.md`](docs/case_studies.md)):

- **Wi-Fi-like** — packet observability of short-range benign traffic.
- **BLE/IIoT-like** — low-rate telemetry periodicity and gateway logging.
- **IEEE 802.15.4/Zigbee-like** — low-power, constrained-payload sensing.
- **LoRa/Sub-GHz/SDR-like** — long-range event logging; optional receive-only SDR.

## Reproducibility

Generation is driven by a fixed seed per config. Each run writes a `manifest.json`
recording the config, seed, git commit, output files, and their SHA-256 hashes,
producing CSV traces that regenerate deterministically. The committed traces in
`data/synthetic_demo/` are canonical references that
`scripts/verify_reproducibility.py` checks for byte/hash consistency. See
[`docs/reproducibility_protocol.md`](docs/reproducibility_protocol.md).

## Safety and ethics

Safe by design:

- synthetic mode emits no RF signal and touches no network interface;
- the optional receive-only SDR extension only observes;
- owned-device observation applies only in authorised, controlled environments;
- there is no jamming, flooding, deauthentication, exploitation, or unauthorised
  scanning.

See [`docs/safety_and_ethics.md`](docs/safety_and_ethics.md), [`SECURITY.md`](SECURITY.md),
and [`hardware/safety_notes.md`](hardware/safety_notes.md).

## Documentation

- [Overview](docs/overview.md)
- [Quickstart](docs/quickstart.md)
- [Reproducibility protocol](docs/reproducibility_protocol.md)
- [Case studies](docs/case_studies.md)
- [Packet schema](docs/packet_schema.md)
- [Metrics](docs/metrics.md)
- [Limitations and non-goals](docs/limitations_and_non_goals.md)
- [Safety and ethics](docs/safety_and_ethics.md)
- [Reviewer checklist](docs/reviewer_checklist.md)
- [Paper alignment (C1–C6)](docs/paper_alignment.md)

## Citation

If you use this artifact, please cite it. A placeholder entry is provided in
[`CITATION.cff`](CITATION.cff); replace the author and DOI fields before
publication.

## License

- **Code:** MIT (see [`LICENSE`](LICENSE)).
- **Documentation, figures, and synthetic data:** Creative Commons Attribution
  4.0 International (CC BY 4.0).
