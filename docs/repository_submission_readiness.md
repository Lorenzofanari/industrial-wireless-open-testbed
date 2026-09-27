# Repository submission readiness

Status of the repository for public release and MDPI *Hardware* Supplementary
Material submission. This reflects the standalone-artifact coherence pass; the
internal narrative is in
[`audits/repository_coherence_report.md`](audits/repository_coherence_report.md).

> **Status note.** This page is a historical snapshot written before the
> `v0.1.0` release. `v0.1.0` has since been tagged and archived on Zenodo
> (DOI 10.5281/zenodo.21347262). The current corrected release is `v0.1.1`;
> see [`../CHANGELOG.md`](../CHANGELOG.md) and
> [`../RELEASE_CHECKLIST.md`](../RELEASE_CHECKLIST.md).

## Files present (key set)

Root: `README.md`, `LICENSE`, `CITATION.cff`, `requirements.txt`,
`pyproject.toml`, `environment.yml`, `RELEASE_CHECKLIST.md`,
`SUPPLEMENTARY_MATERIALS_CHECKLIST.md`, `claims_included.md`,
`claims_excluded.md`, plus the standard `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `SECURITY.md`.

Docs: a documentation index (`docs/README.md`), get-started (`overview.md`,
`quickstart.md`, `build_instructions.md`), teaching set
(`operating_instructions.md`, `learning_objectives.md`, `lab_activity_plan.md`,
`student_worksheet.md`, `instructor_guide.md`, `assessment_rubric.md`,
`common_student_mistakes.md`), data/metrics (`case_studies.md`,
`packet_schema.md`, `metrics.md`), reproducibility/validation
(`reproducibility_protocol.md`, `reproducibility_expected_outputs.md`,
`validation_walkthrough.md`), scope/safety/design (`safety_and_ethics.md`,
`limitations_and_non_goals.md`, `design_files_checklist.md`,
`design_integrity_statement.md`), reviewer/paper (`reviewer_checklist.md`,
`paper_alignment.md`, `repository_submission_readiness.md`), and internal
reports under `docs/audits/`.

Hardware: `topology.md`, `bill_of_materials.csv`, `bill_of_materials.md`,
`adoption_tiers.md`, `owned_devices_notes.md`, `receive_only_sdr_notes.md`,
`wiring_diagrams/README.md`, `safety_notes.md`.

## Changed in the coherence pass

- `README.md` rewritten to a repository-first identity (short title, practical
  navigation, paper details moved to a "Related paper" section).
- `docs/README.md` documentation index added.
- `docs/paper_alignment.md` restructured around the six Hardware sections.
- Internal alignment report moved to `docs/audits/paper_repository_alignment.md`;
  `docs/audits/repository_coherence_report.md` added; the top-level
  `PAPER_REPOSITORY_ALIGNMENT.md` removed to keep the root lightweight.

## Checks run

- `pytest` — all tests pass (incl. the scope/terminology guard).
- `python scripts/run_demo.py --all` — produces all expected outputs.
- `python scripts/verify_reproducibility.py --all` — PASS for all four cases.
- Firewall scan over tracked, non-archive files — no prohibited
  scheduler/claim material.

## Checks not run

- Zenodo archival / DOI minting — requires a published release (see
  `RELEASE_CHECKLIST.md`).
- `ruff` lint — not installed locally; runs (non-blocking) in CI.
- GitHub Actions — runs on push/PR on GitHub, not locally.

## Remaining TODOs

- Tag `v0.1.0`, archive on Zenodo, and insert the DOI into `CITATION.cff` and the
  README citation section.
- Optionally add real laboratory photos / vector diagrams under
  `hardware/wiring_diagrams/` once available.
- Replace the private security/conduct contact placeholders before publication.

## Readiness score

**9/10 — ready for submission pending the Zenodo DOI.** The repository is
understandable on its own, the software-only demo reproduces deterministically,
the teaching materials support a full lab session, and no out-of-scope or
prohibited material is present. The only remaining external step is the archival
DOI.
