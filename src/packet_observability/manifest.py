"""Per-run reproducibility manifests.

A manifest records *what* was produced, *how*, and *under which safety mode*, so
that a third party can regenerate or audit a synthetic demo-mode run. It captures
only benign metadata: the configuration path and contents, the seed, the script
version / git commit (when available), the output files with their SHA-256
hashes, a UTC timestamp, and the Python/OS environment.
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packet_observability import __version__
from packet_observability.hash_utils import sha256_file


def git_commit(short: bool = False) -> str | None:
    """Return the current git commit hash, or ``None`` when unavailable."""
    cmd = ["git", "rev-parse", "--short", "HEAD"] if short else ["git", "rev-parse", "HEAD"]
    try:
        out = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).resolve().parent,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    commit = out.stdout.strip()
    return commit or None


def build_manifest(
    *,
    experiment_id: str,
    config: dict[str, Any],
    config_path: str | Path | None = None,
    seed: int | None = None,
    mode: str = "synthetic_demo",
    output_files: list[Path] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble a manifest dictionary describing a synthetic demo-mode run."""
    output_files = output_files or []
    file_records = []
    for f in output_files:
        f = Path(f)
        if f.exists() and f.is_file():
            file_records.append(
                {
                    "name": f.name,
                    "relative_path": str(f),
                    "size_bytes": f.stat().st_size,
                    "sha256": sha256_file(f),
                }
            )

    manifest: dict[str, Any] = {
        "schema": "packet-observability-manifest/1.0",
        "experiment_id": experiment_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "safety_mode": config.get("safety_mode"),
        "tool_version": __version__,
        "git_commit": git_commit(),
        "config_path": str(config_path) if config_path is not None else None,
        "seed": seed if seed is not None else config.get("random_seed"),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "config": config,
        "outputs": file_records,
        "note": "Synthetic demo-mode output. No radio emission, no network capture.",
    }
    if extra:
        manifest["extra"] = extra
    return manifest


def write_manifest(manifest: dict[str, Any], out_path: str | Path) -> Path:
    """Write a manifest as JSON.

    ``out_path`` may be a directory (``manifest.json`` is written inside it) or a
    full file path.
    """
    out_path = Path(out_path)
    if out_path.suffix.lower() == ".json":
        out_path.parent.mkdir(parents=True, exist_ok=True)
        path = out_path
    else:
        out_path.mkdir(parents=True, exist_ok=True)
        path = out_path / "manifest.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
    return path
