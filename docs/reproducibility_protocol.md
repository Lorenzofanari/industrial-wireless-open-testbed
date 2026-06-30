# Reproducibility protocol

This artifact is designed so that a third party can regenerate every synthetic
demo-mode output exactly from a clean clone.

## The reproducible unit

Each synthetic demo-mode run is defined by:

| Element | Where it lives |
|---------|----------------|
| **YAML config** | `configs/<case>.yaml` (case name, seed, sizes, intervals, duration, repetitions, node count, missing-sample model, output naming). |
| **Seed** | `random_seed` in the config, overridable with `--seed`. |
| **Script / code version** | recorded as the git commit in the manifest (when available) plus the package `tool_version`. |
| **Generated trace** | `packets.csv` (canonical schema, see [`packet_schema.md`](packet_schema.md)). |
| **Metrics** | `metrics.csv` + `metrics_summary.json` (see [`metrics.md`](metrics.md)). |
| **Figures** | `figures/*.png`. |
| **Manifest** | `manifest.json`. |
| **Hashes** | SHA-256 of every output file, embedded in the manifest. |

## How determinism is achieved

- **Seeded generation.** The synthetic generator uses a single seeded
  `random.Random`. Same code + same config + same seed → byte-identical
  `packets.csv`.
- **Pinned dependencies.** `requirements.txt`, `pyproject.toml`, and
  `environment.yml` set conservative lower bounds on `numpy`, `pandas`,
  `matplotlib`, and `PyYAML`.
- **Headless plotting.** Matplotlib uses the `Agg` backend with default styling
  for environment-independent figures.

## The manifest

Every run writes `manifest.json` containing the schema id, experiment id, UTC
timestamp, mode, safety mode, tool version, git commit, config path, seed, the
Python/OS environment, the full config, and an `outputs` list where each entry
records the file name, size, and SHA-256 digest.

## Canonical references and verification

The committed traces under `data/synthetic_demo/<case>/packets.csv` are the
canonical references. `scripts/verify_reproducibility.py` performs two checks per
case study:

1. **Determinism** — generating the trace twice yields the same SHA-256.
2. **Regression** — the freshly generated trace matches the committed reference.

```bash
python scripts/verify_reproducibility.py --all
```

A non-zero exit code indicates a divergence, which is why this command runs in
continuous integration.

## Recommended command sequence

```bash
python scripts/run_demo.py --config configs/wifi_like.yaml        --out results/demo/wifi_like
python scripts/run_demo.py --config configs/ble_like.yaml         --out results/demo/ble_like
python scripts/run_demo.py --config configs/ieee802154_like.yaml  --out results/demo/ieee802154_like
python scripts/run_demo.py --config configs/lora_sdr_like.yaml    --out results/demo/lora_sdr_like
# or all at once:
python scripts/run_demo.py --all
# then verify:
python scripts/verify_reproducibility.py --all
```

## Honesty note

Reproducibility here means the **software pipeline** is regenerated exactly. It
is not a claim about real radio measurements; synthetic demo-mode outputs are not
real measurements. See [`limitations_and_non_goals.md`](limitations_and_non_goals.md).
