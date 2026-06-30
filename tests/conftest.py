"""Shared test configuration: make the ``src/`` package importable."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

CONFIG_DIR = REPO_ROOT / "configs"
ALL_CONFIGS = sorted(CONFIG_DIR.glob("*.yaml"))
