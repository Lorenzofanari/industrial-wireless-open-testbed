# Student worksheet

Complete every section. Keep your answers concise and evidence-based.

## Identification

- **Student name:** _______________________________
- **Date:** _______________________________
- **Selected case profile:** ☐ wifi_like ☐ ble_like ☐ ieee802154_like ☐ lora_sdr_like

## 1. YAML parameters to record

From `configs/<case>.yaml`:

| Parameter | Value |
|-----------|-------|
| `case_name` | |
| `experiment_id` | |
| `random_seed` | |
| `packet_size_bytes` (first value) | |
| `packet_interval_ms` (first value) | |
| `experiment_duration_s` | |
| `number_of_nodes` | |
| `missing_sample_model.drop_probability` | |
| `safety_mode` | |

## 2. Command log

Record the exact commands you ran:

```text
1.
2.
3.
4.
```

## 3. Output files generated

List the files produced under `results/demo/<case>/`:

- [ ] `packets.csv`
- [ ] `metrics.csv`
- [ ] `metrics_summary.json`
- [ ] `inter_arrival.csv`
- [ ] `manifest.json`
- [ ] `figures/*.png`

## 4. Metrics table to fill

| Metric | Value |
|--------|-------|
| `total_packets` | |
| `duration_s` | |
| `packet_rate_pps` | |
| `mean_packet_size_bytes` | |
| `inter_arrival_mean_ms` | |
| `inter_arrival_std_ms` (jitter proxy) | |
| `missing_sequence_ids` | |
| `duplicate_sequence_ids` | |
| `capture_completeness` | |

## 5. Manifest / hash check

- SHA-256 of `packets.csv` (from `manifest.json`): _______________________________
- Did `python scripts/verify_reproducibility.py --all` report **PASS**? ☐ Yes ☐ No

## 6. Interpretation questions

1. Why might the global `inter_arrival_mean_ms` differ from the configured
   per-node interval?
2. What do missing or duplicate sequence identifiers indicate in this synthetic
   trace?
3. How does `capture_completeness` relate to the missing-sample model?

## 7. Safety reflection

State one reason the optional hardware tiers must be owned-device or
receive-only, and one activity this artifact must never be used for.

## 8. Synthetic-vs-real explanation

In two or three sentences, explain why these results verify the software
pipeline but do not measure real radio performance.
