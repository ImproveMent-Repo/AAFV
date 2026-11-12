# Research Positioning, Novelty Audit, and Statistical Integrity Assessment (`AAFV-Net` for *IEEE TIFS*)

**Prepared For:** Alignment of *AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate*  
**Target Venue:** *IEEE Transactions on Information Forensics and Security* (TIFS)  
**Audited Code & Artifacts:** `src/aafv/{pairs.py, thresholds.py, calib.py, evaluation.py}`, `scripts/{p3_build_pairs.py, p78_calibrate_freeze.py, p9_test.py, p12_extended.py}`, `q/thresholds/thresholds.json`, `q/logs/test_access.log`, `q/report/test_pair_zones_look1.csv`, `ablations/{ablation_freeze.json, extended_test.csv}`, and [`publication/main.tex`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/main.tex)  
**Stage:** Phase 4 Deliverable (`Prompt-2.md`)  
**Date:** November 12, 2026

---

## 1. Honest Component-by-Component Novelty Deconstruction

In accordance with TIFS reviewing standards (`Prompt-2.md` line 302: *"Do not describe existing techniques as novel simply because they are combined in our framework"*), we strictly separate inherited building blocks from AAFV-Net's defensible innovations across the 12 core elements of the system:

| Pipeline Element | Underlying Precedent in Literature | Verdict: Novel or Existing? | Specific Delta / Defensible Claim for TIFS |
|---|---|---|---|
| **Direct facial evidence (5 metrics)** | ArcFace (`deng2019arcface`), VGG-Face (`parkhi2015vgg`), EfficientNet (`tan2019efficientnet`), LPIPS (`zhang2018lpips`), SSIM (`wang2004ssim`) | **Existing components** | Combining heterogeneous metrics is standard score fusion; **not claimed as algorithmically novel**. Ablations prove ArcFace + LPIPS supply nearly all discriminative lift while EfficientNet is redundant. |
| **SAM bidirectional transformation** | StyleGAN2 latent age regression (`alaluf2021sam`); prior progressive cGAN aging (`huang2021mtlface`, *PFA-GAN* TIFS 2021) | **Existing generator** | AAFV-Net treats SAM strictly as a **frozen noisy counterfactual sensor** conditioned on source/target ages rather than trusting synthesized images directly as identity-preserving replacements. |
| **Shared-target age comparisons ($K \le 7$)** | 5-year canonical progression grids comparing $(\hat{I}_1^{(t_k)}, \hat{I}_2^{(t_k)})$ | **Domain-specific engineering design** | Empirically introduces an **acceptance-vs.-robustness trade-off**: removing shared targets raises MORPH test accept ($70.07\% \to 83.91\%$) while lowering neutral hard rejection ($57.49\% \to 53.98\%$). |
| **Reliability-aware fusion ($R_{\text{sam}}$ + $p_{\text{mask}}=0.12$)** | Quality-dependent & missing-channel biometric fusion (**Poh *et al.*, TIFS 2009**); quality uncertainty embeddings (**Ahn *et al.*, TIFS 2024**) | **Targeted adaptation** | Adapts Poh *et al.*'s multi-sensor quality & channel-dropout framework to single-face longitudinal verification, using inter-target cosine variance ($R_{\text{sam}}$) and runtime SAM masking ($p_{\text{mask}}=0.12$). |
| **Calibrated Fusion MLP ($11 \to 32 \to 16 \to 1$)** | Platt scaling (`platt1999`), confidence calibration (**Xu *et al.*, TIFS 2024**) | **Existing calibration method** | Parameter-efficient fusion (947 params, $0.19\ \mu\text{s}$ CPU) is an engineering advantage; **not novel ML theory**. |
| **Quality & Branch Probability Guards ($Q, R_{\text{sam}}, P_d, P_s$)** | Quality thresholding (`Poh et al., TIFS 2009`) | **Architectural safeguard (Critical Empirical Role)** | **Key empirical mechanism:** Without $\rho = 0.20$ branch probability floors, calibration outliers force $T_{\text{acc}} > 1.0$, collapsing auto-accept to $0.00\%$ (Table VI). |
| **Three-Way Decisions (`Accept/Review/Reject`)** | Chow's reject-option theory (`chow1970reject`) | **Known statistical theory** | Novelty is in the **asymmetric biometric operationalization**: fixing $T_{\text{acc}}$ for minimax zero calibration FA under guards while sweeping quantile $T_{\text{rej}}(\beta)$ for hard-impostor absorption. |
| **Frozen SHA-256 Thresholds & Logged Access** | Pre-registration / locked test evaluation protocols | **Methodological / Engineering rigor** | Prevents post-hoc threshold snooping via cryptographic hash checks (`thresholds.sha256`, `ablation_freeze.json`) and explicit look accounting (`test_access.log`, `LOOKS_MAX=2`). |
| **Statistically Bounded FAR ($1 - (\alpha/M)^{1/N}$)** | Clopper-Pearson (`clopper1934`), Rule of Three (`hanley1983rule3`), Neyman-Pearson detection (**Hu *et al.*, TIFS 2025**) | **Rigorous statistical application (Not new theorem)** | Distinguishing factor is **exact bipartite person-disjoint sampling (`pairs.d_random`)** + Bonferroni multi-look adjustment—avoiding invalid i.i.d. claims on correlated grids (`D_all_random`). |
| **Person-Disjoint & Quarantine Audit** | Subject-disjoint biometric protocols (`Klare et al. TIFS 2012`, `Schuckers 2010`) | **Strict data hygiene protocol** | Identifies and quarantines 858 corrupted/merged identities (6.4% of MORPH) prior to splitting and prevents identity leakage across splits. |
| **Random + Neutral Hard-Impostor Testing** | Hard/twin impostor stress testing (**Paone *et al.*, TIFS 2014**) | **Experimental protocol contribution** | Evaluates unbiased **model-neutral** top-1% hard impostors mined independently by Siamese ViT/CNN (`D_by_both`), eliminating circular mining bias against ArcFace. |

---

## 2. Six-Category Classification of Actual Contributions (TIFS-Defensible)

1. **Novel Methodology (Scoped):** A hedged dual-branch verification methodology that treats StyleGAN age synthesis (`SAM`) as an unreliable counterfactual channel—quantifying inter-target consistency ($R_{\text{sam}}$), training under stochastic branch masking ($p_{\text{mask}}=0.12$), and gating final acceptance through branch-level probability floors ($P_d, P_s \ge \rho$).
2. **Novel Architecture / System Integration:** Integration of heterogeneous angular/perceptual scores ($5$-D per branch), continuous context ($g, Q, R_{\text{sam}}$), a 947-parameter MLP, and Platt calibration into a cascaded architecture where direct scoring and lightweight fusion ($0.19\ \mu\text{s}$) isolate ambiguity rather than replacing frozen deep backbones.
3. **Novel Decision Framework:** An operational three-way biometric decision rule separating **zero-calibration-FA auto-accept ($T_{\text{acc}}$)** from **$\beta$-quantile auto-reject ($T_{\text{rej}}(\beta)$)**—empirically resolving the dilemma where high-AUC learners (Siamese ViT AUC $= 0.972$, Qwen2-VL AUC $= 0.906$) collapse to $\approx 0\%$ throughput and single-branch matchers (ArcFace) reject $0.00\%$ of hard impostors.
4. **Statistical Evaluation Contribution:** Pairing exact **multi-look Bonferroni-corrected Clopper-Pearson zero-failure upper bounds** on strictly bipartite identity-disjoint pairs ($\mathcal{D}_{\text{random}}$) with **subject-clustered bootstrap intervals** (`500` resamples) on correlated genuine/adversarial splits (`Bolle et al. CVIU 2004`). Distinguished from *Xu et al.* (TIFS 2024, ECE calibration) and *Ahn et al.* (TIFS 2024, vMF open-set accuracy) by tying finite-sample test guarantees directly to frozen operational thresholds.
5. **Experimental Contribution:** Comprehensive empirical characterization across clean person-disjoint MORPH ($N = 339{,}011$ test pairs), external MORPH-frozen transfer to FG-NET (exposing genuine adult gains up to $+2.71\times$ at $30+$ years alongside critical $0$–$4$ year pediatric failure), and fair comparisons against CNN, ViT, and LoRA-adapted VLM baselines.
6. **Engineering & Reproducibility Contribution:** Pre-registered cryptographic sealing (`SHA-256`), tamper-evident look logging (`test_access.log`), exhaustive 26-variant ablation logging, and open-source artifact traceability satisfying TIFS Reproducible Research standards.

---

## 3. Deep Audit of the Core Claim: *"Measured, Bounded False-Accept Rate"*

We directly audited the codebase and primary test logs (`src/aafv/pairs.py`, `thresholds.py`, `p9_test.py`, `p12_extended.py`, `test_access.log`, `extended_test.csv`, `test_pair_zones_look1.csv`) against every statistical question in `Prompt-2.md`.

### 3.1 Verification of Independence Assumptions & Person-Disjoint Sampling
- **MORPH $\mathcal{D}_{\text{random}}$ ($N = 1{,}149$): STRICTLY JUSTIFIED.** Inspection of [`src/aafv/pairs.py`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/Code/AAFV_Net/src/aafv/pairs.py) (lines 26–39, `d_random()`) confirms that test subjects are shuffled within biological sex groups and paired **without replacement into disjoint consecutive tuples** `(ids[k], ids[k+1])`, sampling **one photograph per individual**. Every subject appears **at most once** across all $1{,}149$ pairs ($2{,}298$ distinct subjects across $167$ female pairs and $982$ male pairs). Moreover, forcing **same-sex pairing** avoids easy cross-sex mismatches, making $\mathcal{D}_{\text{random}}$ slightly stricter than uniform random pairing. Conditional on the frozen calibration checkpoint, these $1{,}149$ comparisons genuinely satisfy independent Bernoulli trial assumptions.
- **MORPH $\mathcal{D}_{\text{all\_random}}$ ($N = 277{,}822$): INDEPENDENCE VIOLATED.** `pairs.d_all_random()` draws random images with replacement (`rng.integers`), repeating individuals hundreds of times across pairs. Note that `scripts/p12_extended.py` (line 78) computed a spurious column `D_all_random_FA_bound95` $= 1.078 \times 10^{-5}$ inside `extended_test.csv`. **That $10^{-5}$ number is statistically invalid** under intra-subject correlation and must **never** be cited as an analytical bound in the paper; $\mathcal{D}_{\text{all\_random}}$ serves purely as a large-pool empirical zero-incident stress test ($0 / 277{,}822$).
- **MORPH $\mathcal{D}_{\text{hard}}$ ($N = 35{,}735$): I.I.D. VIOLATED (Adversarial Selection).** `hard_negatives()` selects top-$5$ ArcFace look-alikes per image, violating random independence; $5/35{,}735$ ($0.014\%$) FAs actually occurred in Look 2 ($3/35{,}735$ in Look 1).
- **FG-NET Adults ($N = 3{,}670$ impostors): IDENTITY CORRELATION PRESENT.** FG-NET contains only $\le 82$ total subjects, meaning $3{,}670$ impostor pairs heavily reuse the same faces. Thus `0 / 3,670` on FG-NET adults is an encouraging zero-incident generalization observation, **not** an independent binomial upper bound.

### 3.2 Audit of Calibration-Test Separation & Multi-Look Bonferroni Validity
- **Separation in Pipeline:** Calibration (`p78_calibrate_freeze.py`) strictly reads `train_fit`, `train_val`, and `calibration`; neither `thresholds.json` nor `frozen.pkl` ever accesses `test`.
- **Two-Look Accounting (`LOOKS_MAX = 2`):**
  * **Look 1 (`2026-11-05T21:42:09Z`):** Ran `p9_test.py` on `thresholds.json` (`T_acc = 0.956575`, `T_reject = -0.000385`, Stage A model). Observed `0 / 1,149` FA on $\mathcal{D}_{\text{random}}$ and `3 / 35,735` FA on $\mathcal{D}_{\text{hard}}$.
  * **Look 2 (`2026-11-07T19:45:00Z`):** Ran `p12_extended.py` on `ablations/variants/full/frozen.pkl` (`T_acc = 0.956438`, quantile $T_{\text{rej}}(\beta)$ calibrated strictly on `calibration`) alongside 7 comparator/ablation variants. Observed `0 / 1,149` FA on $\mathcal{D}_{\text{random}}$ and `5 / 35,735` FA on $\mathcal{D}_{\text{hard}}$.
  * **Statistical Assessment of Bonferroni ($\alpha' = 0.05/2 = 0.025 \implies 0.320\%$):** Across the two logged primary checkpoints (`thresholds.json` in Look 1 and `frozen.pkl` in Look 2), testing on the *same* underlying $\mathcal{D}_{\text{random}}$ pairs yields positively correlated tests whose family-wise Type-I error rate is conservatively bounded at $\le 0.05$ by $\alpha' = 0.025$. Crucially, because Look 2's $\beta$-sweep only alters $T_{\text{rej}}$ (never $T_{\text{acc}}$ or auto-accept decisions) and because authors retained the pre-registered `full` variant over Look 2's higher-accept `agg_no_shared_targets`, test-set cherry-picking did not occur. **However**, full TIFS transparency requires noting that Look 2 evaluated 8 variants simultaneously on the same test split for comparative benchmarking.

### 3.3 CRITICAL FACTUAL & STATISTICAL DISCREPANCIES UNCOVERED IN `AAFV-02.pdf` (`publication/main.tex`)

Direct verification against `extended_test.csv`, `test_pair_zones_look1.csv`, `thresholds.py`, `thresholds.json`, `ablation_freeze.json`, and `test_access.log` uncovered **seven severe factual/code discrepancies** inside `publication/main.tex` that MUST be corrected in Phase 7:

1. **Calibration Result Masquerading as Test Result (`VLM Qwen2-VL-2B` in Table I):**
   Table I (`tab:main_results`) lists `VLM (Qwen2-VL-2B)` alongside MORPH `test` rows with `0` FAs on `D_random (N=1,149)`, `D_all_random (N=277,822)`, and `D_hard (N=35,735)`, and `10.20%` `D_hard` rejection! **IN REALITY:** `extended_test.csv` has **NO `baseline_vlm` row**. VLM was evaluated **strictly on the 13,319-pair `calibration` common subset** (`decision_table_calibration.csv`)! Reporting VLM inside Table I as a MORPH test row violates scientific integrity (`Prompt-2.md` Phase 8 rule #7). It must be moved to a calibration-subset table or prose footnote!
2. **Wrong False-Accept Count & Metric Precision in Table I / Appendix Table IX:**
   - `AAFV-Net (No Shared Targets)` (`agg_no_shared_targets`) actually had **`0` FA on $D_{\text{hard}}$** in `extended_test.csv` (NOT `4` as Table I reports!), with `same_acc = 83.91% [82.03, 85.72]`, `D_hard_rej = 97.85% [97.57, 98.12]`, `D_by_both_rej = 53.98% [51.77, 56.18]`.
   - `AAFV-Net (Full)` exact `extended_test.csv` values at $\beta=0.01$: `same_acc = 70.07% [66.52, 73.11]`, `D_hard_rej = 98.04% [97.77, 98.31]`, `D_by_both_rej = 57.49% [55.34, 59.73]` (Table I/IX had slightly mismatched intervals `[66.49, 73.08]`, `[97.68, 98.39]`, and `57.53`).
   - `ArcFace (No Guards)` neutral rejection is **`28.46%` (`[26.61, 30.54]`)** in `extended_test.csv`, not `--`.
   - Other small rounding mismatches in Table I/IX (`ArcFace Only` `89.45%` not `89.44%`, `Direct 5-Score LR` `87.10%` not `87.14%`, `Direct-Only MLP` `97.77%` / `49.96%`, `Siamese CNN` `0.21%` / `9.86%`, `Siamese ViT` `10.04%`).
3. **Wrong Same-Person Sample Size (`1,150` vs `24,305`) in Table I & Table II:**
   - Table I header declares `Same-Person Auto-Accept (%) (N = 1,150)` and Table II writes `(917/1,150)`, `(806/1,150)`, and `Auto-Reject Rate: 1.00% (11/1,150)`!
   - **TRUE COUNT ON DISK:** MORPH `test` has **`24,305` same-person pairs** (`19,382/24,305 = 79.74%` accept in Look 1; `17,030/24,305 = 70.07%` accept, `7,143/24,305 = 29.39%` review, and **`132/24,305 = 0.54%`** auto-reject in Look 2!). Also `D_hard` rejected count at Look 2 is `35,034/35,735` (`98.0383%`). Notice Fig. 2 caption/box also states `Auto-Reject Rate: 1.00%` and `Review Rate: 28.93%` and `57.53% Neutral` instead of empirical Look 2 values `0.54%`, `29.39%`, and `57.49%`!
4. **Look 1 / Look 2 Hash & Timestamp Errors in Table II (`tab:reconciliation`) & `publication/README.md`:**
   - Look 1 log timestamp: `2026-11-05 21:42:09 UTC` (not `21:04`).
   - Look 2 log timestamp: `2026-11-07 19:45:00 UTC` (not `19:42`).
   - Look 2 artifact `ablations/variants/full/frozen.pkl` SHA-256: **`a47c916b...35b9`** (verified in `ablation_freeze.json["full"]`), **NOT** `0fb68e7b...45cf`.
5. **Equation & Hyperparameter Mismatches Against Actual Source Code:**
   - `main.tex` claims margin $\epsilon = 10^{-4}$ in (14); actual `src/aafv/thresholds.py` uses adaptive half-spread margin $\max(0.001, \frac{1}{2}(P_{(1)} - P_{(5)}))$.
   - `main.tex` claims hardcoded $Q_{\min}=0.20, R_{\min}=0.30$; actual `p78_calibrate_freeze.py` & `thresholds.json` compute empirical 5th percentiles on `train_fit` (**$Q_{\min} = 0.2948$, $R_{\min} = 0.3944$**).
   - `thresholds.zone` rejects when $P < T_{\text{rej}}$ (strict inequality), whereas `main.tex` eq. (2) writes $P \le T_{\text{rej}}$.
6. **Table VII (`tab:fairness`) Sex-Disaggregated Numbers Are Incorrect/Stale:**
   - Table VII reports `Male (N=926): 80.25%` and `Female (N=224): 77.95%` (Disparate Impact `0.971`).
   - Actual `Code/AAFV_Net/q/report/test_pair_zones_look1.csv` (Look 1, the only gender-resolved test log on disk) contains **$N_{\text{male}} = 20{,}774$ same pairs (`81.07%` accept, `0/982` random FA, `3/30{,}921` hard FA)** and **$N_{\text{female}} = 3{,}531$ same pairs (`71.93%` accept, `0/167` random FA, `0/4{,}814` hard FA)** — a real **$9.14$ percentage-point disparity** (ratio `0.887`, consistent with *Klare et al., TIFS 2012*)! Look 2 did not save per-pair gender zones.
7. **Unverified Visual Inspection Claim in Section VIII-B:**
   - Line 510 states *"Visual inspection reveals that these five pairs correspond to look-alike individuals of identical race, sex, and approximate age..."*, contradicting original `paper.tex` line 221 (*"5 false accepts in 35,735 pairs, which we have not inspected visually"*). We have no image contact sheet on disk for the 5 Look-2 `test` $D_{\text{hard}}$ false accepts (only `audit_different_top50.jpg` from *calibration*). Section VIII-B must honestly disclose that visual inspection of the 5 test $D_{\text{hard}}$ FAs was not completed.

---

## 4. Recommended Reframing & More Defensible Wording for TIFS

Because TIFS reviewers scrutinize biometric security bounds severely, overstating $0.320\%$ random FAR bounds as general adversarial guarantees invites rejection. We recommend the following disciplined wording upgrades:

### 4.1 Title Recommendation
- **Original Title:** *AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate*
  - *Risk:* Implies a universal/adversarial FAR bound across all operating distributions; TIFS reviewers may ask why $5/35{,}735$ hard FAs and $4/20{,}000$ pediatric FAs still occur if FAR is "bounded."
- **Recommended More Defensible Options (User to Confirm Preference in Phase 6/7):**
  - **Option 1 (Most Defensible & Scientifically Accurate):**  
    ***AAFV-Net: Guarded Three-Way Age-Aware Face Verification With Empirically Bounded Random False-Accept Risk***
  - **Option 2 (Closer to Original Title With Scope Qualifier):**  
    ***AAFV-Net: Age-Aware Face Verification With a Calibrated Three-Way Decision Rule and Bounded Random False-Accept Rate***

### 4.2 Abstract, Contribution, & Guarantee Wording Corrections

| Claim Context | Overstated / Vulnerable Phrasing (`AAFV-02.pdf`) | Recommended Defensible TIFS Wording |
|---|---|---|
| **FAR Bound Scope** | *"with an analytical false-accept rate (FAR) bound on person-disjoint random impostors... FAR $\le 0.320\%$."* | *"establishes an exact one-sided 95% Clopper-Pearson upper confidence bound of 0.320% on same-sex, person-disjoint random impostor false accepts under a two-look Bonferroni adjustment, while separately auditing adversarial look-alikes where empirical residual false accepts (5 of 35,735) persist."* |
| **Operational Domain** | *"Automated verification of facial identity across multi-year age gaps..."* | *"Automated adult cross-age facial verification (ages $\ge 16$), explicitly restricting pediatric faces (0–4 years) where generative aging introduces identity drift."* |
| **Statistical Contribution** | *"a statistically bounded false-accept rate"* | *"an auditable verification framework that locks thresholds prior to test evaluation under cryptographic hashes and applies exact zero-failure binomial bounds strictly to mutually person-disjoint random pairs rather than correlated all-pairs pools."* |
| **Performance Superiority** | *"AAFV-Net occupies the optimal upper-right trade-off quadrant... complete collapse of learned baselines."* | *"AAFV-Net trades nominal genuine acceptance against ArcFace (70.07% vs. 89.45%) in exchange for filtering 98.04% of ArcFace-mined hard impostors and 57.49% of neutral hard impostors that uncalibrated thresholders defer to review or fail to separate under minimax zero-calibration-FA rules."* |
| **Fairness Audit** | *"Disparate Impact Ratio of 0.971... only 2.30 percentage points..."* (based on wrong numbers) | Report the verified **Look 1** sex breakdown (**81.07% male vs. 71.93% female** auto-accept, $\Delta = 9.14$ pp, ratio $0.887$, $0$ random FAs in both sexes), clearly noting that female genuine drift matches prior TIFS demographic findings (*Klare et al.*, 2012) and that Look 2 did not retain per-pair gender logs. |

---

## 5. Phase 4 Summary of Findings & Unresolved Questions

### Findings
1. **True Novelty Clarified:** AAFV-Net's defensible academic contribution for TIFS lies in **system integration, guarded three-way thresholding under quality/reliability floors, model-neutral look-alike evaluation, and pre-registered statistical risk accounting**—not new foundational embeddings, GANs, or binomial theorems.
2. **Independence Confirmed on `D_random`:** Code verification (`pairs.d_random`) mathematically validates mutual person-disjoint independence across all $N=1{,}149$ test pairs (same-sex 1-to-1 matching without replacement).
3. **Serious Factual Mismatches Exposed in `AAFV-02.pdf`:** Audited disk artifacts revealed 7 critical factual errors currently embedded in `publication/main.tex` (VLM calibration leak in Table I; wrong `D_hard_FA` for no-shared-targets; wrong `N=1,150` denominator instead of `24,305`; wrong Look 2 SHA-256 hash `0fb68e7b` vs `a47c916b`; wrong margin/guard parameter formulas; stale/wrong Table VII sex-disparity percentages; and an unsubstantiated visual inspection claim for the 5 test $D_{\text{hard}}$ FAs).

### Unresolved Questions Carried Into Phase 5
1. Check `scripts/p6_train.py` and `scripts/p5_vectors.py` to recover all unreported TIFS *Guidelines for Deep Learning Submissions* hyperparameters (optimizer, LR, epochs, input scaling, exact gap-balanced BCE weighting) and resolve Fig. 2 numerical labels (`0.54%` reject, `29.39%` review, `57.49%` neutral).
2. Decide exact preferred title refinement (Option 1 vs Option 2) and inspect all 18 manuscript sections systematically in Phase 5 (`MANUSCRIPT_REVIEW.md`).

---

**Phase 4 Status:** **COMPLETE.** Ready to proceed to **Phase 5 — Full Manuscript Review** (`MANUSCRIPT_REVIEW.md`) upon your confirmation.

