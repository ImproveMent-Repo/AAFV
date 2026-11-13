# Findings from the shared Google Drive backup (`miniproject_backup`)

> Inspected 2026-11-14 in the built-in browser, by viewing folder listings and one text log. **Nothing was downloaded.** Folder IDs are recorded so files can be located later.

## 1. Security issue (act on this first)
The folder is shared by public link and contains **`.ssh/`** and **`.kaggle/`** directories, plus `.bash_history`.
- These normally hold SSH private keys, a Kaggle API token (`kaggle.json`) and command history that may contain secrets.
- I did not open them.
- **Recommended:** remove these items from the shared folder, or restrict the link. Rotate the SSH keys and the Kaggle API token, because anyone with the link may already have them.
- Personal tool folders (`.anaconda`, `.jupyter`, `.nv`, `.triton`, `snap`) do not belong in a research share either.

## 2. What the backup contains (`aafv/artifacts/`, folder id `[redacted]`)
| Folder or file | What it is | What it would unlock |
|---|---|---|
| `p5/pair_vectors_{calibration,test,train_fit,train_val}.csv` (122.7 / 120.4 / 42.9 / 7.7 MB) | Per-pair feature vectors: direct and SAM similarity scores, gap, quality, R_sam, availability flags | Matched-FPR ArcFace-vs-fusion curves on calibration; direct-only vs SAM-only per pair and per bin; re-scoring with the frozen models; risk–coverage |
| `p5/faces.csv` (35.3 MB) | Per face (original or SAM): estimated age, quality, ArcFace similarity to the original | SAM failure by target age (E12); whether R_sam components track identity (still ArcFace-based, so circular) |
| `p5/raw_*.npz`, `standardizers.json` | Raw scores and z-score parameters | Exact re-scoring |
| `p5_fg/`, `pairs_fg/`, `gen_fg/` | The same for FG-NET, including SAM outputs | Matched-FPR FG-NET comparison, which the logs could not support |
| `models/` | Probably `fusion_seed*.pt` and the calibrator (not opened) | Look-1 model inspection |
| `gen/`, `p1/`, `p1_recrops/` | SAM outputs and aligned crops (licensed face images) | Identity-preservation checks with an independent recognizer (E0-style) on MORPH/FG-NET; visual audits (E1) |
| `pairs/`, `q/`, `audit/`, `ablations/`, `baselines/` | Pair lists, Q-stage outputs, audit files | Fold/pair reconstruction; label-correction history |
| `*.log` (`q_calib.log`, `q_train.log`, `step*.log`, `ablations_run.log`) | Run logs | Provenance (Phase 9 gaps) |
| `../morph_person_split_v5.csv`, `../person_merge_map_v5.csv` | MORPH filename → person mapping, and the merge map | **The MORPH identity-linkage audit (E1)**: shows how record IDs were merged into persons |
| `third_party/`, `shape_predictor_68_face_landmarks.dat.bz2` | Generator code and the dlib model | Re-running the pipeline |

## 3. Resolved: the calibration set was changed after its scores were seen
**Evidence** (`artifacts/q_calib.log`, the draft run before `--freeze`; and the local `Code/AAFV_Net/audit/quarantine_*.csv`):
1. In the draft calibration, the highest-scoring "different-person" pairs were D_hard pairs between persons `314177`↔`321217` (P = 0.9958, gap 0) and `290132`↔`303269` (P = 0.9614).
2. At ρ = 0.20 this gave **T_accept = 1.0129 with 0% genuine acceptance**. The draft chose ρ = 0.50 (T_accept = 0.7976, 71.75% accept).
3. The log ends: *"DRAFT only. Review the two sheets; list any wrong labels … then run again with --freeze."*
4. The frozen Look-1 thresholds are **ρ = 0.20, T_accept = 0.9566** (79.74% test accept).
5. Of the 858 quarantined persons, 854 are explained by the duplicate-ID rule (`quarantine_pairs.csv`). **Exactly 4 are not: 290132, 303269, 314177, 321217.** All four are in the calibration split, and they are exactly the two top-scoring impostor pairs above. They were therefore added by hand (`p_quarantine.py --extra_people`, "quarantined after visual audit (D30)") after the score-sorted contact sheet had been viewed.

**What it means:**
- **The reported operating point exists only because of this step.** Without it, the guarded system at ρ = 0.20 accepts nothing on calibration.
- **If the two pairs really are one person each** (duplicate records under different ids, which happens in MORPH), the correction is legitimate, but it was made *after seeing scores and only for the top-scoring pairs*. It must be disclosed as such.
- **If they are look-alikes**, the deployed threshold (0.9566) would auto-accept impostors scoring about 0.96–0.996. The calibration-side "zero false accepts" would then have been achieved by removing the false accepts.
- **For the 0.349% certificate:** Proposition 1 needs T ≥ the maximum D_random score, and that still holds. But persons were excluded from the calibration population *because of their scores*, and the rest of the threshold procedure was developed on the same split. The certificate must therefore be reported as conditional on this exclusion, or dropped. The decision is already made in the redesign: the certificate is no longer a headline (Phases 4 and 8).
- **Still open:** whether the four persons are duplicates. That needs a look at their crops (`artifacts/p1/`, located through `morph_person_split_v5.csv`), blind to the scores where possible.

## 4. Downloads that would help (need your explicit approval; none done)
| File | Size | Purpose |
|---|---|---|
| `artifacts/p5/pair_vectors_calibration.csv` | 122.7 MB | Matched-FPR ArcFace vs fusion and direct vs SAM per pair and bin, on calibration (allowed: not the test split) |
| `artifacts/p5/faces.csv` | 35.3 MB | SAM failure by target age; R_sam components vs ArcFace identity similarity |
| `artifacts/p5_fg/` pair vectors | Size to check | Matched-FPR FG-NET comparison (external set) |
| `morph_person_split_v5.csv`, `person_merge_map_v5.csv` | 6.4 MB, 382 KB | MORPH linkage audit (E1); finding the four quarantined persons' images |

These contain derived data from licensed datasets (scores and identifiers, not images). If downloaded, they would go to a git-ignored folder. `pair_vectors_test.csv` would be read only descriptively, since the test split is spent.
