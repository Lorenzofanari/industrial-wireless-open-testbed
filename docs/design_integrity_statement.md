# Design integrity statement

This statement summarises how the integrity and reproducibility of the artifact's
design are maintained.

## Editable source files

All design files are open, plain-text, and editable with standard tooling:
Python (`src/`, `scripts/`, `tests/`), YAML configurations (`configs/`), CSV
reference data (`data/synthetic_demo/`), environment definitions
(`requirements.txt`, `pyproject.toml`, `environment.yml`), and Markdown/CSV
documentation (`docs/`, `hardware/`). See
[`design_files_checklist.md`](design_files_checklist.md).

## Versioned repository

The artifact is tracked in Git. Releases are tagged (`v0.1.0` archived
baseline, `v0.1.1` corrected release) and archived for citation (see
[`../RELEASE_CHECKLIST.md`](../RELEASE_CHECKLIST.md) and
[`../CHANGELOG.md`](../CHANGELOG.md)). Tags are never moved or re-created.

## SHA-256 hashes in manifests

Each run writes a `manifest.json` that records the configuration, the seed, the
git commit (when available), the tool version, the environment, and an `outputs`
list in which every produced file is accompanied by its SHA-256 digest. This
allows any artefact to be tied back to the exact inputs that produced it.

## Reproducibility commands

```bash
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

`verify_reproducibility.py` confirms that traces regenerate identically (by
SHA-256) and match the committed canonical references in `data/synthetic_demo/`.
See [`reproducibility_protocol.md`](reproducibility_protocol.md).

## Licensing

Code is licensed under the MIT License; documentation, figures, and synthetic
data are offered under CC BY 4.0. See [`../LICENSE`](../LICENSE).

## Safety boundaries

The synthetic demo mode emits no RF signal and touches no network interface.
Optional extensions are passive / receive-only and default to a dry-run. See
[`safety_and_ethics.md`](safety_and_ethics.md) and
[`../hardware/safety_notes.md`](../hardware/safety_notes.md).

## Release checklist

Release, archival, and DOI steps are tracked in
[`../RELEASE_CHECKLIST.md`](../RELEASE_CHECKLIST.md).
