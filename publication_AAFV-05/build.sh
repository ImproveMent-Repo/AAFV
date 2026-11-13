#!/usr/bin/env bash
# Build AAFV-05: tables/figures and bibliography from sources, check prose numbers, then compile.
set -e
cd "$(dirname "$0")"
python scripts/build_assets.py
python scripts/build_bib.py
python scripts/check_claims.py
pdflatex -interaction=nonstopmode main.tex >/dev/null
bibtex main >/dev/null
pdflatex -interaction=nonstopmode main.tex >/dev/null
pdflatex -interaction=nonstopmode main.tex >/dev/null
grep -E "^!|undefined|Overfull" main.log && { echo "LaTeX problems above"; exit 1; } || echo "main.pdf built cleanly"
