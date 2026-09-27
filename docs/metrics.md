# Metrics

Metrics are computed from a canonical `packets.csv` by
`src/packet_observability/metrics.py`. Scalar metrics are written to
`metrics.csv` (long form) and `metrics_summary.json`; the per-packet
inter-arrival series is written to `inter_arrival.csv`.

## Definitions

| Metric | Definition |
|--------|------------|
| `total_packets` | Number of packet rows with a valid (finite, numeric) timestamp, `N`. |
| `duration_s` | `t_max - t_min = max(timestamp) - min(timestamp)`, in seconds (the observed span). |
| `packet_rate_pps` | Span-based event rate `R_span = (N - 1) / (t_max - t_min)` (packets per second); see below. |
| `mean_packet_size_bytes` | Mean of the valid (positive, numeric) `packet_size_bytes` values. |
| `inter_arrival_mean_ms` | Mean of successive timestamp differences, in ms. |
| `inter_arrival_std_ms` | Population standard deviation of inter-arrival times, in ms. |
| `jitter_proxy_ms` | Jitter proxy, defined here as `inter_arrival_std_ms`. |
| `missing_sequence_ids` | Sum over nodes of gaps in the observed per-node sequence range. |
| `duplicate_sequence_ids` | Sum over nodes of repeated per-node sequence ids. |
| `capture_completeness` | Observed unique sequences / expected sequence span, across all nodes, in `(0, 1]`. |
| `per_node_packet_counts` | Mapping of `node_id` → packet count. |
| `per_node_inter_arrival_mean_ms` | Mapping of `node_id` → mean gap between that node's successive packets, in ms. |

`n_nodes` (the number of distinct `node_id` values) is also reported.

## Span-based event rate (Equation (4))

`N` timestamps delimit exactly `N - 1` observed inter-event intervals, so the
event rate over the observed span is

```
R_span = (N - 1) / (t_max - t_min)        for N >= 2 and t_max > t_min
```

This is implemented once, in `metrics.span_event_rate()`, and every caller
(`compute_metrics`, `compute_from_csv`, `scripts/run_demo.py`,
`scripts/compute_metrics.py`) uses that single function. Release v0.1.0 used
`N / (t_max - t_min)`, which over-estimates the rate by a factor `N / (N - 1)`;
v0.1.1 corrects this.

**Boundary behaviour.** The estimator is *undefined* and reported as `NaN`
(the project convention for undefined metrics) when

- fewer than two usable timestamps are present (`N < 2`), or
- the timestamp span is zero (`t_max <= t_min`, e.g. all timestamps identical).

`duration_s` is still reported (`0.0` in both cases) and the inter-arrival
statistics are `NaN` for `N < 2`.

## Input validation

- **Mandatory columns.** `timestamp`, `node_id` and `packet_size_bytes` must be
  present; otherwise `compute_metrics` raises `ValueError`. An empty table also
  raises `ValueError`.
- **Timestamps.** Values are coerced to numbers. Rows whose timestamp is
  missing, non-numeric or non-finite (`NaN`, `±inf`) are discarded before any
  metric is computed and do not count towards `N`. If no usable row remains,
  `ValueError` is raised.
- **Packet sizes.** Values are coerced to numbers; missing, non-numeric or
  non-positive sizes are treated as invalid and excluded from
  `mean_packet_size_bytes` (timing metrics are unaffected).
- **Sequence identifiers.** `sequence_id` is optional. When the column is
  absent, `missing_sequence_ids` and `duplicate_sequence_ids` are `0` and
  `capture_completeness` is `NaN`; per-row non-numeric ids are ignored.

## Notes

- **Independent verification.** `tests/test_metrics_independent.py` checks
  every definition above against hand-written packet tables with analytically
  derived expected values (e.g. timestamps `[0.0, 0.5, 1.0]` → `2.0` packets/s
  and a `500 ms` mean gap); none of those tables is produced by the synthetic
  generator.
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
