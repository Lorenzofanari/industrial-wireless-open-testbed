# Industrial Wireless Open Testbed v0.1.0

Initial archival release of the software-first educational artifact accompanying
the manuscript:

**An Open-Source Educational Artifact for Wireless Packet Observability in
Cyber–Physical Laboratories**

## Included functionality

- Configuration-driven deterministic synthetic packet-trace generation.
- Wi-Fi-like, BLE/IIoT-like, IEEE 802.15.4/Zigbee-like, and
  LoRa/Sub-GHz/SDR-like educational profiles.
- Packet-level observability metrics.
- Automatically generated scientific figures.
- Per-run manifests containing configuration data, seeds, Git revision
  information, and SHA-256 hashes.
- Reproducibility verification against canonical synthetic traces.
- Teaching, laboratory, safety, and validation documentation.
- Optional owned-device and receive-only hardware extensions.

## Reproduction

```bash
git clone https://github.com/Lorenzofanari/industrial-wireless-open-testbed.git
cd industrial-wireless-open-testbed
git checkout v0.1.0

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

python scripts/run_demo.py --all
python scripts/verify_reproducibility.py --all
pytest
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Scope

The default artifact is entirely software-only and generates synthetic packet
traces. It emits no radio signal and does not access a network interface.

The technology-like profiles demonstrate reproducible packet-observability
workflows. They are not standard-conformant implementations and do not validate
the performance of Wi-Fi, BLE, IEEE 802.15.4, Zigbee, LoRa, or SDR systems.

Optional hardware extensions are restricted to owned or authorised devices,
owned laboratory networks, and receive-only observation where legally permitted.

## Licences

* Source code: MIT.
* Documentation, figures, tables, and synthetic datasets: CC BY 4.0.

## Citation

Citation metadata are available in `CITATION.cff`.

The Zenodo DOI will be added after this GitHub release has been archived
successfully.
