# Metrics

Metrics are computed from a canonical `packets.csv` by
`src/packet_observability/metrics.py`. Scalar metrics are written to
`metrics.csv` (long form) and `metrics_summary.json`; the per-packet
inter-arrival series is written to `inter_arrival.csv`.

## Definitions

| Metric | Definition |
|--------|------------|
| `total_packets` | Number of packet rows in the trace. |
| `duration_s` | `max(timestamp) - min(timestamp)`, in seconds. |
| `packet_rate_pps` | `total_packets / duration_s` (packets per second). |
| `mean_packet_size_bytes` | Mean of `packet_size_bytes`. |
| `inter_arrival_mean_ms` | Mean of successive timestamp differences, in ms. |
| `inter_arrival_std_ms` | Population standard deviation of inter-arrival times, in ms. |
| `jitter_proxy_ms` | Jitter proxy, defined here as `inter_arrival_std_ms`. |
| `missing_sequence_ids` | Sum over nodes of gaps in the observed per-node sequence range. |
| `duplicate_sequence_ids` | Sum over nodes of repeated per-node sequence ids. |
| `capture_completeness` | Observed unique sequences / expected sequence span, across all nodes, in `(0, 1]`. |
| `per_node_packet_counts` | Mapping of `node_id` → packet count. |

`n_nodes` (the number of distinct `node_id` values) is also reported.

## Notes

- **Jitter proxy.** `jitter_proxy_ms` is explicitly a *proxy* (the standard
  deviation of inter-arrival times), not a calibrated jitter measurement.
- **Completeness and loss.** Missing/duplicate counts and completeness rely on
  per-node `sequence_id`. Traces without sequence ids cannot express these.
- **Repeatability.** `metrics.repeatability()` aggregates mean/std/min/max of the
  scalar metrics across repeated runs, quantifying run-to-run stability of the
  pipeline.

## Scope

These metrics characterise the **synthetic demo-mode pipeline** (and, optionally,
owned-device observations you collect). They are not measurements of any radio
standard and make no real radio-performance claim. See
[`limitations_and_non_goals.md`](limitations_and_non_goals.md).
