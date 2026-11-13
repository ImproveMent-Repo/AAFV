"""Inspect the frozen AAFV fusion models (ablations/variants/*/frozen.pkl) without data:
seed count, linear-head weights over the five similarity scores, and functional probes of the 11-input MLP.
Pickles are loaded with a restricted unpickler (only torch/numpy/sklearn containers are allowed).
Probes are evaluated on a grid of inputs, not on the data distribution (no pair vectors are available), so they describe
what the network *can* respond to, not how often each region occurs. Usage: python probe_fusion.py"""
import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
VAR = HERE.parent.parent / "Code" / "AAFV_Net" / "ablations" / "variants"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
ALLOW = {("collections", "OrderedDict"), ("torch._utils", "_rebuild_tensor_v2"), ("torch.storage", "_load_from_bytes"),
         ("numpy._core.multiarray", "_reconstruct"), ("numpy", "ndarray"), ("numpy", "dtype"), ("numpy._core.multiarray", "scalar"),
         ("sklearn.linear_model._logistic", "LogisticRegression")}
SCORES = ["arc", "eff", "vgg", "lpips", "ssim"]
INPUTS = ["Wd", "Ws", "Wf", "g", "Q", "enhanced", "R_sam", "R_diff", "avail_sam", "avail_diff", "avail_multi"]


class Dummy:
    def __init__(self, *a, **k): pass
    def __setstate__(self, s): self.__dict__.update(s if isinstance(s, dict) else {"state": s})


class U(pickle.Unpickler):
    def find_class(self, mod, name):
        if (mod, name) in (("__main__", "Scorer"), ("p10_ablations", "Scorer"), ("aafv.calib", "Calibrator")):
            return Dummy
        if (mod, name) in ALLOW:
            return super().find_class(mod, name)
        raise pickle.UnpicklingError(f"blocked {mod}.{name}")


class Fusion(nn.Module):                       # copy of Code/AAFV_Net/src/aafv/fusion.py (eval mode, dropout inactive)
    def __init__(self):
        super().__init__()
        self.ld, self.ls, self.lf = nn.Linear(5, 1), nn.Linear(5, 1), nn.Linear(5, 1)
        self.mlp = nn.Sequential(nn.Linear(11, 32), nn.ReLU(), nn.Dropout(0.1), nn.Linear(32, 16), nn.ReLU(), nn.Dropout(0.1), nn.Linear(16, 1))


def load(v):
    d = U(open(VAR / v / "frozen.pkl", "rb")).load()
    sc = d["scorer"]
    if sc.kind != "mlp":
        return None, d
    ms = []
    for st in sc.p:
        m = Fusion()
        m.load_state_dict(st)
        ms.append(m.eval())
    return ms, d


def probe(ms):
    """'Swing' of the fused logit S when one input moves across a plausible range, others held at typical values.
    Wd = ld(z_d) and Ws = ls(z_s) act on z-scored similarities, so their plausible range is taken as bias +/- 3 * ||w||_2
    (three standard deviations if the scores were uncorrelated). Averaged over a 21-point grid of the other branch and over seeds."""
    res = []
    for m in ms:
        bd, bs, wf = float(m.ld.bias), float(m.ls.bias), float(m.lf.bias)
        rd, rs = 3 * float(m.ld.weight.norm()), 3 * float(m.ls.weight.norm())
        def S(Wd, Ws, g=5 / 80, Q=0.6, R=0.6, asam=1.0, amulti=1.0):
            n = len(Wd)
            x = torch.zeros(n, 11)
            x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4] = Wd, Ws, wf, g, Q
            x[:, 6], x[:, 8], x[:, 10] = R, asam, amulti
            with torch.no_grad():
                return m.mlp(x).squeeze(1)
        gd = torch.linspace(bd - rd, bd + rd, 21)
        gs = torch.linspace(bs - rs, bs + rs, 21)
        Ws0, Wd0 = torch.full((21,), bs), torch.full((21,), bd)
        r = dict(Wd_range=f"{bd - rd:.2f}..{bd + rd:.2f}", Ws_range=f"{bs - rs:.2f}..{bs + rs:.2f}",
                 swing_Wd=float(np.mean([abs(float(S(torch.tensor([bd + rd]), torch.tensor([w]))) - float(S(torch.tensor([bd - rd]), torch.tensor([w])))) for w in gs])),
                 swing_Ws=float(np.mean([abs(float(S(torch.tensor([w]), torch.tensor([bs + rs]))) - float(S(torch.tensor([w]), torch.tensor([bs - rs])))) for w in gd])),
                 swing_R_sam_0p2_0p9=float((S(gd, Ws0, R=0.9) - S(gd, Ws0, R=0.2)).abs().mean()),
                 swing_g_5y_25y=float((S(gd, Ws0, g=25 / 80) - S(gd, Ws0, g=5 / 80)).abs().mean()),
                 swing_Q_0p3_0p9=float((S(gd, Ws0, Q=0.9) - S(gd, Ws0, Q=0.3)).abs().mean()),
                 swing_sam_unavailable=float((S(gd, torch.full((21,), bs), R=0.0, asam=0.0, amulti=0.0) - S(gd, Ws0)).abs().mean()))
        res.append(r)
    df = pd.DataFrame(res)
    out = {c: df[c].mean() for c in df.columns if c.startswith("swing")}
    out.update(Wd_range=res[0]["Wd_range"], Ws_range=res[0]["Ws_range"])
    return out, len(ms)


def main():
    rows, heads = [], []
    for vdir in sorted(VAR.iterdir()):
        try:
            ms, d = load(vdir.name)
        except pickle.UnpicklingError as e:
            print(vdir.name, "skipped:", e)
            continue
        dec = d.get("dec", {})
        if ms is None or ms == []:
            rows.append(dict(variant=vdir.name, kind="non-mlp", seeds=0, t_acc=dec.get("t_acc"), rho=dec.get("rho")))
            continue
        p, k = probe(ms)
        wd = np.stack([m.ld.weight.detach().numpy()[0] for m in ms]).mean(0)
        ws = np.stack([m.ls.weight.detach().numpy()[0] for m in ms]).mean(0)
        heads.append(dict(variant=vdir.name, branch="direct", **{s: float(w) for s, w in zip(SCORES, wd)}))
        heads.append(dict(variant=vdir.name, branch="sam", **{s: float(w) for s, w in zip(SCORES, ws)}))
        rows.append(dict(variant=vdir.name, kind="mlp", seeds=k, t_acc=dec.get("t_acc"), rho=dec.get("rho"),
                         pdl_coef=float(dec["pdl"].coef_[0][0]) if dec.get("pdl") is not None else np.nan,
                         psl_coef=float(dec["psl"].coef_[0][0]) if dec.get("psl") is not None else np.nan, **p))
    r, h = pd.DataFrame(rows), pd.DataFrame(heads)
    r.to_csv(OUT / "fusion_probe.csv", index=False)
    h.to_csv(OUT / "linear_heads.csv", index=False)
    pd.set_option("display.width", 250)
    print(r.round(3).to_string(index=False))
    print("\nLinear-head weights over the five standardized scores (seed mean):")
    print(h.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
