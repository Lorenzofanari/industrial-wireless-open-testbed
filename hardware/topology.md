# Topology and tiers

Simple, text-based topology diagrams for each tier. Tier 0 is software-only and
needs no hardware; Tiers 1–4 are optional, owned-device or receive-only
extensions. None of the topologies transmit interference or target third-party
networks.

## Tier 0 — Software-only (no hardware)

```text
YAML config -> synthetic generator -> packets.csv -> metrics/figures -> manifest
```

Everything runs on a single computer. No radio, no network interface.

## Tier 1 — Owned Wi-Fi observation (optional)

```text
[owned Wi-Fi nodes you control]
        | (benign traffic on a network you own)
   [passive monitor host: owned Wi-Fi adapter] --(pcap)--> packets.csv -> pipeline
```

Passive observation only, on an owned/authorised network. No standard validation.

## Tier 2 — BLE / IEEE 802.15.4 teaching bench (optional)

```text
[owned BLE / 802.15.4 sensor nodes] --> [owned gateway/sink] --(logs)--> packets.csv -> pipeline
```

Owned devices only; low-rate telemetry and low-power sensing observation.

## Tier 3 — Receive-only SDR (optional)

```text
[antenna] --- [RTL-SDR-class receive-only dongle] --- USB --- [PC: logging] -> packets.csv -> pipeline
```

Receive-only. The SDR never transmits; no demodulation guarantee.

## Tier 4 — Contained RF option (optional)

```text
+--------- shielded box / attenuated, cabled bench ---------+
|  [owned nodes] --(contained RF / coax)--> [owned monitor] |
+-----------------------------------------------------------+
                         |
                  packets.csv -> pipeline
```

Improves isolation and repeatability of any owned-device tier.

See [`adoption_tiers.md`](adoption_tiers.md), [`bill_of_materials.csv`](bill_of_materials.csv),
and [`safety_notes.md`](safety_notes.md).
