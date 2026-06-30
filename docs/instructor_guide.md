# Instructor guide

## Preparation checklist

- [ ] Confirm each machine has Python 3.9+ and can create a virtual environment.
- [ ] Pre-install dependencies (`pip install -r requirements.txt`) or have the
      `environment.yml` ready.
- [ ] Run `python scripts/run_demo.py --all` and `pytest` once yourself to
      confirm the environment.
- [ ] Print or share [`student_worksheet.md`](student_worksheet.md) and
      [`assessment_rubric.md`](assessment_rubric.md).

## Suggested timing

Follow [`lab_activity_plan.md`](lab_activity_plan.md). The session fits in
90–120 minutes; the reproducibility and synthetic-vs-real discussion phases are
the most important for learning outcomes.

## How to verify student outputs

- Check that `results/demo/<case>/` contains `packets.csv`, `metrics.csv`,
  `metrics_summary.json`, `inter_arrival.csv`, `manifest.json`, and `figures/`.
- Cross-check the worksheet metrics against `metrics_summary.json`.
- Confirm the recorded SHA-256 matches the `outputs` entry in `manifest.json`.
- Have students run `python scripts/verify_reproducibility.py --all` and confirm
  `PASS`.

## Common mistakes

See [`common_student_mistakes.md`](common_student_mistakes.md). The most frequent
are treating synthetic data as real measurements and confusing the global
inter-arrival mean with the configured per-node interval.

## Discussion prompts

- Why is determinism (same seed → same hash) useful for teaching and review?
- What would change if you increased `drop_probability` in the config?
- How would the workflow differ if observing owned devices instead of synthetic
  data — and what stays the same?

## Adapting to owned-device observation

For groups with suitable owned equipment, the same metrics-to-figures pipeline
accepts traces captured via the optional extensions
([`../hardware/owned_devices_notes.md`](../hardware/owned_devices_notes.md)).
Emphasise that this is owned-device / receive-only only, and that it still does
not constitute standard validation or a real radio-performance claim.

## Safety reminders

Reinforce the boundaries in [`safety_and_ethics.md`](safety_and_ethics.md): no
jamming, flooding, deauthentication, exploitation, unauthorised scanning, or
third-party observation. Optional hardware tiers require authorisation.
