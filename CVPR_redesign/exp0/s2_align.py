"""Step 2: FFHQ-style 256x256 crops (the generator input) for every image in images.csv.
It uses the same dlib 68-landmark alignment as the AAFV pipeline (Code/AAFV_Net/src/aafv/align.py) and falls back to an
InsightFace detector box when dlib finds no face. Resumable.
Output: <out>/crops/<img_id>.png and <out>/align.csv (img_id, ok, stage).
Usage: python s2_align.py [--config config.yaml] [--workers 8]"""
import argparse
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
import PIL.Image

from common import add_aafv_to_path, load_config, out_dir

_G = {}


def _init(predictor):
    import dlib
    add_aafv_to_path()
    from aafv import align
    _G.update(dlib=dlib, det=dlib.get_frontal_face_detector(), sp=dlib.shape_predictor(predictor), align=align)


def _landmarks(rgb, box):
    shp = _G["sp"](rgb, _G["dlib"].rectangle(*[int(v) for v in box]))
    return np.array([[q.x, q.y] for q in shp.parts()])


def _largest(rects):
    return max(rects, key=lambda r: (r.right() - r.left()) * (r.bottom() - r.top()))


def align_one(job):
    img_id, path, dst = job
    try:
        im = PIL.Image.open(path).convert("RGB")
        rgb = np.asarray(im)
        for up in (1, 2):
            d = list(_G["det"](rgb, up))
            if d:
                r = _largest(d)
                lm = _landmarks(rgb, (r.left(), r.top(), r.right(), r.bottom()))
                _G["align"].align_face(im, lm, output_size=256).save(dst)
                return dict(img_id=img_id, ok=1, stage=f"dlib_up{up}")
        return dict(img_id=img_id, ok=0, stage="dlib_none")
    except Exception as e:  # noqa: BLE001 - record and continue
        return dict(img_id=img_id, ok=0, stage="error:" + type(e).__name__)


def fallback(rows, paths, crops, predictor):
    """InsightFace box + dlib landmarks for images dlib could not detect."""
    import cv2
    from insightface.app import FaceAnalysis
    _init(predictor)
    app = FaceAnalysis(name="buffalo_l", allowed_modules=["detection"], providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.3)
    for r in rows:
        if r["ok"]:
            continue
        try:
            f = app.get(cv2.imread(paths[r["img_id"]]))
            if not f:
                continue
            b = max(f, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1])).bbox
            im = PIL.Image.open(paths[r["img_id"]]).convert("RGB")
            _G["align"].align_face(im, _landmarks(np.asarray(im), b), output_size=256).save(crops / f"{r['img_id']}.png")
            r.update(ok=1, stage="scrfd_box")
        except Exception as e:  # noqa: BLE001
            r.update(stage="fallback_error:" + type(e).__name__)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    cfg = load_config(a.config)
    out = out_dir(cfg)
    crops = out_dir(cfg, "crops")
    imgs = pd.read_csv(out / "images.csv")
    res_csv = out / "align.csv"
    old = pd.read_csv(res_csv) if res_csv.exists() else pd.DataFrame(columns=["img_id", "ok", "stage"])
    done = set(old[old.ok == 1].img_id)
    jobs = [(r.img_id, r.path, str(crops / f"{r.img_id}.png")) for r in imgs.itertuples() if r.img_id not in done]
    print(f"{len(jobs)} to align, {len(done)} already done")
    with Pool(a.workers, initializer=_init, initargs=(cfg["align"]["dlib_predictor"],)) as pool:
        rows = list(pool.imap_unordered(align_one, jobs, chunksize=16))
    if any(not r["ok"] for r in rows):
        fallback(rows, dict(zip(imgs.img_id, imgs.path)), crops, cfg["align"]["dlib_predictor"])
    df = pd.concat([old[old.ok == 1], pd.DataFrame(rows)], ignore_index=True)
    df.to_csv(res_csv, index=False)
    print("stages:", df.stage.value_counts().to_dict(), "| aligned", int(df.ok.sum()), "of", len(imgs))


if __name__ == "__main__":
    main()
