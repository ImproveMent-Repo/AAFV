# Prioritized IEEE TIFS Revision Roadmap (`publication_tifs/`)

**Baseline Audited:** `AAFV-02.pdf` / [`publication/main.tex`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/main.tex) (`621` lines) & [`publication/references.bib`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/references.bib) (`26` entries)  
**Target Output Directory (Stage 7):** `publication_tifs/` (`main.tex`, `references.bib`, `figures/`, `tables/`, `supplementary/`, `README.md`)  
**Target Journal:** *IEEE Transactions on Information Forensics and Security* (IEEE TIFS — Signal Processing Society, `punumber=10206`)  
**Stage:** Stage 6 / Phase 6 Deliverable (`Prompt-2.md`)  
**Date:** November 12, 2026

> [!IMPORTANT]
> **Preservation Guarantee:** Original files (`paper.tex`, `Paper/`, `publication/`, `AAFV-01.pdf`, `AAFV-02.pdf`) and all frozen experimental CSVs/checkpoints/hashes in `Code/AAFV_Net/` remain strictly **unmodified**. All Stage 7 rewrites happen exclusively inside the new `publication_tifs/` workspace.

---

## 1. Execution Priority Tiers

To prevent IEEE TIFS desk rejection and eliminate every code-to-manuscript, statistical, visual, and citation flaw uncovered across Phases 1–5, Stage 7 edits are organized into **four priority tiers**:

| Priority Tier | Scope | Objective | Target Files |
|---|---|---|---|
| **P0 — Mandatory Compliance & Citation Integrity** | `IEEEtran` class, abstract format, author/COI/ethics/EDICS metadata, verified BibTeX (`references.bib`) | Prevent immediate SPS desk rejection and purge all corrupted DOIs/authors | `publication_tifs/main.tex`, `publication_tifs/references.bib` |
| **P1 — Code Fidelity & Data Traceability Fixes** | Exact math/code alignment (`quality.py`, `pairvec.py`, `gap.py`, `fusion.py`, `thresholds.py`, `p6_train.py`), Table I–IX ground-truth reconciliation, statistical bound scoping | Ensure 100% traceability between manuscript claims and disk code/CSVs | `publication_tifs/main.tex`, `publication_tifs/tables/*.tex`, `publication_tifs/supplementary/*` |
| **P2 — TIFS Narrative, Literature & Academic Prose** | Section restructuring, 5-theme TIFS Related Work, Deep Learning checklist compliance, negative-result & fairness candor, de-promotionalizing tone | Achieve peer-review rigor expected by TIFS Area Editors | `publication_tifs/main.tex`, `publication_tifs/supplementary/` |
| **P3 — Visual Figures, Layout, & Page Budget** | Regenerating `fig1`–`fig7` from verified CSVs, fixing legend collisions & `(\%)` typos, ensuring 100% `\ref{}` citation, balancing 10–13 page budget | Guarantee publication-grade vector graphics & TIFS page-limit adherence | `publication_tifs/figures/*`, `publication_tifs/README.md` |

---

## 2. Detailed Action Plan by Priority Tier

### P0: IEEE TIFS Format Compliance, Authorship, & Clean Bibliography

1. **LaTeX Preamble & Template Conversion (`publication_tifs/main.tex`):**
   - Replace `\documentclass[10pt,journal,compsoc]{IEEEtran}` with `\documentclass[journal]{IEEEtran}`.
   - Remove `\usepackage{caption}` (restoring native IEEE SPS caption styling and eliminating compiler overrides).
   - Replace Computer Society title macros (`\IEEEtitleabstractindextext`, `\IEEEdisplaynontitleabstractindextext`, `\IEEEpeerreviewmaketitle`) with standard `\maketitle`.
   - Set clean TIFS running header via `\markboth{Submitted to IEEE Transactions on Information Forensics and Security}{...}`.

2. **Title & Plain-Text Abstract:**
   - **Title (Recommended Option 1 unless user specifies Option 2):**  
     *AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk*
   - **Abstract:** Rewrite as a single plain-text paragraph of **185–215 words** (inside IEEE's 150–250 word window), with **zero `$...$` math delimiters, equations, or citations**, explicitly stating:
     - Adult operational domain (`ages >= 16`);
     - Exact same-sex person-disjoint random bound (`0.320%` upper bound at 95% confidence under two-look Bonferroni on `1,149` test pairs);
     - Verified Look 2 test rates (`70.07%` accept, `98.04%` hard-impostor reject with `5` residual hard FAs in `35,735` pairs, `57.49%` neutral hard reject);
     - FG-NET adults zero-retraining transfer (`51.92%` vs. `40.38%` ArcFace, `0/3,670` impostor FAs).
   - **Index Terms:** Alphabetically order IEEE Taxonomy / Unified EDICS terms (`Biometric security`, `Calibration`, `Cross-age face verification`, `Generative age synthesis`, `Reject option`, `Statistical confidence bounds`, `Three-way decision`).

3. **Author Metadata, Disclosures, & Mandatory Statements (Non-Fabricated):**
   - Retain verified first author (`Anurag Nayak`, `Graduate Student Member, IEEE`) and mark co-author/affiliation/ORCID/grant slots cleanly in LaTeX comments + explicit bracketed placeholders (`[CO-AUTHOR FULL NAMES]`, `[DEPARTMENT, INSTITUTION, CITY, COUNTRY]`, `\orcidlink{0000-0000-0000-0000}`) plus document them prominently in `publication_tifs/README.md` so no author identity or grant number is ever invented.
   - Add dedicated **Acknowledgment, Funding, Conflict of Interest, Author Contributions, Biometric Data Ethics & Privacy, Reproducibility, and IEEE Generative AI Disclosure** declarations, plus suggested **Unified EDICS** (`BIO-FACE`, `BIO-AUTH`) documented in `README.md`.

4. **Complete BibTeX Overhaul (`publication_tifs/references.bib`):**
   - **Delete corrupted entry:** `he2019defrcn` (false DOI `10.1109/ICASSP.2019.8683526`).
   - **Correct 6 faulty existing entries:**
     - `wang2019dal` (replace `liu2019dal`; Hao Wang *et al.*, CVPR 2019, `10.1109/CVPR.2019.00364`).
     - `wang2018oecnn` (Yitong Wang *et al.*, ECCV 2018, pp. `764--779`, `10.1007/978-3-030-01267-0_45`).
     - `huang2021mtlface` (`Zhizhong Huang, Junping Zhang, Hongming Shan`, CVPR 2021, `10.1109/CVPR46437.2021.00720`).
     - `ricanek2006morph` (`Karl Ricanek and Tesfa Tesafaye`, FGR 2006, `10.1109/FGR.2006.78`).
     - `clopper1934` (Oxford *Biometrika* DOI `10.1093/biomet/26.4.404`).
     - Replace unverified `schuckers2001` with verified `bolle2004subsets` (*CVIU* 2004, `10.1016/j.cviu.2003.08.002`) and `schuckers2010book` (Springer 2010, `10.1007/978-1-84996-202-5`).
   - **Add missing cited/essential works (all DOIs verified in Phases 2–3 & Step 6 prep):**
     - `wang2018cosface` (Hao Wang *et al.*, CVPR 2018, `10.1109/CVPR.2018.00552`);
     - `zhang2017caae` (CVPR 2017, `10.1109/CVPR.2017.463`), `tang2018ipcgan` (CVPR 2018, `10.1109/CVPR.2018.00828`);
     - `grother2019frvt_part3` (NISTIR 8280, `10.6028/NIST.IR.8280`), `bestrowden2018longitudinal` (TPAMI 2018, `10.1109/TPAMI.2017.2652466`);
     - **Verified IEEE TIFS Corpus:** `poh2009quality` (`10.1109/TIFS.2009.2034885`), `li2011aifr` (`10.1109/TIFS.2011.2156787`), `klare2012demographics` (`10.1109/TIFS.2012.2214212`), `paone2014twins` (`10.1109/TIFS.2013.2296373`), `huang2021pfagan` (`10.1109/TIFS.2020.3047753`), `xu2024asc` (`10.1109/TIFS.2023.3318957`), `ahn2024ucface` (`10.1109/TIFS.2024.3426973`), `otroshi2024inversion` (`10.1109/TIFS.2024.3381820`), `osorioroig2024indexing` (`10.1109/TIFS.2024.3386310`), `hu2025neyman` (`10.1109/TIFS.2024.3515834`), `wang2025ordcon` (`10.1109/TIFS.2025.3597187`).
   - Standardize all journal/conference titles to IEEE abbreviations (`IEEE Trans. Inf. Forensics Security`, `Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)`).

---

### P1: Implementation Fidelity, Mathematical Rigor, & Data Reconciliation

| Manuscript Target | Current Error in `publication/main.tex` | Ground-Truth Revision in `publication_tifs/` |
|---|---|---|
| **Problem Formulation (Eq. 1–3)** | Uses $P \le T_{\text{rej}}(\beta)$ and overloads $g = a_2 - a_1$ (years) with fusion input $g \in [0, 1]$. | Enforce strict `P < T_rej` matching [`thresholds.py`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/thresholds.py#L19); distinguish $\Delta a = |a_2 - a_1|$ (years) from normalized $g = \min(1, \Delta a / 80)$; frame thresholding accurately as **empirical zero-calibration-FA minimax thresholding** rather than density-ratio Neyman-Pearson. |
| **Statistical Framework** | Asserts $\mathcal{D}_{\text{random}}$ independence without showing construction; fails to clarify Look 1 vs Look 2 same-test correlation. | Prove i.i.d. validity via [`pairs.d_random`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairs.py#L26-L39) (within-sex bipartite 1-to-1 matching without replacement across $2{,}298$ unique subjects); state why $\mathcal{D}_{\text{all\_random}}$ ($10^{-5}$ heuristic column in CSV), $\mathcal{D}_{\text{hard}}$, and FG-NET ($0/3{,}670$) do **not** yield valid i.i.d. binomial bounds; document Look 2 simultaneous evaluation of 8 comparative variants alongside retained pre-registered `full`. |
| **Face Quality $Q$** | Claims landmark symmetry + $\min(Q_1, Q_2)$ + $Q_{\min}=0.20$. | Write exact [`quality.py`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/quality.py) formula: 5 `train_fit` $[5,95]$-percentile-normalized measures (`sharp`, `illum`, `contrast`, `noise`, `detail`), pair **mean** $Q = \frac{1}{2}(Q_1 + Q_2)$, and `train_fit` 5th-percentile cutoff $Q_{\min}=0.2948$. |
| **SAM Branch & $R_{\text{sam}}$** | Claims un-snapped target ages, *median* pooling, $R_{\text{sam}} = 1 - \min(1, 2\operatorname{Var})$, and $R_{\min}=0.30$. | Write exact [`gap.py`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/gap.py) 5-year snapped grid targets, z-standardization (`train_fit`), **mean** shared pooling `0.5*base + 0.5*mean(shared)`, exact [`pairvec.reliability`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairvec.py#L46-L55) formula ($0.7\sqrt{r_1 r_2} + 0.3 R_c$ using `sigma_max`), and `train_fit` 5th-percentile $R_{\min}=0.3944$. |
| **Fusion Vector $\vect{z}$ & Margin** | Wrong vector order `[v_d, v_s, g, ... 0,0,0,0]`, hardcoded $\epsilon = 10^{-4}$, missing DL specs. | Exact [`fusion.py`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/fusion.py) 11-D input `[W_d, W_s, W_f, g, Q, enhanced_pair, R_sam, R_diff, avail_sam, avail_diff, avail_multi]` (explaining Stage A inactive `W_f` bias slot); exact adaptive margin $\max(0.001, \frac{1}{2}(P_{(1)}-P_{(5)}))$; full Deep Learning hyperparameter table (`AdamW`, `lr=3e-3, wd=1e-2`, `bs=2048`, `patience=10`, early stopping epochs `27–47`, inverse-bin sample weighting, `reliability_by_bin.csv` check). |
| **Table I & Appendix Table IX** | `N=1,150`, fabricated `VLM` test row, `No Shared Targets` `D_hard_FA=4`, wrong `ArcFace No Guards` (`--`), rounding errors, wrong footnote `†`. | Fix `N = 24,305`; **remove VLM from MORPH `test` Table I** and place it in a clean **Calibration Common-Subset Table** (`N_same=1,500`, `N_hard=1,500`); update every single number & 95% cluster CI verbatim from [extended_test.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/extended_test.csv) (`Full: 70.07% / 98.04% / 57.49%`; `No Shared: 83.91% / 0 FA / 97.85% / 53.98%`; `ArcFace No Guards: 93.58% / 28.46%`); fix `†` footnote accurately. |
| **Table II (Reconciliation)** | Wrong timestamps (`21:04`, `19:42`), wrong Look 2 hash (`0fb68e7b`), wrong `1,150` counts & `1.00%`/`28.93%` rates. | Exact [`test_access.log`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/q/logs/test_access.log) timestamps (`21:42:09 UTC`, `19:45:00 UTC`), [`ablation_freeze.json`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/ablation_freeze.json) hash `a47c916b...35b9`, and exact counts (`19,382/24,305`, `17,030/24,305`, `7,143/24,305 = 29.39%`, `132/24,305 = 0.54%`, `35,034/35,735`). |
| **Table IV (Ranking Quality)** | Reports `AAFV-Net` `0.988 / 0.842`, omits `ArcFace Only`, mixes `N=1,500` VLM seamlessly. | Report verified calibration `D_hard` ranking metrics from [`ablation_calibration.csv`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/ablation_calibration.csv): `AAFV-Net` (`AUC=0.998, TPR@1e-3=0.973`), `ArcFace Only` (`AUC=0.980, TPR=0.969`), `Siamese ViT` (`0.972, 0.605`), `Siamese CNN` (`0.953, 0.311`), `VLM` (`0.906, 0.054` flagged as `N=1,500` subset). Define `BA` formula or replace with unambiguous mean automation/accuracy breakdown. |
| **Table V (Age-Gap Strata)** | Mislabels bins `0–3y..16–19y` and drops `G6`. | Label exact bins `G1 (0–4y, N=23,631)`, `G2 (5–9y, N=266)`, `G3 (10–14y, N=184)`, `G4 (15–19y, N=75)`, `G5 (20–29y, N=137)`, and `G6 (30+y, N=12)` cleanly with exact `extended_test.csv` percentages and candid G4–G6 collapse discussion. |
| **Table VI (FG-NET)** | Unweighted 2-bin averages (`5–15y`, `>20y`) hiding `G4`, minor rounding mismatches (`55.01%` vs `55.04%`). | Present all 6 exact bins (`<5, 5–9, 10–14, 15–19, 20–29, 30+`) with sample sizes (`405..78`), exact `extended_calibration_fg16.csv` / `fg.csv` rates (`55.04%` / `71.28%`, `66.45%` / `64.42%`), and check/scrub unverified pair IDs (`069A00` etc.) if not confirmed on disk. |
| **Table VII (Fairness) & Visual Audit** | Stale `926/224` (`2.30 pp`) numbers + fabricated Look 2 `D_hard` FA visual inspection. | Report verified Look 1 test sex breakdown from [`test_pair_zones_look1.csv`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/q/report/test_pair_zones_look1.csv) (`Male 20,774: 81.07%` vs `Female 3,531: 71.93%`, `9.14 pp` gap, ratio `0.887`, `0` random FAs in both sexes), disclose Look 2 lacked sex tags & race metadata audit, and replace fabricated visual-inspection prose with honest non-inspection disclosure. |
| **Table VIII (Complexity)** | Double-counts `947` params vs `12` linear params; prints unmeasured CPU/GPU ms/$\mu\text{s}$ timings. | Fix exact parameter decomposition (`18` linear + `929` MLP = `947` per seed; `4,735` across 5 seeds + `6` Platt scalars), remove unverified hardware timing numbers, report algorithmic call bounds (`<= 16` SAM forward passes/pair + cascaded gating rate), and optionally run a local CPU benchmark exclusively for the `Fusion` MLP if cleanly reproducible (explicitly hardware-scoped). |

---

### P2: Section Restructuring, Academic Tone, & TIFS Literature Depth

1. **Logical TIFS Organization (`11.5–12.5` initial pages, safely $\le 13$-page cap):**
   - **I. Introduction:** Sharpen TIFS gap via 3-way abstention, quality-weighted fusion, and minimax collapse under zero-calibration-FA; remove promotional adjectives; fix `fig:concept` framing.
   - **II. Related Work (Expanded 5-Theme Synthesis):** Restructure into **II-A Cross-Age AIFR**, **II-B Generative Aging & Counterfactual Skepticism**, **II-C Quality-Dependent Multi-Metric Fusion & Calibration**, **II-D Reject-Option & Bounded Biometric Risk**, **II-E Look-Alikes, OOD Shifts & Demographic Fairness**, tightly weaving in 12–14 verified TIFS papers.
   - **III. Problem Formulation & Three-Way Decision Rule** (tight math + strict `< T_rej` + normalized `g`).
   - **IV. Statistical Risk Framework** (Clopper-Pearson, bipartite `D_random` independence proof, correlated Look 1/Look 2 Bonferroni bound, explicit scope exclusions).
   - **V. Proposed Methodology (`AAFV-Net`)** (accurate `quality.py`, `gap.py`, `pairvec.py`, `fusion.py`, `p6_train.py`, `thresholds.py`, `calib.py`, `reliability_by_bin.csv`, `fig:architecture`).
   - **VI. Experimental Setup & Protocols** (MORPH quarantine, splits, 4 test pools, baseline training budgets & fair caveats, cluster bootstrap).
   - **VII. Comparative Results, Calibration Subset, & Reconciliation** (Table I fixed MORPH `test` + separate Calibration Common-Subset table w/ VLM, Table II reconciliation, Table IV ranking quality, $\beta$-sensitivity via `fig:beta_sweep`, `fig:results`, `fig:outcomes`).
   - **VIII. Longitudinal Generalization & Component Ablations** (Table V 6-bin MORPH + FG-NET Adults/All-Ages 6-bin evaluation, `fig:gap_neutral`, Table VII subset ablations + `fig:ablations`, parsimony note on `Drop EfficientNet` and `RHO=0.35` on `No Branch Masking`).
   - **IX. Demographic Fairness, Complexity, & Ethical Scope** (Verified Look 1 sex parity `9.14 pp`, missing race audit disclosure, accurate parameter/call complexity, pediatric $a < 16$ safety boundary, licensing, Biometric Ethics & AI disclosures).
   - **X. Discussion, Limitations, & Conclusion** (Candid trade-off synthesis acknowledging `ArcFace` wins nominal throughput & random rejection, 7 transparent limitations, factual conclusion).
   - **References** & **Appendix A** (Complete verified Look 2 MORPH `test` 95% cluster CIs from `extended_test.csv`).

---

### P3: Regenerated Publication Figures & Standalone Supplementary Artifacts

1. **New Generator Script (`publication_tifs/scripts/generate_tifs_figures.py`):**
   - Reads directly from verified CSVs (`Code/AAFV_Net/ablations/extended_test.csv`, `decision_table_calibration.csv`, `extended_calibration_fg16.csv`)—zero hardcoded hand-typed plot arrays where CSVs exist.
   - Fixes every defect verified in Phase 5:
     - **`fig1_concept`:** Clean non-overlapping legend outside/above zones.
     - **`fig2_architecture`:** Exact code formulas (`mean` quality $0.5(Q_1+Q_2)$, $Q_{\min}=0.2948$, 5-yr grid **mean** pooling, $R_{\text{sam}}=0.7\sqrt{r_1 r_2}+0.3 R_c$, $R_{\min}=0.3944$, exact 11-D $\vect{z}$ order, Look 2 verified `70.07% / 29.39% / 0.54%` & `57.49%` neutral).
     - **`fig3_results`:** Remove `(\%)`, clear legend away from Siamese CNN/ViT markers, sync points to `extended_test.csv`.
     - **`fig4_ablations`:** Remove `(\%)`, move legend to top horizontal bar outside plot area, match `decision_table_calibration.csv` and caption calibration-subset scope.
     - **`fig5_gap_neutral`:** Fix x-axis ticks to **`G1 (0–4y) ... G6 (30+y)`** matching `extended_test.csv`, update neutral reject bars (`57.49%` etc.).
     - **`fig6_beta_sweep`:** Remove `(\%)`, clean linear ticks `[0.005, 0.010, 0.020]`, top shared legend, plot verified `extended_test.csv` or `decision_table_calibration.csv` with explicit split label.
     - **`fig7_decision_outcomes`:** Move legend above subplots so green `Auto-Reject` bars (`10%–12%`) are 100% visible, and specify calibration common-subset scope (`N=1,500`) in caption.
   - Ensure **all 7 figures** (`fig:concept`..`fig:outcomes`) and **all tables** are explicitly `\ref{}`-referenced in prose and export vector `.pdf` + 300-DPI `.png`.

2. **Supplementary Package (`publication_tifs/supplementary/`):**
   - `TIFS_Supplementary.tex` / `.pdf` (excluded from the 10/13-page count):
     - Full 26-variant `ablation_calibration.csv` + calibration `decision_table_calibration.csv` across $\beta \in \{0.005, 0.01, 0.02\}$;
     - Full FG-NET 6-bin Adult & All-Ages tables with 95% cluster CIs;
     - Calibration bin-wise prior-matching reliability table (`audit/reliability_by_bin.csv`);
     - IEEE TIFS Deep Learning Reproducibility Checklist & SHA-256 Artifact Manifest (`thresholds.json`, `frozen.pkl`, `ablation_freeze.json`).

---

## 3. Target Workspace Layout (`publication_tifs/`)

```text
publication_tifs/
├── IEEEtran.cls                       # Official IEEEtran class (from publication/)
├── IEEEtran.bst                       # Official IEEEtran bibliography style
├── main.tex                           # Complete TIFS-aligned journal manuscript
├── main.pdf                           # Compiled validated double-column PDF (Stage 8)
├── references.bib                     # Verified & standardized IEEE TIFS BibTeX
├── figures/                           # Clean vector PDFs + 300-DPI PNGs (fig1..fig7)
├── tables/                            # Clean modular LaTeX tables
├── scripts/generate_tifs_figures.py   # Reproducible figure generator reading frozen CSVs
├── supplementary/                     # TIFS Supplementary Material & DL Checklist PDF/LaTeX
└── README.md                          # Reproducibility, checksums, EDICS & author-slot guide
```

---

## 4. Decisions Carried Into Stage 7 (Proceeding with TIFS Best-Practice Defaults Unless Overridden)

Before writing `publication_tifs/`, please confirm (or tell me `"proceed with defaults"`):
1. **Title Choice:** Use **Option 1** (*AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk*)?
2. **Complexity Profiling (Table VIII):** Remove unverified millisecond timings (`14.2 ms ... 58.2 ms`, `0.19 us`) in favor of exact verified parameter counts (`947` per-seed fusion / upstream backbones) + algorithmic call counts (`<= 16` SAM passes/pair) + optionally benchmark real CPU wall-clock inference of the `947`-parameter PyTorch fusion module?
3. **Author / Institution Metadata:** Leave transparent `[CO-AUTHOR / INSTITUTION / ORCID / GRANT]` placeholders documented in `README.md` for your final fill-in prior to portal upload, or supply real co-author details right now?
4. **Page Budget:** Target **11–12.5 pages** for initial TIFS submission (strictly $\le 13$-page cap, comprehensive TIFS rigor) with extended 26-variant logs in `supplementary/` (providing easy trimming path to $\le 10$ pages if avoiding overlength fees at camera-ready)?

---

**Stage 6 Status:** **COMPLETE.** Ready to execute **Stage 7 — Revise Manuscript & Build `publication_tifs/`** upon your confirmation.

