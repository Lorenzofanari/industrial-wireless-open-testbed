# Limitations and non-goals

Being explicit about scope keeps this artifact honest, safe, and clearly
separated from other work. This page is authoritative for what the artifact does
and does not claim.

## What this artifact is

- An open-source instrumentation and reproducibility workflow for packet-level
  observability.
- A configuration-driven, software-only synthetic demo-mode pipeline.
- A safe educational packet-observability testbed, extensible to owned-device
  and receive-only observation.

## Non-goals (explicit boundaries)

In a single sentence: **this artifact does not implement wireless algorithms,
interference mitigation, offensive cybersecurity functionality, or radio-standard
validation. Its purpose is to teach reproducible packet-observability
workflows.**

Concretely, the following are out of scope and not claimed:

| Out of scope | Statement |
|--------------|-----------|
| Real radio performance | Synthetic demo-mode outputs are not real radio measurements and assert no real radio performance. |
| Radio-standard validation | No implementation or validation of Wi-Fi, BLE, IEEE 802.15.4/Zigbee, LoRa, or SDR standards; profiles are technology-like, not standard-conformant. |
| Offensive cybersecurity | No jamming, flooding, deauthentication, exploitation, or unauthorised scanning. |
| Interference mitigation | No interference detection, mitigation, or protection of any kind. |
| Wireless algorithms | No scheduling or other wireless control algorithm is implemented or evaluated. |
| Industrial certification / deployment readiness | No industrial-grade reliability, safety, SIL, or certification claim; this is a teaching/research artifact. |

The full, concise lists are kept in [`../claims_included.md`](../claims_included.md)
and [`../claims_excluded.md`](../claims_excluded.md).

## Measurement limitations

- **Synthetic results verify the software pipeline only.** They demonstrate that
  the generate → metrics → figures workflow is deterministic and consistent;
  they say nothing about real radio behaviour.
- **Jitter is a proxy** (standard deviation of inter-arrival times), not a
  calibrated measurement.
- **Optional `rssi_dbm` / `channel`** are synthetic labels in demo mode and
  best-effort metadata otherwise.
- **Completeness / loss indicators** depend on per-node sequence identifiers;
  without them, loss cannot be inferred.
- **Receive-only SDR** (optional extension) is for channel-occupancy and
  event-timing observation, not demodulation guarantees.

## Safety / legal boundaries

- No transmission of interference; no offensive functionality.
- Any real observation is restricted to owned/authorised interfaces and bands.
- Local laws on radio, privacy, and wiretapping apply and are the user's
  responsibility.

See [`safety_and_ethics.md`](safety_and_ethics.md) for the use policy and
[`paper_alignment.md`](paper_alignment.md) for how the artifact maps to the
paper's structure.
