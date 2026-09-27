"""Independent regression tests for the metric implementation.

Every packet table in this module is written out **by hand** and every expected
value is derived **analytically** in the test body. Nothing here is produced by
``packet_observability.synthetic_generator``; the purpose is to validate the
metric implementation against ground truth that does not share code with the
data generator.

Covered:
  * Equation (4): span-based event rate ``(N - 1) / (t_max - t_min)``.
  * Mean inter-event interval.
  * Missing / duplicate sequence identifiers.
  * Independent per-node timing.
  * Boundary inputs: empty trace, one-record trace, zero span, invalid
    timestamps, missing mandatory columns, non-positive packet sizes.
"""
from __future__ import annotations

import math

import pandas as pd
import pytest

from packet_observability.metrics import compute_metrics, span_event_rate


def _table(rows: list[dict]) -> pd.DataFrame:
    """Build a packets table from hand-written rows, filling optional columns."""
    df = pd.DataFrame(rows)
    for col, default in (
        ("node_id", "n0"),
        ("packet_size_bytes", 64),
        ("packet_id", None),
        ("rssi_dbm", -60),
        ("channel", 1),
        ("payload_type", "manual"),
    ):
        if col not in df.columns:
            df[col] = default if default is not None else range(len(df))
    return df


# ---------------------------------------------------------------------------
# TEST A - analytical event rate and inter-event interval
# ---------------------------------------------------------------------------

def test_a_span_rate_three_timestamps_two_intervals():
    """Timestamps [0.0, 0.5, 1.0]: N = 3, span = 1.0 s, 2 intervals -> 2.0 pkt/s."""
    timestamps = [0.0, 0.5, 1.0]
    n_observed = 3
    span_s = 1.0 - 0.0
    n_intervals = n_observed - 1          # = 2
    expected_rate = n_intervals / span_s  # = 2.0 packets / s

    assert n_intervals == 2
    assert expected_rate == 2.0

    # Canonical estimator directly.
    assert span_event_rate(timestamps) == pytest.approx(2.0)

    # Through the full metric pipeline.
    m = compute_metrics(_table([{"timestamp": t, "sequence_id": i + 1} for i, t in enumerate(timestamps)]))
    assert m["total_packets"] == 3
    assert m["duration_s"] == pytest.approx(1.0)
    assert m["packet_rate_pps"] == pytest.approx(2.0)
    # The old N / span estimator would have returned 3.0; make the regression explicit.
    assert m["packet_rate_pps"] != pytest.approx(3.0)


def test_a_mean_inter_event_interval_is_500ms():
    """Timestamps [0.0, 0.5, 1.0] contain two 0.5 s gaps -> mean gap 500 ms."""
    timestamps = [0.0, 0.5, 1.0]
    gaps_s = [0.5 - 0.0, 1.0 - 0.5]
    expected_mean_gap_ms = (sum(gaps_s) / len(gaps_s)) * 1000.0  # = 500.0 ms

    assert expected_mean_gap_ms == 500.0

    m = compute_metrics(_table([{"timestamp": t, "sequence_id": i + 1} for i, t in enumerate(timestamps)]))
    assert m["inter_arrival_mean_ms"] == pytest.approx(500.0)
    assert m["inter_arrival_std_ms"] == pytest.approx(0.0)
    assert m["jitter_proxy_ms"] == pytest.approx(0.0)


@pytest.mark.parametrize(
    "timestamps, expected_rate",
    [
        ([0.0, 1.0], 1.0),                       # 1 interval over 1 s
        ([10.0, 10.1, 10.2, 10.3, 10.4], 10.0),  # 4 intervals over 0.4 s
        ([0.0, 0.25, 0.5, 0.75, 1.0], 4.0),      # 4 intervals over 1 s
        ([5.0, 7.0, 8.0], 2.0 / 3.0),            # irregular: 2 intervals over 3 s
        ([5.0, 6.0, 8.0, 9.0], 0.75),            # irregular: 3 intervals over 4 s
    ],
)
def test_a_span_rate_additional_analytical_cases(timestamps, expected_rate):
    assert span_event_rate(timestamps) == pytest.approx(expected_rate)
    m = compute_metrics(_table([{"timestamp": t} for t in timestamps]))
    # The pipeline reports the rate rounded to 4 decimals (existing convention).
    assert m["packet_rate_pps"] == pytest.approx(expected_rate, abs=5e-5)


def test_a_span_rate_is_order_independent():
    """Unsorted input must give the same estimate as sorted input."""
    assert span_event_rate([1.0, 0.0, 0.5]) == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# TEST B - missing and duplicate sequence identifiers
# ---------------------------------------------------------------------------

def test_b_missing_and_duplicate_sequence_ids():
    """Sequence ids [1, 3, 3] on one node -> 1 missing (id 2), 1 duplicate (id 3)."""
    sequence_ids = [1, 3, 3]
    observed = len(sequence_ids)                      # 3
    unique = len(set(sequence_ids))                   # 2  -> {1, 3}
    expected_span = max(sequence_ids) - min(sequence_ids) + 1  # 3 -> {1, 2, 3}
    expected_missing = expected_span - unique         # 1  -> id 2 never seen
    expected_duplicate = observed - unique            # 1  -> id 3 seen twice

    assert expected_missing == 1
    assert expected_duplicate == 1

    df = _table(
        [
            {"timestamp": 0.0, "node_id": "n0", "sequence_id": 1},
            {"timestamp": 0.1, "node_id": "n0", "sequence_id": 3},
            {"timestamp": 0.2, "node_id": "n0", "sequence_id": 3},
        ]
    )
    m = compute_metrics(df)
    assert m["missing_sequence_ids"] == 1
    assert m["duplicate_sequence_ids"] == 1
    # Completeness = unique observed / expected span = 2 / 3.
    assert m["capture_completeness"] == pytest.approx(2 / 3, abs=1e-4)


def test_b_complete_sequence_has_no_missing_or_duplicates():
    df = _table([{"timestamp": 0.1 * i, "sequence_id": i + 1} for i in range(5)])
    m = compute_metrics(df)
    assert m["missing_sequence_ids"] == 0
    assert m["duplicate_sequence_ids"] == 0
    assert m["capture_completeness"] == pytest.approx(1.0)


def test_b_sequence_metrics_are_per_node():
    """Identical ids on *different* nodes are not duplicates."""
    df = _table(
        [
            {"timestamp": 0.0, "node_id": "a", "sequence_id": 1},
            {"timestamp": 0.1, "node_id": "b", "sequence_id": 1},
            {"timestamp": 0.2, "node_id": "a", "sequence_id": 2},
            {"timestamp": 0.3, "node_id": "b", "sequence_id": 2},
        ]
    )
    m = compute_metrics(df)
    assert m["missing_sequence_ids"] == 0
    assert m["duplicate_sequence_ids"] == 0


# ---------------------------------------------------------------------------
# TEST C - independent per-node timing
# ---------------------------------------------------------------------------

def test_c_per_node_mean_gaps_100ms_and_250ms():
    """Node A spaced 0.1 s, node B spaced 0.25 s -> 100 ms and 250 ms mean gaps."""
    spacing_a_s = 0.1
    spacing_b_s = 0.25
    expected_gap_a_ms = spacing_a_s * 1000.0   # 100 ms
    expected_gap_b_ms = spacing_b_s * 1000.0   # 250 ms
    assert expected_gap_a_ms == 100.0
    assert expected_gap_b_ms == 250.0

    rows = []
    for i in range(6):   # A: 0.0, 0.1, ..., 0.5
        rows.append({"timestamp": i * spacing_a_s, "node_id": "A", "sequence_id": i + 1})
    for i in range(4):   # B: 0.0, 0.25, 0.5, 0.75
        rows.append({"timestamp": i * spacing_b_s, "node_id": "B", "sequence_id": i + 1})

    m = compute_metrics(_table(rows))
    gaps = m["per_node_inter_arrival_mean_ms"]
    assert set(gaps) == {"A", "B"}
    assert gaps["A"] == pytest.approx(100.0)
    assert gaps["B"] == pytest.approx(250.0)
    assert m["per_node_packet_counts"] == {"A": 6, "B": 4}
    assert m["n_nodes"] == 2


def test_c_per_node_gap_is_independent_of_interleaving():
    """Interleaved streams must not leak each other's timestamps into the gap."""
    rows = [
        {"timestamp": 0.00, "node_id": "A"},
        {"timestamp": 0.05, "node_id": "B"},
        {"timestamp": 0.10, "node_id": "A"},
        {"timestamp": 0.30, "node_id": "B"},
        {"timestamp": 0.20, "node_id": "A"},
        {"timestamp": 0.55, "node_id": "B"},
    ]
    m = compute_metrics(_table(rows))
    gaps = m["per_node_inter_arrival_mean_ms"]
    assert gaps["A"] == pytest.approx(100.0)
    assert gaps["B"] == pytest.approx(250.0)


# ---------------------------------------------------------------------------
# Boundary tests
# ---------------------------------------------------------------------------

def test_boundary_empty_trace_raises():
    empty = pd.DataFrame(columns=["timestamp", "node_id", "packet_size_bytes", "sequence_id"])
    with pytest.raises(ValueError):
        compute_metrics(empty)


def test_boundary_one_record_trace_has_undefined_rate():
    m = compute_metrics(_table([{"timestamp": 12.5, "sequence_id": 1}]))
    assert m["total_packets"] == 1
    assert m["duration_s"] == 0.0
    assert math.isnan(m["packet_rate_pps"])
    assert math.isnan(m["inter_arrival_mean_ms"])
    assert math.isnan(m["inter_arrival_std_ms"])
    assert math.isnan(m["per_node_inter_arrival_mean_ms"]["n0"])
    assert span_event_rate([12.5]) != span_event_rate([12.5])  # NaN is not equal to itself


def test_boundary_zero_timestamp_span_has_undefined_rate():
    """Several records with identical timestamps: N >= 2 but t_max == t_min."""
    m = compute_metrics(_table([{"timestamp": 3.0} for _ in range(4)]))
    assert m["total_packets"] == 4
    assert m["duration_s"] == 0.0
    assert math.isnan(m["packet_rate_pps"])
    assert math.isnan(span_event_rate([3.0, 3.0, 3.0, 3.0]))
    # Inter-arrival statistics remain defined (all gaps are exactly zero).
    assert m["inter_arrival_mean_ms"] == pytest.approx(0.0)


def test_boundary_invalid_timestamps_are_discarded():
    """Non-numeric / non-finite timestamps do not count towards N or the span."""
    rows = [
        {"timestamp": 0.0},
        {"timestamp": "not-a-number"},
        {"timestamp": None},
        {"timestamp": float("nan")},
        {"timestamp": float("inf")},
        {"timestamp": 0.5},
        {"timestamp": 1.0},
    ]
    m = compute_metrics(_table(rows))
    assert m["total_packets"] == 3
    assert m["duration_s"] == pytest.approx(1.0)
    assert m["packet_rate_pps"] == pytest.approx(2.0)
    assert span_event_rate([0.0, float("nan"), 0.5, float("inf"), 1.0]) == pytest.approx(2.0)


def test_boundary_all_timestamps_invalid_raises():
    with pytest.raises(ValueError):
        compute_metrics(_table([{"timestamp": "x"}, {"timestamp": None}]))


def test_boundary_span_event_rate_direct_edge_cases():
    assert math.isnan(span_event_rate([]))
    assert math.isnan(span_event_rate([1.0]))
    assert math.isnan(span_event_rate([1.0, 1.0]))
    assert math.isnan(span_event_rate([float("nan"), float("nan")]))
    assert math.isnan(span_event_rate([float("nan"), 2.0]))
    # Non-numeric entries are ignored, not counted.
    assert math.isnan(span_event_rate(["x", "y", 2.0]))
    assert span_event_rate(["x", 0.0, "1.0"]) == pytest.approx(1.0)


@pytest.mark.parametrize("missing_column", ["timestamp", "node_id", "packet_size_bytes"])
def test_boundary_missing_required_column_raises(missing_column):
    df = _table([{"timestamp": 0.0, "sequence_id": 1}, {"timestamp": 1.0, "sequence_id": 2}])
    df = df.drop(columns=[missing_column])
    with pytest.raises(ValueError, match=missing_column):
        compute_metrics(df)


def test_boundary_missing_sequence_column_yields_undefined_sequence_metrics():
    df = _table([{"timestamp": 0.0}, {"timestamp": 1.0}])
    assert "sequence_id" not in df.columns
    m = compute_metrics(df)
    assert m["missing_sequence_ids"] == 0
    assert m["duplicate_sequence_ids"] == 0
    assert math.isnan(m["capture_completeness"])
    assert m["packet_rate_pps"] == pytest.approx(1.0)


def test_boundary_non_positive_packet_sizes_are_excluded_from_size_statistics():
    rows = [
        {"timestamp": 0.0, "packet_size_bytes": 100},
        {"timestamp": 0.5, "packet_size_bytes": 0},        # invalid: not positive
        {"timestamp": 1.0, "packet_size_bytes": -7},       # invalid: negative
        {"timestamp": 1.5, "packet_size_bytes": "abc"},    # invalid: non-numeric
        {"timestamp": 2.0, "packet_size_bytes": 300},
    ]
    m = compute_metrics(_table(rows))
    # Timing metrics still use all five valid timestamps.
    assert m["total_packets"] == 5
    assert m["packet_rate_pps"] == pytest.approx(4 / 2.0)
    # Only the two valid sizes contribute: (100 + 300) / 2 = 200.
    assert m["mean_packet_size_bytes"] == pytest.approx(200.0)
    assert sorted(m["_packet_size_series"]) == [100.0, 300.0]
