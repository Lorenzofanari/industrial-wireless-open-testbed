"""Metric computation on a small, known CSV."""
import pandas as pd
import pytest

from packet_observability.metrics import compute_metrics, repeatability


def _make_df():
    # Two nodes, periodic 100 ms, with one missing sequence id on node "a".
    rows = []
    pid = 0
    for i in range(10):
        for node in ("a", "b"):
            seq = i + 1
            if node == "a" and seq == 5:  # drop -> one missing sequence id
                continue
            rows.append(
                {
                    "timestamp": i * 0.1 + (0.0 if node == "a" else 0.05),
                    "node_id": node,
                    "packet_id": pid,
                    "packet_size_bytes": 100,
                    "rssi_dbm": -60,
                    "channel": 36,
                    "sequence_id": seq,
                    "payload_type": "synthetic",
                }
            )
            pid += 1
    return pd.DataFrame(rows)


def test_basic_metrics():
    m = compute_metrics(_make_df())
    assert m["total_packets"] == 19
    assert m["n_nodes"] == 2
    assert m["mean_packet_size_bytes"] == 100.0
    assert m["missing_sequence_ids"] == 1
    assert m["duplicate_sequence_ids"] == 0
    assert 0 < m["capture_completeness"] <= 1.0
    assert "a" in m["per_node_packet_counts"]


def test_duplicate_detection():
    df = _make_df()
    dup = df.iloc[[0]].copy()
    df = pd.concat([df, dup], ignore_index=True)
    m = compute_metrics(df)
    assert m["duplicate_sequence_ids"] >= 1


def test_empty_raises():
    with pytest.raises(ValueError):
        compute_metrics(pd.DataFrame(columns=["timestamp", "node_id", "sequence_id", "packet_size_bytes"]))


def test_repeatability_aggregation():
    summaries = [
        {"packet_rate_pps": 10.0, "capture_completeness": 1.0},
        {"packet_rate_pps": 12.0, "capture_completeness": 0.9},
    ]
    rep = repeatability(summaries)
    assert rep["n_runs"] == 2
    assert rep["metrics"]["packet_rate_pps"]["mean"] == 11.0
    assert "capture_completeness" in rep["metrics"]
