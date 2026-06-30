# Paper ↔ repository alignment — final report

Paper: *An Open-Source Educational Artifact for Wireless Packet Observability in
Cyber–Physical Laboratories* (MDPI *Hardware*: Introduction, Design, Build
Instructions, Operating Instructions, Validation, Conclusion).

This report summarises the work done to bring the repository into coherence with
the manuscript and its readiness for Supplementary Material submission. A more
detailed inspection report is in
[`docs/PAPER_REPOSITORY_ALIGNMENT.md`](docs/PAPER_REPOSITORY_ALIGNMENT.md).

## What was added

- **Build & operating instructions:** `docs/build_instructions.md`,
  `docs/operating_instructions.md`.
- **Educational materials:** `docs/learning_objectives.md`,
  `docs/lab_activity_plan.md`, `docs/student_worksheet.md`,
  `docs/instructor_guide.md`, `docs/assessment_rubric.md`,
  `docs/common_student_mistakes.md`.
- **Validation:** `docs/validation_walkthrough.md`,
  `docs/reproducibility_expected_outputs.md`.
- **Design integrity:** `docs/design_files_checklist.md`,
  `docs/design_integrity_statement.md`.
- **Hardware design files:** `hardware/topology.md`,
  `hardware/bill_of_materials.csv`, `hardware/wiring_diagrams/README.md`.
- **Submission & scope:** `SUPPLEMENTARY_MATERIALS_CHECKLIST.md`,
  `RELEASE_CHECKLIST.md`, `claims_included.md`, `claims_excluded.md`,
  `docs/repository_submission_readiness.md`,
  `docs/PAPER_REPOSITORY_ALIGNMENT.md`, and this file.

## What was changed

- **Title and metadata** aligned to the manuscript title in `README.md`,
  `CITATION.cff` (authors: Lorenzo Fanari, Patxi Galán, Ángel Monteagudo;
  version 0.1.0; repository URL; DOI placeholder), `pyproject.toml`, and
  `docs/overview.md`.
- **README** rewritten with reviewer-friendly sections (summary, what it teaches,
  quickstart, structure, profiles, build tiers, operating, reproducibility,
  safety, supplementary, citation, license).
- **Non-goals reframed** to be educational/artifact-facing in
  `docs/limitations_and_non_goals.md`, `docs/overview.md`, `README.md`, and
  `docs/paper_alignment.md`, with the concise lists in `claims_*.md`.
- **Reviewer checklist** extended with build/operating/lab/rubric/supplementary/
  design-integrity/citation/DOI checks.
- **Hardware index** updated to reference the new topology, BOM CSV, and wiring
  notes.

## Verification

- `pytest` — all tests pass (including the terminology-guard test).
- `python scripts/run_demo.py --all` — produces all expected outputs for the four
  case studies.
- `python scripts/verify_reproducibility.py --all` — PASS (deterministic and
  reference-consistent).
- Firewall scan over tracked, non-archive files — no prohibited scheduler or
  out-of-scope claim material (no cooldown-on-failure scheduler, π_on/p_loss/χ,
  ns-3 campaign, S4/S8/S9, PDR/anti-jamming/Wi-Fi 6 validation, deployment-ready,
  SIL/PROFIsafe claims).

## What remains TODO

- Mint a Zenodo DOI for the tagged `v0.1.0` release and insert it into
  `CITATION.cff` and the README (tracked in `RELEASE_CHECKLIST.md`).
- Optionally add real laboratory photos / vector diagrams under
  `hardware/wiring_diagrams/`.
- Replace the private security/conduct contact placeholders before publication.

## Readiness

The repository is **ready for MDPI *Hardware* Supplementary submission pending
the Zenodo DOI**. It is a safe, reproducible, educational packet-observability
artifact: software-only by default, with optional owned-device / receive-only
tiers, complete build/operating/validation documentation, and an explicit scope
that excludes real radio performance, standard validation, interference
mitigation, wireless scheduling, offensive functionality, and industrial
certification.
