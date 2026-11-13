# AAFV-Net → CVPR: Final Report (Deliverables A–H)

> Phase 10 of the advisor's brief. Prepared 2026-11-13. This report consolidates and **supersedes** `STAGE1_ASSESSMENT.md` where they differ, because later phases found new evidence.
> Every claim is labelled:
> - **[V]** verified today from code, logs or models (file given);
> - **[R]** reported in AAFV-04, not re-executed;
> - **[P]** proposed;
> - **[O]** open.
>
> No new experiment on images has been run. Nothing in this report is a result of the proposed method.

**Supporting documents** (all under `CVPR_redesign/`):
| Phase | File |
|---|---|
| 1–3 | `STAGE1_ASSESSMENT.md`, `exp0/` (Experiment 0, coded and tested) |
| Log evidence | `log_analyses/LOG_FINDINGS.md` |
| 4 | `architecture_review/ARCHITECTURE_REVIEW.md` |
| Images | `image_audit/IMAGE_AUDIT.md` |
| 5 | `phase5_literature/RELATED_WORK.md` |
| 6 | `phase6_experiments/EXPERIMENT_PLAN.md` |
| 7 | `phase7_originality/ORIGINALITY_REVIEW.md` |
| 8 | `phase8_manuscript/MANUSCRIPT_BLUEPRINT.md` |
| 9 | `phase9_reproducibility/REPRODUCIBILITY_AUDIT.md` |

---

## A. Critical assessment of the current research

**What AAFV-Net does.**
- Five frozen similarity scores (ArcFace, EfficientNet, VGG-Face, LPIPS, SSIM), computed on the original pair and on SAM-age progressed pairs.
- A 947-parameter MLP fuses them. Guards for quality, branch probability and synthesis reliability follow.
- A three-way rule sits on top, with a zero-calibration-false-accept accept threshold [V, code].

**What the evidence now shows:**
| Finding | Status |
|---|---|
| At matched FPR, AAFV-Net ranks pairs **no better than ArcFace**. TAR@FPR 10⁻³: 0.992 vs 0.990 (0–4 y), 0.668 vs 0.668 (5–9 y), 0.649 vs 0.649 (10–14 y). The 70% vs 89% auto-accept gap comes from the threshold and guards | [V] LA1 |
| The **SAM branch adds nothing measurable.** All CIs of full vs direct-only overlap in every gap bin. The look-alike advantage exists equally without SAM, so it comes from fusion trained on mined negatives | [V] LA1–LA2 |
| The trained fusion uses ArcFace almost alone: direct-head weight −0.255 vs ≤ 0.016 for the other scores; logit swing 25.1 (ArcFace branch) vs 4.1 (SAM branch). SAM and R_sam effects are no larger than untrained controls | [V] probe |
| **MORPH long-gap genuine pairs are probably mislabelled.** 95–97% of 15–29 y genuine test pairs are impostor-like for both AAFV-Net and an independently trained ViT; every method is at chance at 15–19 y; at least one certain identity error in the audit sheet | [V] LA4, audit; confirmation needs E1 |
| The headline FAR certificate (0.349%) is arithmetically correct but does not tell methods apart: plain ArcFace earns the same bound. Its assumptions are compromised: the calibration split was used for development, and **the 4 persons behind the two top-scoring calibration impostor pairs were quarantined after their scores were seen. Without that, the guarded system accepted 0% at ρ = 0.20 (T_acc = 1.0129)** | [V] Stage 1 §B; `DRIVE_FINDINGS.md` |
| **Re-scored per pair (frozen model reproduces T_acc 0.956438 and 73.26% exactly):** with the 4 hand-quarantined persons put back, the guarded system accepts **0% at every ρ**. At matched FMR, generated-face evidence is worse than ArcFace alone and adding it changes TAR by 0. 18–29% of MORPH 15+ y 'same-person' pairs have different recorded sexes | [V] `drive_analyses/DRIVE_ANALYSES.md` |
| The FG-NET adult gain (51.9% vs 40.4%) comes with 18.2% false rejects. The four all-ages false accepts are infants that ArcFace alone rejected | [V] LA5, image audit |
| Factual corrections: the Look-2 model has 3 seeds, not 5; ArcFace inputs were misaligned; the Bonferroni bound rounds to 0.321%; the "55% similarity" Turnitin report is actually AI-writing | [V] Phase 9, Phase 7 |

**Genuine contributions of the existing work (narrow):**
- Good data-handling discipline: identity quarantine, person-disjoint splits, a logged test budget, transparent chronology.
- The observation that branch-probability guards make a zero-false-accept threshold feasible for a fused score.

**Why it is not competitive for CVPR.**
- No new visual representation or learning mechanism.
- The generative component has no demonstrated value.
- It is not better than its main baseline at matched operating points.
- The main dataset cannot test long gaps.
- The statistical headline is not a vision contribution.

**What remains valuable:** the data hygiene and protocol; the reject-option framing as an application layer; the insight that synthetic aging must be trusted *selectively*; the negative results, which now motivate the redesign; and the MORPH label-noise observation.

## B. Research directions (ranked)
| Rank | Direction | Idea | Novelty after the prior-art check | Main risk | CVPR suitability |
|---|---|---|---|---|---|
| **1** | **D.1 Reliability-weighted Age Transport (RAT)** | Frozen recognizer + age-conditioned transport and uncertainty in embedding space; synthetic aging used only for training, weighted by a learned reliability validated with an independent recognizer | Medium. Synthetic training data is prior art (MTLFace FT-Sel, Banerjee et al. 2023). New: frozen-backbone transport, gap-dependent uncertainty, learned and validated reliability | Experiment 0 may show generated faces carry no identity signal; gains over AdaFace may be small | Plausible only with clear long-gap gains at low FMR. Possibly Findings track |
| 2 | D.2 Test-time trajectory consistency | Verify by agreement of the two faces' generated age trajectories | Medium-low | The logs already show no test-time SAM value on MORPH; high cost | Borderline |
| 3 | D.3 Verification-discriminative aging generator | Fine-tune a generator with an impostor-contrastive identity objective | Higher | Weeks of GPU; crowded area | Plausible, but not on this timeline or hardware |
| 4 | D.4 / Paper B: controlled study and protocol | Does synthetic aging help? Strong baselines, long-gap protocol, MORPH audit | Low as a method; useful as evidence | – | Biometrics venue or workshop |

**Recommendation.** Run Experiment 0 first. If it returns GO, pursue D.1 (Paper A). If it returns NO-GO, or D.1 fails Gate B, write Paper B for a biometrics venue.
**Positioning:** no AIFR paper was found at CVPR 2024/2025 or ICCV 2023 (search not exhaustive). Paper A should be framed as learning from unreliable generative supervision on a frozen foundation model, with cross-age verification as the testbed.

## C. Proposed revised architecture
**Baseline of record (always built):** a frozen AdaFace recognizer (WebFace-trained, to avoid the MS-Celeb-1M-derived MS1MV2), cosine score, gap- and quality-conditioned calibration (about 6 parameters), and a three-way rule with conformal thresholds fitted on a fresh calibration split [P].

**RAT (D.1), only if E0 = GO** [P]:
- Transport T_θ(e, a, t) = normalize(e + g_θ[e, γ(a), γ(t)]).
- vMF concentration κ_θ(e, a, t).
- Loss: real-pair vMF NLL + synthetic-pair loss weighted by a learned reliability w_ψ(φ), where φ is computed with an independent recognizer h ≠ f + an impostor margin.
- Score: S = ½[κ₁₂ T(e₁, a₁, a₂)⊤e₂ + κ₂₁ e₁⊤T(e₂, a₂, a₁)].
- Test time: two backbone passes + an MLP of 1–3 M parameters, with **no generation**.

**Removed from AAFV-Net:** the four extra similarity scores, test-time SAM, the shared-target grid, R_sam as built, branch masking, the 11-input MLP, and the probability guards. Each was shown to have no measurable ranking effect, or to exist only to support another removed part [V, Phase 4].
Equations and the ablation ladder: `architecture_review/ARCHITECTURE_REVIEW.md` §3, `phase8_manuscript/MANUSCRIPT_BLUEPRINT.md` §3.5.

## D. Reviewer response and resolution matrix
| # | Criticism | Underlying problem | Correction | Required evidence | Status now |
|---|---|---|---|---|---|
| W1 | Limited novelty | No learned vision mechanism | RAT (D.1), or Paper B if it fails | E0 GO; E4 > E2 at long gaps; E7 | Design ready; **not run** |
| W2 | Generative branch unproven | Circular ArcFace check; no branch study | Independent recognizers, 2 generators, controls | E0, E4 rows 3–8, E5, E6, E10 | **Confirmed per pair at matched FMR on MORPH calibration: generated-only worse, added value 0 [V]** (`DRIVE_ANALYSES` DA3). SAM identity drift grows with shift [V, ArcFace-based]. E0 (independent recognizers, long gaps) **not run** |
| W3 | Loses to ArcFace | Decision layer, not discrimination | Compare at matched FMR and workload | E2 curves | **Explained from logs [V].** Curves on new data not run |
| W4 | Short gaps | MORPH composition **and probable label errors** | AgeDB, FG-NET, ECAF per pre-registered bin; MORPH short-gap only | E1, E2, E4 per bin | **Label errors established without images [V]:** 18–29% sex mismatch, 86–98% impostor-like at 15+ y (DA4). New evaluation **not run** |
| W5 | Certificate inconsistent | Mixed statements; calibration reuse; **post-hoc quarantine of the 4 top-scoring calibration impostors** | One statement per number; fresh calibration; demote; disclose the exclusion | E3; visual check of the 4 persons | Derivation done [V]. **Post-hoc exclusion confirmed and quantified [V]:** without it, 0% accept at every ρ (DA2). Duplicate-or-look-alike question open [O] |
| W6 | Weak baselines | ArcFace only; unconverged ViT | AdaFace, MagFace, MTLFace / FT-Sel, Banerjee-style fine-tune, PFE-style head | E2, E7 | Baselines chosen; **not run** |
| W7 | Post-hoc adult cut, small FG-NET | Cohort chosen after failure | Pre-registered scope (adults primary; children reported separately); larger external sets | E0, E2 on AgeDB and ECAF | Scope pre-registered in `exp0` [V] |
| W8 | Calibration | Probability mis-calibrated mid-range | Report as diagnostics; per-bin, per-dataset ECE | E8 | Look-1 diagnostics exist [R]; new **not run** |
| W9 | Fairness | Sex only, pair-level CIs | Race × sex × age with cluster CIs; review-rate disparity | E9 | **Not run** |
| W10 | Reproducibility, cost | Missing per-pair logs and weights; `Code/` not versioned | Reproducibility package; per-pair logging; runtime | E11; Phase 9 §6 | Audit done: 71/73 checks pass, 17/17 + 8/8 tests [V]; package **not built** |

## E. Prioritized experimental roadmap (detail: `phase6_experiments/EXPERIMENT_PLAN.md`)
| Order | Experiment | Needs | Gate |
|---|---|---|---|
| 1 | **E1 MORPH identity audit** | Images + 2 annotators, no GPU | – |
| 1 | **E0 generated-evidence probe** (coded) | AgeDB, FG-NET (+ sex labels), GPU inference | **Gate A** |
| 1 | **E2 baseline of record** | Same embeddings as E0 | – |
| 2 | E4 RAT + ablation ladder | Synthetic generation at scale; small training | **Gate B** |
| 3 | E5 generators, E6 reliability validation, E7 prior art | Inference; fine-tuning (E7 needs a bigger GPU) | – |
| 4 | E3 certificate; E8 calibration; E9 fairness; E10 qualitative; E11 runtime | CPU / light GPU | – |
| 5 | E12 degradation; E13 training negatives; E14 estimated ages | Optional | – |

**Timeline:** about 15 weeks to an ICCV-2027-class deadline (to be confirmed when announced).

## F. Revised manuscript blueprint (detail: `phase8_manuscript/MANUSCRIPT_BLUEPRINT.md`)
- **Paper A (if both gates pass):**
  - Working title *"Trusting Synthetic Aging Selectively: Reliability-Weighted Age Transport for Long-Gap Face Verification"*.
  - One central question; three contributions (method, controlled evidence, protocol), each dropped if its experiment fails.
  - 8-page budget; 9 equations with fixed notation; 3 tables; 7 figures. The figures include a SliderEdit-style probe figure and a SAM 3D-style cumulative ablation table.
- **Required by CVPR 2027 rules [V]:** a mandatory LLM Usage Statement; IRB and consent statements; justification or avoidance of MS-Celeb-1M-derived data; double-blind submission.
- **Paper B (fallback):** a controlled study, a long-gap protocol, and the MORPH audit.
- **Writing:** the authors write the prose (Phase 7). The blueprint gives content, evidence and placeholders only.

## G. Remaining research risks
1. **E0 may return NO-GO.** Generated aging may carry no identity signal under independent recognizers. The MORPH logs already lean that way, though MORPH cannot test long gaps.
2. **Small or saturated gains.** AgeDB-30 is about 98% for strong models; long-gap bins have few persons, so CIs may include zero.
3. **Narrow novelty.** MTLFace FT-Sel and Banerjee et al. cover synthetic training data; TimeBooth and recent generation work move fast. Re-check contemporaneous work (on or after 15 Sep 2026) before submission.
4. **Venue fit.** AIFR has had few recent CVF main-track papers.
5. **Data:**
   - Licences (MORPH, FG-NET, AgeDB, ECAF).
   - Celebrity sets overlap recognizer pretraining.
   - MORPH label noise affects training as well as testing.
   - FG-NET is small and needs sex annotation.
   - MS-Celeb-1M-derived backbones need justification.
6. **Ages.** Real deployments have only estimated ages; gains may shrink (E14).
7. **Compute.** The laptop GPU is likely enough for SAM, recognizers and RAT heads, but not for FADING at scale or prior-art fine-tuning. No software install has been approved.
8. **Reproducibility.** `Code/` is not versioned here; the Look-2 hash is not in the access log. The label-correction history is now known: 4 calibration persons were quarantined after their scores were seen, which is what made the reported operating point possible (`DRIVE_FINDINGS.md`).
9. **Originality and authorship.** No similarity check has ever been run. The flagged prose must be rewritten by the authors, and AI use disclosed truthfully.
10. **Time.** CVPR 2027 is no longer reachable (deadline 16 Nov 2026; registration closed 10 Nov).

## H. Final research readiness assessment
- **As it stands, the work is not ready for CVPR or ICCV, and no evidence yet supports a CVPR-level method contribution.**
  - The existing system's measurable behaviour reduces to ArcFace plus a conservative decision layer.
  - Its generative component shows no value in any logged artifact.
  - Its main dataset cannot test the paper's central claim.
- **What is ready:**
  - an honest diagnosis, verified against the code, logs and models;
  - a coded and tested go/no-go experiment;
  - a concrete, smaller architecture;
  - a full experiment and ablation plan with decision gates;
  - a verified literature map;
  - a venue-compliant manuscript blueprint;
  - an originality plan.
- **What would make it competitive:**
  1. E0 returns GO under independent recognizers.
  2. RAT beats the strong frozen-recognizer baseline and the synthetic-fine-tuning prior art at low FMR in the 15–29 y and 30+ y bins, with person-clustered CIs excluding zero, on AgeDB and FG-NET.
  3. The learned reliability demonstrably tracks independent identity preservation.

  None of these is known today.
- **If they fail,** the honest outcome is Paper B at a biometrics venue. It would still be a publishable, useful paper, built on the negative findings and the MORPH audit.
