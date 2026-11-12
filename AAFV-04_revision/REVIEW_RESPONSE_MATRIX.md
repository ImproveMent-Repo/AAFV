# AAFV-04 — Reviewer Response Matrix

**Review being answered:** *IEEE_Transactions_Expert_Review.docx*. The review was written against the AAFV-02 manuscript; AAFV-03 is the baseline that was revised here.
**Revised manuscript:** `AAFV-04_revision/manuscript/main.tex` (12 pages, compiles with no undefined references and no overfull boxes).
**Evidence labels:** **Verified** = supported by a logged artifact in `Code/AAFV_Net/` or by a script in `AAFV-04_revision/analysis/`; **Reported** = stated in an earlier draft but not traceable to an artifact; **Required** = needs new work; **Unavailable** = data or logs not on disk.

### How "status" is used

| Status | Meaning |
|---|---|
| **Addressed** | The manuscript now handles the issue correctly, using evidence that already exists. |
| **Partly addressed** | The text is corrected and some existing evidence was added, but the reviewer's request needs new experiments. |
| **Open** | New experiments or data are needed; the manuscript only discloses the gap. |

No issue is marked Addressed because its wording changed. Every Addressed item points to a verified artifact or a derivation.

---

## A. Summary matrix (Section 3 of the review: 14 major comments)

| # | Reviewer concern | Weakness in AAFV-03 (location) | Correction in AAFV-04 (section) | New evidence or experiment required | Status |
|---|---|---|---|---|---|
| 3.1 | Novelty is integrative; no hypothesis; no component novelty table | Four contributions claimed "verifiable" but framed as an architecture (Sec. I); no comparison table | Explicit research question; contributions limited to what evidence supports, including what is **not** claimed (Sec. I); component-level positioning table: adopted / modified / new + evidence (Table I); Discussion separates supported from unsupported (Sec. VIII) | A methodological advance beyond the protocol (see NOVELTY_ASSESSMENT.md, directions N1–N3) | **Partly addressed** |
| 3.2 | FAR bound: independence, sampling unit, clustering, sample size for 0.1–0.001% | Bound presented as the main guarantee; dependence handled in prose only (Sec. IV) | (i) New calibration-side certificate (Prop. 1), derived from the threshold rule, which does not use test data; (ii) sampling unit and identity overlap stated (2,298 distinct persons, 1 image each); (iii) design-effect sensitivity; (iv) sample-size table for 1e-3/1e-4/1e-5 with k=0,1,2 (Table III) | Larger independent impostor pool (E5); cluster-aware analysis of correlated pools | **Partly addressed** (statistics correct; scale limited by data) |
| 3.3 | Two-look adaptive leakage; chronology; untouched external test | Reconciliation table only; Bonferroni presented as sufficient | Chronology table rebuilt from logs (Table V): Look 2 used a **re-trained checkpoint**, a **changed reject rule**, new baselines and new neutral sets; states that adaptivity cannot be excluded; Look 2 downgraded to a secondary evaluation; FAR guarantee moved to the calibration certificate | Signed author declaration on what Look 1 informed; confirmatory evaluation on an untouched external set (E1) | **Partly addressed** |
| 3.4 | Calibration: ECE, Brier, NLL, slope/intercept, reliability diagrams, subgroups, cross-dataset, Platt vs isotonic vs temperature | Only bin-level mean-P checks (`reliability_by_bin.csv`) | (i) Shows that decisions are invariant to the monotone Platt map except through ρ, so guarantees do not rest on calibration (Sec. V-E); (ii) post hoc ECE/MCE/Brier/NLL/slope/intercept on Look-1 test outputs, by pool and by sex (Table X); reliability diagram (Fig. 3b) reveals strong under-confidence at intermediate P; (iii) FG-NET false-reject failure reported as a calibration-under-shift failure | Cross-dataset calibration and Platt/isotonic/temperature comparison need per-pair outputs that were not saved (E3) | **Partly addressed** |
| 3.5 | SAM identity preservation with independent recognizers and humans; multiple generators | R_sam uses ArcFace (circular); no independent check | Circularity stated (Sec. V-C, IX); no claim of identity preservation remains; contribution of generated vs original features separated via ablations (Sec. VII-H) | Independent recognizer audit (AdaFace/MagFace) across gaps; blinded human study; second generator (E4) | **Open** |
| 3.6 | Dataset diversity; strict cross-dataset protocol | FG-NET only; adult cut-off post hoc | Datasets described with composition, capture conditions, and **age-gap composition (97.2% of MORPH genuine test pairs < 5 years)**; FG-NET results now include review and **false-reject** rates (Table XI); post hoc cut-off flagged | AgeDB, CACD-VS, CALFW with frozen checkpoint (E1); FG-NET leave-out protocol | **Open** |
| 3.7 | Broader controlled baselines; risk-coverage curves; not a single threshold | ArcFace, Siamese (ViT unconverged), VLM only; single β | ViT non-convergence and VLM scope stated; β sweep reported, showing ArcFace reaches 71.94% hard rejection at β=0.02; descriptive risk-coverage curve of the Look-1 scorer (Fig. 3c) | AdaFace, MagFace, ≥1 AIFR model, converged ViT, selective-classifier baselines, matched-FAR risk-coverage curves with per-pair scores (E2, E6) | **Open** |
| 3.8 | Hard-impostor failure analysis; mining details; not used for tuning; broader threats | 5 FAs only counted; threat model in prose | (i) Mining fully specified; (ii) **new finding:** half of the training negatives are ArcFace-mined like D_hard, and the fused P is lower on D_hard than on random impostors (median 0.0013 vs 0.0096), so 98.04% is not read as general look-alike robustness; (iii) metadata of the 3 Look-1 hard FAs (sex, gap bin, P); (iv) threat-model table with in/out of scope (Table II) | Characterize the 5 Look-2 FAs (requires re-scoring logged test pairs, disclosed as forensic, E7); ablation without mined training negatives (E8); degradation stress test (E11) | **Partly addressed** |
| 3.9 | Age-gap deficit vs ArcFace is central | Framed as a security trade-off | Deficit stated as a central negative result (Abstract, Sec. VII-D, VIII); shows most of the deficit comes from the **guards** (97.38% → 79.74% genuine coverage at T_acc on Look 1); new workload table: AAFV-Net generates **~3× the manual reviews** of guarded ArcFace at realistic impostor rates (Table VIII); no cross-age improvement claimed on MORPH | Matched-FAR risk-coverage comparison (E2); large-gap protocol (youngest vs oldest image) on external data (E1) | **Partly addressed** (honestly reported; superiority not established) |
| 3.10 | Fairness too narrow; CIs; unit of analysis | Sex only; stale counts in AAFV-02 (926/224) | Correct Look-1 counts and unit of analysis (pairs; persons not logged); sex × gap-bin rates with pair-level Wilson CIs flagged as understated; subgroup calibration by sex (Table X) | Race × sex × age analysis with person-clustered CIs on calibration and external data (E9) | **Partly addressed** |
| 3.11 | End-to-end computational cost; cascade | AAFV-03 Table VIII gave microsecond MLP timings; earlier drafts quoted per-stage ms that cannot be traced | All unlogged timings **removed**; table reports parameters and per-pair work only | p50/p95 latency, throughput, memory, utilization, cascade evaluation (E10) | **Open** |
| 3.12 | Fusion vector: constant dims, ranges, normalization, missing values, branch masking | Partially described | Full 11-slot definition table with ranges, missing-value handling, and Stage-A status (Table IV); shows the four constant slots are output-irrelevant and an equivalent 7-input network exists; masking procedure specified exactly | Missing-branch robustness test (force I_sam = 0 at inference) (E12) | **Partly addressed** |
| 3.13 | Numerical inconsistencies; consolidated table | 70.07 vs 74.07/74.13; 80.25/77.95; 3 vs 5 FAs not reconciled in one place | Consolidated population table (Table VI) with split, checkpoint, thresholds, N, A/R/X, FA, source file; text explains each discrepancy; persons per row marked "not recorded" where unavailable | Person counts per evaluation row (re-derivable from pair files, E13) | **Addressed** (except person counts) |
| 3.14 | Related work: AIFR, ageing/identity, uncertainty, open-set, selective, conformal, calibration, fairness, PAD/morphing | Several citations were tangential or misused (e.g., a deepfake-detection paper cited for SAM identity drift; template inversion cited for TMR@FMR reporting practice; a game-theoretic NP paper for threshold selection) | Related work rewritten in six threads with 26 new references, including AIM and OrdCon read in full; misused citations removed; positioning table | Verify the bibliographic fields of the new entries (see UNRESOLVED_ISSUES.md U-12) | **Addressed** (pending bibliography check) |

---

## B. Section 4 of the review — "Additional experiments required"

| Review item | Plan ID | Status |
|---|---|---|
| ≥2 further age-related/unconstrained benchmarks, separated train/cal/test | E1 | Open |
| Frozen identity-disjoint external test, untouched | E1 | Open |
| More independent impostor identities; justify sample size; clustering | E5 (+ Table III done) | Partly addressed |
| ArcFace, AdaFace, MagFace, AIFR, selective baselines at matched operating conditions | E2, E6 | Open |
| Risk-coverage curves; accept / reject / review trade-off | E2 (Fig. 3c descriptive; Table VIII workload done) | Partly addressed |
| ECE, Brier, NLL, reliability diagrams, subgroup and cross-dataset calibration | E3 (Table X done for MORPH Look 1) | Partly addressed |
| SAM identity preservation (independent recognizers / humans) | E4 | Open |
| Age-gap-stratified results with CIs; analysis of the deficit | E2, E13 (Table IX + guard analysis done) | Partly addressed |
| Subgroup and intersectional fairness with CIs | E9 | Open |
| Degradation, look-alikes, morphing, PA within a threat model | E11 (threat model done) | Partly addressed |
| End-to-end latency, p95, throughput, memory, cascade | E10 | Open |
| Complete ablations: branches, generated input, fusion, calibration, threshold policy | E8, E12, E3 (26-variant ablation exists) | Partly addressed |

## C. Section 5 of the review — "Recommended methodological direction"

| Recommended element | AAFV-04 response | Status |
|---|---|---|
| Formal threat model and operational objective (target FAR, coverage) | Sec. III-B objective (Eq. 2), Table II | Addressed |
| Principled uncertainty-aware fusion distinguishing identity, age, quality, generator reliability | Not changed; the current fusion is a learned combiner. Direction N2 in NOVELTY_ASSESSMENT.md | Open |
| Risk-control procedure with stated assumptions, finite-sample guarantees, identity-aware sampling, untouched test | Prop. 1 with assumptions; identity-aware D_random; untouched test still missing | Partly addressed |
| Selective policy evaluated by risk-coverage incl. review cost | Workload table done; risk-coverage at matched FAR missing | Partly addressed |
| Cross-dataset and subgroup validity of calibration and risk | FG-NET false-reject failure reported; remedy (weighted conformal) proposed, not run | Open |

---

## D. Item-by-item detail (the reviewer's seven-step request)

Each entry gives: (1) criticism, (2) location in AAFV-03, (3) why it was insufficient, (4) what resolves it, (5) revision made, (6) remaining experiments, (7) how the revision answers the criticism.

**3.1 Novelty.** (1) The work looks like engineering integration. (2) AAFV-03 Sec. I contributions 1–4. (3) The contributions described components, not a methodological claim; there was no hypothesis and no component table. (4) Identify the precise advance and support it, or narrow the claim. (5) Research question added; contributions restated as (i) a decision policy with a calibration-side certificate, (ii) the empirical role of guards, (iii) reliability-gated synthetic evidence (benefit stated as unproven), (iv) transparent evaluation; Table I positions each component. (6) Directions N1–N3. (7) The paper no longer claims more than the evidence supports, but the methodological novelty is still modest; see NOVELTY_ASSESSMENT.md.

**3.2 FAR statistics.** (1) The binomial bound needs independence and representativeness. (2) AAFV-03 Sec. IV-A/B. (3) Independence was asserted from pair construction; operational sample sizes were absent. (4) State the sampling unit, dependence, sensitivity, and required N. (5) Sec. IV-A (Prop. 1, calibration certificate 0.349%); IV-B (audit 0.260%/0.320%); IV-C (2,298 distinct persons; design-effect table: 0.48% at D = 1.5, 0.64% at D = 2; correlated pools are never given binomial bounds); Table III (N for 1e-3/1e-4/1e-5). (6) E5. (7) The statement is now correctly scoped and its scale (~3×10⁻³) is stated as insufficient for border-control targets.

**3.3 Two looks.** (1) Bonferroni does not repair adaptivity. (2) AAFV-03 Sec. IV-B, Table III. (3) It claimed that the pre-registered model was "retained", but the Look-2 checkpoint is a re-train with a different hash. (4) Provide a chronology and an untouched test set. (5) Table V and Sec. VI-D; the guarantee now rests on calibration data (Remark 1). (6) Author declaration; E1. (7) The reader can see exactly what changed between looks; no confirmatory claim depends on Look 2.

**3.4 Calibration.** See matrix. An important conceptual correction: Platt is monotone, so it cannot affect the order-statistic thresholds; it only affects the ρ floors and the interpretability of P. The reliability diagram shows that intermediate P values are almost all genuine pairs, so P should not be shown to examiners as a probability.

**3.5 SAM identity.** Nothing in the repository measures identity preservation independently. The manuscript removes every implication that it does and lists E4.

**3.6 Datasets.** A new negative fact surfaced: on MORPH, 97.2% of genuine test pairs span less than 5 years, so the MORPH evaluation is mostly not cross-age. This is now in Sec. VI-A and the Discussion.

**3.7 Baselines.** The β sweep in `extended_test.csv` shows that ArcFace's 0% hard rejection is specific to β ≤ 0.01; at β = 0.02 it rejects 71.94%. This weakens AAFV-03's "0% hard rejection" argument and is now stated.

**3.8 Hard impostors.** `p3_build_pairs.py` shows that training negatives are 50% ArcFace-mined. The Look-1 P distributions (Fig. 3a) show that D_hard is easier for the fused model than random impostors. This is a plausible explanation of the 98.04%, not a proof; E8 tests it.

**3.9 Age gap.** The deficit is now a headline result. New quantitative explanations: (a) guards remove ~18 pp of genuine coverage at T_acc (Look 1); (b) the workload table (Table VIII) shows ~2,970 vs ~970 reviews per 10,000 transactions at 1% impostors.

**3.10 Fairness.** The AAFV-02 figures (926/224) came from an early development split; correct Look-1 figures are reported. Sex × gap rates show the gap persists within G1 (82.34% vs 72.05%).

**3.11 Cost.** No timing log exists in the repository for any latency quoted in AAFV-01 to AAFV-03 (searched `Code/` for 77.2 µs, 58.2 ms, 2.14 s, 124.5 ms). These numbers were removed.

**3.12 Fusion vector.** Table IV gives the full vector definition. The constant slots are inert (zero inputs and one constant head), so they cannot mislead the model, but they inflate the stated dimensionality.

**3.13 Numbers.** Table VI resolves every discrepancy quoted by the reviewer:

| Pair of numbers | Explanation |
|---|---|
| 70.07 vs 74.07/74.13 | Look-2 test vs 1,500-pair calibration subset (74.13 in the logs; "74.07" appears in no artifact) |
| 80.25/77.95 | Stale AAFV-02 figures. The correct Look-1 figures are 81.07/71.93, which average to 79.74 |
| 3 vs 5 hard false accepts | Two different checkpoints |

**3.14 Related work.** Rewritten in six threads (Sec. II). AIM and OrdCon are discussed from the full papers, including their evaluation protocols (largest-gap MORPH settings, multiple datasets) as a contrast with this paper's short-gap MORPH protocol.
