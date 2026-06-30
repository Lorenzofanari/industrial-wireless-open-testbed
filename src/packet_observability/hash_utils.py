"""SHA-256 hashing helpers used by manifests and reproducibility checks.

These helpers support the reproducibility layer: deterministic regeneration of
synthetic demo-mode outputs is verified by comparing SHA-256 digests.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

_CHUNK_SIZE = 65536


def sha256_bytes(data: bytes) -> str:
    """Return the hex SHA-256 digest of a bytes object."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the hex SHA-256 digest of a file, read in chunks."""
    path = Path(path)
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_files(paths: list[str | Path]) -> dict[str, str]:
    """Return a mapping of file name -> SHA-256 digest for existing files."""
    digests: dict[str, str] = {}
    for p in paths:
        p = Path(p)
        if p.exists() and p.is_file():
            digests[p.name] = sha256_file(p)
    return digests
