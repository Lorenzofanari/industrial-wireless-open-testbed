# Hardware-Style Paper Outline (MDPI *Hardware*)

This outline maps the repository onto a Hardware-style artifact paper. The paper
is about the **testbed and instrumentation**, not any scheduling algorithm.

## Working title

> *Open-Source Industrial Wireless Instrumentation Testbed for Packet Capture,
> Reproducibility, and Educational Cyber-Physical Experiments*

Alternative titles:
- *A Low-Cost, Reproducible Multi-Technology Wireless Observability Testbed for IIoT Education*
- *Benign-by-Design: An Open Wireless Capture and Analysis Toolkit for Teaching Labs*

## Contribution statement

We present an open-source, low-cost, **safe-by-design** wireless instrumentation
testbed that (i) unifies packet capture, benign traffic generation, and analysis
for four wireless technologies; (ii) runs fully software-only in demo mode for
reproducible teaching; (iii) extends to commodity hardware and receive-only SDR;
and (iv) ships a reproducibility package (configs, seeds, manifests, figures).

## Section outline

1. **Introduction** — motivation for reproducible wireless observability in IIoT
   education; gap addressed; explicit scope (observability, not control).
2. **Related hardware/testbeds** — commodity capture setups, SDR rx, teaching
   testbeds; positioning.
3. **Hardware description** — variants A–E, bill of materials, topology,
   safety-by-design.
4. **Design and architecture** — software toolkit (capture/traffic/analysis),
   canonical data schema, manifests.
5. **Case studies** — four wireless technologies; parameters; outputs; metrics.
6. **Validation (minimal, fitness-for-purpose)** — demo reproducibility,
   repeatability across runs, completeness/jitter sanity checks.
7. **Reproducibility & instructions for use** — install, quickstart, protocol.
8. **Safety, limitations, and non-goals.**
9. **Conclusions and future work** (advanced scheduling cited only as future
   work / external motivation).

## Figure list

| Fig | Content | Source |
|-----|---------|--------|
| F1 | Testbed architecture / variants | `hardware/topology.md` diagrams |
| F2 | Canonical data + processing pipeline | new diagram |
| F3 | Packet count over time | `make_plots.py` |
| F4 | Inter-arrival time distribution | `make_plots.py` |
| F5 | Packet size distribution | `make_plots.py` |
| F6 | Per-node packet count | `make_plots.py` |
| F7 | Repeatability across runs | `make_plots.py` |

## Table list

| Tbl | Content | Source |
|-----|---------|--------|
| T1 | Contribution summary | `paper_assets/hardware_paper_tables.md` |
| T2 | Case study matrix | `paper_assets/hardware_paper_tables.md` |
| T3 | Bill of materials summary | `hardware/bill_of_materials.csv` |
| T4 | Validation metrics | `paper_assets/hardware_paper_tables.md` |
| T5 | Non-goals / scope firewall | `paper_assets/hardware_paper_tables.md` |
| T6 | Reproducibility checklist | `docs/reproducibility.md` |

## Supplementary material checklist

- [ ] Source repository (this artifact) with tagged release + DOI.
- [ ] `configs/` for all four case studies.
- [ ] Demo `results/` for a reference seed (or regeneration instructions).
- [ ] Figures in `paper_assets/figures/`.
- [ ] `CITATION.cff`, `LICENSE`, safety notes.
- [ ] Reproducibility checklist completed.

## Author guidance

- Frame all claims as **observability** and **educational fitness-for-purpose**.
- Avoid certification language (no "validated 802.11ax", no "anti-jamming").
- Keep the scheduler firewall intact (see `paper_assets/hardware_paper_tables.md`).
