"""Analyses that the logged AAFV results can support without images, generated faces or weights.
Nothing here trains a model or sets a threshold. LA4 reads logged MORPH *test* outputs post hoc (Look-1 fused P and the
Siamese-ViT logits); it changes no parameter and is descriptive only (the MORPH test budget is spent).

LA1  ranking quality per age-gap bin, all 23 variants, MORPH calibration       (ablations/results/gap_report_calibration.csv)
LA2  ranking quality per impostor pool, all variants, MORPH calibration       (ablations/ablation_calibration.csv)
LA3  ranking vs decision: matched-FPR TPR next to auto-accept                 (both files)
LA4  matched-FMR comparison on identical MORPH test pairs, per gap bin:
     AAFV-Net (Look-1 P) vs Siamese ViT-B/16 logit, plus an impostor-like-genuine indicator
LA5  FG-NET adults (a >= 16), per gap bin, every logged variant               (ablations/extended_calibration_fg16.csv)
Usage: python run_log_analyses.py   (writes out/*.csv, out/*.png, out/summary.txt)"""
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
AAFV = ROOT / "Code" / "AAFV_Net"
sys.path.insert(0, str(HERE.parent / "exp0"))
from common import auc_w, tar_at_fmr  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
LOG = []
BIN_YEARS = {"G1": "0-4", "G2": "5-9", "G3": "10-14", "G4": "15-19", "G5": "20-29", "G6": "30+"}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def split_ci(s):
    """'0.9962 [0.9954,0.9969]' -> (0.9962, 0.9954, 0.9969)."""
    m = re.match(r"\s*([-\d.]+)\s*\[([-\d.]+),\s*([-\d.]+)\]", str(s))
    return tuple(float(x) for x in m.groups()) if m else (np.nan, np.nan, np.nan)


# ------------------------------------------------------------------ LA1
def la1():
    g = pd.read_csv(AAFV / "ablations/results/gap_report_calibration.csv")
    for c in ("AUC", "TPR@FPR0.001", "TPR@FPR0.01"):
        v = g[c].map(split_ci)
        g[c], g[c + "_lo"], g[c + "_hi"] = v.str[0], v.str[1], v.str[2]
    g["years"] = g.bin.map(BIN_YEARS)
    g.to_csv(OUT / "la1_gap_ranking_calibration.csv", index=False)
    key = ["arcface_only", "direct5_logreg", "direct_only_mlp", "sam_only_mlp", "full", "agg_no_shared_targets", "no_reliability",
           "no_branch_masking", "agg_fwd_only", "agg_shared_only", "guard_none"]
    piv = g[g.variant.isin(key)].pivot(index="variant", columns="bin", values="AUC").loc[key]
    say("\n[LA1] Calibration AUC by age-gap bin (genuine vs all impostors of that bin; n genuine G1..G6 = 22914, 594, 174, 44, 77, 35)")
    say(piv.round(3).to_string())
    piv2 = g[g.variant.isin(key)].pivot(index="variant", columns="bin", values="TPR@FPR0.001").loc[key]
    say("\n[LA1] Calibration TPR at FPR = 1e-3 by age-gap bin")
    say(piv2.round(3).to_string())

    # contrasts: CI overlap is the only test possible (bootstrap replicates were not saved, so paired differences cannot be formed)
    def cmp(a, b, metric="AUC"):
        rows = []
        for bn in BIN_YEARS:
            x = g[(g.variant == a) & (g.bin == bn)].iloc[0]
            y = g[(g.variant == b) & (g.bin == bn)].iloc[0]
            sep = "a>b" if x[metric + "_lo"] > y[metric + "_hi"] else ("a<b" if x[metric + "_hi"] < y[metric + "_lo"] else "overlap")
            rows.append(dict(contrast=f"{a} vs {b}", metric=metric, bin=bn, a=x[metric], b=y[metric], diff=x[metric] - y[metric], ci_relation=sep))
        return rows
    pairs = [("full", "direct_only_mlp"), ("full", "direct5_logreg"), ("full", "arcface_only"), ("sam_only_mlp", "direct_only_mlp"),
             ("full", "no_reliability"), ("full", "no_branch_masking"), ("full", "agg_no_shared_targets"), ("full", "agg_fwd_only"),
             ("full", "guard_none")]
    c = pd.DataFrame([r for a, b in pairs for m in ("AUC", "TPR@FPR0.001") for r in cmp(a, b, m)])
    c.to_csv(OUT / "la1_contrasts.csv", index=False)
    say("\n[LA1] Contrasts whose 95% CIs do not overlap (all others overlap):")
    say(c[c.ci_relation != "overlap"].round(4).to_string(index=False))

    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    show = {"arcface_only": "ArcFace only", "direct_only_mlp": "Direct-only MLP (no SAM)", "sam_only_mlp": "SAM-only MLP",
            "full": "AAFV-Net full", "agg_no_shared_targets": "No shared targets"}
    xs = np.arange(6)
    for k, (v, lab) in enumerate(show.items()):
        d = g[g.variant == v].set_index("bin").loc[list(BIN_YEARS)]
        for j, m in enumerate(("AUC", "TPR@FPR0.001")):
            ax[j].errorbar(xs + (k - 2) * 0.08, d[m], yerr=[d[m] - d[m + "_lo"], d[m + "_hi"] - d[m]], fmt="o-", ms=3, lw=1, capsize=2, label=lab)
    for j, (m, t) in enumerate((("AUC", "AUC per age-gap bin"), ("TPR@FPR0.001", "TPR at FPR = 0.1% per age-gap bin"))):
        ax[j].set_xticks(xs, [f"{b}\n{BIN_YEARS[b]}y" for b in BIN_YEARS])
        ax[j].set_title(t + " (MORPH calibration)", fontsize=9)
        ax[j].grid(alpha=0.3)
    ax[0].axhline(0.5, color="grey", lw=0.8, ls="--")
    ax[0].legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "la1_gap_ranking.png", dpi=200)
    return g


# ------------------------------------------------------------------ LA2 + LA3
def la2_la3():
    a = pd.read_csv(AAFV / "ablations/ablation_calibration.csv")
    cols = ["variant", "T_accept", "same_accept_all", "AUC_D_random", "TPR@FPR1e-3_D_random", "AUC_D_all_random", "TPR@FPR1e-3_D_all_random",
            "AUC_D_hard", "TPR@FPR1e-3_D_hard"]
    t = a[cols].copy()
    t.to_csv(OUT / "la2_pool_ranking_calibration.csv", index=False)
    say("\n[LA2/LA3] Calibration: ranking quality per impostor pool (threshold-free) next to the decision-rule auto-accept rate")
    keep = ["full", "arcface_only", "arcface_only_noguard", "direct5_logreg", "direct_only_mlp", "sam_only_mlp", "agg_no_shared_targets",
            "no_reliability", "no_branch_masking", "guard_none"]
    say(t.set_index("variant").loc[[k for k in keep if k in set(t.variant)]].round(4).to_string())


# ------------------------------------------------------------------ LA4
def boot_pairs(gs, ims, fmr, n_boot=200, seed=0):
    rng = np.random.default_rng(seed)
    tars, aucs = [], []
    for _ in range(n_boot):
        gw = rng.multinomial(len(gs), np.full(len(gs), 1 / len(gs))).astype(float)
        iw = rng.multinomial(len(ims), np.full(len(ims), 1 / len(ims))).astype(float)
        tars.append(tar_at_fmr(gs, gw, ims, iw, fmr)[0])
        aucs.append(auc_w(gs, gw, ims, iw))
    q = lambda x: (float(np.quantile(x, 0.025)), float(np.quantile(x, 0.975)))
    return q(tars), q(aucs)


def la4():
    z = pd.read_csv(AAFV / "q/report/test_pair_zones_look1.csv")
    v = np.load(AAFV / "baselines/siamese_vit/scores.npz")
    vit = pd.Series(v["logit"].astype(float), index=v["pair_id"])
    z["vit"] = vit.reindex(z.pair_id).to_numpy()
    assert z.vit.notna().all()
    rows, noise = [], []
    for pool in ("D_all_random", "D_hard"):
        for b in BIN_YEARS:
            gm = (z.set == "same") & (z.gap_bin == b)
            im = (z.set == pool) & (z.gap_bin == b)
            for model, col in (("AAFV-Net (Look-1 P)", "P"), ("Siamese ViT-B/16 (3 epochs)", "vit")):
                gs, ims = z.loc[gm, col].to_numpy(), z.loc[im, col].to_numpy()
                fmr = 1e-3 if len(ims) >= 3000 else 1e-2
                tar, _ = tar_at_fmr(gs, np.ones(len(gs)), ims, np.ones(len(ims)), fmr)
                auc = auc_w(gs, np.ones(len(gs)), ims, np.ones(len(ims)))
                (tl, th), (al, ah) = boot_pairs(gs, ims, fmr)
                rows.append(dict(pool=pool, bin=b, years=BIN_YEARS[b], model=model, n_genuine=len(gs), n_impostor=len(ims), fmr=fmr,
                                 tar=tar, tar_lo=tl, tar_hi=th, auc=auc, auc_lo=al, auc_hi=ah))
            if pool == "D_all_random":
                # impostor-like genuine pairs: below the 99th percentile of same-bin random impostors, per model
                lowp = z.loc[gm, "P"] < np.quantile(z.loc[im, "P"], 0.99)
                lowv = z.loc[gm, "vit"] < np.quantile(z.loc[im, "vit"], 0.99)
                noise.append(dict(bin=b, years=BIN_YEARS[b], n_genuine=int(gm.sum()), aafv_impostor_like=float(lowp.mean()),
                                  vit_impostor_like=float(lowv.mean()), both=float((lowp & lowv).mean()),
                                  expected_both_if_independent=float(lowp.mean() * lowv.mean())))
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "la4_test_matched_fmr.csv", index=False)
    nz = pd.DataFrame(noise)
    nz.to_csv(OUT / "la4_impostor_like_genuine.csv", index=False)
    say("\n[LA4] MORPH test, post hoc on logged outputs: TPR at matched FMR (1e-3 if >=3000 impostors in the bin, else 1e-2) and AUC,")
    say("      genuine pairs of a bin vs impostors of the same bin; 95% pair-level bootstrap CIs (person ids not logged, so CIs are too narrow)")
    say(r.assign(tar=r.tar.round(3), auc=r.auc.round(3), tar_ci=r.apply(lambda x: f"[{x.tar_lo:.3f},{x.tar_hi:.3f}]", axis=1),
                 auc_ci=r.apply(lambda x: f"[{x.auc_lo:.3f},{x.auc_hi:.3f}]", axis=1))
        [["pool", "bin", "years", "model", "n_genuine", "n_impostor", "fmr", "tar", "tar_ci", "auc", "auc_ci"]].to_string(index=False))
    say("\n[LA4] Genuine pairs scoring below the 99th percentile of same-bin random impostors ('impostor-like'), per model and jointly")
    say(nz.round(3).to_string(index=False))

    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    for j, pool in enumerate(("D_all_random", "D_hard")):
        for k, m in enumerate(r.model.unique()):
            d = r[(r.pool == pool) & (r.model == m)]
            xs = np.arange(len(d)) + (k - 0.5) * 0.12
            ax[j].errorbar(xs, d.tar, yerr=[d.tar - d.tar_lo, d.tar_hi - d.tar], fmt="o-", ms=3, lw=1, capsize=2, label=m)
        ax[j].set_xticks(np.arange(6), [f"{b}\n{BIN_YEARS[b]}y\nn={n}" for b, n in zip(BIN_YEARS, d.n_genuine)], fontsize=7)
        ax[j].set_title(f"MORPH test (post hoc): TPR at matched FMR vs {pool}", fontsize=9)
        ax[j].grid(alpha=0.3)
    ax[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "la4_test_matched_fmr.png", dpi=200)
    return r, nz


# ------------------------------------------------------------------ LA5
def la5():
    f = pd.read_csv(AAFV / "ablations/extended_calibration_fg16.csv")
    f = f[(f.split == "fgnet") & (np.isclose(f.beta, 0.01))]
    cols = ["variant", "T_accept", "same_acc", "same_acc_lo", "same_acc_hi", "same_rej"] + [f"same_acc_G{i}" for i in range(1, 7)]
    t = f[cols].copy()
    t.to_csv(OUT / "la5_fgnet_adults_by_gap.csv", index=False)
    say("\n[LA5] FG-NET adults (a >= 16, cut-off chosen post hoc), MORPH-frozen thresholds, beta = 0.01: auto-accept by gap bin and false-reject rate")
    say("      genuine counts G1..G6 = 405, 356, 261, 170, 186, 78; every rate is at that method's own zero-calibration-FA threshold")
    say(t.round(3).to_string(index=False))


if __name__ == "__main__":
    la1()
    la2_la3()
    la4()
    la5()
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")
    print(f"\nwrote {OUT}")
