"""Additional AAFV-06 tables (run after build_assets.py). All values are read from logged AAFV artifacts; none are typed.
T8  original MORPH test results (Look 2)           <- Code/AAFV_Net/ablations/extended_test.csv
T9  FG-NET adults by gap                           <- Code/AAFV_Net/ablations/extended_calibration_fg16.csv
T10 decision-level ablations (calibration subset)  <- Code/AAFV_Net/ablations/decision_table_calibration.csv
T11 protocol chronology                            <- Code/AAFV_Net/q/logs/test_access.log (+ run log facts in DRIVE_FINDINGS.md)
T12 planned ablation ladder of the proposed model  (a plan: no results)
Usage: python scripts/build_tables_06.py   (from publication_AAFV-06/)"""
from pathlib import Path

import pandas as pd

PUB = Path(__file__).resolve().parent.parent
A = PUB.parent / "Code" / "AAFV_Net"
TAB = PUB / "tables"


def pct(x, d=2):
    return f"{100 * x:.{d}f}"


def write(name, body):
    body = body.replace(r"\begin{tabular}", r"\fittab{\begin{tabular}").replace(r"\end{tabular}", r"\end{tabular}}")
    (TAB / name).write_text(body, encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- T8
e = pd.read_csv(A / "ablations/extended_test.csv")
e = e[e.beta.round(3) == 0.01].set_index("variant")
names = [("full", "AAFV-Net (full)"), ("agg_no_shared_targets", "AAFV-Net, no shared targets"), ("arcface_only", "ArcFace, guarded"),
         ("arcface_only_noguard", "ArcFace, no guards"), ("direct5_logreg", "Direct 5-score LogReg"), ("direct_only_mlp", "Direct-only MLP"),
         ("baseline_siamese_cnn", "Siamese ResNet-18"), ("baseline_siamese_vit", "Siamese ViT-B/16")]
rows = []
for k, lab in names:
    x = e.loc[k]
    nb = "--" if pd.isna(x.D_by_both_rej) else pct(x.D_by_both_rej)
    rows.append(f"{lab} & {pct(x.same_acc)} & {pct(x.same_rev)} & {pct(x.same_rej)} & {int(x.D_random_FA)} & "
                f"{int(x.D_all_random_FA)} & {int(x.D_hard_FA)} & {pct(x.D_hard_rej)} & {nb} \\\\")
f0 = e.loc["full"]
n_gen = int(sum(f0[f"n_same_G{i}"] for i in range(1, 7)))
write("tab_test_results.tex", r"""\begin{table*}[t]
\centering
\caption{AAFV-Net and comparators on the person-disjoint MORPH test split as logged at the second test look ($\beta=1\%$). Genuine pairs: """
      + f"{n_gen:,}" + r"""; person-disjoint random impostors $\mathcal{D}_\mathrm{random}$: """ + f"{int(f0.D_random_n):,}"
      + r"""; random impostors with repeated persons $\mathcal{D}_\mathrm{all\,random}$: """ + f"{int(f0.D_all_random_n):,}"
      + r"""; ArcFace-mined look-alikes $\mathcal{D}_\mathrm{hard}$: """ + f"{int(f0.D_hard_n):,}" + r"""; model-neutral hard set: """
      + f"{int(f0.D_by_both_n):,}" + r""" (not scored for the two Siamese models, which mined it). These are the reported outcomes; Section~\ref{sec:reanalysis} examines what produces them.}
\label{tab:test}
\footnotesize
\begin{tabular}{@{}lcccccccc@{}}
\toprule
 & \multicolumn{3}{c}{Genuine pairs (\%)} & \multicolumn{3}{c}{False accepts (count)} & \multicolumn{2}{c}{Auto-reject (\%)} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(l){8-9}
Method & Accept & Review & Reject & $\mathcal{D}_\mathrm{random}$ & $\mathcal{D}_\mathrm{all\,random}$ & $\mathcal{D}_\mathrm{hard}$ & $\mathcal{D}_\mathrm{hard}$ & Neutral \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
""")

# ---------------------------------------------------------------- T9
fg = pd.read_csv(A / "ablations/extended_calibration_fg16.csv")
fg = fg[(fg.split == "fgnet") & (fg.beta.round(3) == 0.01)].set_index("variant")
rows = []
for k, lab in (("full", "AAFV-Net"), ("arcface_only", "ArcFace, guarded")):
    x = fg.loc[k]
    rows.append(f"{lab} & {pct(x.same_acc)} & {pct(x.same_rej)} & {int(x.FG_random_FA)}/{int(x.FG_random_n):,} & "
                + " & ".join(pct(x[f"same_acc_G{i}"], 1) for i in range(1, 7)) + r" \\")
ncount = " / ".join(str(int(fg.loc["full"][f"n_same_G{i}"])) for i in range(1, 7))
write("tab_fgnet.tex", r"""\begin{table*}[t]
\centering
\caption{External evaluation on FG-NET adults (both ages $\geq 16$; cut-off chosen after child false accepts had been observed) with MORPH-frozen models and thresholds. Genuine pairs per gap bin: """ + ncount
      + r""". Impostor pairs re-use images of at most 82 persons and are not independent trials. No per-pair scores were logged, so the two methods cannot be compared at a matched false-match rate.}
\label{tab:fgnet}
\footnotesize
\begin{tabular}{@{}lccccccccc@{}}
\toprule
 & & & & \multicolumn{6}{c}{Genuine auto-accept by gap (\%)} \\
\cmidrule(l){5-10}
Method & Accept (\%) & False reject (\%) & FA & 0--4 & 5--9 & 10--14 & 15--19 & 20--29 & 30+ \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
""")

# ---------------------------------------------------------------- T10
dt = pd.read_csv(A / "ablations/decision_table_calibration.csv")
dt = dt[dt.beta.round(3) == 0.01].set_index("variant")
groups = [("Full system", [("full", "full")]),
          ("Similarity measures", [("drop_arc", "drop ArcFace"), ("drop_eff", "drop EfficientNet"), ("drop_vgg", "drop VGG-Face"),
                                   ("drop_lpips", "drop LPIPS"), ("drop_ssim", "drop SSIM"), ("arc_only_scores", "ArcFace score only")]),
          ("Generated evidence", [("direct_only_mlp", "direct only (no SAM)"), ("sam_only_mlp", "SAM only"), ("agg_no_shared_targets", "no shared targets"),
                                  ("agg_fwd_only", "forward target only"), ("agg_shared_only", "shared targets only"),
                                  ("no_reliability", "no $R_\\mathrm{sam}$"), ("no_branch_masking", "no branch masking")]),
          ("Fusion and guards", [("fusion_logreg_no_mlp", "logistic fusion (no MLP)"), ("no_context", "no context ($g$, $Q$, $R_\\mathrm{sam}$)"),
                                 ("no_pair_weights", "no pair weights"), ("guard_none", "no probability guards")])]
rows = []
for gname, vs in groups:
    rows.append(r"\multicolumn{5}{@{}l}{\emph{" + gname + r"}} \\")
    for v, lab in vs:
        x = dt.loc[v]
        t = "$>1$" if x.T_accept >= 1 else f"{x.T_accept:.3f}"
        rows.append(f"\\quad {lab} & {t} & {pct(x.same_acc)} & {pct(x.D_hard_rej)} & {pct(x.D_random_rej)} \\\\")
write("tab_ablations.tex", r"""\begin{table}[t]
\centering
\caption{Decision-level ablations of AAFV-Net on the calibration common subset (1,500 genuine, 1,170 random and 1,500 mined impostor pairs; $\beta=1\%$), as logged. A threshold above 1 admits nobody; such variants differ in ranking far less than their acceptance suggests (Table~\ref{tab:decision}, Fig.~\ref{fig:gap}).}
\label{tab:ablations}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}lcccc@{}}
\toprule
Variant & $T_\mathrm{acc}$ & Accept (\%) & $\mathcal{D}_\mathrm{hard}$ rej. (\%) & $\mathcal{D}_\mathrm{random}$ rej. (\%) \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T11
log = (A / "q/logs/test_access.log").read_text().splitlines()
t1 = [l for l in log if "look=1" in l][0].split()[0].replace("T", " ").replace("Z", "")
t2 = [l for l in log if "look=2" in l][0].split()[0].replace("T", " ").replace("Z", "")
write("tab_chronology.tex", r"""\begin{table}[t]
\centering
\caption{Protocol chronology reconstructed from logged artifacts and run logs. Steps without a logged time stamp are marked ``not logged''.}
\label{tab:chronology}
\footnotesize
\begin{tabular}{@{}p{0.25\linewidth}p{0.68\linewidth}@{}}
\toprule
Time (UTC) & Event \\
\midrule
not logged & Person-level split; automatic quarantine of 854 persons; pair construction; fusion training (5 networks). \\
not logged & Draft calibration: at $\rho=0.20$, $T_\mathrm{acc}=1.0129$ (no acceptance); draft chose $\rho=0.50$, $T_\mathrm{acc}=0.7976$. Contact sheets of the top-scoring impostors reviewed; 4 further persons quarantined; calibration frozen at $\rho=0.20$, $T_\mathrm{acc}=0.956575$. \\
""" + t1 + r""" & Test look 1 (main system; thresholds hash recorded in the log). \\
not logged & All 26 variants re-trained as 3-network ensembles; reject rule changed to the $\beta$-quantile; baselines trained; neutral hard sets defined. \\
""" + t2 + r""" & Test look 2 (8 variants $\times$ 3 values of $\beta$; no hash recorded in the log). \\
after look 2 & FG-NET scored with frozen thresholds; adult cut-off chosen after the child false accepts were seen. \\
\bottomrule
\end{tabular}
\end{table}
""")

# ---------------------------------------------------------------- T12 (plan, no results)
plan = [("1", "Recognizer cosine", "--", "reference"),
        ("2", "+ gap/quality-conditioned calibration", "context", "small gain"),
        ("3", "+ transport head, real pairs only", "transport", "gain where real long gaps exist"),
        ("4", "+ synthetic targets, unweighted", "synthetic data", "mixed effect"),
        ("5", "+ synthetic, fixed hand-made weights", "hand-made reliability", "between rows 4 and 6"),
        ("6", "+ synthetic, learned reliability", "learned reliability", "best long-gap TAR"),
        ("7", "row 6 without $\\kappa$", "uncertainty", "worse risk--coverage"),
        ("8", "generator or backbone swap", "dependence", "same ordering of rows")]
write("tab_plan.tex", r"""\begin{table}[t]
\centering
\caption{Planned ablation ladder for the proposed age-transport model (Fig.~\ref{fig:proposed}). Each row changes one component. \emph{No row has been run}; the last column states the outcome that would support the design, not a result.}
\label{tab:plan}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}clll@{}}
\toprule
\# & Variant & Isolates & Supports the design if \\
\midrule
""" + "\n".join(f"{a} & {b} & {c} & {d} \\\\" for a, b, c, d in plan) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
