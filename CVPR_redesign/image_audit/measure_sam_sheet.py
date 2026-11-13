"""Image-level measurements on Result_Images/sam_sheet.jpeg (2 rows x 6 tiles). No face recognizer is used.
1. Which tiles are identical (repeated originals) vs generated.
   Result: tiles 1, 3, 5 of each row are the same original (identical after a ~5.5 px shift); tiles 2, 4, 6 are generated.
2. Texture: variance of the Laplacian (sharpness) on the central face region, original vs generated.
3. Colour: mean Lab shift of the central face region, and of the eye band, generated vs original.
4. Pixel change maps (generated - original), saved as images to show where the generator edits.
Usage: python measure_sam_sheet.py"""
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "Result_Images" / "sam_sheet.jpeg"
OUT = HERE / "out"

im = cv2.imread(str(SRC))
H, W = im.shape[:2]
th, tw = H // 2, W // 6
tiles = [[im[r * th:(r + 1) * th, c * tw:(c + 1) * tw] for c in range(6)] for r in range(2)]
print(f"sheet {W}x{H}, tile {tw}x{th}")

# 1. tile identity: mean absolute difference between every pair of tiles in a row
rows = []
for r in range(2):
    T = [t.astype(np.float32) for t in tiles[r]]
    M = np.array([[np.abs(a - b).mean() for b in T] for a in T])
    print(f"row {r}: mean |diff| between tiles (0-255)\n", pd.DataFrame(M).round(1).to_string())
    rows.append(M)


def face_box(t, frac=0.5):
    h, w = t.shape[:2]
    return t[int(h * 0.25):int(h * 0.25 + h * frac), int(w * 0.25):int(w * 0.75)]


def eye_band(t):
    h, w = t.shape[:2]
    return t[int(h * 0.30):int(h * 0.48), int(w * 0.18):int(w * 0.82)]


def sharp(t):
    return float(cv2.Laplacian(cv2.cvtColor(t, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())


def lab(t):
    return cv2.cvtColor(t, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32).mean(0)


def align_to(o, g):
    """Shift g onto o (translation from phase correlation); the sheet places successive tiles a few pixels apart."""
    a, b = (cv2.cvtColor(x, cv2.COLOR_BGR2GRAY).astype(np.float32) for x in (o, g))
    (dx, dy), _ = cv2.phaseCorrelate(a, b)
    M = np.float32([[1, 0, -dx], [0, 1, -dy]])
    return cv2.warpAffine(g, M, (g.shape[1], g.shape[0]), borderMode=cv2.BORDER_REFLECT), (dx, dy)


res = []
for r in range(2):
    for k in range(3):
        o = tiles[r][2 * k]
        g, shift = align_to(o, tiles[r][2 * k + 1])
        dl = lab(face_box(g)) - lab(face_box(o))
        de = lab(eye_band(g)) - lab(eye_band(o))
        graw = tiles[r][2 * k + 1]                    # sharpness is shift-invariant: measure on the unresampled tile
        half = lambda t: cv2.resize(face_box(t), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        res.append(dict(row=r + 1, pair=k + 1, sharp_orig=sharp(face_box(o)), sharp_gen=sharp(face_box(graw)),
                        sharp_ratio=sharp(face_box(graw)) / sharp(face_box(o)), sharp_ratio_half_res=sharp(half(graw)) / sharp(half(o)), dL_face=dl[0], da_face=dl[1], db_face=dl[2],
                        dL_eyes=de[0], db_eyes=de[2], mean_abs_change=float(np.abs(face_box(g).astype(np.float32) - face_box(o).astype(np.float32)).mean()), shift_px=round(float(shift[0]), 1)))
        diff = np.abs(g.astype(np.int16) - o.astype(np.int16)).sum(2)
        diff = np.clip(diff * 255.0 / max(diff.max(), 1), 0, 255).astype(np.uint8)
        cv2.imwrite(str(OUT / f"change_row{r + 1}_pair{k + 1}.png"), np.hstack([o, g, cv2.applyColorMap(diff, cv2.COLORMAP_INFERNO)]))
df = pd.DataFrame(res)
df.to_csv(OUT / "sam_sheet_measurements.csv", index=False)
print(df.round(2).to_string(index=False))
print("\nLab: L = lightness, a = green(-)/red(+), b = blue(-)/yellow(+). Face box = central 50% of the tile; eye band = rows 30-48%.")
