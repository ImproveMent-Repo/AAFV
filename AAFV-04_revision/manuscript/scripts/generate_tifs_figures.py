"""Generate IEEE TIFS publication figures directly from frozen AAFV-Net CSVs.

Preserves original publication/figures/ untouched and writes clean vector PDFs + 300 DPI PNGs
into publication_tifs/figures/.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = Path(__file__).resolve().parent.parent.parent
ABL = ROOT / "Code" / "AAFV_Net" / "ablations"
OUT = ROOT / "publication_tifs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.2,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.9,
})

BLUE = "#0b57d0"
TEAL = "#137333"
AMBER = "#b06000"
RED = "#c5221f"
GRAY = "#5f6368"
PURPLE = "#6a1b9a"
ORANGE = "#d95f02"


def save_fig(fig, stem):
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(OUT / f"{stem}.png", bbox_inches="tight", dpi=300)
    plt.close(fig)


def make_fig1_concept():
    x = np.linspace(0, 1, 600)
    imp = np.exp(-0.5 * ((x - 0.30) / 0.11) ** 2)
    gen = np.exp(-0.5 * ((x - 0.70) / 0.13) ** 2)

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.5), sharey=True)

    # Panel (a) Conventional binary threshold
    ax = axes[0]
    t_bin = 0.52
    ax.plot(x, imp, color=RED, lw=2.0, label=r"Different-Person ($\mathcal{D}_{\mathrm{diff}}$)")
    ax.plot(x, gen, color=TEAL, lw=2.0, label=r"Same-Person ($\mathcal{D}_{\mathrm{same}}$)")
    ax.axvline(t_bin, color="#202124", ls="--", lw=1.8, label=r"Single Threshold $T$")
    ax.fill_between(x[x >= t_bin], 0, imp[x >= t_bin], color=RED, alpha=0.25, label="Unbounded FAR Tail")
    ax.fill_between(x[x < t_bin], 0, gen[x < t_bin], color=AMBER, alpha=0.22, label="False-Reject Tail")
    ax.set_title("(a) Conventional Binary Threshold Matcher")
    ax.set_xlabel("Normalized Similarity Score")
    ax.set_ylabel("Schematic Density")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.24)
    ax.grid(True, ls=":", alpha=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=True)

    # Panel (b) Guarded 3-way rule
    ax = axes[1]
    t_rej, t_acc = 0.22, 0.86
    ax.axvspan(0, t_rej, color=RED, alpha=0.10)
    ax.axvspan(t_rej, t_acc, color=AMBER, alpha=0.10)
    ax.axvspan(t_acc, 1.0, color=TEAL, alpha=0.12)
    ax.plot(x, imp, color=RED, lw=2.0, label="Calibrated Impostor Pool")
    ax.plot(x, gen, color=TEAL, lw=2.0, label="Genuine Cross-Age Pool")
    ax.axvline(t_rej, color=RED, ls="-.", lw=1.9, label=r"Auto-Reject $T_{\mathrm{rej}}(\beta)$")
    ax.axvline(t_acc, color=TEAL, ls="-", lw=2.1, label=r"Auto-Accept $T_{\mathrm{acc}}$ (+ Guards)")

    ax.text(0.11, 1.08, "Auto-Reject\nZone", ha="center", va="top", color=RED, fontweight="bold", fontsize=8.5)
    ax.text(0.54, 1.08, "Manual Review Zone\n(Absorbs Ambiguity)", ha="center", va="top", color=AMBER, fontweight="bold", fontsize=8.5)
    ax.text(0.93, 1.08, "Auto-\nAccept", ha="center", va="top", color=TEAL, fontweight="bold", fontsize=8.5)

    ax.set_title("(b) Proposed Guarded Three-Way Decision Rule")
    ax.set_xlabel(r"Calibrated Posterior $P(y=1 \mid \mathbf{z})$ under Guards")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.24)
    ax.grid(True, ls=":", alpha=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=True)

    fig.tight_layout()
    save_fig(fig, "fig1_concept")


def make_fig2_architecture():
    fig, ax = plt.subplots(figsize=(13.2, 6.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")

    def hdr(x, w, title):
        box = patches.FancyBboxPatch((x, 45.2), w, 3.6, boxstyle="round,pad=0.35,rounding_size=0.6",
                                     fc="#e8eef7", ec="#7a8ea8", lw=1.0)
        ax.add_patch(box)
        ax.text(x + w / 2, 47.0, title, ha="center", va="center", fontweight="bold", fontsize=8.8, color="#1f2937")
        col = patches.FancyBboxPatch((x, 1.5), w, 42.9, boxstyle="round,pad=0.25,rounding_size=0.6",
                                     fc="none", ec="#cbd5e1", lw=0.8)
        ax.add_patch(col)

    def node(x, y, w, h, title, body, fc="#ffffff", ec="#374151", tc="#111827", title_y_off=2.1):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=0.6",
                                     fc=fc, ec=ec, lw=1.2)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - title_y_off, title, ha="center", va="center", fontweight="bold", fontsize=8.6, color=tc)
        ax.plot([x + 0.8, x + w - 0.8], [y + h - 3.6, y + h - 3.6], color=ec, lw=0.6, alpha=0.6)
        ax.text(x + w / 2, y + (h - 3.8) / 2, body, ha="center", va="center", fontsize=7.6, color="#1f2937", linespacing=1.32)

    def arr(x1, y1, x2, y2, color="#374151", label="", lx=None, ly=None):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.32,head_length=0.5", color=color, lw=1.3))
        if label:
            px = (x1 + x2) / 2 if lx is None else lx
            py = (y1 + y2) / 2 if ly is None else ly
            ax.text(px, py, label, ha="center", va="center", fontsize=7.3,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.7), color=color)

    hdr(1.0, 16.5, "STAGE 1: INPUT & QUALITY")
    hdr(19.0, 22.5, "STAGE 2: EVIDENCE EXTRACTION")
    hdr(43.0, 17.5, "STAGE 3: BRANCH HEADS")
    hdr(62.0, 18.0, "STAGE 4: FUSION & CALIB.")
    hdr(81.5, 17.5, "STAGE 5: 3-WAY DECISION")

    node(1.8, 24.5, 14.9, 18.5, "Aligned Photo Pair",
         "Faces: $I_1, I_2$ ($256\\times256$ FFHQ)\nAges: $a_1 \\leq a_2$, span $\\Delta a$\nNormalized context:\n$g = \\min(1, \\Delta a / 80)$",
         fc="#eef6fc", ec=BLUE, tc=BLUE)
    node(1.8, 4.0, 14.9, 17.5, "5-Measure Quality Q",
         "Train [5,95]-pct norm of:\nsharp, illum, contrast,\nnoise(inv), detail (box px)\n$Q = 0.5(Q(I_1)+Q(I_2))$\nGuard: $Q \\geq Q_{\\min}=0.2948$",
         fc="#fef7e0", ec=AMBER, tc=AMBER)

    node(19.9, 25.5, 20.7, 17.5, "Direct Similarity Branch",
         "Raw pair $(I_1, I_2)$ z-scored 5-D:\nArcFace (512-D), EffNet-B0,\nVGG-Face, LPIPS, SSIM\nFixed across all age gaps",
         fc="#ffffff", ec="#374151")
    node(19.9, 4.0, 20.7, 19.2, "SAM Counterfactual Branch",
         "5-yr grid targets: fwd, bwd,\n+ $K\\leq7$ interior shared targets\nMean-pooled z-scored $\\mathbf{s}_{\\mathrm{sam}}$\n$R_{\\mathrm{sam}} = 0.7\\sqrt{r_1 r_2} + 0.3 R_c$\nGuard: $R_{\\mathrm{sam}} \\geq 0.3944$",
         fc="#ffffff", ec="#374151")

    node(43.8, 25.5, 15.9, 17.5, "Direct Linear & Guard",
         "Linear projection (6 params):\n$W_d = \\mathbf{w}_d^T \\mathbf{s}_{\\mathrm{dir}} + b_d$\nPlatt auxiliary prob:\n$P_d = \\sigma(A_d W_d + B_d)$\nGuard: $P_d \\geq \\rho = 0.20$",
         fc="#ffffff", ec="#374151")
    node(43.8, 4.0, 15.9, 19.2, "SAM Linear & Masking",
         "Linear projection (6 params):\n$W_s = \\mathbf{w}_s^T \\mathbf{s}_{\\mathrm{sam}} + b_s$\nTrain SAM mask $p_{\\mathrm{mask}}=0.12$\nPlatt auxiliary prob:\n$P_s = \\sigma(A_s W_s + B_s) \\geq 0.20$",
         fc="#ffffff", ec="#374151")

    node(62.8, 25.5, 16.4, 17.5, "11-D Fusion Input z",
         "Stage A exact vector order:\n$[W_d, W_s, W_f, g, Q, I_{\\mathrm{enh}},$\n$R_{\\mathrm{sam}}, R_{\\mathrm{diff}}, I_{\\mathrm{sam}}, I_{\\mathrm{diff}}, I_{\\mathrm{multi}}]^T$\n(Diff & enh channels inactive = 0)",
         fc="#eefbf1", ec=TEAL, tc=TEAL)
    node(62.8, 4.0, 16.4, 19.2, "MLP Ensemble & Platt",
         "MLP: $11 \\rightarrow 32 \\rightarrow 16 \\rightarrow 1$\nReLU, Dropout 0.10 (947 params\nincl. 3 heads; 5 seeds, AdamW)\nPlatt: $P = \\sigma(A_{\\mathrm{cal}}\\bar{\\ell}+B_{\\mathrm{cal}})$",
         fc="#eefbf1", ec=TEAL, tc=TEAL)

    node(82.3, 30.8, 15.9, 12.2, "AUTO-ACCEPT",
         "$P \\geq T_{\\mathrm{acc}}=0.9564$ & Guards\nTest $\\mathcal{D}_{\\mathrm{random}}$: 0/1,149 FA\nBonf. Bound: $\\leq 0.320\\%$\nSame Accept: 70.07%",
         fc="#e6f4ea", ec=TEAL, tc=TEAL)
    node(82.3, 17.2, 15.9, 12.2, "MANUAL REVIEW",
         "$T_{\\mathrm{rej}} \\leq P < T_{\\mathrm{acc}}$ or Guard Fail\nAbsorbs ambiguous pairs\nSame Review: 29.39%\n(7,143 / 24,305 MORPH test)",
         fc="#fef7e0", ec=AMBER, tc=AMBER)
    node(82.3, 3.6, 15.9, 12.2, "AUTO-REJECT",
         "$P < T_{\\mathrm{rej}}(0.01)=0.0075$\nRejects 98.04% $\\mathcal{D}_{\\mathrm{hard}}$\nRejects 57.49% $\\mathcal{D}_{\\mathrm{neutral}}$\nSame False Reject: 0.54%",
         fc="#fce8e6", ec=RED, tc=RED)

    # Orthogonal routing paths
    arr(9.2, 24.5, 9.2, 21.6, color=AMBER)
    arr(16.7, 34.0, 19.9, 34.0, color=BLUE)
    arr(16.7, 29.5, 18.2, 29.5, color=BLUE)
    ax.plot([18.2, 18.2], [29.5, 13.5], color=BLUE, lw=1.3)
    arr(18.2, 13.5, 19.9, 13.5, color=BLUE)

    # Top context bypass g -> Stage 4
    ax.plot([9.2, 9.2], [43.0, 44.3], color=BLUE, lw=1.2)
    ax.plot([9.2, 71.0], [44.3, 44.3], color=BLUE, lw=1.2)
    arr(71.0, 44.3, 71.0, 43.0, color=BLUE, label="Context g", lx=40.0, ly=44.3)

    # Bottom context bypass Q -> Stage 4 & 5
    ax.plot([9.2, 9.2], [4.0, 2.5], color=AMBER, lw=1.2)
    ax.plot([9.2, 61.2], [2.5, 2.5], color=AMBER, lw=1.2)
    ax.plot([61.2, 61.2], [2.5, 31.0], color=AMBER, lw=1.2)
    arr(61.2, 31.0, 62.8, 31.0, color=AMBER, label="Quality Q Guard", lx=35.0, ly=2.5)

    arr(40.6, 34.0, 43.8, 34.0, label=r"$\mathbf{s}_{\mathrm{dir}}$", lx=42.2, ly=35.8)
    arr(40.6, 13.5, 43.8, 13.5, label=r"$\mathbf{s}_{\mathrm{sam}}$", lx=42.2, ly=15.3)
    arr(59.7, 34.0, 62.8, 34.0, label=r"$W_d,P_d$")
    arr(59.7, 13.5, 61.8, 13.5, color="#374151")
    ax.plot([61.8, 61.8], [13.5, 29.0], color="#374151", lw=1.2)
    arr(61.8, 29.0, 62.8, 29.0, label=r"$W_s,R_{\mathrm{sam}}$", lx=60.5, ly=21.2)
    arr(71.0, 25.5, 71.0, 23.2, color=TEAL, label=r"$\mathbf{z}\in\mathbb{R}^{11}$", lx=71.0, ly=24.35)

    ax.plot([79.2, 80.7], [13.5, 13.5], color=TEAL, lw=1.3)
    ax.plot([80.7, 80.7], [9.7, 36.9], color="#374151", lw=1.2)
    arr(80.7, 36.9, 82.3, 36.9, color=TEAL)
    arr(80.7, 23.3, 82.3, 23.3, color=AMBER)
    arr(80.7, 9.7, 82.3, 9.7, color=RED)

    save_fig(fig, "fig2_architecture")


def make_fig3_results():
    et = pd.read_csv(ABL / "extended_test.csv")
    d = et[et.beta == 0.01].set_index("variant")

    fg16 = pd.read_csv(ABL / "extended_calibration_fg16.csv")
    fg16 = fg16[(fg16.beta == 0.01) & (fg16.split == "fgnet")].set_index("variant")

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.9))

    # Panel (a) MORPH test trade-off
    ax = axes[0]
    specs = [
        ("full", "AAFV-Net (Full)", "o", BLUE, 95, (-72, -14)),
        ("agg_no_shared_targets", "No Shared Targets", "s", "#2b8cbe", 85, (-72, 6)),
        ("arcface_only", "ArcFace Only", "^", GRAY, 90, (8, -4)),
        ("direct5_logreg", "Direct 5-Score LR", "v", "#374151", 80, (8, -8)),
        ("direct_only_mlp", "Direct-Only MLP", "D", PURPLE, 75, (-76, 8)),
        ("baseline_siamese_cnn", "Siamese CNN", "P", ORANGE, 85, (8, 5)),
        ("baseline_siamese_vit", "Siamese ViT", "X", RED, 85, (8, -10)),
    ]
    for k, lbl, mk, col, sz, off in specs:
        xr = 100.0 * d.loc[k, "D_hard_rej"]
        ya = 100.0 * d.loc[k, "same_acc"]
        ax.scatter(xr, ya, marker=mk, color=col, s=sz, zorder=4, edgecolors="white", lw=0.6, label=lbl)
        ax.annotate(lbl, (xr, ya), xytext=off, textcoords="offset points", fontsize=7.5, color=col, fontweight="bold" if k == "full" else "normal")

    ax.set_title("(a) MORPH Test Accept vs. Hard Rejection")
    ax.set_xlabel(r"ArcFace-Mined Hard Impostor Rejection ($\mathcal{D}_{\mathrm{hard}}$, %)")
    ax.set_ylabel("Same-Person Auto-Accept Rate (%)")
    ax.set_xlim(-6, 108)
    ax.set_ylim(-8, 102)
    ax.grid(True, ls=":", alpha=0.55)

    # Panel (b) FG-NET Adults 6 bins
    ax = axes[1]
    bins = ["G1", "G2", "G3", "G4", "G5", "G6"]
    lbls = ["<5y", "5-9y", "10-14y", "15-19y", "20-29y", "30+y"]
    x = np.arange(len(bins))
    w = 0.36
    ours = [100.0 * fg16.loc["full", f"same_acc_{b}"] for b in bins]
    arc = [100.0 * fg16.loc["arcface_only", f"same_acc_{b}"] for b in bins]
    ax.bar(x - w / 2, ours, w, color=BLUE, label="AAFV-Net (Full)")
    ax.bar(x + w / 2, arc, w, color="#9aa0a6", label="ArcFace Only")
    ax.set_xticks(x)
    ax.set_xticklabels(lbls)
    ax.set_ylim(0, 84)
    ax.set_title(r"(b) External FG-NET Adults ($a_1, a_2 \geq 16$)")
    ax.set_xlabel("Age-Gap Bin")
    ax.set_ylabel("Auto-Accept Rate (%)")
    ax.grid(True, axis="y", ls=":", alpha=0.55)
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    save_fig(fig, "fig3_results")


def make_fig4_ablations():
    dt = pd.read_csv(ABL / "decision_table_calibration.csv")
    d = dt[dt.beta == 0.01].set_index("variant")

    order = [
        ("full", "Full AAFV-Net"),
        ("drop_arc", "Drop ArcFace"),
        ("drop_lpips", "Drop LPIPS"),
        ("drop_eff", "Drop EfficientNet"),
        ("drop_vgg", "Drop VGG-Face"),
        ("drop_ssim", "Drop SSIM"),
        ("no_branch_masking", r"No Masking ($p=0$)"),
        ("no_context", "No Context Inputs"),
        ("agg_no_shared_targets", "No Shared Targets"),
        ("direct_only_mlp", "Direct-Only MLP"),
        ("sam_only_mlp", "SAM-Only MLP"),
        ("guard_none", "No Guards"),
    ][::-1]

    y = np.arange(len(order))
    acc = [100.0 * d.loc[k, "same_acc"] for k, _ in order]
    rej = [100.0 * d.loc[k, "D_hard_rej"] for k, _ in order]

    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    h = 0.36
    ax.barh(y + h / 2, acc, h, color=TEAL, label="Same-Person Auto-Accept (%)")
    ax.barh(y - h / 2, rej, h, color=BLUE, label=r"Hard-Impostor Rejection ($\mathcal{D}_{\mathrm{hard}}$, %)")
    ax.set_yticks(y)
    ax.set_yticklabels([lbl for _, lbl in order])
    ax.set_xlim(0, 106)
    ax.set_xlabel(r"Rate (%) on Calibration Common Subset ($\beta = 0.01$)")
    ax.set_title("Component Ablation Trade-Offs (Calibration Common Subset)")
    ax.grid(True, axis="x", ls=":", alpha=0.55)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.07), ncol=2, frameon=True)

    fig.tight_layout()
    save_fig(fig, "fig4_ablations")


def make_fig5_gap_neutral():
    et = pd.read_csv(ABL / "extended_test.csv")
    d = et[et.beta == 0.01].set_index("variant")

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.7))

    # Panel (a): exact 6 gap bins G1..G6
    ax = axes[0]
    bins = ["G1", "G2", "G3", "G4", "G5", "G6"]
    xlabs = ["G1\n(0-4y)", "G2\n(5-9y)", "G3\n(10-14y)", "G4\n(15-19y)", "G5\n(20-29y)", "G6\n(30+y)"]
    x = np.arange(len(bins))
    w = 0.36
    ours = [100.0 * d.loc["full", f"same_acc_{b}"] for b in bins]
    arc = [100.0 * d.loc["arcface_only", f"same_acc_{b}"] for b in bins]
    ax.bar(x - w / 2, ours, w, color=BLUE, label="AAFV-Net (Full)")
    ax.bar(x + w / 2, arc, w, color="#9aa0a6", label="ArcFace Only")
    ax.set_xticks(x)
    ax.set_xticklabels(xlabs, fontsize=8.0)
    ax.set_ylim(0, 112)
    ax.set_title("(a) MORPH Test Accept by Age-Gap Bin")
    ax.set_ylabel("Same-Person Auto-Accept (%)")
    ax.grid(True, axis="y", ls=":", alpha=0.55)
    ax.legend(loc="upper center", frameon=True)

    # Panel (b): neutral hard impostors (D_by_both)
    ax = axes[1]
    vars_n = [
        ("direct5_logreg", "Direct 5-Score LR", "#4b5563"),
        ("arcface_only", "ArcFace Only", "#9aa0a6"),
        ("direct_only_mlp", "Direct-Only MLP", PURPLE),
        ("agg_no_shared_targets", "No Shared Targets", "#2b8cbe"),
        ("full", "AAFV-Net (Full)", BLUE),
    ]
    yn = np.arange(len(vars_n))
    vals = [100.0 * d.loc[k, "D_by_both_rej"] for k, _, _ in vars_n]
    bars = ax.barh(yn, vals, height=0.55, color=[c for _, _, c in vars_n])
    for b_, v_ in zip(bars, vals):
        ax.text(v_ + 1.2, b_.get_y() + b_.get_height() / 2, f"{v_:.2f}%", va="center", fontsize=8.0)
    ax.set_yticks(yn)
    ax.set_yticklabels([lbl for _, lbl, _ in vars_n])
    ax.set_xlim(0, 72)
    ax.set_title(r"(b) Neutral Hard Impostor Rejection ($\mathcal{D}_{\mathrm{neutral}}$)")
    ax.set_xlabel("Auto-Reject Rate (%)")
    ax.grid(True, axis="x", ls=":", alpha=0.55)

    fig.tight_layout()
    save_fig(fig, "fig5_gap_neutral")


def make_fig6_beta_sweep():
    et = pd.read_csv(ABL / "extended_test.csv")
    betas = [0.005, 0.010, 0.020]
    x = np.arange(len(betas))
    x_lbls = ["0.005 (0.5%)", "0.010 (1.0%)", "0.020 (2.0%)"]

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6))
    models = [
        ("full", "AAFV-Net (Full)", "o-", BLUE),
        ("direct_only_mlp", "Direct-Only MLP", "s--", PURPLE),
        ("arcface_only", "ArcFace Only", "^:", GRAY),
    ]

    for ax, col_name, title, ylabel in [
        (axes[0], "D_hard_rej", r"(a) ArcFace-Mined Hard Impostor Rejection ($\mathcal{D}_{\mathrm{hard}}$)", "Auto-Reject Rate (%)"),
        (axes[1], "D_by_both_rej", r"(b) Neutral Hard Impostor Rejection ($\mathcal{D}_{\mathrm{neutral}}$)", "Auto-Reject Rate (%)"),
    ]:
        for var, lbl, fmt, c in models:
            sub = et[et.variant == var].set_index("beta")
            ys = [100.0 * sub.loc[b, col_name] for b in betas]
            ax.plot(x, ys, fmt, color=c, lw=2.0, ms=6.5, label=lbl)
        ax.set_xticks(x)
        ax.set_xticklabels(x_lbls)
        ax.set_xlabel(r"Calibration False-Reject Budget $\beta$")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_ylim(-5, 108)
        ax.grid(True, ls=":", alpha=0.55)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, frameon=True)
    fig.tight_layout()
    save_fig(fig, "fig6_beta_sweep")


def make_fig7_decision_outcomes():
    dt = pd.read_csv(ABL / "decision_table_calibration.csv")
    d = dt[dt.beta == 0.01].set_index("variant")

    order = [
        ("full", "AAFV-Net"),
        ("arcface_only", "ArcFace"),
        ("direct_only_mlp", "Direct MLP"),
        ("baseline_siamese_cnn", "Siamese CNN"),
        ("baseline_siamese_vit", "Siamese ViT"),
        ("baseline_vlm", "VLM (Qwen2)"),
    ]
    x = np.arange(len(order))
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.7), sharey=True)

    # Panel (a) Same-person calibration common subset
    ax = axes[0]
    acc = np.array([100.0 * d.loc[k, "same_acc"] for k, _ in order])
    rev = np.array([100.0 * d.loc[k, "same_rev"] for k, _ in order])
    rej = np.array([100.0 * d.loc[k, "same_rej"] for k, _ in order])
    ax.bar(x, acc, color=TEAL, label="Auto-Accept")
    ax.bar(x, rev, bottom=acc, color="#e3b341", label="Manual Review")
    ax.bar(x, rej, bottom=acc + rev, color=RED, label="False Reject (~1%)")
    ax.set_xticks(x)
    ax.set_xticklabels([l for _, l in order], rotation=25, ha="right")
    ax.set_ylim(0, 104)
    ax.set_ylabel("Outcome Share (%)")
    ax.set_title("(a) Same-Person Pairs (Calib. Subset)")
    ax.grid(True, axis="y", ls=":", alpha=0.45)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.24), ncol=3, frameon=True, fontsize=7.8)

    # Panel (b) Hard different-person calibration common subset
    ax = axes[1]
    hrej = np.array([100.0 * d.loc[k, "D_hard_rej"] for k, _ in order])
    hrev = np.array([100.0 * d.loc[k, "D_hard_rev"] for k, _ in order])
    hfa = np.array([100.0 * d.loc[k, "D_hard_FA"] / 1500.0 for k, _ in order])
    ax.bar(x, hrej, color=TEAL, label="Auto-Reject")
    ax.bar(x, hrev, bottom=hrej, color="#e3b341", label="Manual Review")
    ax.bar(x, hfa, bottom=hrej + hrev, color=RED, label="False Accept (0%)")
    ax.set_xticks(x)
    ax.set_xticklabels([l for _, l in order], rotation=25, ha="right")
    ax.set_title(r"(b) Hard Impostors ($\mathcal{D}_{\mathrm{hard}}$ Calib. Subset)")
    ax.grid(True, axis="y", ls=":", alpha=0.45)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.24), ncol=3, frameon=True, fontsize=7.8)

    fig.tight_layout()
    save_fig(fig, "fig7_decision_outcomes")


if __name__ == "__main__":
    make_fig1_concept()
    make_fig2_architecture()
    make_fig3_results()
    make_fig4_ablations()
    make_fig5_gap_neutral()
    make_fig6_beta_sweep()
    make_fig7_decision_outcomes()
    print("Generated 7 TIFS figures cleanly in", OUT)
