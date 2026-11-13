# Changes from AAFV-04 to AAFV-05

AAFV-05 is a different paper, not a revision. AAFV-04 presented AAFV-Net as a contribution. AAFV-05 re-analyses it and reports what holds and what does not.

## Claims withdrawn or corrected
| AAFV-04 claim | AAFV-05 position | Evidence |
|---|---|---|
| A random-impostor FAR certificate of 0.349% (headline) | The bounds are arithmetically correct but **do not distinguish methods** (plain ArcFace attains the same). Their assumptions are compromised by development on the calibration split and by a post-hoc exclusion. They are not presented as evidence about the method | Tab. V; §IV-E |
| Reliability-gated SAM evidence as a contribution | **No measurable contribution at matched FMR.** Generated-only is worse; adding it gives Δ = 0 | Tab. III; §IV-C |
| 98.04% rejection of look-alikes as a property of the system | Present without SAM; consistent with training on similarly mined negatives | §IV-C |
| "Guards are essential" | Guards are needed only because of this fused score's impostor tail. They do not change ranking and they reduce automation | Tab. II; §IV-B |
| MORPH long-gap "collapse" attributed to scarcity | Caused by **label-linkage errors** (18–29% sex mismatch, 86–98% impostor-like) | Tab. VI; §IV-F |
| Operating point at T_acc = 0.9564 (ρ = 0.20) | **Depends on 4 identities removed after their scores were seen.** Without them, 0% acceptance | Tab. I; §IV-E |
| 5-seed ensemble | The evaluated (Look-2) checkpoint has **3** networks | §III-C |
| ArcFace baseline | It was fed resized FFHQ crops, not standard alignment | §III-C |
| Bonferroni audit bound "0.320%" | Rounds to **0.321%** | Tab. V |

## Kept
- Person-disjoint splitting, duplicate-identity quarantine (now with the post-hoc additions disclosed), and the logged test budget.
- Honest reporting of negative results.
- The three-way decision as an application concept. It is not a contribution here.

## New in AAFV-05
- Exact reconstruction of the frozen pipeline from recovered per-pair vectors.
- Per-pair, paired-bootstrap comparisons at matched FMR.
- A probe of the trained fusion network against untrained controls.
- The label-integrity analysis from file names, which needs no images.
- SAM identity drift over 379,930 generated faces.
- A pre-registered protocol (Experiment 0) for the open question.

## Removed
- The 0.349% headline.
- The Siamese/VLM comparisons (unconverged baselines).
- Most component-positioning text.
- Unrelated references: of the 69 entries in AAFV-04's bibliography, only those the new text uses are kept. `references.bib` has 48 entries, 8 of them newly verified.
