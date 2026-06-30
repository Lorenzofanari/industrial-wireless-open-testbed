# Receive-only SDR extension notes

The optional SDR tier (Tier 4) supports **receive-only** observation of legally
observable sub-GHz activity. It is not required for the software-only demo, and
the `lora_sdr_like` case study runs fully in synthetic demo mode without any
radio.

## Principles

- **Receive-only.** The SDR is used to observe only. It never transmits, and the
  artifact provides no transmit, active-probing, or signal-disruption path.
- **Legally observable bands only.** Observe only the bands you may lawfully
  observe in your jurisdiction; radio and privacy regulations vary by country
  and are your responsibility.
- **Owned/authorised context.** Use the extension in a controlled laboratory
  setting on activity you are authorised to observe.

## Typical receive-only chain

```
[antenna] --- [RTL-SDR-class receive-only dongle] --- USB --- [PC: logging]
```

Logged observations can be mapped onto the canonical `packets.csv` schema (event
timestamps, logical identifiers, sizes, optional channel metadata) and then fed
into the same metrics-to-figures pipeline used by the synthetic demo.

## Scope

This extension is for channel-occupancy and event-timing **observation**. It is
not a demodulation guarantee and makes no standard-conformance or real
radio-performance claim. See
[`../docs/limitations_and_non_goals.md`](../docs/limitations_and_non_goals.md)
and [`safety_notes.md`](safety_notes.md).
