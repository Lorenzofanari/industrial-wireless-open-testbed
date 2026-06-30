# Contributing

Thank you for your interest in improving this artifact. Contributions that
strengthen reproducibility, clarity, documentation, and educational value are
very welcome.

## Ground rules

- **Stay within scope.** This is a safe-by-design, software-only synthetic
  packet-observability and reproducibility workflow with optional passive /
  receive-only extensions. Contributions must not add offensive functionality
  (no jamming, flooding, deauthentication, exploitation, or unauthorised
  scanning), interference transmission, scheduler implementations, or
  standard-validation/real radio-performance claims. See
  [`docs/limitations_and_non_goals.md`](docs/limitations_and_non_goals.md).
- **Use conservative wording.** Prefer terms such as "synthetic demo-mode
  output", "technology-like profile", and "not a standard-conformant
  implementation". The test suite enforces a terminology guard
  (`tests/test_no_unsafe_terminology.py`).

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Before opening a pull request

1. Run the tests:
   ```bash
   pytest
   ```
2. Verify reproducibility (and regenerate references if you intentionally
   changed the generator or a config):
   ```bash
   python scripts/verify_reproducibility.py --all
   ```
3. If you changed the synthetic generator or a config such that the canonical
   traces change, regenerate them and explain why in your pull request:
   ```bash
   python scripts/generate_traces.py --config configs/<case>.yaml \
       --out data/synthetic_demo/<case>/packets.csv
   ```
4. Keep the code style consistent (`ruff check src tests scripts`).

## Code organisation

- Core library: `src/packet_observability/`.
- Optional extensions: `src/packet_observability/extensions/`.
- Command-line entry points (thin wrappers): `scripts/`.
- Documentation: `docs/`.

## Reporting issues

For bugs and documentation problems, please open an issue. For security or
misuse concerns, follow [`SECURITY.md`](SECURITY.md). All participants are
expected to follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
