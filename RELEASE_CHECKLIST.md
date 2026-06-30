# Release checklist

Steps to publish a citable release of this artifact and prepare it as
Supplementary Material for MDPI *Hardware*.

## Pre-release verification

- [ ] CI passes on the default branch
      (`.github/workflows/reproducibility.yml`: tests + demo + reproducibility).
- [ ] Local checks pass:
      ```bash
      python scripts/run_demo.py --all
      python scripts/verify_reproducibility.py --all
      pytest
      ```
- [ ] `docs/repository_submission_readiness.md` is up to date.

## Metadata

- [ ] `CITATION.cff` title, authors (Lorenzo Fanari, Patxi Galán, Ángel
      Monteagudo), version (`0.1.0`), and `repository-code` are correct.
- [ ] README title matches the manuscript title.
- [ ] License is present and correct (see `LICENSE`).
- [ ] Safety notes are present (`docs/safety_and_ethics.md`,
      `hardware/safety_notes.md`).

## Firewall

- [ ] No protected scheduler material is present (no cooldown-on-failure
      scheduler, π_on/p_loss/χ coefficients, ns-3 campaign, S4/S8/S9
      comparison, PDR/anti-jamming/Wi-Fi 6 validation claims). Confirm with the
      grep scan in `docs/repository_submission_readiness.md`.

## Tag and archive

- [ ] Tag the release:
      ```bash
      git tag -a v0.1.0 -m "v0.1.0"
      git push origin v0.1.0
      ```
- [ ] Archive the tagged release on Zenodo (or another archival service).
- [ ] Add the resulting DOI to `CITATION.cff` (replace
      `TO_BE_ADDED_AFTER_ZENODO_RELEASE`) and to the README citation section.

## Supplementary package

- [ ] Build the supplementary ZIP from the items in
      `SUPPLEMENTARY_MATERIALS_CHECKLIST.md` (exclude the local `.venv/` and the
      git-ignored `results/` outputs; reviewers regenerate them).
- [ ] Verify the manuscript references the repository URL and the DOI.

## Final

- [ ] Sanity-check the supplementary ZIP unpacks and the quickstart works from a
      clean clone.
