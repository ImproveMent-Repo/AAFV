# Audit of the supplied result images (`Result_Images/`)

> Prepared 2026-11-13. Inputs: the only two images supplied, `sam_sheet.jpeg` and `audit_fg_fa.png`. No face recognizer is available on this machine, and installing one would need a download that has not been approved. Everything here is visual inspection plus image-level measurement (`measure_sam_sheet.py` → `out/`).
> **Two people and four pairs are anecdotes.** This audit can supply the qualitative figures a CVPR paper needs and can suggest mechanisms. It cannot establish whether generated faces preserve identity. That remains Experiment 0.

## 1. `sam_sheet.jpeg`: SAM-age outputs for two people
**Layout, verified by measurement.** Each row shows one person as [original, SAM output] three times. Tiles 1, 3 and 5 are the same original: after a ~5.5 px horizontal offset they agree to within 0.1–0.6/255 mean absolute difference. Tiles 2, 4 and 6 are three different SAM outputs. Visually they are a younger, a similar and an older target age. The exact target ages are not printed on the sheet.
The backgrounds (red curtain, plaid shirt; grey-blue wall) and the scan quality suggest FG-NET-type photographs. I have not verified that.

**What the generator changes** (`out/sam_change_maps.png`: original | output | per-pixel change):
1. **The eyes change most.** In all six outputs the largest pixel changes sit on the irises. The younger outputs give both people lighter, bluer-looking eyes (eye-band Lab b* shift −2.3 and −1.5 in row 1, pairs 1–2). The periocular region is where face recognizers concentrate.
2. **A distinctive identity cue is edited away.** Row 2's original has a thick, joined eyebrow (a unibrow). The younger and similar-age outputs thin and separate it. The older output keeps more of it. This is exactly the failure that a reliability score built on ArcFace may not catch, and an independent recognizer is needed to measure it.
3. **Non-identity content is regenerated.** The background turns into the blurred FFHQ-style backdrop, the clothing changes, and a scratch on row 2's scan disappears.
4. **Synthetic fine texture is added.** On the unshifted tiles the face region's Laplacian variance is 1.6–2.5× higher in the outputs. At half resolution it is still 1.3–1.5× higher for the blurrier row-1 photo, but about equal for row 2 (0.89–0.97). So the generator adds fine-scale texture that was not in a low-resolution source. Part of the full-resolution ratio may come from the sheet's own resizing and JPEG compression, so this is weak evidence.
5. **Global lightness drifts by a few Lab units** (−1.5 to −7 L*), more for the older outputs.

**What this means for the plan.**
- It is consistent with the logged result that the SAM branch adds nothing measurable (`log_analyses/LOG_FINDINGS.md`, Finding 2). A generator that rewrites the eye region and removes distinctive brows supplies little *identity* evidence, even when the face looks plausible.
- It sharpens Experiment 0: identity preservation should be reported per facial region, and per target-age direction (younger vs older), not only as one cosine.
- These panels, with their change maps, are suitable as the qualitative "success and failure of synthesis" figure that the review (W2) asks for. They must be labelled as illustrative, because n = 2.

## 2. `audit_fg_fa.png`: the four FG-NET all-ages false accepts
| Pair | Ages (from file names) | Fused P |
|---|---|---|
| 069A00 vs 023A00 | 0 vs 0 | 1.000 |
| 019A00 vs 024A00 | 0 vs 0 | 0.993 |
| 021A03 vs 064A04 | 3 vs 4 | 0.966 |
| 070A00 vs 010A01 | 0 vs 1 | 0.999 |

**What the images show.**
- These are different children by the dataset's labels. To a human viewer they differ in face shape, hair and expression.
- Three of the four pairs involve infants under 1 year.
- All four are short-gap pairs (0–1 year), photographed under poor conditions: colour-cast scans, red tint, low resolution and a hood.
- The system is close to fully confident on all of them.

AAFV-03/04 identified these pairs by file name and age only; neither manuscript shows or discusses the images. (AAFV-04's statement that no false-accept image was inspected refers to the MORPH test false accepts, which are still uninspected.)

**What can be inferred, and what cannot.**
- Guarded ArcFace made **0 false accepts in the same 20,000 FG-NET impostor pairs** (AAFV-04 Table XI). So the false accepts arise in the fused system, not in ArcFace's own decision.
- The logs do not hold per-pair scores for these pairs, so the share of the fused score due to the SAM branch, the context inputs or the calibration cannot be separated.
- One plausible mechanism, **not tested**: for age-0 inputs the 5-year grid snaps both images to the same young target, and the generator's infant prior produces similar "prototype" babies, which inflates the SAM-branch similarity.
- The pediatric exclusion (adults ≥ 16) remains a post-hoc scope decision. These images justify it as a known failure mode but do not make it pre-specified. Experiment 0 pre-registers the scope and reports children separately.

## 3. What these images do and do not change
| Brief item | Effect |
|---|---|
| 2B identity preservation | **Qualitative only.** Edits concentrate on eyes and brows, and a distinctive cue is removed. Quantitative test still needs Experiment 0 |
| 2D where generated evidence misleads | **Qualitative only.** Infant pairs are accepted with P ≈ 1 by the fused system but not by ArcFace. The cause cannot be attributed from the logs |
| W2 qualitative success/failure figure | **Material available:** `out/sam_change_maps.png` and `Result_Images/audit_fg_fa.png` |
| Direction decision (Experiment 0) | **Unchanged.** It still needs a recognizer outside the pipeline on many pairs |

## 4. Image handling
The derived images in `out/` show faces from a licensed dataset. They are excluded from git (`.gitignore`), as the Experiment 0 outputs already are. `Result_Images/` is left untracked. Check the FG-NET licence before any image goes into a public repository or a paper.
