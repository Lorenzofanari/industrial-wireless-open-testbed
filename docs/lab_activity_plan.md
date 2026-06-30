# Lab activity plan

A suggested 90–120 minute session. Times are indicative and can be adapted.

| Phase | Student task | Instructor check | Evidence generated | Estimated time |
|-------|--------------|------------------|--------------------|----------------|
| Introduction | Read the overview and learning objectives; understand software-only scope. | Students know no radio hardware is needed and that demo data are synthetic. | — | 10 min |
| YAML inspection | Open a chosen `configs/<case>.yaml`; note seed, sizes, intervals, duration, nodes, missing-sample model. | Parameters correctly identified in the worksheet. | Worksheet YAML section | 15 min |
| Trace generation | Run `run_demo.py`/`generate_traces.py` for the chosen profile. | `packets.csv` exists under `results/demo/<case>/`. | `packets.csv`, `manifest.json` | 15 min |
| Metric computation | Run `compute_metrics.py`; record metrics. | Metrics table filled correctly. | `metrics.csv`, `metrics_summary.json` | 15 min |
| Figure inspection | Run `plot_results.py`; inspect the four figures. | Figures generated and interpreted. | `figures/*.png` | 15 min |
| Reproducibility check | Run `verify_reproducibility.py --all`; record PASS/FAIL and a hash. | Result is `PASS`; hash recorded. | Verification output | 10 min |
| Synthetic-vs-real discussion | Explain what the results do and do not show. | Student states synthetic ≠ real measurement. | Worksheet reflection | 15 min |
| Submission | Complete and submit the worksheet. | Worksheet complete and consistent. | Completed `student_worksheet.md` | 10 min |

See [`instructor_guide.md`](instructor_guide.md) for preparation and verification
guidance, and [`common_student_mistakes.md`](common_student_mistakes.md) for
pitfalls to watch for.
