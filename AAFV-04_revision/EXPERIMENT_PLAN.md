# AAFV-04 — Additional Experiment Plan (prioritized)

## Ground rules for every experiment

- **The MORPH test split is closed.** Both logged looks are used. No experiment may tune, select, or re-threshold on it. The only permitted test-split work is E7: forensic re-scoring with frozen artifacts, disclosed as such, with no decisions changed.
- **Pre-register before running.** Write a one-page analysis plan per experiment: hypothesis, metric, decision rule, and the population row it will add to Table VI. Commit it to git with a timestamp before running.
- **Log per-pair outputs.** Every evaluation must save, for every pair: P, P_d, P_s, Q, R_sam, I_sam, guard flags, zone, set, gap, sex, race, person ids, and the score of every baseline. Missing per-pair logs are the main reason several reviewer requests cannot be answered today.
- **Cluster by person.** Use person-clustered bootstrap for all rates. Use binomial bounds only for person-disjoint pools.

**Priority key:** P0 is required for any resubmission. P1 is strongly expected by TIFS reviewers. P2 strengthens the paper.

---

### E1 (P0): Confirmatory external evaluation on untouched adult cross-age benchmarks
- **Objective.** Provide the untouched confirmatory test the reviewer requires (3.3, 3.6). Test whether accept-side FAR control, coverage, and reject-side FRR transfer.
- **Data.** AgeDB (AgeDB-30 protocol plus a large-gap subset), CACD-VS, and CALFW. Apply the same adult filter (≥16) **declared in advance**. Quarantine duplicate identities with the same rule as MORPH.
- **Protocol.**
  - Freeze the MORPH checkpoint, guards, ρ, and T_acc. Run once, with a single logged look per dataset.
  - Report two decision settings: (a) MORPH thresholds unchanged (transfer), and (b) thresholds re-set on a person-disjoint *calibration* half of each target dataset, evaluated on the other half (in-domain calibration).
  - Also build the AIFR-standard large-gap protocol: youngest vs oldest image per person.
- **Baselines.** ArcFace, AdaFace, MagFace (each wrapped in the identical three-way rule), direct-only fusion, and No Shared Targets.
- **Metrics.**
  - Genuine A/R/X with person-clustered CIs.
  - Random-impostor FA with the binomial bound on person-disjoint pairs.
  - Calibration-side certificate (Prop. 1) recomputed in setting (b).
  - Hard and neutral impostor rejection; per-gap-bin rates.
- **Statistics.** Paired person-level bootstrap for differences between methods. Holm correction across datasets.
- **Outputs.** New rows in Table VI; a new external-results table; per-gap coverage figure.

### E2 (P0): Matched-FAR risk–coverage and workload curves
- **Objective.** Answer 3.7 and 3.9 at matched operating points rather than at a single threshold.
- **Data.** MORPH calibration split (per-pair re-scoring with frozen models), and E1 data.
- **Protocol.**
  - For each method, sweep T_acc (with and without guards) and T_rej.
  - Compute genuine coverage vs. random FAR and vs. hard FA; review rate vs. hard-rejection rate; the AURC.
  - Compare at matched certified FAR (Prop. 1) and at matched hard-rejection rate.
- **Baselines.** As in E1, plus generic selective classifiers: softmax-response / score-margin selection [Geifman & El-Yaniv 2017] and a Learn-then-Test threshold pair [Angelopoulos et al. 2021].
- **Metrics.** AURC; coverage at FAR certificate ∈ {0.5%, 0.3%}; review per 10k transactions under impostor mixtures (extends Table VIII).
- **Outputs.** Risk–coverage figure (replaces Fig. 3c); workload table.

### E3 (P0): Calibration suite and shift analysis
- **Objective.** Complete 3.4.
- **Data.** Per-pair outputs on MORPH calibration (re-scored), FG-NET, and E1 datasets.
- **Protocol.**
  - Compare Platt, isotonic, and temperature scaling, plus prior-corrected Platt. Fit on train_val; evaluate without refitting on each target.
  - Fit nothing on the evaluation sets, except a separately reported "recalibrated" condition fitted on target calibration halves.
- **Metrics.** ECE (15 bins and adaptive), MCE, Brier, NLL, calibration slope and intercept, reliability diagrams. Report by dataset, gap bin, sex, and race.
- **Additional.** Measure reject-side FRR transfer, and test weighted conformal thresholds under covariate shift [Tibshirani et al. 2019] as a remedy for the FG-NET 18.20% false-reject rate.
- **Outputs.** Calibration table per dataset; reliability figure; FRR-transfer table.

### E4 (P0): Independent identity-preservation audit of SAM outputs
- **Objective.** Answer 3.5 and break the ArcFace circularity in R_i.
- **Data.** Generated faces already cached for calibration pairs (or regenerated with the frozen SAM).
- **Protocol.**
  - Score original-vs-generated and generated-vs-true-older-image similarity with AdaFace and MagFace, which are not used in the pipeline.
  - Stratify by target age gap, source age, sex, and race.
  - Run a blinded human study: raters see (source, generated) or (generated, real later photo) pairs mixed with real genuine and impostor pairs, and answer same/different. Report agreement and the effect of the generator on rater accuracy.
  - Repeat with a second generator (e.g., a diffusion-based or another StyleGAN-based age editor).
- **Metrics.** Identity-similarity distributions; TAR at fixed FAR of the independent recognizer on generated-vs-real pairs; human accuracy with Wilson CIs at the rater level.
- **Outputs.** Identity-preservation table and figure; failure examples, if the dataset licence permits publication.

### E5 (P0): Larger independent impostor pool for the FAR statement
- **Objective.** Move the certified FAR toward 1e-3 or better (3.2; Table III).
- **Protocol.**
  - Assemble person-disjoint random impostor pairs from additional licensed adult datasets (E1 data, plus large public sets with identity labels).
  - Target ≥ 3,000 independent pairs (≥ 6,000 persons) per dataset for 1e-3.
  - Report the calibration certificate and the held-out audit separately.
- **Statistics.** Exact Clopper–Pearson; design-effect sensitivity; person-clustered intervals for correlated pools.

### E6 (P1): Stronger and properly trained baselines
- **Objective.** Complete 3.7.
- **Protocol.**
  - Train the Siamese ViT to convergence (early stopping on train_val).
  - Evaluate AdaFace and MagFace embeddings, and at least one reproducible AIFR model with released code (e.g., OrdCon or MTLFace, if weights or code are available), as (a) stand-alone matchers in the three-way rule, and (b) replacements for ArcFace inside AAFV-Net.
- **Metrics.** As in E2.

### E7 (P1): Forensic characterization of the five Look-2 hard false accepts
- **Objective.** Answer 3.8.
- **Protocol.**
  - Re-score the test D_hard pairs with the frozen Look-2 artifacts **only to identify the five pairs**. Change no threshold. Log the action in `test_access.log` as "forensic, non-decision".
  - Report gap, sex, race, Q, R_sam, P_d, P_s, ArcFace cosine, and branch contributions.
  - Visually inspect the pairs under the dataset licence, and publish only categories.
- **Note.** The authors must decide whether this re-scoring is acceptable under their pre-registration. If not, report the gap as unresolved.

### E8 (P1): Effect of mined training negatives
- **Objective.** Test the hypothesis that the 98% D_hard rejection reflects training on similarly mined negatives.
- **Protocol.**
  - Re-train the full variant with (a) random-only negatives and (b) negatives mined by a different model (e.g., AdaFace).
  - Evaluate on calibration D_hard, D_neutral, and E1 hard sets.
- **Metrics.** Hard / neutral rejection, genuine coverage, certified FAR.

### E9 (P1): Intersectional fairness
- **Objective.** Answer 3.10.
- **Data.** MORPH calibration (race and sex labels available) and E1 data.
- **Metrics.**
  - Genuine A/R/X, impostor FA and rejection, and review rate by race × sex × age band, with person-clustered CIs.
  - Subgroup calibration (from E3).
  - Within-subgroup impostor pairs, because demographically matched impostors produce higher false-match rates.
- **Statistics.** Report differences and ratios with bootstrap CIs. Avoid relying on the 4/5ths rule alone.

### E10 (P1): End-to-end cost and cascade
- **Objective.** Answer 3.11.
- **Protocol.**
  - Profile the full pipeline on a stated GPU and CPU, cold and warm. Measure p50/p95 latency, throughput at concurrency 1/8/32, peak memory (`torch.cuda.max_memory_allocated`), and model-loading time.
  - Evaluate the cascade (direct branch first; SAM only for undecided pairs) for both cost and decisions. The cascade changes the decision function, so its certificate must be recomputed on calibration.
- **Outputs.** Cost table; cascade risk–coverage.

### E11 (P1): Degradation and threat robustness
- **Objective.** Cover the threat-model rows marked "partly in scope".
- **Protocol.**
  - Apply controlled blur, JPEG compression, down-sampling, and illumination change to calibration pairs.
  - Track zone transitions and verify that degraded pairs move to review rather than to acceptance.
  - Keep morphing and presentation attacks out of scope unless a morph-attack set is added.

### E12 (P2): Missing-branch robustness and fusion simplification
- **Objective.** Answer 3.12.
- **Protocol.**
  - Force I_sam = 0 at inference on all calibration pairs and report A/R/X and certified FAR.
  - Re-train a 7-input network without the constant slots and a 3-score variant (ArcFace + LPIPS + SSIM, dropping EfficientNet and VGG) as a next-generation design. Evaluate only on calibration and E1.

### E13 (P2): Reporting completeness from existing pair files
- **Objective.** Fill "n/r" person counts in Table VI and add per-bin CIs to Table IX.
- **Protocol.** Recompute from the pair CSVs and stored vectors without touching decisions on test. Person counts and bootstrap CIs for already-logged rates are descriptive.

### E14 (P2): Shared-target value at matched FAR
- **Objective.** Decide whether the shared-target grid should remain.
- **Protocol.** Use the K-sensitivity (K ∈ {0, 1, 3, 5, 7}) on calibration and E1, comparing coverage, review, neutral rejection, and cost at matched certified FAR.

---

## How results enter the manuscript

| Result | Destination |
|---|---|
| Every new evaluation | A new row in Table VI, with split, checkpoint, thresholds, persons, pairs, A/R/X, FA, source file |
| E1 | Replaces FG-NET as the primary external evidence (FG-NET kept) |
| E2 | Replaces the single-operating-point comparison as the main comparison against ArcFace, AdaFace, and MagFace |
| E3 + E9 | Replace Table X and the sex-only Table XIV |
| E4 | Required before any statement that generated faces carry identity evidence |
| Any experiment that contradicts a current claim | The claim is removed |
