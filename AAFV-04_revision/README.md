# AAFV-04 revision package

This folder contains the revision of AAFV-03 in response to *IEEE_Transactions_Expert_Review.docx*. It does not modify `publication_tifs/`, `publication/`, `Code/`, or any earlier PDF.

## Deliverables

| Deliverable | File |
|---|---|
| A. Revised manuscript (LaTeX source + PDF, 12 pp.) | `manuscript/main.tex`, `manuscript/main.pdf` (bibliography: `manuscript/references.bib`; tables in `manuscript/tables/`) |
| B. Reviewer response matrix | `REVIEW_RESPONSE_MATRIX.md` |
| C. Additional experiment plan | `EXPERIMENT_PLAN.md` |
| D. Research novelty assessment | `NOVELTY_ASSESSMENT.md` |
| E. Unresolved issues report | `UNRESOLVED_ISSUES.md` |
| F. Publication readiness assessment | `READINESS_ASSESSMENT.md` |

## New analyses (no model re-run, no test re-look)

| Script | Inputs | Produces |
|---|---|---|
| `analysis/a1_look1_posthoc.py` | `Code/AAFV_Net/q/report/test_pair_zones_look1.csv`, `ablations/extended_*.csv` | Calibration metrics, P distributions, risk–coverage of the Look-1 scorer, sex × gap rates, sample-size and design-effect tables, workload model, FG-NET false-reject table → `analysis/out/` |
| `analysis/a2_figures.py` | Same, plus `out/` | `manuscript/figures/figR1_posthoc_diagnostics.pdf`, `figR2_outcomes.pdf` |

Re-reading the logged Look-1 outputs is not a new test look. All resulting numbers are labelled *post hoc, descriptive* in the manuscript.

## Main changes from AAFV-03

1. **New title and framing:** a reliability-gated three-way decision protocol with an audited random-impostor FAR. The paper no longer claims a better cross-age verifier.
2. **Calibration-side FAR certificate (Prop. 1):** 0.349% at 95% confidence (n = 1,170, union over three ρ values), independent of test data. The test audit (0/1,149) is now a check, not the source of the guarantee.
3. **Protocol chronology table:** Look 2 used a re-trained checkpoint and a changed reject rule. Look 2 is downgraded to a secondary evaluation.
4. **Consolidated evaluation-population table:** resolves 70.07 / 73.26 / 74.13 / 79.74, 81.07 / 71.93, and 3 vs 5 hard FAs.
5. **New negative results surfaced from existing logs:**

| Finding | Value |
|---|---|
| MORPH genuine test pairs spanning < 5 years | 97.2% |
| FG-NET adult genuine false rejects (target 1%) | 18.20% |
| Manual reviews vs guarded ArcFace on MORPH | ≈ 3× |
| ArcFace hard rejection at β = 0.02 | 71.94% |
| D_hard vs random impostors | D_hard is easier, consistent with training on similarly mined negatives |
| Genuine coverage removed by guards at T_acc (Look 1) | ~18 pp |

6. **Post hoc calibration diagnostics:** Table X and Fig. 3, plus the argument that monotone calibration cannot affect the order-statistic guarantees.
7. **Complete fusion-vector definition:** the four constant slots are shown to be output-irrelevant.
8. **Unverifiable numbers removed:** all latency figures and misused citations. Related work rewritten with AIM and OrdCon read in full. 27 references added; these must be bibliographically checked before submission (U-12).
9. **Threat-model table and positioning table added.**

## Compile

```
cd manuscript
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
