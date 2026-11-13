"""Recover which lines of the Turnitin AI-writing report (AAFV-04_Report.pdf) are highlighted.
Method: text lines and positions from pypdf; page images rendered beforehand with
  pdftoppm -r 100 -f 3 -l 14 -png AAFV-04_Report.pdf <dir>/pg
A line is 'flagged' when at least 50% of the pixels in its box have the report's cyan highlight colour.
Usage: python extract_flagged.py <dir with pg-NN.png>   -> flagged_lines.csv, flagged_passages.md (next to this script)"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
PDF = HERE.parent.parent / "AAFV-04_Report.pdf"
DPI = 100


def cyan(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r >= 150) & (r <= 205) & (g >= 205) & (b >= 220) & (g - r >= 25)


def main(img_dir):
    rd = PdfReader(str(PDF))
    imgs = sorted(glob.glob(str(Path(img_dir) / "pg-*.png")))
    rows = []
    for k, path in enumerate(imgs):
        page = rd.pages[2 + k]
        H = float(page.mediabox.height)
        a = np.asarray(Image.open(path).convert("RGB")).astype(int)
        mask = cyan(a)
        sc = DPI / 72.0
        items = []

        def v(text, cm, tm, fd, fs):
            if text.strip():
                x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
                y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                f = fs * (abs(tm[0]) if tm[0] else 1) * (abs(cm[0]) if cm[0] else 1)
                items.append((x, y, f, text))
        page.extract_text(visitor_text=v)
        for x, y, f, text in items:
            for j, line in enumerate(t for t in text.split("\n") if t.strip()):
                yy = y - j * f * 1.1
                x0, x1 = int(x * sc), int(min(a.shape[1] - 1, (x + 0.48 * f * len(line)) * sc))
                yc = H - yy - 0.1 * f            # line centre; offset calibrated on the report (maximises all-or-nothing line scores)
                y0, y1 = int((yc - 0.35 * f) * sc), int((yc + 0.35 * f) * sc)
                if x1 <= x0 or y1 <= y0 or y0 < 0 or y1 >= a.shape[0]:
                    continue
                frac = float(mask[y0:y1, x0:x1].mean())
                rows.append(dict(report_page=3 + k, x=round(x, 1), y=round(yy, 1), size=round(f, 1), cyan=round(frac, 3), flagged=frac >= 0.50, text=line.strip()))
    df = pd.DataFrame(rows)
    df["text"] = df.text.astype(str)
    df = df[~df.text.str.contains("Page \d+ of 14|Submission ID|turnitin", case=False, regex=True)]
    df.to_csv(HERE / "flagged_lines.csv", index=False)
    # passages: consecutive flagged lines in reading order (page, column by x, then top to bottom)
    df["col"] = (df.x > 300).astype(int)
    df = df.sort_values(["report_page", "col", "y"], ascending=[True, True, False]).reset_index(drop=True)
    out, cur, n_words = [], [], 0
    for r in df.itertuples():
        if r.flagged:
            cur.append(r.text)
        elif cur:
            out.append((r.report_page, " ".join(cur)))
            cur = []
    if cur:
        out.append((df.report_page.iloc[-1], " ".join(cur)))
    prose = df[(df["size"].between(8.5, 10.6)) & (df.text.str.len() >= 45)]      # full-width body lines (Turnitin counts prose only)
    words_all = prose.text.str.split().str.len().sum()
    words_flag = prose[prose.flagged].text.str.split().str.len().sum()
    with open(HERE / "flagged_passages.md", "w", encoding="utf-8") as f:
        f.write(f"# Lines highlighted in the Turnitin AI-writing report\n\nFlagged words (approx.): {words_flag} of {words_all} "
                f"({100 * words_flag / words_all:.0f}%) of full-width body-prose lines; Turnitin reports 31% of its qualifying text. {len(out)} passages.\n\n")
        for pg, t in out:
            f.write(f"- (report p.{pg}) {t}\n")
    print(f"lines {len(df)}, flagged {int(df.flagged.sum())}; words {words_flag}/{words_all} = {100 * words_flag / words_all:.1f}%; passages {len(out)}")


if __name__ == "__main__":
    main(sys.argv[1])
