# Overview

## What this artifact is

This repository is an open-source **educational hardware/software artifact** for
teaching reproducible wireless packet observability in cyber–physical
laboratories. It accompanies the paper *An Open-Source Educational Artifact for
Wireless Packet Observability in Cyber–Physical Laboratories*.

It provides a configuration-driven, **software-only synthetic demo mode**: from
a YAML configuration it generates deterministic synthetic packet traces,
computes packet-level metrics, produces figures, and writes per-run manifests
with SHA-256 hashes. The same workflow extends to optional owned-device and
receive-only observation.

## Motivation

Reproducible, low-cost instrumentation is a recurring bottleneck in teaching and
preliminary research on industrial wireless communication. Real radios introduce
cost, safety, legal, and variability barriers that make it hard for students and
reviewers to reproduce results. This artifact lets the *entire* capture →
metrics → figures workflow run with no hardware, so that:

- students can learn packet-level observability without radios;
- reviewers can reproduce every figure from a clean clone;
- continuous integration can exercise the pipeline without special hardware.

## Intended users

- Journal reviewers checking the artifact.
- Educators and students in cyber–physical / IIoT laboratory courses.
- Open-source hardware evaluators.
- Early-stage researchers needing a reproducible observability baseline.

## How it relates to the paper

The repository is the artifact that supports the paper's contributions. Each
contribution (C1–C6) maps to concrete evidence in the repository; see
[`paper_alignment.md`](paper_alignment.md). The four technology-like case-study
profiles are described in [`case_studies.md`](case_studies.md).

## What it is not

This artifact does not implement wireless algorithms, interference mitigation,
offensive cybersecurity functionality, or radio-standard validation. Its purpose
is to teach reproducible packet-observability workflows. Synthetic demo-mode
outputs are not real radio measurements. See
[`limitations_and_non_goals.md`](limitations_and_non_goals.md),
[`claims_included.md`](../claims_included.md),
[`claims_excluded.md`](../claims_excluded.md), and
[`safety_and_ethics.md`](safety_and_ethics.md).

## Where to go next

- [`quickstart.md`](quickstart.md) — reproduce the demo from a clean clone.
- [`reproducibility_protocol.md`](reproducibility_protocol.md) — how
  reproducibility is achieved and verified.
- [`packet_schema.md`](packet_schema.md) and [`metrics.md`](metrics.md) — the
  data format and the metrics.
- [`reviewer_checklist.md`](reviewer_checklist.md) — a checklist for artifact
  reviewers.
