"""Optional owned-device and receive-only extensions.

These tools are NOT part of the software-only synthetic demo workflow. They are
provided to support the tiered adoption model described in
``hardware/adoption_tiers.md``: capturing benign traffic on devices and networks
you own or are explicitly authorised to use, and receive-only observation.

Safety policy (enforced by these tools)
---------------------------------------
* Passive / receive-only by design: they never transmit interference, never
  scan or target third-party devices, and provide no jamming, flooding,
  deauthentication, or exploitation functionality.
* Capture and replay helpers default to a dry-run and require an explicit
  ``--confirm-owned`` flag before touching a real interface.
* The user is responsible for legal compliance in their jurisdiction.
"""
