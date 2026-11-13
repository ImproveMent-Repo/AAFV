"""Build every table (tables/*.tex) and copy every figure (figures/*.png) of AAFV-05 from the verified analysis outputs.
No number in the manuscript tables is typed by hand: re-run this script after any analysis is re-run.

Sources (all produced by scripts in CVPR_redesign/):
  log_analyses/out/la1_gap_ranking_calibration.csv, la2_pool_ranking_calibration.csv, la4_impostor_like_genuine.csv
  architecture_review/out/fusion_probe.csv, linear_heads.csv
  drive_analyses/out/da2_threshold_counterfactual.csv, da3_matched_fmr_calibration.csv,
                     da4_label_linkage.csv, da4b_sex_mismatch.csv, da5_sam_identity_by_shift.csv
Usage: python scripts/build_assets.py   (from publication_AAFV-05/)"""
import shutil
from pathlib import Path

import pandas as pd

PUB = Path(__file__).resolve().parent.parent
R = PUB.parent / "CVPR_redesign"
TAB, FIG = PUB / "tables", PUB / "figures"
TAB.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
YEARS = {"G1": "0--4", "G2": "5--9", "G3": "10--14", "G4": "15--19", "G5": "20--29", "G6": "30+"}


def f3(x):
    return f"{x:.3f}"


def pct(x, d=2):
    return f"{100 * x:.{d}f}"


def sgn(x):
    v = round(float(x), 3)
    return f"{0.0 if v == 0 else v:+.3f}"          # avoid printing "-0.000"


def ci(lo, hi):
    return f"[{sgn(lo)}, {sgn(hi)}]"


def write(name, body):
    # every tabular is wrapped in \fittab{...} (defined in main.tex): shrunk only if wider than the column
    body = body.replace(r"\begin{tabular}", r"\fittab{\begin{tabular}").replace(r"\end{tabular}", r"\end{tabular}}")
    (TAB / name).write_text(body, encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- T1 reconstruction and counterfactual
c = pd.read_csv(R / "drive_analyses/out/da2_threshold_counterfactual.csv")
off = c.iloc[0]
rows = []
for rho in (0.20, 0.35, 0.50):
    a = c[(c.set == "official") & (c.rho.round(2) == rho)].iloc[0]
    b = c[(c.set == "official + 4 persons") & (c.rho.round(2) == rho)].iloc[0]
    fa = "none passes" if a.t_acc >= 2 else f"{a.t_acc:.4f}"
    fb = "none passes" if b.t_acc >= 2 else f"{b.t_acc:.4f}"
    rows.append(f"{rho:.2f} & {fa} & {pct(a.accept)} & {fb} & {pct(b.accept)} \\\\")
write("tab_reconstruction.tex", r"""\begin{table}[t]
\centering
\caption{Reconstruction of the frozen decision layer on the MORPH calibration split, and the effect of the four persons removed after the draft calibration. Accept = genuine auto-accept rate. ``None passes'': no impostor passes the guards, which the pipeline encodes as an unattainable threshold.}
\label{tab:reconstruction}
\footnotesize
\begin{tabular}{@{}lccc@{}}
\toprule
Quantity (official set, $\rho=0.20$, $n=""" + f"{int(off.n):,}" + r"""$ pairs) & Recomputed & Published \\
\midrule
Accept threshold $T_\mathrm{acc}$ & """ + f"{off.t_acc:.6f}" + r""" & 0.956438 \\
Reject threshold $T_\mathrm{rej}(\beta{=}0.01)$ & """ + f"{off.t_rej:.6f}" + r""" & 0.007541 \\
Genuine auto-accept (\%) & """ + pct(off.accept) + r""" & 73.26 \\
\bottomrule
\end{tabular}

\vspace{4pt}
\begin{tabular}{@{}ccccc@{}}
\toprule
 & \multicolumn{2}{c}{Official set} & \multicolumn{2}{c}{Official $+$ 4 persons} \\
\cmidrule(lr){2-3}\cmidrule(l){4-5}
$\rho$ & $T_\mathrm{acc}$ & Accept (\%) & $T_\mathrm{acc}$ & Accept (\%) \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T2 decision rate vs ranking
p = pd.read_csv(R / "log_analyses/out/la2_pool_ranking_calibration.csv").set_index("variant")
names = [("full", "AAFV-Net (full)"), ("arcface_only", "ArcFace, guarded"), ("arcface_only_noguard", "ArcFace, no guards"),
         ("direct5_logreg", "Direct 5-score LogReg"), ("direct_only_mlp", "Direct-only MLP (no SAM)"),
         ("agg_no_shared_targets", "AAFV-Net, no shared targets")]
rows = []
for k, lab in names:
    x = p.loc[k]
    t = "none" if x.T_accept >= 1 else f"{x.T_accept:.3f}"
    rows.append(f"{lab} & {t} & {pct(x.same_accept_all, 1)} & {f3(x['TPR@FPR1e-3_D_all_random'])} & {f3(x['AUC_D_all_random'])} & {f3(x['TPR@FPR1e-3_D_hard'])} & {f3(x['AUC_D_hard'])} \\\\")
write("tab_decision_ranking.tex", r"""\begin{table}[t]
\centering
\caption{Decision rate versus ranking quality on the MORPH calibration split. The auto-accept rate depends on where each method's zero-false-accept threshold falls; the threshold-free ranking metrics show that the methods discriminate almost identically. A threshold $\geq 1$ (``none'') admits nobody.}
\label{tab:decision}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}lcccccc@{}}
\toprule
 & & & \multicolumn{2}{c}{Random impostors} & \multicolumn{2}{c}{ArcFace-mined} \\
\cmidrule(lr){4-5}\cmidrule(l){6-7}
Method & $T_\mathrm{acc}$ & Accept (\%) & TPR@$10^{-3}$ & AUC & TPR@$10^{-3}$ & AUC \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T3 matched FMR (per pair, paired bootstrap)
m = pd.read_csv(R / "drive_analyses/out/da3_matched_fmr_calibration.csv")
order = ["ArcFace direct (d_arc)", "SAM-branch ArcFace (s_arc)", "AAFV-Net fused (Look-2)", "LogReg [d_arc, s_arc] (cross-fitted)"]
short = {order[0]: "ArcFace (original pair)", order[1]: "ArcFace (generated pair)", order[2]: "AAFV-Net fused", order[3]: "LogReg: original $+$ generated"}
rows = []
for pool, plab in (("D_all_random", "Random impostors"), ("D_hard", "ArcFace-mined look-alikes")):
    rows.append(r"\multicolumn{5}{@{}l}{\emph{" + plab + r"}} \\")
    for b in ("G1", "G2", "G3"):
        t = m[(m.pool == pool) & (m.bin == b)].set_index("score")
        first = True
        for s in order:
            x = t.loc[s]
            lead = f"{YEARS[b]} ({int(x.n_genuine)})" if first else ""
            first = False
            d = "--" if s == order[0] else f"{sgn(x.d_tar_vs_arcface)} {ci(x.d_tar_ci_lo, x.d_tar_ci_hi)}"
            rows.append(f"{lead} & {short[s]} & {f3(x.tar)} & {d} & {f3(x.auc)} \\\\")
        rows.append(r"\addlinespace[1pt]")
lg = m[(m.pool == "D_all_random") & m.bin.isin(["G4", "G5", "G6"]) & (m.score == order[0])]
note = "; ".join(f"{YEARS[r.bin]} y: {f3(r.tar)} (n={int(r.n_genuine)})" for r in lg.itertuples())
write("tab_matched_fmr.tex", r"""\begin{table}[t]
\centering
\caption{Per-pair comparison at matched false-match rate (FMR $=10^{-3}$) on the MORPH calibration split. $\Delta$ is the difference in TAR from ArcFace on the original pair, with a 95\% paired two-way person-cluster bootstrap interval (300 replicates). For gaps of 15 years and more every score has the same TAR against random impostors (""" + note + r"""); those bins are analysed in Section~\ref{sec:labels}.}
\label{tab:matched}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llccc@{}}
\toprule
Gap, y ($n$ gen.) & Score & TAR & $\Delta$TAR [95\% CI] & AUC \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T4 probe of the fusion network
fp = pd.read_csv(R / "architecture_review/out/fusion_probe.csv").set_index("variant")
lh = pd.read_csv(R / "architecture_review/out/linear_heads.csv")
dh = lh[(lh.variant == "full") & (lh.branch == "direct")].iloc[0]
sh = lh[(lh.variant == "full") & (lh.branch == "sam")].iloc[0]
F, DO, NC = fp.loc["full"], fp.loc["direct_only_mlp"], fp.loc["no_context"]
write("tab_probe.tex", r"""\begin{table}[t]
\centering
\caption{What the frozen fusion network uses. Top: weights of the two linear branch heads on the five z-scored similarities (mean of """ + f"{int(F.seeds)}" + r""" seeds). Bottom: change of the fused logit when one input moves across a plausible range (branch logits: bias $\pm 3\|w\|$; gap 5$\to$25 y; quality 0.3$\to$0.9; $R_\mathrm{sam}$ 0.2$\to$0.9). Untrained controls are variants trained with that input held constant, whose response is arbitrary.}
\label{tab:probe}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
Head & ArcFace & EfficientNet & VGG-Face & LPIPS & SSIM \\
\midrule
Original pair & """ + " & ".join(f"{dh[k]:+.3f}" for k in ("arc", "eff", "vgg", "lpips", "ssim")) + r""" \\
Generated pairs & """ + " & ".join(f"{sh[k]:+.3f}" for k in ("arc", "eff", "vgg", "lpips", "ssim")) + r""" \\
\bottomrule
\end{tabular}

\vspace{4pt}
\begin{tabular}{@{}lcc@{}}
\toprule
Input & Swing (full model) & Untrained control \\
\midrule
Original-pair branch logit & """ + f"{F.swing_Wd:.1f}" + r""" & -- \\
Generated-pair branch logit & """ + f"{F.swing_Ws:.1f}" + r""" & """ + f"{DO.swing_Ws:.1f}" + r""" (direct-only) \\
Synthesis reliability $R_\mathrm{sam}$ & """ + f"{F.swing_R_sam_0p2_0p9:.2f}" + r""" & """ + f"{NC.swing_R_sam_0p2_0p9:.2f}" + r""" (no context) \\
Age gap & """ + f"{F.swing_g_5y_25y:.2f}" + r""" & """ + f"{NC.swing_g_5y_25y:.2f}" + r""" (no context) \\
Image quality & """ + f"{F.swing_Q_0p3_0p9:.2f}" + r""" & """ + f"{NC.swing_Q_0p3_0p9:.2f}" + r""" (no context) \\
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T5 label integrity
L = pd.read_csv(R / "drive_analyses/out/da4_label_linkage.csv").set_index("bin")
S = pd.read_csv(R / "drive_analyses/out/da4b_sex_mismatch.csv").set_index("gap_bin")
T = pd.read_csv(R / "log_analyses/out/la4_impostor_like_genuine.csv").set_index("bin")
rows = []
for b in ("G1", "G2", "G3", "G4", "G5", "G6"):
    rows.append(f"{YEARS[b]} & {int(L.loc[b, 'n_genuine']):,} & {pct(S.loc[b, 'sex_mismatch'], 1)} & {pct(L.loc[b, 'file_ids_differ'], 1)} & "
                f"{pct(L.loc[b, 'arcface_impostor_like'], 1)} & {pct(L.loc[b, 'impostor_like_if_ids_differ'], 1)} / {pct(L.loc[b, 'impostor_like_if_ids_same'], 1)} & "
                f"{int(T.loc[b, 'n_genuine'])} & {pct(T.loc[b, 'aafv_impostor_like'], 1)} / {pct(T.loc[b, 'vit_impostor_like'], 1)} \\\\")
write("tab_labels.tex", r"""\begin{table*}[t]
\centering
\caption{Integrity of MORPH ``same-person'' pairs as processed by the pipeline. Sex mismatch: the sex letters encoded in the two file names differ. Impostor-like: the pair scores below the 99th percentile of random impostors in the same gap bin. Calibration columns use the direct ArcFace score; test columns are a post-hoc reading of logged outputs of the fused system (Look~1) and of an independently trained Siamese ViT.}
\label{tab:labels}
\footnotesize
\begin{tabular}{@{}lccccccc@{}}
\toprule
 & \multicolumn{5}{c}{Calibration split} & \multicolumn{2}{c}{Test split (post hoc)} \\
\cmidrule(lr){2-6}\cmidrule(l){7-8}
Gap (y) & $n$ & Sex mismatch (\%) & File ids differ (\%) & Impostor-like (\%) & Impostor-like: ids differ / same (\%) & $n$ & Impostor-like: fused / ViT (\%) \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
""")

# ---------------------------------------------------------------- T6 SAM identity drift
D5 = pd.read_csv(R / "drive_analyses/out/da5_sam_identity_by_shift.csv")
rows = [f"{r.direction} & {r.abs_shift_bin.replace('-', '--')} & {int(r.n):,} & {r.id_cos_median:.3f} & {r.id_cos_p10:.3f} & {pct(r.share_below_0p3, 1)} & {r.age_err_median:.1f} \\\\"
        for r in D5.itertuples()]
write("tab_sam.tex", r"""\begin{table}[t]
\centering
\caption{Identity similarity of SAM-generated faces to their source image (ArcFace cosine) and age accuracy, by direction and size of the age shift. ArcFace is the recognizer used inside AAFV-Net and received resized FFHQ crops, so these values are descriptive, not an independent identity test.}
\label{tab:sam}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}lcrcccc@{}}
\toprule
Direction & $|$shift$|$ (y) & $n$ & Median cos & 10th pct & $<0.30$ (\%) & Age error (y) \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T7 statistical statements
stat = [("Calibration certificate", "1{,}170", "0.05", 1170, 0.05), ("Calibration certificate, union over 3 values of $\\rho$", "1{,}170", "$0.05/3$", 1170, 0.05 / 3),
        ("Held-out audit, one look", "1{,}149", "0.05", 1149, 0.05), ("Held-out audit, Bonferroni over 2 looks", "1{,}149", "0.025", 1149, 0.025)]
rows = [f"{a} & {b} & {c_} & {100 * (1 - d ** (1 / n)):.3f} \\\\" for a, b, c_, n, d in stat]
write("tab_statistics.tex", r"""\begin{table}[t]
\centering
\caption{The zero-failure upper bounds $\varepsilon = 1-\delta^{1/n}$ on random-impostor FAR that appeared in earlier versions, recomputed. All are arithmetically correct; they describe two different statements (a calibration-side certificate and a held-out audit), and every method in Table~\ref{tab:decision} attains the same values.}
\label{tab:stats}
\footnotesize
\begin{tabular}{@{}lccc@{}}
\toprule
Statement & $n$ & $\delta$ & $\varepsilon$ (\%) \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- figures (aggregate plots only; no face images)
for src, dst in [("log_analyses/out/la1_gap_ranking.png", "fig_gap_ranking.png"),
                 ("drive_analyses/out/da3_matched_fmr.png", "fig_matched_fmr.png"),
                 ("drive_analyses/out/da5_sam_identity_age.png", "fig_sam_drift.png")]:
    shutil.copy(R / src, FIG / dst)
    print("copied", dst)
