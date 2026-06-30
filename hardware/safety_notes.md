# Safety and legal-use notes (hardware)

These notes apply to **every** optional hardware extension. The software-only
synthetic demo mode emits no radio signal and touches no network interface; read
this page before connecting any radio or observing any traffic.

## Golden rules

1. **Own it or be authorised.** Only observe traffic on devices and networks you
   own or are explicitly authorised to use.
2. **No transmission of interference.** This project provides no jamming,
   deauthentication, flooding, or signal-disruption capability — by design.
3. **Receive-only for spectrum observation.** SDR usage (Tier 4) is strictly
   receive-only on bands you may legally observe in your jurisdiction.
4. **Prefer contained RF.** Use cabled links, attenuators, or a shielded box to
   keep experiments isolated and repeatable.
5. **No third-party data.** Do not observe, store, or analyse traffic from
   networks or persons you are not authorised to monitor.
6. **Know your local law.** Radio, privacy, and wiretap regulations vary by
   country. Compliance is your responsibility.

## What these extensions never do

- They are not an anti-jamming tool and provide no interference mitigation.
- They provide no offensive functionality: no jamming, flooding,
  deauthentication, exploitation, or unauthorised scanning.
- They make no standard-conformance, real radio-performance, industrial
  reliability, or safety-certification claim.

## Default-safe software behaviour

- Capture and replay helpers default to a dry-run and require an explicit
  `--confirm-owned` flag before touching a real interface.
- The UDP telemetry sender enforces a conservative packet-rate cap and is not a
  load generator.
- Synthetic demo mode emits no radio signal and touches no network interface.

## Incident handling

If you observe unexpected interference, stop the experiment, disconnect the
radio, and review your configuration. Report environmental or safety concerns to
your laboratory supervisor.
