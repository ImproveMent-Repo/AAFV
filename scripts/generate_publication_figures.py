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
# FIGURE 2: Architecture Flowchart (Clean 5-Stage Left-to-Right Vector Diagram)
# -----------------------------------------------------------------------------
def generate_fig2_architecture():
    fig, ax = plt.subplots(figsize=(13.2, 6.2))
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    def draw_stage_bg(x, y, w, h, stage_num, stage_title):
        bg = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2",
                                    linewidth=0.8, edgecolor="#cbd5e1", facecolor="#f8fafc", zorder=1)
        ax.add_patch(bg)
        header_pill = patches.FancyBboxPatch((x + 0.8, y + h - 4.2), w - 1.6, 3.6,
                                             boxstyle="round,pad=0.2,rounding_size=0.6",
                                             linewidth=0.5, edgecolor="#94a3b8", facecolor="#e2e8f0", zorder=2)
        ax.add_patch(header_pill)
        ax.text(x + w/2, y + h - 2.4, f"STAGE {stage_num}: {stage_title}",
                ha="center", va="center", fontsize=8.0, weight="bold", color="#1e293b", zorder=3)

    def draw_box(x, y, w, h, title, lines, fc="#ffffff", ec="#334155", lw=1.2,
                 title_color="#0f172a", title_bg=None, text_color="#1e293b", fs=7.8):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.8",
                                     linewidth=lw, edgecolor=ec, facecolor=fc, zorder=4)
        ax.add_patch(box)
        cur_y = y + h - 2.5
        if title:
            if title_bg:
                tb = patches.FancyBboxPatch((x + 0.3, cur_y - 2.2), w - 0.6, 4.0,
                                            boxstyle="round,pad=0.1,rounding_size=0.5",
                                            linewidth=0.5, edgecolor=ec, facecolor=title_bg, zorder=5)
                ax.add_patch(tb)
                ax.text(x + w/2, cur_y - 0.2, title, ha="center", va="center",
                        fontsize=fs+0.6, weight="bold", color=title_color, zorder=6)
                cur_y -= 4.2
            else:
                ax.text(x + w/2, cur_y, title, ha="center", va="center",
                        fontsize=fs+0.6, weight="bold", color=title_color, zorder=6)
                cur_y -= 3.5

        for line in lines:
            if line == "---":
                ax.plot([x + 0.8, x + w - 0.8], [cur_y, cur_y], color=ec, lw=0.6, linestyle=":", zorder=5)
                cur_y -= 2.2
            else:
                ax.text(x + w/2, cur_y, line, ha="center", va="center",
                        fontsize=fs, color=text_color, zorder=6)
                cur_y -= 2.7
        return (x, y, w, h)

    def draw_ortho_arrow(points, color="#1e293b", lw=1.3, label=None, label_pos=None,
                         label_offset=(0, 1.2), label_fs=7.2):
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            if i == len(points) - 2:
                ax.annotate("", xy=p2, xytext=p1,
                            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                            mutation_scale=10, shrinkA=0, shrinkB=0), zorder=7)
            else:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=7)
        if label and label_pos:
            ax.text(label_pos[0] + label_offset[0], label_pos[1] + label_offset[1],
                    label, fontsize=label_fs, color=color, ha="center", va="center",
                    weight="bold",
                    bbox=dict(boxstyle="square,pad=0.18", fc="#ffffff", ec="#94a3b8", lw=0.6, alpha=0.95),
                    zorder=8)

    # 1. Background panels
    draw_stage_bg(2.0, 4.0, 16.5, 92.0, 1, "INPUT")
    draw_stage_bg(21.5, 4.0, 22.0, 92.0, 2, "EVIDENCE EXTRACTION")
    draw_stage_bg(46.0, 4.0, 17.5, 92.0, 3, "FEATURE PROCESSING")
    draw_stage_bg(65.5, 4.0, 17.5, 92.0, 4, "FUSION & CALIBRATION")
    draw_stage_bg(85.0, 4.0, 13.5, 92.0, 5, "THREE-WAY DECISION")

    # 2. Stage 1 Boxes
    b1a_lines = [
        r"Face 1: $I_1$ (Age $a_1$)",
        r"Face 2: $I_2$ (Age $a_2$)",
        r"Age Gap: $g = a_2 - a_1$",
        r"Aligned to $256 \times 256$",
        r"(FFHQ Landmark Standard)"
    ]
    draw_box(3.2, 53.0, 14.1, 34.0, "Input Photo Pair", b1a_lines,
             fc="#f0f9ff", ec="#0284c7", lw=1.3, title_color="#0369a1", title_bg="#e0f2fe")

    b1b_lines = [
        r"Quality Metric $Q(I_1, I_2)$",
        r"$Q = \min(Q_1, Q_2) \in [0, 1]$",
        r"Symmetry, Sharpness, Illum.",
        "---",
        r"Quality Guard:",
        r"$Q \geq Q_{\min} = 0.20$"
    ]
    draw_box(3.2, 11.0, 14.1, 32.0, "Face Quality Module", b1b_lines,
             fc="#fefce8", ec="#ca8a04", lw=1.3, title_color="#854d0e", title_bg="#fef9c3")

    # 3. Stage 2 Boxes
    b2a_lines = [
        r"Original Pair $(I_1, I_2)$",
        r"5-Score Similarity Vector $\mathbf{s}_{\mathrm{dir}}$:",
        "• ArcFace Cosine " + r"$s_{\mathrm{arc}}$ (512-D)",
        "• EfficientNet-B0 Feats " + r"$s_{\mathrm{eff}}$",
        "• VGG-Face Feats " + r"$s_{\mathrm{vgg}}$",
        "• LPIPS Perceptual Dist " + r"$d_{\mathrm{lpips}}$",
        "• Structural SSIM Metric " + r"$s_{\mathrm{ssim}}$"
    ]
    draw_box(23.0, 53.0, 19.0, 34.0, "Direct Evidence Branch", b2a_lines,
             fc="#ffffff", ec="#334155", lw=1.3, title_color="#0f172a", title_bg="#f1f5f9")

    b2b_lines = [
        r"SAM Latent Age Progression:",
        "• Forward: " + r"$I_1 \to a_2$ (at older age)",
        "• Backward: " + r"$I_2 \to a_1$ (at younger age)",
        "• Shared Targets " + r"$t_k$ ($K \leq 7$ grids)",
        r"$\mathbf{s}_{\mathrm{sam}}$ = Median Target Scores",
        "---",
        r"Reliability: $R_{\mathrm{sam}} \in [0, 1]$",
        r"Guard: $R_{\mathrm{sam}} \geq R_{\min} = 0.30$"
    ]
    draw_box(23.0, 11.0, 19.0, 34.0, "SAM Aging Branch", b2b_lines,
             fc="#ffffff", ec="#334155", lw=1.3, title_color="#0f172a", title_bg="#f1f5f9")

    # 4. Stage 3 Boxes
    b3a_lines = [
        r"Linear Model $W_d \in \mathbb{R}^5$",
        r"Projection: $5 \to 1$",
        r"$v_d = W_d^T \mathbf{s}_{\mathrm{dir}} + b_d$",
        "---",
        r"Platt Guard:",
        r"$P_d = \sigma(A_d v_d + B_d)$",
        r"Guard: $P_d \geq \rho = 0.20$"
    ]
    draw_box(47.5, 53.0, 14.5, 34.0, "Direct Learner", b3a_lines,
             fc="#ffffff", ec="#475569", lw=1.3, title_color="#0f172a", title_bg="#f1f5f9")

    b3b_lines = [
        r"Linear Model $W_s \in \mathbb{R}^5$",
        r"Projection: $5 \to 1$",
        r"$v_s = W_s^T \mathbf{s}_{\mathrm{sam}} + b_s$",
        "---",
        r"Training Branch Mask:",
        r"Mask $p_{\mathrm{mask}} = 0.12$",
        r"Platt Guard: $P_s \geq 0.20$"
    ]
    draw_box(47.5, 11.0, 14.5, 34.0, "SAM Learner", b3b_lines,
             fc="#ffffff", ec="#475569", lw=1.3, title_color="#0f172a", title_bg="#f1f5f9")

    # 5. Stage 4 Boxes
    b4a_lines = [
        r"11-D Input Vector $\mathbf{z} \in \mathbb{R}^{11}$:",
        r"$\mathbf{z} = [v_d, v_s, g, Q, R_{\mathrm{sam}},$",
        r"$\quad \mathbb{I}_{\mathrm{sam}}, \mathbb{I}_{\mathrm{enh}}, 0, 0, 0, 0]^T$",
        r"Concatenates branch outputs,",
        r"age gap $g$, quality $Q$, and reliability."
    ]
    draw_box(67.0, 56.0, 14.5, 27.0, "Calibrated Fusion Vector", b4a_lines,
             fc="#f0fdf4", ec="#16a34a", lw=1.3, title_color="#14532d", title_bg="#dcfce7")

    b4b_lines = [
        r"Multimodal Fusion MLP:",
        r"$\mathbb{R}^{11} \to \mathbb{R}^{32} \to \mathbb{R}^{16} \to \mathbb{R}^{1}$",
        r"ReLU, Dropout $p=0.10$",
        r"Ensemble of 5 Trained Seeds",
        "---",
        r"Platt Calibration:",
        r"$P = \sigma(A_{\mathrm{cal}}\bar{\ell} + B_{\mathrm{cal}}) \in [0, 1]$",
        r"Calibrated Posterior Probability"
    ]
    draw_box(67.0, 11.0, 14.5, 35.0, "MLP & Platt Scaling", b4b_lines,
             fc="#f0fdf4", ec="#16a34a", lw=1.3, title_color="#14532d", title_bg="#dcfce7")

    # 6. Stage 5 Boxes
    b5a_lines = [
        r"$P \geq T_{\mathrm{acc}} = 0.9564$",
        r"$\wedge$ Guards Satisfied",
        "---",
        r"Zero Random FA (0/1,149)",
        r"FAR $\leq$ 0.320% (95% CI)",
        r"Auto-Accept: 70.07%"
    ]
    draw_box(86.2, 65.0, 11.2, 26.0, "AUTO-ACCEPT", b5a_lines,
             fc="#dcfce7", ec="#15803d", lw=1.5, title_color="#14532d", title_bg="#bbf7d0", fs=7.4)

    b5b_lines = [
        r"$T_{\mathrm{rej}} < P < T_{\mathrm{acc}}$",
        r"$\vee$ Guard Failure",
        "---",
        r"Uncertainty Absorption",
        r"Review Rate: 28.93%",
        r"Human Biometric Audit"
    ]
    draw_box(86.2, 38.0, 11.2, 24.0, "MANUAL REVIEW", b5b_lines,
             fc="#fef9c3", ec="#ca8a04", lw=1.5, title_color="#854d0e", title_bg="#fef08a", fs=7.4)

    b5c_lines = [
        r"$P \leq T_{\mathrm{rej}}(\beta) = 0.0075$",
        r"Target FRR $\beta = 1.0\%$",
        "---",
        r"Rejects 98.04% Hard Imp.",
        r"Rejects 57.53% Neutral",
        r"Auto-Reject Rate: 1.00%"
    ]
    draw_box(86.2, 11.0, 11.2, 24.0, "AUTO-REJECT", b5c_lines,
             fc="#fee2e2", ec="#dc2626", lw=1.5, title_color="#991b1b", title_bg="#fecaca", fs=7.4)

    # 7. Strictly Orthogonal Arrow Routing
    # Input Pair -> Direct Branch
    draw_ortho_arrow([(17.3, 75.0), (23.0, 75.0)], color="#0284c7", lw=1.4)
    # Input Pair -> SAM Branch
    draw_ortho_arrow([(17.3, 60.0), (19.8, 60.0), (19.8, 28.0), (23.0, 28.0)], color="#0284c7", lw=1.4)
    # Input Pair -> Face Quality Module
    draw_ortho_arrow([(10.25, 53.0), (10.25, 43.0)], color="#0284c7", lw=1.4)

    # Upper Bypass Lane: Age Gap g
    draw_ortho_arrow([(10.25, 87.0), (10.25, 90.5), (74.25, 90.5), (74.25, 83.0)],
                     color="#0369a1", lw=1.3,
                     label=r"Age Gap $g = a_2 - a_1$ Context Bypass", label_pos=(42.0, 90.5), label_offset=(0, 0))

    # Lower Bypass Lane: Face Quality Q
    draw_ortho_arrow([(10.25, 11.0), (10.25, 6.5), (64.8, 6.5), (64.8, 61.0), (67.0, 61.0)],
                     color="#854d0e", lw=1.3,
                     label=r"Face Quality $Q(I_1, I_2)$ Context Bypass", label_pos=(37.0, 6.5), label_offset=(0, 0))

    # Direct Branch -> Direct Learner
    draw_ortho_arrow([(42.0, 70.0), (47.5, 70.0)],
                     color="#334155", lw=1.4,
                     label=r"$\mathbf{s}_{\mathrm{dir}}$", label_pos=(44.75, 70.0), label_offset=(0, 1.8), label_fs=7.5)

    # SAM Aging Branch -> SAM Learner
    draw_ortho_arrow([(42.0, 28.0), (47.5, 28.0)],
                     color="#334155", lw=1.4,
                     label=r"$\mathbf{s}_{\mathrm{sam}}$", label_pos=(44.75, 28.0), label_offset=(0, 1.8), label_fs=7.5)

    # Direct Learner -> Fusion Vector
    draw_ortho_arrow([(62.0, 70.0), (67.0, 70.0)],
                     color="#334155", lw=1.4,
                     label=r"$v_d, P_d$", label_pos=(64.5, 70.0), label_offset=(0, 1.8), label_fs=7.5)

    # SAM Learner -> Fusion Vector
    draw_ortho_arrow([(62.0, 28.0), (63.8, 28.0), (63.8, 65.0), (67.0, 65.0)],
                     color="#334155", lw=1.4,
                     label=r"$v_s, P_s, R_{\mathrm{sam}}$", label_pos=(62.9, 28.0), label_offset=(0, 2.0), label_fs=7.0)

    # Fusion Vector -> MLP
    draw_ortho_arrow([(74.25, 56.0), (74.25, 46.0)],
                     color="#16a34a", lw=1.4,
                     label=r"Vector $\mathbf{z} \in \mathbb{R}^{11}$", label_pos=(74.25, 51.0), label_offset=(4.8, 0), label_fs=7.5)

    # MLP -> Three-Way Decision Tree
    draw_ortho_arrow([(81.5, 28.5), (84.2, 28.5)],
                     color="#16a34a", lw=1.4,
                     label=r"Prob $P \in [0, 1]$", label_pos=(82.85, 28.5), label_offset=(0, 2.0), label_fs=7.2)
    ax.plot([84.2, 84.2], [23.0, 78.0], color="#334155", lw=1.4, zorder=7)
    draw_ortho_arrow([(84.2, 78.0), (86.2, 78.0)], color="#15803d", lw=1.4)
    draw_ortho_arrow([(84.2, 50.0), (86.2, 50.0)], color="#ca8a04", lw=1.4)
    draw_ortho_arrow([(84.2, 23.0), (86.2, 23.0)], color="#dc2626", lw=1.4)

    fig.tight_layout(pad=0.4)
    fig.savefig(OUT_DIR / "fig2_architecture.pdf")
    fig.savefig(OUT_DIR / "fig2_architecture.png")
    plt.close(fig)
    print("  -> Saved redesigned fig2_architecture (pdf, png)")

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
