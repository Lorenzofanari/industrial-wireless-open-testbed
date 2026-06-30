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

## Documentation for the Hardware-journal structure

- [ ] Build instructions are present and copy-paste runnable
      (`docs/build_instructions.md`).
- [ ] Operating instructions are present (`docs/operating_instructions.md`).
- [ ] A lab guide and educational materials are present
      (`docs/lab_activity_plan.md`, `docs/learning_objectives.md`,
      `docs/instructor_guide.md`, `docs/common_student_mistakes.md`).
- [ ] An assessment rubric and student worksheet are present
      (`docs/assessment_rubric.md`, `docs/student_worksheet.md`).
- [ ] A validation walkthrough and expected outputs are present
      (`docs/validation_walkthrough.md`, `docs/reproducibility_expected_outputs.md`).

## Submission and design integrity

- [ ] Supplementary materials checklist is present
      (`SUPPLEMENTARY_MATERIALS_CHECKLIST.md`).
- [ ] Design files checklist and integrity statement are present
      (`docs/design_files_checklist.md`, `docs/design_integrity_statement.md`).
- [ ] Citation metadata is complete (`CITATION.cff`: title, authors,
      repository URL, version).
- [ ] Release DOI procedure is documented (`RELEASE_CHECKLIST.md`); the DOI is
      added after the Zenodo release.

## Paper alignment

- [ ] Contributions C1–C6 map to repository evidence
      (`docs/paper_alignment.md`).
- [ ] Paper sections (Introduction → Conclusion) map to repository evidence
      (`docs/paper_alignment.md`; detailed report in
      `docs/audits/paper_repository_alignment.md`).
