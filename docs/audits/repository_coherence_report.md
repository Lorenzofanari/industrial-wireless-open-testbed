# Repository coherence report

An internal report on the standalone-artifact coherence pass. The goal of this
pass was to give the repository a natural, repository-first identity that is
useful on its own, while keeping its support for the related paper accurate but
non-invasive.

## Repository-first identity statement

**Industrial Wireless Open Testbed** is an open-source educational workflow for
reproducible wireless packet observability. In its default mode it is
software-only: from a YAML profile it generates a deterministic synthetic packet
trace, computes packet-observability metrics, produces figures, and writes a
manifest with SHA-256 hashes. It serves instructors, students, early-stage
researchers, and artifact reviewers, and it extends optionally and safely to
owned-device or receive-only observation. It is useful without reading the
related paper.

## What changed

- `README.md` rewritten to lead with project identity (short H1
  "Industrial Wireless Open Testbed" + subtitle), a 10-minute quickstart, a
  practical "what you can do" table, and a concise safety paragraph. The long
  paper title moved into a "Related paper" section, and defensive exclusions
  were trimmed from the README (kept in the scope/safety docs).
- `docs/paper_alignment.md` restructured around the six Hardware sections as the
  single, non-invasive paper-to-repository mapping.
- `docs/overview.md` softened so the paper relationship is secondary.
- `docs/repository_submission_readiness.md` updated for this pass.

## What was added

- `docs/README.md` — a documentation index linking every important document,
  organised by user need (get started, teach, data/metrics, reproduce, scope,
  reviewers).
- `docs/audits/repository_coherence_report.md` — this report.

## What moved

- `docs/PAPER_REPOSITORY_ALIGNMENT.md` → `docs/audits/paper_repository_alignment.md`.
- The top-level `PAPER_REPOSITORY_ALIGNMENT.md` was removed; its content is
  represented here, keeping the repository root lightweight.

## What was intentionally not added

- No real measurements, datasets, photos, or CAD files (none exist yet; optional
  diagrams remain ASCII/CSV/Markdown).
- No new hardware tiers beyond the existing optional, owned-device / receive-only
  ones.
- No offensive wireless functionality and no scheduler/cooldown material.
- No standard-validation, real radio-performance, or deployment-readiness claims.
- No source-code removal or core-folder renames.

## How the repository supports the paper

The six paper sections (Introduction, Design, Build Instructions, Operating
Instructions, Validation, Conclusion) each map to concrete repository evidence in
`docs/paper_alignment.md`, with a detailed report in
`docs/audits/paper_repository_alignment.md`. Supplementary packaging and release
steps are in `SUPPLEMENTARY_MATERIALS_CHECKLIST.md` and `RELEASE_CHECKLIST.md`.

## How the repository remains useful beyond the paper

The README, quickstart, and teaching set let any instructor run a 90–120 minute
lab and any reviewer reproduce the demo in minutes, with no reference to the
paper required. The workflow, metrics, schema, and reproducibility tooling are
generally reusable for packet-observability teaching.

## Checks run

- `pytest` — all tests pass (incl. the scope/terminology guard).
- `python scripts/run_demo.py --all` — all expected outputs produced.
- `python scripts/verify_reproducibility.py --all` — PASS for all four cases.
- Firewall scan over tracked, non-archive files — no prohibited material.

## Checks not run

- Zenodo archival / DOI minting (post-release).
- `ruff` lint locally (runs in CI).
- GitHub Actions (runs on GitHub).

## Release-readiness score

**9/10 — ready pending the Zenodo DOI.**

## Suggested next GitHub issues

1. Mint the Zenodo DOI for `v0.1.0` and insert it into `CITATION.cff` and the
   README.
2. Add real wiring photos / vector diagrams under `hardware/wiring_diagrams/`.
3. Replace the security/conduct contact placeholders before publication.
4. Optional: add a `make demo` / task runner shortcut for the quickstart.
5. Optional: publish the rendered docs (e.g. GitHub Pages) from `docs/`.
