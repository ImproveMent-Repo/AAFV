# Cross-Age Face Verification Research & Publication Package

This repository contains the publication manuscript, reproducibility assets, figure generators, and research audit documentation for the cross-age biometric verification study.

## Repository Overview

```text
Project/
├── publication/              # Publication package for IEEE manuscript
│   ├── main.tex              # Primary LaTeX source file
│   ├── main.pdf              # Pre-compiled paper PDF
│   ├── references.bib        # Bibliographic references
│   ├── IEEEtran.cls          # IEEE document class
│   ├── IEEEtran.bst          # IEEE bibliography style
│   ├── figures/              # High-resolution vector (PDF) and raster (PNG) figures
│   ├── tables/               # Table definitions
│   └── supplementary/        # Supplementary evaluation notes
├── scripts/                  # Reproduction and visualization scripts
│   └── generate_publication_figures.py # Automated figure generation pipeline
├── Figures/                  # Standalone publication figure assets
├── missing_experiments.md    # Experimental audit and gap analysis
├── literature_review.md      # Literature review documentation
├── research_audit.md         # Statistical and methodological audit log
├── results_verification.md   # Result reproduction and verification trail
├── reviewer_assessment.md    # Reviewer critique and quality checks
└── requirements.txt          # Python dependencies
```

## Quick Start

### 1. Python Environment Setup

Clone this repository and install required packages:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Generating Publication Figures

Run the figure generation script to reproduce all vector and raster figures:

```bash
python scripts/generate_publication_figures.py
```

Generated plots will be saved into `publication/figures/`.

### 3. Compiling the LaTeX Manuscript

The paper is typeset with `IEEEtran`. To compile using `pdflatex` or `latexmk`:

```bash
cd publication
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Core Implementation

The underlying computational pipeline, data splits, and model checkpoints are maintained separately and excluded from this repository.

## License

This project is released under the MIT License.
