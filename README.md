# Cross-Age Face Verification Research & Publication Package

This repository contains the publication manuscripts, revision packages, supplementary materials, reproducibility analysis pipelines, expert reviews, and comprehensive research audit documentation for the **AAFV-Net** (Age-Aware Face Verification Network) project.

---

## Repository Overview

```text
Project/
├── AAFV-04_revision/                  # Latest AAFV-04 revision package (addressing expert review)
│   ├── manuscript/                    # Revised 12-page manuscript (main.tex, main.pdf, tables, figures)
│   ├── analysis/                      # Post-hoc calibration & diagnostic scripts (a1, a2, a3)
│   │   └── out/                       # Audited diagnostic CSVs, reports, and sample-size tables
│   ├── REVIEW_RESPONSE_MATRIX.md      # Itemized responses to IEEE Transactions expert review
│   ├── EXPERIMENT_PLAN.md             # Additional proposed experimental protocols
│   ├── NOVELTY_ASSESSMENT.md          # Theoretical positioning & contribution analysis
│   ├── READINESS_ASSESSMENT.md        # Publication readiness evaluation
│   ├── UNRESOLVED_ISSUES.md           # Tracked methodological and operational items
│   └── README.md                      # Detailed guide to the AAFV-04 revision package
├── publication_tifs/                  # AAFV-03 IEEE TIFS submission package
│   ├── main.tex / main.pdf            # TIFS manuscript LaTeX source & compiled PDF
│   ├── references.bib                 # Verified BibTeX bibliography
│   ├── IEEEtran.cls / IEEEtran.bst    # IEEEtran class and bibliography style
│   ├── figures/                       # Vector (PDF) and 300-DPI raster (PNG) figures
│   ├── tables/                        # Modular verified LaTeX tables (tab1–tab9)
│   ├── scripts/                       # Figure & supplementary generation scripts
│   ├── supplementary/                 # Standalone supplementary material PDF & source
│   ├── SUBMISSION_AUTHOR_CHECKLIST.md # IEEE submission checklist & action items
│   └── README.md                      # Detailed TIFS package guide & checksums
├── Paper/                             # Early manuscript drafts (Paper-01.tex, Paper-02.tex)
├── Report/                            # Project report (AAFV-01_Report.pdf)
├── scripts/                           # Early figure generation & testing scripts
├── comprehensive_context.md           # Master research continuity & knowledge-base document
├── AAFV-01.pdf ... AAFV-04.pdf        # Historical compiled manuscript snapshots (v1–v4)
├── CHANGELOG.md                       # Formatting & visual correction logs
├── MANUSCRIPT_REVIEW.md               # Technical critique & audit of manuscript drafts
├── IEEE_Transactions_Expert_Review.docx # External expert review document
├── TIFS_AUTHOR_GUIDELINES.md          # IEEE TIFS author guide & checklist
├── TIFS_LITERATURE_AND_STYLE_ANALYSIS.md # Literature & writing style alignment
├── TIFS_NOVELTY_AND_POSITIONING.md    # Novelty framing & contribution notes
├── TIFS_RELATED_WORK_REASSESSMENT.md  # Related work positioning notes
├── TIFS_REVISION_ROADMAP.md           # Revision roadmap & milestones
├── literature_review.md               # Literature survey documentation
├── missing_experiments.md             # Experimental audit & gap analysis
├── research_audit.md                  # Statistical & methodological audit log
├── results_verification.md            # Result reproduction & verification trail
├── reviewer_assessment.md             # Reviewer critique & quality checks
└── requirements.txt                   # Python dependencies
```

---

## Research Continuity & Master Reference

The authoritative reference for this project is:
- **[`comprehensive_context.md`](comprehensive_context.md)**: Master knowledge base covering scientific motivation, mathematical formulations, empirical results, expert critique, historical progression (AAFV-01 through AAFV-04), and research roadmap.

---

## Quick Start

### 1. Python Environment Setup

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Running AAFV-04 Post-Hoc Analysis

To run the post-hoc diagnostic and figure reproduction scripts for the AAFV-04 revision:

```bash
# Post-hoc calibration & workload analysis:
python AAFV-04_revision/analysis/a1_look1_posthoc.py

# Diagnostic figure generation:
python AAFV-04_revision/analysis/a2_figures.py

# Number verification:
python AAFV-04_revision/analysis/a3_verify_numbers.py
```

### 3. Compiling Manuscripts

#### AAFV-04 Revised Manuscript:
```bash
cd AAFV-04_revision/manuscript
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

#### AAFV-03 TIFS Submission Package:
```bash
cd publication_tifs
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

---

## Core Implementation Note

The underlying model training/inference pipeline (`Code/`), raw biometric datasets, and heavy binary checkpoints (`*.pkl`, `*.npz`) are maintained separately and excluded via `.gitignore`. See [`publication_tifs/README.md`](publication_tifs/README.md) and [`AAFV-04_revision/README.md`](AAFV-04_revision/README.md) for audited SHA-256 artifact digests.

---

## License

This project is released under the MIT License.
