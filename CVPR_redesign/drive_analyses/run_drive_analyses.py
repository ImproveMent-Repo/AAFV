"""Analyses on the AAFV calibration pair vectors and per-face file downloaded from the shared Drive backup
(CVPR_redesign/drive_data/, git-ignored). Calibration split only (allowed: it is not the spent MORPH test split).
No model is trained except cross-fitted 2-feature logistic regressions used as model-free branch probes.

DA1  Reconstruct the frozen Look-2 'full' decision layer and check that it reproduces the published T_acc, T_rej, accept rate.
DA2  Counterfactual: put back the 4 persons quarantined by hand after the draft calibration; recompute T_acc and accept.
DA3  Matched-FMR comparisons per gap bin and impostor pool with a paired person-cluster bootstrap:
     ArcFace direct cosine (d_arc), SAM-branch ArcFace (s_arc), fused logit, and a cross-fitted logistic on [d_arc, s_arc].
DA4  Label linkage: genuine pairs whose image-file prefixes disagree with the person id, by gap bin, and their scores.
DA5  SAM faces: identity similarity to the source and age accuracy by target age and direction (ArcFace-based: circular).
Usage: python run_drive_analyses.py [--bootstrap 300]"""
import argparse
import pickle
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = HERE.parent / "drive_data"
AAFV = ROOT / "Code" / "AAFV_Net"
sys.path.insert(0, str(HERE.parent / "exp0"))
sys.path.insert(0, str(AAFV / "src"))
from common import ClusterBootstrap, auc_w, percentile_ci, tar_at_fmr  # noqa: E402
from aafv import thresholds as TH  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
LOG = []
COLS = ["arc", "eff", "vgg", "lpips", "ssim"]
CTX = ["g", "Q", "enhanced_pair", "R_sam", "R_diff", "avail_sam", "avail_diff", "avail_multi"]
MANUAL4 = {"290132", "303269", "314177", "321217"}
BINS = ["G1", "G2", "G3", "G4", "G5", "G6"]
YEARS = {"G1": "0-4", "G2": "5-9", "G3": "10-14", "G4": "15-19", "G5": "20-29", "G6": "30+"}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ frozen model (restricted unpickler)
class Dummy:
    def __init__(self, *a, **k): pass
    def __setstate__(self, s): self.__dict__.update(s if isinstance(s, dict) else {"state": s})


ALLOW = {("collections", "OrderedDict"), ("torch._utils", "_rebuild_tensor_v2"), ("torch.storage", "_load_from_bytes"),
         ("numpy._core.multiarray", "_reconstruct"), ("numpy", "ndarray"), ("numpy", "dtype"), ("numpy._core.multiarray", "scalar"),
         ("sklearn.linear_model._logistic", "LogisticRegression")}


class U(pickle.Unpickler):
    def find_class(self, m, n):
        if (m, n) in (("__main__", "Scorer"), ("p10_ablations", "Scorer"), ("aafv.calib", "Calibrator")):
            return Dummy
        if (m, n) in ALLOW:
            return super().find_class(m, n)
        raise pickle.UnpicklingError(f"blocked {m}.{n}")


class Fusion(nn.Module):
    def __init__(self):
        super().__init__()
        self.ld, self.ls, self.lf = nn.Linear(5, 1), nn.Linear(5, 1), nn.Linear(5, 1)
        self.mlp = nn.Sequential(nn.Linear(11, 32), nn.ReLU(), nn.Dropout(0.1), nn.Linear(32, 16), nn.ReLU(), nn.Dropout(0.1), nn.Linear(16, 1))

    def forward(self, D, S, F, C):
        W = torch.cat([self.ld(D), self.ls(S), self.lf(F)], 1)
        return self.mlp(torch.cat([W, C], 1)).squeeze(1), W


def score_full(v):
    d = U(open(AAFV / "ablations/variants/full/frozen.pkl", "rb")).load()
    arr = lambda p: torch.from_numpy(v[[p + c for c in COLS]].to_numpy(np.float32))
    D, S, F = arr("d_"), arr("s_"), arr("f_")
    C = torch.from_numpy(v[CTX].to_numpy(np.float32))
    Ssum, Wsum = 0, 0
    with torch.no_grad():
        for st in d["scorer"].p:
            m = Fusion()
            m.load_state_dict(st)
            m.eval()
            s, w = m(D, S, F, C)
            Ssum, Wsum = Ssum + s.numpy(), Wsum + w.numpy()
    k = len(d["scorer"].p)
    return Ssum / k, Wsum / k, d["dec"]


def decision(v, S, W, dec, rho=None):
    cal = dec["cal"]
    P = cal.m.predict_proba(np.asarray(S).reshape(-1, 1))[:, 1]
    Pd = dec["pdl"].predict_proba(W[:, [0]])[:, 1]
    Ps = dec["psl"].predict_proba(W[:, [1]])[:, 1]
    rho = dec["rho"] if rho is None else rho
    ok = (v.Q.to_numpy() >= dec["qmin"]) & (Pd >= rho) & ((v.avail_sam.to_numpy() == 0) | ((v.R_sam.to_numpy() >= dec["rmin"]) & (Ps >= rho)))
    return P, ok


def fit_thresholds(P, ok, y, beta=0.01):
    imp = P[(y == 0) & ok]
    t_acc = 2.0 if len(imp) == 0 else TH.thresholds(imp, P[y == 1])[0]
    t_rej = float(np.quantile(P[y == 1], beta))
    acc = float(((P >= t_acc) & ok)[y == 1].mean())
    return t_acc, t_rej, acc


# ------------------------------------------------------------------ DA1 + DA2
def da1_da2(v, S, W, dec):
    q = set(pd.read_csv(AAFV / "audit/quarantine_people.csv", dtype=str).person_id)
    in_q = v.person_id_1.isin(q) | v.person_id_2.isin(q)
    in4 = v.person_id_1.isin(MANUAL4) | v.person_id_2.isin(MANUAL4)
    keep = (~in_q).to_numpy()
    keep4 = (~in_q | in4).to_numpy()                     # official set plus the 4 hand-quarantined persons' pairs
    y = v.label.to_numpy()
    P, ok = decision(v, S, W, dec)
    say("\n[DA1] Reconstruction of the frozen Look-2 'full' decision layer on the official calibration set (858 persons removed)")
    ta, tr, acc = fit_thresholds(P[keep], ok[keep], y[keep])
    say(f"  n pairs {keep.sum():,} | T_acc {ta:.6f} (published 0.956438) | T_rej(0.01) {tr:.6f} (published 0.007541) | genuine accept {100 * acc:.2f}% (published 73.26%)")
    rows = [dict(set="official (858 quarantined)", rho=dec["rho"], t_acc=ta, t_rej=tr, accept=acc, n=int(keep.sum()))]
    say("\n[DA2] Counterfactual: official set + the 4 persons quarantined by hand after the draft calibration")
    for rho in (0.20, 0.35, 0.50):
        P2, ok2 = decision(v, S, W, dec, rho)
        for lab, m in (("official", keep), ("official + 4 persons", keep4)):
            ta, tr, acc = fit_thresholds(P2[m], ok2[m], y[m])
            rows.append(dict(set=lab, rho=rho, t_acc=ta, t_rej=tr, accept=acc, n=int(m.sum())))
            say(f"  rho {rho:.2f} | {lab:22s} | T_acc {ta:.4f} | genuine accept {100 * acc:6.2f}%")
    pd.DataFrame(rows).to_csv(OUT / "da2_threshold_counterfactual.csv", index=False)
    t = v[in4].assign(P=P[in4], guard_ok=ok[in4])
    top = t[t.label == 0].sort_values("P", ascending=False).head(12)
    say("\n[DA2] Highest-scoring impostor pairs involving the 4 persons (Look-2 model)")
    say(top[["pair_id", "set_name", "person_id_1", "person_id_2", "img_id_1", "img_id_2", "gap", "d_arc", "P", "guard_ok"]].round(4).to_string(index=False))
    gen4 = t[t.label == 1]
    say(f"  their 16 genuine pairs: median d_arc z {gen4.d_arc.median():.2f} (all genuine: {v[v.label == 1].d_arc.median():.2f})")
    dr = t[t.set_name == "D_random"]
    say(f"  their D_random pairs: {len(dr)}; max P {dr.P.max():.4f}; guard-passing: {int(dr.guard_ok.sum())}")
    top.to_csv(OUT / "da2_manual4_top_pairs.csv", index=False)
    return keep, P, ok


# ------------------------------------------------------------------ DA3
def crossfit_logit(X, y, groups, k=5, seed=0):
    rng = np.random.default_rng(seed)
    persons = np.unique(groups)
    fold_of = dict(zip(persons, rng.integers(0, k, len(persons))))
    f = np.array([fold_of[g] for g in groups])
    s = np.zeros(len(y))
    for i in range(k):
        tr, te = f != i, f == i
        s[te] = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X[tr], y[tr]).decision_function(X[te])
    return s


def da3(v, keep, S, W, n_boot):
    d = v[keep].reset_index(drop=True)
    y = d.label.to_numpy()
    scores = {"ArcFace direct (d_arc)": d.d_arc.to_numpy(),
              "SAM-branch ArcFace (s_arc)": d.s_arc.to_numpy(),
              "AAFV-Net fused (Look-2)": S[keep],
              "LogReg [d_arc, s_arc] (cross-fitted)": crossfit_logit(d[["d_arc", "s_arc"]].to_numpy(), y, d.person_id_1.to_numpy())}
    base = "ArcFace direct (d_arc)"
    rows = []
    for pool in ("D_all_random", "D_hard"):
        for b in BINS:
            m = (d.gap_bin == b).to_numpy() & ((y == 1) | (d.set_name == pool).to_numpy())
            yy = y[m]
            n_i = int((yy == 0).sum())
            fmr = 1e-3 if n_i >= 3000 else 1e-2
            bs = ClusterBootstrap(d.person_id_1.to_numpy()[m], d.person_id_2.to_numpy()[m], n_boot, 7)
            pts = {k: (tar_at_fmr(s[m][yy == 1], np.ones((yy == 1).sum()), s[m][yy == 0], np.ones(n_i), fmr)[0],
                       auc_w(s[m][yy == 1], np.ones((yy == 1).sum()), s[m][yy == 0], np.ones(n_i))) for k, s in scores.items()}
            reps = {k: [] for k in scores}
            for w in bs.weights():
                for k, s in scores.items():
                    reps[k].append((tar_at_fmr(s[m][yy == 1], w[yy == 1], s[m][yy == 0], w[yy == 0], fmr)[0],
                                    auc_w(s[m][yy == 1], w[yy == 1], s[m][yy == 0], w[yy == 0])))
            for k in scores:
                tar = np.array([r[0] for r in reps[k]])
                au = np.array([r[1] for r in reps[k]])
                tb = np.array([r[0] for r in reps[base]])
                ab = np.array([r[1] for r in reps[base]])
                rows.append(dict(pool=pool, bin=b, years=YEARS[b], score=k, n_genuine=int((yy == 1).sum()), n_impostor=n_i, fmr=fmr,
                                 tar=pts[k][0], tar_ci=percentile_ci(tar, 0.95), auc=pts[k][1], auc_ci=percentile_ci(au, 0.95),
                                 d_tar_vs_arcface=pts[k][0] - pts[base][0], d_tar_ci=percentile_ci(tar - tb, 0.95),
                                 d_auc_vs_arcface=pts[k][1] - pts[base][1], d_auc_ci=percentile_ci(au - ab, 0.95)))
    r = pd.DataFrame(rows)
    for c in [c for c in r.columns if c.endswith("_ci")]:
        r[c + "_lo"], r[c + "_hi"] = r[c].str[0], r[c].str[1]
    r = r.drop(columns=[c for c in r.columns if c.endswith("_ci")])
    r.to_csv(OUT / "da3_matched_fmr_calibration.csv", index=False)
    say(f"\n[DA3] Calibration split, matched FMR per gap bin (1e-3 if >=3000 impostors else 1e-2); paired person-cluster bootstrap ({n_boot}); deltas vs ArcFace direct")
    for pool in ("D_all_random", "D_hard"):
        say(f"\n  vs {pool}")
        t = r[r.pool == pool]
        for b in BINS:
            tt = t[t.bin == b]
            say(f"  {b} ({YEARS[b]} y, n={tt.n_genuine.iloc[0]}, FMR {tt.fmr.iloc[0]:g}): " + " | ".join(
                f"{s.split(' (')[0][:22]} TAR {x.tar:.3f} (d {x.d_tar_vs_arcface:+.3f} [{x.d_tar_ci_lo:+.3f},{x.d_tar_ci_hi:+.3f}])" for s, x in zip(tt.score, tt.itertuples())))
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    for j, pool in enumerate(("D_all_random", "D_hard")):
        for k, s in enumerate(scores):
            t = r[(r.pool == pool) & (r.score == s)]
            xs = np.arange(6) + (k - 1.5) * 0.09
            ax[j].errorbar(xs, t.tar, yerr=[t.tar - t.tar_ci_lo, t.tar_ci_hi - t.tar], fmt="o-", ms=3, lw=1, capsize=2, label=s)
        ax[j].set_xticks(np.arange(6), [f"{b}\n{YEARS[b]}y" for b in BINS])
        ax[j].set_title(f"MORPH calibration: TAR at matched FMR vs {pool}", fontsize=9)
        ax[j].grid(alpha=0.3)
    ax[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "da3_matched_fmr.png", dpi=200)


# ------------------------------------------------------------------ DA4
def da4(v, keep):
    g = v[keep & (v.label == 1).to_numpy()].copy()
    pre = lambda s: s.str.split("_").str[0].str.lstrip("0")
    g["p1"], g["p2"], g["pid"] = pre(g.img_id_1), pre(g.img_id_2), g.person_id_1.str.lstrip("0")
    g["file_ids_differ"] = g.p1 != g.p2
    g["file_id_not_person"] = (g.p1 != g.pid) | (g.p2 != g.pid)
    imp = v[keep & (v.set_name == "D_all_random").to_numpy()]
    rows = []
    for b in BINS:
        t = g[g.gap_bin == b]
        thr = np.quantile(imp[imp.gap_bin == b].d_arc, 0.99)
        low = t.d_arc < thr
        rows.append(dict(bin=b, years=YEARS[b], n_genuine=len(t), file_ids_differ=float(t.file_ids_differ.mean()),
                         file_id_not_person=float(t.file_id_not_person.mean()), arcface_impostor_like=float(low.mean()),
                         impostor_like_if_ids_differ=float(low[t.file_ids_differ].mean()) if t.file_ids_differ.any() else np.nan,
                         impostor_like_if_ids_same=float(low[~t.file_ids_differ].mean()) if (~t.file_ids_differ).any() else np.nan))
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "da4_label_linkage.csv", index=False)
    say("\n[DA4] Genuine calibration pairs: do the two image files carry different MORPH ids? ('impostor-like' = ArcFace below the 99th pct of same-bin random impostors)")
    say(r.round(3).to_string(index=False))
    ex = g[g.file_ids_differ].groupby("gap_bin").head(2)[["gap_bin", "person_id_1", "img_id_1", "img_id_2", "d_arc"]]
    say("  examples:\n" + ex.round(2).to_string(index=False))


# ------------------------------------------------------------------ DA5
def da5():
    f = pd.read_csv(DATA / "faces.csv")
    o = f[f.kind == "orig"].set_index("img_id")
    s = f[f.kind != "orig"].copy()
    s["src_est_age"] = o.est_age.reindex(s.img_id).to_numpy()
    s["shift"] = s.target_age - s.src_est_age
    s["direction"] = np.where(s["shift"] >= 0, "older", "younger")
    s["abs_shift_bin"] = pd.cut(s["shift"].abs(), [0, 5, 15, 30, 100], right=False, labels=["0-4", "5-14", "15-29", "30+"])
    s["age_err"] = (s.est_age - s.target_age).abs()
    s["target_bin"] = pd.cut(s.target_age, [0, 20, 30, 40, 50, 60, 70, 101], right=False)
    say(f"\n[DA5] SAM faces: {len(s):,} generated, {len(o):,} originals. Identity = ArcFace cosine to the source image (in-pipeline recognizer: circular, and fed misaligned crops)")
    t1 = s.groupby(["direction", "abs_shift_bin"], observed=True).agg(n=("arc_to_orig", "size"), id_cos_median=("arc_to_orig", "median"),
                                                                   id_cos_p10=("arc_to_orig", lambda x: x.quantile(0.1)),
                                                                   share_below_0p3=("arc_to_orig", lambda x: (x < 0.3).mean()),
                                                                   age_err_median=("age_err", "median"))
    t2 = s.groupby("target_bin", observed=True).agg(n=("arc_to_orig", "size"), id_cos_median=("arc_to_orig", "median"),
                                                    share_below_0p3=("arc_to_orig", lambda x: (x < 0.3).mean()), age_err_median=("age_err", "median"))
    say(t1.round(3).to_string())
    say(t2.round(3).to_string())
    t1.to_csv(OUT / "da5_sam_identity_by_shift.csv")
    t2.to_csv(OUT / "da5_sam_identity_by_target_age.csv")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for k, dirn in enumerate(("younger", "older")):
        t = s[s.direction == dirn]
        b = pd.cut(t["shift"].abs(), np.arange(0, 61, 5), right=False)
        g = t.groupby(b, observed=True).arc_to_orig
        ax[0].plot([i.left for i in g.median().index], g.median().values, "o-", ms=3, label=f"{dirn}: median")
        ax[0].fill_between([i.left for i in g.median().index], g.quantile(0.1).values, g.quantile(0.9).values, alpha=0.15)
        g2 = t.groupby(b, observed=True).age_err.median()
        ax[1].plot([i.left for i in g2.index], g2.values, "o-", ms=3, label=dirn)
    ax[0].set_xlabel("|target age - source age| (years)")
    ax[0].set_ylabel("ArcFace cosine to source")
    ax[0].set_title("SAM identity drift (10-90% band)", fontsize=9)
    ax[1].set_xlabel("|target age - source age| (years)")
    ax[1].set_ylabel("median |estimated age - target|")
    ax[1].set_title("SAM age accuracy", fontsize=9)
    for a in ax:
        a.grid(alpha=0.3)
        a.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "da5_sam_identity_age.png", dpi=200)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=300)
    a = ap.parse_args()
    v = pd.read_csv(DATA / "pair_vectors_calibration.csv", dtype={"person_id_1": str, "person_id_2": str, "img_id_1": str, "img_id_2": str})
    S, W, dec = score_full(v)
    keep, P, ok = da1_da2(v, S, W, dec)
    da3(v, keep, S, W, a.bootstrap)
    da4(v, keep)
    da5()
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
