# Build Instructions

## 1. Overview

The artifact is software-only at its core. **Tier 0** requires **no radio
hardware**: a computer with a supported Python version is enough to build, run,
and reproduce the entire workflow. Tiers 1–4 are *optional* educational
extensions for laboratories that own suitable devices; they are owned-device or
receive-only, and they make no standard-validation or real radio-performance
claim.

## 2. Tier 0 — Software-only build

**Requirements**

- Python 3.9 or newer.
- `pip` (bundled with modern Python).
- Runtime dependencies: `numpy`, `pandas`, `matplotlib`, `PyYAML`.

**Copy-paste build**

```bash
git clone https://github.com/Lorenzofanari/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

> **Windows note:** activate the virtual environment with
> `.venv\Scripts\activate` instead of `source .venv/bin/activate`. The remaining
> commands are identical.

**Expected output files** (per case under `results/demo/<case>/`):

- `packets.csv`
- `metrics.csv`
- `metrics_summary.json`
- `inter_arrival.csv`
- `manifest.json`
- `figures/*.png`

`verify_reproducibility.py --all` should report `PASS`, and `pytest` should pass.

## 3. Tier 1 — Basic owned Wi-Fi observation (optional)

Optional extension for observing benign traffic on a Wi-Fi network you own or
are explicitly authorised to use. It uses a passive capture helper that defaults
to a dry-run and requires `--confirm-owned` before touching a real interface. No
offensive tooling is provided, and no standard-validation claim is made. See
[`../hardware/owned_devices_notes.md`](../hardware/owned_devices_notes.md).

## 4. Tier 2 — Multi-technology teaching bench (optional)

Optional BLE and IEEE 802.15.4 educational extension on owned devices, for
observing low-rate telemetry and low-power sensing patterns. Owned devices only.
See [`../hardware/adoption_tiers.md`](../hardware/adoption_tiers.md).

## 5. Tier 3 — Receive-only SDR extension (optional)

Optional receive-only observation on legally observable bands. The SDR is used
to observe only: it never transmits, and there is no demodulation guarantee. See
[`../hardware/receive_only_sdr_notes.md`](../hardware/receive_only_sdr_notes.md).

## 6. Tier 4 — Contained RF option (optional)

Optional use of a shielded box, attenuators, or cabled isolation to improve
repeatability and containment of any owned-device tier. Optional and additive.

## 7. Build verification

After `python scripts/run_demo.py --all`, confirm the following exist for each
case (for example `results/demo/wifi_like/`):

- `results/demo/<case>/packets.csv`
- `results/demo/<case>/metrics.csv`
- `results/demo/<case>/metrics_summary.json`
- `results/demo/<case>/inter_arrival.csv`
- `results/demo/<case>/manifest.json`
- `results/demo/<case>/figures/*.png`

Then run `python scripts/verify_reproducibility.py --all` (expect `PASS`) and
`pytest` (expect all tests to pass).

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError: numpy/pandas/...` | Missing dependency | `python -m pip install -r requirements.txt` inside the activated venv. |
| `SyntaxError` / unexpected failures | Wrong Python version | Use Python 3.9+ (`python --version`). |
| `Permission denied` writing outputs | Running outside the repo or no write access | Run from the repository root; ensure `results/` is writable. |
| Output directory missing | Skipped `run_demo` | Run `python scripts/run_demo.py --all`; directories are created automatically. |
| Reproducibility mismatch (`FAIL`) | Changed generator/config/seed | Regenerate references intentionally (`scripts/generate_traces.py`) and document the change, or revert local edits. |
| CI mismatch | Local Python differs from CI matrix | Test against a supported version (3.9 / 3.11 / 3.12) or use `environment.yml`. |

## 9. Safety notes

All hardware tiers are optional and owned-device or receive-only. Before any
hardware use, read [`safety_and_ethics.md`](safety_and_ethics.md) and
[`../hardware/safety_notes.md`](../hardware/safety_notes.md).
