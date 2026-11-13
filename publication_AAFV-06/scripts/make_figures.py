"""Figures for AAFV-06.
1. AAFV-Net concept, architecture and outcome figures, regenerated with the AAFV-04 generator
   (AAFV-04_revision/manuscript/scripts/generate_tifs_figures.py). One correction is applied to the architecture box:
   the evaluated (Look-2) checkpoint is a 3-network ensemble, not 5 (verified in CVPR_redesign/phase9_reproducibility).
2. The proposed reliability-weighted age-transport (RAT) architecture, drawn here (a proposal, not an evaluated system).
3. Image results assembled from existing images. Every file containing faces is prefixed `faces_` and is git-ignored
   (licensed datasets; the GitHub repository is public).
Usage: python scripts/make_figures.py   (from publication_AAFV-06/)"""
import types
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

PUB = Path(__file__).resolve().parent.parent
ROOT = PUB.parent
FIG = PUB / "figures"
FIG.mkdir(exist_ok=True)


# ---------------------------------------------------------------- 1. AAFV-Net figures (AAFV-04 generator, corrected)
def aafv_figures():
    src_path = ROOT / "AAFV-04_revision/manuscript/scripts/generate_tifs_figures.py"
    src = src_path.read_text(encoding="utf-8")
    assert "5 seeds, AdamW" in src, "architecture text changed upstream; review the correction"
    src = src.replace("5 seeds, AdamW", "3 seeds evaluated, AdamW")
    src = src.replace('if __name__ == "__main__":', "if False:")
    mod = types.ModuleType("gen04")
    mod.__file__ = str(src_path)
    exec(compile(src, str(src_path), "exec"), mod.__dict__)
    mod.OUT = FIG
    mod.ABL = ROOT / "Code" / "AAFV_Net" / "ablations"
    for fn, stem in [("make_fig1_concept", "fig1_concept"), ("make_fig2_architecture", "fig2_architecture"),
                     ("make_fig7_decision_outcomes", "fig7_decision_outcomes")]:
        getattr(mod, fn)()
        print("regenerated", stem)


# ---------------------------------------------------------------- 2. proposed architecture (drawn)
def box(ax, x, y, w, h, title, body, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="top", fontsize=9.5, fontweight="bold", color=ec)
    ax.text(x + w / 2, y + h - 0.85, body, ha="center", va="top", fontsize=7.6, linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, color="#374151", style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=12, color=color, lw=1.3, linestyle=ls))


def proposed_architecture():
    fig, ax = plt.subplots(figsize=(13, 5.6))
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.text(0.2, 10.6, "TRAINING (generator used offline only)", fontsize=10, fontweight="bold", color="#6b7280")
    ax.text(0.2, 4.9, "VERIFICATION (no generation)", fontsize=10, fontweight="bold", color="#6b7280")
    ax.plot([0, 26], [5.35, 5.35], color="#d1d5db", lw=1, ls="--")
    blue, green, amber, red, grey = "#1d4ed8", "#047857", "#b45309", "#b91c1c", "#374151"
    # training row
    box(ax, 0.3, 7.0, 4.6, 3.2, "Real longitudinal pairs", "same person at ages\n$(I_y, a_y)$, $(I_o, a_o)$\n+ gap-matched impostors", "#eff6ff", blue)
    box(ax, 5.6, 7.0, 4.6, 3.2, "Face-aging generator $G$", "SAM / FADING\n$G(I, t)$ at target ages $t$\n(offline, training only)", "#fffbeb", amber)
    box(ax, 10.9, 7.0, 4.8, 3.2, "Frozen recognizer $f$", "AdaFace (WebFace)\n$e = f(I)$ for real faces\n$\\hat e_t = f(G(I,t))$ for synthetic", "#f0fdf4", green)
    box(ax, 16.4, 7.0, 4.4, 3.2, "Reliability net $w_\\psi$", "features $\\phi$ from an\nindependent recognizer $h \\neq f$\n(identity, age error, quality)", "#fef2f2", red)
    box(ax, 21.4, 7.0, 4.3, 3.2, "Training loss", "vMF NLL on real pairs\n+ $\\sum_s w_\\psi(\\phi_s)\\,\\ell_s$ (synthetic)\n$-\\lambda \\log w_\\psi$ + impostor margin", "#f9fafb", grey)
    arrow(ax, 4.9, 7.55, 10.9, 7.55, blue)
    arrow(ax, 10.2, 7.25, 10.9, 7.25, amber)
    arrow(ax, 15.7, 7.55, 21.4, 7.55, green)
    arrow(ax, 20.8, 7.25, 21.4, 7.25, red)
    ax.text(13.3, 6.55, "precomputed once", fontsize=7.5, ha="center", color="#6b7280", style="italic")
    # test row
    box(ax, 0.3, 0.6, 4.6, 3.7, "Input pair", "$(I_1, a_1)$, $(I_2, a_2)$\nages known or\nestimated", "#eff6ff", blue)
    box(ax, 5.6, 0.6, 4.6, 3.7, "Frozen recognizer $f$", "$e_1 = f(I_1)$\n$e_2 = f(I_2)$\n(two passes)", "#f0fdf4", green)
    box(ax, 10.9, 0.6, 5.6, 3.7, "Age transport $T_\\theta$ + $\\kappa_\\theta$", "$\\tilde e_{12} = T_\\theta(e_1, a_1 \\rightarrow a_2)$\n$\\tilde e_{21} = T_\\theta(e_2, a_2 \\rightarrow a_1)$\ngap-dependent concentration $\\kappa$", "#f5f3ff", "#6d28d9")
    box(ax, 17.2, 0.6, 4.2, 3.7, "Gap-aware score", "$S = \\frac{1}{2}[\\kappa_{12}\\,\\tilde e_{12}^{\\top}e_2$\n$+\\ \\kappa_{21}\\,e_1^{\\top}\\tilde e_{21}]$", "#f9fafb", grey)
    box(ax, 22.1, 0.6, 3.6, 3.7, "Three-way rule", "Accept / Review /\nReject at fresh,\nconformal thresholds", "#ecfdf5", green)
    arrow(ax, 4.9, 2.45, 5.6, 2.45, blue)
    arrow(ax, 10.2, 2.45, 10.9, 2.45, green)
    arrow(ax, 16.5, 2.45, 17.2, 2.45, "#6d28d9")
    arrow(ax, 21.4, 2.45, 22.1, 2.45, grey)
    arrow(ax, 23.5, 7.0, 13.7, 4.3, "#6d28d9", ls="--")
    ax.text(19.6, 5.75, "trained $T_\\theta, \\kappa_\\theta$", fontsize=8, color="#6d28d9")
    fig.tight_layout()
    fig.savefig(FIG / "fig_proposed_architecture.pdf", bbox_inches="tight")
    fig.savefig(FIG / "fig_proposed_architecture.png", bbox_inches="tight", dpi=250)
    plt.close(fig)
    print("drew fig_proposed_architecture")


# ---------------------------------------------------------------- 3. image results (faces; git-ignored)
def label(im, text):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        f = ImageFont.load_default()
    d.rectangle([0, 0, im.width, 22], fill="white")
    d.text((6, 3), text, fill="black", font=f)
    return im


def face_figures():
    # (a) SAM outputs and change maps (FG-NET-type photographs; from CVPR_redesign/image_audit)
    src = ROOT / "CVPR_redesign/image_audit/out/sam_change_maps.png"
    if src.exists():
        Image.open(src).convert("RGB").save(FIG / "faces_sam_change_maps.png")
        print("copied faces_sam_change_maps")
    # (b) the SAM sheet itself (original | output x 3 targets, 2 persons)
    sheet = ROOT / "Result_Images/sam_sheet.jpeg"
    if sheet.exists():
        Image.open(sheet).convert("RGB").save(FIG / "faces_sam_sheet.png")
        print("copied faces_sam_sheet")
    # (c) FG-NET all-ages false accepts (children aged 0-4)
    fa = ROOT / "Result_Images/audit_fg_fa.png"
    if fa.exists():
        Image.open(fa).convert("RGB").save(FIG / "faces_fgnet_false_accepts.png")
        print("copied faces_fgnet_false_accepts")
    # (d) MORPH calibration audit sheets written by the pipeline (Look-1 checkpoint): crop selected cells
    cell_w, cell_h, cols = 2 * 112 + 8, 112 + 26, 4

    def cells(path, idx, title):
        im = Image.open(path).convert("RGB")
        crops = [im.crop(((i % cols) * cell_w, (i // cols) * cell_h, (i % cols + 1) * cell_w, (i // cols + 1) * cell_h)) for i in idx]
        row = Image.new("RGB", (len(crops) * (cell_w + 6), cell_h + 24), "white")
        for k, c in enumerate(crops):
            row.paste(c, (k * (cell_w + 6), 24))
        return label(row, title)

    same = ROOT / "Code/AAFV_Net/q/audit/audit_same_bottom50.jpg"
    diff = ROOT / "Code/AAFV_Net/q/audit/audit_different_top50.jpg"
    if same.exists() and diff.exists():
        r1 = cells(same, [21, 0, 5, 7], "(a) Lowest-scoring 'same-person' calibration pairs (left pair: recorded as one person, gap 12 y)")
        r2 = cells(diff, [0, 1, 2, 6], "(b) Highest-scoring 'different-person' calibration pairs (fused P shown)")
        out = Image.new("RGB", (max(r1.width, r2.width), r1.height + r2.height + 8), "white")
        out.paste(r1, (0, 0))
        out.paste(r2, (0, r1.height + 8))
        out.save(FIG / "faces_morph_audit.png")
        print("built faces_morph_audit")


if __name__ == "__main__":
    aafv_figures()
    proposed_architecture()
    face_figures()
