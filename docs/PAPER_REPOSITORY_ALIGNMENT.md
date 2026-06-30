# Paper ↔ repository alignment (inspection report)

Paper: *An Open-Source Educational Artifact for Wireless Packet Observability in
Cyber–Physical Laboratories* (MDPI *Hardware* structure: Introduction, Design,
Build Instructions, Operating Instructions, Validation, Conclusion).

This report records the state of the repository relative to the manuscript and
the actions taken to bring it into coherence. A concise final report is kept at
the repository root in `PAPER_REPOSITORY_ALIGNMENT.md`.

## Current repository strengths

- Clean core library `src/packet_observability/` (synthetic generator, metrics,
  plotting, manifest, hashing, I/O) with thin CLIs in `scripts/`.
- Four technology-like YAML profiles and committed canonical synthetic traces in
  `data/synthetic_demo/`.
- Deterministic, hash-verified reproducibility (`verify_reproducibility.py`) and
  hardware-free CI (`.github/workflows/reproducibility.yml`).
- Safety-by-design: synthetic mode emits no RF; optional extensions are passive /
  receive-only and dry-run by default; a terminology-guard test enforces this.
- Documentation set: overview, quickstart, reproducibility protocol, case
  studies, packet schema, metrics, limitations/non-goals, safety/ethics,
  reviewer checklist, paper alignment.

## Files added to support the Hardware-journal structure

| Paper section | Added/updated material |
|---------------|------------------------|
| Design | `docs/design_files_checklist.md`, `docs/design_integrity_statement.md`, `hardware/topology.md`, `hardware/bill_of_materials.csv`, `hardware/wiring_diagrams/README.md` |
| Build Instructions | `docs/build_instructions.md` |
| Operating Instructions | `docs/operating_instructions.md`, plus educational materials (`learning_objectives.md`, `lab_activity_plan.md`, `student_worksheet.md`, `instructor_guide.md`, `assessment_rubric.md`, `common_student_mistakes.md`) |
| Validation | `docs/validation_walkthrough.md`, `docs/reproducibility_expected_outputs.md` |
| Submission | `SUPPLEMENTARY_MATERIALS_CHECKLIST.md`, `RELEASE_CHECKLIST.md`, `docs/repository_submission_readiness.md`, `claims_included.md`, `claims_excluded.md` |

## Unsupported / out-of-scope claims (must remain absent)

The repository must not assert real radio performance, radio-standard
validation, interference mitigation, wireless scheduling, industrial
certification, or deployment-ready reliability. These are tracked in
`claims_excluded.md` and guarded by `tests/test_no_unsafe_terminology.py`.

## Traceability matrix (paper section → repository evidence)

| Paper section | Repository evidence |
|---------------|---------------------|
| 1. Introduction | `README.md`, `docs/overview.md`, `docs/learning_objectives.md` |
| 2. Design | `src/packet_observability/`, `configs/*.yaml`, `docs/packet_schema.md`, `docs/metrics.md`, `docs/design_files_checklist.md`, `docs/design_integrity_statement.md`, `hardware/topology.md`, `hardware/adoption_tiers.md`, `hardware/bill_of_materials.csv` |
| 3. Build Instructions | `docs/build_instructions.md`, `requirements.txt`, `pyproject.toml`, `environment.yml` |
| 4. Operating Instructions | `docs/operating_instructions.md`, `docs/lab_activity_plan.md`, `docs/student_worksheet.md`, `docs/instructor_guide.md`, `docs/assessment_rubric.md`, `docs/common_student_mistakes.md`, `scripts/*.py` |
| 5. Validation | `docs/validation_walkthrough.md`, `docs/reproducibility_expected_outputs.md`, `scripts/verify_reproducibility.py`, `tests/*.py`, `.github/workflows/reproducibility.yml` |
| 6. Conclusion | `docs/limitations_and_non_goals.md`, `claims_included.md`, `claims_excluded.md` |

## Immediate fix list (status)

- [x] Align public title and metadata (README, CITATION.cff, overview, pyproject).
- [x] Add Build Instructions and Operating Instructions documents.
- [x] Add educational materials (objectives, lab plan, worksheet, instructor
      guide, rubric, common mistakes).
- [x] Recreate hardware design files (topology, BOM CSV, wiring diagrams README).
- [x] Add validation walkthrough and expected-outputs documents.
- [x] Add supplementary-materials and release checklists, design-integrity docs.
- [x] Reframe non-goals as educational/artifact-facing; confirm no protected
      scheduler material is present.
- [ ] Mint a Zenodo DOI and insert it into `CITATION.cff` (post-release; tracked
      in `RELEASE_CHECKLIST.md`).
