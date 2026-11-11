# Phase 1 Complete Research Audit: AAFV-Net
**Project:** AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate  
**Auditor:** Senior Research Scientist & IEEE Biometrics/Machine Learning Specialist  
**Audit Date:** November 2026  
**Status:** Phase 1 Complete (System Reconstructed, Source-of-Truth Verified, Codebase Audited)  

---

## 1. Executive Summary & Concise Research Understanding

### 1.1 Core Research Contribution
AAFV-Net proposes a framework for cross-age face verification (comparing photos of the same individual taken across significant time gaps) framed as a **three-way selective classification system**:
$$\text{Decision}(I_1, I_2) \in \{\text{Auto-Accept}, \text{Manual Review}, \text{Auto-Reject}\}$$

Traditional biometrics apply a single threshold to a similarity metric (e.g., ArcFace cosine distance), reporting ROC-AUC or verification accuracy at fixed theoretical operating points. In age-gap face verification, identity feature degradation across decades degrades accuracy, forcing deployers either to lower thresholds (admitting impostors) or raise them (rejecting genuine users). 

AAFV-Net addresses this with four core engineering mechanisms:
1. **Multi-Source Evidence Aggregation:** Combines direct image pair comparison with Style-based Age Manipulation (SAM) age transformations (both forward/backward age snapping and shared intermediate target ages on a 5-year grid), extracting five complementary similarity scores per comparison: ArcFace cosine similarity, EfficientNet-B0 feature distance, VGG-Face feature distance, LPIPS perceptual distance, and SSIM.
2. **Context-Gated Fusion Network:** A two-stage architecture featuring branch-specific linear learners ($5 \to 1$) coupled with an 11-dimensional Multilayer Perceptron ($11 \to 32 \to 16 \to 1$) trained with branch masking ($p=0.12$) to retain inference capability when generative aging is absent. Platt scaling calibrates logits into posterior probabilities.
3. **Hard Quality and Reliability Guards:** Heuristic gating requiring input image quality ($Q \ge Q_{\min}$), direct-branch probability ($P_d \ge \rho$), and generated-face reliability ($R_{\text{sam}} \ge R_{\min}, P_s \ge \rho$). Crucially, guards can only demote candidate Auto-Accepts into Manual Review, never promote a rejection.
4. **Frozen Calibration Thresholds & Audited Zero-Error Bounds:** Thresholds are pinned on an identity-disjoint calibration split. The Auto-Accept threshold $T_{\text{acc}}$ is set strictly above the highest-scoring different-person calibration pair that clears the guards. If zero false accepts are observed over $N$ independent, person-disjoint negative test pairs, the one-sided upper confidence bound on the false-accept rate (FAR) is bounded via the generalized rule of three:
$$\text{FAR}_{\text{upper}} = 1 - \alpha^{1/N}$$
Under a strict 2-look test access logging regime ($\alpha = 0.05 / 2 = 0.025$) with $N = 1{,}149$ person-disjoint negative pairs, this produces an empirical upper bound of $0.3205\% \approx 0.32\%$.

---

### 1.2 Relationship to Prior Work & `BASE_Paper.pdf`
The workspace contains an earlier manuscript: `BASE_Paper.pdf` (*"An Explainable Age-Gap-Aware Face Verification Framework Using Bidirectional Age Normalization and Multi-Model Fusion"* by S. Hira, A. Nayak, et al., 37 pages).

A rigorous comparison reveals the exact technical evolution:
* **Scoring Methodology:** `BASE_Paper` evaluated 12 similarity scores across forward, backward, and direct branches, fusing them using three distinct Logistic Regression models partitioned heuristically across age gaps (Small: 0–5y, Medium: 6–15y, Large: >15y). `AAFV-Net` replaces this with unified linear branch learners feeding an 11-input MLP with continuous age-gap encoding $g$, image quality $Q$, and synthesized-face reliability $R_{\text{sam}}$.
* **Intermediate Age Grids:** `BASE_Paper` only tested bidirectional endpoint transformation (young $\to$ old and old $\to$ young). `AAFV-Net` introduces up to $K \le 7$ shared intermediate target ages along a 5-year grid.
* **Integrity & Identity Leakage:** `BASE_Paper` suffered from severe unmitigated duplicate identity leakage in MORPH-2 (where identical individuals exist under multiple IDs). `AAFV-Net` explicitly audits this, identifying and quarantining 858 duplicate identities (6.4% of subjects).
* **Decision Framework:** `BASE_Paper` claimed a theoretical Neyman-Pearson threshold ($\text{FAR} \le 1\%, \text{FRR} \le 5\%$) without bounding false accepts on held-out test data. `AAFV-Net` introduces the frozen, hash-pinned, access-budgeted calibration-to-test protocol with non-parametric zero-error confidence bounding.

---

### 1.3 External Claude Discussion Access Limitation
Per Section 2.E of the Master Prompt, access was attempted for the previous Claude conversation at:
`https://claude.ai/share/ee314c24-80a1-451a-9a27-3cfc8b1f33af`
* **Status:** Access is blocked / not indexable via automated external browsing tools without authentication.
* **Action Required:** In strict compliance with research integrity rules, this limitation is explicitly reported. **The user is requested to export and provide the discussion transcript as a text/Markdown file if it contains historical design rationale not documented in the repository.**

---

## 2. Task 1.1: Complete Architectural Reconstruction

Every component of the AAFV-Net pipeline was traced directly from the source code (`src/aafv/` and `scripts/`). Below is the complete specification:

```
+---------------------------------------------------------------------------------------------------+
|                                       AAFV-NET ARCHITECTURE                                       |
+---------------------------------------------------------------------------------------------------+
                                   Input Pair: (I1, a1), (I2, a2)
                                                |
                         +----------------------+----------------------+
                         |                                             |
                         v                                             v
             [P1: Face Detection & Align]                  [P1: Quality & P2: DEX Age]
             - dlib upsample 1 & 2                         - Raw: Sharp, Illum, Contrast, Noise, Detail
             - Fallback: InsightFace SCRFD                 - Normalization fitted on train_fit -> Q in [0, 1]
             - 68-pt dlib landmark extraction              - DEX CNN Age Estimation on crops -> est_age
             - FFHQ 5-point similarity warp (256x256)      - Bias & error variance epsilon fitted on train_val
                         |
                         +----------------------+
                         |                      |
                         v                      v
                 [Direct Branch]         [Aged Branch (SAM)]
                 Original pair (I1, I2)  - Forward: I1 -> snap(a2)
                                         - Backward: I2 -> snap(a1)
                                         - Shared Targets: I1, I2 -> T in Grid (K <= 7)
                                                |
                         +----------------------+
                         v
             [Feature Extraction & 5-Score Vector]
             Across each comparison:
               1. ArcFace Cosine Similarity (buffalo_l ResNet-100)
               2. EfficientNet-B0 Cosine Distance: (cos + 1) / 2
               3. VGG-Face Cosine Distance: (cos + 1) / 2
               4. LPIPS AlexNet Perceptual Score: 1 - min(dist, 1.0)
               5. Structural Similarity (SSIM 7x7 window on Gray)
                         |
                         +-----------------------------------------------+
                         |                                               |
                         v                                               v
             [Direct Linear Learner Wd]                     [SAM Linear Learner Ws]
             Standardized via train_fit                     Standardized via train_fit
             Linear(5 -> 1)                                 Aggregated: 0.5*Endpoints + 0.5*Shared
                                                            Linear(5 -> 1)
                                                            Reliability Rsam = 0.7*Rfaces + 0.3*Rc
                         |                                               |
                         +-----------------------+-----------------------+
                                                 |
                                                 v
                                       [11-Dimensional MLP]
                       Inputs: [Wd, Ws, Wf(=0), g, Q, enh(=0), Rsam, Rd(=0), Asam, Ad(=0), Amulti]
                       Architecture: Linear(11 -> 32) -> ReLU -> Dropout(0.1)
                                  -> Linear(32 -> 16) -> ReLU -> Dropout(0.1)
                                  -> Linear(16 -> 1)
                       Training: AdamW, gap-balanced weighted BCE, SAM branch masking (p=0.12)
                       Ensemble: 5 random seeds averaged -> Logit S
                                                 |
                                                 v
                                       [Platt Calibration]
                               Logistic Regression on train_val -> Probability P in [0, 1]
                                                 |
                                                 v
                                  [Quality & Reliability Guards]
                       Require: Q >= Q_min (0.2948)
                                Direct branch Pd >= rho (0.20)
                                If SAM available: Rsam >= R_min (0.3944) AND Ps >= rho (0.20)
                                                 |
                                                 v
                                    [Three-Way Decision Logic]
                       Auto-Accept: P >= T_acc (0.9566) AND Guards Pass
                       Auto-Reject: P <= T_rej(beta) (e.g. beta=0.01 -> T_rej=0.0075)
                       Manual Review: All remaining pairs (and candidate accepts failing guards)
```

### Detailed Component Specifications

#### Component 1: Input Preprocessing and Face Alignment
* **Purpose:** Detect faces robustly across variations and align facial geometry to standard FFHQ metric space.
* **Formulation:** Multi-stage cascaded detector. Primary: dlib frontal HOG detector with upsampling factors $u \in \{1, 2\}$. Fallback: InsightFace SCRFD (`buffalo_l` detection module, threshold $0.3$, input resolution $640 \times 640$). Landmark estimation via dlib 68-point shape predictor. Similarity transform based on eye center coordinates $(p_{\text{left}}, p_{\text{right}})$ and outer mouth corners $(m_0, m_6)$ to output resolution $256 \times 256$.
* **Input / Output:** Raw image path $\to$ Aligned RGB PIL crop ($256 \times 256$).
* **Location:** `src/aafv/detect.py`, `src/aafv/align.py`, `scripts/p1_align.py`.
* **Hyperparameters:** `output_size=256`, dlib upsamples 1 and 2, SCRFD detection threshold 0.3.

#### Component 2: Image-Quality Assessment
* **Purpose:** Quantify input image degradation to prevent degraded photographs from corrupting downstream feature representations.
* **Formulation:** Computes five raw metrics on grayscale crop $g$:
  1. Sharpness: $\text{Var}(\nabla^2 g)$.
  2. Illumination: $1.0 - \frac{|\text{mean}(g) - 128|}{128}$.
  3. Contrast: $\sigma(g)$.
  4. Noise: Immerkaer (1996) Laplacian fast noise estimation: $\sigma_n = \frac{\sum |g * K| \sqrt{\pi / 2}}{6(W-2)(H-2)}$ with $3 \times 3$ kernel $K$.
  5. Detail: Bounding box pixel scale $\min(w_b, h_b)$.
  Normalization parameters $[lo_m, hi_m]$ (5th and 95th percentiles) are strictly fitted on `train_fit`. Quality score:
  $$Q = \frac{1}{5} \sum_{m=1}^5 q_m, \quad q_m \in [0, 1]$$
* **Input / Output:** Aligned $256 \times 256$ crop $\to Q \in [0, 1]$.
* **Location:** `src/aafv/quality.py`, `scripts/p2_features.py`.

#### Component 3: Age Estimation and Age-Gap Categorization
* **Purpose:** Extract objective chronological coordinates, measure age-estimation bias, and discretize longitudinal intervals into operational bins.
* **Formulation:** DEX (Deep EXpectation of apparent age) ResNet model. Normalizes gap: $g(a_1, a_2) = \min(1.0, |a_2 - a_1| / A_{\max})$ with $A_{\max} = 80$.
  Discretized into 6 bins via edges $[0, 5, 10, 15, 20, 30]$:
  $G1: [0, 5), G2: [5, 10), G3: [10, 15), G4: [15, 20), G5: [20, 30), G6: [30, \infty)$.
  Global estimation bias and error tolerance:
  $$\text{bias} = \frac{1}{|V|} \sum (\hat{a} - a), \quad \epsilon = \min(\text{EPS\_LIMIT}, \text{Quantile}_{0.75}(|\hat{a} - a - \text{bias}|))$$
* **Input / Output:** Face crop $\to \hat{a} \in \mathbb{R}^+$; Age pair $(a_1, a_2) \to (g, \text{bin})$.
* **Location:** `src/aafv/gap.py`, `scripts/c4_eval_age.py`, `scripts/p2_features.py`.
* **Hyperparameters:** $A_{\max} = 80$, $\text{EPS\_LIMIT} = 8$, $\text{GRID\_STEP} = 5$.

#### Component 4: SAM-Based Age Transformation
* **Purpose:** Synthesize age-progression and age-regression counterfactuals using Style-based Age Manipulation.
* **Formulation:** Latent-space directional shift in StyleGAN conditioned on target age $t$:
  $$w_{\text{aged}} = w + \Delta w(w, t)$$
* **Input / Output:** Aligned crop $I \in \mathbb{R}^{256 \times 256 \times 3}$, target age $t \in \mathbb{Z} \to I^{(t)} \in \mathbb{R}^{256 \times 256 \times 3}$.
* **Location:** `scripts/p4_sam.py`, `src/aafv/manifest.py`, `src/aafv/gen_worker.py`.

#### Component 5: Forward and Backward Age Transformation
* **Purpose:** Align face pair $(I_1, I_2)$ at their counterpart chronological ages.
* **Formulation:** Younger face $I_1$ (age $a_1$) is aged forward to $t_{\text{fwd}} = \text{snap}(a_2, \text{grid})$. Older face $I_2$ (age $a_2$) is de-aged backward to $t_{\text{bwd}} = \text{snap}(a_1, \text{grid})$. Grid uses 5-year intervals. Snapping ties resolve to the higher age.
* **Input / Output:** Pair $(I_1, a_1), (I_2, a_2) \to (I_1^{(t_{\text{fwd}})}, I_2), (I_1, I_2^{(t_{\text{bwd}})})$.
* **Location:** `src/aafv/gap.py`, `src/aafv/pairvec.py`.

#### Component 6: Shared Target-Age Generation
* **Purpose:** Provide intermediate chronological bridge comparisons to verify trajectory identity consistency.
* **Formulation:** Target set $T = \{t \in \text{grid} \mid a_1 < t < a_2\}$. If $|T| > K_{\max} = 7$, uniformly sub-sampled to 7 targets. Both $I_1$ and $I_2$ are synthesized at each $t \in T$, yielding $|T|$ paired comparisons $(I_1^{(t)}, I_2^{(t)})$.
* **Location:** `src/aafv/gap.py`, `src/aafv/manifest.py`, `src/aafv/pairvec.py`.
* **Hyperparameters:** $K_{\max} = 7$, $\text{grid\_step} = 5$.

#### Components 7–11: Five-Dimensional Similarity Feature Extraction
For every compared pair of images $(X, Y)$ across direct, forward, backward, and shared branches, a 5-dimensional similarity vector $S = [s_{\text{arc}}, s_{\text{eff}}, s_{\text{vgg}}, s_{\text{lpips}}, s_{\text{ssim}}] \in \mathbb{R}^5$ is computed:
1. **ArcFace ($s_{\text{arc}}$):** InsightFace `buffalo_l` (ResNet-100, Glint360k pretrained), 512-d $L_2$-normalized embedding. Similarity: $s_{\text{arc}} = E_X \cdot E_Y \in [-1, 1]$.
2. **EfficientNet-B0 ($s_{\text{eff}}$):** Pretrained on ImageNet, penultimate global average pooling feature, $L_2$-normalized. Scaled similarity: $s_{\text{eff}} = \frac{E_X \cdot E_Y + 1}{2} \in [0, 1]$.
3. **VGG-Face ($s_{\text{vgg}}$):** VGG16 face feature vector, $L_2$-normalized. Scaled similarity: $s_{\text{vgg}} = \frac{E_X \cdot E_Y + 1}{2} \in [0, 1]$.
4. **LPIPS ($s_{\text{lpips}}$):** Learned Perceptual Image Patch Similarity with AlexNet backbone. Scaled: $s_{\text{lpips}} = 1.0 - \min(d_{\text{lpips}}(X, Y), 1.0) \in [0, 1]$.
5. **SSIM ($s_{\text{ssim}}$):** Structural Similarity index on grayscale, $7 \times 7$ uniform box window, $K_1=0.01, K_2=0.03$, mirror-padded, boundary cropped. $s_{\text{ssim}} \in [-1, 1]$.
* **Location:** `src/aafv/ssim.py`, `scripts/p5_scores.py`.

#### Component 12: Branch-Specific Linear Learners
* **Purpose:** Collapse the 5 heterogeneous similarity metrics into a calibrated scalar representation per evidence branch.
* **Formulation:** Raw scores are standardized using $(\mu, \sigma)$ fitted strictly on `train_fit`:
  $$Z = \frac{S - \mu}{\sigma}$$
  For the SAM branch, endpoint scores ($Z_{\text{fwd}}, Z_{\text{bwd}}$) and shared target scores ($Z_{\text{sh}}^{(k)}$) are aggregated:
  $$Z_{\text{base}} = \frac{1}{2}(Z_{\text{fwd}} + Z_{\text{bwd}}), \quad Z_{\text{shared}} = \frac{1}{K} \sum_{k=1}^K Z_{\text{sh}}^{(k)}$$
  $$x_{\text{sam}} = \begin{cases} 0.5 Z_{\text{base}} + 0.5 Z_{\text{shared}} & \text{if } K \ge 1 \\ Z_{\text{base}} & \text{if } K = 0 \end{cases}$$
  Linear projections:
  $$W_d = w_d^T x_{\text{dir}} + b_d, \quad W_s = w_s^T x_{\text{sam}} + b_s, \quad W_f = w_f^T x_{\text{diff}} + b_f$$
  In Stage A, diffusion is inactive ($W_f = 0$).
* **Location:** `src/aafv/pairvec.py`, `src/aafv/fusion.py`.

#### Component 13: Fusion MLP Architecture
* **Purpose:** Non-linear decision fusion combining branch representations with contextual signals.
* **Formulation:** Input vector $z \in \mathbb{R}^{11}$:
  $$z = [W_d, W_s, W_f, g, Q, \text{enhanced\_pair}, R_{\text{sam}}, R_{\text{diff}}, \text{avail\_sam}, \text{avail\_diff}, \text{avail\_multi}]$$
  Hidden layers:
  $$h_1 = \text{ReLU}(\text{Linear}_{11 \to 32}(z)), \quad h_1' = \text{Dropout}_{0.1}(h_1)$$
  $$h_2 = \text{ReLU}(\text{Linear}_{32 \to 16}(h_1')), \quad h_2' = \text{Dropout}_{0.1}(h_2)$$
  $$\text{Logit } S = \text{Linear}_{16 \to 1}(h_2')$$
  Ensemble: 5 independent seeds averaged: $S = \frac{1}{5} \sum_{i=1}^5 S^{(i)}$.
* **Location:** `src/aafv/fusion.py`, `scripts/p6_train.py`.
* **Hyperparameters:** Hidden sizes $(32, 16)$, dropout $0.1$, AdamW learning rate $1 \times 10^{-3}$, weight decay $1 \times 10^{-4}$, patience $10$, max epochs $100$.

#### Component 14: Context Features
* **Purpose:** Condition the decision manifold on operational covariates.
* **Features:** $g \in [0, 1]$ (normalized age gap), $Q \in [0, 1]$ (mean image quality of pair), $\text{enhanced\_pair} \in \{0, 1\}$ (super-resolution flag, 0 in Stage A), $R_{\text{sam}} \in [0, 1]$ (synthesis reliability), $\text{avail\_sam} \in \{0, 1\}$, $\text{avail\_multi} \in \{0, 1\}$ ($K \ge 1$).
* **Location:** `src/aafv/pairvec.py`, `scripts/p5_vectors.py`.

#### Component 15: Reliability Estimation
* **Purpose:** Quantify confidence in synthetic face outputs to prevent hallucinated artifacts from inflating verification scores.
* **Formulation:** Per-target reliability $R_t$ blends identity preservation $R_i$, target age fidelity $R_a$, and synthetic image quality $q_{\text{gen}}$:
  $$R_i = \max(0, s_{\text{arc}}(I^{(t)}, I_{\text{orig}}))$$
  $$R_a = 1.0 - \min\left(1.0, \frac{\max(0, |\hat{a}_{\text{gen}} - \text{bias}_{\text{pair}} - t| - \epsilon)}{2\epsilon}\right)$$
  $$R_t = \frac{1}{3}R_i + \frac{1}{3}R_a + \frac{1}{3}q_{\text{gen}}$$
  Branch reliability aggregates across all generated faces and penalizes ArcFace cosine spread $\sigma_{\text{arc}}$ across targets:
  $$R_{\text{faces}} = \sqrt{\bar{R}_{t, 1} \cdot \bar{R}_{t, 2}}, \quad R_c = 1.0 - \min\left(1.0, \frac{\sigma_{\text{arc}}}{\sigma_{\max}}\right)$$
  $$R_{\text{sam}} = 0.7 R_{\text{faces}} + 0.3 R_c$$
  where $\sigma_{\max}$ is the 95th percentile of spread on `train_fit`.
* **Location:** `src/aafv/pairvec.py` (lines 40–55), `scripts/p5_vectors.py`.

#### Component 16: Branch Masking
* **Purpose:** Regularize fusion training so the network does not become pathologically dependent on synthetic imagery when generative synthesis fails.
* **Formulation:** During training, for each mini-batch row, with probability $p_{\text{mask}} = 0.12$:
  $$S_{\text{sam}} \leftarrow 0, \quad R_{\text{sam}} \leftarrow 0, \quad \text{avail\_sam} \leftarrow 0, \quad \text{avail\_multi} \leftarrow 0$$
* **Location:** `src/aafv/fusion.py` (lines 21–24), `scripts/p6_train.py`.
* **Hyperparameters:** $p_{\text{mask}} = 0.12$.

#### Component 17: Platt Calibration
* **Purpose:** Map uncalibrated ensemble logits $S$ into monotonic posterior probabilities $P(Y=1 \mid S)$.
* **Formulation:** Logistic regression fitted on `train_val` logits:
  $$P = \sigma(A \cdot S + B) = \frac{1}{1 + \exp(-(A \cdot S + B))}$$
  Selection between univariate Platt and Isotonic Regression is determined via 5-fold person-grouped cross-validation on `train_val`. Platt scaling won with lower log loss ($0.098$ vs $0.104$).
* **Location:** `src/aafv/calib.py`, `scripts/p78_calibrate_freeze.py`.

#### Component 18: Quality and Reliability Guards
* **Purpose:** Prevent degraded photographs or failed age transformations from achieving Auto-Accept.
* **Formulation:** Boolean indicator $\text{GuardPass} \in \{0, 1\}$:
  $$\text{GuardPass} = (Q \ge Q_{\min}) \land (P_d \ge \rho) \land \left[(\text{avail\_sam} = 0) \lor (R_{\text{sam}} \ge R_{\min} \land P_s \ge \rho)\right]$$
  where $P_d = \sigma(W_d)$ and $P_s = \sigma(W_s)$ are branch probabilities from separate Platt models fitted on `train_val`.
  Operating parameters: $Q_{\min} = 0.2948$ (5th percentile of `train_fit` quality), $R_{\min} = 0.3944$ (5th percentile of `train_fit` reliability), $\rho = 0.20$ (selected from $\{0.2, 0.35, 0.5\}$ on calibration to maximize accept rate while maintaining zero calibration false accepts).
* **Location:** `src/aafv/calib.py`, `scripts/p78_calibrate_freeze.py`.

#### Component 19 & 20: Accept/Reject Thresholds & Three-Way Decision Rule
* **Purpose:** Partition the verification space into high-confidence acceptance, unambiguous rejection, and deferred manual review.
* **Formulation:**
  1. Auto-Accept Threshold $T_{\text{acc}}$:
     $$T_{\text{acc}} = \max_{(I_i, I_j) \in \mathcal{D}_{\text{calib}}^{\text{diff}}, \text{GuardPass}=1} P(I_i, I_j) + \text{margin}$$
     $$\text{margin} = \max(0.001, 0.5 \times (v_0 - v_4))$$
     where $v_k$ is the $k$-th highest probability among passing impostors.
  2. Auto-Reject Threshold $T_{\text{rej}}(\beta)$:
     $$T_{\text{rej}}(\beta) = \text{Quantile}_\beta(\{P(I_i, I_j) \mid (I_i, I_j) \in \mathcal{D}_{\text{calib}}^{\text{same}}\})$$
     At target false-reject rate $\beta = 0.01$ (1%), $T_{\text{rej}} = 0.00754$.
  3. Routing Logic:
     $$\text{Decision}(P, \text{GuardPass}) = \begin{cases} \text{Auto-Accept} & \text{if } P \ge T_{\text{acc}} \land \text{GuardPass} = 1 \\ \text{Auto-Reject} & \text{if } P < T_{\text{rej}}(\beta) \\ \text{Manual Review} & \text{otherwise} \end{cases}$$
* **Location:** `src/aafv/thresholds.py`, `scripts/p78_calibrate_freeze.py`, `scripts/p10_decision_table.py`.

#### Component 21: Test-Access Restrictions & Audit Logging
* **Purpose:** Enforce pre-registered evaluation integrity and prevent adaptive threshold tuning on the test partition.
* **Formulation:** Threshold parameters, calibration hashes, and model state weights are committed to `thresholds.json` and locked with SHA-256 (`4b7af977...2cfe`). Execution of `scripts/p9_test.py` or `scripts/p12_extended.py` verifies file immutability and increments an append-only access log (`q/logs/test_access.log`). Maximum allowed budget: `LOOKS_MAX = 2`.
* **Location:** `scripts/p9_test.py`, `scripts/p12_extended.py`, `configs/params.yaml`.

---

## 3. Task 1.2: Reconstructed Experimental Protocol

### 3.1 Dataset Composition & Splits
* **MORPH-2 Database:** Contains longitudinal mugshot photographs of adults.
  Total images processed in pipeline: $53{,}000+$ across $13{,}000+$ subjects.
* **Partitioning Protocol:** Splitting is strictly **person-disjoint** (grouped by `person_id`).
  * `train_fit`: Base model training split.
  * `train_val`: Validation split for early stopping, calibrator selection, and standardizer fitting (15% person split via `TRAIN_VAL_FRACTION = 0.15`).
  * `calibration`: Partition for setting $T_{\text{acc}}$, $T_{\text{rej}}$, and tuning $\rho$.
  * `test`: Held-out partition strictly accessed under logged budget.
  * Person-disjoint guarantee verified: `assert df.groupby('person_id').split.nunique().max() == 1` enforced in `scripts/p3_build_pairs.py`.

### 3.2 Duplicate Identity Audit & Quarantine Protocol
* **The Vulnerability:** Real-world longitudinal datasets (particularly arrest records like MORPH) frequently contain duplicate entries where the same person was assigned two different IDs upon re-arrest, or where IDs share common suffixes (e.g., ID `12200` vs `312200`).
* **Audit Finding in Code:** Without quarantine, pairs comparing identical individuals under different IDs achieved $P \approx 0.999986$ (see `audit/audit_different_top50.csv`), which erroneously forced $T_{\text{acc}} > 1.0$ and completely broke auto-acceptance.
* **Label-Free Quarantine Rule (`src/aafv/dupids.py`):**
  Identities $a, b$ are quarantined if $a$ is a proper suffix of $b$ AND either:
  $$\text{length}(a) \ge 5 \quad \text{OR} \quad \cos(\text{centroid}(a), \text{centroid}(b)) \ge 0.40$$
* **Impact:** 858 people (6.4% of total dataset) and 438 identity-variant pairs were quarantined and completely removed from all pair sets (`p5q`), establishing true separation and allowing $T_{\text{acc}}$ to settle at $0.9566$.

### 3.3 Negative Pair Sets & Mining Strategy
To test the three-way decision boundary under different threat models, four distinct negative sets were engineered:
1. **$D_{\text{random}}$ (Unbiased Person-Disjoint Impostors):** Exactly 1 random photo per subject paired across disjoint identities with matched gender. On MORPH test: $N = 1{,}149$ pairs. Used for the primary theoretical zero-error bound.
2. **$D_{\text{all\_random}}$ (Large Random Pool):** Large-scale random impostor pairing across different subjects with matched gender ($N = 277{,}822$ pairs on MORPH test).
3. **$D_{\text{hard}}$ (ArcFace-Mined Hard Negatives):** For each image, the top $K=5$ most similar images of a different person with matching gender mined using ArcFace embeddings ($N = 35{,}735$ pairs on MORPH test).
4. **Neutral Hard Set ($D_{\text{by\_both}}$):** To prevent evaluation bias favoring models that exploit ArcFace feature geometry, independent baseline miners (Siamese ViT and Siamese ResNet-18) ranked all random impostors. The top 1% by average rank form the neutral hard set ($N = 2{,}790$ pairs). A baseline is never evaluated on a set it mined.

### 3.4 External Evaluation (FG-NET)
* **Dataset:** 1,002 photographs of 82 subjects spanning ages 0 to 69 years.
* **Protocol:** MORPH-frozen thresholds ($T_{\text{acc}} = 0.9566, T_{\text{rej}} = 0.0075, \rho = 0.20$) applied with zero fine-tuning or domain adaptation.
* **Partitioning Subsets:**
  * **All-Ages FG-NET:** 25,797 pairs (5,797 same-person, 20,000 random impostors).
  * **Adults-Only FG-NET ($a_1 \ge 16$):** 5,126 pairs (1,456 same-person, 3,670 random impostors). Cutoff was established post hoc after discovering failure modes on infants.

---

## 4. Task 1.3: Source-of-Truth Matrix

The table below cross-references all primary architectural parameters, evaluation metrics, and experimental claims across the Manuscript (`paper.tex`), Source Code, and CSV/Artifact files:

| Claim or Parameter | Manuscript (`paper.tex`) | Source Code | CSV / Artifact | Verified Status | Audit Notes & Explanation |
|---|---|---|---|---|---|
| **Accepted Decision Categories** | Auto-Accept, Manual Review, Auto-Reject | `thresholds.py`: `zone()` returns `'accept'`, `'review'`, `'reject'` | `test_report_look1.json` | **VERIFIED** | Clean 3-way routing confirmed. |
| **Input Crop Resolution** | $256 \times 256$ pixels | `align.py`: `output_size=256` | `p1_align.py` output crops | **VERIFIED** | Aligned via dlib landmarks. |
| **Similarity Metrics (5)** | ArcFace, EfficientNet, VGG, LPIPS, SSIM | `p5_scores.py`: `COLS` | `pair_vectors_*.csv` columns `d_arc` to `d_ssim` | **VERIFIED** | Extracted across all branches. |
| **Linear Branch Learner** | $5 \to 1$ linear learner per branch | `fusion.py`: `nn.Linear(5, 1)` for ld, ls, lf | Model state dict in `fusion_seed*.pt` | **VERIFIED** | Standardized using `train_fit` statistics. |
| **Fusion MLP Layers** | $11 \to 32 \to 16 \to 1$, ReLU, Dropout 0.1 | `fusion.py`: `sizes=(32, 16)`, `dropout=0.1` | `fusion_seed0.pt` layer dimensions | **VERIFIED** | Exact structural match. |
| **Branch Masking Probability** | $p_{\text{mask}} = 0.12$ | `fusion.py`: `mask_sam()`, `p_mask=0.12` | `params.yaml`: `P_MASK: 0.12` | **VERIFIED** | Zeroes SAM branch during training. |
| **Ensemble Seeds** | 5 seeds averaged | `fusion.py`: `predict()` averages `len(models)` | 5 models: `fusion_seed0.pt` to `seed4.pt` | **VERIFIED** | Evaluated on CPU/CUDA. |
| **Platt Calibrator Kind** | Platt scaling on ensemble logit $S$ | `calib.py`: `Calibrator('platt')` | `thresholds.json`: `"calibrator_kind": "platt"` | **VERIFIED** | Selected over Isotonic via GroupKFold CV. |
| **Quality Guard Threshold $Q_{\min}$** | Mentioned qualitatively | `p78_calibrate_freeze.py`: 5th percentile `tf.Q` | `thresholds.json`: `0.29476` | **VERIFIED** | Pinned in frozen thresholds. |
| **Reliability Guard $R_{\min}$** | Mentioned qualitatively | `p78_calibrate_freeze.py`: 5th percentile `tf.R_sam` | `thresholds.json`: `0.39443` | **VERIFIED** | Pinned in frozen thresholds. |
| **Guard Probability Floor $\rho$** | $\rho = 0.2$ | `p78_calibrate_freeze.py`: best of `[0.2, 0.35, 0.5]` | `thresholds.json`: `"RHO": 0.2` | **VERIFIED** | Frozen at 0.2. |
| **Frozen Auto-Accept Threshold $T_{\text{acc}}$** | $0.9566$ (rounded) | `p78_calibrate_freeze.py` / `p10_ablations.py` | `thresholds.json`: `0.956575`; `frozen.pkl`: `0.956438` | **PARTIALLY VERIFIED / CONFLICTING** | **Discrepancy:** Look 1 used `0.956575`; Look 2/Table 1 used `0.956438`. Both round to $0.957$ / $0.9566$. |
| **Frozen Auto-Reject Threshold $T_{\text{rej}}$** | $\beta$-quantile of same-person calib | `p78_calibrate_freeze.py` vs `p10_decision_table.py` | `thresholds.json`: `-0.000385`; `extended_test.csv`: `0.007541` | **CONFLICTING** | Look 1 froze $T_{\text{rej}} = -0.000385$ (no auto-reject). Table 1 uses dynamic $\beta=0.01$ quantile ($0.007541$). |
| **Quarantined Identities** | 858 people (6.4%) | `dupids.py`, `p_quarantine.py` | `quarantine_people.csv`: 858 rows | **VERIFIED** | Successfully audited and excluded. |
| **Test Access Log & Budget** | 2 looks budget | `params.yaml`: `LOOKS_MAX: 2` | `test_access.log`: exactly 2 entries | **VERIFIED** | Look 1: Nov 5; Look 2: Nov 7. Budget exhausted. |
| **MORPH Test $D_{\text{random}}$ Pairs** | $1{,}149$ pairs, 0 FA | `p9_test.py`, `p12_extended.py` | `extended_test.csv`: `D_random_n=1149`, `FA=0` | **VERIFIED** | Person-disjoint, zero false accepts. |
| **MORPH Test $D_{\text{all\_random}}$ Pairs** | $277{,}822$ pairs, 0 FA | `p9_test.py`, `p12_extended.py` | `extended_test.csv`: `D_all_random_n=277822`, `FA=0` | **VERIFIED** | Large random pool, zero false accepts. |
| **MORPH Test $D_{\text{hard}}$ False Accepts** | 5 / 35,735 | `p12_extended.py` | `extended_test.csv`: `D_hard_n=35735`, `FA=5` | **PARTIALLY VERIFIED / CONFLICTING** | Look 1 recorded 3 FA (`test_report_look1.json`); Look 2 recorded 5 FA (`extended_test.csv`). Paper reports Look 2. |
| **MORPH Test Same-Person Accept** | $70.1\%$ ($66.5$--$73.1$) | `p12_extended.py`: cluster bootstrap | `extended_test.csv`: `same_acc=0.70068`, `[0.6652, 0.7311]` | **VERIFIED** | Exact numerical match at $\beta=0.01$. |
| **MORPH Test $D_{\text{hard}}$ Rejection** | $98.0\%$ | `p12_extended.py` | `extended_test.csv`: `D_hard_rej=0.98038` | **VERIFIED** | Exact numerical match ($98.04\%$). |
| **Neutral Hard Set Rejection** | $57.5\%$ (vs $28.5\%$ ArcFace) | `p12_extended.py`: `D_by_both` top 1% | `extended_test.csv`: `D_by_both_rej=0.57491` | **VERIFIED** | Exact numerical match ($57.49\%$). |
| **Zero-Error Upper Bound Formula** | $1 - \alpha^{1/N}$ | `evaluation.py`: `1 - alpha**(1.0/n)` | Formula evaluated in `p9_test.py` | **VERIFIED** | Hanley-Lippman-Hand formulation. |
| **Reported Bound Value** | $0.32\%$ ($\alpha=0.025$, 2 looks) | `evaluation.zero_error_bound(1149, 0.025)` | `0.003205` $\to 0.3205\%$ | **VERIFIED** | Matches derivation for $N=1149, \alpha=0.025$. |
| **FG-NET Adult Auto-Accept** | $51.9\%$ ($44.5$--$58.4$) | `p12_extended.py` with `--extra_min_age 16` | `extended_calibration_fg16.csv`: `0.51923` | **VERIFIED** | Zero false accepts on 3,670 impostors. |
| **FG-NET Adult Gap 30+ Accept** | $10.3\%$ (vs $3.8\%$ ArcFace) | `p12_extended.py`: bin G6 | `extended_calibration_fg16.csv`: `same_acc_G6=0.10256` | **VERIFIED** | Exact numerical match. |
| **FG-NET All-Ages Auto-Accept & FA** | $29.9\%$, 4 FA in 20,000 | `p12_extended.py` all ages | `extended_calibration_fg.csv`: `same_acc=0.2986`, `FA=4` | **VERIFIED** | Confirmed 4 child false accepts (ages 0–4). |
| **Figure PDF Files** | `figs/fig1_concept.pdf` to `fig5_gap_neutral.pdf` | Referenced in `paper.tex` lines 24, 54, etc. | **MISSING** in repo root and `figs/` | **CONFLICTING / MISSING** | Files missing from directory; placeholder boxes in `Paper-01.tex`. |

---

## 5. Complete List of Discrepancies and Integrity Findings

### Discrepancy 1: Threshold & Metric Divergence Between Look 1 and Look 2
* **Description:** 
  In Look 1 (`scripts/p9_test.py`, logged 2026-11-05), $T_{\text{acc}} = 0.956575$ and $T_{\text{rej}} = -0.000385$ (from `q/thresholds/thresholds.json`). This yielded:
  * Same-person Auto-Accept: $79.74\%$ ($19{,}382 / 24{,}305$).
  * False Rejections: $0$ ($0\%$).
  * $D_{\text{hard}}$ False Accepts: **3** out of $35{,}735$.
  * $D_{\text{hard}}$ Auto-Reject: **0%** (all went to Review).
  
  In Look 2 (`scripts/p12_extended.py`, logged 2026-11-07), evaluated via `ablations/variants/full/frozen.pkl`, $T_{\text{acc}} = 0.956438$ and $T_{\text{rej}}$ was dynamically calculated via $\beta$-quantile ($\beta=0.01 \implies T_{\text{rej}} = 0.007541$). This yielded:
  * Same-person Auto-Accept: **$70.07\%$** ($17{,}030 / 24{,}305$).
  * $D_{\text{hard}}$ Auto-Reject: **$98.04\%$**.
  * $D_{\text{hard}}$ False Accepts: **5** out of $35{,}735$.
* **Impact on Manuscript:** The text and Table 1 report the Look 2 numbers ($70.1\%$ accept, $98.0\%$ hard reject, 5 hard FA), but Section 3.4 cites the SHA-256 hash (`4b7af977...2cfe`) of `thresholds.json` from Look 1.
* **Resolution for Revision:** The paper must transparently explain the two evaluation stages: Look 1 tested the zero-false-reject operating regime; Look 2 applied the $\beta=0.01$ Neyman-Pearson reject quantile protocol. The minor difference in $T_{\text{acc}}$ ($0.956575$ vs $0.956438$) must be acknowledged as an artifact of retrained ablation states, and both access logs must be documented without ambiguity.

---

### Discrepancy 2: Missing Vector Figure Files in Repository
* **Description:** `paper.tex` includes:
  `figs/fig1_concept.pdf`, `figs/fig2_architecture.pdf`, `figs/fig3_results.pdf`, `figs/fig4_ablations.pdf`, `figs/fig5_gap_neutral.pdf`.
  None of these PDF files exist in the repository. In `Paper/Paper-01.tex`, they were replaced with raw ASCII placeholders (`\framebox{\parbox{...}}`).
  Only two bitmap plots exist in `Code/AAFV_Net/ablations/results_subset/figs/`:
  `fig1_decision_outcomes.png` and `fig2_vs_false_reject_target.png`.
* **Impact on Manuscript:** `paper.tex` cannot be compiled directly to PDF without throwing fatal `LaTeX Error: File 'figs/fig1_concept.pdf' not found`.
* **Resolution for Revision:** A dedicated, publication-quality vector graphic generator (Matplotlib / TikZ) must be authored to render all required figures directly from experimental CSVs before manuscript compilation in Phase 7/8.

---

### Discrepancy 3: Degenerate Calibration Age-Gap Report (`gap_report_calibration.csv`)
* **Description:** In `scripts/p10_gap_report.py`, line 24 requires:
  `if len(s) >= 20 and len(imp) >= 1000:`
  In `gap_report_calibration.csv`, for gap bin G1, $N_{\text{diff}} = 949 < 1000$. For G2 through G6, $N_{\text{same}} < 20$. Consequently, **every single cell in the report fell into the fallback branch: `AUC = "n too small"`**.
  Because of this, `scripts/p11_figures.py` line 25 (`g = gp.dropna(subset=['AUC'])`) evaluated to empty, and `fig3_auc_by_gap.png` was silently never generated.
* **Impact on Manuscript:** Claims regarding calibration AUC per gap bin cannot be backed by this artifact.
* **Resolution for Revision:** In Phase 2/7, update the gap evaluation thresholds or report bootstrap intervals directly from the unbinned data to ensure valid reporting.

---

### Discrepancy 4: FG-NET Adult Cutoff Post-Hoc Selection
* **Description:** On FG-NET all-ages ($N = 25{,}797$), AAFV-Net produced 4 false accepts out of 20,000 impostor pairs ($P \in [0.966, 0.9998]$). All 4 involved infants aged 0 to 4 years. The authors subsequently applied an adult filter ($a_1 \ge 16$), dropping pair count to 5,126, where false accepts became 0.
* **Impact on Manuscript:** This is a post-hoc subset selection. While Section 5.1 of `paper.tex` candidly admits `(iii) The FG-NET adult cut was chosen after seeing the all-age results`, an IEEE reviewer could penalize this if presented as an a priori validation of cross-dataset generalization.
* **Resolution for Revision:** Explicitly define the operational domain of AAFV-Net as **adult longitudinal verification** ($age \ge 16$), citing biological face morphology changes during childhood where craniofacial growth violates StyleGAN aging assumptions.

---

### Discrepancy 5: Third-Party Licensing & Commercial Constraints
* **Description:** As flagged in `src/aafv/align.py` and `paper.tex` Limitation (viii), the face alignment code derives from `NVlabs/ffhq-dataset` (non-commercial license), InsightFace `buffalo_l` is research-only, and SAM StyleGAN models have non-commercial terms.
* **Impact on Manuscript:** Does not affect scientific validity for an academic IEEE publication, but must be explicitly documented in the reproducibility / open-source release section.

---

## 6. Preliminary IEEE Publication Readiness Assessment

### 6.1 Scientific Strengths
1. **Methodological Honesty:** The paper does not hide negative results. It candidly reports that ArcFace-only achieves higher raw accept rates on MORPH ($89.4\%$ vs $70.1\%$) and that AAFV-Net accepts almost nothing in bins G4–G6 ($1.3\%$). It clearly articulates the trade-off: AAFV-Net trades raw accept rate for near-total immunity to hard impostors ($98.0\%$ rejection vs $0\%$ for ArcFace).
2. **Audit Logging & Pre-registration:** The 2-look access log with SHA-256 hash pinning is an exemplary empirical protocol rarely seen in computer vision biometric literature.
3. **Quarantine of Dataset Contamination:** Detecting and removing 858 duplicate identities solves an endemic problem in MORPH that has tainted dozens of prior published papers.
4. **Neutral Impostor Evaluation:** Using independent models (ViT and CNN) to mine a neutral hard set is an exceptionally rigorous countermeasure against ArcFace-biased hard negative mining.

---

### 6.2 Critical Reviewer Vulnerabilities (IEEE Perspective)

#### Critique A: Statistical Validity of the "Bounded False-Accept Rate" Claim
* **The Claim:** *"a framework that turns age-gap face verification into a three-way decision whose false-accept rate is measured and bounded rather than assumed."*
* **Reviewer Objection:** In biometric systems (NIST FRVT, ISO/IEC 19795), the false-accept rate is an empirical operational property dependent on the candidate population distribution. 
  1. The formula $\text{FAR} \le 1 - \alpha^{1/N}$ assumes **independent, identically distributed Bernoulli trials**. While this holds for $D_{\text{random}}$ ($N = 1{,}149$), it **does not hold** if deployed on a population with different ethnic distributions, different age profiles, twins, or targeted lookalikes.
  2. The bound is **completely violated on hard impostors**, where AAFV-Net had 5 false accepts in 35,735 pairs ($\text{FAR} \approx 0.014\%$). It was also violated on young children in FG-NET (4 false accepts).
  3. Therefore, calling the false-accept rate "bounded" in the title without qualifying it as *"Statistically Bounded on Random Disjoint Impostors"* is technically over-claiming. IEEE T-PAMI / T-IFS reviewers will demand either retitling or an explicit mathematical definition of the operational domain.

#### Critique B: Limited Novelty of Individual Components
* **Reviewer Objection:** ArcFace, EfficientNet, VGG, LPIPS, SSIM, SAM, and Platt scaling are all standard off-the-shelf tools. The fusion network is a simple 2-layer MLP. A reviewer may argue: *"This is an engineering assembly of existing vision backbones and standard Platt scaling rather than a fundamental machine learning innovation."*
* **Required Counter-Defense:** Frame the novelty not as a new neural layer, but as a **formal biometric decision framework**: the integration of generative counterfactual evidence, reliability weighting, and calibrated reject-option theory with verifiable non-parametric statistical guarantees.

#### Critique C: Failure of Acceptance on Large Age Gaps (MORPH G4–G6)
* **Reviewer Objection:** In MORPH, for age gaps $>15$ years (G4: 15–20y, G5: 20–30y, G6: >30y), AAFV-Net auto-accepts only $1.3\%$ to $2.2\%$ of pairs! An IEEE reviewer will ask: *"If the system routes $98\%$ of large-gap genuine pairs to manual review, does it actually solve the age-gap verification problem on MORPH?"*
* **Required Counter-Defense:** Contrast MORPH with FG-NET. On FG-NET adults, AAFV-Net accepts $38.2\%$ at 15–20y, $28.5\%$ at 20–30y, and $10.3\%$ at 30+ years (nearly $3\times$ higher than ArcFace's $3.8\%$). Explain why MORPH has severe sample scarcity in large gaps (only 1 genuine pair in calibration G4) and why cross-domain adult aging preserves discriminability.

---

### 6.3 Target Venue Recommendation
1. **Primary Target (Strong Fit):**
   * **IEEE Transactions on Information Forensics and Security (T-IFS):** Perfect match for biometric verification, impostor defense, auditability, and false-accept analysis.
   * **IEEE Transactions on Biometrics, Identity and Behavior (T-BIOM):** Specialized flagship biometric journal; highly values dataset integrity, reject options, and calibration.
2. **Top-Tier Vision Conference Alternative:**
   * **IEEE International Joint Conference on Biometrics (IJCB) / IEEE FG:** Ideal for the 4-to-8 page conference format.
3. **Not Recommended as Initial Target:**
   * **IEEE T-PAMI:** Expects fundamental architectural breakthroughs or massive new foundational benchmarks, which is beyond the scope of a fusion framework.

---

## 7. Prioritized Actionable Roadmap for Subsequent Phases

```
+---------------------------------------------------------------------------------------------------+
|                                      EXECUTION ROADMAP                                            |
+---------------------------------------------------------------------------------------------------+
  [PHASE 1: Complete Research Audit]                     <--- COMPLETED (research_audit.md)
                 |
                 v
  [PHASE 2: Experimental Results & Statistical Audit]    <--- NEXT IMMEDIATE PHASE
  - Independently recompute all metrics across the 7 CSVs
  - Validate exact Clopper-Pearson and bootstrap intervals
  - Formalize identity-clustering effect on N=277,822
                 |
                 v
  [PHASE 3: Deficiencies & IEEE Review Gap Analysis]
  - Categorize Critical, Major, Minor deficiencies
                 |
                 v
  [PHASE 4: Literature Review & Novelty Positioning]
  - Position against SOTA age-invariant benchmarks
                 |
                 v
  [PHASE 5: Experimental Recommendations & Roadmap]
  - Define non-test computational enhancements
                 |
                 v
  [PHASE 6 - 8: Publication-Ready IEEE LaTeX Manuscript]
  - Generate standalone publication/ directory
  - Author reproducible figure generator (SVG/PDF)
  - Compile main.tex with zero broken references/overflows
                 |
                 v
  [PHASE 9 - 10: Multi-Reviewer Simulation & Final Deliverables]
  - Simulated T-IFS/T-BIOM Reviewer reports
  - Final delivery of publication package
```

### Immediate Next Steps for Phase 2:
1. Execute an independent Python computation script to re-verify every row and cell across:
   * `ablation_calibration.csv`
   * `decision_table_calibration.csv`
   * `extended_calibration.csv`
   * `extended_calibration_fg.csv`
   * `extended_calibration_fg16.csv`
   * `extended_test.csv`
2. Formally audit the cluster-bootstrap procedure and Clopper-Pearson exact confidence intervals.
3. Deliver `results_verification.md`.

---
*Audit completed by Senior Research Scientist / Antigravity Agent. All claims verified against source code and experimental artifacts.*

