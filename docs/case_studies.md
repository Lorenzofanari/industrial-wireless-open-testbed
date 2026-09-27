# Case studies

The artifact ships four synthetic **reference workload profiles**, `W1`–`W4`,
over one common toolchain. In scientific-facing text (manuscript, figures,
tables, reports) the profiles are referred to by their neutral identifiers
`W1`–`W4`. The YAML configuration files keep their historical `*_like` names
for backward compatibility; the `*_like` wording is only a loose description
of the *shape* of the packet stream that inspired each profile. The profiles
are **not** standard-conformant implementations or validations of any named
technology.

## W1–W4 mapping

| Profile | Config file (unchanged for compatibility) | `experiment_id` | Informal description | Profile focus |
|---------|-------------------------------------------|-----------------|----------------------|---------------|
| **W1** | `configs/wifi_like.yaml` | `wifi_like` | high-rate, short-interval, larger frames | Packet observability of short-range benign traffic between owned nodes. |
| **W2** | `configs/ble_like.yaml` | `ble_like` | low-rate periodic telemetry, small frames | Telemetry periodicity, missing samples, gateway logging. |
| **W3** | `configs/ieee802154_like.yaml` | `ieee802154_like` | low-power, low-rate constrained payloads | Constrained-payload sensing. |
| **W4** | `configs/lora_sdr_like.yaml` | `lora_sdr_like` | very low-rate, long-interval event logging | Long-interval event logging; optional receive-only SDR. |

Command-line tools print both identifiers, e.g. `W1 (wifi_like)`, and the
`experiment_id` values (and therefore output directory names) are unchanged.

## Default profile parameters

| Profile | Nodes | Sizes (B) | Intervals (ms) | Duration (s) | Repetitions | Seed |
|---------|-------|-----------|----------------|--------------|-------------|------|
| W1 (`wifi_like`) | 4 | 128 / 256 / 512 | 20 / 50 / 100 | 60 | 5 | 12345 |
| W2 (`ble_like`) | 4 | 20 / 32 / 64 | 250 / 500 / 1000 | 120 | 5 | 22345 |
| W3 (`ieee802154_like`) | 5 | 32 / 64 / 96 | 500 / 1000 / 2000 | 180 | 5 | 32345 |
| W4 (`lora_sdr_like`) | 3 | 12 / 24 / 51 | 1000 / 5000 / 10000 | 300 | 3 | 42345 |

The synthetic generator uses the first value of each list by default. The
remaining values document the intended profile sweep.

## Important scope note

- These profiles are **not standard-conformant** implementations of Wi-Fi, BLE,
  IEEE 802.15.4/Zigbee, or LoRa, and they perform **no standard validation**.
- The channel/band fields in the configs are cosmetic labels for a
  technology-like profile, not real PHY/MAC parameters.
- Synthetic demo-mode outputs are not real radio measurements.

See [`limitations_and_non_goals.md`](limitations_and_non_goals.md) for the full
scope statement, and [`../hardware/adoption_tiers.md`](../hardware/adoption_tiers.md)
for how each case study can optionally extend to owned-device or receive-only
observation.
