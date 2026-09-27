# Changelog

All notable changes to this repository are documented here. Versions are Git
tags; each tag is archived on Zenodo under the concept DOI
[10.5281/zenodo.21347261](https://doi.org/10.5281/zenodo.21347261).

## v0.1.1

Corrected release consolidating the software state used for the revised
manuscript evaluation into a single public tag. `v0.1.0` remains available,
unchanged, as the archived baseline.

### Corrected

- Corrected the finite-span packet/event-rate estimator (`packet_rate_pps`,
  manuscript Equation (4)) to use the `N - 1` observed inter-event intervals
  represented by `N` timestamps:
  `R_span = (N - 1) / (t_max - t_min)` instead of `N / (t_max - t_min)`.
  The estimator now lives in one canonical function,
  `packet_observability.metrics.span_event_rate()`, used by every caller.
- Defined boundary behaviour for traces containing fewer than two usable
  observations or zero timestamp span: the rate is undefined and reported as
  `NaN` (the existing project convention for undefined metrics).
- Consistent input validation in `compute_metrics()`: mandatory `timestamp`,
  `node_id` and `packet_size_bytes` columns (`ValueError` otherwise); rows with
  missing, non-numeric or non-finite timestamps are discarded (`ValueError` if
  none remain); non-positive or non-numeric packet sizes are excluded from the
  size statistics; a missing optional `sequence_id` column yields `0` missing /
  duplicate ids and `NaN` completeness instead of a `KeyError`.

### Added

- `tests/test_metrics_independent.py`: independent regression tests based on
  manually constructed packet traces with analytically derived expected values
  (timestamps `[0.0, 0.5, 1.0]` → `2.0` packets/s, `500 ms` mean gap).
- Regression coverage for missing and duplicate sequence identifiers
  (`[1, 3, 3]` → 1 missing, 1 duplicate).
- Regression coverage for per-node timing metrics (0.1 s / 0.25 s spacing →
  `100 ms` / `250 ms` mean per-node gaps) via the new
  `per_node_inter_arrival_mean_ms` summary field.
- Additional boundary-input tests: empty trace, one-record trace, zero
  timestamp span, invalid timestamps, missing mandatory columns, non-positive
  packet sizes.
- `CHANGELOG.md` (this file) and `RELEASE_NOTES_v0.1.1.md`.

### Reproducibility

- Consolidated the software state used for the revised manuscript evaluation
  into a single tagged release (`v0.1.1`); no separate reviewer-only patch is
  required to reproduce it.
- Verified that the scripts in `scripts/` (`run_demo.py`, `compute_metrics.py`)
  use the corrected canonical metric implementation and that no duplicate
  `N / span` computation remains in the repository.
- Continuous integration (`.github/workflows/reproducibility.yml`) runs the
  full test suite (including the new independent tests) with `pytest -v`,
  executes the synthetic demo for all four profiles, and verifies trace
  reproducibility on Python 3.9, 3.11 and 3.12; it is now also triggered on
  `v*` tags and manually.

### Documentation

- Clarified the neutral W1–W4 workload terminology and its mapping to the
  unchanged configuration files (`W1 → wifi_like.yaml`, `W2 → ble_like.yaml`,
  `W3 → ieee802154_like.yaml`, `W4 → lora_sdr_like.yaml`); command-line tools
  print `W1 (wifi_like)`-style labels.
- Documented the corrected estimator, its boundary behaviour and the input
  validation rules in `docs/metrics.md`.
- Clarified the distinction between the original `v0.1.0` archived baseline and
  the corrected `v0.1.1` release in the README, quickstart and release
  checklist; recorded the existing `v0.1.0` Zenodo DOI and concept DOI.

### Unchanged

- Synthetic trace generation, canonical reference traces in
  `data/synthetic_demo/`, configuration files, manifests and figures are
  unchanged; `verify_reproducibility.py --all` continues to pass against the
  committed references.

## v0.1.0

Initial archival release (Zenodo DOI
[10.5281/zenodo.21347262](https://doi.org/10.5281/zenodo.21347262)). See
`RELEASE_NOTES_v0.1.0.md`. The packet-rate estimator in this release was
`N / (t_max - t_min)`.
