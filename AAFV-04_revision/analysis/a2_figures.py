"""Figures for the AAFV-04 revision from verified logs/CSVs only (no new model runs).
Fig R1: post hoc diagnostics of the Look-1 scorer on MORPH test. Fig R2: three-way outcome shares, MORPH test (Look 2) and FG-NET adults."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(R, "..", "..", "Code", "AAFV_Net"); F = os.path.join(R, "..", "manuscript", "figures")
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7})
L = pd.read_csv(os.path.join(C, "q/report/test_pair_zones_look1.csv"))
fig, ax = plt.subplots(1, 3, figsize=(7.16, 2.4))
bins = np.logspace(-4, 0, 60)
for s, c, lab in (("same", "#1b7837", "Genuine (24,305)"), ("D_random", "#2166ac", r"$\mathcal{D}_{\rm random}$ (1,149)"), ("D_all_random", "#92c5de", r"$\mathcal{D}_{\rm all\_random}$ (277,822)"), ("D_hard", "#b2182b", r"$\mathcal{D}_{\rm hard}$ (35,735)")):
    p = np.clip(L[L.set == s].P.to_numpy(), 1e-4, 1); ax[0].hist(p, bins=bins, density=True, histtype="step", lw=1.2, color=c, label=lab)
ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].axvline(0.007541, ls="--", c="k", lw=0.8); ax[0].axvline(0.95657, ls=":", c="k", lw=0.8)
ax[0].set_xlabel("Look-1 fused probability $P$"); ax[0].set_ylabel("Density (log)"); ax[0].set_title("(a) Class-conditional $P$", pad=26); ax[0].legend(loc="lower center", bbox_to_anchor=(0.5, 1.12), ncol=2, frameon=False, fontsize=5.5, handlelength=1.2, columnspacing=0.8)
rel = pd.read_csv(os.path.join(R, "out", "a1_reliability_genuine+D_all_random.csv"))
ax[1].plot([0, 1], [0, 1], c="0.6", lw=0.8); ax[1].scatter(rel.mean_p, rel.frac_pos, s=8 + 30 * np.log10(rel.n) / np.log10(rel.n.max()), c="#2166ac")
for _, r in rel.iterrows(): ax[1].plot([r.mean_p, r.mean_p], [r.mean_p, r.frac_pos], c="#b2182b", lw=0.6)
ax[1].set_xlabel("Mean predicted $P$ (15 bins)"); ax[1].set_ylabel("Observed genuine fraction"); ax[1].set_title("(b) Reliability: genuine + $\\mathcal{D}_{\\rm all\\_random}$")
rc = pd.read_csv(os.path.join(R, "out", "a1_risk_coverage_look1.csv")).sort_values("thr")
ax[2].plot(rc.genuine_cov, rc.FA_hard, c="#b2182b", label=r"FA on $\mathcal{D}_{\rm hard}$"); ax[2].plot(rc.genuine_cov, rc.FA_all_random, c="#92c5de", label=r"FA on $\mathcal{D}_{\rm all\_random}$")
ax[2].set_yscale("symlog", linthresh=1); ax[2].set_xlim(0.5, 1.0); ax[2].axvline(0.7974, c="k", ls=":", lw=0.8)
ax[2].set_xlabel("Genuine coverage (ungated $P\\geq t$)"); ax[2].set_ylabel("False accepts (count)"); ax[2].set_title("(c) Accept-side risk-coverage"); ax[2].legend(frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(F, "figR1_posthoc_diagnostics.pdf")); fig.savefig(os.path.join(F, "figR1_posthoc_diagnostics.png"), dpi=200)
# ---- Fig R2
E = pd.read_csv(os.path.join(C, "ablations/extended_test.csv")); E = E[E.beta == 0.01].set_index("variant")
G = pd.read_csv(os.path.join(C, "ablations/extended_calibration_fg16.csv")); G = G[(G.beta == 0.01) & (G.split == "fgnet")].set_index("variant")
rows = []
for v, n in (("full", "AAFV-Net"), ("arcface_only", "ArcFace")):
    e = E.loc[v]; g = G.loc[v]
    rows += [(f"MORPH genuine\n{n}", e.same_acc, e.same_rev, e.same_rej, "g"), (f"MORPH $\\mathcal{{D}}_{{\\rm random}}$\n{n}", e.D_random_FA / e.D_random_n, e.D_random_rev, e.D_random_rej, "i"),
             (f"MORPH $\\mathcal{{D}}_{{\\rm hard}}$\n{n}", e.D_hard_FA / e.D_hard_n, e.D_hard_rev, e.D_hard_rej, "i"),
             (f"FG-NET adult gen.\n{n}", g.same_acc, g.same_rev, g.same_rej, "g"), (f"FG-NET adult imp.\n{n}", g.FG_random_FA / g.FG_random_n, g.FG_random_rev, g.FG_random_rej, "i")]
order = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]; rows = [rows[i] for i in order]
fig, ax = plt.subplots(figsize=(7.16, 2.3)); y = np.arange(len(rows))[::-1]
for k, (lab, acc, rev, rej, kind) in enumerate(rows):
    ca, cj = ("#1b7837", "#d6604d") if kind == "g" else ("#b2182b", "#4393c3")
    ax.barh(y[k], acc, color=ca, height=0.7); ax.barh(y[k], rev, left=acc, color="#f4c542", height=0.7); ax.barh(y[k], rej, left=acc + rev, color=cj, height=0.7)
    ax.text(1.005, y[k], f"A {100*acc:.2f} | R {100*rev:.1f} | X {100*rej:.2f}", va="center", fontsize=6)
ax.set_yticks(y); ax.set_yticklabels([r[0].replace("\n", " - ") for r in rows], fontsize=6.5); ax.set_xlim(0, 1.32); ax.set_xticks([0, .25, .5, .75, 1])
ax.set_xlabel("Share of pairs: Auto-Accept (A), Manual Review (R), Auto-Reject (X); $\\beta=0.01$")
fig.tight_layout(); fig.savefig(os.path.join(F, "figR2_outcomes.pdf")); fig.savefig(os.path.join(F, "figR2_outcomes.png"), dpi=200); print("ok")
