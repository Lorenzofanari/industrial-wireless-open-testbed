# Repository submission readiness

Status of the repository for MDPI *Hardware* Supplementary Material submission.

## Files added (this alignment pass)

Root:

- `SUPPLEMENTARY_MATERIALS_CHECKLIST.md`
- `RELEASE_CHECKLIST.md`
- `claims_included.md`, `claims_excluded.md`
- `PAPER_REPOSITORY_ALIGNMENT.md` (final report)

Docs:

- `docs/PAPER_REPOSITORY_ALIGNMENT.md` (inspection report)
- `docs/build_instructions.md`, `docs/operating_instructions.md`
- `docs/learning_objectives.md`, `docs/lab_activity_plan.md`,
  `docs/student_worksheet.md`, `docs/instructor_guide.md`,
  `docs/assessment_rubric.md`, `docs/common_student_mistakes.md`
- `docs/validation_walkthrough.md`, `docs/reproducibility_expected_outputs.md`
- `docs/design_files_checklist.md`, `docs/design_integrity_statement.md`

Hardware:

- `hardware/topology.md`, `hardware/bill_of_materials.csv`,
  `hardware/wiring_diagrams/README.md`

## Files changed

- `README.md` — rewritten with the final title and reviewer-friendly sections.
- `CITATION.cff` — final title, authors, repository URL, DOI placeholder.
- `pyproject.toml` — description and authors updated.
- `docs/overview.md`, `docs/limitations_and_non_goals.md`,
  `docs/paper_alignment.md`, `docs/reviewer_checklist.md`,
  `hardware/README.md` — reframed to be educational/artifact-facing.

## Checks run

- `pytest` — all tests pass.
- `python scripts/run_demo.py --all` — produces all expected outputs.
- `python scripts/verify_reproducibility.py --all` — reports PASS for all four
  cases (deterministic and reference-consistent).
- Firewall scan over tracked, non-archive files — no prohibited
  scheduler/claim material present.

## Checks not run

- **Zenodo archival / DOI minting** — requires a published release; tracked in
  `RELEASE_CHECKLIST.md`.
- **`ruff` lint** — not installed in the local environment; runs (non-blocking)
  in CI.
- **GitHub Actions run** — executes on push/PR on GitHub, not locally.

## Remaining TODOs

- Tag `v0.1.0`, archive on Zenodo, and insert the DOI into `CITATION.cff` and the
  README citation section.
- Optionally add real laboratory photos / vector diagrams under
  `hardware/wiring_diagrams/` once available.
- Replace the private security/conduct contact placeholders before publication.

## Readiness score

**9/10 — ready for submission pending the Zenodo DOI.** All required documents,
educational materials, build/operating instructions, validation workflow, and
metadata are present; the synthetic demo reproduces deterministically; and no
out-of-scope or prohibited material is present. The only remaining external step
is minting and inserting the archival DOI.
