"""The synthetic generator must be deterministic for a fixed seed."""
from pathlib import Path

import pytest

from packet_observability.hash_utils import sha256_file
from packet_observability.io import CSV_FIELDS, load_config, write_packets_csv
from packet_observability.synthetic_generator import generate_packets

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"
ALL_CONFIGS = sorted(CONFIG_DIR.glob("*.yaml"))
WIFI = CONFIG_DIR / "wifi_like.yaml"


def test_same_seed_same_records():
    cfg = load_config(WIFI)
    assert generate_packets(cfg, seed=123) == generate_packets(cfg, seed=123)


def test_different_seed_changes_records():
    cfg = load_config(WIFI)
    assert generate_packets(cfg, seed=1) != generate_packets(cfg, seed=2)


def test_same_seed_same_file_hash(tmp_path):
    cfg = load_config(WIFI)
    a = write_packets_csv(generate_packets(cfg, seed=7), tmp_path / "a.csv")
    b = write_packets_csv(generate_packets(cfg, seed=7), tmp_path / "b.csv")
    assert sha256_file(a) == sha256_file(b)


def test_records_have_canonical_fields():
    cfg = load_config(WIFI)
    records = generate_packets(cfg, seed=7)
    assert records, "generator produced no records"
    for field in CSV_FIELDS:
        assert field in records[0]


def test_timestamps_sorted():
    cfg = load_config(WIFI)
    ts = [r["timestamp"] for r in generate_packets(cfg, seed=9)]
    assert ts == sorted(ts)


def test_missing_sample_model_creates_gaps():
    cfg = load_config(WIFI)
    full = generate_packets(cfg, seed=5, drop_probability=0.0)
    dropped = generate_packets(cfg, seed=5, drop_probability=0.3)
    assert len(dropped) < len(full)


@pytest.mark.parametrize("config_path", ALL_CONFIGS, ids=lambda p: p.stem)
def test_every_config_generates_deterministically(config_path):
    cfg = load_config(config_path)
    assert generate_packets(cfg) == generate_packets(cfg)
