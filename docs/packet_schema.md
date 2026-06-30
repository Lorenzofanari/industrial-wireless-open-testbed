# Packet schema

All traces use a single canonical per-packet CSV schema, `packets.csv`. The same
schema is produced by the synthetic generator and by the optional owned-device
capture extension, so the analysis pipeline is identical in every case.

## Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `timestamp` | float | yes | Time in seconds (experiment-relative or epoch). |
| `node_id` | string | yes | Logical node identifier (e.g. `sta_01`, `sensor_02`). |
| `packet_id` | int | yes | Global packet index within the run. |
| `packet_size_bytes` | int | yes | Packet/frame size in bytes. |
| `rssi_dbm` | float | optional | Signal-strength metadata when available; empty otherwise. |
| `channel` | int | optional | Channel/band label when available; empty otherwise. |
| `sequence_id` | int | yes | Per-node sequence number; gaps indicate missing samples. |
| `payload_type` | string | yes | Label, e.g. `synthetic_telemetry` or `captured`. |

The canonical column order is defined by `CSV_FIELDS` in
`src/packet_observability/io.py`.

## Example

```csv
timestamp,node_id,packet_id,packet_size_bytes,rssi_dbm,channel,sequence_id,payload_type
0.0,sta_01,0,128,-72.3,36,1,synthetic_telemetry
0.000572,sta_02,1,115,-62.8,36,1,synthetic_telemetry
0.020298,sta_01,2,121,-56.8,36,2,synthetic_telemetry
```

## Conventions

- **Per-node sequence identifiers.** `sequence_id` increments per `node_id`.
  Missing values within a node's observed range are counted as missing sequence
  ids; repeated values are counted as duplicates (see [`metrics.md`](metrics.md)).
- **Optional fields may be empty.** `rssi_dbm` and `channel` are written as empty
  strings when not applicable to a profile.
- **Timestamps are sorted.** Generated traces are sorted by `timestamp`.

## Note on optional metadata

In synthetic demo mode, `rssi_dbm` and `channel` are synthetic labels for a
technology-like profile. They are not real measurements.
