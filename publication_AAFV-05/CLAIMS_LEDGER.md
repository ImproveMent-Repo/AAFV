# Claims ledger: AAFV-05

Every quantitative statement in `main.tex` is listed with the file that produces it and the script that made that file.
**Paths:**
- `R/` = `CVPR_redesign/`
- `A/` = `Code/AAFV_Net/` (logged AAFV artifacts, hash-verified in `R/phase9_reproducibility/`)
- `D/` = `R/drive_data/` (downloaded calibration vectors; git-ignored)

**Labels:**
- **[V]** recomputed and checked on 2026-11-13/14;
- **[R]** reported in AAFV-04 and re-derived from its logs (Phase 9: 42/43 match);
- **[L]** from a run log viewed on the Drive (not downloaded).

| # | Claim (section) | Value | Source file | Produced by | Label |
|---|---|---|---|---|---|
| 1 | Reconstruction of T_acc / T_rej / accept (IV-A, Tab. I) | 0.956438 / 0.007541 / 73.26% | `R/drive_analyses/out/da2_threshold_counterfactual.csv` | `run_drive_analyses.py` (DA1) on `D/pair_vectors_calibration.csv` + `A/ablations/variants/full/frozen.pkl` | [V] |
| 2 | Calibration split composition (III-B) | 338,871 / 23,838 / 1,170 / 278,094 / 35,769 | `A/ablations/extended_calibration.csv`; recount in DA1 | `verify_artifacts.py`; DA1 | [V] |
| 3 | Pre-quarantine vectors; 858 persons removed (III-C) | 363,647 → 338,871 | `D/pair_vectors_calibration.csv`, `A/audit/quarantine_people.csv` | DA1 | [V] |
| 4 | 379,930 SAM + 51,003 original faces (III-C, IV-G) | – | `D/faces.csv` | DA5 | [V] |
| 5 | Look-2 checkpoint = 3 networks, not 5 (III-C) | 3 | `A/ablations/variants/full/frozen.pkl` | `R/phase9_reproducibility/verify_artifacts.py` | [V] |
| 6 | ArcFace fed resized FFHQ crops (III-C) | – | `A/scripts/p5_faces.py` (code reading) | – | [V] |
| 7 | Test acceptance 70.07% vs 89.45% (Abstract, I) | – | `A/ablations/extended_test.csv` | AAFV pipeline; checked by `verify_artifacts.py` | [R] |
| 8 | Calibration accept 73.3% vs 87.7%; TAR 0.977 vs 0.980 (IV-B, Tab. II) | – | `R/log_analyses/out/la2_pool_ranking_calibration.csv` (from `A/ablations/ablation_calibration.csv`) | `run_log_analyses.py` | [V] |
| 9 | Per-bin ranking (Fig. 1) | – | `R/log_analyses/out/la1_gap_ranking_calibration.csv` (from `A/ablations/results/gap_report_calibration.csv`) | `run_log_analyses.py` | [V] |
| 10 | Matched-FMR per pair, all Δ and CIs (IV-C, Tab. III, Fig. 2) | e.g. −0.076, −0.072, 0.000, −0.002, +0.003 | `R/drive_analyses/out/da3_matched_fmr_calibration.csv` | DA3 (300 paired person-cluster bootstrap replicates) | [V] |
| 11 | Generated-pair AUC +0.043 [0.000, 0.106]; combination −0.026 [−0.065, +0.003] (IV-C) | – | same as 10 | DA3 | [V] |
| 12 | Direct-only TPR 0.971 vs full 0.973 on mined look-alikes (IV-C) | – | `la2_pool_ranking_calibration.csv` | `run_log_analyses.py` | [V] |
| 13 | Linear-head weights; swings 25.1 vs 4.1; controls (IV-D, Tab. IV) | – | `R/architecture_review/out/fusion_probe.csv`, `linear_heads.csv` | `probe_fusion.py` | [V] |
| 14 | Draft calibration T_acc = 1.0129 at ρ = 0.20; top impostors P 0.996 / 0.961; "5 models" (IV-E) | – | `artifacts/q_calib.log` on the Drive backup | Viewed in browser 2026-11-14 | [L] |
| 15 | 854 of 858 quarantined by rule; 4 by hand (IV-E) | – | `A/audit/quarantine_people.csv`, `quarantine_pairs.csv` | `R/DRIVE_FINDINGS.md` §3 | [V] |
| 16 | Restoring 932 pairs → 0% accept at every ρ (IV-E, Tab. I) | – | `da2_threshold_counterfactual.csv` | DA2 | [V] |
| 17 | Zero-failure bounds 0.256 / 0.349 / 0.260 / 0.321% (IV-E, Tab. V) | – | arithmetic | `build_assets.py`; `verify_artifacts.py` | [V] |
| 18 | Sex mismatch 0.0% → 18–29% (Abstract, IV-F, Tab. VI) | – | `R/drive_analyses/out/da4b_sex_mismatch.csv` | DA4b | [V] |
| 19 | Impostor-like 86–98% at 15+ y; 58–80% vs 5–8% by file ids (IV-F) | – | `da4_label_linkage.csv` | DA4 | [V] |
| 20 | Test split: fused and ViT both 97% impostor-like at 15–19 y (IV-F) | – | `R/log_analyses/out/la4_impostor_like_genuine.csv` | `run_log_analyses.py` (post hoc) | [V] |
| 21 | SAM similarity 0.51 → 0.35; 23% < 0.30; age error 2 → 5 y (IV-G, Tab. VII, Fig. 3) | – | `da5_sam_identity_by_shift.csv` | DA5 | [V] |
| 22 | FG-NET adults 51.92% vs 40.38%; false reject 18.20% (IV-H) | – | `A/ablations/extended_calibration_fg16.csv` | AAFV pipeline; checked by `check_claims.py` | [R] |
| 23 | FG-NET all-ages false accepts: 4, children aged 0–4, P 0.966–1.000 (IV-H) | – | `Result_Images/audit_fg_fa.png`; AAFV-04 Table XI | Image audit | [R] |
| 24 | AgeDB-30 above 98% for strong models (II) | 98.37–98.57% | Dahan & Keller 2023 (read 2026-11-13) | Phase 5 | [V] |

**Automated check:** `python scripts/check_claims.py` confirms 33 prose numbers against these files (33/33 on 2026-11-14). The tables are generated directly from the files, so they cannot drift from them.
