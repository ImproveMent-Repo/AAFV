# Cross-Age Face Verification Research & Publication Package

This repository contains the IEEE TIFS publication manuscript, supplementary material, reproducibility figure/table scripts, expert reviews, and research audit documentation for the **AAFV-Net** cross-age biometric verification study.

## Repository Overview

```text
Project/
├── publication_tifs/                  # IEEE TIFS submission package
│   ├── main.tex                       # TIFS-compliant LaTeX manuscript
│   ├── main.pdf                       # Compiled manuscript PDF
│   ├── references.bib                 # Verified BibTeX bibliography
│   ├── IEEEtran.cls / IEEEtran.bst    # IEEEtran class & bibliography style
│   ├── figures/                       # Vector (PDF) and 300-DPI raster (PNG) figures
│   ├── tables/                        # Modular verified LaTeX tables (tab1–tab9)
│   ├── scripts/
│   │   ├── generate_tifs_figures.py   # Reproducible figure generation pipeline
│   │   └── build_supp.py              # Supplementary LaTeX generator
│   ├── supplementary/
│   │   ├── TIFS_Supplementary.tex     # Supplementary material source
│   │   └── TIFS_Supplementary.pdf     # Compiled supplementary PDF
│   └── README.md                      # Detailed TIFS package guide & checksums
├── Paper/                             # Earlier manuscript drafts (Paper-01.tex, Paper-02.tex)
├── Report/                            # Technical project report (AAFV-01_Report.pdf)
├── scripts/                           # Earlier figure generation & redesign test scripts
├── AAFV-01.pdf / AAFV-02.pdf          # Historical compiled manuscript snapshots
├── CHANGELOG.md                       # Visual and formatting revision log
├── MANUSCRIPT_REVIEW.md               # Comprehensive technical manuscript review
├── IEEE_Transactions_Expert_Review.docx # Expert evaluation document
├── TIFS_AUTHOR_GUIDELINES.md          # IEEE TIFS formatting & submission checklist
├── TIFS_LITERATURE_AND_STYLE_ANALYSIS.md # Literature & writing style alignment
├── TIFS_NOVELTY_AND_POSITIONING.md    # Novelty framing and contribution analysis
├── TIFS_RELATED_WORK_REASSESSMENT.md  # Related work positioning notes
├── TIFS_REVISION_ROADMAP.md           # Revision plan and action items
├── literature_review.md               # Literature survey documentation
├── missing_experiments.md             # Experimental audit and gap analysis
├── research_audit.md                  # Statistical and methodological audit log
├── results_verification.md            # Result reproduction and verification trail
├── reviewer_assessment.md             # Reviewer critique and quality checks
└── requirements.txt                   # Python dependencies
```

## Quick Start

### 1. Python Environment Setup

Clone this repository and install the required packages:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Regenerating Figures & Supplementary Material

Run the TIFS figure and supplementary generators from the repository root:

```bash
python publication_tifs/scripts/generate_tifs_figures.py
python publication_tifs/scripts/build_supp.py
```

Generated graphics are saved to `publication_tifs/figures/` and supplementary LaTeX to `publication_tifs/supplementary/`.

### 3. Compiling the IEEE TIFS Manuscript

The manuscript uses `\documentclass[journal]{IEEEtran}`. To compile with `pdflatex` and `bibtex`:

```bash
cd publication_tifs
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

To compile the supplementary PDF:

```bash
cd publication_tifs/supplementary
pdflatex -interaction=nonstopmode TIFS_Supplementary.tex
pdflatex -interaction=nonstopmode TIFS_Supplementary.tex
```

## Core Implementation

The underlying training/evaluation codebase (`Code/`), raw datasets, and large binary checkpoints/models are maintained separately and excluded via `.gitignore`. See [`publication_tifs/README.md`](publication_tifs/README.md) for verified SHA-256 artifact checksums.

## License

This project is released under the MIT License.
