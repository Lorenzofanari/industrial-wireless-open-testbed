"""Guard against offensive/unsafe terminology leaking into public surfaces.

Unsafe action terms (jamming, deauthentication, exploitation, flooding, attack
tooling) are permitted only where they are explicitly negated (e.g. "this is
**not** a jamming tool") or inside an explicit non-goals / safety / limitations
section. They must never appear as offered functionality in the README or in the
source/CLI help of ``src/`` and ``scripts/``.

Detection is paragraph-based (blank-line separated blocks) so that negations
that wrap across lines or use Markdown emphasis are still recognised.
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Offensive action terms that must never be presented as functionality.
BANNED_TERMS = [
    "jamming",
    "jammer",
    "anti-jamming",
    "deauth",
    "exploit",
    "flood",
    "attack",
]

# Tokens indicating the term is being explicitly excluded / negated.
NEGATION_TOKENS = [
    "no ",
    "not ",
    "never",
    "without",
    "prohibit",
    "exclud",
    "forbidden",
    "refus",
    "neither",
    "nor ",
    "non-",
    "rather than",
    "instead of",
    "free of",
    "no-",
]

ALLOWED_SECTION_RE = re.compile(
    r"non[- ]?goal|safety|ethic|scope|limitation|prohibited|firewall|not\b", re.IGNORECASE
)


def _normalize(text: str) -> str:
    return re.sub(r"[*_`>]", " ", text).lower()


def _paragraphs(text: str):
    """Yield contiguous blocks of non-blank lines (joined into one string)."""
    block: list[str] = []
    for line in text.splitlines() + [""]:
        if line.strip() == "":
            if block:
                yield block
                block = []
        else:
            block.append(line)


def _scan_markdown(path: Path) -> list[str]:
    offenders = []
    in_allowed_section = False
    for block in _paragraphs(path.read_text(encoding="utf-8")):
        joined = " ".join(block)
        if any(line.lstrip().startswith("#") for line in block):
            in_allowed_section = bool(ALLOWED_SECTION_RE.search(joined))
        norm = _normalize(joined)
        has_negation = any(tok in norm for tok in NEGATION_TOKENS)
        if in_allowed_section or has_negation:
            continue
        for term in BANNED_TERMS:
            if term in norm:
                offenders.append(joined.strip())
                break
    return offenders


def _scan_code(path: Path) -> list[str]:
    offenders = []
    for block in _paragraphs(path.read_text(encoding="utf-8")):
        joined = " ".join(block)
        norm = _normalize(joined)
        if any(tok in norm for tok in NEGATION_TOKENS):
            continue
        for term in BANNED_TERMS:
            if term in norm:
                offenders.append(joined.strip())
                break
    return offenders


def test_readme_has_no_unframed_unsafe_terms():
    offenders = _scan_markdown(REPO_ROOT / "README.md")
    assert not offenders, f"Unframed unsafe terms in README.md: {offenders}"


@pytest.mark.parametrize(
    "py_file",
    sorted((REPO_ROOT / "src").rglob("*.py")) + sorted((REPO_ROOT / "scripts").rglob("*.py")),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_source_has_no_unframed_unsafe_terms(py_file):
    offenders = _scan_code(py_file)
    assert not offenders, f"Unframed unsafe terms in {py_file.name}: {offenders}"
