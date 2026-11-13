# AAFV-Net → CVPR: Stage 1 Assessment, Statistical Audit, and Research-Direction Recommendation

> Prepared 2026-11-13. Stage 1 of the staged plan in the advisor brief (understand → audit → recommend direction).
> Nothing in the manuscript has been rewritten. No experiment has been run. Every number below is either
> re-computed from a file in this repository (`[VERIFIED]`, with path), quoted from AAFV-04 (`[REPORTED]`),
> or a proposal (`[PROPOSED]`). Facts about external datasets, weights and papers that I could not check
> against the original source are marked `[VERIFY]`.

Documents read in full or in the parts relevant here: `AAFV-04.pdf` (12 pp., all), `AAFV_Net_CVPR_2027_Style_Review.docx` (all),
`AAFV-04_Report.pdf` (Turnitin, all 14 pp. incl. highlight layout), SliderEdit (CVPR 2026, body in full),
SAM 3D (CVPR 2026, intro, formulation, architecture, training overview, experiments, analysis, conclusion).
`Alike_papers/1.pdf` is MimicTalker (CVPR); it was not part of the brief and was only identified.
Code inspected: `Code/AAFV_Net/{configs,src/aafv,scripts/p78_calibrate_freeze.py,scripts/p_quarantine.py}` and all logged CSV/JSON/NPZ outputs.

---

## 0. Two facts that change the plan

**0.1 CVPR 2027 cannot be the next submission.** The official CVPR 2027 call lists paper registration on
**10 Nov 2026 (AoE, already passed)** and the paper deadline on **16 Nov 2026 AoE**, three days from now, with no extension
([CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers), [Dates](https://cvpr.thecvf.com/Conferences/2027/Dates)).
Even if a registration exists, the experiments in this document need weeks of GPU work.
Realistic CVF-family targets are **ICCV 2027** (deadline usually early March, `[VERIFY]` once announced) or **CVPR 2028**
(about November 2027). The CVPR/ICCV biometrics workshops are a fallback. The research plan below is written for an
ICCV-2027-class submission (roughly 14–16 weeks).

**0.2 Almost nothing new can be computed from what is on this machine.** `[VERIFIED]` The repository holds:
per-pair *fused probabilities only* for the Look-1 MORPH test (`q/report/test_pair_zones_look1.csv`: pair_id, set, label,
gap_bin, gender, P, zone), aggregate rate tables (`ablations/*.csv`), Siamese-ViT/CNN and VLM per-pair logits
(`baselines/*/scores*.npz`), and 26 small `frozen.pkl` threshold/variant files. It does **not** hold: MORPH or FG-NET images,
aligned crops, any SAM output, the `pair_vectors_*.csv` feature files, the `fusion_seed*.pt` weights, per-pair ArcFace scores,
or anything for AgeDB/CALFW/CACD. `configs/params.yaml` has empty data paths. **Every experiment that the advisor's five
priorities require needs the original compute environment or a full re-run on licensed data.** Before planning further,
the team must say where `artifacts/` (p5 vectors, crops, SAM caches, model weights) lives and how much GPU time is available (Section 10).

---

## A. Critical assessment of the current research

### A.1 What AAFV-Net does
For an aligned pair (I₁, I₂) with ages a₁ ≤ a₂ it computes five frozen similarities (ArcFace, EfficientNet-B0, VGG-Face, LPIPS, SSIM)
on the original pair and on SAM age-progressed pairs at a 5-year grid (forward, backward, up to 7 shared targets). It then
projects each branch to one logit, fuses 11 scalars in a 947-parameter MLP (5 seeds, Platt), and applies guards (quality, branch-probability
floor ρ, SAM reliability R_sam) and a three-way rule (T_acc = highest guard-passing calibration-impostor P + margin; T_rej = β-quantile of genuine P).

### A.2 What is genuinely supported by evidence `[VERIFIED]` / `[REPORTED]`
1. **Guards make a zero-calibration-FA accept threshold usable** for a fused score. Without probability floors, T_acc = 1.005 and acceptance is 0% (Table XII).
   This is a real but narrow engineering observation.
2. **The fused score separates ArcFace-mined look-alikes from genuine pairs better than raw ArcFace does** (98.04% vs 0% auto-reject at β = 0.01).
   AAFV-04 itself warns that half of the training negatives were mined the same way, so D_hard is in-distribution. The model-neutral set
   (57.49% vs 28.46%) is the fairer number.
3. **On FG-NET adults the fused system accepts more genuine pairs than ArcFace in every gap bin** (51.92% vs 40.38%). This comes with
   18.20% false rejects against a 1% target, so part of the gain comes from deciding wrongly rather than deferring.
4. **The protocol work** (quarantine of 858 duplicate identities, person-disjoint splits, logged test budget, chronology table) is good practice.
   It is also not a CV contribution.

### A.3 Why it is not competitive for CVPR (agreeing with W1–W4 of the review, plus points the review did not raise)
- **No new visual representation, no new learning mechanism.** Every learned part is either frozen (all five extractors, SAM) or a 947-parameter
  score combiner. A CVPR reviewer will read it as score-level fusion plus a selective-classification threshold. AAFV-04 says so itself in Table I.
- **The generative branch has no demonstrated value.** Removing shared targets *raises* MORPH test acceptance from 70.07% to 83.91% with
  overlapping neutral-rejection CIs. Removing R_sam changes calibration acceptance by under 1 pp. SAM-only MLP accepts 0%.
  Identity preservation has never been measured with a recognizer outside the pipeline (R_i uses ArcFace, which is also a fusion input).
- **It loses to its own principal baseline on the main dataset.** On MORPH genuine pairs it auto-accepts 70.07% vs 89.45% for guarded ArcFace,
  with about 3× the review load. On MORPH the evaluated full system is not even the best of its own variants.
- **The main dataset cannot test the paper's own claim.** 23,631 of 24,305 MORPH test genuine pairs (97.2%) have gaps under 5 years.
  Gaps of 15 years or more total 224 pairs `[VERIFIED: test_pair_zones_look1.csv]`.
- **(New) The headline statistical claim does not tell methods apart.** Every method in Table VII, including plain ArcFace, has 0/1,170
  calibration and 0/1,149 test random false accepts, so every method gets the *same* 0.349% certificate. The certificate is a property
  of the pool size n, not of AAFV-Net (Section B.4).
- **(New) Name collision.** At CVPR, "SAM" means Segment Anything (one of the two exemplar papers is *SAM 3D*). Calling the age generator
  "SAM" will confuse reviewers. Use "SAM-age (Alaluf et al.)" or, better, make the method generator-agnostic.

### A.4 What remains scientifically valuable and should be carried forward
- The data hygiene (quarantine, person-disjoint splits) and the logged-look discipline.
- The idea of treating synthetic age evidence as *unreliable* and not trusting it unconditionally. This is the one design intuition the
  review praises, and it can become the centre of a real method (Section D).
- The three-way decision rule, demoted to an application/evaluation layer rather than a contribution.
- The negative results (MORPH deficit, FG-NET false-reject failure, pediatric false accepts). These are now motivation for a better method, not something to hide.

### A.5 Lessons from the two exemplar CVPR papers (presentation and method, not content to copy)
| What the exemplar does | SliderEdit | SAM 3D | What AAFV-Net lacks |
|---|---|---|---|
| One precisely stated gap | Instruction edits are applied with fixed strength | Single-image 3D fails in cluttered natural scenes because of a data gap | AAFV-04 states four loosely linked contributions |
| A motivating probe before the method | Fig. 2: interpolating instruction tokens toward padding already changes edit strength, so control is possible | Psychophysics/recognition argument plus the data-barrier analysis | No experiment shows that age-progressed evidence carries identity information |
| One mechanism that follows from the probe | PPS loss + selective-token LoRA | Data engine + multi-stage training recipe | Mechanism = assembly of frozen parts |
| One-line problem formulation | Per-instruction strength α_i | Learn q(S,T,R,t,s \| I,M) ≈ p | Formulation is about thresholds, not about vision |
| Metrics built for the claimed property | Continuity, extrapolation, disentanglement | Shape/layout metrics + human preference | Metrics measure the decision rule, not the claimed age-awareness |
| Ablations that establish causality | Variants vs CFG baselines | Cumulative stage table (Tab. 4) | Ablations show the guards are needed, not that the age evidence helps |
| A benchmark where none existed | Facial-edit evaluation set | SA-3DAO | No long-gap verification protocol exists in the project |

The most transferable lesson is SliderEdit's: **show a cheap probe that the signal exists, then build the smallest mechanism that exploits it.**
That is exactly what AAFV-Net is missing, and it is Experiment 0 below.

---

## B. Priority 5 first: re-derivation of the FAR statement (done now, from logged files)

I am doing this first because it is the only priority that existing artifacts can fully settle.

### B.1 Derivation (correct as written in AAFV-04)
Let s(z) = P if the guards pass, else −∞. Let s₁…s_n be the scores of n calibration random-impostor pairs, and s_new the score of a future random impostor pair,
all i.i.d. given a scorer fixed independently of these n pairs. Let F̄(t) = Pr(s_new ≥ t). For any T ≥ max_i s_i, FAR(T) ≤ F̄(max_i s_i).
- *High-probability form:* F̄(max s_i) > ε requires all n scores to fall below the upper-ε quantile, so Pr(FAR(T) > ε) ≤ (1−ε)ⁿ. Setting (1−ε)ⁿ = δ gives **ε = 1 − δ^{1/n}**.
- *Expectation form:* E[FAR(T)] ≤ 1/(n+1) by exchangeability (rank of s_new among n+1 values).

### B.2 Every number recomputed `[VERIFIED: ablations/extended_calibration.csv, extended_test.csv, q/report/test_report_look1.json]`
| Quantity | n | δ | Value | Where it appears |
|---|---|---|---|---|
| Calibration certificate, no multiplicity correction | 1,170 | 0.05 | **0.2557%** | AAFV-04 §IV-A; CSV column `D_random_FA_bound95` = 0.002557 |
| Calibration certificate, union bound over 3 values of ρ | 1,170 | 0.05/3 | **0.3493%** | AAFV-04 abstract, contributions, conclusion |
| Calibration expected-FAR bound | 1,170 | – | **0.0854%** | AAFV-04 §IV-A |
| Held-out test audit, one look | 1,149 | 0.05 | **0.2604%** | AAFV-04 §IV-B, Table III note; CSV `D_random_FA_bound95` = 0.002604 |
| Held-out test audit, Bonferroni over 2 looks | 1,149 | 0.025 | **0.3205%** | AAFV-04 Fig. 1 ("Bonf. bound ≤ 0.320%"); `test_report_look1.json` `bound` = 0.0032054; AAFV-03 headline |

All five values are arithmetically correct. The sample counts are consistent: 1,170 calibration and 1,149 test D_random pairs.
**The inconsistency the reviewer saw is real but presentational.** Two different statements (a calibration-side certificate and a held-out audit),
each with and without a multiplicity correction, appear interchangeably. Fig. 1 of AAFV-04 shows the 0.320% audit number next to text that claims 0.349%,
and AAFV-03 called 0.320% the "authoritative bound". The fix is one name and one number per statement, used everywhere.

### B.3 Validity problems that go beyond what AAFV-04 discloses
1. **The calibration split was a development set, so "scorer fixed independently of the n pairs" cannot be shown.** The guard design, the 26 variants,
   ρ, the margin rule, and the Look-2 reject rule were all developed while the calibration decision tables were visible (`decision_table_calibration.csv`).
   In addition, `p78_calibrate_freeze.py` switches the calibrator to `platt_g` when the *calibration-split* reliability deviation exceeds 0.10.
   That is a second data-dependent choice the union bound does not cover. The certificate holds only conditional on the claim that none of these choices
   reacted to the D_random scores. That claim cannot be verified from the repository. T_acc is usually set by D_hard or D_all_random rather than D_random, which limits the damage but does not remove it.
2. **The pipeline has a built-in post-hoc relabelling path.** `p78_calibrate_freeze.py` writes a contact sheet of the 50 highest-P calibration impostors and,
   with `--freeze`, applies `audit/label_corrections.csv` (impostor → genuine). `p_quarantine.py` has `--extra_people` "quarantined after visual audit (D30)".
   Removing or relabelling the *highest-scoring* impostors after seeing their scores is selection on the outcome. If it removed any true impostor, the bound is invalid.
   The repository contains no `label_corrections.csv` and no log saying whether either path was used. The top calibration impostor in
   `q/audit/audit_different_top50.csv` has **P = 0.980 > T_acc = 0.9566**, so it was either guard-failing or removed. Which one must be established from the run logs.
3. **The population is narrow.** The guarantee covers same-sex, MORPH-booking-condition, adult random impostors (AAFV-04 says so). It says nothing about look-alikes
   (5/35,735 false accepts), other capture conditions, or children (FG-NET: 4/20,000, all aged 0–4).
4. **Two looks.** Bonferroni controls multiplicity, not adaptivity. Look 2 tested a re-trained checkpoint after Look 1. Look 2 is secondary evidence only, as AAFV-04 states.
5. **Under any revised method the existing certificate does not carry over.** A new model needs new calibration on a split never used for development, and a new
   confirmatory test. The MORPH test split is spent (D-5), so the confirmatory evaluation must be a pre-registered external one.

### B.4 What can and cannot be claimed
- **Can:** "For the frozen AAFV-04 checkpoint, 0 of 1,149 person-disjoint test random impostors were accepted (one-sided 95% upper bound 0.32% with Bonferroni over two looks)."
  This is a held-out empirical fact. The calibration-side certificate (0.349%) may be stated *only* with the conditionality in B.3-1 and after B.3-2 is resolved.
- **Cannot:** any guarantee for look-alikes, other datasets, children, or at the 10⁻⁴–10⁻⁵ level. Certifying 10⁻⁴ with zero errors needs about 29,956 independent pairs, or roughly
  60k persons in this design (AAFV-04 Table III; I checked: 1 − 0.05^{1/29956} = 1.0000×10⁻⁴).
- **For a CVPR paper:** the certificate cannot be a headline contribution because it does not tell methods apart (A.3). Report standard verification metrics instead:
  TAR@FMR on large impostor sets with person-clustered bootstrap CIs, plus risk–coverage. Keep the zero-failure bound as one sentence about the deployed operating point.

---

## C. Inventory: what can be reproduced without retraining

| Item | Available here? | Usable for |
|---|---|---|
| Look-1 per-pair fused P on MORPH test (339,011 pairs, with gap bin and sex) | Yes | Post-hoc descriptive analyses only (already done in AAFV-04 `a1_*`). No ArcFace score per pair, so no matched-FAR comparison |
| Aggregate rate tables for 26 variants (calibration) and 8 variants × 3 β (test) | Yes | Re-checking the manuscript's numbers (done for Section B) |
| Siamese ViT/CNN per-pair logits (calibration+test, FG-NET), VLM logits (13,319 calibration pairs) | Yes | Baseline curves *for those baselines only* |
| `pair_vectors_{split}.csv` (5 scores × branches, Q, R_sam, g) | **No** | Would enable Priority-2 ablations on calibration without new generation |
| Aligned crops, SAM outputs | **No** | Identity-preservation audit, generator comparison |
| `fusion_seed*.pt`, calibrator.pkl | **No** (hashes only) | Re-scoring |
| MORPH / FG-NET / AgeDB / CALFW / CACD images | **No** | Everything new |

**Consequence:** if `artifacts/p5/pair_vectors_*.csv` and the SAM caches still exist in the original compute environment, about half of Priority 2
can run on CPU in a day. If they do not, the pipeline must be re-run: alignment → SAM → scores, with SAM about 58 ms/face on GPU and up to 16 faces per pair `[REPORTED]`.

---

## D. Research directions (Priority 1)

Each direction below answers a different version of "what is the CV contribution?". All four depend on one cheap experiment, which should run first.

### D.0 Experiment 0, the go/no-go probe (run before committing to any direction)
**Question.** Measured with a recognizer that is *not* in the pipeline, does an age-progressed image make a genuine long-gap pair more separable from a gap-matched impostor pair than the original images alone?
**Design.** Use AgeDB (long gaps) and FG-NET adults. Recognizers: AdaFace IR-101 and MagFace (independent of ArcFace). Generators: SAM-age and FADING (a `patch_fading.py` already exists in `scripts/`).
For each pair compute s₀ = cos h(I₁), h(I₂); s_fwd = cos h(G(I₁→a₂)), h(I₂); s_bwd, symmetrically. Use impostor pairs matched on gap and source ages and progressed identically.
**Metrics.** Use pre-registered gap bins: 0–4, 5–14, 15–29, ≥30 years. In each bin compute ΔTAR@FMR=10⁻³ and ΔAUC of (i) s_bridge alone and (ii) a person-disjoint cross-validated logistic fusion of [s₀, s_bridge], each against s₀.
Report identity preservation cos(h(G(I)), h(I)) per target age. Use person-clustered bootstrap CIs.
**Pre-registered decision.**
- *Go:* fusion improves TAR@FMR=10⁻³ in the ≥15-year bins, with a CI excluding 0, for at least one independent recognizer and at least one generator.
- *No-go:* otherwise. The generated evidence then has no demonstrable identity value, and every generator-centred direction below is dropped. Say so in the paper.

**Cost.** About 1–3 GPU-days for AgeDB + FG-NET with two generators. This is inference only.

This single experiment answers the reviewer's question "How much improvement does the SAM branch provide when evaluated using an independent face-recognition model?" (Priority 2B) and decides Priority 1.

### D.1 Reliability-weighted generative distillation into a gap-conditioned embedding transport *(recommended primary, conditional on D.0 = go)*
- **Problem.** Long-gap genuine pairs are scarce in every longitudinal set (MORPH test: 224 pairs ≥ 15 y). Strong recognizers lose genuine similarity with gap. Generators can produce long-gap counterfactuals cheaply, but their identity fidelity varies per sample.
- **Core idea.** Do *not* run the generator at test time. Use it at training time as a source of unreliable supervision. Learn a small age-transport head on a frozen recognizer that maps an embedding from age a to age t, plus a gap-dependent uncertainty. Train it on real longitudinal pairs and on generated pairs whose influence is set by a **learned per-sample reliability**, the heteroscedastic noise of the synthetic targets. That replaces the hand-made R_sam and puts reliability inside the learning method rather than in a decision guard.
- **Novelty argument (prior-art check of 2026-11-13, Section L).** OE-CNN, DAL and MTLFace remove age from the representation. AIM and MTLFace train synthesis and recognition jointly. OrdCon aligns feature differences with an ordinal age direction.
  **Synthetic aged faces as training data are not new.** MTLFace's TPAMI version adds *FT-Sel*, which fine-tunes the recognizer on synthesized faces selected by a two-component GMM over face-quality scores. Banerjee et al. (IJCB 2023) fine-tune ArcFace on diffusion-aged faces after a hard quality threshold.
  No paper read so far learns an **age transport in the embedding space of a frozen recognizer, with a gap-dependent uncertainty and no test-time generation**. D.1's defensible novelty is therefore narrower than first written. It consists of:
  1. the embedding-space transport and uncertainty;
  2. a *continuous, learned* reliability that is *validated against identity preservation measured by an independent recognizer*, as opposed to MTLFace's quality-based selection (a filter);
  3. evaluation at matched FMR in long-gap bins.
  
  MTLFace FT-Sel and Banerjee et al. 2023 are now mandatory baselines and related work. One relevant ICCV 2025 paper (TimeBooth) could not be read and must be checked before writing.
- **Why it could be CVPR-level.** One clear problem (scarce long-gap supervision), one mechanism, and one probe (D.0). It is generator-agnostic, so it can be tested across generators. Test-time cost is about that of the backbone, which also resolves W10's cost concern.
- **Validation.** Long-gap TAR@FMR vs AdaFace/MagFace/ArcFace/an AIFR model, and against the two closest synthetic-data baselines: a recognizer fine-tuned on generated faces with a quality filter (MTLFace FT-Sel style and Banerjee et al. style). Ablations: no synthetic data / synthetic unweighted / fixed R_sam weights / learned reliability; generator swap; reliability vs measured identity preservation (does the learned σ predict cos h(G(I)), h(I))?
- **Compute.** Embeddings are precomputed once. Generation covers each training image at about 5–8 target ages (about 50k–200k generated faces, several GPU-days for SAM-age, more for diffusion generators). Training the heads takes minutes to hours.
- **Risks.** (i) D.0 = no-go kills it. (ii) Gains over AdaFace may be small. AgeDB-30 accuracy is near saturation for modern recognizers (`[VERIFY]` exact published numbers), so improvements must be shown at low FMR in long-gap bins, not on the 10-fold accuracy protocol. (iii) Recognizer pretraining sets (MS1M, WebFace) may contain AgeDB/CALFW/CACD celebrities, so the test identities leak into the frozen backbone. Report it and lean on MORPH/FG-NET as cleaner tests.

### D.2 Test-time counterfactual trajectory consistency *(closest to the current system)*
- **Idea.** Keep generating at test time. Instead of five generic similarities averaged over targets, embed the two trajectories {h(G(I₁,t))}_t and {h(G(I₂,t))}_t with an independent recognizer and learn a small set/sequence verifier over the *agreement of the two trajectories*, with per-target learned uncertainty. Genuine pairs should converge at shared ages; impostors should not.
- **Novelty.** Moderate: verification by trajectory agreement in a counterfactual age space.
- **Pros.** Reuses the 5-year grid and shared-target code.
- **Cons.** Current evidence is weakly negative (shared targets hurt acceptance). Test-time cost of up to 16 generations per pair. Attacks on the generator become attacks on the verifier.
- **Ranking.** Second. Choose it over D.1 only if D.0 shows large test-time bridging gains but D.1's distillation does not reproduce them.

### D.3 Verification-discriminative age progression *(highest novelty, highest cost)*
- **Idea.** Fine-tune an age generator (encoder or diffusion LoRA) with real longitudinal supervision so that G(I_young→a_old) matches the real older photo of the *same* person under an independent recognizer, plus a contrastive term so that it does *not* move toward other people of that age. That second term directly targets the "generic prototype" failure seen on FG-NET children.
- **Novelty.** Identity-preserving aging is a crowded area (IPCGANs, PFA-GAN, …). The new element would be the impostor-discriminative objective and its evaluation as verification evidence.
- **Cost and risk.** Generator training takes weeks of GPU. There is a risk of learning recognizer shortcuts, so evaluate with a *third* recognizer. Too large for the ICCV-2027 timeline unless substantial GPU is available.

### D.4 Keep the decision-protocol paper *(not a CVPR paper)*
Shift-robust, person-clustered joint FAR/FRR control: weighted conformal for the FG-NET failure, plus a pre-registered external confirmatory test. This was AAFV-04's own recommended "N1". It is a sound biometrics contribution for T-BIOM or IJCB, but it will not satisfy W1 at CVPR, because the contribution is statistical, not visual.

### D.5 Ranking and recommendation
| | D.1 Distillation + transport | D.2 Trajectory consistency | D.3 Discriminative generator | D.4 Decision protocol |
|---|---|---|---|---|
| CV novelty | Medium–high `[VERIFY literature]` | Medium | High | Low |
| Fit to review's ask ("novel representation or identity-preserving mechanism") | Good | Good | Best | Poor |
| Test-time cost | ≈ backbone | High | Medium–high | Unchanged |
| Training cost | Low–medium | Low | High | None |
| Clean ablations for Priority 2 | Yes (with/without/weighted synthetic) | Partial | Yes | n/a |
| Depends on D.0 = go | Yes | Yes | Partly (could create the signal) | No |
| CVPR suitability | Plausible if long-gap gains are real | Borderline | Plausible, but timeline risk | Low |

**Recommendation.** Run D.0 now. If it is a *go*, adopt **D.1** as the primary direction, keep the three-way rule only as an application section, and keep D.2 as the fallback.
If it is a *no-go*, there is no defensible generator-centred CVPR paper in this project. The honest choices are then D.4 at a biometrics venue, or D.3 as a new, longer project.

**Plainly:** the existing AAFV-04 work does not contain a sufficiently novel CVPR contribution. Better presentation of the current architecture will not change that.

---

## E. Provisional architecture for D.1 (to be finalised only after D.0)

**Input.** An aligned pair (I₁, I₂) with ages (a₁, a₂), either known metadata or estimated (e.g. MiVOLO/DEX). Both settings must be reported.
**Output.** A gap-aware match score S, an uncertainty u, and (application layer) Accept / Review / Reject.

1. Frozen recognizer f (AdaFace IR-101; also report ArcFace and MagFace): e_i = f(I_i) ∈ 𝕊⁵¹¹.
2. Transport head T_θ(e, a, t) = normalize(e + MLP_θ([e, φ(a), φ(t)])), with φ a sinusoidal age embedding. Uncertainty head κ_θ(e, a, t) > 0 (von Mises–Fisher concentration).
3. **Real supervision.** For genuine longitudinal pairs (e_y, a_y; e_o, a_o), use L_real = −κ·cos(T(e_y,a_y,a_o), e_o) + log C(κ) (vMF NLL), symmetrised. Add a margin term against gap-matched impostors so the transport cannot collapse identities.
4. **Synthetic supervision.** For a generated face G(I, t), the target is f(G(I,t)) with a learned per-sample noise σ_s². The loss is L_syn = ‖T(e,a,t) − f(G(I,t))‖²/(2σ_s²) + ½ log σ_s², where σ_s is predicted from (identity-preservation, age-fidelity and quality features of the generated face, using an *independent* recognizer h ≠ f). Unreliable syntheses therefore lose influence automatically. Total loss: L = L_real + λ L_syn.
5. **Score.** S = ½[κ₁₂ cos(T(e₁,a₁,a₂), e₂) + κ₂₁ cos(e₁, T(e₂,a₂,a₁))] / normalizer. Uncertainty u increases with gap and decreases with reliability.
6. **Application layer.** The three-way rule with T_acc and T_rej set on a *fresh* calibration split. Report TAR@FMR, risk–coverage, and the review workload at matched FAR.

**What makes it different.** No test-time generation. Reliability is a learned weight inside training, not a hand-set guard. The backbone stays frozen, so the result is an add-on to any recognizer. Generated data is tested as a controllable variable rather than assumed useful.
**Complexity.** Test time is two backbone passes plus an MLP of about 1–3 M parameters. Training is one generation pass over the training set plus head training.

Components of AAFV-04 under D.1:
| Component | Decision | Reason |
|---|---|---|
| ArcFace/AdaFace embedding | Keep (frozen backbone) | Indispensable (drop_arc → 0.73%) |
| EfficientNet, VGG-Face, SSIM | Remove | Redundant or negligible (Table XII). Generic ImageNet features are not identity evidence |
| LPIPS | Remove from the score; possibly keep as a reliability feature | It measures image change, not identity |
| SAM-age at test time | Remove | Cost; no demonstrated benefit |
| SAM-age / FADING at train time | New role | Reliability-weighted supervision |
| Hand-made R_sam | Replace | Learned σ_s, validated against independent identity preservation |
| Branch masking | Not needed | No synthetic input at test time |
| Shared-target grid | Becomes the set of synthetic training targets | Ablate the number K of targets |
| 11-d MLP fusion, 4 constant slots | Remove | Design debt |
| Three-way rule, guards | Keep as the application layer | Operationally meaningful, but not the contribution |

---

## F. Priority 2 experimental framework: does generated evidence carry identity information?

All experiments use person-disjoint splits, pre-registered gap bins (0–4 / 5–14 / 15–29 / ≥30 y), and person-clustered bootstrap CIs. Per-pair scores for **every** method are logged (AAFV-04 could not draw matched-FAR curves because they were not).

| ID | Comparison (Brief A–E) | Data | Needs | Metric |
|---|---|---|---|---|
| F1 | Original-only vs generated-only vs original+generated, without and with reliability weighting (A) | AgeDB, FG-NET adults, MORPH calibration | Generation + embeddings | TAR@FMR 10⁻³/10⁻⁴ per gap bin, ΔAUC |
| F2 | Identity preservation measured by independent recognizers (B) | Same | AdaFace, MagFace, a third model (e.g. FaceNet) | cos(h(G(I)), h(I)); rank-1 of G(I→a₂) against a gallery containing the true older image; per target age and gap |
| F3 | Generator comparison (C) | AgeDB subset | SAM-age, FADING, ≥1 more (HRFAE or CUSP, `[VERIFY]` licence and weights) | F1 and F2 metrics per generator; does the method's ranking change? |
| F4 | Does reliability predict identity preservation? Where does generated evidence mislead? (D) | F2 outputs | – | Spearman ρ (reliability vs independent identity score); risk of using synthetic evidence by reliability decile; failure taxonomy (age, gap, sex, quality) |
| F5 | Controlled ablations (E) | AgeDB, MORPH calibration | D.1 implementation | No synthetic / unweighted / fixed-R_sam weights / learned σ; K targets ∈ {0,1,3,5,7}; endpoint vs shared targets |
| F6 | Gating harms or helps? (D, E) | F1 | – | Fraction of pairs where adding synthetic evidence flips a correct decision to wrong, with and without reliability |

F1, F2 and F4 are Experiment 0 extended. They can run as soon as aligned images and generator weights are available.

---

## G. Priorities 3 and 4: baselines and long-gap evaluation

**Baselines** (all with public weights, `[VERIFY]` availability and licences): ArcFace (already used, `buffalo_l`), AdaFace IR-101, MagFace iResNet-100, at least one AIFR model with released weights (MTLFace has public code; check for weights). For selective verification: uncertainty-thresholded AdaFace/MagFace (MagFace magnitude as a quality score), so the "three-way" comparison is fair.
Train or fine-tune nothing on test data. If Siamese networks are kept at all, train them to convergence. Otherwise drop them; they are weak strawmen.

**Fair comparison.** Same aligned crops, same splits, same calibration rule. Report results at (1) matched FMR, (2) matched review workload, (3) matched genuine-accept target, per gap bin. Show risk–coverage and FAR–coverage curves and DET curves.
The reviewer's question "why prefer 70% over 89%?" can only be answered with curves at matched points. If the new method does not beat AdaFace at matched FMR in the long-gap bins, the paper should report that, and the method must be reconsidered.

**Datasets** (checked 2026-11-13 against secondary sources and the dataset papers' abstracts; see Section L for sources):
| Dataset | Size | Gap character | Role | Caveat |
|---|---|---|---|---|
| MORPH-2 | ~55k images, ~13k persons `[REPORTED in repo]` | 97% < 5 y | Training (real longitudinal pairs) and fresh calibration | Test split spent; booking conditions; demographics |
| AgeDB | 16,488 images, 568 persons, ages 1–101, ~29 images/person, mean per-person age range 50.3 y | **Plenty of long gaps** | **Primary long-gap test** (all within-identity pairs binned by gap) plus AgeDB-30 (10 folds × 300+300 pairs) for comparability | Celebrities likely in recognizer pretraining. AgeDB-30 accuracy is near saturation (≈98.4–98.6% reported for a strong 2023 method), so gains must be shown at low FMR in long-gap bins |
| FG-NET | 1,002 images, 82 persons, 0–69 | Very long | External test; children reported separately | Small. **No sex labels**: annotate the 82 persons for FADING and for demographic matching |
| ECAF (MTLFace benchmark) | ≈5.3k images, 613 persons; ≈6k adult–child and 4k child–child pairs; mean gap ≈41 y (per a summary of the TPAMI paper, `[VERIFY]` on the project page) | Child-to-adult | Very-long-gap stress test, outside the adult scope; report separately | LFW identities, so pretraining overlap; check availability and licence |
| CALFW | 3,000 positive pairs plus gender- and race-matched negatives; LFW identities | Moderate; ages estimated with DEX | Unconstrained comparability | Pretraining overlap; gap labels are estimates |
| CACD-VS | 4,000 pairs (2,000+2,000) | Photos from 2004–2013, so **gaps of at most about 9 years** | Medium gaps only | **Cannot support a long-gap claim**. CACD is noisy; year labels are rough |
| LAG | 3,828 images, 1,010 celebrities | Large, child-to-adult | Pooled large-gap test only | **No age labels**, so it cannot be binned by gap without estimated ages; pair counts unconfirmed |

If, after binning, fewer than about 300 genuine pairs at ≥20 y remain across adult sets, a defensible statement at that gap is not possible. Report it as a limitation and use pooled ≥15-y bins with CIs.

---

## H. Turnitin report: what it measures

- **The supplied file is an AI-writing report only.** "31% detected as AI", i.e. text segments the detector judges likely AI-generated or AI-revised. **No similarity (text-matching) report is included**, so the file contains no evidence about plagiarism or missing attribution. Getting the similarity report for AAFV-04 is necessary before anything about originality can be concluded. AAFV-01's earlier similarity report showed 55% `[REPORTED in comprehensive_context.md]`; that number was not re-checked here.
- **Turnitin's own page says the score must not be used as the sole basis for adverse action**, and an AI percentage is not proof of misconduct.
- **Where the highlights fall** (checked visually on all 12 content pages): almost the whole abstract, the contributions list, "We do not claim…", the related-work positioning sentences, the setup of Proposition 1 and Remark 1, the independence/sample-size paragraph, protocol chronology, operational workload, age-gap analysis, discussion, limitations and conclusion. In other words, the interpretive framing prose. Tables, equations and the reference list are largely unflagged.
- **The honest reading.** AAFV-03 and AAFV-04 were in large part drafted and revised by AI assistants (AAFV-04 by Claude cowork). The flagged regions are mostly where that happened, so the flag is plausibly correct, not a false positive. The remedy is not to rephrase to lower the score. It is:
  (i) the authors write the new CVPR manuscript's framing sections themselves, from their own understanding of the method, and use AI for checking rather than drafting;
  (ii) they disclose AI assistance as the target venue's policy requires (read the CVPR/ICCV 2027 author guidelines on LLM use, `[VERIFY]`);
  (iii) the new paper is written fresh for a new method anyway, so very little AAFV-04 prose should survive.
- **Real attribution issues found in the text (independent of the detector).**
  1. The abstract says "We show that this rule gives a distribution-free, finite-sample FAR certificate", which reads as a novel result. The argument is the standard order-statistic/conformal one (Vovk et al.; Hanley & Lippman-Hand), and it should be attributed in the sentence itself.
  2. The R_sam design and quality-conditioned fusion follow Poh et al. (2009) closely enough to need explicit citation at the point of use, not only in related work.
  3. Statements about what AIM and OrdCon "do not address" must be checked against those papers. Both PDFs are in the repository, and nobody in this audit has verified the specific claims.

---

## I. Review response matrix (W1–W10)

| # | Criticism | Underlying problem | Correction | Evidence needed | Status |
|---|---|---|---|---|---|
| W1 | Novelty | No learned visual mechanism | D.1 (or D.2/D.3) after D.0 | D.0 go; D.1 > AdaFace at matched FMR, long gaps | Not started |
| W2 | Generative branch unproven | ArcFace-circular identity check; no branch study | F1–F6 with independent recognizers and ≥2 generators | Per-bin ΔTAR, identity-preservation curves, qualitative success/failure grid | **Log analysis done (M):** no measurable SAM value at matched FPR on MORPH; independent-recognizer test (Experiment 0) pending |
| W3 | Loses to ArcFace | Decision layer (threshold + guards), not discrimination | Compare at matched FMR/workload | Risk–coverage and DET curves with per-pair logs | **Log analysis done (M):** at matched FPR AAFV-Net = ArcFace; the 70 vs 89% gap is threshold- and guard-driven |
| W4 | Short gaps | MORPH composition **and probable MORPH long-gap label errors** | AgeDB/FG-NET long-gap bins, pre-registered; MORPH not used for long-gap claims | ≥15 y and ≥20 y results with CIs | **Log analysis done (M):** 95–97% of MORPH 15–29 y genuine pairs impostor-like for two unrelated models; long-gap evidence must come from AgeDB/FG-NET |
| W5 | Certificate inconsistent | Mixed statements; development-set reuse; relabel path | Section B: one statement per number; fresh calibration for the new method; demote the certificate | Run logs on label corrections; fresh calibration split | **Derivation done**; logs pending |
| W6 | Weak baselines | Only ArcFace; unconverged ViT | AdaFace, MagFace, AIFR, uncertainty-based selective baselines | Same-protocol table | Not started |
| W7 | Generalization; post-hoc adult cut | Small external set; cut chosen after failure | Pre-register scope (adult ≥16 *and* a reported child stratum); larger adult sets | AgeDB/CALFW confirmatory looks | Not started |
| W8 | Calibration | P mis-calibrated mid-range; prior-dependent | Calibration reported as diagnostic; decisions on scores with fresh thresholds | ECE/MCE/Brier/NLL/slope per subgroup and dataset | Partly (Look-1 post hoc only) |
| W9 | Fairness | Sex only, Look 1, pair-level CIs | Race × sex × age with person-clustered CIs; review-rate disparity | Demographic logging in all new runs | Not started |
| W10 | Reproducibility, cost | Weights, data and per-pair outputs not saved | Release scripts; log per-pair scores; measure p50/p95 latency and VRAM | End-to-end timing | Not started (D.1 removes test-time generation) |

---

## J. Remaining risks and readiness

**Risks.**
1. D.0 may come out no-go. Then no generator-centred CVPR paper exists in this project.
2. Even with a go, gains over AdaFace/MagFace may be within CI at the long-gap bins, because the sets are small.
3. Recognizer pretraining may overlap AgeDB/CALFW/CACD test identities, inflating every baseline and the method alike.
4. Ages: using ground-truth ages at test time is unrealistic. Estimated ages add noise that may erase gains.
5. Compute and licences: MORPH and FG-NET licences; SAM-age, FADING and InsightFace non-commercial licences; GPU availability unknown.
6. The literature check for D.1's novelty is still outstanding.
7. Time: about 14–16 weeks to an ICCV-class deadline, with D.0 → D.1 → full evaluation → writing all sequential.

**Readiness.** The current work (AAFV-04) is **not suitable for CVPR or ICCV**, and CVPR 2027 is no longer reachable on the calendar.
The recommended direction is **plausible but unproven**. Its CVPR/ICCV suitability depends entirely on Experiment 0 and then on matched-FMR long-gap gains over AdaFace.
I would not estimate acceptance odds before D.0 results exist.

---

## K. Decisions and information needed from the team (blocking)

1. **Where are the original artifacts** (`artifacts/p5/pair_vectors_*.csv`, crops, SAM outputs, `fusion_seed*.pt`, run logs)? Is the original compute environment still available?
2. **GPU budget** (GPU type × days) and data access: MORPH and FG-NET licences in hand? AgeDB, CALFW, CACD, LAG obtainable?
3. **Venue and timeline.** Accept that CVPR 2027 is not reachable and target ICCV 2027 / CVPR 2028 (or a biometrics venue if D.0 is no-go)?
4. **Was `label_corrections.csv` or `--extra_people` ever used** on the calibration split? This decides whether the 0.349% statement can be kept at all.
5. ~~Approval to run Experiment 0.~~ The scripts are written (`exp0/`). Still needed: compute, data, and the commit of `exp0/PREREGISTRATION.md` (plus the FG-NET sex annotation) before generated faces are embedded.

---

## L. Verification log (2026-11-13)

**Tool interfaces** (read from source, recorded in `exp0/config.yaml`):
- **FADING** (`MunchkinChen/FADING@master`, `age_editing.py`):
  - `--gender` accepts only `female` / `male`.
  - `--target_ages` takes `nargs='+'` integers.
  - The output is `<save_aged_dir>/<stem>_<age>.png`, with the stem split on `/`.
  - The input is centre-cropped to 512×512.
  - `--specialized_path` is a diffusers directory.
  - The supported age range is not stated.
- **SAM-age** (`yuval-alaluf/SAM`):
  - Output goes to `<exp_dir>/inference_results/<age>/<input basename>`.
  - `--target_age` is a comma-separated string.
  - `--resize_outputs` gives 256×256 outputs (1024×1024 otherwise).
  - Inputs are resized to 256 without alignment, and CUDA is required.
- **AdaFace** (`mk-minchul/AdaFace`): checkpoint keys prefixed `model.`; input BGR scaled to (x/255 − 0.5)/0.5; forward returns (unit feature, norm). `build_model('ir_101')` corresponds to the README's "R100" rows (MS1MV2 / MS1MV3 / WebFace4M / WebFace12M).
- **MagFace** (`IrvingMeng/MagFace`): `builder_inf(args)` reads arch, embedding_size, resume and cpu_mode; input BGR in [0, 1]; forward returns the raw embedding. The bare `torch.load` needs a `weights_only=False` shim on torch ≥ 2.6, which is now in `s5_embed.py`.

**Datasets.** Sources:
- [AgeDB (Papers with Code)](https://ml.paperswithcode.com/dataset/agedb)
- [MTLFace TPAMI, arXiv 2210.09835](https://arxiv.org/pdf/2210.09835)
- [CACD / CARC](https://bcsiriuschen.github.io/CARC)
- [CALFW, arXiv 1708.08197](https://arxiv.org/abs/1708.08197v1)
- [LAG, arXiv 1602.06149](https://arxiv.org/pdf/1602.06149.pdf)
- [Wasserstein AIFR, arXiv 2305.02745](https://arxiv.org/abs/2305.02745), for current AgeDB-30 levels

**Closest prior work to D.1/D.2** (abstract and method sections read):
| Paper | What it does | Overlap |
|---|---|---|
| MTLFace TPAMI ([2210.09835](https://arxiv.org/abs/2210.09835)) | Joint AIFR + age synthesis; FT-Sel fine-tunes on synthesized faces selected by a GMM over quality scores; ECAF benchmark | **Synthetic-data component of D.1** (filter, not learned continuous weight; no frozen-recognizer transport) |
| Banerjee et al., IJCB 2023 ([2307.08585](https://arxiv.org/abs/2307.08585)) | DreamBooth-style diffusion aging with identity loss; ArcFace fine-tuned on about 3,400 age-edited images; checks identity with a recognizer different from the one in its loss | Synthetic-data component; independent-recognizer evaluation (same idea as our Experiment 0) |
| Luevano et al., IJCB 2025 ([2508.08808](https://arxiv.org/abs/2508.08808)) | Identity-preserving StyleGAN aging; evaluated with two recognizers; releases a synthetic dataset | Candidate third generator; no verification method |
| DiverAge, arXiv 2026 ([2606.04881](https://arxiv.org/abs/2606.04881)) | Diffusion aging guided by a real-data, age-bin cross-age identity-similarity prior | Gap-dependent prior idea, used for generation guidance |
| Dahan & Keller 2023 ([2305.02745](https://arxiv.org/abs/2305.02745)) | Trained identity/age embedding disentanglement; reports AgeDB-30 98.4–98.6% | Shows AgeDB-30 saturation; not frozen-recognizer transport |
| TimeBooth, ICCV 2025 | Age editing with an age-invariant identity representation | **Not read** (PDF access refused). Must be checked |

**Still unverified:** FADING's age range; the ECAF statistics and availability; TimeBooth; and the claim seen in a search snippet of a 2019 paper reporting a "10–40%" cross-age verification gain from synthesized faces, which remains unidentified. A full search of CVPR/ICCV/ECCV 2023–2026 proceedings for "cross-age" and "age-invariant" is still to be done before the related-work section is written.

---

## M. Results from the logged artifacts (2026-11-13)

Full write-up: `log_analyses/LOG_FINDINGS.md`; script `log_analyses/run_log_analyses.py`; outputs in `log_analyses/out/`. No model was trained and no threshold was set. The MORPH test outputs were read post hoc only.

1. **At matched FPR, AAFV-Net ranks pairs no better than ArcFace.** TPR@FPR 0.1% on MORPH calibration is 0.992 vs 0.990 (0–4 y), 0.668 vs 0.668 (5–9 y), 0.649 vs 0.649 (10–14 y). The 70% vs 89% auto-accept gap is produced by the threshold and guards, not by discrimination.
2. **No measurable SAM contribution.** Full vs direct-only MLP: all CIs overlap in every bin. The look-alike advantage exists equally without SAM, so it comes from the fusion trained on mined negatives. SAM-only is worse than direct-only at low FPR where data exist.
3. **MORPH long-gap genuine pairs are probably mislabelled.** 97% (15–19 y) and 95–98% (20–29 y) of test genuine pairs score below the 99th percentile of same-bin random impostors for *both* AAFV-Net and an independently trained ViT, and every method is at chance at 15–19 y. The audit sheet shows at least one certain identity error and one person id spanning four filename prefixes. MORPH cannot carry any long-gap claim.
4. **The hard-impostor result reflects the training negatives.** AAFV-Net ranks even the impostor-like long-gap "genuine" pairs above mined look-alikes; the independent ViT does the opposite.
5. **The calibration top-impostor sheet** (`q/audit/audit_different_top50.jpg`) contains several pairs that look like the same person, including the top pair (P = 0.980 > T_acc). That suggests residual duplicate identities. It also confirms that the label-correction path (B.3-2) was a live issue. Whether it was used is still unknown.

**Effect on the direction.** Nothing in the logged artifacts supports the generated-evidence branch. Experiment 0 on AgeDB/FG-NET is the only remaining test of D.1/D.2. A separate, image-only (no GPU) check of a random sample of MORPH long-gap genuine pairs against the MORPH index would confirm or refute Finding 3.

---

## N. Phase 4: architecture reconsidered (2026-11-13)

Full audit: `architecture_review/ARCHITECTURE_REVIEW.md`; frozen-model probe: `architecture_review/probe_fusion.py`.
- Of 15 components, 6 are removed (four of the five similarity measures, test-time SAM, the shared-target grid, branch masking, the 11-input MLP, the guards), 6 are redesigned, and 3 are kept.
- The direct branch learned to use ArcFace alone, and the fused logit is dominated by it (swing 25.1 vs 4.1 for the SAM branch). The SAM and R_sam effects are no larger than those of untrained controls.
- The Look-2 checkpoint is a 3-seed ensemble, not 5. ArcFace inputs were misaligned (FFHQ crop resized).
- Proposed: a gap-aware selective verifier on a frozen recognizer as the baseline of record (Section 3.1). The reliability-weighted age-transport model (3.2, direction D.1) is built only if Experiment 0 returns GO.

---

## O. Supplied result images (2026-11-13)

Full audit: `image_audit/IMAGE_AUDIT.md`. Two images were supplied, and no face recognizer is available here, so the findings are qualitative.
- **SAM-age outputs (2 people × 3 target ages).** The edits concentrate on the eyes (iris colour and shape) and brows. A distinctive joined eyebrow is thinned and split in the younger outputs. Backgrounds and clothing are regenerated, and fine synthetic texture is added to blurry sources. This is consistent with Finding 2 (no measurable SAM value) and gives the qualitative figure W2 asks for.
- **FG-NET false accepts.** Different children, three of four under 1 year, all short-gap and poorly captured, with fused P of 0.966–1.000. Guarded ArcFace accepted none of the same 20,000 impostor pairs. The logs cannot attribute the cause.
- **No change to the direction decision.** The quantitative identity-preservation test is still Experiment 0.
