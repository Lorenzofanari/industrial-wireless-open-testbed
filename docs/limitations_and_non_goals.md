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

| Non-goal | Statement |
|----------|-----------|
| Anti-jamming / interference mitigation | The artifact does not detect, mitigate, or protect against interference, and provides no such capability. |
| Offensive cybersecurity functionality | The artifact provides no jamming, flooding, deauthentication, exploitation, or unauthorised scanning. |
| Wireless scheduler | The artifact does not implement or evaluate any scheduling algorithm. |
| Standard implementation / validation | The artifact does not implement or validate Wi-Fi, BLE, IEEE 802.15.4/Zigbee, LoRa, or SDR standards; profiles are technology-like, not standard-conformant. |
| Real radio-performance claim | Synthetic demo-mode outputs are not real radio measurements and assert no real radio performance. |
| Industrial reliability | The artifact makes no industrial-grade reliability claim. |
| Safety certification | The artifact makes no safety, SIL, or certification claim. |

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
[`paper_alignment.md`](paper_alignment.md) for how these boundaries map to the
paper's safety firewall (contribution C6).
