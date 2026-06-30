# Design files checklist

In MDPI *Hardware* terms, the "design files" of this artifact are its
**human-editable source files**: the code, configurations, documentation, and
data references from which the whole artifact can be rebuilt. Because the
artifact is software-only at its core (Tier 0), the design files are text-based
and fully open.

## What counts as a design/source file

| Category | Files | Role |
|----------|-------|------|
| Core source code | `src/packet_observability/*.py` | The generator, metrics, plotting, manifest, hashing, and I/O logic. |
| Optional extensions | `src/packet_observability/extensions/*.py` | Owned-device / receive-only tooling (optional tiers). |
| Entry points | `scripts/*.py` | Thin command-line wrappers around the library. |
| Configurations | `configs/*.yaml` | Technology-like case-study profiles (the experiment "design"). |
| Reference data | `data/synthetic_demo/*/packets.csv` | Canonical, regenerable synthetic traces. |
| Build/packaging | `requirements.txt`, `pyproject.toml`, `environment.yml` | Reproducible environment definitions. |
| Documentation | `docs/*.md`, `hardware/*.md`, `hardware/bill_of_materials.csv` | Build, operating, design, validation, and safety documentation. |
| Tests / CI | `tests/*.py`, `.github/workflows/reproducibility.yml` | Verification of the design. |

## Why the files are editable

All design files are plain text (Python, YAML, CSV, Markdown, TOML). They can be
opened, read, modified, and re-run with standard open-source tooling, with no
proprietary formats. This makes the artifact inspectable and adaptable for
teaching and reuse.

## How the artifact can be rebuilt

From a clean clone, the entire artifact is rebuilt with:

```bash
python -m pip install -r requirements.txt
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

See [`build_instructions.md`](build_instructions.md) for the full procedure and
[`reproducibility_expected_outputs.md`](reproducibility_expected_outputs.md) for
the files this produces.

## How design integrity is maintained

- **Manifests.** Every run writes `manifest.json` recording config, seed, git
  commit, and outputs.
- **SHA-256 hashes.** Each manifest records the hash of every output file.
- **Git versioning.** All design files are version-controlled; releases are
  tagged.
- **Tests.** `tests/*.py` check determinism, metrics, manifest fields/hashes,
  config validity, and terminology safety.
- **CI.** `.github/workflows/reproducibility.yml` re-runs the workflow on every
  push/PR with no radio hardware.

See [`design_integrity_statement.md`](design_integrity_statement.md) for the
consolidated statement.
