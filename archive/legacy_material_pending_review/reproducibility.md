# Reproducibility Guide & Checklist

This artifact is designed so that a third party can reproduce demo results
exactly and real-hardware results within stated tolerances.

## How reproducibility is achieved

- **Deterministic demo data.** The synthetic generator is seeded
  (`random_seed` in each config, overridable with `--seed`). Same seed →
  identical `packets.csv`.
- **Per-run manifests.** Every run writes `manifest.json` containing the config,
  mode, safety mode, seeds, output file SHA-256 hashes, tool version, and
  Python/OS environment.
- **Pinned dependencies.** `requirements.txt` / `pyproject.toml` set conservative
  lower bounds; the toolkit relies only on `numpy`, `pandas`, `matplotlib`,
  `PyYAML`.
- **Headless plotting.** Matplotlib uses the `Agg` backend with default styling
  for stable, environment-independent figures.
- **Repeatability reports.** `repeatability_report.py` aggregates metrics across
  repetitions and reports mean/std/min/max.

## Reproduce the demo end-to-end

```bash
python -m pip install -r requirements.txt
bash experiments/run_case_wifi_latency.sh 5
```

Compare your `results/case_wifi_latency/run01/metrics_summary.json` against a
reference run. With identical seed and dependency versions, scalar metrics match.

## Reproducibility checklist

- [ ] Dependency versions recorded (`pip freeze > results/<exp>/pip-freeze.txt`).
- [ ] `random_seed` documented (config + manifest).
- [ ] `manifest.json` present for every run.
- [ ] Output hashes recorded in each manifest.
- [ ] Repeatability report generated across all repetitions.
- [ ] Hardware variant documented (`hardware/topology.md` + photos).
- [ ] `safety_mode` matches the actual experiment.
- [ ] Raw captures archived separately (not committed).
- [ ] Figures regenerated from committed CSVs (no manual edits).
- [ ] README/quickstart commands verified on a clean environment.

## Notes on real-hardware reproducibility

Over-the-air results vary with environment (multipath, interference, device
firmware). For real runs:
- prefer cabled/attenuated/shielded setups to reduce variance;
- report mean ± std across repetitions rather than single runs;
- record the exact hardware (model, firmware) in the manifest `extra` field.

> Honesty note: real wireless measurements are **observability demonstrations**,
> not certification-grade validation. See [`limitations.md`](limitations.md).
