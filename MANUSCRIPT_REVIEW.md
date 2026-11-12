# Full Manuscript Review of `AAFV-02.pdf` (`publication/main.tex`) for IEEE TIFS Submission

**Manuscript Reviewed:** [`publication/main.tex`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/main.tex) (`621` lines; compiled as `AAFV-02.pdf`) & [`publication/references.bib`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/references.bib) (`26` entries)  
**Target Venue:** *IEEE Transactions on Information Forensics and Security* (IEEE TIFS — Signal Processing Society, `punumber=10206`)  
**Ground-Truth Verification Sources:** `Code/AAFV_Net/{configs/params.yaml, src/aafv/*.py, scripts/*.py, q/**, audit/**, baselines/**, ablations/**}`, cross-referenced against Phases 1–4 deliverables ([TIFS_AUTHOR_GUIDELINES.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_AUTHOR_GUIDELINES.md), [TIFS_LITERATURE_AND_STYLE_ANALYSIS.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_LITERATURE_AND_STYLE_ANALYSIS.md), [TIFS_RELATED_WORK_REASSESSMENT.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_RELATED_WORK_REASSESSMENT.md), and [TIFS_NOVELTY_AND_POSITIONING.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_NOVELTY_AND_POSITIONING.md)).  
**Stage:** Phase 5 Deliverable (`Prompt-2.md`)  
**Date:** November 12, 2026

---

## Executive Summary & Severity Triage

While `AAFV-02.pdf` improved layout flow relative to earlier drafts, **our ground-truth audit exposes severe IEEE TIFS format non-compliance, major code-to-text mismatches, corrupted citations, statistical/sample-size misstatements, and visual figure defects** that would trigger Desk Rejection or Major Reject at IEEE TIFS:

1. **Structural / TIFS Format Non-Compliance (Desk-Reject Risk):**
   - Uses `\documentclass[10pt,journal,compsoc]{IEEEtran}` and `\usepackage{caption}` instead of SPS standard `\documentclass[journal]{IEEEtran}` (already flagged in Phase 1).
   - Contains **placeholder author metadata** (`and~Collaborators`, missing ORCIDs, missing institution/city/country, missing TIFS Unified EDICS, missing COI/funding/AI-use statements, missing Deep Learning reproducibility disclosures).
   - Leaves **5 of 7 figures unreferenced** by macro (`fig:architecture`, `fig:results`, `fig:outcomes`, `fig:gap_neutral`, `fig:beta_sweep`).
2. **Code-to-Manuscript Implementation Fictions (Major Scientific Flaws):**
   - **Quality metric $Q$ (line 163):** Manuscript describes landmark symmetry + $\min(Q_1, Q_2)$; actual code ([quality.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/quality.py), [p5_vectors.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p5_vectors.py#L59)) computes the arithmetic mean of 5 normalized image measures (`sharp`, `illum`, `contrast`, `noise`, `detail`) and pair mean $0.5(Q_1+Q_2)$.
   - **SAM aggregation & reliability $R_{\text{sam}}$ (lines 194–202):** Manuscript claims median pooling and $1 - \min(1, 2\operatorname{Var})$; actual code ([pairvec.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairvec.py), [gap.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/gap.py)) uses 5-year snapped grid targets, **z-standardized mean pooling** `0.5*base + 0.5*mean(shared)`, and $R_{\text{sam}} = 0.7 R_{\text{faces}} + 0.3 R_c$.
   - **Fusion vector $\vect{z}$ (line 213):** Manuscript writes wrong element order and 4 zero-padded slots; actual code ([fusion.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/fusion.py#L4)) uses `[W_d, W_s, W_f, g, Q, enhanced_pair, R_sam, R_diff, avail_sam, avail_diff, avail_multi]`.
   - **Guards & Margin formulas (lines 231, 236–238):** Manuscript claims hardcoded $Q_{\min}=0.20, R_{\min}=0.30, \epsilon=10^{-4}$; actual code ([thresholds.json](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/q/thresholds/thresholds.json), [thresholds.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/thresholds.py)) uses empirical 5th percentiles $Q_{\min}=0.2948, R_{\min}=0.3944$, adaptive half-spread margin $\max(0.001, \frac{1}{2}(P_{(1)}-P_{(5)}))$, and strict inequality $P < T_{\text{rej}}$.
3. **Experimental Data, Hash, & Traceability Errors (Integrity Risk):**
   - **`VLM (Qwen2-VL-2B)` in Table I:** Reported inside MORPH `test` ($N=35{,}735$), whereas VLM is absent from [extended_test.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/extended_test.csv) and was only evaluated on the `calibration` common subset (`N_hard = 1,500`, `AUC = 0.906` in [ablation_calibration.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/ablation_calibration.csv)).
   - **Wrong Same-Person Test Size:** Tables I & II and Fig. 2 state $N=1{,}150$ (`1.00%` auto-reject); true MORPH `test` size is **$24{,}305$ same-person pairs** (`0.54%` = `132/24,305` auto-reject, `29.39%` = `7,143/24,305` review).
   - **Wrong Ablation & Table IV Metrics:** `No Shared Targets` had **`0` FAs** on $\mathcal{D}_{\text{hard}}$ (not `4`); `ArcFace (No Guards)` neutral reject is `28.46%` (not `--`); Table IV reports `0.988 / 0.842` instead of `ablation_calibration.csv`'s `0.998 / 0.973`; Table V & Fig. 5 mislabel all age-gap bin ranges (`0–3y...` instead of `0–4y, 5–9y, 10–14y, 15–19y, 20–29y, 30+y`); Table VII sex fairness reports stale numbers (`80.25% vs 77.95%`) instead of Look 1's actual `81.07%` male vs `71.93%` female disparity (`9.14 pp`, ratio `0.887`); Sec. VIII-B claims visual inspection of the 5 test $D_{\text{hard}}$ FAs contradicting [paper.tex](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/paper.tex) line 221; Table VIII reports unverified millisecond/microsecond timing estimates (`14.2 ms`, `58.2 ms`, `0.19 us`, etc.) absent from any profiling code on disk; Look 2 SHA-256 hash (`0fb68e7b`) and Look 1/2 timestamps are incorrect.
4. **BibTeX / Citation Corruption (Verified in Phase 3):** 3 mismatched/false DOIs (`he2019defrcn`, `liu2019dal`, `wang2018oecnn`), 2 author name errors (`huang2021mtlface`, `ricanek2006morph`), 1 unverified monograph (`schuckers2001`), missing NISTIR 8280 demographic reference, and uncited `CosFace`.

---

## Global Pre-Manuscript Metadata & Compliance Audit

| Field (`publication/main.tex` lines 1–43) | Current State | Assessment & Required Action |
|---|---|---|
| Document Class (`line 1`) | `\documentclass[10pt,journal,compsoc]{IEEEtran}` | **NON-COMPLIANT:** Must use `\documentclass[journal]{IEEEtran}` (Signal Processing Society), remove `compsoc`, remove `\usepackage{caption}` (`line 14`), remove `\IEEEtitleabstractindextext` / `\IEEEdisplaynontitleabstractindextext` (`lines 31, 41`), and drop `\IEEEpeerreviewmaketitle` (TIFS is single-blind). |
| Authors (`lines 23–24`) | `Anurag Nayak` and **`and~Collaborators`** | **INCOMPLETE:** Placeholder co-author text (`and Collaborators`) must be replaced by verified co-authors (user-supplied), each with IEEE membership grade and mandatory **ORCID** (`\orcidlink` / `\IEEEauthorblockA`). *We do not invent missing co-authors.* |
| Affiliations & Running Head (`lines 25–29`) | `"Department of Computer Science and Engineering"`, `contact@anuragnayak.dev` | **INCOMPLETE:** Missing University/Institution name, city, state/postal code, country, institutional email (optional), and proper TIFS `\markboth` / `Submitted to IEEE Transactions on Information Forensics and Security`. |
| Funding, COI, Ethics, AI Disclosure (`line 25`) | Generic department line only; no COI/ethics/AI clauses | **MISSING:** Must add formal grant/funding numbers (or "no external funding"), Conflict-of-Interest declaration, dataset ethics/IRB/MORPH-FGNET license compliance statement, and IEEE generative AI editorial disclosure. |
| Unified EDICS | Omitted | **MISSING:** Must specify primary/secondary IEEE SPS EDICS (e.g., `BIO-FACE`, `BIO-AUTH`, `FOR-DATA`) for submission metadata and note in cover letter. |
| Code Repository Link (`line 25`) | `https://github.com/anuragnayak01/AAFV_Net` | **VERIFY:** User must verify that the public repository reflects the final TIFS `publication_tifs/` code and contains no unintended raw MORPH/FG-NET images. |

---

## Section-by-Section Manuscript Evaluation (All 18 Components)

### 1. Title (`main.tex` line 21)
* **What is already good:** Concise (11 words), immediately identifies the subject (`Age-Aware Face Verification`) and core operational theme (`Bounded False-Accept Rate`).
* **What is missing / technically unclear:** Leaves `"Bounded False-Accept Rate"` unqualified, implying a distribution-free or adversarial bound across look-alike and pediatric impostors—despite Look 2 observing `5/35,735` hard impostor FAs and FG-NET observing `4/20,000` pediatric FAs.
* **What should be rewritten:** Scope accurately per Phase 4 Option 1 or Option 2 (e.g., *AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk*).

### 2. Abstract (`main.tex` lines 32–34)
* **What is already good:** Covers problem motivation, dual-branch design, three-way zones, pre-registered Look 1/Look 2 bounds, and external FG-NET transfer.
* **What is missing:** Exceeds the **150–250 word IEEE TIFS limit** (currently `259` raw words / `~273` cleaned words with LaTeX); omits explicit **adult operational age restriction ($a \ge 16$)** and **residual hard-impostor FA (`5/35,735`)**; omits explicit mention of **same-sex bipartite random pairing** on $\mathcal{D}_{\text{random}}$.
* **What is technically unclear / violates rules:** Contains **inline LaTeX math** ($\{\text{Auto-Accept},\dots\}$, $N=1{,}149$, $\text{FAR}\le 0.320\%$, $\beta=1.0\%$), violating IEEE Xplore's plain-text abstract rule (`TIFS_AUTHOR_GUIDELINES.md`); quotes `57.53%` neutral reject instead of verified `57.49%` ([extended_test.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/extended_test.csv)).
* **What should be rewritten:** Compress to ~210–235 plain-text words with zero LaTeX math delimiters, fixed `57.49%`, explicit `>= 16` adult domain, and balanced mention of hard-impostor filtering (`98.04%` reject, `5/35,735` residual FA).

### 3. Index Terms (`main.tex` lines 36–38)
* **What is already good:** Correctly uses `\begin{IEEEkeywords}` and lists 7 relevant descriptors (`Cross-age face verification`, `biometric security`, `generative age synthesis`, `three-way decision`, `reject option`, `bounded false-accept rate`, `Neyman-Pearson lemma`).
* **What is missing / should be refined:** Should align alphabetically with **IEEE Taxonomy / TIFS EDICS** terms (e.g., add `Calibration`, `Face recognition`, `Biometric access control`; reconsider `Neyman-Pearson lemma` since the system implements empirical zero-calibration minimax thresholding with Clopper-Pearson post-test bounds rather than exact likelihood-ratio density estimation).

### 4. Introduction (`main.tex` lines 44–76)
* **What is already good:** Establishes high-assurance motivation (border control, missing persons, asymmetric FA vs. FR cost), introduces Fig. 1 cleanly, and structures 4 clear contributions.
* **What is missing:**
  * **Research gap rigor:** Does not contrast AAFV-Net sharply against existing TIFS threads identified in Phase 2/3—specifically AIFR representation learning (*Wang et al.* 2025, *Huang et al.* 2021), score calibration without abstention bounds (*Xu et al.* 2024), open-set quality uncertainty (*Ahn et al.* 2024), or missing-channel quality fusion (*Poh et al.* 2009).
  * **Pedagogical preview of why deep baselines fail:** Mentions binary threshold flaws in general, but fails to set up the **minimax threshold collapse** empirically observed on uncalibrated Siamese/VLM matchers.
* **What is repetitive / promotional:** Repeats `"zero observed false accepts and a mathematically bounded risk"` across abstract, lines 62, 71, 72 without clarifying *which* impostor distribution (`D_random`) carries the bound vs. `D_hard`. Uses strong adjectives (`fatal vulnerabilities`, `catastrophic`, `comprehensive`, `rigorous`).
* **What should be supported with citations:** Support biometric demographic/NIST evaluation claims with *Grother et al.* (2019 NISTIR 8280) and *Klare et al.* (TIFS 2012); ground quality-aware reject-option fusion in *Poh et al.* (TIFS 2009) and *Ahn et al.* (TIFS 2024).

### 5. Related Work (`main.tex` lines 77–91, audited deeply in Phase 3)
* **What is already good:** Covers three logical pillars: (A) Cross-age recognition & generative aging, (B) Reject-option & calibrated verification, (C) Person-disjoint statistical bounds.
* **What is missing (verified in Phase 3 & [TIFS_RELATED_WORK_REASSESSMENT.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_RELATED_WORK_REASSESSMENT.md)):** Very short (only 3 brief paragraphs, lines 77–91); lacks deep critical synthesis of **recent TIFS papers (2021–2026)** (*Wang et al.* TIFS 2025 AIFR, *Huang et al.* TIFS 2021 PFA-GAN, *Xu et al.* TIFS 2024 confidence calibration, *Ahn et al.* TIFS 2024 quality uncertainty, *Hu et al.* TIFS 2025 Neyman-Pearson, *Poh et al.* TIFS 2009 quality-weighted missing-channel fusion); omits `CosFace` citation (`wang2018cosface`) despite naming it in text (`line 78`).
* **What must be fixed (Citation Bugs):** Corrupted DOIs (`he2019defrcn`, `liu2019dal`, `wang2018oecnn`), author misspellings (`huang2021mtlface`, `ricanek2006morph`), unverified monograph (`schuckers2001`).

### 6. Problem Formulation (`main.tex` lines 92–118)
* **What is already good:** Clean notation for image pair $(I_1, I_2)$ with chronological ages $a_1 \le a_2$, age gap $g = a_2 - a_1$, calibrated probability $P(y=1 \mid \vect{z})$, and explicit piecewise three-way decision rule in eq. (1)–(3) (`lines 103–109`).
* **What is technically unclear / mismatches code:**
  * **Inequality sign in eq. (2):** Manuscript writes Auto-Reject as $P \le T_{\text{rej}}(\beta)$ (`line 107`), whereas [`zone()`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/thresholds.py#L16-L20) executes strict inequality **`p < t_rej`**! Also review condition requires $T_{\text{rej}}(\beta) \le P < T_{\text{acc}}$.
  * **Feature/Normalized age gap mismatch:** Line 95 defines raw years $g = a_2 - a_1$, whereas fusion input `g` in [p5_vectors.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p5_vectors.py#L59) and [gap.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/gap.py#L3-L4) is normalized $\min(1.0, |a_2 - a_1|/80)$! Both symbols need distinct notation (e.g., $\Delta a = |a_2 - a_1|$ in years vs. normalized $g = \min(1, \Delta a / A_{\max})$).
  * **Zero-failure constraint on calibration:** Line 115 describes `Neyman-Pearson` optimization; should clarify accurately that `AAFV-Net` uses an **empirical zero-calibration-FA minimax rule** on guarded impostors rather than continuous density-ratio estimation.

### 7. Statistical Framework (`main.tex` lines 120–151)
* **What is already good:** Clear derivation from Clopper-Pearson exact binomial bound $1 - \alpha^{1/N}$ (`eq:hanley_bound`), Taylor expansion reproducing Hanley's Rule of Three, Bonferroni multi-look adjustment $1 - (\alpha/M)^{1/N}$ giving $0.320\%$ for $N=1{,}149, M=2, \alpha=0.05$, and explicit scope limitation distinguishing $\mathcal{D}_{\text{random}}$ from $\mathcal{D}_{\text{all\_random}}$ and $\mathcal{D}_{\text{hard}}$.
* **What is missing / needs sharpening:**
  * **Proof of i.i.d. validity on $\mathcal{D}_{\text{random}}$:** Line 150 asserts independence on $\mathcal{D}_{\text{random}}$ without explaining *why* (`pairs.d_random` performs **within-sex bipartite 1-to-1 matching without replacement**, guaranteeing every subject appears at most once across $2{,}298$ distinct subjects—harder than cross-sex random pairing).
  * **Clarify correlation in Look 2 & Look 1:** Should explicitly note that Look 1 and Look 2 evaluate two checkpoints on the *same* fixed `test` partition (`correlated tests`), where Bonferroni still conservatively bounds family-wise Type-I error at $\le \alpha$, and that Look 2 evaluated 8 comparative variants simultaneously (without selecting `agg_no_shared_targets` post-hoc).
  * **Citation hygiene:** Use exact Clopper-Pearson DOI `10.1093/biomet/26.4.404` (`clopper1934`).

### 8. Proposed Methodology (`main.tex` lines 152–247)
This section suffers from **the highest density of implementation factual inaccuracies** in the manuscript:
* **What is already good:** Logical 4-stage organization (Preprocessing/5-Score -> Dual Branches -> Fusion MLP & Platt -> Guards & Threshold Calibration) and clean architectural walkthrough matching Fig. 2's overall topology.
* **Critical Code-vs-Text Discrepancies Requiring Rewrite:**
  1. **Face Quality $Q$ (`line 163`):** Wrongly claims *"facial landmark symmetry, sharpness, and illumination consistency; $Q = \min(Q_1, Q_2)$"*. **Actual code** ([quality.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/quality.py), [p5_vectors.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p5_vectors.py#L59)): averages 5 `train_fit` $[5, 95]$-percentile-normalized raw measures (`sharp` = Laplacian variance, `illum` = $1 - |\bar{g}-128|/128$, `contrast` = gray std, `noise` = inverted Immerkær $\sigma$, `detail` = face box side in source px), and pair quality is the **arithmetic mean** $Q = \frac{1}{2}(Q(I_1) + Q(I_2))$.
  2. **SAM Grid Snapping & Aggregation (`lines 194–198`):** Wrongly states forward age $= a_2$, backward $= a_1$, and **median pooling**. **Actual code** ([gap.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/gap.py), [pairvec.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairvec.py)): targets snap to a 5-year age grid (ties rounded up); per-comparison vectors are **z-standardized** on `train_fit`; shared targets are **mean-pooled** across $K_{\text{used}}$ interior grid ages ($a_1 < t < a_2$, uniformly subsampled if $>7$) and blended equally with bidirectional scores: $\vect{s}_{\text{sam}} = 0.5\,\bar{\vect{z}}_{\text{bidir}} + 0.5\,\bar{\vect{z}}_{\text{shared}}$ when $K_{\text{used}} \ge 1$.
  3. **Reliability $R_{\text{sam}}$ Formula (`lines 199–202`):** Wrongly writes $1 - \min(1, 2\operatorname{Var}(\dots))$. **Actual code** ([pairvec.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairvec.py#L40-L55)): $R_{\text{sam}} = 0.7 \sqrt{r_1 r_2} + 0.3\,(1 - \min(1, \text{spread}/\sigma_{\max}))$, combining generated-face quality/age-accuracy/ArcFace-identity preservation ($r_1, r_2$) with ArcFace cosine spread normalized by `train_fit` 95th percentile $\sigma_{\max}$.
  4. **11-D Fusion Vector $\vect{z}$ & Context Columns (`line 213`):** Wrongly writes `[v_d, v_s, g, Q, R_sam, I_sam, I_enhanced, 0,0,0,0]`. **Actual code** ([fusion.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/fusion.py#L4)): `[W_d, W_s, W_f, g, Q, enhanced_pair, R_sam, R_diff, avail_sam, avail_diff, avail_multi]`, where inactive Stage A diffusion branch inputs are `0` (so `W_f` contributes only a learned constant bias scalar; note also **Stage A architecture clarifies why 3 linear heads exist for multi-branch extensibility**).
  5. **Training Protocol Details Missing (`line 217`):** Missing exact Deep Learning training parameters verified in [p6_train.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p6_train.py) & [p6_training_curves.json](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/q/models/p6_training_curves.json): **AdamW**, `train_val` grid search yielding **`lr=3e-3, wd=1e-2`**, batch size `2048`, max `100` epochs, early stopping `patience=10` (`\Delta < 1e-5` unweighted `train_val` log loss; converged at `27–47` epochs across 5 seeds), inverse gap-bin frequency sample weights normalized to mean 1 ([p5_vectors.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p5_vectors.py#L57-L58)), and Platt calibrators fitted per-branch (`P_d, P_s`) and jointly (`P`) on `train_val` ([p78_calibrate_freeze.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p78_calibrate_freeze.py)). Also clarify **calibrated reliability prior-matching check** ([reliability_by_bin.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/audit/reliability_by_bin.csv)).
  6. **Guards & Margin (`lines 231, 236–238`):** Replace fake $Q_{\min}=0.20, R_{\min}=0.30$ with empirical 5th-percentile `train_fit` values (**$Q_{\min}=0.2948, R_{\min}=0.3944$**), and replace $\epsilon=10^{-4}$ with adaptive half-spread margin $\epsilon = \max(0.001, \frac{1}{2}(P_{(1)} - P_{(5)}))$ from [`margin()`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/thresholds.py#L4-L6).
  7. **Broken Figure Reference:** `fig:architecture` (`line 159`) is **never cited** (`\ref{fig:architecture}`) in prose!

### 9. Experimental Setup (`main.tex` lines 248–282)
* **What is already good:** Clearly covers MORPH quarantine (`858` identities = `6.4%`), 60/20/20 person-disjoint splits, FG-NET Adult vs. All-Ages cohorts, four impostor pools (`D_random`, `D_all_random`, `D_hard`, `D_neutral`), and 500-iteration subject-clustered bootstrap.
* **What is missing / misleading:**
  * **Baseline fairness & training details:** Must disclose **exact training budgets and input resolutions** verified in [p11_siamese.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p11_siamese.py), [siamese_cnn/training_log.json](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/baselines/siamese_cnn/training_log.json), [siamese_vit/training_log.json](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/baselines/siamese_vit/training_log.json), and [p11_vlm.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p11_vlm.py):
    * Siamese CNN (`resnet18`, `128x128`, 6 epochs, `bs=128`, stopped epoch 4, `val_logloss=0.1950`);
    * Siamese ViT (`vit_base_patch16_224.augreg_in21k_ft_in1k`, `224x224`, **only `3` epochs** where `val_logloss` was still falling at epoch 2 (`0.1847 -> 0.1593 -> 0.1285`));
    * VLM (`Qwen2-VL-2B-Instruct-bnb-4bit`, `r=16, alpha=16`, `224x224`, `8,000` balanced pairs, **1 epoch**, **never scored on MORPH `test`**—only evaluated on the `5,670`-pair calibration common subset!).
  * **Pair counts omitted:** Does not report calibration (`338,871` total; `23,838` same, `1,170` random, `278,094` all_random, `35,769` hard) vs. test (`339,011` total; **`24,305` same**, `1,149` random, `277,822` all_random, `35,735` hard, plus `2,790` neutral `D_by_both`).
  * **`ArcFace` `0.40` mining threshold (`line 265`) & `D_neutral` clarity:** Clarify that `D_hard` uses `top-k=5` same-gender ArcFace nearest neighbors ([pairs.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairs.py#L70-L88))—verify/avoid unconfirmed `>= 0.40` claim—and specify `D_neutral` as `D_by_both` (`2,790` pairs = overlap/union top-1% mined by Siamese CNN & ViT on test).
  * **Citation fix (`line 281`):** Replace unverified `schuckers2001` with verified *Schuckers* (2010) and *Bolle et al.* (CVIU 2004).
  * **Missing definition of Balanced Automation (`BA`):** `BA` is never defined mathematically anywhere in `main.tex`, despite appearing in Tables IV & VII and Fig. 6! Actual formula in [p10_decision_table.py](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/scripts/p10_decision_table.py#L24) must be explicitly stated (or replaced with clean non-FA-counting balanced coverage if disclosed precisely).

### 10. Results and Comparative Evaluation (`main.tex` lines 283–392)
Contains **critical factual & data integrity errors**:
* **Table I (`tab:main_results` lines 295–311) errors:**
  1. Wrong header sample size `N = 1,150` -> true MORPH test same-person sample size is **`N = 24,305`**.
  2. **`VLM (Qwen2-VL-2B)` row is fabricated as a test result:** VLM has NO test results on disk (`extended_test.csv` has 8 rows only); must be removed from the MORPH `test` table and placed in a calibration-subset table (`N_same=1,500`, `N_hard=1,500`, `AUC=0.906`!).
  3. **`AAFV-Net (No Shared Targets)`:** `D_hard` FA is **`0`** (not `4`), `Hard Rej` = **`97.85%`** (not `97.94%`), `Neutral Rej` = **`53.98%`** (not `54.01%`).
  4. **`ArcFace (No Guards)`:** `Same Accept` = **`93.58%`** (not `93.62%`), `Neutral Rej` = **`28.46%`** (not `--`!).
  5. **Full rounding mismatches:** `Full` Neutral Rej = **`57.49%`** (not `57.53%`); `ArcFace Only` = `89.45%` / `28.46%`; `Direct 5-Score LR` = `87.10%`; `Direct-Only MLP` = `97.77%` / `49.96%`; `Siamese CNN` = `0.21%` / `9.86%`; `Siamese ViT` = `10.04%`.
  6. **Footnote `†` error (`line 309`):** Falsely claims VLM was used to mine Neutral Hard set; in reality VLM was evaluated on calibration `D_by_both` (`8.70%` reject, `N=23`) and omitted from test simply because it was never run on `test`.
* **Table II (`tab:reconciliation` lines 332–359) errors:**
  * Wrong timestamps (`21:42:09 UTC` & `19:45:00 UTC`, not `21:04` & `19:42`), wrong Look 2 `frozen.pkl` SHA-256 (`a47c916b...35b9`, not `0fb68e7b...45cf`), wrong denominators (`917/1,150` vs actual **`19,382/24,305`**; `806/1,150` vs **`17,030/24,305`**; `11/1,150 = 1.00%` vs **`132/24,305 = 0.54%`**; `28.93%` vs **`29.39% (7,143/24,305)`**; `35,035/35,735` vs **`35,034/35,735`**).
* **Table IV (`tab:baseline_ranking` lines 373–389) errors:**
  * `AAFV-Net (Ours)` actually achieved **`AUC = 0.998`** (`0.99809`) and **`TPR @ FPR=1e-3 = 0.973`** (`0.97324`) on calibration `D_hard` (`N=35,769`), NOT `0.988` / `0.842`!
  * Omission: `ArcFace Only` (`AUC = 0.980`, `TPR = 0.969`) is left out despite being the main comparator; VLM's `N=1,500` subset evaluation is mixed seamlessly alongside `N=35,769` models without footnote disclosure!
* **Text / Figure omissions & framing (`lines 315–326, 363–368`):**
  * Unreferenced figures `fig:results` and `fig:outcomes`.
  * Fig. 7 caption omits that it displays **calibration common-subset** outcomes (`decision_table_calibration.csv`, $N_{\text{same}}=1{,}500$), NOT MORPH `test`!
  * Text overclaims *"AAFV-Net occupies the optimal upper-right quadrant"* while ignoring that `ArcFace Only` beats `AAFV-Net` on `D_random` rejection (`47.9% vs 26.2%` on cal subset) and overall acceptance (`89.45% vs 70.07%`), as candidly recorded in [comparison_all.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/comparison_all.md)!

### 11. Ablation Studies (`main.tex` lines 452–506)
* **What is already good:** Covers all 18 meaningful variant groupings from `ablation_calibration.csv`, isolates ArcFace criticality, LPIPS complementarity, `p_mask=0.12` anti-collapse, and `P_d, P_s >= rho` guard necessity.
* **What is missing / inconsistent:**
  * **Header omits dataset identity (`line 457`):** Does not state that Table VII numbers (`74.07%`? Actually `decision_table_calibration.csv` at $\beta=0.01$ shows **`74.13%`**, **`98.20%`**, `0.516`) come from the **5,670-pair calibration common subset** ([results_subset/decision_table_full.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/results_subset/decision_table_full.md)) rather than full `calibration` (`338,871` pairs, where `Full` gives `73.26%` / `98.19%`)! Several table cells show `0.10%`-level mismatches (`Full` `74.07 / 98.24` vs `74.13 / 98.20`; `No Shared Targets` `57.53 -> 54.01` vs test `57.49 -> 53.98`).
  * **Missing exact guard breakdown & RHO difference:** `No Branch Masking` triggered threshold-guard `RHO = 0.35` (`T_acc = 0.593`, [ablation_calibration.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/ablations/ablation_calibration.csv#L17))—worth explaining why masking prevents $T_{\text{acc}}$ shift and collapse! Also clarify `Drop EfficientNet` improved acceptance (`74.13% -> 81.27%`) cleanly—a critical negative/parsimony finding that is ignored in prose!

### 12. Generalization Analysis — Age Gaps & FG-NET (`main.tex` lines 393–451)
Note: Currently sits split awkwardly between Results X-D/E and ablations; should be tightened in sequence.
* **Table V (`tab:gap_analysis` lines 396–410) CRITICAL BUG:**
  * Column headers read **`G1 (0–3y), G2 (4–7y), G3 (8–11y), G4 (12–15y), G5 (16–19y)`**, omitting `G6`.
  * **ACTUAL CODE (`gap.py`, `params.yaml`):** `G1 = 0–4y` (`N=23,631`), `G2 = 5–9y` (`N=266`), `G3 = 10–14y` (`N=184`), `G4 = 15–19y` (`N=75`), `G5 = 20–29y` (`N=137`), `G6 = 30+y` (`N=12`: Full `50.0%` vs ArcFace `100.0%`!). Both Table V and Fig. 5(a) have **false age-range labels** and omit small-$N$ denominators!
* **Table VI (`tab:fgnet` lines 425–445) ERRORS:**
  * Headers `Gap 5–15y` and `Gap >20y` conceal **unweighted 2-bin averages** (`(G2+G3)/2 = (59.55+49.04)/2 = 54.3%`; `(G5+G6)/2 = (28.49+10.26)/2 = 19.4%`) while silently omitting `G4 (15–19y: 38.24% vs 25.88%)`! Should report the exact 6 bins (`<5, 5–9, 10–14, 15–19, 20–29, 30+`) matching `Fig. 3(b)`, with exact sample counts `n=405, 356, 261, 170, 186, 78`!
  * `Impostor Rej.` minor rounding fixes: Adults `55.04%` / `71.28%` (not `55.01%` / `71.30%`); All-Ages `66.45%` / `64.42%` (not `66.42%` / `64.40%`).
  * **Negative result framing:** Must candidly discuss why MORPH test gaps G4–G6 collapse (`1.3%–2.2%`) and why FG-NET Adults has **lower impostor rejection than ArcFace (`55.04% vs 71.28%`)** alongside pediatric failure (`4/20,000` FAs aged `0–4`).
  * **Unverified claim (`line 450`):** Verify if pair names `069A00/023A00` and `019A00/024A00` are logged on disk or inherited from prior notes (`paper.tex` / `missing_experiments.md`) before retaining them!

### 13. Fairness and Demographic Evaluation (`main.tex` lines 507–543)
Contains **two severe scientific integrity violations**:
* **Table VII (`tab:fairness` lines 513–532) STALE / WRONG DATA:**
  * Claims `Male (N=926): 80.25%` vs `Female (N=224): 77.95%` (`\Delta = 2.30 pp`, DI Ratio `0.971`).
  * **ACTUAL GROUND TRUTH ([test_pair_zones_look1.csv](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/q/report/test_pair_zones_look1.csv)):** `N_male = 20,774` (`81.07%` accept, `3/30,921` hard FA, `0/982` random FA) vs `N_female = 3,531` (`71.93%` accept, `0/4,814` hard FA, `0/167` random FA) — a **`9.14` percentage-point disparity (ratio `0.887`)**, and Look 2 did not retain per-pair sex tags!
  * Also **missing race/ethnicity and age-group fairness analysis**—if MORPH race/age fairness is not logged on disk, explicitly report this as a limitation/future audit rather than omitting or guessing; cite *Klare et al.* (TIFS 2012) & *NISTIR 8280* (2019).
* **Section XII-B Unverified Visual Inspection (`line 542`):**
  * Claims visual inspection of the 5 Look-2 test `D_hard` FAs (*"near-identical bone structure, hairline geometry..."*), directly contradicting [paper.tex](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/paper.tex) line 221 (*"which we have not inspected visually"*) with zero test FA contact sheets on disk! Must replace with an honest statement (and audit calibration `audit_different_top50.jpg` separately if inspected, or disclose that visual inspection of Look-2 test FAs was not performed).
* **Unreferenced Figure:** `fig:beta_sweep` (`line 538`) is never cited in prose and sits misplaced inside Section XII (Fairness) instead of Results / Sensitivity Analysis!

### 14. Discussion & Computational Complexity (`main.tex` lines 544–575)
* **Table VIII (`tab:complexity` lines 547–566) Unverified Timing Estimates:**
  * Parameter count **`947`** actually sums the **entire trainable Fusion module** (`3 x Linear(5,1) = 18` + `MLP 11->32->16->1 = 929` = **`947`**), yet Table VIII lists `Linear Branch Learners: 12` separately AND `Fusion MLP: 947`! (Plus Platt scalars `A_d, B_d, A_s, B_s, A_cal, B_cal` = `6` scalars, 5 ensemble seeds = `4,735` trainable weights total).
  * Latency values (`14.2 ms`, `82.5 ms`, `45.1 ms`, `18.4 ms`, `58.2 ms`, `2,140 ms`, `0.19 us`, `0.05 us`) and upstream backbone counts (`65.1 M`, `14.5 M`, `1.2 M`, `30.2 M`) have **no profiling script in `Code/AAFV_Net/`** (`missing_experiments.md` origin only)! Under TIFS integrity rules, unmeasured CPU/GPU timings **must not be presented as measured benchmarks**—either measure fusion CPU latency directly in Python with full hardware disclosure or report exact parameter counts + qualitative bottleneck analysis (SAM StyleGAN forward passes up to `2 + 2K <= 16` per pair).
* **Discussion (`line 574`):** Good operational synthesis of manual-review containment, though `"70.07% high automated throughput"` must be balanced candidly against ArcFace's `89.45%` nominal accept and review-queue cost (`29.39%`). Missing dedicated **calibration reliability discussion** (`audit/reliability_by_bin.csv` shows `< 0.0011` bin error on G1–G3 and sparsity on G5–G6).

### 15. Limitations (`main.tex` lines 576–584)
* **What is already good:** Strong 4-item structure (Random Bound Scope, Pediatric 0–4y Failure, Research Model Licensing, Exhausted 2-Look Budget).
* **What is missing:** Should add **(5) Female Acceptance Disparity (`9.14 pp` in Look 1, unlogged by sex in Look 2) & Absence of Racial Subgroup Audit**, **(6) Generative Compute Latency (`SAM` Multi-Target Grid Overhead)**, and **(7) Baseline Training Horizon Caveat (`ViT 3 epochs`, `VLM calibration-subset-only`)**.

### 16. Conclusion (`main.tex` lines 585–588)
* **What is already good:** Crisp one-paragraph wrap-up restating the three-way formulation and core metrics.
* **What must be rewritten:** Fix `57.53% -> 57.49%`; align title/bound claim (`person-disjoint random impostors` at `0.320%`, acknowledging `5/35,735` residual hard FAs); avoid claiming `"all audited logs"` without noting Look 2 lacks sex tags and VLM was calibration-subset evaluated.

### 17. References (`main.tex` lines 618–619 & `publication/references.bib`)
Verified in Phase 3 ([TIFS_RELATED_WORK_REASSESSMENT.md](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/TIFS_RELATED_WORK_REASSESSMENT.md)):
* **Delete/Replace 3 Corrupted DOIs:** `he2019defrcn` (`10.1109/ICASSP.2019.8683526` is remote-sensing), `liu2019dal` (`10.1145/3343031.3350993` is VQA — use *Wang et al.* CVPR 2019 `10.1109/CVPR.2019.00364`), `wang2018oecnn` (replace with *Yitong Wang et al.* ECCV 2018 `10.1007/978-3-030-01267-0_45`).
* **Fix Author/DOI Metadata:** `huang2021mtlface` (`Zhizhong Huang, Junping Zhang, Hongming Shan`), `ricanek2006morph` (`Karl Ricanek and Tesfa Tesafaye`), `clopper1934` (`10.1093/biomet/26.4.404`), replace `schuckers2001` with `Schuckers 2010` + `Bolle et al. CVIU 2004`.
* **Add Core TIFS Literature & Missing Citations:** `wang2018cosface`, `grother2019frvt_part3` (NISTIR 8280 demographic differentials), *Klare et al.* TIFS 2012, *Paone et al.* TIFS 2014, *Poh et al.* TIFS 2009, *Huang et al.* TIFS 2021 (PFA-GAN), *Xu et al.* TIFS 2024, *Ahn et al.* TIFS 2024, *Hu et al.* TIFS 2025, *Wang et al.* TIFS 2025.

### 18. Appendices & Supplementary Material (`main.tex` lines 589–617 + `publication/supplementary/`)
* **Appendix Table IX (`tab:supp_intervals` lines 595–616) Errors:**
  * Same errors as Table I (`VLM` test claim; `No Shared Targets` / `ArcFace No Guards` `--`; slightly mismatched 95% CIs vs. `extended_test.csv` such as Full `[66.49, 73.08]` vs actual `[66.52, 73.11]` and `[97.68, 98.39]` vs actual `[97.77, 98.31]`).
* **Empty / Missing TIFS Supplementary Material:** `publication/supplementary/` should house: (a) **Calibration Common-Subset Comparison (`N_same=1,500`, including VLM)**, (b) **Full 26-Variant Calibration Table + Bootstrap Confidence Intervals**, (c) **Look-2 FG-NET 6-Bin Detailed Table & Audit Calibration Reliability (`reliability_by_bin.csv`)**, and (d) **IEEE TIFS Deep Learning Reproducibility Checklist** (`seed`, `optimizer`, `lr`, `wd`, `batch size`, epochs stopped, standardizer schema, hash manifest).

---

## Visual Inspection Summary of All 7 Figures (`AAFV-02.pdf` / `publication/figures/*.png`)

| Figure | In-Text Ref? | Ground-Truth Visual & Scientific Defects Observed | Required Phase 7 Action |
|---|---|---|---|
| **Fig. 1 (`fig1_concept.png`)** | Yes (`line 60`) | Panel (b) legend covers `"Auto-Reject Zone"` text and clips `"Manual Review Zone"` text. Note schematic shows $T_{\text{acc}} \approx 0.82$. | Reposition legend outside/below or top-clear without occluding zone headers. |
| **Fig. 2 (`fig2_architecture.png`)** | **NO** | **5 internal text errors:** (1) $Q = \min(Q_1,Q_2)$, symmetry, $Q_{\min}=0.20$; (2) Median target scores, $R_{\min}=0.30$; (3) Wrong $\vect{z}$ vector order; (4) `28.93%` review, `1.00%` auto-reject, `57.53%` neutral (true Look 2: **`29.39%`**, **`0.54%`**, **`57.49%`**); (5) Truncated caption/metrics relative to actual code. | Regenerate cleanly preserving clean layout while fixing all formulas (`mean` pooling, $Q_{\min}=0.2948, R_{\min}=0.3944$, exact Look-2 rates, exact 11-D $\vect{z}$) and add `\ref{fig:architecture}`. |
| **Fig. 3 (`fig3_results.png`)** | **NO** | Literal `(\%)` printed on both x/y axes of Panel (a); legend overlaps `Siamese CNN` & `Siamese ViT` points near `(10, 0)`. Panel (b) accurately shows all 6 FG-NET adult bins `<5..30+`. | Fix LaTeX percent escaping (`%` not `\%`), move legend to center-left/upper-middle clear space, align scatter values to `extended_test.csv`, add `\ref{fig:results}`. |
| **Fig. 4 (`fig4_ablations.png`)** | `line 498` | Legend prints literal `(\%)` twice and overlaps the bottom-right `No Guards` blue bar! | Fix `%` string in legend, move legend cleanly (e.g., upper horizontal strip above axes), verify numbers match `decision_table_calibration.csv`, note calibration common-subset scope. |
| **Fig. 5 (`fig5_gap_neutral.png`)** | **NO** | Panel (a) **mislabels all 5 age-gap x-ticks** (`G1 0-3y .. G5 16-19y` instead of `0-4y, 5-9y, 10-14y, 15-19y, 20-29y`) and drops `G6 (30+y)`. Panel (b) uses slightly off neutral rejection values (`57.53` vs `57.49`). | Fix x-tick bin labels to exact `[0,5), [5,10), [10,15), [15,20), [20,30), 30+`, add `G6`, update neutral reject bars from `extended_test.csv`, add `\ref{fig:gap_neutral}`. |
| **Fig. 6 (`fig6_beta_sweep.png`)** | **NO** | Literal `(\%)` on Panel (a) y-axis; legends overlap `ArcFace Only` curves in **both** panels; x-axis minor log tick `6 x 10^-3` crowds `0.005`. | Clean y-axis label, place shared legend cleanly above subplots, use linear/clean categorical ticks `[0.005, 0.010, 0.020]` without minor-tick clutter, verify whether Look 2 test or calibration sweep is plotted (`extended_test.csv` or `decision_table_calibration.csv`), add `\ref{fig:beta_sweep}`. |
| **Fig. 7 (`fig7_decision_outcomes.png`)** | **NO** | Panel (b) legend completely hides green `Auto-Reject` bars (`10%–12%`) for `Siamese CNN/ViT/VLM`; caption fails to disclose this comes from the **calibration common subset (`N=1,500`)** rather than test. | Move legend outside top above panels, explicitly state calibration common subset + `N` in caption, add `\ref{fig:outcomes}`. |

---

## Unresolved Questions & Decisions Needed Before Stage 6 (`TIFS_REVISION_ROADMAP.md`)

1. **Author List, Affiliations, & ORCID:** Confirm the exact author list (replacing `and~Collaborators`), institutional affiliation(s) with city/country, institutional/contact email, ORCID IDs, and funding/grant disclosures (or confirm "no external grant funding") to insert into `publication_tifs/`.
2. **Preferred Title Scope:** Confirm **Option 1** (*AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk*) vs. **Option 2** (*AAFV-Net: Age-Aware Face Verification With a Calibrated Three-Way Decision Rule and Bounded Random False-Accept Rate*).
3. **Complexity Profiling (Table VIII):** Since disk scripts contain no runtime benchmarking of InsightFace/EfficientNet/VGG/LPIPS/SAM (`14.2 ms ... 58.2 ms`), do you prefer removing unverified hardware timings in favor of **exact verified parameter counts (`947` fusion / component weights) + algorithmic call counts (`<= 16` SAM calls) + real local CPU fusion MLP latency measurement**, or do you have the original GPU profiling logs/hardware spec to cite explicitly?
4. **Target Page Budget:** Target **10 pages** (fee-free IEEE TIFS allowance, moving extended tables/proofs to IEEE Xplore Supplementary PDF) or **12–13 pages** (within 13-page initial submission limit, noting potential overlength fee if accepted >10 pages)?

---

**Phase 5 Status:** **COMPLETE.** Ready to proceed to **Stage 6 (`TIFS_REVISION_ROADMAP.md`)** upon your confirmation.

