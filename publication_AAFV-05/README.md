# AAFV-05: *Does Synthetic Age Progression Help Cross-Age Face Verification? A Controlled Re-Analysis of a Reliability-Gated Three-Way Verifier*

**Status:** complete draft, **not submitted**. It compiles to 7 pages (IEEEtran journal format).
The text was drafted with an AI assistant and **must be revised by the authors** before any submission. See `SUBMISSION_CHECKLIST.md`.

## What this paper is, and why
The advisor's brief asked for a CVPR-level method paper. The proposed method (reliability-weighted age transport) depends on experiments that have not been run: Experiment 0 and E4 in `CVPR_redesign/phase6_experiments/EXPERIMENT_PLAN.md`. Writing it now would mean inventing results.

AAFV-05 is therefore the paper the **existing evidence supports**: a controlled re-analysis of AAFV-Net (AAFV-01 to AAFV-04). It shows:
1. At matched FMR the fused system ranks pairs no better than ArcFace, and the 70.07% vs 89.45% acceptance gap comes from the decision layer.
2. Generated (SAM) evidence adds nothing at matched operating points, and the fusion network relies on ArcFace.
3. The published operating point exists only because four calibration identities were removed after their scores were seen.
4. MORPH long-gap "same-person" pairs are dominated by linkage errors.
5. A pre-registered protocol is described for the question that remains open.

**Suitable venues:** a biometrics journal or conference (e.g. IEEE T-BIOM, IJCB) or a CVPR/ICCV workshop, not a CVPR main track. If Experiment 0 later returns GO and the method succeeds, Paper A (`CVPR_redesign/phase8_manuscript/MANUSCRIPT_BLUEPRINT.md`) supersedes this.

## Folder contents
| Path | What |
|---|---|
| `main.tex`, `main.pdf` | Manuscript and compiled PDF |
| `references.bib` | 48 entries: 40 reused from the audited AAFV-04 bibliography, 8 verified on 2026-11-13. Built by `scripts/build_bib.py` |
| `tables/*.tex` | All 7 tables, **generated** by `scripts/build_assets.py` from the analysis CSVs. Do not edit by hand |
| `figures/*.png` | 3 aggregate plots copied from the analysis outputs. **No face images** (licensed data) |
| `scripts/build_assets.py` | Regenerates tables and figures |
| `scripts/build_bib.py` | Regenerates the bibliography |
| `scripts/check_claims.py` | Checks the 33 numbers written in the prose against their source files (currently 33/33) |
| `build.sh` | One-command build: assets → bibliography → claim check → LaTeX |
| `CLAIMS_LEDGER.md` | Every result in the paper mapped to the file and script that produce it |
| `CHANGES_FROM_AAFV-04.md` | What changed, and which earlier claims are withdrawn or corrected |
| `SUBMISSION_CHECKLIST.md` | Everything still needed from the authors before submission |
| `supplementary/` | Pre-registration of the open experiment, and the analysis-script index |
| `IEEEtran.cls`, `IEEEtran.bst` | IEEE class files (copied from AAFV-04) |

## How to rebuild
```bash
bash build.sh
```
This needs Python 3 with pandas and matplotlib, and a LaTeX distribution (MiKTeX was used).
The analysis outputs it reads live in `../CVPR_redesign/*/out/`. To regenerate those from raw logs and data, run, in order:
1. `CVPR_redesign/log_analyses/run_log_analyses.py`
2. `CVPR_redesign/architecture_review/probe_fusion.py`
3. `CVPR_redesign/drive_analyses/run_drive_analyses.py`

The third script needs `CVPR_redesign/drive_data/`, which is git-ignored and was downloaded from the project's Drive backup.

## Data handling
- No images from MORPH or FG-NET are included anywhere in this folder.
- The downloaded calibration vectors (`../CVPR_redesign/drive_data/`) are git-ignored.
- The MORPH test split was **not** used for any new analysis. Test-split numbers in the paper are either the earlier logged results or post-hoc descriptive readings, and they are labelled as such.
