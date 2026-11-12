# AAFV-Net IEEE TIFS Publication Package (`publication_tifs/`)

Target Venue: **IEEE Transactions on Information Forensics and Security (TIFS)** (IEEE Signal Processing Society, `punumber=10206`)

## Directory Contents

- `main.tex`: Revised TIFS-compliant manuscript (`\documentclass[journal]{IEEEtran}`, no `compsoc`, no `\usepackage{caption}`).
- `references.bib`: Audited and corrected BibTeX bibliography integrating verified IEEE TIFS corpus citations (`2009–2026`).
- `figures/`: Re-generated clean vector PDF & 300-DPI PNG graphics (`fig1_concept` through `fig7_decision_outcomes`).
- `tables/`: Modular verified LaTeX tables (`tab1_morph_test.tex` through `tab9_appendix_ci.tex`) traced directly to `Code/AAFV_Net/`.
- `scripts/generate_tifs_figures.py`: Reproducible Matplotlib script reading frozen CSVs (`extended_test.csv`, `decision_table_calibration.csv`, `extended_calibration_fg16.csv`).
- `scripts/build_supp.py`: Script emitting `supplementary/TIFS_Supplementary.tex` verbatim from frozen audit CSVs.
- `supplementary/TIFS_Supplementary.tex`: Standalone Supplementary Material PDF source (26-variant calibration audit, bin reliability table, Deep Learning checklist, SHA-256 manifest).

## Verified Frozen Checksums

| Artifact | Path | Verified SHA-256 | Notes |
|---|---|---|---|
| `thresholds.json` (LF) | `Code/AAFV_Net/q/thresholds/thresholds.json` | `4b7af9772d209ce6315d36f36df6b191728c830159f04355e7a2238fd9732cfe` | Look 1 checkpoint (`2026-11-05 21:42:09 UTC`); Windows CRLF digest `8c2fdd00...e147` |
| `frozen.pkl` | `Code/AAFV_Net/ablations/variants/full/frozen.pkl` | `a47c916bc819379f9fa5a35b29fdc5ecf3a09f092fbe1cb2c4fbf3347f0035b9` | Look 2 checkpoint (`2026-11-07 19:45:00 UTC`), matching `ablation_freeze.json["full"]` |
| `ablation_freeze.json` | `Code/AAFV_Net/ablations/ablation_freeze.json` | `c66c4266...81ed` (disk digest) | Contains all 26 calibration variant hashes |

## Pre-Submission Author Action Items

Before uploading to IEEE Author Portal / ScholarOne Manuscripts:
1. Replace placeholder author metadata in `main.tex` lines 22–28 (`[Co-Author Names To Be Completed]`, `[Department, University/Institution Name, City, State/Postal Code, Country]`, `[0000-0000-0000-0000]` ORCIDs, and Funding statement in `\section*{Acknowledgments and Disclosures}`).
2. Confirm IEEE SPS **Unified EDICS** selection in portal (recommended: Biometrics / Face Recognition & Authentication).
3. Note page budget: Initial TIFS regular submission limit is **13 pages** (references and appendices count; camera-ready fee-free limit is **10 pages**, excess pages 11–16 incur SPS overlength fees—check live 2026 schedule at portal).

## Reproduction Commands

```powershell
# 1. Regenerate figures & supplementary LaTeX
python publication_tifs/scripts/generate_tifs_figures.py
python publication_tifs/scripts/build_supp.py

# 2. Compile main manuscript & supplementary PDF
cd publication_tifs
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

