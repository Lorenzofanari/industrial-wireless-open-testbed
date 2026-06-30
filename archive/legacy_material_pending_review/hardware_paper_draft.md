# Open-Source Industrial Wireless Instrumentation Testbed for Packet Capture, Reproducibility, and Educational Cyber-Physical Experiments

**Manuscript type:** MDPI *Hardware*-style artifact paper (draft).
**Status:** publication-ready draft. All quantitative results below are produced
by the accompanying open-source repository and are reproducible from a fixed
seed. **All current measurements are software-only (synthetic) demonstrations of
the instrumentation pipeline; they are not measurements of any radio standard.**

> **Scope and firewall.** This is a *companion instrumentation artifact*. It does
> not present, implement, or evaluate any wireless scheduler, anti-jamming
> method, analytical loss/availability model, ns-3 campaign, or IEEE 802.11ax
> PHY/MAC validation. Such topics appear only as external motivation and future
> work. See Section 6 (Limitations and Non-Goals).

---

## Abstract

Reproducible, low-cost instrumentation is a recurring bottleneck in teaching and
preliminary research on industrial wireless communication. We present an
open-source testbed and software toolkit that unifies **benign packet capture**,
**benign traffic generation**, and **packet-level analysis** behind a single
reproducible pipeline, and that runs **fully software-only in a demonstration
mode** requiring no radio hardware. The artifact ships four wireless
communication case studies (Wi-Fi-like, BLE/IIoT-like, IEEE 802.15.4/Zigbee-like,
and LoRa/Sub-GHz/SDR receive-only) expressed as configurable traffic profiles
over one common toolchain. We demonstrate that the toolchain is (i) **bit-exact
reproducible** (identical SHA-256 of generated logs for a fixed seed across all
four case studies), (ii) **repeatable** (run-to-run standard deviation of packet
rate below 0.04 pps and of capture completeness below 0.003 across 3–5 seeded
runs), and (iii) **fast and lightweight** (a complete generate→metrics→plot cycle
runs in under 0.8 s and produces under 0.4 MB of logs per single run on a
commodity laptop). The toolkit is safe by design: it provides no interference,
jamming, or attack functionality, defaults capture/replay tools to dry-run, and
restricts SDR usage to receive-only. We position the artifact as a foundation for
reproducible industrial-wireless teaching and preliminary experimentation, and we
are explicit about what it does and does not validate.

**Keywords:** wireless instrumentation; packet capture; reproducibility;
industrial IoT; education; software-defined radio (receive-only); open hardware.

---

## 1. Motivation and Significance

Hands-on experimentation with industrial wireless links is pedagogically valuable
but practically difficult: capture tooling is fragmented, experiments are hard to
reproduce across machines and cohorts, and safe operation (no unauthorized
transmission or interference) is easy to get wrong. Existing teaching setups often
mix ad-hoc scripts with manual steps, which undermines reproducibility and makes
results difficult to audit.

This artifact addresses the **instrumentation and reproducibility** gap, not the
algorithmic one. Its contributions are:

- **C1.** An open-source, safe-by-design, multi-technology **observability**
  testbed spanning four wireless traffic profiles behind one toolchain.
- **C2.** A **software-only demonstration mode** with a seeded synthetic trace
  generator, enabling reproducible teaching with zero hardware.
- **C3.** A unified **capture → metrics → figures** pipeline with per-run
  manifests (seeds, configuration, SHA-256 output hashes, environment).
- **C4.** Four documented **case studies** with conservative, lab-plausible
  parameters and clearly stated non-goals.
- **C5.** A **reproducibility package** (configs, seeds, manifests, repeatability
  reports, continuous integration) and a **safety/legal firewall** that excludes
  offensive or interference capability.

The artifact is intended for instructors, students, and researchers who need a
credible, auditable starting point before investing in radio hardware.

---

## 2. Hardware Description

The testbed is layered so that it can be adopted incrementally, from a zero-cost
software-only configuration to a contained multi-technology bench. All variants
are **receive/observe-only**; no transmit or interference path is provided.

**Variants.** (A) laptop-only (software-only demo); (B) Raspberry Pi capture/
gateway node; (C) RTL-SDR receive-only sub-GHz observation; (D) educational lab
(owned Wi-Fi/cabled nodes + optional monitor); (E) industrial teaching lab with
contained RF (attenuators/shielded box). Variants and wiring are documented in
the repository (`hardware/topology.md`).

**Cost.** The minimal configuration is free (existing PC + Python). Optional
tiers add commodity components: a Wi-Fi monitor-mode adapter (~€25), a Raspberry
Pi node (~€80 with PSU/SD), BLE and IEEE 802.15.4 dongles (~€12 and ~€30), an
RTL-SDR receive-only dongle with sub-GHz antenna (~€40), and optional attenuators
or a shielded enclosure for contained RF. The full bill of materials with
indicative prices is provided in the repository
(`hardware/bill_of_materials.csv`) and summarized in Table 1.

> **Figure 1 (architecture/variants).** Hardware variants from software-only to a
> contained multi-technology teaching bench, with a role legend (sender/sensor,
> receiver/gateway/sink, optional passive monitor, analysis host). Rendered from
> `hardware/topology.md`. *Message:* buildable at multiple cost tiers,
> observability-only. *(Diagram to be exported to `paper_assets/figures/`.)*

---

## 3. Design and Architecture

### 3.1 Pipeline

A single toolchain is shared by all case studies:

```
config (YAML) ──► capture (synthetic demo OR owned-interface tshark)
              ──► packets.csv (canonical schema)
              ──► compute_metrics ──► metrics.csv / metrics_summary.json
              ──► repeatability_report ──► repeatability_summary.json
              ──► make_plots ──► figures (PNG)
   (every run also emits manifest.json: seed, config, SHA-256 hashes, environment)
```

> **Figure 2 (data/software pipeline).** Block diagram of the acquisition and
> analysis pipeline, highlighting the manifest/hash reproducibility artifacts.
> *Message:* one reproducible toolchain; every run is self-describing.

### 3.2 Canonical data schema

All capture sources (synthetic or real) are normalized to a per-packet CSV:
`timestamp, node_id, packet_id, packet_size_bytes, rssi_dbm (optional),
channel (optional), sequence_id, payload_type`. Per-node sequence IDs enable
loss and duplicate indicators.

### 3.3 Computed metrics

Total packets; duration; packet rate; mean packet size; inter-arrival mean/std;
jitter proxy (inter-arrival std); missing sequence IDs; duplicate sequence IDs;
capture completeness (unique observed sequences / expected span); per-node packet
counts. Repeatability aggregates mean/std/min/max of these across repetitions.

### 3.4 Safety by design

The synthetic generator emits no radio and touches no interface. The `tshark`
wrapper and trace-replay tool default to **dry-run** and require an explicit
`--confirm-owned` flag to touch a real interface. The benign UDP telemetry sender
enforces a conservative packet-rate cap and is not a load generator. SDR is
receive-only by configuration. No jamming, deauthentication, scanning, flooding,
or exploit functionality is included.

---

## 4. Results

> **All Section 4 quantitative results are synthetic demonstration-mode outputs.**
> They demonstrate that the *instrument* faithfully produces, ingests, and
> summarizes packet-level traffic; they are **not** measurements of Wi-Fi, BLE,
> 802.15.4/Zigbee, or LoRa radio behavior. Numbers below were produced by
> `scripts/build_report.py` and are reproducible from the committed seeds.

### 4.1 Testbed Construction and Reproducibility

The artifact builds from commodity parts at several cost tiers (Table 1) and is
reproducible by construction: for a fixed seed, the synthetic generator produces
**byte-identical** packet logs. Table 2 reports identical SHA-256 digests of
`packets.csv` for two independent generations per case study (seed 4242); all
four match.

**Table 2 — Determinism (same seed → identical `packets.csv`).**

| Case | Seed | SHA-256 (first 16 hex) | Match |
|------|------|------------------------|-------|
| Wi-Fi-like | 4242 | `e16ce2c22b7db734…` | yes |
| BLE-like | 4242 | `82e70498f932c18c…` | yes |
| 802.15.4-like | 4242 | `7091cc5755e17db8…` | yes |
| LoRa/SDR-like | 4242 | `db490e35f04b7986…` | yes |

Each run additionally emits a `manifest.json` capturing the configuration, seed,
output hashes, tool version, and Python/OS environment, so a third party can
reproduce or audit any result.

### 4.2 Packet-Capture and Data-Acquisition Workflow

The same pipeline ingests synthetic demo traces and (on owned interfaces) real
captures parsed via `tshark`. Table 3 reports per-case demonstration metrics for
a representative run; the metric values track the configured traffic profiles
(e.g., mean packet size ≈ configured payload, inter-arrival consistent with the
configured interval divided across nodes), confirming the acquisition and metric
computation are correct.

**Table 3 — Per-case demonstration metrics (representative run, synthetic).**

| Case | Tech-like | Packets | Rate (pps) | Mean size (B) | IA mean (ms) | Jitter proxy (ms) | Missing seq | Completeness |
|------|-----------|---------|------------|---------------|--------------|-------------------|-------------|--------------|
| Wi-Fi | Wi-Fi-like | 5939 | 99.02 | 127.3 | 10.10 | 9.36 | 61 | 0.990 |
| BLE | BLE-like | 1422 | 11.87 | 19.5 | 84.27 | 109.49 | 18 | 0.988 |
| 802.15.4 | 802.15.4-like | 1422 | 7.92 | 31.4 | 126.33 | 200.10 | 18 | 0.988 |
| LoRa/SDR | LoRa/SDR-like | 888 | 2.97 | 11.5 | 337.14 | 437.98 | 11 | 0.988 |

The non-zero "missing sequence" counts and sub-unity completeness arise from a
controllable synthetic drop fraction (here ~1%), demonstrating that the loss
indicators respond correctly to known ground truth. (Duplicate indicators are
zero in synthetic mode by construction and become meaningful only with real
captures; see Section 6.)

> **Figure 3 (four-panel, synthetic).** Inter-arrival time distributions for the
> four traffic profiles (`f3a_wifi`, `f3b_ble`, `f3c_802154`, `f3d_lora`).
> *Message:* one toolchain handles four distinct, plausible traffic profiles.
> *Caption draft:* "Representative packet-level observability across four
> synthetic traffic profiles. Data are synthetic demonstrations of the
> acquisition/analysis pipeline, not measurements of the respective radio
> standards."

![Figure 3a Wi-Fi-like inter-arrival](figures/f3a_wifi_inter_arrival.png)
![Figure 3b BLE-like inter-arrival](figures/f3b_ble_inter_arrival.png)
![Figure 3c 802.15.4-like inter-arrival](figures/f3c_802154_inter_arrival.png)
![Figure 3d LoRa/SDR-like inter-arrival](figures/f3d_lora_inter_arrival.png)

### 4.3 Four Wireless Case-Study Demonstrations

Each case study is a parameterization of the common toolchain with conservative,
lab-plausible settings (Table 4). They are presented as **traffic-profile
demonstrations**, not technology validations: the Wi-Fi-like case exercises higher
rate and larger payloads; the LoRa/SDR-like case exercises long intervals and
small payloads in a receive-only/synthetic posture; BLE-like and 802.15.4-like
sit in between. This spread shows the toolchain operates across roughly two orders
of magnitude in packet rate (≈3–99 pps) and payload size (≈12–512 B) without code
changes.

**Table 4 — Case-study parameters (conservative defaults).**

| Case | Tech-like | Nodes | Sizes (B) | Interval (ms) | Duration (s) | Reps | Safety mode |
|------|-----------|-------|-----------|---------------|--------------|------|-------------|
| 1 | Wi-Fi | 4 | 128/256/512 | 20/50/100 | 60 | 5 | owned_lab_network_only |
| 2 | BLE/IIoT | 4 | 20/32/64 | 250/500/1000 | 120 | 5 | synthetic_or_owned_devices_only |
| 3 | 802.15.4/Zigbee | 5 | 32/64/96 | 500/1000/2000 | 180 | 5 | synthetic_or_owned_testbed_only |
| 4 | LoRa/Sub-GHz/SDR | 3 | 12/24/51 | 1000/5000/10000 | 300 | 3 | receive_only_or_synthetic_only |

### 4.4 Repeatability and Fitness-for-Purpose

Across 3–5 seeded repetitions per case, summary metrics exhibit very low
run-to-run variance (Table 5): packet-rate standard deviation ≤ 0.04 pps and
capture-completeness standard deviation ≤ 0.003 in all cases. This indicates the
acquisition/analysis toolchain is stable and **fit for purpose** as a measuring
instrument. Figure 4 illustrates the Wi-Fi-like case (per-run packet rate with
the across-run mean).

![Figure 4 Repeatability (Wi-Fi-like)](figures/f4_repeatability_wifi.png)

**Table 5 — Repeatability across runs (mean ± std).**

| Case | Runs | Rate mean (pps) | Rate std | Completeness mean | Completeness std | Jitter proxy mean (ms) | Jitter proxy std |
|------|------|-----------------|----------|-------------------|------------------|------------------------|------------------|
| Wi-Fi | 5 | 98.96 | 0.040 | 0.989 | 0.0004 | 9.36 | 0.010 |
| BLE | 5 | 11.89 | 0.035 | 0.989 | 0.0029 | 109.62 | 0.378 |
| 802.15.4 | 5 | 7.93 | 0.023 | 0.989 | 0.0029 | 200.23 | 0.461 |
| LoRa/SDR | 3 | 2.98 | 0.007 | 0.990 | 0.0019 | 438.03 | 0.215 |

**Usability.** A complete generate→metrics→plot cycle for a single run completes
in well under one second on a commodity laptop and produces small logs (Table 6).
The dominant cost is figure rendering; metric computation is sub-30 ms even for
the ~6k-packet Wi-Fi-like case.

**Table 6 — Usability: runtime and storage (single run).**

| Case | Packets | Generate (s) | Metrics (s) | Plots (s) | Total (s) | run01 CSV (KB) | Case dir (KB) |
|------|---------|--------------|-------------|-----------|-----------|----------------|---------------|
| Wi-Fi | 5952 | 0.039 | 0.028 | 0.662 | 0.729 | 349.0 | 2502.6 |
| BLE | 1428 | 0.011 | 0.011 | 0.613 | 0.635 | 84.7 | 723.8 |
| 802.15.4 | 1428 | 0.011 | 0.013 | 0.640 | 0.664 | 82.3 | 719.1 |
| LoRa/SDR | 889 | 0.008 | 0.010 | 0.782 | 0.800 | 50.4 | 371.0 |

*(Case-directory size includes all repetitions and figures; environment: commodity
x86-64 laptop, Python 3.13, headless matplotlib. Absolute timings are indicative
and hardware-dependent; the relative profile and reproducibility are the claims.)*

---

## 5. Instructions for Use (Reproducibility)

```bash
python -m pip install -r requirements.txt
# One case study end-to-end (generate N runs + metrics + repeatability + figures):
bash experiments/run_case_wifi_latency.sh 5
# Regenerate all paper tables/figures data:
PYTHONPATH=. python3 scripts/build_report.py
```

Determinism can be checked by regenerating any case with a fixed seed and
comparing the SHA-256 of `packets.csv` against the manifest. The repository
includes a continuous-integration workflow that installs dependencies, runs the
unit tests, and executes a demo smoke run on Python 3.9/3.11/3.12. A full
reproducibility checklist is provided in `docs/reproducibility.md`.

---

## 6. Limitations and Non-Goals

**Measurement limitations.** Latency is reported only as a *proxy* (UDP send/recv
timestamps or synthetic timing), not calibrated end-to-end latency. RSSI/channel
fields are optional and, in demo mode, synthetic. Loss/duplicate indicators rely
on per-node sequence IDs and are not inferable from arbitrary real captures
lacking sequence information. Cross-node latency requires explicit clock
synchronization, which is out of scope by default. SDR support is receive-only and
intended for channel-occupancy/event-timing observation, not demodulation
guarantees. **All Section 4 results are synthetic** demonstrations of the
instrument; they are not radio-standard measurements.

**Non-goals (explicit firewall).** This artifact does not implement or evaluate:
advanced retry/cooldown scheduling; analytical loss/availability models; full
network-simulation campaigns; certified IEEE 802.11ax PHY/MAC validation;
anti-jamming or interference-mitigation methods; safety/SIL/PROFIsafe/certified
protection; or any deployment-ready industrial product claim. Advanced scheduling
and resilience under interference are mentioned only as **external motivation and
future work**. See `docs/limitations.md` and the non-goals table in
`paper_assets/hardware_paper_tables.md`.

**Safety and legal.** All experiments must use owned/authorized devices and
networks. The toolkit provides no interference or attack capability; SDR is
receive-only; capture/replay default to dry-run. Local radio, privacy, and
wiretap regulations apply and are the user's responsibility
(`hardware/safety_notes.md`).

---

## 7. Conclusions and Future Work

We presented a low-cost, safe-by-design, reproducible instrumentation testbed for
benign industrial-wireless observability, demonstrated through a deterministic,
repeatable, lightweight software pipeline across four traffic profiles. The
artifact is immediately usable for teaching and preliminary experimentation and
is honest about what it does not validate. Future work includes adding real owned
captures for a real-vs-demo comparison, legal receive-only spectrum-occupancy
campaigns, and small educational user studies. Advanced scheduling and resilience
under interference are deliberately left to separate work and are referenced here
only as motivation.

---

## Appendix A — Reproducibility artifacts

- Configs: `configs/*.yaml` (four case studies).
- Seeds and manifests: `results/<case>/run*/manifest.json`.
- Aggregated data: `paper_assets/report_data.json`.
- Auto-rendered tables: `paper_assets/tables/auto_tables.md`.
- Figures: `paper_assets/figures/`.
- CI: `.github/workflows/ci.yml`.

## Appendix B — Author checklist before submission

- [ ] Export Figure 1 (variants) and Figure 2 (pipeline) as vector graphics.
- [ ] Replace placeholder lab photos with real owned-setup photos.
- [ ] Confirm every Results figure/table is labeled "synthetic / demonstration".
- [ ] (Optional) Add one owned real capture and a real-vs-demo overlay.
- [ ] Verify the non-goals firewall against the latest manuscript text.
- [ ] Tag a release and mint a DOI; update `CITATION.cff`.

---

*Data availability:* all code, configurations, seeds, and synthetic outputs are in
the accompanying open-source repository (MIT for code; CC BY 4.0 for docs/figures/
data). *Conflicts of interest:* none declared. *Funding:* to be completed.
