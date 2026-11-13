"""Collect the reference lists of every prior version (BASE_Paper, AAFV-01..AAFV-05) for the reference analysis.
Reads the PDFs with pdftotext (reference section only) and the .bib files. Writes ../reference_sources.txt.
Usage: python scripts/collect_references.py   (from publication_AAFV-06/)"""
import re
import subprocess
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent
ROOT = PUB.parent
out = []
for pdf in ["BASE_Paper.pdf", "AAFV-01.pdf", "AAFV-02.pdf", "AAFV-03.pdf", "AAFV-04.pdf"]:
    txt = subprocess.run(["pdftotext", "-layout", str(ROOT / pdf), "-"], capture_output=True, text=True, errors="ignore").stdout
    i = max(txt.rfind("REFERENCES"), txt.rfind("References"))
    refs = txt[i:] if i > 0 else ""
    n = len(re.findall(r"^\s*\[\d+\]", refs, flags=re.M)) or len(re.findall(r"\n\s*\d+\.\s+[A-Z]", refs))
    out.append(f"===== {pdf}: about {n} numbered references =====\n{refs}\n")
for bib in ["publication_tifs/references.bib", "AAFV-04_revision/manuscript/references.bib", "publication_AAFV-05/references.bib"]:
    s = (ROOT / bib).read_text(encoding="utf-8")
    keys = re.findall(r"@\w+\{([^,]+),", s)
    out.append(f"===== {bib}: {len(keys)} entries =====\n" + ", ".join(keys) + "\n")
(PUB / "reference_sources.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(l for l in out[0:0]))
for l in out:
    print(l.splitlines()[0])
