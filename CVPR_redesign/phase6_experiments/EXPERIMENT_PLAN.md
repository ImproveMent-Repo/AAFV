# Phase 6: Experimental Design and Ablation Strategy

> Brief Section 6: a complete plan that can establish the value of the proposed method. For every experiment: question, hypothesis, dataset, split and identity-disjoint protocol, models and baselines, procedure, metrics, statistics, expected outputs, manuscript section and reviewer concern addressed.
> Separate what existing artifacts can do from what needs new data, training or compute.
> Prepared 2026-11-13. Nothing in this file has been run. Every result slot is empty until it has been produced and checked.

## 0. Ground rules for every experiment
1. **No MORPH test-split use.** The MORPH test split is spent. MORPH test outputs may be re-read post hoc and descriptively only, as in LA4.
2. **Identity-disjoint folds.** Persons are assigned to folds before any pair is built, and all pairs are formed within a fold (as `exp0/s3_pairs.py` does).
3. **Pre-registration.** Each external confirmatory evaluation (AgeDB, FG-NET, CALFW, ECAF) gets one pre-registered look with a committed analysis plan.
4. **Fresh calibration.** Thresholds and certificates for any new method come from a calibration split never used during development.
5. **Statistics.**
   - Two-way person-cluster bootstrap (1,000 replicates; the `exp0/common.py` implementation).
   - Paired differences computed on the same replicate.
   - Holm correction within each pre-declared family of tests.
   - Binomial or order-statistic bounds only for impostor pools with no shared persons.
6. **Log per-pair scores for every method.** Their absence is what blocked matched-FMR comparisons in AAFV-04.
7. **Fixed gap bins** (pre-registered): 0–4, 5–14, 15–29 and 30+ years.
8. **Scope.** The adult stratum (all ages ≥ 16) is primary. Children are always reported as a separate stratum, never dropped.

## 1. Resource classes
| Class | Meaning | Needs |
|---|---|---|
| **R0** | Done from existing logs and artifacts | Nothing |
| **R1** | CPU only, on images or outputs once available | Images and an annotator, no GPU |
| **R2** | Inference with public pretrained weights | GPU recommended (the laptop's RTX 4060, 8 GB, after a CUDA PyTorch install); no training |
| **R3** | Small training: heads or calibrators on frozen embeddings | Minutes to hours of GPU; precomputed embeddings |
| **R4** | Substantial: generator generation at scale, backbone fine-tuning, reimplemented prior art | Days of GPU, possibly more than 8 GB (FADING unverified) |

## 2. Already completed (R0)
| ID | What | Result | File |
|---|---|---|---|
| D0 | Certificate re-derivation | All five FAR numbers arithmetically correct. Calibration reuse and the label-correction path threaten validity | `STAGE1_ASSESSMENT.md` §B |
| LA1–3 | Matched-FPR ranking per gap bin and impostor pool, 23 variants | AAFV-Net equals ArcFace; the accept gap comes from the decision layer; no measurable SAM value | `log_analyses/` |
| LA4 | Post-hoc test comparison and label-noise indicator | 95–97% of MORPH 15–29 y genuine pairs impostor-like for two unrelated models | `log_analyses/` |
| LA5 | FG-NET by bin, all variants | No usable non-SAM comparator; 18% false rejects | `log_analyses/` |
| P1 | Frozen-model probe | Direct branch is ArcFace; fused logit dominated by it; Look-2 model is 3 seeds | `architecture_review/` |
| Q1 | Qualitative audit of the supplied images | Edits concentrate on eyes and brows; FG-NET infant false accepts | `image_audit/` |

## 3. Experiment cards

### Critical
| ID | E0: Does generated aging carry identity evidence? (the go/no-go) |
|---|---|
| Question | Under recognizers outside the pipeline, does adding G(I₁→a₂) and G(I₂→a₁) improve separation of genuine from gap-matched impostor pairs at long gaps? |
| Hypothesis | H1: ΔTAR@FMR > 0 in the 15–29 y and/or 30+ y adult bins. H0: no gain. The age-only control shows no gain under either |
| Data / split | AgeDB and FG-NET (sex annotated); 5 person-disjoint folds; age-matched-swap impostors |
| Models | AdaFace IR-101, MagFace iResNet-100 (decision); ArcFace (reference). Generators: SAM-age, FADING |
| Procedure | Already coded and tested: `exp0/s1`–`s6` |
| Metrics | TAR@FMR 10⁻³ (10⁻² if fewer than 3,000 impostors in a bin), AUC, identity preservation per age shift, generation and detection failure rates |
| Statistics | Bonferroni over 8 tests (99.375% intervals); cluster bootstrap; cross-fitted fusion |
| Output | `results/REPORT.md`, `decision.json`, and the success/failure figure |
| Paper | Motivation probe in the method section (like SliderEdit's Fig. 2); appendix detail |
| Addresses | W2, reviewer question 2, Priority 2A/2B |
| Class | R2 (SAM about 2 GPU-hours per 100k faces as reported; FADING about 90 s per image plus 26 s per age as reported) |

| ID | E1: MORPH identity-linkage audit |
|---|---|
| Question | Are MORPH long-gap genuine pairs in this pipeline mislabelled? |
| Hypothesis | Most 15–29 y genuine pairs are wrong-identity or wrong-age (LA4). Short-gap pairs are mostly correct |
| Data | Random sample of genuine pairs per gap bin (e.g. 50 per bin, 200 in all), drawn by seed *before* viewing; the MORPH index file |
| Procedure | (a) Check each pair's filename prefixes and record ids against the index. (b) Two annotators judge same / different / unsure, blind to the bin and to each other. (c) Cohen's κ |
| Metrics | Error rate per bin with Wilson CIs; inter-annotator agreement |
| Output | `morph_audit.csv`, a grid of example pairs (shown only if the licence allows) |
| Paper | Data section; possibly a short data-hygiene finding |
| Addresses | W4; the reliability of every MORPH number; reviewer reproducibility concern (W10) |
| Class | **R1: needs only images and two people**. The cheapest high-value experiment |

| ID | E2: Baseline of record (gap-aware selective verifier, architecture review 3.1) |
|---|---|
| Question | How far do strong frozen recognizers get at each gap bin, and what does gap- and quality-aware calibration with a reject option add? |
| Hypothesis | TAR@FMR falls with gap for every backbone. Gap-conditioned calibration gives small, consistent gains in risk–coverage. AdaFace is at least as good as ArcFace, which is at least as good as MagFace at long gaps |
| Data / split | AgeDB (all within-identity pairs binned, plus the AgeDB-30 protocol for comparability), FG-NET, CALFW, CACD-VS (medium gaps only), ECAF (child stratum), MORPH calibration (short gaps; after E1) |
| Models | ArcFace (`norm_crop` aligned), AdaFace, MagFace: cosine; + Platt; + gap-conditioned logistic calibration; + quality-based deferral |
| Procedure | Embed once (reuses `exp0/s5`), fit calibrators on training folds, set thresholds on the calibration fold, evaluate the held-out fold; one confirmatory look per dataset |
| Metrics | TAR@FMR 10⁻³/10⁻⁴ per bin; ROC and DET; risk–coverage and AURC; FAR–coverage; review workload at matched FAR; AgeDB-30 accuracy (comparability only) |
| Output | Main results table and curves |
| Paper | Results: baselines; and the base row of every ablation |
| Addresses | W3, W6, W4; Priority 3 |
| Class | R2 + R3 (minutes) |

| ID | E3: Statistical guarantee for the new system |
|---|---|
| Question | What FAR and FRR can be guaranteed for the final operating point, and under which assumptions? |
| Procedure | Use a fresh, cleaned calibration split. Apply an order-statistic threshold allowing k ≥ 0 errors at target α (exact binomial). Build a person-disjoint impostor pool for the bound. Use cluster-bootstrap CIs for correlated pools. Run a shift check (weighted conformal) on FG-NET and AgeDB. State the assumptions in writing |
| Metrics | Certified FAR at 95% confidence; observed held-out FAR and FRR; FRR under shift |
| Output | A one-paragraph proposition with its assumptions; a sample-size table |
| Paper | Application section or appendix (supporting, not a headline) |
| Addresses | W5, Priority 5 |
| Class | R1 (CPU, after E2/E4 scores exist) |

| ID | E4: Main method, reliability-weighted age transport (D.1). Run only if E0 = GO |
|---|---|
| Question | Does a frozen-backbone transport head with gap-dependent uncertainty, trained on real plus reliability-weighted synthetic aging, improve long-gap TAR@FMR over E2? |
| Hypothesis | Gains are concentrated in the 15–29 y and 30+ y bins. Learned weighting beats both unweighted and fixed weighting |
| Data / split | Training: MORPH train (short gaps, cleaned per E1) + AgeDB/FG-NET training folds + synthetic targets. Evaluation: held-out folds and external sets as in E2 |
| Models | AdaFace frozen (also ArcFace and MagFace); transport MLP (1–3 M parameters); vMF uncertainty; reliability network on independent-recognizer identity features |
| Procedure | Precompute embeddings of real and generated faces, train heads (5 seeds), select on the training-validation fold, and evaluate once per external set |
| Metrics | As E2, plus the correlation between learned reliability and independent identity preservation |
| Output | Main table; ablation table (Section 4) |
| Paper | Method and main results |
| Addresses | W1, W2, W4, Priority 1 |
| Class | R3, after generation (R2/R4) |

### High priority
| ID | Experiment | Question → hypothesis | Data / models | Metrics and statistics | Paper / addresses | Class |
|---|---|---|---|---|---|---|
| E5 | **Generator comparison** | Does the method depend on one generator? → Variant ranking unchanged across SAM-age, FADING (and a StyleGAN-latent method such as Luevano et al., if code is available) | E4 setup | ΔTAR per generator; identity preservation per generator, per age direction and per facial region | Ablations / W2, 2C | R2–R4 |
| E6 | **Reliability validation** | Does the learned reliability predict identity preservation, and does it prevent harm? → Spearman ρ > 0; the share of decisions harmed by synthetic data falls with weighting | E4 outputs; independent recognizer (MagFace if AdaFace is the backbone) | Spearman ρ with cluster CI; harm/benefit flip counts by reliability decile | Analysis / 2D | R3 |
| E7 | **Closest prior art** | Is the frozen-backbone transport better or cheaper than fine-tuning on synthetic data? | MTLFace public model (if weights exist) and FT-Sel-style fine-tuning; Banerjee-style ArcFace fine-tune on quality-filtered synthetic faces | Same metrics as E2; training cost | Main table / W6, W1 | R4 |
| E8 | **Calibration diagnostics** | Are probabilities usable under shift? | E2/E4 scores | ECE, MCE, Brier, NLL, slope and intercept per bin, dataset and sex; reliability diagrams | Appendix / W8 | R1 |
| E9 | **Demographic subgroups** | Do accept, review and error rates differ by sex, race (MORPH), age group, and their intersections? | E2/E4 outputs with metadata (AgeDB sex; MORPH race and sex) | Rates and differences with cluster-bootstrap CIs; review-rate disparity | Analysis / W9 | R1 |
| E10 | **Failure analysis** | Where do the method and baselines fail? | E0/E4 outputs | Qualitative grids (success/failure of synthesis; false accepts and false rejects); failure taxonomy by gap, quality, age direction and region | Qualitative section / W2, Q1 follow-up | R1 |
| E11 | **Runtime and memory** | Cost per pair of 3.1, D.1 and AAFV-style test-time generation | Laptop GPU | p50/p95 latency, throughput, peak VRAM | Discussion / W10, reviewer question 8 | R2 |

### Medium priority
| ID | Experiment | Purpose | Class |
|---|---|---|---|
| E12 | Degradation robustness (blur, JPEG, low resolution) with quality-based deferral | Threat-model coverage (W12 in the TIFS review) | R2 |
| E13 | Training negatives with vs without mined look-alikes, evaluated on an independently mined hard set | Tests the "in-distribution hard set" explanation (LA4 Finding 4) | R3 |
| E14 | Estimated vs ground-truth ages at test time | Realism of the age input; sensitivity of gains to age-estimation error | R2 + R3 |

## 4. Ablation strategy for the main method (E4)
Each row changes exactly one thing relative to the row above or to the full model. Rows 1–3 also serve as the Priority 2A branch study, and rows 4–6 as the Priority 2E component study.

| # | Variant | Isolates | Prediction if the method works |
|---|---|---|---|
| 1 | Recognizer cosine | – | Reference |
| 2 | + gap- and quality-conditioned calibration (E2) | Context | Small gain |
| 3 | + transport head, real pairs only | Transport | Gain where real long-gap data exist |
| 4 | + synthetic targets, unweighted | Synthetic supervision | Mixed: gains at long gaps, losses from bad syntheses |
| 5 | + synthetic, fixed hand-made weights (R_sam-style) | Hand-made reliability | Between rows 4 and 6 |
| 6 | **+ synthetic, learned reliability (full)** | Learned reliability | Best long-gap TAR@FMR |
| 7 | Full without uncertainty κ | Uncertainty | Worse risk–coverage at matched FAR |
| 8 | Full with generated-only test-time evidence (AAFV-style, for reference) | Test-time synthesis | No better than row 6, at far higher cost |
| 9 | Generator swap | Generator dependence | Same ordering of rows |
| 10 | Backbone swap | Backbone dependence | Same ordering of rows |
| 11 | Number of synthetic target ages per image (1, 3, 5) | Synthetic budget | Saturating gain |

**Families for multiplicity:**
- Rows 2–8 vs row 1 in the two long-gap bins (Holm).
- Generator and backbone swaps are reported descriptively.

## 5. Order, dependencies and decision gates
```
E1 (MORPH audit, R1) ──┐
E0 (go/no-go, R2) ─────┼──► GATE A: E0 = GO? ── yes ──► generation at scale ─► E4 ─► E5, E6, E7 ─► E3 (final certificate)
E2 (baseline, R2/R3) ──┘                     └─ no ───► paper = E2 + E1 + decision-layer and label-noise findings (biometrics venue)
E8, E9, E10, E11 run on whichever system is final; E12–E14 if time allows.
```
**Gate B (after E4):** if row 6 does not beat row 2 at matched FMR in a long-gap bin with a CI excluding 0, report it, stop claiming a method contribution, and fall back as at Gate A.

## 6. What existing artifacts can and cannot do
| Can be done now, without images | Needs images (no GPU) | Needs GPU inference | Needs training |
|---|---|---|---|
| D0, LA1–LA5, P1 (done); writing the E3 proposition; preparing E1 sampling lists *if the MORPH pair list is available* | E1; FG-NET sex annotation for E0; E10 qualitative grids | E0, E2 embeddings, E5 generation, E11, E12, E14 | E4, E6, E7, E13 |

## 7. Rough timeline to an ICCV-2027-class deadline (about 15 weeks; deadline to be checked when announced)
| Weeks | Work |
|---|---|
| 1 | Data access (AgeDB, FG-NET, CALFW, ECAF); environment; E1 sampling and annotation; FG-NET sex annotation; commit the E0 pre-registration |
| 2–3 | E0 and E2 (embeddings shared) → **Gate A** |
| 4–6 | Synthetic generation at scale; E4 rows 1–7 |
| 7–8 | E5, E6, E7 → **Gate B** |
| 9–10 | E3, E8, E9, E10, E11 |
| 11–15 | Writing (Phase 8 blueprint), figures, supplementary, internal review |

## 8. Mapping to the review and the advisor's priorities
| Concern | Experiments |
|---|---|
| W1 / Priority 1: novelty | E0 (gate), E4, E7 |
| W2 / Priority 2: value of generated evidence | E0, E4 rows 3–8, E5, E6, E10 |
| W3 / Priority 3: vs ArcFace and strong baselines | LA1–3 (done), E2, E7 |
| W4 / Priority 4: long gaps | E1, E2, E4 per gap bin; ECAF stratum |
| W5 / Priority 5: statistics | D0 (done), E3 |
| W6: modern baselines | E2, E7 |
| W7: generalization, post-hoc cohort | Pre-registered scope; external confirmatory looks |
| W8: calibration | E8 |
| W9: fairness | E9 |
| W10: reproducibility and cost | Per-pair logging, released scripts, E11 |
