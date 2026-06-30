# Limitations and Non-Goals

Being explicit about scope keeps this artifact honest, safe, and clearly
separate from other research.

## What this artifact IS

- An **open-source instrumentation testbed** for benign wireless traffic.
- A **reproducible, educational** toolkit runnable software-only (demo mode) and
  extendable to commodity hardware.
- A demonstration of **observability** (packet rate, inter-arrival, jitter proxy,
  completeness, periodicity) across four wireless technologies.

## What this artifact is NOT (non-goals)

| Non-goal | Why it is excluded |
|----------|--------------------|
| Advanced retry/cooldown scheduling | Belongs to a separate main paper; only referenced as external motivation / future work. |
| Analytical loss/availability models | Out of scope; not implemented or reproduced here. |
| Full network-simulation campaigns | Out of scope; this artifact uses synthetic traces + light analysis. |
| Certified IEEE 802.11ax PHY/MAC validation | This is observability, not standards-grade validation. |
| Anti-jamming / interference mitigation product | No jamming or mitigation is implemented; safety policy forbids it. |
| Safety / SIL / PROFIsafe / certified protection | No safety-certification claims are made. |
| Deployment-ready industrial product | This is a teaching/research artifact, not a product. |

## Measurement limitations

- **Latency** is a *proxy* (UDP send/recv timestamps or synthetic timing), not a
  calibrated end-to-end industrial latency measurement.
- **RSSI/channel** fields are optional and best-effort; demo values are synthetic.
- **Completeness/loss indicators** use per-node sequence IDs; without sequence
  IDs (some real captures), loss cannot be inferred precisely.
- **Clock synchronisation** across nodes is not guaranteed; cross-node latency
  comparisons require explicit time sync (out of scope by default).
- **SDR** support is **receive-only** and intended for channel-occupancy and
  event-timing observation, not demodulation guarantees.

## Safety/legal limitations

- No transmission of interference; no jamming; no attack tooling.
- Real capture restricted to **owned/authorised** interfaces.
- Local laws on radio, privacy, and wiretapping apply and are the user's
  responsibility.

## Relationship to advanced scheduling research (firewall)

This repository intentionally **does not** disclose, implement, or reproduce
advanced cooldown-on-failure scheduling, its analytical models, or its
comparative simulation results. Such scheduling appears here only as **external
motivation** and **future work**, never as an implemented contribution.
