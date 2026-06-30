# Installation

> Demo mode works fully offline and needs only Python + a few packages. Hardware
> is optional and only required for Phase 2 real-capture experiments.

## 1. Prerequisites

- **Python 3.9 or newer** (`python --version`).
- **pip** (bundled with modern Python).
- Linux is recommended; macOS and Windows also work for demo mode.

## 2. Get the code

```bash
git clone https://example.org/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
```

## 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Or install the package (editable) with dev extras:

```bash
python -m pip install -e ".[dev]"
```

Runtime dependencies: `numpy`, `pandas`, `matplotlib`, `PyYAML`.
(`seaborn` is intentionally **not** used.)

## 5. Verify the install (smoke test)

```bash
python -m src.capture.synthetic_capture_generator --config configs/case_wifi_latency.yaml
python -m src.analysis.compute_metrics --input results/case_wifi_latency/run01/packets.csv
```

You should see a `results/case_wifi_latency/run01/` directory with
`packets.csv`, `metrics.csv`, `metrics_summary.json`, and `manifest.json`.

Run the unit tests (optional):

```bash
pytest
```

## 6. Optional: real-capture tooling (Phase 2)

For real packet capture you additionally need:

- **Wireshark / tshark** on `PATH` (`tshark --version`).
- Appropriate OS permissions to capture on an interface you **own**.
- Optional radios from [`hardware/bill_of_materials.csv`](../hardware/bill_of_materials.csv).

> ⚠️ Real capture is **dry-run by default** and requires `--confirm-owned`.
> Read [`hardware/safety_notes.md`](../hardware/safety_notes.md) first.

## Troubleshooting

- **`ModuleNotFoundError: src`** — run commands from the repository root using
  `python -m src.<...>` so the package is importable.
- **No figures produced** — ensure `matplotlib` installed; the toolkit uses the
  headless `Agg` backend, so no display is required.
- **`tshark: command not found`** — install Wireshark, or stay in demo mode.
