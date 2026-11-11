"""
Test and refine the redesigned Architecture Diagram (Figure 2) for AAFV-Net.
Ensures zero overlapping arrows, zero arrows passing through boxes,
strictly orthogonal routing, clean 5-stage left-to-right organization,
and complete preservation of all technical notation.
"""
import os, sys, tempfile
from pathlib import Path

os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# IEEE style configuration
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Times"],
    "font.size": 8.5,
    "axes.labelsize": 8.5,
    "axes.titlesize": 9.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

def generate_redesigned_fig2(output_pdf="publication/figures/fig2_architecture.pdf",
                             output_png="publication/figures/fig2_architecture.png"):
    fig, ax = plt.subplots(figsize=(13.2, 6.2))
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # -------------------------------------------------------------------------
    # Helper functions
    # -------------------------------------------------------------------------
    def draw_stage_bg(x, y, w, h, stage_num, stage_title):
        # Stage background panel
        bg = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2",
                                    linewidth=0.8, edgecolor="#cbd5e1", facecolor="#f8fafc", zorder=1)
        ax.add_patch(bg)
        # Stage header pill
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
        
        # If title background provided
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

        # Lines of text
        for line in lines:
            if line == "---":
                # Divider line
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

    # -------------------------------------------------------------------------
    # Draw Stage Background Panels (Stages 1 through 5)
    # -------------------------------------------------------------------------
    # Stage 1: Input (x: 2 to 18)
    draw_stage_bg(2.0, 4.0, 16.5, 92.0, 1, "INPUT")
    # Stage 2: Evidence Extraction (x: 22 to 43)
    draw_stage_bg(21.5, 4.0, 22.0, 92.0, 2, "EVIDENCE EXTRACTION")
    # Stage 3: Feature Processing (x: 46.5 to 63)
    draw_stage_bg(46.0, 4.0, 17.5, 92.0, 3, "FEATURE PROCESSING")
    # Stage 4: Fusion & Calibration (x: 66 to 82.5)
    draw_stage_bg(65.5, 4.0, 17.5, 92.0, 4, "FUSION & CALIBRATION")
    # Stage 5: Three-Way Decision (x: 85.5 to 98)
    draw_stage_bg(85.0, 4.0, 13.5, 92.0, 5, "THREE-WAY DECISION")

    # -------------------------------------------------------------------------
    # Stage 1 Boxes: Input Pair & Face Quality Module
    # -------------------------------------------------------------------------
    # Box 1A: Input Pair
    b1a_lines = [
        r"Face 1: $I_1$ (Age $a_1$)",
        r"Face 2: $I_2$ (Age $a_2$)",
        r"Age Gap: $g = a_2 - a_1$",
        r"Aligned to $256 \times 256$",
        r"(FFHQ Landmark Standard)"
    ]
    draw_box(3.2, 53.0, 14.1, 34.0, "Input Photo Pair", b1a_lines,
             fc="#f0f9ff", ec="#0284c7", lw=1.3, title_color="#0369a1", title_bg="#e0f2fe")

    # Box 1B: Face Quality Module
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

    # -------------------------------------------------------------------------
    # Stage 2 Boxes: Direct Branch & SAM Aging Branch
    # -------------------------------------------------------------------------
    # Box 2A: Direct Evidence Branch
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

    # Box 2B: SAM Generative Aging Branch
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

    # -------------------------------------------------------------------------
    # Stage 3 Boxes: Direct Linear Learner & SAM Linear Learner
    # -------------------------------------------------------------------------
    # Box 3A: Direct Learner
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

    # Box 3B: SAM Learner
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

    # -------------------------------------------------------------------------
    # Stage 4 Boxes: Fusion Vector & Multimodal MLP + Platt Scaling
    # -------------------------------------------------------------------------
    # Box 4A: Calibrated Fusion Vector
    b4a_lines = [
        r"11-D Input Vector $\mathbf{z} \in \mathbb{R}^{11}$:",
        r"$\mathbf{z} = [v_d, v_s, g, Q, R_{\mathrm{sam}},$",
        r"$\quad \mathbb{I}_{\mathrm{sam}}, \mathbb{I}_{\mathrm{enh}}, 0, 0, 0, 0]^T$",
        r"Concatenates branch outputs,",
        r"age gap $g$, quality $Q$, and reliability."
    ]
    draw_box(67.0, 56.0, 14.5, 27.0, "Calibrated Fusion Vector", b4a_lines,
             fc="#f0fdf4", ec="#16a34a", lw=1.3, title_color="#14532d", title_bg="#dcfce7")

    # Box 4B: Multimodal MLP & Platt Scaling
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

    # -------------------------------------------------------------------------
    # Stage 5 Boxes: Three-Way Decision Outcomes
    # -------------------------------------------------------------------------
    # Box 5A: Auto-Accept
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

    # Box 5B: Manual Review
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

    # Box 5C: Auto-Reject
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

    # -------------------------------------------------------------------------
    # STRICTLY ORTHOGONAL ARROW ROUTING (ZERO BOX CROSSINGS)
    # -------------------------------------------------------------------------
    # 1. Input Pair (right-upper, y=75.0) -> Direct Branch (left-upper, y=75.0)
    # Direct horizontal connection!
    draw_ortho_arrow([(17.3, 75.0), (23.0, 75.0)],
                     color="#0284c7", lw=1.4)

    # 2. Input Pair (right-lower, y=60.0) -> SAM Aging Branch (left-mid, y=28.0)
    # Exits to vertical lane between Stage 1 & Stage 2 at x=19.5, goes down to y=28.0, then into SAM branch
    draw_ortho_arrow([(17.3, 60.0), (19.8, 60.0), (19.8, 28.0), (23.0, 28.0)],
                     color="#0284c7", lw=1.4)

    # 3. Input Pair (bottom, x=10.25, y=53.0) -> Face Quality Module (top, x=10.25, y=43.0)
    # Direct vertical connection!
    draw_ortho_arrow([(10.25, 53.0), (10.25, 43.0)],
                     color="#0284c7", lw=1.4)

    # 4. Upper Bypass Lane: Age Gap g from Input Pair (top, x=10.25, y=87.0) -> Fusion Vector (top, x=74.25, y=83.0)
    # Ascends to y=90.5 (above Direct Branch), travels right across to x=74.25, drops into Fusion Vector
    draw_ortho_arrow([(10.25, 87.0), (10.25, 90.5), (74.25, 90.5), (74.25, 83.0)],
                     color="#0369a1", lw=1.3,
                     label=r"Age Gap $g = a_2 - a_1$ Context Bypass", label_pos=(42.0, 90.5), label_offset=(0, 0))

    # 5. Lower Bypass Lane: Quality Q from Face Quality Module (bottom, x=10.25, y=11.0) -> Fusion Vector (left, y=61.0)
    # Descends to y=6.5 (below SAM Branch), travels right to x=64.8 (between Stage 3 & Stage 4), ascends to y=61.0, enters Fusion Vector
    draw_ortho_arrow([(10.25, 11.0), (10.25, 6.5), (64.8, 6.5), (64.8, 61.0), (67.0, 61.0)],
                     color="#854d0e", lw=1.3,
                     label=r"Face Quality $Q(I_1, I_2)$ Context Bypass", label_pos=(37.0, 6.5), label_offset=(0, 0))

    # 6. Direct Branch (right, y=70.0) -> Direct Learner (left, y=70.0)
    # Direct horizontal connection!
    draw_ortho_arrow([(42.0, 70.0), (47.5, 70.0)],
                     color="#334155", lw=1.4,
                     label=r"$\mathbf{s}_{\mathrm{dir}}$", label_pos=(44.75, 70.0), label_offset=(0, 1.8), label_fs=7.5)

    # 7. SAM Aging Branch (right, y=28.0) -> SAM Learner (left, y=28.0)
    # Direct horizontal connection!
    draw_ortho_arrow([(42.0, 28.0), (47.5, 28.0)],
                     color="#334155", lw=1.4,
                     label=r"$\mathbf{s}_{\mathrm{sam}}$", label_pos=(44.75, 28.0), label_offset=(0, 1.8), label_fs=7.5)

    # 8. Direct Learner (right, y=70.0) -> Fusion Vector (left-upper, y=70.0)
    # Direct horizontal connection!
    draw_ortho_arrow([(62.0, 70.0), (67.0, 70.0)],
                     color="#334155", lw=1.4,
                     label=r"$v_d, P_d$", label_pos=(64.5, 70.0), label_offset=(0, 1.8), label_fs=7.5)

    # 9. SAM Learner (right, y=28.0) -> Fusion Vector (left-lower, y=65.0)
    # Exits at y=28.0, goes right to lane at x=63.8 (parallel to Q-lane at x=65.2), ascends to y=65.0, enters Fusion Vector
    draw_ortho_arrow([(62.0, 28.0), (63.8, 28.0), (63.8, 65.0), (67.0, 65.0)],
                     color="#334155", lw=1.4,
                     label=r"$v_s, P_s, R_{\mathrm{sam}}$", label_pos=(62.9, 28.0), label_offset=(0, 2.0), label_fs=7.0)

    # 10. Fusion Vector (bottom, x=74.25, y=56.0) -> MLP & Platt Scaling (top, x=74.25, y=46.0)
    # Direct vertical connection!
    draw_ortho_arrow([(74.25, 56.0), (74.25, 46.0)],
                     color="#16a34a", lw=1.4,
                     label=r"Vector $\mathbf{z} \in \mathbb{R}^{11}$", label_pos=(74.25, 51.0), label_offset=(4.8, 0), label_fs=7.5)

    # 11. MLP & Platt Scaling (right, y=28.5) -> Three-Way Decision Tree (x=86.2)
    # Exits to vertical decision distribution bus at x=84.2:
    # - Branch to Auto-Accept (y=78.0)
    # - Branch to Manual Review (y=50.0)
    # - Branch to Auto-Reject (y=23.0)
    draw_ortho_arrow([(81.5, 28.5), (84.2, 28.5)],
                     color="#16a34a", lw=1.4,
                     label=r"Prob $P \in [0, 1]$", label_pos=(82.85, 28.5), label_offset=(0, 2.0), label_fs=7.2)
    # Distribution bus line
    ax.plot([84.2, 84.2], [23.0, 78.0], color="#334155", lw=1.4, zorder=7)
    # Branch to Auto-Accept (y=78.0)
    draw_ortho_arrow([(84.2, 78.0), (86.2, 78.0)],
                     color="#15803d", lw=1.4)
    # Branch to Manual Review (y=50.0)
    draw_ortho_arrow([(84.2, 50.0), (86.2, 50.0)],
                     color="#ca8a04", lw=1.4)
    # Branch to Auto-Reject (y=23.0)
    draw_ortho_arrow([(84.2, 23.0), (86.2, 23.0)],
                     color="#dc2626", lw=1.4)

    fig.tight_layout(pad=0.4)
    fig.savefig(output_pdf)
    fig.savefig(output_png)
    plt.close(fig)
    print(f"Successfully generated redesigned Figure 2 in:\n  - {output_pdf}\n  - {output_png}")

if __name__ == "__main__":
    generate_redesigned_fig2()
