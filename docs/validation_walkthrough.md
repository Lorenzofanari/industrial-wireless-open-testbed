# Validation Walkthrough

## What validation means here

Validation verifies that the artifact supports the intended **teaching
workflow**: that it generates synthetic traces deterministically, computes the
documented metrics, produces figures, writes manifests, and reproduces
hash-consistent outputs.

It does **not** validate real radio performance, and it makes no
standard-conformance claim. Synthetic demo-mode outputs are not real
measurements.

## Synthetic demo-mode validation

The workflow is validated end-to-end:

- **Trace generation** — each config produces a deterministic `packets.csv`.
- **Metrics computation** — `metrics.csv` and `metrics_summary.json` are written.
- **Figure generation** — the standard four figures are written under `figures/`.
- **Manifest generation** — `manifest.json` records config, seed, git commit, and
  output hashes.
- **Hash reproducibility** — regeneration yields identical SHA-256 digests, which
  also match the committed references in `data/synthetic_demo/`.

## Commands

```bash
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

## Expected files

Per case under `results/demo/<case>/`:

- `packets.csv`
- `metrics.csv`
- `metrics_summary.json`
- `inter_arrival.csv`
- `manifest.json`
- `figures/packet_count_over_time.png`
- `figures/inter_arrival_distribution.png`
- `figures/packet_size_distribution.png`
- `figures/per_node_packet_count.png`

Aggregated copies are also placed under `results/metrics/<case>.json`,
`results/figures/<case>/`, and `results/manifests/<case>.json`. See
[`reproducibility_expected_outputs.md`](reproducibility_expected_outputs.md).

## Inter-arrival explanation

The global `inter_arrival_mean_ms` can differ from a config's per-node interval
because:

- multiple nodes are aggregated into one stream;
- timestamps are sorted globally before differencing;
- per-packet jitter is added around the nominal interval;
- the synthetic missing-sample model may omit some records;
- per-node sequence logic is separate from global packet ordering.

So with N nodes emitting at interval T, the globally-ordered inter-arrival mean
is approximately T/N, not T.

## Same seed vs different seed vs changed configuration

- **Same seed + same config + same code** → byte-identical traces (identical
  SHA-256).
- **Different seed** → similar statistical shape but not byte-identical.
- **Changed configuration** → intentionally different outputs; regenerate the
  canonical reference and document the change (see
  [`../CONTRIBUTING.md`](../CONTRIBUTING.md)).
