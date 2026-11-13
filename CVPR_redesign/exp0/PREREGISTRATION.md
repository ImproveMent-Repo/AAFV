# Experiment 0: Pre-registration

**Status:** DRAFT. It becomes binding when the team commits this file *before* any embedding of generated faces is computed.
Record the commit hash here: `________`. After that commit, changes to anything in Sections 2–6 must be logged in Section 8 together with the reason.

## 1. Question
Measured with face recognizers that are **not** part of AAFV-Net, does an age-progressed image make a genuine
cross-age pair more separable from a gap-matched impostor pair than the two original images alone?
In particular, does it do so at long age gaps (15 years or more)?

This experiment decides whether any generator-centred research direction is pursued (Stage-1 assessment, Section D.0).

## 2. Data and pairs (fixed by `config.yaml` and `s3_pairs.py`)
- **Datasets:** AgeDB and FG-NET. No MORPH data is used; the MORPH test split is spent.
- **Folds:** persons are assigned to 5 folds with the fixed seed in `config.yaml`. All pairs, genuine and impostor, are formed **within** a fold, so every pair belongs to exactly one fold.
- **Genuine pairs:** two images of the same person, ordered so that a₁ ≤ a₂, with gap = a₂ − a₁. At most 20 pairs per person per gap bin, sampled with the fixed seed.
- **Impostor pairs (age-matched swap):** for each genuine pair (I₁, I₂), up to 10 impostors (I₁, I₂′) are formed. I₂′ is an image of a different person in the same fold, with |age(I₂′) − a₂| ≤ 2 years (widened step by step to at most 4 years) and the same sex when both sexes are known. Impostors inherit the genuine pair's gap bin and ages.
- **Gap bins:** `0-4`, `5-14`, `15-29`, `30+` years (edges 0, 5, 15, 30).
- **Strata:** the *adult* stratum requires every image in the pair to be at least 16 years old. The *all-ages* stratum includes children. Both are reported. **The decision uses the adult stratum.** This scope is fixed now, before any result is seen.

## 3. Generation (fixed)
- **Generators:** SAM-age (Alaluf et al. 2021, official FFHQ-aging checkpoint) and FADING (Chen & Lathuilière 2023). The `identity` backend (it returns the input unchanged) is used only to test the pipeline. It is never part of the decision.
- **Targets:** I₁ is progressed to round(a₂) (forward). I₂, and each impostor I₂′, is regressed to round(a₁) (backward). Target ages are clipped to each generator's range. The forward job is shared between a genuine pair and its impostors, so both receive exactly the same operation on I₁.
- **Inputs:** the 256×256 FFHQ crop produced by `s2_align.py`, identical for both generators.

## 4. Scores (fixed)
- **Recognizer input:** every face, real or generated, goes through the same steps: SCRFD detection on the 256 crop, five landmarks, `norm_crop` to 112×112. A detection failure on a generated face counts as a generation failure.
- **Recognizers:** AdaFace IR-101 and MagFace iResNet-100 are the *independent* recognizers that enter the decision. ArcFace (`buffalo_l`) is reported for reference only.
- **Preflight:** on original images in the `0-4` bin, the AUC of s₀ must be at least 0.95. Otherwise the run is aborted, because preprocessing is wrong.
- **Pair scores:**
  - s₀ = cos(h(I₁), h(I₂))
  - s_fwd = cos(h(G(I₁→a₂)), h(I₂))
  - s_bwd = cos(h(I₁), h(G(I₂→a₁)))
  - s_bridge = (s_fwd + s_bwd)/2
- **Fused score:** logistic regression on standardized [s₀, s_fwd, s_bwd], with no gap or age features and balanced class weights. It is **cross-fitted**: the model for fold k is trained on the other folds, pooled over all bins and both strata, separately for each recognizer × generator.
- **Complete-case set:** the primary analysis uses pairs for which every decision generator produced detectable faces for both jobs. Failure rates are reported per generator, target age and gap bin.

## 5. Metrics (fixed)
- **Primary:** TAR at FMR = 10⁻³, with the threshold set *within each gap bin* on that bin's impostors.
  - If a bin's impostor weight is below 3,000, the primary FMR for that bin is 10⁻² instead. This rule is pre-registered and the actual value is reported.
- **Secondary:** AUC per bin; mean identity preservation cos(h(G(I,t)), h(I)) per |t − a| bin; mean s_fwd − s₀ for genuine and for impostor pairs; generation failure rates.
- **Uncertainty:**
  - A two-way person-cluster bootstrap with 1,000 replicates. Persons are resampled with replacement; a genuine pair is weighted by the count of its person and an impostor pair by the product of the counts of its two persons.
  - Differences (fused − s₀) are computed on the same replicate.
  - The fused model is **not** refitted inside the bootstrap. This understates uncertainty slightly, and we accept and report that.
- **Multiplicity:** the decision family has 2 independent recognizers × 2 generators × 2 long-gap bins = **8 tests**. Decision intervals are Bonferroni-adjusted two-sided **99.375%** (α = 0.05/8) percentile intervals.

## 6. Decision rule (fixed)
- **GO** requires all of the following:
  1. For at least one (independent recognizer, real generator, bin ∈ {`15-29`, `30+`}) in the adult stratum, the lower bound of the adjusted interval of ΔTAR (fused − s₀) is above 0.
  2. For that same combination, the **age-only control** does not show a gain: its adjusted ΔTAR interval must include 0 or lie below it. In the control, each generated embedding is replaced by the generated embedding of a different, randomly chosen person's job with the same target age in the same fold.
  3. The preflight passed for that recognizer.
- **NO-GO:** otherwise.
- A GO in only one bin, or only for one generator, is reported as *narrow*.

Secondary metrics never override the decision. They are used only to describe the result.

## 7. What a NO-GO means
The generated evidence has no demonstrable identity value under independent recognizers at long gaps on these data.
Generator-centred directions D.1 and D.2 are then dropped, and the result is reported as a negative finding.

## 8. Deviations log
| Date | Change | Reason | Made before or after seeing generated-face embeddings? |
|---|---|---|---|
| | | | |
