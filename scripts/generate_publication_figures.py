"""
Generate publication-quality vector (PDF) and raster (PNG) figures for AAFV-Net IEEE submission.
Saves all figures directly into publication/figures/.
"""
import os, sys, tempfile
from pathlib import Path

# Ensure Matplotlib has a writable temp cache directory
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# IEEE style configuration
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Times"],
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.titlesize": 11,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "lines.linewidth": 1.5,
    "lines.markersize": 5,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})

OUT_DIR = Path("publication/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Colors
C_ACCEPT = "#2da44e"   # Green
C_REVIEW = "#d4a72c"   # Yellow/Amber
C_REJECT = "#cf222e"   # Red
C_PRIMARY = "#1f6feb"  # Blue
C_MUTED = "#8b949e"    # Gray

print("Generating publication figures in:", OUT_DIR)

# -----------------------------------------------------------------------------
# FIGURE 1: Conceptual Schematic (Single-threshold vs 3-way guarded decision)
# -----------------------------------------------------------------------------
def generate_fig1_concept():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.7))
    
    # Subplot 1: Traditional Binary Threshold
    x = np.linspace(0, 1, 500)
    # Impostor score distribution (shifted left)
    imp_dist = np.exp(-0.5 * ((x - 0.35) / 0.12) ** 2)
    # Genuine score distribution (shifted right, wide under age-gap)
    gen_dist = np.exp(-0.5 * ((x - 0.65) / 0.18) ** 2)
    
    ax1.plot(x, imp_dist, color=C_REJECT, label=r"Different-Person ($D_{\mathrm{diff}}$)")
    ax1.plot(x, gen_dist, color=C_ACCEPT, label=r"Same-Person ($D_{\mathrm{same}}$)")
    ax1.axvline(x=0.52, color="black", linestyle="--", linewidth=1.5, label=r"Single Threshold $T$")
    
    # Fill error regions
    ax1.fill_between(x[x >= 0.52], imp_dist[x >= 0.52], color=C_REJECT, alpha=0.3, label="Unbounded FAR")
    ax1.fill_between(x[x < 0.52], gen_dist[x < 0.52], color=C_REVIEW, alpha=0.3, label="FRR (False Reject)")
    
    ax1.set_title("(a) Conventional Binary Face Matcher", fontweight="bold")
    ax1.set_xlabel("Face Similarity Score")
    ax1.set_ylabel("Probability Density")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1.15)
    ax1.legend(loc="upper right", frameon=True, fontsize=7)
    ax1.grid(True)
    
    # Subplot 2: AAFV-Net Three-Way Guarded Decision
    ax2.plot(x, imp_dist, color=C_REJECT, label=r"Impostor Pool")
    ax2.plot(x, gen_dist, color=C_ACCEPT, label=r"Genuine (Cross-Age)")
    
    # Two thresholds
    T_rej = 0.22
    T_acc = 0.82
    
    ax2.axvline(x=T_rej, color=C_REJECT, linestyle="-.", linewidth=1.5, label=r"Auto-Reject $T_{\mathrm{rej}}(\beta)$")
    ax2.axvline(x=T_acc, color=C_ACCEPT, linestyle="-", linewidth=1.8, label=r"Auto-Accept $T_{\mathrm{acc}}$")
    
    # Highlight zones
    ax2.axvspan(0, T_rej, color=C_REJECT, alpha=0.15)
    ax2.text(0.10, 0.85, "Auto-Reject\nZone", color=C_REJECT, ha="center", fontsize=7.5, fontweight="bold")
    
    ax2.axvspan(T_rej, T_acc, color=C_REVIEW, alpha=0.15)
    ax2.text(0.52, 0.85, "Manual Review Zone\n(Rejection of Uncertainty)", color="#9a6700", ha="center", fontsize=7.5, fontweight="bold")
    
    ax2.axvspan(T_acc, 1.0, color=C_ACCEPT, alpha=0.18)
    ax2.text(0.91, 0.85, "Auto-Accept\nZone\n(FAR = 0%)", color=C_ACCEPT, ha="center", fontsize=7.5, fontweight="bold")
    
    ax2.set_title("(b) Proposed AAFV-Net 3-Way Bounded Rule", fontweight="bold")
    ax2.set_xlabel("Calibrated Probability $P(y=1 \mid z, \mathrm{Guards})$")
    ax2.set_ylabel("Probability Density")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc="upper left", frameon=True, fontsize=7)
    ax2.grid(True)
    
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig1_concept.pdf")
    fig.savefig(OUT_DIR / "fig1_concept.png")
    plt.close(fig)
    print("  -> Saved fig1_concept (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 2: Architecture Flowchart (Vector schematic)
# -----------------------------------------------------------------------------
def generate_fig2_architecture():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.axis("off")
    
    # Helper to draw boxes
    def draw_box(x, y, w, h, text, fc="#f6f8fa", ec="#24292f", lw=1.2, fs=8, bold=False):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                     linewidth=lw, edgecolor=ec, facecolor=fc)
        ax.add_patch(box)
        weight = "bold" if bold else "normal"
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, weight=weight, color="#1f2328")
        return (x + w/2, y + h/2)
    
    def draw_arrow(x1, y1, x2, y2, color="#57606a", lw=1.2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=lw, shrinkA=3, shrinkB=3))

    # Input Images
    draw_box(0.02, 0.60, 0.14, 0.30, "Input Pair\n$I_1(a_1), I_2(a_2)$\n$g = a_2 - a_1$", fc="#ddf4ff", ec="#0969da", bold=True)
    draw_box(0.02, 0.15, 0.14, 0.28, "Face Quality\nModule\n$Q(I_1, I_2)$", fc="#fff8c5", ec="#9a6700")

    # Direct Branch
    draw_box(0.22, 0.65, 0.18, 0.25, "Direct Branch\n$(I_1, I_2)$\n5-Score Extractor\n(ArcFace, EffNet, VGG,\nLPIPS, SSIM)", fc="#f6f8fa", ec="#24292f")
    draw_box(0.44, 0.67, 0.12, 0.21, "Direct Linear\nLearner $W_d$\n$5 \\to 1$", fc="#eaeef2", ec="#57606a")

    # SAM Synthesis Branch
    draw_box(0.22, 0.12, 0.18, 0.40, "SAM Aging Branch\n$I_1 \\to a_2$, $I_2 \\to a_1$\nShared Targets $t_k$\n$K \\leq 7$ grids\n$R_{\\mathrm{sam}}$ Reliability", fc="#f6f8fa", ec="#24292f")
    draw_box(0.44, 0.20, 0.12, 0.24, "SAM Linear\nLearner $W_s$\n$5 \\to 1$\n(Mask $p=0.12$)", fc="#eaeef2", ec="#57606a")

    # Fusion Vector & MLP
    draw_box(0.60, 0.35, 0.15, 0.45, "Calibrated Fusion\nVector $z \\in \\mathbb{R}^{11}$\n[Scores, $g, Q, R_{\\mathrm{sam}}$]\nMLP $11 \\to 32 \\to 16 \\to 1$\nPlatt Scaling $\\to P$", fc="#dafbe1", ec="#1a7f37", bold=True)

    # Guards & Decision
    draw_box(0.80, 0.65, 0.17, 0.25, "Accept Decision\n$P \\geq T_{\\mathrm{acc}} \\; (0.9564)$\nGuards Satisfied\nAUTO-ACCEPT", fc="#d1f2d9", ec="#1a7f37", bold=True)
    draw_box(0.80, 0.38, 0.17, 0.22, "Review Decision\n$T_{\\mathrm{rej}} < P < T_{\\mathrm{acc}}$\nor Guard Failure\nMANUAL REVIEW", fc="#fff8c5", ec="#bf8700", bold=True)
    draw_box(0.80, 0.10, 0.17, 0.22, "Reject Decision\n$P \\leq T_{\\mathrm{rej}}(\\beta) \\; (0.0075)$\nAUTO-REJECT", fc="#ffebe9", ec="#cf222e", bold=True)

    # Connections
    draw_arrow(0.16, 0.75, 0.22, 0.75)
    draw_arrow(0.16, 0.70, 0.22, 0.35)
    draw_arrow(0.16, 0.28, 0.60, 0.45) # Quality to fusion
    draw_arrow(0.40, 0.77, 0.44, 0.77)
    draw_arrow(0.40, 0.32, 0.44, 0.32)
    draw_arrow(0.56, 0.77, 0.60, 0.65)
    draw_arrow(0.56, 0.32, 0.60, 0.50)
    draw_arrow(0.75, 0.65, 0.80, 0.75)
    draw_arrow(0.75, 0.55, 0.80, 0.50)
    draw_arrow(0.75, 0.45, 0.80, 0.20)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig2_architecture.pdf")
    fig.savefig(OUT_DIR / "fig2_architecture.png")
    plt.close(fig)
    print("  -> Saved fig2_architecture (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 3: MORPH Results Trade-off & FG-NET Adults Gap Bin Evaluation
# -----------------------------------------------------------------------------
def generate_fig3_results():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
    
    # Subplot A: Trade-off on MORPH Test
    methods = [
        "AAFV-Net (Full)", "No Shared Targets", "ArcFace Only",
        "Direct 5-Score LR", "Direct-Only MLP", "Siamese CNN", "Siamese ViT"
    ]
    same_acc = [70.07, 83.91, 89.44, 87.14, 0.0, 0.17, 0.0]
    hard_rej = [98.04, 97.94, 0.0, 0.0, 97.80, 9.94, 9.98]
    colors = [C_PRIMARY, "#0969da", C_MUTED, "#57606a", "#8250df", "#d29922", "#cf5c36"]
    markers = ["o", "s", "^", "v", "D", "P", "X"]
    
    for m, acc, rej, c, mk in zip(methods, same_acc, hard_rej, colors, markers):
        ax1.scatter(rej, acc, color=c, marker=mk, s=55, label=m, zorder=5)
    
    ax1.set_title("(a) Same-Person Accept vs Hard Rejection (MORPH)", fontweight="bold")
    ax1.set_xlabel(r"ArcFace-Mined Hard Impostor Rejection Rate (\%)")
    ax1.set_ylabel(r"Same-Person Auto-Accept Rate (\%)")
    ax1.set_xlim(-5, 105)
    ax1.set_ylim(-5, 100)
    ax1.grid(True)
    ax1.legend(loc="lower left", fontsize=7, frameon=True)

    # Subplot B: FG-NET Adults Accept Rate by Age-Gap Bin
    bins = ["<5", "5-10", "10-15", "15-20", "20-30", "30+"]
    aafv_gap = [71.6, 59.6, 49.0, 38.2, 28.5, 10.3]
    arc_gap = [60.7, 49.2, 35.6, 25.9, 14.5, 3.8]
    
    x = np.arange(len(bins))
    width = 0.35
    
    ax2.bar(x - width/2, aafv_gap, width, label="AAFV-Net (Ours)", color=C_PRIMARY)
    ax2.bar(x + width/2, arc_gap, width, label="ArcFace Baseline", color=C_MUTED)
    
    ax2.set_title("(b) External Generalization on FG-NET Adults", fontweight="bold")
    ax2.set_xlabel("Age-Gap Bin (Years)")
    ax2.set_ylabel("Auto-Accept Rate (%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(bins)
    ax2.set_ylim(0, 85)
    ax2.grid(True, axis="y")
    ax2.legend(loc="upper right", fontsize=7.5, frameon=True)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig3_results.pdf")
    fig.savefig(OUT_DIR / "fig3_results.png")
    plt.close(fig)
    print("  -> Saved fig3_results (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 4: Calibration Ablation Study (Accept & Hard Rejection)
# -----------------------------------------------------------------------------
def generate_fig4_ablations():
    dt_path = Path("Code/AAFV_Net/ablations/decision_table_calibration.csv")
    if dt_path.exists():
        dt = pd.read_csv(dt_path)
        d = dt[dt.beta == 0.01].copy()
    else:
        d = None

    variants = [
        "Full AAFV-Net", "Drop ArcFace", "Drop LPIPS", "Drop EfficientNet",
        "Drop VGG", "Drop SSIM", "No Branch Masking", "No Context Inputs",
        "No Shared Targets", "Direct-Only MLP", "SAM-Only MLP", "No Guards"
    ]
    # Verified numbers from results_verification.md & ablation_calibration.csv
    acc_vals = [74.07, 0.70, 62.90, 81.30, 73.90, 72.80, 3.60, 0.0, 84.80, 0.0, 0.0, 0.0]
    rej_vals = [98.24, 17.90, 97.50, 97.60, 97.20, 97.40, 98.40, 98.10, 98.30, 98.50, 44.80, 98.20]

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    y = np.arange(len(variants))
    height = 0.38
    
    ax.barh(y - height/2, acc_vals, height, label=r"Same-Person Accept Rate (\%)", color=C_ACCEPT)
    ax.barh(y + height/2, rej_vals, height, label=r"Hard-Impostor Rejection Rate (\%)", color=C_PRIMARY)
    
    ax.set_yticks(y)
    ax.set_yticklabels(variants, fontsize=8)
    ax.invert_yaxis()  # Top-down order
    ax.set_xlabel("Calibration Rate (%) at Target False-Reject Rate $\\beta=0.01$")
    ax.set_title("AAFV-Net Component Ablation Analysis (Calibration Split)", fontweight="bold")
    ax.set_xlim(0, 105)
    ax.legend(loc="lower right", fontsize=8, frameon=True)
    ax.grid(True, axis="x")
    
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig4_ablations.pdf")
    fig.savefig(OUT_DIR / "fig4_ablations.png")
    plt.close(fig)
    print("  -> Saved fig4_ablations (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 5: Gap Bins & Neutral Hard Impostor Rejection
# -----------------------------------------------------------------------------
def generate_fig5_gap_neutral():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    
    # Subplot A: MORPH Test Same-Person Accept by Gap Bin
    gap_bins = ["G1 (0-3y)", "G2 (4-7y)", "G3 (8-11y)", "G4 (12-15y)", "G5 (16-19y)"]
    aafv_morph = [71.0, 56.4, 45.7, 1.3, 2.2]
    arc_morph = [90.5, 80.1, 69.0, 2.7, 2.2]
    
    x = np.arange(len(gap_bins))
    w = 0.35
    ax1.bar(x - w/2, aafv_morph, w, label="AAFV-Net", color=C_PRIMARY)
    ax1.bar(x + w/2, arc_morph, w, label="ArcFace Only", color=C_MUTED)
    ax1.set_xticks(x)
    ax1.set_xticklabels(gap_bins, rotation=25, ha="right")
    ax1.set_ylabel("Auto-Accept Rate (%)")
    ax1.set_title("(a) MORPH Test Accept by Gap Bin", fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.grid(True, axis="y")
    ax1.legend(loc="upper right", fontsize=7.5)

    # Subplot B: Neutral Hard Impostor Auto-Rejection (Test)
    neutral_methods = ["AAFV-Net (Full)", "No Shared Targets", "Direct-Only MLP", "ArcFace Only", "Direct 5-Score LR"]
    neutral_rej = [57.5, 54.0, 50.0, 28.5, 22.4]
    colors = [C_PRIMARY, "#0969da", "#8250df", C_MUTED, "#57606a"]
    
    y = np.arange(len(neutral_methods))
    ax2.barh(y, neutral_rej, color=colors, height=0.55)
    ax2.set_yticks(y)
    ax2.set_yticklabels(neutral_methods, fontsize=8)
    ax2.invert_yaxis()
    ax2.set_xlabel("Auto-Rejection Rate (%) on Neutral Hard Set")
    ax2.set_title("(b) Neutral Hard Impostor Rejection", fontweight="bold")
    ax2.set_xlim(0, 75)
    ax2.grid(True, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig5_gap_neutral.pdf")
    fig.savefig(OUT_DIR / "fig5_gap_neutral.png")
    plt.close(fig)
    print("  -> Saved fig5_gap_neutral (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 6: Sensitivity to False-Reject Target Beta
# -----------------------------------------------------------------------------
def generate_fig6_beta_sweep():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.8))
    
    # Data from extended_test.csv for beta in [0.005, 0.010, 0.020]
    betas = [0.005, 0.010, 0.020]
    # AAFV-Net
    aafv_rej = [97.02, 98.04, 99.11]  # D_hard rej
    aafv_bal = [0.492, 0.516, 0.534]
    
    # ArcFace
    arc_rej = [0.0, 0.0, 0.0]
    arc_bal = [0.651, 0.670, 0.690]
    
    # Direct only MLP
    dmlp_rej = [96.5, 97.8, 98.9]
    dmlp_bal = [0.125, 0.139, 0.155]
    
    ax1.plot(betas, aafv_rej, "o-", color=C_PRIMARY, label="AAFV-Net (Ours)", linewidth=1.8)
    ax1.plot(betas, dmlp_rej, "s--", color="#8250df", label="Direct-Only MLP")
    ax1.plot(betas, arc_rej, "^:", color=C_MUTED, label="ArcFace Only")
    
    ax1.set_xscale("log")
    ax1.set_xticks(betas)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.set_xlabel(r"Target False-Reject Rate $\beta$")
    ax1.set_ylabel(r"$D_{\mathrm{hard}}$ Auto-Rejected (\%)")
    ax1.set_title(r"(a) Hard-Impostor Rejection vs $\beta$", fontweight="bold")
    ax1.set_ylim(-5, 105)
    ax1.grid(True)
    ax1.legend(loc="lower right", fontsize=7.5)

    ax2.plot(betas, aafv_bal, "o-", color=C_PRIMARY, label="AAFV-Net (Ours)", linewidth=1.8)
    ax2.plot(betas, dmlp_bal, "s--", color="#8250df", label="Direct-Only MLP")
    ax2.plot(betas, arc_bal, "^:", color=C_MUTED, label="ArcFace Only")
    
    ax2.set_xscale("log")
    ax2.set_xticks(betas)
    ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax2.set_xlabel(r"Target False-Reject Rate $\beta$")
    ax2.set_ylabel("Balanced Automation Metric")
    ax2.set_title(r"(b) Balanced Automation vs $\beta$", fontweight="bold")
    ax2.set_ylim(0, 0.8)
    ax2.grid(True)
    ax2.legend(loc="upper left", fontsize=7.5)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig6_beta_sweep.pdf")
    fig.savefig(OUT_DIR / "fig6_beta_sweep.png")
    plt.close(fig)
    print("  -> Saved fig6_beta_sweep (pdf, png)")

# -----------------------------------------------------------------------------
# FIGURE 7: Calibration Decision Outcome Breakdown
# -----------------------------------------------------------------------------
def generate_fig7_decision_outcomes():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
    
    methods = ["AAFV-Net", "ArcFace", "Direct MLP", "Siamese CNN", "Siamese ViT", "VLM"]
    
    # Same person breakdown: [auto-accept, manual review, false reject]
    # At beta = 0.01, false reject is fixed at ~1.0%
    same_acc = np.array([74.07, 87.20, 0.0, 0.58, 0.0, 0.0])
    same_rej = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    same_rev = 100.0 - same_acc - same_rej
    
    # Hard impostor breakdown: [false accept, manual review, auto-reject]
    # At zero false accept on calibration: false accept = 0%
    hard_rej = np.array([98.24, 0.0, 98.50, 0.60, 3.60, 10.20])
    hard_fa  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    hard_rev = 100.0 - hard_rej - hard_fa
    
    x = np.arange(len(methods))
    w = 0.55
    
    # Panel 1: Same Person
    ax1.bar(x, same_acc, w, label="Auto-Accept", color=C_ACCEPT)
    ax1.bar(x, same_rev, w, bottom=same_acc, label="Manual Review", color=C_REVIEW)
    ax1.bar(x, same_rej, w, bottom=same_acc+same_rev, label="False Reject (1%)", color=C_REJECT)
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods, rotation=35, ha="right", fontsize=7.5)
    ax1.set_ylabel("Outcome Share (%)")
    ax1.set_title("(a) Same-Person Pairs", fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.legend(loc="lower right", fontsize=7.5)
    
    # Panel 2: Hard Impostors
    ax2.bar(x, hard_rej, w, label="Auto-Reject", color=C_ACCEPT)
    ax2.bar(x, hard_rev, w, bottom=hard_rej, label="Manual Review", color=C_REVIEW)
    ax2.bar(x, hard_fa, w, bottom=hard_rej+hard_rev, label="False Accept (0%)", color=C_REJECT)
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods, rotation=35, ha="right", fontsize=7.5)
    ax2.set_ylabel("Outcome Share (%)")
    ax2.set_title(r"(b) Hard Impostor Pairs ($D_{\mathrm{hard}}$)", fontweight="bold")
    ax2.set_ylim(0, 100)
    ax2.legend(loc="lower right", fontsize=7.5)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig7_decision_outcomes.pdf")
    fig.savefig(OUT_DIR / "fig7_decision_outcomes.png")
    plt.close(fig)
    print("  -> Saved fig7_decision_outcomes (pdf, png)")

if __name__ == "__main__":
    generate_fig1_concept()
    generate_fig2_architecture()
    generate_fig3_results()
    generate_fig4_ablations()
    generate_fig5_gap_neutral()
    generate_fig6_beta_sweep()
    generate_fig7_decision_outcomes()
    print("All 7 publication figures successfully generated in vector PDF and 300-dpi PNG formats.")
