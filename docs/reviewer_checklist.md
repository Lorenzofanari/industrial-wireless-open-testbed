# Reviewer checklist

A short checklist for artifact reviewers. The whole sequence runs software-only
on a commodity machine in a few minutes and needs no radio hardware.

## Installation

- [ ] The repository clones cleanly.
- [ ] Dependencies install via `pip install -r requirements.txt` (or
      `pip install -e ".[dev]"`, or `conda env create -f environment.yml`).

## Synthetic demo

- [ ] `python scripts/run_demo.py --all` completes without error.
- [ ] A single case runs: `python scripts/run_demo.py --config configs/wifi_like.yaml --out results/demo/wifi_like`.

## Generated artefacts

- [ ] `packets.csv` files are generated for each case.
- [ ] Metrics are regenerated (`metrics.csv`, `metrics_summary.json`).
- [ ] Figures are regenerated (`figures/*.png`).
- [ ] Manifests are produced (`manifest.json`) with SHA-256 hashes of outputs.

## Reproducibility

- [ ] `python scripts/verify_reproducibility.py --all` reports PASS.
- [ ] Generated traces match the committed references in `data/synthetic_demo/`.

## Tests

- [ ] `pytest` passes.

## Scope and safety

- [ ] Non-goals are clearly stated (`docs/limitations_and_non_goals.md`).
- [ ] Safety and ethics policy is present (`docs/safety_and_ethics.md`).
- [ ] No offensive wireless functionality is present (no jamming, flooding,
      deauthentication, exploitation, or unauthorised scanning).
- [ ] The repository structure is unambiguous and understandable quickly.

## Paper alignment

- [ ] Contributions C1–C6 map to repository evidence
      (`docs/paper_alignment.md`).
