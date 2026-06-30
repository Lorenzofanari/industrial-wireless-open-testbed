# Safety and ethics

This artifact is safe by design. The software-only synthetic demo mode emits no
radio signal and touches no network interface. Optional hardware extensions are
passive or receive-only and are restricted to owned/authorised use.

## Safe-by-design principles

- **Synthetic mode emits no RF.** Demo mode only reads YAML files and writes
  CSV/JSON/PNG files.
- **Receive-only SDR only observes.** The optional SDR extension never transmits
  and performs no active probing.
- **Owned-device observation only.** Optional capture applies solely to devices
  and networks you own or are explicitly authorised to use, in controlled
  laboratory settings.
- **Default-safe tooling.** Capture and replay helpers default to a dry-run and
  require an explicit `--confirm-owned` flag; the telemetry sender is
  rate-capped and is not a load generator.

## Prohibited usage

This artifact must not be used for, and provides no support for:

- jamming or any interference transmission;
- flooding or load/stress generation against networks;
- deauthentication or any disruption of other devices;
- exploitation of vulnerabilities;
- unauthorised scanning or observation of third-party networks or persons;
- any activity that is unlawful in your jurisdiction.

## Your responsibilities

- Observe only what you own or are authorised to observe.
- Comply with all applicable radio, privacy, and wiretap regulations.
- Prefer cabled, attenuated, or shielded setups to keep experiments contained.

See [`../hardware/safety_notes.md`](../hardware/safety_notes.md) for the hardware
use policy and [`limitations_and_non_goals.md`](limitations_and_non_goals.md) for
the full scope statement.
