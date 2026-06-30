"""All shipped case-study configs must be valid and complete."""
from pathlib import Path

import pytest
import yaml

from packet_observability.io import ALLOWED_SAFETY_MODES, load_config

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"
ALL_CONFIGS = sorted(CONFIG_DIR.glob("*.yaml"))
EXPECTED_IDS = {"wifi_like", "ble_like", "ieee802154_like", "lora_sdr_like"}


def test_four_configs_present():
    ids = {p.stem for p in ALL_CONFIGS}
    assert EXPECTED_IDS.issubset(ids)


@pytest.mark.parametrize("config_path", ALL_CONFIGS, ids=lambda p: p.stem)
def test_config_loads_and_validates(config_path):
    cfg = load_config(config_path)
    assert cfg.experiment_id
    assert cfg.technology
    assert cfg.number_of_nodes >= 1
    assert len(cfg.packet_size_bytes) >= 1
    assert len(cfg.packet_interval_ms) >= 1
    assert cfg.experiment_duration_s > 0
    assert cfg.repetitions >= 1
    assert cfg.safety_mode in ALLOWED_SAFETY_MODES


@pytest.mark.parametrize("config_path", ALL_CONFIGS, ids=lambda p: p.stem)
def test_config_documents_scope_and_naming(config_path):
    with config_path.open("r", encoding="utf-8") as fh:
        text = fh.read()
        data = yaml.safe_load(text)
    # Each config must declare a human-readable case name and an output naming
    # convention, and carry an explicit technology-like (not standard) note.
    assert "case_name" in data
    assert "missing_sample_model" in data
    assert "output_naming" in data
    assert "TECHNOLOGY-LIKE" in text.upper()


def test_missing_key_raises(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("experiment_id: x\n")
    with pytest.raises(ValueError):
        load_config(bad)


def test_bad_safety_mode_raises(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "experiment_id: x\ntechnology: wifi\nnumber_of_nodes: 1\n"
        "packet_size_bytes: [64]\npacket_interval_ms: [100]\n"
        "experiment_duration_s: 1\nrepetitions: 1\nrandom_seed: 1\n"
        "safety_mode: definitely_not_allowed\n"
    )
    with pytest.raises(ValueError):
        load_config(bad)
