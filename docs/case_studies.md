# Case studies

The artifact ships four **technology-like** case-study profiles. Each is a
configurable synthetic traffic profile over one common toolchain. They are named
`*_like` deliberately: they reproduce the *shape* of a packet stream for
teaching and pipeline demonstration, and are **not** standard-conformant
implementations or validations of the named technologies.

| Case | Config | Profile focus |
|------|--------|---------------|
| Wi-Fi-like | `configs/wifi_like.yaml` | Packet observability of short-range benign traffic between owned nodes. |
| BLE/IIoT-like | `configs/ble_like.yaml` | Low-rate telemetry periodicity, missing samples, gateway logging. |
| IEEE 802.15.4/Zigbee-like | `configs/ieee802154_like.yaml` | Low-power, low-rate constrained-payload sensing. |
| LoRa/Sub-GHz/SDR-like | `configs/lora_sdr_like.yaml` | Long-range, low-rate event logging; optional receive-only SDR. |

## Default profile parameters

| Case | Nodes | Sizes (B) | Intervals (ms) | Duration (s) | Repetitions | Seed |
|------|-------|-----------|----------------|--------------|-------------|------|
| Wi-Fi-like | 4 | 128 / 256 / 512 | 20 / 50 / 100 | 60 | 5 | 12345 |
| BLE/IIoT-like | 4 | 20 / 32 / 64 | 250 / 500 / 1000 | 120 | 5 | 22345 |
| IEEE 802.15.4-like | 5 | 32 / 64 / 96 | 500 / 1000 / 2000 | 180 | 5 | 32345 |
| LoRa/SDR-like | 3 | 12 / 24 / 51 | 1000 / 5000 / 10000 | 300 | 3 | 42345 |

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
