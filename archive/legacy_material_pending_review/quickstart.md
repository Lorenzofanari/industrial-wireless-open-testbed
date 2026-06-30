# Quickstart

This guide takes you from a fresh clone to figures in a few minutes — **no
hardware required**.

> Safety: everything here runs in demo mode (synthetic data) or on localhost
> loopback. No radio emission, no third-party networks.

## 1. Install

```bash
python -m pip install -r requirements.txt
```

## 2. One command per case study

```bash
bash experiments/run_case_wifi_latency.sh           # Case Study 1
bash experiments/run_case_ble_telemetry.sh          # Case Study 2
bash experiments/run_case_802154_sensing.sh         # Case Study 3
bash experiments/run_case_lora_sdr_observability.sh # Case Study 4
```

Each script:
1. generates several synthetic runs (`run01`, `run02`, …) with different seeds,
2. computes metrics for each run,
3. aggregates a repeatability report,
4. produces figures.

Outputs land under `results/<experiment_id>/`.

## 3. Step-by-step (manual)

```bash
# Generate one synthetic run
python -m src.capture.synthetic_capture_generator \
    --config configs/case_wifi_latency.yaml --run-label run01 --seed 1001

# Compute metrics
python -m src.analysis.compute_metrics \
    --input results/case_wifi_latency/run01/packets.csv

# Make figures
python -m src.analysis.make_plots \
    --input results/case_wifi_latency/run01/packets.csv \
    --out-dir results/case_wifi_latency/figures
```

## 4. Benign live demo on localhost (optional)

Generate *real* UDP telemetry between two processes on your own machine:

```bash
# Terminal A: receiver/logger
python -m src.traffic.udp_telemetry_receiver --port 9999 --duration 15

# Terminal B: sender (rate-limited, localhost)
python -m src.traffic.udp_telemetry_sender \
    --host 127.0.0.1 --port 9999 --interval-ms 50 --packet-size 128 --duration 12
```

Logs are written under `results/_traffic_logs/`. The receiver log includes a
**latency proxy** (recv − send) and lets you detect missing sequence IDs.

## 5. Inspect outputs

```
results/case_wifi_latency/
├── run01/
│   ├── packets.csv
│   ├── metrics.csv
│   ├── metrics_summary.json
│   ├── inter_arrival.csv
│   └── manifest.json
├── run02/ ...
├── repeatability.csv
├── repeatability_summary.json
└── figures/
    ├── packet_count_over_time.png
    ├── inter_arrival_distribution.png
    ├── packet_size_distribution.png
    ├── per_node_packet_count.png
    └── repeatability_summary.png
```

## Next steps

- Real hardware procedures: [`experiment_protocol.md`](experiment_protocol.md).
- Make results reproducible: [`reproducibility.md`](reproducibility.md).
- Understand scope/limits: [`limitations.md`](limitations.md).
