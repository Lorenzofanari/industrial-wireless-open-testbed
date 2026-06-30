# Reproducibility: expected outputs

This document describes what `python scripts/run_demo.py --all` produces and how
`python scripts/verify_reproducibility.py --all` interprets the result.

## Files that should be generated

Per case (`wifi_like`, `ble_like`, `ieee802154_like`, `lora_sdr_like`) under
`results/demo/<case>/`:

| File | Description |
|------|-------------|
| `packets.csv` | Canonical synthetic packet trace. |
| `metrics.csv` | Scalar metrics in long form. |
| `metrics_summary.json` | Structured metrics summary (incl. per-node counts). |
| `inter_arrival.csv` | Per-packet inter-arrival series. |
| `manifest.json` | Config, seed, git commit, environment, and output hashes. |
| `figures/*.png` | Four figures (count-over-time, inter-arrival, size, per-node). |

Aggregated copies:

| Path | Description |
|------|-------------|
| `results/metrics/<case>.json` | Copy of each case's metrics summary. |
| `results/figures/<case>/*.png` | Copy of each case's figures. |
| `results/manifests/<case>.json` | Copy of each case's manifest. |

> The `results/` directory is git-ignored (except its README and `.gitkeep`
> placeholders); reviewers regenerate it.

## How hashes are checked

- Each `manifest.json` records the SHA-256 of every output file.
- `verify_reproducibility.py` regenerates each trace twice and compares digests
  (determinism), then compares the fresh digest to the committed canonical
  reference in `data/synthetic_demo/<case>/packets.csv` (regression).

## How to interpret PASS / FAIL

- **PASS** — every checked trace is deterministic (same seed → same SHA-256) and
  matches its committed reference. This is the expected result on an unmodified
  clone, and it is what CI enforces.
- **FAIL** — a trace was non-deterministic, or it diverged from its reference.
  This usually means the generator, a config, or a seed changed. If the change
  was intentional, regenerate the reference
  (`scripts/generate_traces.py --config configs/<case>.yaml --out data/synthetic_demo/<case>/packets.csv`)
  and document it; otherwise revert the local change.
