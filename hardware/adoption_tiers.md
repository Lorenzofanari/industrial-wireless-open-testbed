# Adoption tiers

The artifact is designed for staged adoption. Each tier is optional and builds
on the previous one. The synthetic demo mode (Tier 0) is sufficient to run,
teach, and review the entire workflow with no hardware.

| Tier | Name | What it adds | Hardware |
|------|------|--------------|----------|
| 0 | **Software-only demo** | Synthetic traces, metrics, figures, manifests, reproducibility checks. | None (existing PC). |
| 1 | **Owned Wi-Fi devices** | Passive observation of benign traffic between Wi-Fi devices you own. | Wi-Fi monitor-mode adapter. |
| 2 | **BLE / IIoT teaching bench** | Low-rate telemetry observation on owned BLE/IIoT devices. | BLE dongle, small node (e.g. Raspberry Pi-class). |
| 3 | **IEEE 802.15.4 sniffer** | Low-power sensing observation on an owned 802.15.4 testbed. | 802.15.4 sniffer dongle, sensor nodes. |
| 4 | **Receive-only SDR** | Receive-only observation of legally observable sub-GHz activity. | RTL-SDR-class receive-only dongle, antenna. |
| 5 | **Contained RF** | Improves repeatability and isolation of any of the above. | Shielded box and/or attenuators, coaxial paths. |

## Principles across all tiers

- **Observation only.** Every tier is passive or receive-only. None of them
  transmit interference, and none provide jamming, flooding, deauthentication,
  exploitation, or unauthorised scanning.
- **Owned / authorised only.** Tiers 1–5 apply solely to devices and networks
  you own or are explicitly authorised to use.
- **Same workflow.** All tiers feed the same canonical `packets.csv` schema and
  the same metrics-to-figures pipeline, so results are comparable and the
  software-only demo remains the reference.

See [`bill_of_materials.md`](bill_of_materials.md) for indicative costs and
[`safety_notes.md`](safety_notes.md) for the mandatory use policy.
