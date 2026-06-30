# Claims included

This artifact makes only the following claims. They are educational and
artifact-facing, and they are all demonstrable from a clean clone.

- **Educational packet-observability workflow.** A teaching-oriented workflow
  for configuring profiles and observing packet-level behaviour.
- **Synthetic demo-mode reproducibility.** Deterministic regeneration of
  synthetic traces, verified by SHA-256 hashes.
- **YAML-driven profiles.** Four technology-like case-study profiles defined in
  human-editable YAML.
- **Packet metrics.** Packet count, duration, rate, mean size, inter-arrival
  mean/standard deviation (jitter proxy), missing/duplicate sequence
  identifiers, capture completeness, and per-node counts.
- **Manifest / hash verification.** Per-run manifests recording configuration,
  seed, git commit, and output hashes.
- **Optional owned-device or receive-only extension.** A safe, optional path to
  observe traffic on owned devices or to perform receive-only observation.
- **Safety boundaries.** Safe-by-design operation: no RF emission in demo mode;
  passive / receive-only extensions only.

See [`claims_excluded.md`](claims_excluded.md) for what the artifact explicitly
does not claim.
