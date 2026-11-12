"""Generate verified TIFS Supplementary Material LaTeX from frozen CSVs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
ABL = ROOT / "Code" / "AAFV_Net" / "ablations"
AUD = ROOT / "Code" / "AAFV_Net" / "audit"
OUT = ROOT / "publication_tifs" / "supplementary"
OUT.mkdir(parents=True, exist_ok=True)

abl_cal = pd.read_csv(ABL / "ablation_calibration.csv")
dec_cal = pd.read_csv(ABL / "decision_table_calibration.csv")
d1 = dec_cal[dec_cal.beta == 0.01].set_index("variant")
rel = pd.read_csv(AUD / "reliability_by_bin.csv")
tcol = "TPR@FPR1e-3_D_hard"

rows1 = []
for _, r in abl_cal.iterrows():
    v = str(r["variant"])
    vtex = v.replace("_", r"\_")
    g = str(r["group"]).replace("_", r"\_")
    ta = f"{r['T_accept']:.4f}"
    rho = f"{r['RHO']:.2f}"
    sa_all = f"{r['same_accept_all'] * 100:.2f}"
    auc_r = f"{r['AUC_D_random']:.4f}"
    auc_h = f"{r['AUC_D_hard']:.4f}"
    tpr_h = f"{r[tcol]:.4f}"
    sub_acc = f"{d1.loc[v, 'same_acc'] * 100:.2f}" if v in d1.index else "--"
    sub_hr = f"{d1.loc[v, 'D_hard_rej'] * 100:.2f}" if v in d1.index else "--"
    rows1.append(
        f"{vtex} & {g} & {ta} & {rho} & {sa_all} & {auc_r} & {auc_h} & {tpr_h} & {sub_acc} & {sub_hr} \\\\"
    )

rows2 = []
for _, r in rel.iterrows():
    mp = f"{r['mean_P']:.4f}" if pd.notna(r["mean_P"]) else "--"
    ob = f"{r['observed']:.4f}" if pd.notna(r["observed"]) else "--"
    ad = f"{r['abs_dev']:.4f}" if pd.notna(r["abs_dev"]) else "--"
    nt = str(r["note"]).replace("<", "$<$").replace("_", r"\_") if pd.notna(r["note"]) else "Calibrated"
    rows2.append(
        f"{r['bin']} & {int(r['n']):,} & {int(r['same']):,} & {mp} & {ob} & {ad} & {nt} \\\\"
    )

tex = r"""\documentclass[journal]{IEEEtran}
\usepackage{amsmath,amssymb,booktabs,array,makecell,url}
\usepackage[hidelinks]{hyperref}
\begin{document}
\title{Supplementary Material for ``AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk''}
\author{Anurag~Nayak,~\IEEEmembership{Graduate Student Member,~IEEE,} and [Co-Authors]}
\maketitle

\section*{S-I. Complete 26-Variant Calibration Ablation Audit}
Table~\ref{tab:s1_all} lists all 26 frozen ablation variants and comparator architectures audited on the MORPH \texttt{calibration} split ($338{,}871$ total pairs; $\mathcal{D}_{\text{hard}}$ $N=35{,}769$, except VLM $N=1{,}500$), paired with decision rates on the label-free calibration common subset ($\beta = 1.0\%$, \texttt{decision\_table\_calibration.csv}).

\begin{table*}[t]
\centering
\caption{Full 26-Variant Calibration Performance and Subset Decision Outcomes ($\beta = 1.0\%$). Zero false accepts occurred on calibration across every variant.}
\label{tab:s1_all}
\scriptsize
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{@{}llcccccccc@{}}
\toprule
\textbf{Variant ID} & \textbf{Group} & \textbf{$T_{\text{acc}}$} & \textbf{$\rho$} & \makecell{\textbf{Full Cal.}\\\textbf{Accept (\%)}} & \makecell{\textbf{AUC}\\\textbf{($\mathcal{D}_{\text{random}}$)}} & \makecell{\textbf{AUC}\\\textbf{($\mathcal{D}_{\text{hard}}$)}} & \makecell{\textbf{TPR@$10^{-3}$}\\\textbf{($\mathcal{D}_{\text{hard}}$)}} & \makecell{\textbf{Subset}\\\textbf{Accept (\%)}} & \makecell{\textbf{Subset Hard}\\\textbf{Reject (\%)}} \\
\midrule
""" + "\n".join(rows1) + r"""
\bottomrule
\end{tabular}
\end{table*}

\section*{S-II. Prior-Adjusted Calibration Reliability by Age-Gap Bin}
Table~\ref{tab:s2_rel} reproduces \texttt{audit/reliability\_by\_bin.csv}, verifying calibration alignment between mean predicted probability and observed genuine frequency on \texttt{train\_val} across age-gap bins G1--G4 (with G5--G6 omitted due to $<20$ genuine \texttt{train\_val} samples).

\begin{table}[h]
\centering
\caption{Calibration Probability Reliability Check Across Age-Gap Bins (\texttt{reliability\_by\_bin.csv}).}
\label{tab:s2_rel}
\scriptsize
\setlength{\tabcolsep}{3.0pt}
\begin{tabular}{@{}lcccccc@{}}
\toprule
\textbf{Bin} & \textbf{$N$} & \textbf{Same} & \textbf{Mean $P$} & \textbf{Observed} & \textbf{Abs.\ Dev.} & \textbf{Status} \\
\midrule
""" + "\n".join(rows2) + r"""
\bottomrule
\end{tabular}
\end{table}

\section*{S-III. IEEE TIFS Deep Learning Reproducibility Checklist \& Checksums}
{\sloppy
\begin{itemize}
    \item \textbf{Backbone Extractors (Frozen):} InsightFace \texttt{buffalo\_l} ArcFace (ResNet-100, $112\times 112$), EfficientNet-B0, VGG-Face, AlexNet LPIPS, analytical SSIM, StyleGAN2 SAM (\texttt{sam\_ffhq\_aging.pt}), and DEX age estimator.
    \item \textbf{Image Quality Normalization (\texttt{quality.py}):} Five raw features (\texttt{sharp}, \texttt{illum}, \texttt{contrast}, \texttt{noise} inverted, \texttt{detail}) min-max scaled via 5th/95th \texttt{train\_fit} percentiles; pair quality $Q = 0.5(Q_1 + Q_2)$; empirical 5th percentile $Q_{\min} = 0.294763$.
    \item \textbf{Fusion MLP (\texttt{fusion.py}, \texttt{p6\_train.py}):} 5-seed ensemble ($947$ weights/seed: $3\times 6$ linear heads $+ 929$ MLP $11\to 32\to 16\to 1$, ReLU, Dropout $0.10$), trained with AdamW ($\text{lr}=0.003$, $\text{wd}=0.01$, batch size $2{,}048$), inverse gap-bin frequency weights, SAM branch masking $p_{\text{mask}}=0.12$, early stopping patience $10$ ($\Delta < 10^{-5}$; stopped at epochs 30, 36, 45, 47, 27).
    \item \textbf{Baseline Protocols (\texttt{p11\_siamese.py}, \texttt{p11\_vlm.py}):} Siamese CNN (\texttt{resnet18}, $128\times 128$, 6 epochs, stopped epoch 4, best val log loss $0.1950$); Siamese ViT (\texttt{vit\_base\_patch16\_224.augreg\_in21k\_ft\_in1k}, $224\times 224$, $\text{lr}=2\times 10^{-5}$, 3 epochs, best val log loss $0.1285$); Qwen2-VL-2B (4-bit LoRA $r=16, \alpha=16$, $224\times 224$, 8,000 balanced pairs, 1 epoch, scored strictly on calibration common subset and FG-NET).
    \item \textbf{Cryptographic Sealing:} Look~1 \texttt{thresholds.json} LF SHA-256 \texttt{4b7af9772d209ce6315d36f36df6b191\allowbreak 728c830159f04355e7a2238fd9732cfe} (\texttt{test\_access.log} Look~1: \texttt{2026-11-05T21:42:09Z}); Look~2 \texttt{ablations/variants/full/frozen.pkl} SHA-256 \texttt{a47c916bc819379f9fa5a35b29fdc5ec\allowbreak f3a09f092fbe1cb2c4fbf3347f0035b9} (\texttt{test\_access.log} Look~2: \texttt{2026-11-07T19:45:00Z}).
\end{itemize}
}
\end{document}
"""

(OUT / "TIFS_Supplementary.tex").write_text(tex, encoding="utf-8")
print("Wrote", OUT / "TIFS_Supplementary.tex")
