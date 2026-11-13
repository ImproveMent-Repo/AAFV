# Phase 4: Reconsidering the AAFV-Net Architecture

> Brief Section 4: for every component, what purpose does it serve, is its contribution established, is it necessary, does it add needless complexity, can it be improved, and should it be retained, redesigned or removed? Then: is there a more coherent architecture?
> Prepared 2026-11-13 from the code, the logged results and the frozen models. No images and no new runs.

## 0. Evidence used
| Source | What it gives |
|---|---|
| `Code/AAFV_Net/src/aafv/*.py`, `scripts/*.py` | What each component actually computes |
| `log_analyses/` (LA1–LA5) | Ranking quality (AUC, TPR at matched FPR) per gap bin and per impostor pool for 23 variants; post-hoc test comparison; label-noise indicator |
| **New:** `architecture_review/probe_fusion.py` → `out/fusion_probe.csv`, `out/linear_heads.csv` | What the frozen fusion networks learned: linear-head weights per similarity score, and how far the fused logit moves when each input moves across its plausible range |
| AAFV-04 Tables VII, XII, XV | Decision-level ablations |

**How to read the probe.** `swing_X` is the average change in the fused logit when input X moves across a plausible range with the others held at typical values. Wd and Ws vary over bias ± 3‖w‖; age gap 5→25 y; quality 0.3→0.9; R_sam 0.2→0.9.
Two variants serve as *untrained controls*:
- `direct_only_mlp` was trained with the SAM input constant;
- `no_context` was trained with gap, quality and R_sam constant.

A network's response to an input it never saw vary is arbitrary. So a swing in `full` that is no larger than the control's is **not evidence that the input is used**.
The probe is not weighted by the data distribution, because no pair vectors exist. It shows what each network responds to, not how often.

## 1. Facts found while auditing (new)
1. **The Look-2 checkpoint is a 3-seed ensemble, not 5.** Every `ablations/variants/*/frozen.pkl`, including `full` (SHA `a47c916b…`, the source of the 70.07% figure), stores 3 MLPs. Look 1 used 5 (`thresholds.json`). AAFV-04 Section V-D and Table XV state 5 for the evaluated system. This needs correcting.
2. **The direct branch is ArcFace alone.** The learned weights on the five z-scored similarities in the `full` model (seed mean) are:

   | Branch | ArcFace | EfficientNet | VGG-Face | LPIPS | SSIM |
   |---|---|---|---|---|---|
   | Direct | −0.255 | 0.005 | −0.011 | 0.016 | −0.010 |
   | SAM | −0.101 | +0.149 | −0.057 | −0.004 | +0.023 |

   The other four measures are dead weight in the direct branch. In the SAM branch the largest weight is on EfficientNet, a generic ImageNet descriptor, with the opposite sign to ArcFace. That is not a clean identity signal. Signs of correlated inputs are hard to interpret, so I draw no stronger conclusion.
3. **ArcFace was given misaligned input.** `scripts/p5_faces.py` resizes the 256×256 FFHQ crop to 112×112 instead of using ArcFace's 5-point `norm_crop`. Every ArcFace number, inside AAFV-Net and for the ArcFace baseline, was computed this way.
4. **The fused score is, in effect, ArcFace plus offsets.** The swing for Wd is 25.1, against 4.1 for Ws. In ranking (LA1) the full system equals ArcFace at matched FPR in every populated bin.

## 2. Component-by-component audit

| # | Component | Purpose | Contribution established? | Evidence | Needed? | Decision |
|---|---|---|---|---|---|---|
| 1 | **Alignment** (dlib 68-pt → 256 FFHQ crop; reused for every network) | Common input geometry; SAM needs FFHQ alignment | Partly | Correct for SAM. **Wrong for ArcFace** (fact 3) | Yes | **Redesign:** FFHQ crop only as generator input; `norm_crop` 112×112 for every recognizer (as in Experiment 0) |
| 2 | **Quality Q** (5 hand-crafted measures; input and guard) | Defer poor images | Weak | Swing 0.87 vs 0.26 untrained, so used a little. Quality guard alone still gives 0% accept (Table XII). No degradation test ever run | Partly | **Replace** with the recognizer's own quality signal (AdaFace feature norm or MagFace magnitude), which is learned and standard. Report hand-crafted Q only as a covariate |
| 3 | **Five similarity measures** | Complementary cues | **No** | Direct head uses only ArcFace (fact 2). Dropping EfficientNet *raises* accept (74.1% → 81.3%). Ranking identical with ArcFace alone (LA1) | No | **Remove** EfficientNet, VGG-Face, LPIPS and SSIM. Keep one strong recognizer (AdaFace; report ArcFace and MagFace) |
| 4 | **SAM generation at test time** | Bridge the age gap with counterfactual faces | **No** | Full vs direct-only: all ranking CIs overlap (LA1). Look-alike gain equal without SAM (LA2). SAM swing 4.1 is no larger than the untrained control's 4.4. Up to 16 generations per pair, the dominant cost | Unproven | **Remove from test time.** If Experiment 0 says GO, move generation to *training* (Section 3) |
| 5 | **Shared-target 5-year grid** (K ≤ 7) | Trajectory consistency | **No** | Removing it raises test accept (70.1% → 83.9%); ranking unchanged; neutral-set rejection CIs overlap | No | **Remove.** If generation is kept for training, target ages become a sampling choice, not an architecture component |
| 6 | **Reliability R_sam** (hand-made: ArcFace identity + age error + quality + spread) | Down-weight bad syntheses | **No** | Swing 0.40 is below the untrained control's 0.51. Removing it changes accept by under 1 pp. Circular (uses ArcFace) | Not as built | **Replace** by a *learned* per-sample reliability, validated against identity preservation measured by an independent recognizer |
| 7 | **Branch masking** (p = 0.12) | Graceful fallback when SAM fails | Only for this design | Without it, accept 3.6%; ranking unchanged | Only if a test-time synthetic branch exists | **Remove** together with component 4 |
| 8 | **Linear heads + 11-input MLP** (4 constant slots; 3-seed ensemble) | Context-aware fusion | **No** beyond ArcFace | Fused logit is mostly Wd (fact 4). Gap and quality inputs used modestly (swing 0.9 vs 0.23/0.26 untrained). Four inputs are constant placeholders | No | **Remove.** Context (gap, quality) belongs in a calibrated or conditional score (Section 3) |
| 9 | **Platt calibration** | Probability output | Descriptive only | Monotone, so decisions are unchanged except through branch floors. Reliability diagram poorly calibrated mid-range (AAFV-04 Table X) | For reporting | **Keep as diagnostics only.** If a probability is shown to examiners, calibrate per gap bin and report ECE/Brier under shift |
| 10 | **Branch-probability guards** (Q_min, ρ, R_min) | Make a zero-FA accept threshold usable | For *this* fused score only | Without guards T_acc > 1 (0% accept). The guards then remove 97.4% − 79.7% ≈ 18 pp of genuine accepts (Look 1). Ranking unaffected (LA1) | No, in a single-recognizer system | **Remove.** Guarded ArcFace with ρ applied still loses 4 pp vs unguarded (93.6% vs 89.5%). Deferral should come from quality and uncertainty, judged on risk–coverage |
| 11 | **Accept rule:** T_acc = highest calibration impostor + margin | Zero calibration false accepts | Statistically valid only under the B.3 conditions | A single mislabelled or duplicate calibration pair sets T_acc. The top calibration impostor (P = 0.980) looks like the same person (`q/audit/audit_different_top50.jpg`) | The *idea* of a certified accept threshold, yes | **Redesign:** a conformal/order-statistic threshold that allows k > 0 calibration errors at a stated target FAR, fitted on a cleaned, never-developed-on calibration split. Report the certificate as an operating-point check, not a contribution |
| 12 | **Reject rule:** T_rej = β-quantile of genuine calibration P | Bounded false rejects | Holds in-distribution only | MORPH test 0.54% ≤ 1%. **FG-NET adults 18.2%** | Yes, for three-way use | **Redesign:** gap-conditional (or weighted-conformal) quantile; must be validated on an external set |
| 13 | **Training negatives:** half ArcFace-mined | Learn look-alike rejection | Yes, but in-distribution | Mined look-alikes scored below even impostor-like genuine pairs; an independent ViT does the opposite (LA4) | Yes, with an honest evaluation | **Keep**, but evaluate only on independently mined (neutral) sets and external data |
| 14 | **MORPH identity labels** (858-person quarantine) | Clean evaluation | Partly | 95–97% of 15–29 y genuine test pairs impostor-like for two unrelated models; one person id spans four filename prefixes; certain visual error in the audit sheet (LA4) | Yes | **Redesign:** a linkage audit against the MORPH index plus visual sampling. Use MORPH only for short gaps until it is cleaned |
| 15 | **Three-way decision** (accept / review / reject) | Operational deferral | Operationally meaningful | Valued by the reviewer | Yes, as an application | **Keep as the application layer**, compared at matched FAR and matched review workload |

**Summary of the audit.** Of the 15 components, 2 are kept as they are, 1 is kept with an honest evaluation, 6 are redesigned, and 6 are removed. Every removed component either has no measurable effect on ranking or exists only to support another removed component.
**The minimal system that reproduces AAFV-Net's ranking is ArcFace's cosine.** On the MORPH test split, plain unguarded ArcFace already auto-accepts 93.58% of genuine pairs with zero random-impostor false accepts (Table VII).

## 3. A more coherent architecture

The audit leaves one strong recognizer, a decision layer, and an open question: can generated faces help at long gaps? There are two coherent designs. Experiment 0 decides between them.

### 3.1 Baseline of record: Gap-Aware Selective Verification (needed in either case)
```
I1, I2 ──norm_crop 112──► frozen recognizer f (AdaFace IR-101; also ArcFace, MagFace)
                              │ e1, e2, quality q1, q2 (feature norms)
                              ▼
     s = cos(e1, e2);  context c = [Δage (estimated), min(q1,q2)]
                              ▼
     gap-conditioned calibration  P(same | s, c) = σ(a(c)·s + b(c))      (logistic, few parameters)
                              ▼
     three-way rule with conformal thresholds at target FAR α and FRR β, fitted on a fresh calibration split
```
- **Components:** 1 recognizer and about 6 learned parameters. No generator, no guards.
- **Role:** the honest fallback (Experiment 0 NO-GO), and the ablation base for 3.2: 3.2 minus the transport head equals 3.1.
- **Novelty:** low. This is not the CVPR contribution.

### 3.2 Primary candidate (only if Experiment 0 = GO): Reliability-weighted Age Transport (D.1)
```
TRAINING                                                         TEST (no generation)
real longitudinal pairs (Iy, ay; Io, ao) ──f──► ey, eo            I1, I2 ─f─► e1, e2
generator G (SAM-age / FADING): G(I, t) ──f──► target ê_t                 │
independent recognizer h ≠ f ──► identity-preservation features φ        ▼
                                                                 ẽ12 = T(e1, a1→a2),  ẽ21 = T(e2, a2→a1)
transport head  T_θ(e, a→t) = normalize(e + MLP_θ[e, φ(a), φ(t)])        │
uncertainty     κ_θ(e, a, t)  (vMF concentration)                        ▼
reliability     σ_ψ(φ) for each synthetic target (learned)        S = ½[κ12·cos(ẽ12, e2) + κ21·cos(e1, ẽ21)]
loss: vMF-NLL on real pairs + reliability-weighted                       ▼
      synthetic loss + margin against gap-matched impostors      three-way rule as in 3.1
```
- **Inputs:** two aligned faces and their (estimated) ages.
- **Output:** a gap-aware score with uncertainty, then the three-way decision.
- **Size:** test time is two backbone passes plus a 1–3 M parameter head (vs AAFV-Net's up to 16 generations per pair). Training needs one generation pass over the training images.
- **What differs from prior work:**
  - The backbone stays frozen.
  - Age is handled by a conditional transport in embedding space, not by removing age from the representation (OE-CNN, DAL, MTLFace) or by test-time synthesis (AAFV-Net).
  - Synthetic data enters through a *learned, continuous* reliability that is checked against identity preservation under an independent recognizer. MTLFace FT-Sel instead uses a quality-based GMM *selection* (prior-art check, Stage-1 Section L).
- **What survives from AAFV-Net:** the idea that synthetic faces are unreliable and must be weighted (now learned), the age-gap context (now a conditioning variable), the reject option (now the application layer), and the data hygiene.

### 3.3 Ablation plan for 3.2 (each row isolates one component, as the brief requires)
| Ablation | Isolates | Expected if 3.2 is right |
|---|---|---|
| Recognizer cosine (3.1 without calibration) | Everything | Lowest long-gap TAR@FMR |
| 3.1 (gap-conditioned calibration) | Context without transport | Small gain at long gaps |
| 3.2 trained on real pairs only | Transport head | Gain at gaps well covered by real data |
| 3.2 + synthetic, unweighted | Synthetic supervision | Gain at long gaps, but hurt by bad syntheses |
| 3.2 + synthetic, fixed R_sam-style weights | Hand-made reliability | Between unweighted and learned |
| **3.2 full** (learned reliability) | Learned reliability | Best long-gap TAR@FMR; σ correlates with independent identity preservation |
| 3.2 full without κ (no uncertainty) | Uncertainty | Worse risk–coverage at matched FAR |
| Generator swap (SAM-age ↔ FADING) | Generator dependence | Ranking of variants unchanged |
| Recognizer swap (AdaFace ↔ ArcFace ↔ MagFace) | Backbone dependence | Gains persist |
| MTLFace FT-Sel-style fine-tuning on synthetic faces | Closest prior art | 3.2 at least as good, at lower cost and with a frozen backbone |

## 4. What this phase changes in the plan
1. The current architecture should **not** be carried into the CVPR paper. Most of it has no measurable effect, and the part that matters is ArcFace.
2. **Build 3.1 first, as soon as images are available.** It needs no generator, runs on the laptop GPU, and is the baseline every later claim is measured against. On MORPH it can be compared directly with AAFV-Net's logged test results (post hoc, descriptive), because the test pairs are identified by `pair_id`.
3. 3.2 is built only after Experiment 0 = GO. If NO-GO, the paper becomes 3.1 plus the MORPH label-noise and decision-layer findings, which fits a biometrics venue (T-BIOM/IJCB), not CVPR.
4. **Corrections for any future manuscript:** the 3-seed Look-2 ensemble; ArcFace misalignment; the dead similarity measures and constant inputs; MORPH long-gap label noise.
