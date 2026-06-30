# `results/` — regenerated outputs

This directory holds outputs **regenerated** by the workflow. Its contents are
not version-controlled (see `.gitignore`); only this README and the
subdirectory placeholders are tracked, so that a clean clone can recreate
everything from `configs/` and `data/`.

## Layout

```
results/
├── demo/<case>/        # full per-case run: packets.csv, metrics, figures, manifest
├── metrics/            # aggregated metrics_summary.json per case
├── figures/<case>/     # aggregated PNG figures per case
└── manifests/          # aggregated per-run manifest.json per case
```

## How it is produced

```bash
python scripts/run_demo.py --all
```

`run_demo.py` writes the complete output for each case under `results/demo/<case>/`
and copies the canonical artefacts (metrics summary, figures, manifest) into
`results/metrics/`, `results/figures/`, and `results/manifests/`.

Every run also writes a `manifest.json` recording the config, seed, git commit
(when available), output files, and their SHA-256 hashes, so a reviewer can
audit exactly how each artefact was produced. See
[`../docs/reproducibility_protocol.md`](../docs/reproducibility_protocol.md).

All outputs here are synthetic demo-mode artefacts, not real radio measurements.
