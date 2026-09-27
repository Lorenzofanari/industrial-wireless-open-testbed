# Quickstart

This guide takes you from a clean clone to regenerated metrics, figures, and
manifests in a few minutes — **no hardware required**. Everything here runs in
synthetic demo mode: no radio emission, no network interface.

## 1. Clone

```bash
git clone https://github.com/Lorenzofanari/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
```

For the paper artifact, check out the corrected release used for the revised
evaluation:

```bash
git checkout v0.1.1
```

(`v0.1.0` is the previous, archived baseline; it is kept unchanged for
provenance. See `CHANGELOG.md` for the differences.)

## 2. Create an environment

Using `venv`:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Or using conda:

```bash
conda env create -f environment.yml
conda activate packet-observability
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# or, to install the package and dev tools:
python -m pip install -e ".[dev]"
```

Runtime dependencies are `numpy`, `pandas`, `matplotlib`, and `PyYAML`.

## 4. Run the synthetic demo

One case study:

```bash
python scripts/run_demo.py --config configs/wifi_like.yaml --out results/demo/wifi_like
```

All four reference workload profiles (W1–W4; see
[`case_studies.md`](case_studies.md) for the W1–W4 → config-file mapping):

```bash
python scripts/run_demo.py --all
```

## 5. Or run each step individually

```bash
# Generate a synthetic trace
python scripts/generate_traces.py --config configs/wifi_like.yaml \
    --out results/demo/wifi_like/packets.csv

# Compute metrics
python scripts/compute_metrics.py --input results/demo/wifi_like/packets.csv

# Generate figures
python scripts/plot_results.py --input results/demo/wifi_like/packets.csv \
    --out-dir results/demo/wifi_like/figures
```

## 6. Verify reproducibility

```bash
python scripts/verify_reproducibility.py --all
```

This confirms that each trace is regenerated identically (by SHA-256) and that
it matches the committed canonical reference in `data/synthetic_demo/`.

## 7. Run the tests

```bash
pytest
```

## 8. Inspect outputs

```
results/demo/wifi_like/
├── packets.csv
├── metrics.csv
├── metrics_summary.json
├── inter_arrival.csv
├── manifest.json
└── figures/
    ├── packet_count_over_time.png
    ├── inter_arrival_distribution.png
    ├── packet_size_distribution.png
    └── per_node_packet_count.png
```

## Next steps

- [`reproducibility_protocol.md`](reproducibility_protocol.md)
- [`case_studies.md`](case_studies.md)
- [`limitations_and_non_goals.md`](limitations_and_non_goals.md)
