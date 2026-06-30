"""Manifests must contain the required reproducibility fields and valid hashes."""
from pathlib import Path

from packet_observability.hash_utils import sha256_bytes, sha256_file
from packet_observability.io import load_config, write_packets_csv
from packet_observability.manifest import build_manifest, write_manifest
from packet_observability.synthetic_generator import generate_packets

WIFI = Path(__file__).resolve().parents[1] / "configs" / "wifi_like.yaml"

REQUIRED_FIELDS = {
    "schema",
    "experiment_id",
    "generated_utc",
    "mode",
    "safety_mode",
    "tool_version",
    "config_path",
    "seed",
    "environment",
    "config",
    "outputs",
}


def test_sha256_bytes_known_value():
    # SHA-256 of an empty bytestring is a well-known constant.
    assert sha256_bytes(b"") == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_manifest_has_required_fields(tmp_path):
    cfg = load_config(WIFI)
    packets = write_packets_csv(generate_packets(cfg, seed=11), tmp_path / "packets.csv")
    manifest = build_manifest(
        experiment_id=cfg.experiment_id,
        config=cfg.raw,
        config_path=WIFI,
        seed=11,
        output_files=[packets],
    )
    assert REQUIRED_FIELDS.issubset(manifest.keys())
    assert manifest["experiment_id"] == "wifi_like"
    assert manifest["seed"] == 11
    assert manifest["outputs"], "manifest should record at least one output file"


def test_manifest_output_hashes_match_files(tmp_path):
    cfg = load_config(WIFI)
    packets = write_packets_csv(generate_packets(cfg, seed=11), tmp_path / "packets.csv")
    manifest = build_manifest(
        experiment_id=cfg.experiment_id,
        config=cfg.raw,
        output_files=[packets],
    )
    record = manifest["outputs"][0]
    assert record["sha256"] == sha256_file(packets)


def test_write_manifest_to_path(tmp_path):
    cfg = load_config(WIFI)
    manifest = build_manifest(experiment_id=cfg.experiment_id, config=cfg.raw)
    out = write_manifest(manifest, tmp_path / "manifest.json")
    assert out.exists()
    assert out.name == "manifest.json"
