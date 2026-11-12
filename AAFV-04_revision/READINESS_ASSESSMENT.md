# AAFV-04 — Publication Readiness Assessment (IEEE TIFS)

**Verdict: Not ready for submission.** The manuscript is now technically honest and internally consistent, but the research does not yet meet a Transactions bar. If submitted in its present form, the most likely outcome is again *reject*, now for limited novelty and evidence breadth rather than for inconsistency or over-claiming.

## Scorecard

| Criterion (reviewer's Section 6) | AAFV-03 | AAFV-04 | What still blocks it |
|---|---|---|---|
| Relevance and significance | High | High | — |
| Technical novelty | Not convincing | Clearer, but still modest (decision protocol and a known certificate) | Direction N1, N2, or N3 |
| Technical soundness | Major concerns | Statistics correctly scoped; certificate independent of test; adaptivity disclosed | Untouched confirmatory test (E1); FRR under shift (E3) |
| Experimental validation | Insufficient | Insufficient (same data; more diagnostics) | E1, E2, E4, E6 |
| Clarity and reproducibility | Needs improvement | Good: consolidated populations, chronology, full feature table, scripts for every new number | Person counts; bibliography check; correction log (U-15) |
| Practical significance | Unclear | Clearer, and less favourable: ~3× ArcFace's review load on MORPH; FG-NET false rejects | Must improve with E1/E2 or be presented as a negative finding |

## What a TIFS reviewer would now say

**Positive:**
- Unusually transparent.
- Correct statistics.
- A useful observation that guards make zero-FA thresholds feasible.
- Honest threat model.

**Negative:**
- The proposed system underperforms a guarded ArcFace on the main dataset.
- The age-progression branch has no demonstrated benefit.
- The only external dataset has 82 persons and shows a large false-reject failure.
- No AdaFace, MagFace, or AIFR baselines.
- Evidence comes from one mugshot dataset dominated by gaps under 5 years.

## Minimum path to a credible resubmission

1. Run **E1** (AgeDB / CACD-VS / CALFW, frozen, one logged look each, pre-registered), **E2** (matched-FAR risk–coverage vs ArcFace / AdaFace / MagFace), and **E3** (calibration and FRR under shift).
2. Run **E4**. If generated faces do not add identity evidence at matched FAR, drop or redesign the SAM branch.
3. Adopt **direction N1** (shift-robust, person-clustered joint FAR / FRR control) as the methodological core. It directly addresses the FG-NET failure and the reviewer's "risk-control procedure" recommendation.
4. Then decide the venue. If the results remain mixed after E1–E4, a biometrics-focused venue (e.g., IEEE T-BIOM, IJCB) is a better fit than TIFS for a decision-protocol paper with negative findings.

## What is ready now

- `manuscript/main.tex` + `main.pdf`: a correct, consistent, 12-page draft. Usable as the base for the resubmission once new results replace the "Required" items.
- `analysis/a1_look1_posthoc.py`, `a2_figures.py`: reproducible sources for every new number and figure.
- `REVIEW_RESPONSE_MATRIX.md`: can be adapted into the response letter once experiments are done.
