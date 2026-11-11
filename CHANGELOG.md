# Changelog: AAFV-Net Manuscript Visual & Formatting Corrections (v2)

**Document:** AAFV-Net IEEE Research Manuscript  
**Target Venue:** IEEE Transactions on Information Forensics and Security (T-IFS) / IEEE Transactions on Biometrics, Identity and Behavior (T-BIOM)  
**Output Artifact:** `AAFV-02.pdf` (generated from `publication/main.tex`)  
**Date:** November 11, 2026  
**Reference Prompt:** `prompt-1.md`

---

## 1. Overview of Changes

In strict accordance with the instructions in `prompt-1.md`, targeted visual and formatting corrections were executed without modifying the underlying scientific methodology, experimental results, thresholds, citations, or research contributions.

The two targeted issues resolved:
1. **ISSUE 1:** Redesign of the complete Architecture Diagram (Page 4, Figure 2).
2. **ISSUE 2:** Elimination of Table Overflow on Page 6, Table 1.

---

## 2. Issue 1: Architecture Diagram Redesign (Figure 2)

### Problems Identified in Initial Draft (`fig2_architecture.pdf` in `AAFV-01.pdf`):
- Diagonal arrows intersected module boundaries, passed through intermediate boxes (e.g., Face Quality to Fusion passing through SAM branches), and created visual ambiguity regarding data flow.
- Lack of distinct visual stages made the five-phase processing pipeline difficult to parse.

### Solutions & Modifications Implemented:
1. **Clean 5-Stage Left-to-Right Organization:**
   - **Stage 1 (Input):** Aligned Input Photo Pair ($I_1, I_2$, gap $g = a_2 - a_1$) and Face Quality Module ($Q = \min(Q_1, Q_2)$, landmarks, sharpness, $Q \ge 0.20$ guard).
   - **Stage 2 (Evidence Extraction):** Direct Evidence Branch (5-score extraction: ArcFace, EfficientNet, VGG, LPIPS, SSIM) and SAM Aging Branch (bidirectional $I_1 \to a_2, I_2 \to a_1$, $K \le 7$ shared target grids, reliability $R_{\text{sam}}$, $R_{\text{sam}} \ge 0.30$ guard).
   - **Stage 3 (Feature Processing):** Direct Linear Learner ($W_d \in \mathbb{R}^5 \to v_d, P_d \ge 0.20$) and SAM Linear Learner ($W_s \in \mathbb{R}^5 \to v_s, p_{\text{mask}}=0.12, P_s \ge 0.20$).
   - **Stage 4 (Fusion & Calibration):** 11-D Calibrated Fusion Vector $\mathbf{z} \in \mathbb{R}^{11}$, Multimodal Fusion MLP ($11 \to 32 \to 16 \to 1$, 5 seeds), and Platt Calibration ($P \in [0, 1]$).
   - **Stage 5 (Three-Way Decision):** Auto-Accept ($P \ge 0.9564 \land \text{GuardsPass}$), Manual Review ($T_{\text{rej}} < P < T_{\text{acc}} \lor \neg \text{GuardsPass}$), and Auto-Reject ($P \le 0.0075$).
2. **Strictly Orthogonal Arrow Routing:**
   - All connection segments are exclusively horizontal or vertical.
   - Zero arrows pass through any module box or label.
   - Arrows connect strictly to outer box boundaries with clearly directed arrowheads (`-|>`).
3. **Dedicated Context Bypass Lanes:**
   - **Upper Bypass Lane:** Routes age gap $g = a_2 - a_1$ from the top of the Input Pair box above Stage 2 and Stage 3 directly into the top of the Calibrated Fusion Vector box.
   - **Lower Bypass Lane:** Routes face quality $Q(I_1, I_2)$ from the bottom of the Quality Module beneath Stage 2 and Stage 3 directly into the bottom of the Calibrated Fusion Vector box.
4. **Distribution Tree for Decisions:**
   - Calibrated posterior $P$ exits Stage 4 to a vertical distribution bus at $x=84.2$, branching orthogonally into the three color-coded decision outcomes (Green: Auto-Accept, Amber: Manual Review, Red: Auto-Reject).
5. **Technical Preservation:**
   - All mathematical symbols, thresholds ($0.9564, 0.0075$), parameter counts, guards, dropout rates, and operating metrics were 100% retained.
   - Vector graphics output generated and saved in `publication/figures/fig2_architecture.pdf` (and 300-DPI raster in `.png`).

---

## 3. Issue 2: Table 1 Formatting & Overflow Resolution

### Problems Identified in Initial Draft (Table 1 in `AAFV-01.pdf`):
- Table 1 exceeded the IEEE text margin by 69.7 points due to wide parenthesized confidence intervals and verbose fractions (`0 / 1,149`, `0 / 277,822`, `5 / 35,735`).

### Solutions & Modifications Implemented:
1. **Point Estimates in Table 1:**
   - Removed parenthesized 95% confidence intervals from all cells in Table 1 (e.g., `70.07 (66.49–73.08)` $\to$ `70.07`, `98.04 (97.68–98.39)` $\to$ `98.04`, `57.53 (55.34–59.73)` $\to$ `57.53`).
2. **Sample Sizes Moved to Column Headers:**
   - Column 1: `Method`
   - Column 2: `\makecell{Same-Person\\Auto-Accept (\%)\\\small ($N = 1{,}150$)}`
   - Column 3: `\makecell{Random FA\\$\mathcal{D}_{\text{random}}$\\\small ($N = 1{,}149$)}`
   - Column 4: `\makecell{All-Random FA\\$\mathcal{D}_{\text{all\_random}}$\\\small ($N = 277{,}822$)}`
   - Column 5: `\makecell{Hard FA\\$\mathcal{D}_{\text{hard}}$\\\small ($N = 35{,}735$)}`
   - Column 6: `\makecell{Hard Auto-Reject\\(\%)\\\small ($N = 35{,}735$)}`
   - Column 7: `\makecell{Neutral Auto-Reject\\(\%)\\\small ($N = 2{,}790$)}`
3. **Denominators Removed from False-Accept Cells:**
   - Replaced verbose fractions with exact observed false-accept counts (`0`, `0`, `5`), as sample sizes are now explicitly stated in the column headers.
4. **Preservation of Statistical Transparency (Appendix Table IX):**
   - Added `\appendices` section in `publication/main.tex` containing **Table IX (`tab:supp_intervals`)**, preserving all original 95% identity-clustered bootstrap confidence intervals for all models, metrics, and splits.
   - Linked Table 1 caption and Section VI-A text directly to Appendix Table IX.
5. **Layout Compliance:**
   - Configured `\footnotesize`, `\setlength{\tabcolsep}{4.5pt}`, and `\resizebox{\textwidth}{!}{...}`, completely eliminating the 69.7 pt overfull hbox.
   - The entire table spans exactly across the two-column page width without clipping or overflowing.

---

## 4. Verification and Build Artifacts

1. **Compilation Status:**
   - Compiler: MiKTeX `pdflatex` + `bibtex` toolchain.
   - Exit Code: `0` (Success).
   - Total Pages: Exactly 10 pages.
   - Broken References: `0`.
   - Undefined Citations: `0`.
   - Fatal Overfull/Underfull Boxes: `0`.
2. **Deliverable PDF:**
   - `AAFV-02.pdf` (788.5 KB) generated in root directory and `publication/AAFV-02.pdf`.
3. **Modified Source Files:**
   - `publication/main.tex` (Updated Table 1, Table 5, Appendix Table IX, package imports, figure width).
   - `scripts/generate_publication_figures.py` (Integrated redesigned Figure 2 generator).
   - `scripts/test_fig2_redesign.py` (Standalone verification script for Figure 2).
   - `publication/figures/fig2_architecture.pdf` & `.png` (Regenerated vector and raster diagram).
   - `CHANGELOG.md` (This document).

