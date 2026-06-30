# Paper alignment

This repository is designed to be useful on its own. This page is the single
place that maps it to the related paper, so the repository itself does not need
to refer to manuscript sections.

Related paper (MDPI *Hardware*): *An Open-Source Educational Artifact for
Wireless Packet Observability in Cyber–Physical Laboratories* (Lorenzo Fanari,
Patxi Galán, Ángel Monteagudo).

## Section-by-section mapping

| Paper section | Where it lives in the repository |
|---------------|----------------------------------|
| 1. Introduction | [`../README.md`](../README.md), [`overview.md`](overview.md), [`learning_objectives.md`](learning_objectives.md) |
| 2. Design | `src/packet_observability/`, `configs/*.yaml`, [`packet_schema.md`](packet_schema.md), [`metrics.md`](metrics.md), [`design_files_checklist.md`](design_files_checklist.md), [`design_integrity_statement.md`](design_integrity_statement.md), [`../hardware/topology.md`](../hardware/topology.md), [`../hardware/adoption_tiers.md`](../hardware/adoption_tiers.md), [`../hardware/bill_of_materials.csv`](../hardware/bill_of_materials.csv) |
| 3. Build Instructions | [`build_instructions.md`](build_instructions.md), `requirements.txt`, `pyproject.toml`, `environment.yml` |
| 4. Operating Instructions | [`operating_instructions.md`](operating_instructions.md), [`lab_activity_plan.md`](lab_activity_plan.md), [`student_worksheet.md`](student_worksheet.md), [`instructor_guide.md`](instructor_guide.md), [`assessment_rubric.md`](assessment_rubric.md), [`common_student_mistakes.md`](common_student_mistakes.md), `scripts/*.py` |
| 5. Validation | [`validation_walkthrough.md`](validation_walkthrough.md), [`reproducibility_expected_outputs.md`](reproducibility_expected_outputs.md), [`reproducibility_protocol.md`](reproducibility_protocol.md), `scripts/verify_reproducibility.py`, `tests/*.py`, `.github/workflows/reproducibility.yml` |
| 6. Conclusion | [`limitations_and_non_goals.md`](limitations_and_non_goals.md), [`../claims_included.md`](../claims_included.md), [`../claims_excluded.md`](../claims_excluded.md) |

## How to verify the mapping

- Reproduce the artefacts: `python scripts/run_demo.py --all` (Design, Build,
  Operating).
- Confirm determinism: `python scripts/verify_reproducibility.py --all`
  (Validation).
- Run the tests, including the scope/terminology guard: `pytest` (Validation,
  Conclusion).
- Read the scope statement: [`limitations_and_non_goals.md`](limitations_and_non_goals.md).

Synthetic demo-mode outputs are not real radio measurements; see
[`limitations_and_non_goals.md`](limitations_and_non_goals.md). A detailed
traceability and inspection report is kept in
[`audits/paper_repository_alignment.md`](audits/paper_repository_alignment.md).
