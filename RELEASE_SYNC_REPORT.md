# Software Release Synchronization Report

Generated 2026-09-27 for the revision of the manuscript *An Open-Source
Educational Artifact for Wireless Packet Observability in Cyber-Physical
Laboratories*. Every value below was read from the repository, its Git
history, the public GitHub API, or the public Zenodo API at the time of
writing. Nothing is estimated.

## Previous state

Archived baseline:
    v0.1.0

Original archived commit:
    7a86b306522be8cb3082e7cd81efad481a9ac839
    (annotated tag object 679aeb382c49113aadac63f5ae0681441c346939)

Original archival DOI:
    10.5281/zenodo.21347262  (Zenodo version DOI, version "v0.1.0",
                              publication date 2026-07-14, created by the
                              GitHub-Zenodo integration from
                              https://github.com/Lorenzofanari/industrial-wireless-open-testbed/tree/v0.1.0)
    Concept DOI (all versions): 10.5281/zenodo.21347261

GitHub release v0.1.0:
    https://github.com/Lorenzofanari/industrial-wireless-open-testbed/releases/tag/v0.1.0
    (published 2026-07-13T22:40:12Z)

Important audit finding:
    Before this synchronization the repository HEAD (`master`) was
    byte-identical to `v0.1.0`. The repository contained **no**
    major-revision patch / "Supplementary Software S1", and no revised
    experiment scripts. The estimator in `v0.1.0` was `N / (t_max - t_min)`.

## Revised state

Release:
    v0.1.1

Commit:
    c654a0a3803e296d9dfd2eaa336481aa5f15a50d

Tag:
    v0.1.1  (annotated tag object 61c4ef33a892cbe0ee4f5ccba89076806e3f8fcb,
             message "v0.1.1: corrected span-rate estimator and revision validation")
    `git rev-list -n 1 v0.1.1` == `git rev-parse HEAD` at release time ==
    c654a0a3803e296d9dfd2eaa336481aa5f15a50d

Repository:
    https://github.com/Lorenzofanari/industrial-wireless-open-testbed
    Branch pushed: master (fast-forward 7a86b30..c654a0a, no force-push)
    Tag pushed:    v0.1.1 (new tag; v0.1.0 untouched)

CI:
    Workflow: .github/workflows/reproducibility.yml
    Run on tag v0.1.1 (commit c654a0a):
        https://github.com/Lorenzofanari/industrial-wireless-open-testbed/actions/runs/36338216063
        conclusion: success (Python 3.9, 3.11, 3.12)
    Run on master push (commit c654a0a):
        https://github.com/Lorenzofanari/industrial-wireless-open-testbed/actions/runs/36338214749
        conclusion: success (Python 3.9, 3.11, 3.12)

Archive DOI:
    pending archival synchronization
    (No GitHub *Release* has been published for v0.1.1 yet; the GitHub-Zenodo
    integration is triggered by release publication, not by the tag push.
    As of writing, the Zenodo concept record 21347261 lists only v0.1.0.)

## Equation (4) correction

Previous implementation (v0.1.0, `src/packet_observability/metrics.py`, line 75):
    packet_rate_pps = total_packets / duration_s        # N / (t_max - t_min)

Corrected implementation (v0.1.1, `src/packet_observability/metrics.py`,
`span_event_rate()`, used by `compute_metrics()`):
    R_span = (N - 1) / (t_max - t_min)

Boundary behavior (actual implementation):
    * Timestamps are coerced to numbers; non-numeric and non-finite values
      (NaN, ±inf) are ignored and do not count towards N.
    * N < 2               -> NaN (undefined; existing project convention)
    * t_max <= t_min      -> NaN (zero span)
    * `duration_s` is still reported (0.0 in both cases); inter-arrival
      statistics are NaN for N < 2.
    * `compute_metrics()` raises ValueError for an empty table, for a missing
      mandatory column (`timestamp`, `node_id`, `packet_size_bytes`), or when
      no row has a valid numeric timestamp.
    * Non-positive / non-numeric `packet_size_bytes` values are excluded from
      the size statistics (timing metrics unaffected).
    * `sequence_id` is optional: absent column -> 0 missing, 0 duplicate,
      NaN completeness (v0.1.0 raised KeyError).

Effect on the shipped W1-W4 demo traces (regenerated locally, not committed):
    profile   N     span (s)     v0.1.0 N/span   v0.1.1 (N-1)/span
    W1      6000    59.980352      100.0328         100.0161
    W2      1440   119.751803       12.0249          12.0165
    W3      1440   179.523400        8.0212           8.0157
    W4       900   299.043724        3.0096           3.0062

## Independent verification

File: `tests/test_metrics_independent.py` (24 test cases; all tables are
hand-written, expected values derived analytically in the test body; none
uses the synthetic generator).

- analytical 2 packets/s trace (timestamps [0.0, 0.5, 1.0], N=3, span=1.0 s,
  2 intervals):
    `test_a_span_rate_three_timestamps_two_intervals`
    `test_a_span_rate_additional_analytical_cases[...]` (5 further cases)
    `test_a_span_rate_is_order_independent`
- 500 ms mean gap:
    `test_a_mean_inter_event_interval_is_500ms`
- missing/duplicate sequence test (ids [1, 3, 3] -> 1 missing, 1 duplicate):
    `test_b_missing_and_duplicate_sequence_ids`
    `test_b_complete_sequence_has_no_missing_or_duplicates`
    `test_b_sequence_metrics_are_per_node`
- 100/250 ms per-node gap tests (node A spacing 0.1 s, node B spacing 0.25 s):
    `test_c_per_node_mean_gaps_100ms_and_250ms`
    `test_c_per_node_gap_is_independent_of_interleaving`
- boundary tests:
    `test_boundary_empty_trace_raises`
    `test_boundary_one_record_trace_has_undefined_rate`
    `test_boundary_zero_timestamp_span_has_undefined_rate`
    `test_boundary_invalid_timestamps_are_discarded`
    `test_boundary_all_timestamps_invalid_raises`
    `test_boundary_span_event_rate_direct_edge_cases`
    `test_boundary_missing_required_column_raises[timestamp|node_id|packet_size_bytes]`
    `test_boundary_missing_sequence_column_yields_undefined_sequence_metrics`
    `test_boundary_non_positive_packet_sizes_are_excluded_from_size_statistics`

Pre-existing tests retained unchanged: `tests/test_metrics.py`,
`tests/test_generator_determinism.py`, `tests/test_manifest_hashes.py`,
`tests/test_configs.py`, `tests/test_no_unsafe_terminology.py`.

## Revised evaluation

Scripts present in the repository and their use of the canonical estimator:

| Purpose | Script | Calls corrected canonical implementation? |
|---------|--------|-------------------------------------------|
| deterministic reproduction (fixed-input, hash-verified, W1-W4) | `scripts/verify_reproducibility.py --all` | n/a — hash comparison of generated traces only; computes no rate |
| synthetic demonstration + metrics (W1-W4) | `scripts/run_demo.py --all` | **yes** — `compute_from_csv` → `compute_metrics` → `span_event_rate` |
| metrics from an arbitrary trace | `scripts/compute_metrics.py` | **yes** — `compute_from_csv` → `compute_metrics` → `span_event_rate` |
| trace generation only | `scripts/generate_traces.py` | n/a — no metrics |
| figures only | `scripts/plot_results.py` | n/a — reads metrics, computes no rate |
| 30-seed experiment (30 seeds per profile) | **NOT PRESENT in repository** | — |
| controlled omissions | **NOT PRESENT in repository** | — |
| interval / offered-load sensitivity | **NOT PRESENT in repository** | — |
| local scalability benchmark | **NOT PRESENT in repository** | — |
| malformed / boundary-input tests | `tests/test_metrics_independent.py` (pytest, not a script) | **yes** |

Repository-wide search (`*.py`, `*.md`, excluding `archive/`) found no other
rate computation: no `N / span`, `total_packets / duration`, or equivalent
outside the canonical function. The only legacy consumer,
`archive/legacy_material_pending_review/build_report.py`, imports a
non-existent `src.analysis` module (dead code) and only *reads*
`packet_rate_pps`; it was left untouched as archived material.

UNRESOLVED (author decision required): if the manuscript's 30-seed,
controlled-omission, interval-sensitivity and scalability experiments were
executed with scripts that live outside this repository (e.g. in the
"Supplementary Software S1" package), those scripts are **not** part of
`v0.1.1`. Either (a) add them (importing `packet_observability.metrics`) and
issue `v0.1.2`, or (b) state in the manuscript that those experiment drivers
are provided as Supplementary Software while all metric values are computed
by the `v0.1.1` library. Do not move the `v0.1.1` tag.

## CI validation

Actual results (public GitHub Actions API, 2026-09-27):

    run 36338216063  (tag v0.1.1, commit c654a0a)  success
        reproducibility (3.9)  : all steps success
        reproducibility (3.11) : all steps success
        reproducibility (3.12) : all steps success
    run 36338214749  (master,   commit c654a0a)  success
        reproducibility (3.9 / 3.11 / 3.12): all steps success

Steps executed per job: install dependencies; ruff check (non-blocking);
report package version; `python -m pytest -v` (76 tests incl. the 24
independent tests); `python scripts/run_demo.py --all`;
`python scripts/verify_reproducibility.py --all`.

Local validation of the tagged tree (clean `git archive` export, Python 3.13.5,
pandas 3.0.3, numpy 2.5.1):

    tests passed:            76
    tests failed:            0
    warnings:                0 reported by pytest
    reproducibility checks:  PASS (W1-W4 deterministic and matching committed references)
    demo checks:             PASS (run_demo.py --all, 4 profiles, 4 figures each)
    lint status:             ruff check src tests scripts -> All checks passed
                             (ruff format is not an enforced project check and was not applied)

## Manuscript replacement values

ARTIFACT VERSION: 0.1.1
ARTIFACT TAG:     v0.1.1
ARTIFACT COMMIT:  c654a0a3803e296d9dfd2eaa336481aa5f15a50d
ARTIFACT DOI:     PENDING — DO NOT INSERT A PLACEHOLDER DOI
                  (publish the GitHub Release v0.1.1 to trigger Zenodo; then
                   use the new *version* DOI, not 10.5281/zenodo.21347262)
CI REFERENCE:     https://github.com/Lorenzofanari/industrial-wireless-open-testbed/actions/runs/36338216063

## ARCHIVAL ACTION REQUIRED

The GitHub-Zenodo integration is configured (the v0.1.0 record was created by
it), but Zenodo archives only on **GitHub Release publication**. The author
must:

1. Open https://github.com/Lorenzofanari/industrial-wireless-open-testbed/releases/new?tag=v0.1.1
2. Title: `0.1.1` (or `v0.1.1`); body: contents of `RELEASE_NOTES_v0.1.1.md`.
3. Publish the release (not as draft/pre-release).
4. Wait for Zenodo to create the new version under concept record
   10.5281/zenodo.21347261 and copy the new **version** DOI.
5. Add `doi:` and `date-released:` to `CITATION.cff` (replacing the TODO
   comment), add the DOI to README "Citation"/"Releases", commit on `master`
   (the tag is not moved), and insert the DOI into the manuscript
   `\ArtifactDOI` macro.

## Files modified in the release commit (c654a0a)

    .github/workflows/reproducibility.yml    (CI: pytest -v, run_demo --all, tag + manual triggers)
    CHANGELOG.md                             (new)
    CITATION.cff                             (0.1.1, W1-W4 wording, concept + v0.1.0 DOIs, TODO for v0.1.1 DOI)
    README.md                                (W1-W4 table, Releases table, citation/DOI section)
    RELEASE_CHECKLIST.md                     (v0.1.1 procedure)
    RELEASE_NOTES_v0.1.1.md                  (new)
    SUPPLEMENTARY_MATERIALS_CHECKLIST.md     (changelog, release notes, independent tests rows)
    docs/case_studies.md                     (W1-W4 mapping)
    docs/design_integrity_statement.md       (v0.1.0 baseline / v0.1.1 corrected)
    docs/metrics.md                          (Equation (4), boundary behaviour, input validation)
    docs/quickstart.md                       (git checkout v0.1.1)
    docs/repository_submission_readiness.md  (status note)
    docs/reproducibility_expected_outputs.md (W1-W4, new summary field)
    pyproject.toml                           (version 0.1.1)
    scripts/_bootstrap.py                    (WORKLOAD_LABELS, workload_label)
    scripts/run_demo.py                      (W-label in output)
    scripts/verify_reproducibility.py        (W-label in output)
    src/packet_observability/__init__.py     (__version__ 0.1.1)
    src/packet_observability/metrics.py      (span_event_rate, validation, per-node gaps)
    tests/test_metrics_independent.py        (new)

    20 files changed, 781 insertions(+), 92 deletions(-)

Not modified: configs, `data/synthetic_demo/*` reference traces, generator,
manifests, plotting, extensions, `RELEASE_NOTES_v0.1.0.md`, `archive/`.

## Other observations (not acted upon)

- Repository documents refer to the journal as MDPI *Hardware*; the revision
  brief refers to MDPI *Software*. Not changed (no repository evidence);
  author to reconcile.
- `docs/audits/*.md` are dated audit snapshots that still describe the v0.1.0
  release as pending; left as historical records.
- No git `user.name`/`user.email` is configured on this machine; the release
  commit and tag were authored as `Lorenzofanari <Lorenzofanari@users.noreply.github.com>`,
  the identity of the repository's existing commits, via one-off `-c` options.
