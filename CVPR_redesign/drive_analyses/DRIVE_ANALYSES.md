# Results on the downloaded calibration data (Drive backup)

> Data: `drive_data/pair_vectors_calibration.csv` (363,647 pairs; the pre-quarantine `p5` copy) and `drive_data/faces.csv` (430,933 faces). Both git-ignored.
> Script: `run_drive_analyses.py` (outputs in `out/`). **Calibration split only.** The spent MORPH test split was not used.
> Nothing was trained except cross-fitted two-feature logistic probes. Bootstrap: 300 two-way person-cluster replicates, paired across methods.
> Prepared 2026-11-14.

## DA1: The frozen Look-2 decision layer is reproduced exactly
Re-scoring all pairs with the frozen `full` model (3 seeds, Platt calibrator, branch floors, guards and the margin rule) on the official calibration set (858 quarantined persons removed; 338,871 pairs) gives:

| | Recomputed | Published |
|---|---|---|
| T_accept | **0.956438** | 0.956438 |
| T_reject (β = 0.01) | **0.007541** | 0.007541 |
| Genuine auto-accept | **73.26%** | 73.26% |

The downloaded data and the reconstruction are therefore faithful. Every result below uses the same pipeline.

## DA2: The reported operating point exists only because 4 persons were removed after their scores were seen
Putting back the pairs of the 4 hand-quarantined persons (290132, 303269, 314177, 321217):

| ρ | Official set | Official + 4 persons |
|---|---|---|
| 0.20 (the published setting) | T_acc 0.9564, **73.26% accept** | T_acc **1.0291, 0% accept** |
| 0.35 | 0% | 0% |
| 0.50 | 0% | 0% |

**With the four persons included, no setting of the guarded system accepts anyone.** The pairs that force the threshold above 1 are D_hard pairs between 314177 and 321217:
- both aged 17 in the file names;
- gap 0;
- fused P = 0.995, guards pass;
- direct ArcFace z = 0.80, which is above almost all impostors but below the genuine median of 1.46.

Their 4 D_random pairs are harmless (max P 0.016), so the 0.349% certificate's own pool barely changed. The *operating point* did change, though, along with every accept rate reported for it (73.26% calibration, 79.74% Look 1, 70.07% Look 2).
Whether 314177 and 321217 are one person filed twice or two look-alikes needs their images. Either way, the removal was made after seeing the scores and must be disclosed.

## DA3: At matched FMR, SAM evidence adds nothing to ArcFace (Priority 2A on calibration)
TAR at FMR 10⁻³ (10⁻² where a bin has fewer than 3,000 impostors). Δ is relative to the direct ArcFace score, with a paired 95% cluster-bootstrap interval.

**vs random impostors (D_all_random):**
| Gap | n | ArcFace direct | SAM-branch ArcFace | AAFV-Net fused | LogReg [ArcFace, SAM-ArcFace] |
|---|---|---|---|---|---|
| 0–4 y | 22,914 | 0.996 | 0.920 (Δ −0.076 [−0.112, −0.051]) | 0.994 (Δ −0.002 [−0.004, −0.001]) | 0.996 (Δ 0.000) |
| 5–9 y | 594 | 0.682 | 0.609 (Δ −0.072 [−0.111, −0.032]) | 0.668 (Δ −0.013 [−0.024, 0.000]) | 0.682 (Δ 0.000) |
| 10–14 y | 174 | 0.655 | 0.644 (Δ −0.011) | 0.649 (Δ −0.006) | 0.655 (Δ 0.000) |
| 15–19 / 20–29 / 30+ y | 44 / 77 / 35 | 0.023 / 0.091 / 0.143 | identical | identical | identical |

- **Generated-only evidence is worse than original-only.** The CI excludes 0 at 0–4 and 5–9 years.
- **Adding the generated-face score to the original ArcFace score (cross-fitted logistic regression) changes TAR by exactly 0 in every bin.**
- The fused AAFV-Net score is slightly *worse* than ArcFace at 0–4 years, with the CI excluding 0.

**vs ArcFace-mined look-alikes (D_hard):**
- AAFV-Net is +0.003 at 0–4 years and +0.86 to +0.91 at 15+ years.
- The logistic regression on [ArcFace, SAM-ArcFace] gives no gain.
- So the look-alike advantage does not come from the generated evidence. It comes from the fusion network trained on similarly mined negatives (its other features and context).
- At 15+ years the "genuine" pairs are mostly mislabelled (DA4). The large Δ there means the network pushes mined look-alikes below even wrong-identity pairs; it is not a long-gap capability.

## DA4: MORPH long-gap "genuine" pairs are mostly different people
| Gap | n genuine | File ids differ within the pair | ArcFace impostor-like | Impostor-like if ids differ / same | **Sex letter differs within the pair** |
|---|---|---|---|---|---|
| 0–4 y | 22,914 | 27.5% | 0.2% | 0.8% / 0.0% | **0.0%** |
| 5–9 y | 594 | 49.7% | 31.5% | 58.3% / 5.0% | **1.9%** |
| 10–14 y | 174 | 36.8% | 34.5% | 79.7% / 8.2% | **2.9%** |
| 15–19 y | 44 | 79.5% | 97.7% | 97.1% / 100% | **20.5%** |
| 20–29 y | 77 | 77.9% | 90.9% | 96.7% / 70.6% | **18.2%** |
| 30+ y | 35 | 65.7% | 85.7% | 91.3% / 75.0% | **28.6%** |

("Impostor-like" means the pair scores below the 99th percentile of same-bin random impostors.)

- **Sex mismatches:** 49 of the 23,838 calibration "same-person" pairs have file names recording different sexes, e.g. `0771_00F16.JPG` (female, 16) vs `110771_08M48.JPG` (male, 48). None occur at 0–4 years; 18–29% occur at 15+ years.
- **The mechanism is consistent with ID merging.** Truncated or suffix-sharing record numbers (`0771` / `110771`, `0515` / `110515`) are merged into one person (`person_merge_map_v5.csv`). This links records of different people, who then look like long age gaps.
- Within 0–4 years the same merging is usually correct (0.8% impostor-like), which is why it went unnoticed.
- **Consequence:** MORPH as processed here has *no usable long-gap genuine data*, for training or evaluation. Every AAFV result above 15 years (including the "collapse" in AAFV-04 §VII-D) reflects label errors. This confirms LA4 and largely settles E1. A visual check of a small sample is still recommended for the paper.

## DA5: SAM identity drift grows with the age shift (ArcFace-based, so circular and with misaligned inputs; descriptive only)
| Direction | |shift| | n | ArcFace cosine to source (median / 10th pct) | Share < 0.30 | Median |age error| |
|---|---|---|---|---|---|
| Older | 0–4 y | 46,930 | 0.508 / 0.413 | 0.3% | 2.2 y |
| Older | 5–14 y | 80,657 | 0.485 / 0.387 | 0.8% | 2.9 y |
| Older | 15–29 y | 64,935 | 0.426 / 0.324 | 5.7% | 3.8 y |
| Older | 30+ y | 12,613 | 0.352 / 0.261 | **23.1%** | 4.8 y |
| Younger | 0–4 y | 47,789 | 0.513 / 0.417 | 0.3% | 2.4 y |
| Younger | 30+ y | 8,050 | 0.395 / 0.292 | 11.9% | 4.0 y |

- By target age, identity similarity falls from about 0.49 (targets 20–49) to 0.39 (60–69) and 0.34 (70+). The age error at 70+ is 10 years.
- **Even a 0–4-year shift takes the ArcFace cosine to the source down to about 0.51.** The generator changes the face substantially at every shift, consistent with the eye and brow edits in the image audit.
- **Aging hurts identity more than rejuvenation** at large shifts.
- These are exactly the long shifts that long-gap verification would need.

## What this changes
| Item | Before | After |
|---|---|---|
| W2 / Priority 2A (generated vs original evidence, MORPH) | Logs: no measurable value | **Confirmed per pair at matched FMR:** generated-only is worse; adding it gives Δ = 0; the look-alike gain is not from SAM |
| W4 / E1 (MORPH long-gap labels) | Strong indication | **Established without images:** 18–29% sex mismatch and 86–98% impostor-like at 15+ years |
| W5 (certificate and operating point) | Post-hoc exclusion confirmed | **Quantified:** without the 4 hand-quarantined persons the system accepts 0% at every ρ |
| Experiment 0 | The only test left for generated evidence | Still needed. These results use the in-pipeline ArcFace on MORPH, which has no valid long gaps. E0 uses independent recognizers on AgeDB/FG-NET |
