# Industrial Wireless Open Testbed v0.1.1

Corrected release of the software-first educational artifact accompanying the
manuscript:

**An Open-Source Educational Artifact for Wireless Packet Observability in
Cyber–Physical Laboratories**

`v0.1.1` is the single, self-contained software state used for the revised
manuscript evaluation. It supersedes the combination "`v0.1.0` + supplementary
source patch"; no separate patch is needed. `v0.1.0` remains available and
unchanged as the archived baseline.

## What changed relative to v0.1.0

- **Equation (4) correction.** The finite-span event-rate estimator
  (`packet_rate_pps`) now uses the `N - 1` observed inter-event intervals
  delimited by `N` timestamps: `R_span = (N - 1) / (t_max - t_min)`.
  `v0.1.0` used `N / (t_max - t_min)`. One canonical function,
  `packet_observability.metrics.span_event_rate()`, is used by all callers.
- **Boundary behaviour.** The rate is undefined (`NaN`) for fewer than two
  usable timestamps or zero span.
- **Input validation.** Mandatory columns are checked, invalid timestamps are
  discarded, non-positive packet sizes are excluded, and a missing optional
  `sequence_id` column no longer raises.
- **Independent regression tests** (`tests/test_metrics_independent.py`) built
  from hand-written packet tables with analytically derived expected values,
  including missing/duplicate sequence ids, per-node timing and boundary cases.
- **W1–W4 terminology.** Reference workload profiles are labelled `W1`–`W4`
  in documentation and CLI output; configuration filenames are unchanged
  (`W1 → wifi_like.yaml`, `W2 → ble_like.yaml`, `W3 → ieee802154_like.yaml`,
  `W4 → lora_sdr_like.yaml`).

Full details: `CHANGELOG.md`.

## Reproduction

```bash
git clone https://github.com/Lorenzofanari/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
git checkout v0.1.1

python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

python -m pytest -v
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
```

## Scope

The default artifact is entirely software-only and generates synthetic packet
traces. It emits no radio signal and does not access a network interface. The
W1–W4 profiles demonstrate reproducible packet-observability workflows; they
are not standard-conformant implementations and do not validate the
performance of Wi-Fi, BLE, IEEE 802.15.4, Zigbee, LoRa, or SDR systems.
Optional hardware extensions are restricted to owned or authorised devices,
owned laboratory networks, and receive-only observation where legally
permitted.

## Licences

* Source code: MIT.
* Documentation, figures, tables, and synthetic datasets: CC BY 4.0.

## Citation

Citation metadata are available in `CITATION.cff`. Concept DOI:
10.5281/zenodo.21347261. The `v0.1.1` version DOI will be added to
`CITATION.cff` and the README after Zenodo has archived this GitHub release.
