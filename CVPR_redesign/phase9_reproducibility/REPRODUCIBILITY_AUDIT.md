# Phase 9: Reproducibility and Available Resources

> Brief Section 9: inspect the available artifacts and identify exactly what can be reproduced without retraining. Distinguish inference, fine-tuning, training, recomputing metrics and generating qualitative evidence. Give each experiment's computational requirements. Do not claim reproduction until outputs are verified.
> Prepared 2026-11-13. Every "verified" item below was checked by running code today. Nothing was installed or committed.

## 1. What was checked, and the result
| Check | How | Result |
|---|---|---|
| Frozen-model hashes | SHA-256 of all 26 `ablations/variants/*/frozen.pkl` vs `ablations/ablation_freeze.json` | **26/26 match** |
| Ledger hash | SHA-256 of `ablation_freeze.json` | `c66c4266…81ed`, **matches** `comprehensive_context.md` §13.3 |
| Look-1 thresholds | `thresholds.json` (LF-normalised) vs `thresholds.sha256` and `q/logs/test_access.log` | **Match** (`4b7af977…2cfe`) |
| Test-access log | Count of logged looks | **2**, as stated |
| AAFV-04 numbers | 43 stated values re-derived from the logged CSV/JSON files (`verify_artifacts.py`) | **42 match.** 1 rounding issue: the Bonferroni bound 0.32054% is printed as "0.320%" but rounds to 0.321% (or 0.32%) |
| Model description | Seed count in the Look-2 `full` checkpoint | **3 seeds, not the 5 stated** in AAFV-04 §V-D and Table XV. Look 1 used 5 |
| AAFV unit tests | `Code/AAFV_Net/tests/test_core.py` (17 tests), run with an in-memory stand-in for the `pytest` import (the suite uses no pytest features) | **17/17 pass** |
| Experiment 0 tests | `exp0/tests/test_exp0.py` | **8/8 pass**, including the simulated GO and NO-GO runs |
| Determinism of the new analyses | Re-ran `log_analyses`, `architecture_review`, `image_audit` and `phase9_reproducibility`; compared SHA-256 of all 12 CSV/TXT outputs | **12/12 byte-identical** |

Full table: `verification_report.csv` / `verification_report.txt`.

## 2. Provenance gaps (most serious first)
1. **`Code/` is git-ignored in this repository** (`.gitignore`: "Core implementation maintained separately").
   - None of the frozen models, logs, CSVs or pipeline scripts behind AAFV-01 to AAFV-04 has history here.
   - The hashes above prove the files are internally consistent today. They cannot show what existed when the looks were run.
   - **Action:** identify the external repository and commit (the README cites `ImproveMent-Repo/AAFV`), or deposit `Code/AAFV_Net` minus licensed data in an archive with a DOI.
2. **The Look-2 access-log entry has no hash** (`look=2 p12_extended`). The Look-2 checkpoint is pinned only in `ablation_freeze.json`, which is not itself recorded in the log.
3. **Label corrections:** the calibration code supports post-hoc relabelling (`label_corrections.csv`, `--extra_people`), and no record says whether it was used (Stage-1 §B.3).
4. **Per-pair outputs** were saved only for the Look-1 test and the baselines. There are none for Look 2, the calibration fused scores or FG-NET. This is why matched-FMR curves against ArcFace cannot be reproduced.
5. **Feature vectors, crops, SAM outputs and fusion weights** (`artifacts/p5`, `/dev/shm/aafv/*`, `fusion_seed*.pt`) are not present. `params.yaml` has empty data paths.
6. **Recorded deviations in `params.yaml`:** `RANDOM_DIFF_PAIRS` was reduced from 1,000,000 to 300,000 ("stage A"). The pipeline fed ArcFace FFHQ crops resized to 112 px instead of using ArcFace's alignment (`p5_faces.py`).
7. **External weights are not hash-pinned in the repository:** InsightFace `buffalo_l`, the SAM checkpoint, DEX, VGG. Only the SAM checkpoint's hash is mentioned, in a pipeline comment.

## 3. Inventory: what each artifact can still do
| Artifact | Location | In git here? | Can support |
|---|---|---|---|
| Look-1 per-pair fused P (339,011 test pairs; set, label, gap bin, sex, zone) | `Code/AAFV_Net/q/report/test_pair_zones_look1.csv` | No | Post-hoc descriptive analyses (LA4); fairness by sex; per-bin ROC for AAFV only |
| Variant rate tables (26 variants × 3 β; calibration, test, FG-NET) | `Code/AAFV_Net/ablations/*.csv` | No | Re-deriving every AAFV-04 table (done: 42/43) |
| Per-bin ranking metrics, 23 variants (calibration) | `ablations/results/gap_report_calibration.csv` | No | Matched-FPR comparisons (LA1) |
| Frozen fusion models, calibrators, guards, thresholds (26 variants) | `ablations/variants/*/frozen.pkl` | No | Model inspection (probe P1). Re-scoring would need the missing feature vectors |
| Siamese ViT/CNN and VLM per-pair logits | `baselines/*/*.npz` | No | Baseline curves on identical pairs (LA4) |
| Audit contact sheets (calibration top impostors, bottom genuine) | `q/audit/*.jpg` | No | Visual audit (done) |
| Supplied result images | `Result_Images/` | No (untracked) | Qualitative audit (done) |
| AAFV-04 manuscript sources and figure scripts | `AAFV-04_revision/` | Yes | Regenerating AAFV-04 figures and tables from the CSVs |
| New analyses (this redesign) | `CVPR_redesign/` | Partly (Phases 5–10 uncommitted) | All findings in Phases 1–9 |

## 4. What can be reproduced without retraining
| Category | Reproducible now? | Items |
|---|---|---|
| **Recompute metrics from logs** | **Yes.** 43 key values verified today; the remaining cells of the same tables come from the same files | AAFV-04's decision-rate tables (key values of Tables VI, VII, IX counts, XI, XII, XIV, and the full-system CI of Table XVI) and the certificate arithmetic; LA1–LA5; fusion probe; calibration diagnostics of the Look-1 P (AAFV-04 `a1_*` scripts, not re-run here) |
| **Inference with existing AAFV weights** | **No** | The fusion weights exist, but their inputs (pair feature vectors) do not. Re-scoring needs the full p1–p5 pipeline on licensed images |
| **Inference with public weights** | Not yet (needs data, a CUDA PyTorch build and weight downloads, none approved) | E0, E2 embeddings, E5 generation, E11 runtime |
| **Fine-tuning an existing model** | No (needs data and GPU) | E7 (MTLFace FT-Sel style, Banerjee-style ArcFace fine-tune) |
| **Training a new model** | No | E4 heads (small), E13 |
| **Qualitative evidence** | Partly done | Image audit of the 2 supplied sheets; MORPH audit sheets. E1 and E10 need more images |

## 5. Compute needed per planned experiment (from Phase 6; reported speeds are the AAFV pipeline's own figures)
| Experiment | Kind | Compute | Can it run on the laptop (RTX 4060, 8 GB) once software is approved? |
|---|---|---|---|
| E1 MORPH audit | Visual + index check | None | Yes (no GPU) |
| E0 generated-evidence probe | Inference | SAM ≈ 0.06 s per face (reported); FADING ≈ 90 s per image + 26 s per age (reported) | SAM and recognizers: very likely. FADING: unverified (diffusion; may not fit in 8 GB at fp32) |
| E2 baselines | Inference + tiny calibrators | Minutes per dataset | Yes |
| E3 certificate | CPU | Seconds | Yes |
| E4 transport head | Small training on cached embeddings | Minutes to hours | Yes |
| E5 generator comparison | Inference at scale | Hours (SAM) to days (FADING) | SAM yes; FADING uncertain |
| E6, E8, E9, E10 | Analysis | CPU | Yes |
| E7 prior-art fine-tunes | Fine-tuning a backbone | Days of GPU | Unlikely on 8 GB; needs a larger GPU |
| E11 runtime | Timing | Minutes | Yes |

## 6. Reproducibility package required for the new paper
1. A public repository (or an anonymised one for review) with all scripts. Every result table regenerates from logged **per-pair** scores with one command, as `run_log_analyses.py` and `verify_artifacts.py` do now.
2. Hash manifests for every model checkpoint (ours and third-party), for the pair lists and fold assignments, and for each pre-registration commit.
3. Per-pair score files for every method, dataset and split, so that ROC, DET and risk–coverage curves can be recomputed without images.
4. A data statement: licences, access instructions and identity-list files only (no images), plus withdrawn-dataset status of any pretraining set (Phase 8 §1).
5. An environment file with exact package versions, and the hardware used for E11.
6. A test-access log that records the hash of what was evaluated **for every look**.
