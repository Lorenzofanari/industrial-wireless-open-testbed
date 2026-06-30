# Security and responsible-use policy

## Scope of this artifact

This project is a software-only synthetic packet-observability and
reproducibility workflow, with optional passive / receive-only observation
extensions. By design it contains **no** offensive functionality: no jamming,
flooding, deauthentication, exploitation, or unauthorised scanning, and no
interference transmission. The synthetic demo mode emits no radio signal and
touches no network interface.

## Responsible use

- Use the optional owned-device and receive-only extensions only on devices,
  networks, and bands you own or are explicitly authorised to use.
- Comply with all applicable radio, privacy, and wiretap regulations in your
  jurisdiction.
- See [`docs/safety_and_ethics.md`](docs/safety_and_ethics.md) and
  [`hardware/safety_notes.md`](hardware/safety_notes.md).

## Reporting a vulnerability or a misuse concern

If you discover a security issue in the code, or a way the artifact could be
misused contrary to the policy above, please open a private report to the
maintainers (replace with the project's preferred private contact before
publication) rather than filing a public issue. Please include:

- a description of the issue and its impact;
- steps to reproduce, if applicable;
- any suggested remediation.

We aim to acknowledge reports promptly and to address confirmed issues in a
timely manner.

## Supported versions

This is an early-stage research artifact. Security-relevant fixes are applied to
the latest version on the default branch.
