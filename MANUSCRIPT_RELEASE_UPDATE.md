# Manuscript update instructions after the v0.1.1 release

Companion to `RELEASE_SYNC_REPORT.md`. This file lists the exact manuscript
and response-letter changes needed so that both documents describe **one**
software state: the public tagged release `v0.1.1`.

## 1. Values derived from the repository

| Macro / field | Value | Source |
|---------------|-------|--------|
| `\ArtifactVersion` | `0.1.1` | `pyproject.toml`, `CITATION.cff`, `packet_observability.__version__` |
| `\ArtifactTag` (if used) | `v0.1.1` | `git tag`; pushed to origin |
| `\ArtifactCommit` | `c654a0a3803e296d9dfd2eaa336481aa5f15a50d` | `git rev-list -n 1 v0.1.1` |
| `\ArtifactCommitShort` (if used) | `c654a0a` | idem |
| `\ArtifactDOI` | **PENDING — DO NOT INSERT A PLACEHOLDER DOI.** Fill only with the Zenodo *version* DOI minted after the GitHub Release v0.1.1 is published. Do not reuse `10.5281/zenodo.21347262` (that is v0.1.0). | Zenodo, after archival |
| Concept DOI (optional, all versions) | `10.5281/zenodo.21347261` | Zenodo API (verified) |
| Baseline DOI (v0.1.0, for the "previous version" statement) | `10.5281/zenodo.21347262` | Zenodo API (verified) |
| Baseline commit (v0.1.0) | `7a86b306522be8cb3082e7cd81efad481a9ac839` | `git rev-list -n 1 v0.1.0` |
| CI evidence | `https://github.com/Lorenzofanari/industrial-wireless-open-testbed/actions/runs/36338216063` (tag v0.1.1, success on Python 3.9/3.11/3.12) | GitHub Actions API |
| Repository | `https://github.com/Lorenzofanari/industrial-wireless-open-testbed` | — |

## 2. Replace the "v0.1.0 + Supplementary Software S1" description

Wherever the manuscript or the response letter currently states that the
revised evaluation used **v0.1.0 plus a major-revision patch /
Supplementary Software S1**, replace it with wording equivalent to:

> The revised evaluation was performed using the corrected public release
> v0.1.1 (commit `\ArtifactCommit`), which incorporates the corrected
> Equation (4) implementation, the associated regression tests, and the
> scripts used for the revised experiments. Release v0.1.1 is tagged in the
> public repository and archived on Zenodo (`\ArtifactDOI`). The original
> archived baseline v0.1.0 (DOI 10.5281/zenodo.21347262) is retained
> unchanged for provenance.

Sections typically affected: Data Availability Statement, Supplementary
Materials statement, "Software and reproducibility" / "Artifact" subsection,
figure/table captions that cite the software version, and the response
letter's reply to the Academic Editor.

Justification to give the Editor (why a new tag rather than baseline+patch):
a single immutable tag/commit/DOI chain removes any ambiguity about the exact
state evaluated, is what CI actually validated, and is what Zenodo archives;
a patch on top of v0.1.0 would require the reader to reconstruct that state.

## 3. Equation (4) text

State the estimator exactly as implemented:

> R_span = (N_observed − 1) / (t_max − t_min), for N_observed ≥ 2 and
> t_max > t_min; undefined (reported as NaN) otherwise.

If the manuscript still shows `N / (t_max − t_min)` anywhere (equation,
text, table footnote), correct it and, in the response letter, point to
`src/packet_observability/metrics.py::span_event_rate` and
`docs/metrics.md` in v0.1.1.

## 4. Independent regression tests

Where the manuscript describes the added regression tests, cite the file
`tests/test_metrics_independent.py` (v0.1.1) and, if useful, the specific
analytical cases:

- timestamps `[0.0, 0.5, 1.0]` → 2 intervals over 1.0 s → 2.0 packets/s,
  mean inter-event interval 500 ms
  (`test_a_span_rate_three_timestamps_two_intervals`,
  `test_a_mean_inter_event_interval_is_500ms`);
- sequence ids `[1, 3, 3]` → 1 missing, 1 duplicate
  (`test_b_missing_and_duplicate_sequence_ids`);
- per-node spacing 0.1 s / 0.25 s → 100 ms / 250 ms
  (`test_c_per_node_mean_gaps_100ms_and_250ms`);
- boundary cases: empty trace, one record, zero span, invalid timestamps,
  missing mandatory columns, non-positive packet sizes
  (`test_boundary_*`).

State explicitly that these tables are hand-constructed and their expected
values are analytical, i.e. independent of the synthetic generator.

## 5. W1–W4 terminology

Use `W1`–`W4` as the profile names in the manuscript. If a mapping table is
included, use:

| Profile | Configuration file in the repository |
|---------|--------------------------------------|
| W1 | `configs/wifi_like.yaml` |
| W2 | `configs/ble_like.yaml` |
| W3 | `configs/ieee802154_like.yaml` |
| W4 | `configs/lora_sdr_like.yaml` |

(`docs/case_studies.md` in v0.1.1 documents the same mapping.)

## 6. CI statement

Wording supported by the evidence:

> Continuous integration (GitHub Actions, workflow `reproducibility.yml`)
> executed the complete test suite (76 tests, including the independent
> regression tests), the synthetic demonstration for W1–W4, and the
> reproducibility verification against the committed reference traces on
> Python 3.9, 3.11 and 3.12 for the tagged commit `\ArtifactCommit`
> (run 36338216063, all jobs successful).

## 7. Items the author must resolve before finalising

1. **Zenodo DOI for v0.1.1** — publish the GitHub Release for tag `v0.1.1`
   (see "ARCHIVAL ACTION REQUIRED" in `RELEASE_SYNC_REPORT.md`), then fill
   `\ArtifactDOI`, `CITATION.cff` (`doi:`, `date-released:`) and the README.
2. **Revised-experiment drivers** — the repository at `v0.1.1` contains
   `run_demo.py`, `verify_reproducibility.py`, `compute_metrics.py`,
   `generate_traces.py`, `plot_results.py` and the pytest suite. It does
   **not** contain dedicated scripts for the 30-seed campaign, controlled
   omissions, interval/offered-load sensitivity, or the scalability
   benchmark. If the manuscript reports those experiments, either add the
   drivers to the repository (using `packet_observability.metrics`) and
   release `v0.1.2`, or describe them accurately as Supplementary Software
   that *calls* the v0.1.1 library. The manuscript must not claim that
   `v0.1.1` ships those drivers unless they are added.
3. **Journal name** — repository text says MDPI *Hardware*; the revision
   brief says MDPI *Software*. Align the repository (`README.md`,
   `docs/paper_alignment.md`, `SUPPLEMENTARY_MATERIALS_CHECKLIST.md`,
   `RELEASE_CHECKLIST.md`) with the actual venue in a follow-up commit if
   needed (does not affect the tagged code).
4. **Consistency check** — after filling the macros, grep the manuscript
   and response letter for `0.1.0`, `S1`, `patch` and make sure each
   remaining occurrence refers explicitly to the *previous* baseline.
