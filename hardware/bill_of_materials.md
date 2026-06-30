# Bill of materials (indicative)

Costs are approximate and indicative only; they vary by region and vendor. The
artifact runs fully without any of the items below — the minimal demo tier
costs nothing beyond an existing computer.

| Tier | Items | Approx. cost (EUR) |
|------|-------|--------------------|
| **Minimal demo** | Existing PC/laptop with a Python environment | 0 |
| **Basic capture** | Wi-Fi monitor-mode adapter, cables, powered USB hub | ~50 |
| **Multi-technology teaching bench** | Raspberry Pi-class node, BLE dongle, IEEE 802.15.4 sniffer | ~150 |
| **Receive-only SDR extension** | RTL-SDR-class receive-only dongle and antenna | ~40 |
| **Contained RF option** | Shielded box and/or attenuators with coaxial paths | ~170 |

## Notes

- **Minimal demo (0 EUR).** Everything in this repository can be run, taught,
  and reviewed with only an existing computer and the Python dependencies.
- **Basic capture (~50 EUR).** A Wi-Fi adapter that supports monitor mode allows
  passive observation of benign traffic on a network you own.
- **Multi-technology teaching bench (~150 EUR).** A small dedicated node plus a
  BLE dongle and an IEEE 802.15.4 sniffer covers the BLE/IIoT and low-power
  sensing tiers on owned devices.
- **Receive-only SDR extension (~40 EUR).** An RTL-SDR-class dongle is used for
  receive-only observation on legally observable bands; it never transmits.
- **Contained RF option (~170 EUR).** A shielded enclosure or attenuators
  improve isolation and repeatability for any owned-device tier.

All components above are optional. See [`adoption_tiers.md`](adoption_tiers.md)
for how they map to tiers and [`safety_notes.md`](safety_notes.md) for the
mandatory use policy.
