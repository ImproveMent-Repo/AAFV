# AAFV-Net Publication Package & Reproducibility Guide

This directory contains the publication-ready package for the research paper:  
**AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate**  
Targeted for **IEEE Transactions on Information Forensics and Security (T-IFS)** and **IEEE Transactions on Biometrics, Identity and Behavior (T-BIOM)**.

---

## 1. Directory Structure

```text
publication/
├── main.tex                       # Complete 10-page IEEEtran LaTeX manuscript
├── main.pdf                       # Compiled, publication-verified PDF manuscript
├── references.bib                 # Verified bibliographic references with DOIs
├── IEEEtran.cls                   # Official IEEEtran document class (v1.8b)
├── IEEEtran.bst                   # Official IEEEtran BibTeX bibliography style
├── figures/                       # Vector (PDF) and 300-DPI raster (PNG) publication figures
│   ├── fig1_concept.pdf / .png    # Conceptual schematic of 3-way guarded decision
│   ├── fig2_architecture.pdf / .png # Full technical architecture flowchart
│   ├── fig3_results.pdf / .png    # MORPH trade-off & FG-NET Adults gap bin results
│   ├── fig4_ablations.pdf / .png  # Calibration ablation study bar chart
│   ├── fig5_gap_neutral.pdf / .png# MORPH gap bins & Neutral hard impostor rejection
│   ├── fig6_beta_sweep.pdf / .png # Sensitivity across false-reject targets beta
│   └── fig7_decision_outcomes.pdf / .png # Decision outcome breakdown (same vs hard diff)
├── tables/                        # Auxiliary LaTeX table templates
├── supplementary/                 # Supplementary experimental documentation
└── README.md                      # This reproducibility guide
```

---

## 2. System Requirements & Dependencies

### Python Environment
- Python 3.10+ (tested on Python 3.11.9)
- Packages: `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn`, `torch`, `torchvision`
- Standard installation:
  ```bash
  pip install numpy scipy pandas matplotlib seaborn torch torchvision
  ```

### LaTeX Compilation Environment
- MiKTeX or TeX Live (2022+)
- Required packages (included in standard distributions): `amsmath`, `amssymb`, `graphicx`, `booktabs`, `multirow`, `array`, `microtype`, `xcolor`, `cite`, `url`, `hyperref`, `caption`

---

## 3. How to Reproduce All Figures

To re-generate all 7 publication figures (both vector PDF and 300-DPI PNG) from source experimental data:

```powershell
# From the project root directory:
python scripts/generate_publication_figures.py
```

Output files will be automatically placed in `publication/figures/`:
- `fig1_concept.pdf` / `fig1_concept.png`
- `fig2_architecture.pdf` / `fig2_architecture.png`
- `fig3_results.pdf` / `fig3_results.png`
- `fig4_ablations.pdf` / `fig4_ablations.png`
- `fig5_gap_neutral.pdf` / `fig5_gap_neutral.png`
- `fig6_beta_sweep.pdf` / `fig6_beta_sweep.png`
- `fig7_decision_outcomes.pdf` / `fig7_decision_outcomes.png`

---

## 4. How to Compile the Manuscript

The manuscript uses standard `pdflatex` and `bibtex` toolchains. All required style files (`IEEEtran.cls`, `IEEEtran.bst`) are locally bundled in the `publication/` directory.

### Compilation Command Sequence:
```powershell
cd publication
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### Verification Criteria:
- Exit Code: `0` (Success)
- Page Count: Exactly 10 pages
- Broken References: `0`
- Undefined Citations: `0`
- Overfull/Underfull Fatalities: None

---

## 5. Frozen Artifacts & Integrity Hashes

All experimental thresholds and models were locked and frozen prior to test-set evaluation:

| Artifact Name | Relative Path | SHA-256 Checksum | Description |
|---|---|---|---|
| `thresholds.json` | `Code/AAFV_Net/q/thresholds/thresholds.json` | `4b7af977c05001a1c3bb501309f58ea9c8119eb4519fdb8631ca233f81e62cfe` | Look 1 frozen thresholds ($T_{\text{acc}}=0.956575$) |
| `frozen.pkl` | `Code/AAFV_Net/ablations/frozen.pkl` | `0fb68e7b9ddaa05813f41ffdf715617a9c264a9ce86ee942ea7eb88eb34845cf` | Look 2 frozen calibrated model ($T_{\text{acc}}=0.956438, T_{\text{rej}}=0.007541$) |
| `ablation_freeze.json` | `Code/AAFV_Net/ablations/ablation_freeze.json` | `cbbd6d84f8ee7329ea156e5076cfb169542a98f45a8dfc84fc476be13459c368` | Calibration parameters across all 20 ablation variants |

---

## 6. Access Budget & Audit Trail

In strict adherence to zero-leakage scientific protocols:
- **Total Test Accesses Permitted:** 2 looks
- **Look 1 Date:** 2026-11-05 (Script: `scripts/p9_test.py`, Artifact: `q/report/test_report_look1.json`)
- **Look 2 Date:** 2026-11-07 (Script: `scripts/p12_extended.py`, Artifact: `ablations/extended_test.csv`)
- **Budget Status:** **EXHAUSTED (2 of 2 looks spent).**
- **Statistical Adjustment:** All reported confidence bounds incorporate a 2-look Bonferroni adjustment ($\alpha' = 0.05 / 2 = 0.025$), yielding $\text{FAR}_{\text{upper}} = 1 - (0.025)^{1/1149} \approx 0.320\%$.

---

## 7. Master Deliverables Directory

All 10 project deliverables required by the Master Research Prompt:
1. `research_audit.md`: Complete Phase 1 technical and experimental audit.
2. `results_verification.md`: Complete Phase 2 independent mathematical recalculations and source-of-truth matrix.
3. `missing_experiments.md`: Phase 3 & 5 deficiency matrix and prioritized experimental roadmap.
4. `literature_review.md`: Phase 4 literature survey, novelty taxonomy, and venue positioning.
5. `publication/main.tex`: Phase 6 & 8 revised IEEE journal manuscript.
6. `publication/references.bib`: Phase 8 verified bibliographic database.
7. `publication/figures/`: Phase 7 vector PDF and 300-DPI PNG figures.
8. `publication/main.pdf`: Phase 8 compiled 10-page IEEE publication PDF.
9. `reviewer_assessment.md`: Phase 9 simulated peer review report from three independent perspectives.
10. `publication/README.md`: Phase 10 reproducibility documentation (this document).

