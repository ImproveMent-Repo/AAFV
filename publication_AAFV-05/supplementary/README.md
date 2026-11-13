# Supplementary material for AAFV-05

| Item | Location |
|---|---|
| Pre-registration of the open experiment (Section V of the paper) | `PREREGISTRATION_Experiment0.md` (copy of `CVPR_redesign/exp0/PREREGISTRATION.md`) |
| Tested code for that experiment (6 steps, 8 passing tests including simulated GO and NO-GO runs) | `CVPR_redesign/exp0/` |
| Log-based analyses (per-bin ranking, decision vs ranking, post-hoc test readings) | `CVPR_redesign/log_analyses/run_log_analyses.py` and `out/` |
| Probe of the frozen fusion networks | `CVPR_redesign/architecture_review/probe_fusion.py` and `out/` |
| Per-pair re-analysis of the calibration split (reconstruction, counterfactual, matched FMR, label integrity, SAM drift) | `CVPR_redesign/drive_analyses/run_drive_analyses.py` and `out/` |
| Artifact hash verification (71/73 checks pass; the two failures are reported in the paper) | `CVPR_redesign/phase9_reproducibility/verify_artifacts.py` and `verification_report.txt` |
| Full re-analysis notes | `CVPR_redesign/log_analyses/LOG_FINDINGS.md`, `CVPR_redesign/drive_analyses/DRIVE_ANALYSES.md`, `CVPR_redesign/DRIVE_FINDINGS.md` |

To be assembled into a single supplementary PDF before submission, after the authors' revision.
