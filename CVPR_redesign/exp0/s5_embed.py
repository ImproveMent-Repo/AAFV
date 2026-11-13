"""Step 5: recognizer embeddings for every real crop and every generated face.
Each face (real or generated, 256x256) goes through the same path: SCRFD detection, five landmarks, norm_crop to 112x112 (cached).
Outputs:
  <out>/faces112/<group>.npy + <group>.csv   cached 112x112 BGR crops (group = 'real' or a generator name)
  <out>/emb/<recognizer>/<group>.npy           L2-normalised float32 embeddings (NaN rows where detection failed)
  <out>/emb/<recognizer>/preflight.json        AUC of s0 on real 0-4 y pairs (and with colour channels swapped)
Usage: python s5_embed.py --recognizer adaface [--config config.yaml]"""
import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import numpy as np
import pandas as pd

from common import auc_w, bin_labels, cos_rows, load_config, out_dir


# ---------------------------------------------------------------- 112x112 crops
def make_crops(paths, ids, dst_npy, dst_csv):
    if Path(dst_npy).exists() and Path(dst_csv).exists():
        idx = pd.read_csv(dst_csv)
        if idx.face_id.tolist() == list(ids):
            return np.load(dst_npy, mmap_mode="r"), idx
    import cv2
    from insightface.app import FaceAnalysis
    from insightface.utils import face_align
    app = FaceAnalysis(name="buffalo_l", allowed_modules=["detection"], providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.3)
    arr = np.zeros((len(ids), 112, 112, 3), np.uint8)
    ok, score = np.zeros(len(ids), bool), np.zeros(len(ids), np.float32)
    for k, p in enumerate(paths):
        im = cv2.imread(str(p))
        f = app.get(im) if im is not None else []
        if f:
            b = max(f, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
            arr[k] = face_align.norm_crop(im, landmark=b.kps, image_size=112)
            ok[k], score[k] = True, b.det_score
        if k % 5000 == 0:
            print(f"  crops {k}/{len(ids)}", flush=True)
    idx = pd.DataFrame(dict(face_id=list(ids), det_ok=ok, det_score=score))
    np.save(dst_npy, arr)
    idx.to_csv(dst_csv, index=False)
    print(f"  {Path(dst_npy).name}: detection failed on {int((~ok).sum())} of {len(ids)}", flush=True)
    return arr, idx


# ---------------------------------------------------------------- recognizers (input: N x 112 x 112 x 3 uint8 BGR)
class InsightFaceRec:
    def __init__(self, c):
        from insightface.app import FaceAnalysis
        app = FaceAnalysis(name=c.get("model", "buffalo_l"), allowed_modules=["detection", "recognition"],
                           providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        app.prepare(ctx_id=0)
        self.rec = app.models["recognition"]

    def __call__(self, bgr):
        return self.rec.get_feat(list(bgr))


class TorchRec:
    def __init__(self):
        import torch
        self.torch = torch
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"

    def _run(self, x):
        with self.torch.no_grad():
            t = self.torch.from_numpy(np.ascontiguousarray(x.transpose(0, 3, 1, 2))).float().to(self.dev)
            out = self.model(t)
            out = out[0] if isinstance(out, (tuple, list)) else out
            return out.float().cpu().numpy()


class AdaFaceRec(TorchRec):
    """github.com/mk-minchul/AdaFace: BGR input, (x/255 - 0.5)/0.5; checkpoint keys prefixed 'model.'."""

    def __init__(self, c):
        super().__init__()
        sys.path.insert(0, c["repo"])
        import net
        self.model = net.build_model(c.get("arch", "ir_101"))
        sd = self.torch.load(c["checkpoint"], map_location="cpu", weights_only=False)["state_dict"]
        self.model.load_state_dict({k[6:]: v for k, v in sd.items() if k.startswith("model.")})
        self.model.eval().to(self.dev)

    def __call__(self, bgr):
        return self._run((bgr.astype(np.float32) / 255.0 - 0.5) / 0.5)


class MagFaceRec(TorchRec):
    """github.com/IrvingMeng/MagFace (checked 2026-11-13): builder_inf(args) reads arch, embedding_size, resume, cpu_mode and
    strips 'features.module.' / 'module.features.' prefixes itself; gen_feat.py feeds cv2 BGR through ToTensor (mean 0, std 1);
    forward returns the raw embedding (its magnitude is MagFace's quality). builder_inf calls bare torch.load, which
    defaults to weights_only=True from torch 2.6, so the checkpoint is loaded as a full pickle here (official file only)."""

    def __init__(self, c):
        super().__init__()
        sys.path.insert(0, c["repo"])
        from inference.network_inf import builder_inf
        torch = self.torch
        orig = torch.load
        torch.load = lambda *a, **k: orig(*a, **{"weights_only": False, **k})
        try:
            self.model = builder_inf(Namespace(arch=c.get("arch", "iresnet100"), embedding_size=512, resume=c["checkpoint"],
                                               cpu_mode=self.dev == "cpu"))
        finally:
            torch.load = orig
        self.model.eval().to(self.dev)

    def __call__(self, bgr):
        return self._run(bgr.astype(np.float32) / 255.0)


RECS = {"insightface": InsightFaceRec, "adaface": AdaFaceRec, "magface": MagFaceRec}


def embed(rec, arr, ok, batch=256, swap=False):
    E = np.full((len(arr), 512), np.nan, np.float32)
    idx = np.nonzero(ok)[0]
    for s in range(0, len(idx), batch):
        b = idx[s:s + batch]
        x = np.asarray(arr[b])
        if swap:
            x = x[..., ::-1]
        f = rec(x)
        E[b] = f / np.linalg.norm(f, axis=1, keepdims=True)
    return E


def preflight(rec, cfg, arr, idx, emb):
    """AUC of s0 on real-image pairs in the first gap bin; repeated with colour channels swapped on the same faces."""
    out = out_dir(cfg)
    pairs = pd.read_csv(out / "pairs.csv")
    p = pairs[pairs.gap_bin == bin_labels(cfg["pairs"]["gap_edges"])[0]]
    p = p.sample(min(len(p), 20000), random_state=0)
    pos = {f: k for k, f in enumerate(idx.face_id)}
    i1, i2 = p.img_1.map(pos).to_numpy(), p.img_2.map(pos).to_numpy()
    res = {}
    for name, E in (("as_configured", emb), ("channels_swapped", None)):
        if E is None:
            used = np.unique(np.concatenate([i1, i2]))
            E = np.full_like(emb, np.nan)
            E[used] = embed(rec, arr[used], idx.det_ok.to_numpy()[used], swap=True)
        s = cos_rows(E[i1], E[i2])
        y = p.label.to_numpy()
        m = np.isfinite(s)
        res[name] = auc_w(s[m & (y == 1)], np.ones((m & (y == 1)).sum()), s[m & (y == 0)], np.ones((m & (y == 0)).sum()))
    res["pass"] = bool(res["as_configured"] >= cfg["analysis"]["preflight_min_auc"])
    res["warning"] = "swapped channels score higher: preprocessing likely wrong" if res["channels_swapped"] > res["as_configured"] else ""
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--recognizer", required=True)
    a = ap.parse_args()
    cfg = load_config(a.config)
    out = out_dir(cfg)
    c = cfg["recognizers"][a.recognizer]
    f112, edir = out_dir(cfg, "faces112"), out_dir(cfg, "emb", a.recognizer)
    pairs = pd.read_csv(out / "pairs.csv")
    real_ids = sorted(set(pairs.img_1) | set(pairs.img_2))
    groups = {"real": (real_ids, [out / "crops" / f"{i}.png" for i in real_ids])}
    for gdir in sorted((out / "gen").glob("*")) if (out / "gen").exists() else []:
        st = pd.read_csv(gdir / "status.csv")
        ids = st[st.ok].job_id.tolist()
        groups[gdir.name] = (ids, [gdir / f"{j}.png" for j in ids])
    rec = RECS[c["backend"]](c)
    for name, (ids, paths) in groups.items():
        arr, idx = make_crops(paths, ids, f112 / f"{name}.npy", f112 / f"{name}.csv")
        E = embed(rec, arr, idx.det_ok.to_numpy())
        np.save(edir / f"{name}.npy", E)
        idx.to_csv(edir / f"{name}.csv", index=False)
        print(f"{a.recognizer}/{name}: {int(np.isfinite(E[:, 0]).sum())} embeddings", flush=True)
        if name == "real":
            pf = preflight(rec, cfg, arr, idx, E)
            json.dump(pf, open(edir / "preflight.json", "w"), indent=1)
            print("preflight:", pf, flush=True)
            if not pf["pass"]:
                raise SystemExit(f"PREFLIGHT FAILED for {a.recognizer}: fix preprocessing before continuing")


if __name__ == "__main__":
    main()
