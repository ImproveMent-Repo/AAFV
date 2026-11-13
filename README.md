# Cross-Age Face Verification Research & Publication Package

This repository contains the publication manuscripts, revision packages, empirical analysis pipelines, expert reviews, and comprehensive research audit documentation for the **AAFV-Net** (Age-Aware Face Verification Network) project.

---

## Repository Overview

```text
Project/
├── publication_AAFV-06/               # Latest AAFV-06 complete 13-page manuscript package
│   ├── main.tex                       # Complete 13-page IEEEtran journal manuscript
│   ├── references.bib                 # Comprehensive audited bibliography (90 verified entries)
│   ├── REFERENCE_ANALYSIS.md          # Multi-version reference audit and provenance ledger
│   ├── tables/                        # 12 automated LaTeX tables generated directly from logs
│   ├── figures/                       # Vector architecture, concept & aggregate diagnostic figures
│   ├── scripts/                       # Asset builder, table generator, figure generator & claim checker (44/44 verified)
│   ├── build.sh                       # One-command reproducible build script
│   ├── CLAIMS_LEDGER.md               # Empirical claims-to-data mapping ledger
│   ├── CHANGES_FROM_AAFV-05.md        # Detailed evolution log from AAFV-05 to AAFV-06
│   ├── SUBMISSION_CHECKLIST.md        # Pre-submission author action checklist
│   ├── supplementary/                 # Pre-registration protocol & analysis index
│   └── README.md                      # Detailed guide to the AAFV-06 package
├── publication_AAFV-05/               # AAFV-05 manuscript & re-analysis package
│   ├── main.tex / main.pdf            # 7-page IEEEtran manuscript & compiled PDF
│   ├── references.bib                 # Audited & verified bibliography (48 entries)
│   ├── tables/                        # Automated LaTeX tables generated from analysis CSVs
│   ├── figures/                       # Vector & aggregate plots
│   ├── scripts/                       # Asset builder, bib generator & claim checker (33/33 verified)
│   ├── build.sh                       # One-command reproducible build script
│   ├── CLAIMS_LEDGER.md               # Empirical claims-to-data mapping ledger
│   ├── CHANGES_FROM_AAFV-04.md        # Evolution & claim reconciliation log
│   └── README.md                      # Detailed guide to AAFV-05 package
├── CVPR_redesign/                     # Architectural review & Stage-1 assessment suite
│   ├── STAGE1_ASSESSMENT.md           # Stage-1 empirical assessment & findings
│   ├── FINAL_REPORT.md                # Comprehensive final report on AAFV-Net
│   ├── DRIVE_FINDINGS.md              # Audit of calibration & backup artifacts
│   ├── drive_analyses/                # Threshold counterfactuals & matched-FMR scripts
│   ├── log_analyses/                  # Log-only matched-FPR and label-noise scripts
│   ├── architecture_review/           # Fusion network probing & ablation scripts
│   ├── phase5_literature/             # Literature review & prior-art positioning
│   ├── phase6_experiments/            # Pre-registered experimental protocols
│   ├── phase7_originality/            # Manuscript text originality review & flagged lines
│   ├── phase8_manuscript/             # Target manuscript blueprint & framing
│   └── phase9_reproducibility/        # Checksum manifest & artifact verification
├── AAFV-04_revision/                  # AAFV-04 revision package (addressing expert review)
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
├── Report/                            # Project reports (AAFV-01_Report.pdf, AAFV-04_Report.pdf)
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
- **[`comprehensive_context.md`](comprehensive_context.md)**: Master knowledge base covering scientific motivation, mathematical formulations, empirical results, expert critique, historical progression (AAFV-01 through AAFV-06), and research roadmap.

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

### 2. Building AAFV-06 Package & Manuscript

To verify claims, build assets, and compile the latest AAFV-06 manuscript:

```bash
cd publication_AAFV-06

# Run automated asset generation & claim checking:
python scripts/build_tables_06.py
python scripts/build_assets.py
python scripts/build_bib.py
python scripts/check_claims.py

# Compile manuscript:
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### 3. Building Earlier Versions

#### AAFV-05 Controlled Re-Analysis:
```bash
cd publication_AAFV-05
python scripts/build_assets.py
python scripts/build_bib.py
python scripts/check_claims.py
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

#### AAFV-04 Revised Manuscript:
```bash
cd AAFV-04_revision/manuscript
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

---

## Core Implementation & Data Governance

The underlying model training pipeline (`Code/`), raw biometric datasets (MORPH, FG-NET), derived face crops, and heavy binary checkpoints (`*.pkl`, `*.npz`) are maintained separately and excluded via `.gitignore` to comply with dataset licensing and GitHub storage policies. In `publication_AAFV-06/`, raw face images and PDFs embedding human subjects remain local-only per research ethics agreements.

---

## License

This project is released under the MIT License.
