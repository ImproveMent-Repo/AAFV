# What the logged AAFV results show (no images, no new runs)

> Prepared 2026-11-13 from files already in `Code/AAFV_Net/`. Reproduce with `python run_log_analyses.py`; all tables and figures are in `out/`.
> No model was trained and no threshold was set.
> LA4 reads logged MORPH **test** outputs (Look-1 fused P, Siamese-ViT logits). It is post hoc and descriptive and does not count as a test look.
> Confidence intervals in LA4 resample pairs, because person ids were not logged, so they are too narrow.
> LA1 intervals come from the original pipeline. Its bootstrap replicates were not saved, so differences between methods can only be judged by CI overlap.

## Finding 1: at matched FPR, AAFV-Net ranks pairs no better than ArcFace. The 70% vs 89% gap comes from the decision layer.
On the full MORPH calibration split, TPR at FPR = 0.1% is the same for AAFV-Net, ArcFace-only, the 5-score logistic regression and the direct-only MLP in every populated bin (`la1`):

| Gap bin | n genuine | AAFV-Net | ArcFace only | Direct 5-score LogReg | Direct-only MLP (no SAM) |
|---|---|---|---|---|---|
| 0–4 y | 22,914 | 0.992 | 0.990 | 0.991 | 0.991 |
| 5–9 y | 594 | 0.668 | 0.668 | 0.670 | 0.667 |
| 10–14 y | 174 | 0.649 | 0.649 | 0.649 | 0.655 |

Yet on the same split AAFV-Net auto-accepts 73.3% of genuine pairs, against 87.7% for guarded ArcFace (`la2`: same_accept_all).
The difference therefore comes from where each method's zero-calibration-FA threshold lands (T_acc 0.956 with guards vs 0.850), not from discrimination.

On random impostors overall, ArcFace's AUC is slightly higher (0.992 vs 0.987). Its G1 AUC CI does not overlap AAFV-Net's (0.9987 vs 0.9962).
**Consequence for Priority 3:** the right comparison is at matched FPR, and there AAFV-Net is level with ArcFace, not ahead.

## Finding 2: the logs show no measurable value from the SAM branch at matched FPR
- **Full vs direct-only MLP** (identical except for the SAM branch): TPR@FPR 0.1% differs by ≤ 0.006 in bins 0–14 y. Every AUC and TPR CI overlaps in all six bins.
- **Mined look-alikes:** the direct-only MLP has the same hard-impostor AUC (0.998) and TPR@0.1% (0.971 vs 0.973) as the full system. **The look-alike advantage over ArcFace comes from the learned fusion trained on mined negatives, not from generated faces.**
- **SAM-only vs direct-only** (generated-only vs original-only, the brief's Priority 2A): SAM-only is clearly *worse* at low FPR where data exist (TPR@0.1%: 0.862 vs 0.991 at 0–4 y; 0.502 vs 0.667 at 5–9 y; CIs separated). It has higher AUC at 20–29 y and 30+ y (CIs separated), but those bins hold 77 and 35 genuine pairs, which Finding 3 shows are probably mislabelled. They cannot be read as evidence.
- **Shared targets, reliability R_sam, branch masking:** removing any of them changes no TPR@0.1% by more than 0.013 (one pair in a 77-pair bin) and moves no CI apart. Branch masking matters only at the decision level (3.4% accept without it), not for ranking.
- **Guards:** every guard ablation gives *identical* ranking metrics. Guards act only on the threshold, which is consistent with Finding 1.

**What this does and does not settle.** Within MORPH, using these frozen scores and this fusion design, the generated evidence adds nothing measurable. It does *not* settle whether generated faces carry identity information at real long gaps under an independent recognizer. That needs Experiment 0, because MORPH has no usable long-gap pairs (Finding 3).

## Finding 3: MORPH's long-gap "genuine" pairs are almost all impostor-like for two unrelated models. The labels are probably wrong.
On the MORPH test split (`la4_impostor_like_genuine.csv`), this is the share of genuine pairs that score *below the 99th percentile of random impostors in the same gap bin*:

| Gap bin | n genuine | AAFV-Net | Siamese ViT | Both | Expected if independent |
|---|---|---|---|---|---|
| 0–4 y | 23,631 | 0.4% | 4.3% | 0.3% | 0.02% |
| 5–9 y | 266 | 13.9% | 20.3% | 13.9% | 2.8% |
| 10–14 y | 184 | 23.9% | 23.9% | 22.3% | 5.7% |
| 15–19 y | 75 | **97.3%** | **97.3%** | 97.3% | 94.7% |
| 20–29 y | 137 | **94.9%** | **97.8%** | 94.9% | 92.8% |
| 30+ y | 12 | 0% | 0% | 0% | 0% |

The two models share no features: the ViT was trained end-to-end on pixels, and AAFV-Net uses frozen ArcFace-based scores. They fail on the *same* genuine pairs far more often than chance (5–14 y), and on nearly all of them at 15–29 y.
Every calibration method is at chance at 15–19 y (AUC ≈ 0.43–0.59). Modern recognizers are far above chance on real 15–30-year adult gaps (published AgeDB-30 accuracy is about 98%).
The 30+ y bin points the other way: all 12 pairs are trivially matched, which looks like *age-label* errors on near-identical photos.

The calibration audit sheet (`Code/AAFV_Net/q/audit/audit_same_bottom50.jpg`) contains at least one certain identity error: pair 22, 12-year gap, two people differing visibly in sex and apparent ethnicity. It also shows that one "person" (`239029`) has photos whose filenames start with four different numbers (`239029_`, `39029_`, `229029_`, `9029_`).

**Interpretation, a hypothesis to verify with the MORPH index and images:** under this pipeline's identity mapping, long-gap genuine pairs in MORPH are dominated by mislinked records (wrong identity) or wrong ages. Mislinking two people's records produces arbitrary, and therefore often large, "age gaps", which would explain why errors concentrate in the long bins.

**Consequences:**
- AAFV-04's account of a long-gap "collapse due to scarcity" (Section VII-D) is probably wrong. The bins are contaminated, not merely small.
- MORPH cannot support any long-gap claim (Priority 4). Long-gap evidence must come from AgeDB and FG-NET, which is how Experiment 0 is already designed.
- Label noise in the 5–14 y bins (about 14–22% impostor-like for both models) also caps every method's MORPH TPR at about 0.65–0.83.

## Finding 4: the "hard impostor" advantage is a property of the training negatives
On the MORPH test split (`la4_test_matched_fmr.csv`), AAFV-Net ranks even the impostor-like 15–29 y "genuine" pairs above ArcFace-mined look-alikes (TPR 0.93–0.99 vs `D_hard`). The independent ViT ranks the mined look-alikes *above* those genuine pairs (AUC 0.15–0.25).
AAFV-Net pushes mined look-alikes to very low scores whatever the genuine pair looks like. That is the signature of a pool that is in-distribution for the training negatives (half of training negatives were mined the same way), not of general look-alike robustness. It confirms the caution AAFV-04 itself raised.

## Finding 5: FG-NET cannot isolate the SAM branch from the logs
At each method's own zero-calibration-FA threshold, the direct-only MLP and all three end-to-end baselines accept 0% of FG-NET adults (T_acc ≥ 0.98), so there is no non-SAM learned comparator at a usable operating point (`la5`).
AAFV-Net beats ArcFace in every bin (e.g. 28.5% vs 14.5% at 20–29 y), but with 18.2% false rejects vs 0.3%. The logs hold no per-pair FG-NET scores for AAFV-Net or ArcFace, so a matched-FPR comparison is impossible.

## What the logs cannot answer (needs images; Experiment 0 covers it)
- Identity preservation of generated faces under an independent recognizer (2B).
- Generator comparison (2C).
- Whether R_sam predicts identity preservation (2D).
- Any matched-FPR comparison with ArcFace on FG-NET or the MORPH test split.
- AdaFace and MagFace baselines.
- Person-clustered intervals on the test split.

## Effect on the plan
1. **Stop citing MORPH for long-gap behaviour.** In the next manuscript, MORPH is a short-gap training and calibration source with a documented label-noise problem.
2. **The SAM branch has no supporting evidence in any logged artifact.** Experiment 0 is now the *only* remaining route to a generator-centred contribution. A NO-GO there means dropping the branch.
3. **The MORPH label-noise finding is itself reportable.** It is a data-hygiene result that affects any AIFR work using this MORPH copy. Checking it needs the MORPH index file and a visual check of a random sample of long-gap genuine pairs (images only, no GPU).
