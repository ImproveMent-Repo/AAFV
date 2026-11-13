"""Check that numbers written in the prose of main.tex match their source files (tables are generated, so only prose is checked).
Each claim: (text that must appear in main.tex, value as printed, recomputed value, tolerance, source). Exit code 1 on any failure.
Usage: python scripts/check_claims.py   (from publication_AAFV-05/)"""
import sys
from pathlib import Path

import pandas as pd

PUB = Path(__file__).resolve().parent.parent
R = PUB.parent / "CVPR_redesign"
A = PUB.parent / "Code" / "AAFV_Net"
tex = (PUB / "main.tex").read_text(encoding="utf-8")

la2 = pd.read_csv(R / "log_analyses/out/la2_pool_ranking_calibration.csv").set_index("variant")
da2 = pd.read_csv(R / "drive_analyses/out/da2_threshold_counterfactual.csv")
da3 = pd.read_csv(R / "drive_analyses/out/da3_matched_fmr_calibration.csv")
da4 = pd.read_csv(R / "drive_analyses/out/da4_label_linkage.csv").set_index("bin")
sex = pd.read_csv(R / "drive_analyses/out/da4b_sex_mismatch.csv").set_index("gap_bin")
la4 = pd.read_csv(R / "log_analyses/out/la4_impostor_like_genuine.csv").set_index("bin")
d5 = pd.read_csv(R / "drive_analyses/out/da5_sam_identity_by_shift.csv")
fp = pd.read_csv(R / "architecture_review/out/fusion_probe.csv").set_index("variant")
ext = pd.read_csv(A / "ablations/extended_test.csv")
fg = pd.read_csv(A / "ablations/extended_calibration_fg16.csv")


def m3(pool, b, score, col):
    return float(da3[(da3.pool == pool) & (da3.bin == b) & da3.score.str.startswith(score)][col].iloc[0])


def ext_acc(v):
    return 100 * float(ext[(ext.variant == v) & (ext.beta.round(3) == 0.01)].same_acc.iloc[0])


claims = [
    ("338,871 MORPH calibration pairs", 338871, int(da2.iloc[0].n), 0, "da2"),
    ("70.07\\% versus 89.45\\%", 70.07, ext_acc("full"), 0.005, "extended_test.csv"),
    ("70.07\\% versus 89.45\\%", 89.45, ext_acc("arcface_only"), 0.005, "extended_test.csv"),
    ("auto-accepts 73.3\\% of genuine pairs", 73.3, 100 * la2.loc["full", "same_accept_all"], 0.05, "la2"),
    ("guarded ArcFace 87.7\\%", 87.7, 100 * la2.loc["arcface_only", "same_accept_all"], 0.05, "la2"),
    ("0.977 and 0.980", 0.977, la2.loc["full", "TPR@FPR1e-3_D_all_random"], 0.0005, "la2"),
    ("0.977 and 0.980", 0.980, la2.loc["arcface_only", "TPR@FPR1e-3_D_all_random"], 0.0005, "la2"),
    ("($\\Delta$TAR $=-0.076$)", -0.076, m3("D_all_random", "G1", "SAM", "d_tar_vs_arcface"), 0.0005, "da3"),
    ("5--9 years ($-0.072$)", -0.072, m3("D_all_random", "G2", "SAM", "d_tar_vs_arcface"), 0.0005, "da3"),
    ("($+0.043$, 95\\% CI $[0.000, 0.106]$)", 0.043, m3("D_all_random", "G2", "SAM", "d_auc_vs_arcface"), 0.0005, "da3"),
    ("($+0.043$, 95\\% CI $[0.000, 0.106]$)", 0.106, m3("D_all_random", "G2", "SAM", "d_auc_ci_hi"), 0.0005, "da3"),
    ("($-0.026$, $[-0.065, +0.003]$)", -0.026, m3("D_all_random", "G2", "LogReg", "d_auc_vs_arcface"), 0.0005, "da3"),
    ("($-0.002$, $[-0.004,-0.001]$)", -0.002, m3("D_all_random", "G1", "AAFV", "d_tar_vs_arcface"), 0.0005, "da3"),
    ("fused score gains $+0.003$", 0.003, m3("D_hard", "G1", "AAFV", "d_tar_vs_arcface"), 0.0005, "da3"),
    ("(TAR 0.391 versus 0.985)", 0.391, m3("D_hard", "G1", "SAM", "tar"), 0.0005, "da3"),
    ("(TAR 0.391 versus 0.985)", 0.985, m3("D_hard", "G1", "ArcFace", "tar"), 0.0005, "da3"),
    ("TPR 0.971 versus 0.973", 0.971, la2.loc["direct_only_mlp", "TPR@FPR1e-3_D_hard"], 0.0005, "la2"),
    ("TPR 0.971 versus 0.973", 0.973, la2.loc["full", "TPR@FPR1e-3_D_hard"], 0.0005, "la2"),
    ("about six times more", 6, fp.loc["full", "swing_Wd"] / fp.loc["full", "swing_Ws"], 0.5, "fusion_probe.csv"),
    ("in 18--29\\% at 15 years", 18, 100 * sex.loc[["G4", "G5", "G6"], "sex_mismatch"].min(), 0.5, "da4b"),
    ("in 18--29\\% at 15 years", 29, 100 * sex.loc[["G4", "G5", "G6"], "sex_mismatch"].max(), 0.5, "da4b"),
    ("86--98\\% score like random impostors", 86, 100 * da4.loc[["G4", "G5", "G6"], "arcface_impostor_like"].min(), 0.5, "da4"),
    ("86--98\\% score like random impostors", 98, 100 * da4.loc[["G4", "G5", "G6"], "arcface_impostor_like"].max(), 0.5, "da4"),
    ("(58--80\\% versus 5--8\\%)", 58, 100 * da4.loc[["G2", "G3"], "impostor_like_if_ids_differ"].min(), 0.5, "da4"),
    ("(58--80\\% versus 5--8\\%)", 80, 100 * da4.loc[["G2", "G3"], "impostor_like_if_ids_differ"].max(), 0.5, "da4"),
    ("(97\\% at 15--19 years for both)", 97, 100 * la4.loc["G4", "vit_impostor_like"], 0.5, "la4"),
    ("(97\\% at 15--19 years for both)", 97, 100 * la4.loc["G4", "aafv_impostor_like"], 0.5, "la4"),
    ("median of 0.51 for shifts", 0.51, d5[(d5.direction == "older") & (d5.abs_shift_bin == "0-4")].id_cos_median.iloc[0], 0.005, "da5"),
    ("to 0.35 for aging by 30 years", 0.35, d5[(d5.direction == "older") & (d5.abs_shift_bin == "30+")].id_cos_median.iloc[0], 0.005, "da5"),
    ("when 23\\% of outputs", 23, 100 * d5[(d5.direction == "older") & (d5.abs_shift_bin == "30+")].share_below_0p3.iloc[0], 0.5, "da5"),
    ("auto-accepted 51.92\\% of genuine pairs against 40.38\\%", 51.92,
     100 * float(fg[(fg.split == "fgnet") & (fg.variant == "full") & (fg.beta.round(3) == 0.01)].same_acc.iloc[0]), 0.005, "fg16"),
    ("falsely rejected 18.20\\%", 18.20, 100 * float(fg[(fg.split == "fgnet") & (fg.variant == "full") & (fg.beta.round(3) == 0.01)].same_rej.iloc[0]), 0.005, "fg16"),
    ("(16 genuine, 4 person-disjoint random, 112 mined, 800 repeated random)", 932, 16 + 4 + 112 + 800, 0, "DRIVE_ANALYSES DA2"),
]

fails = 0
for text, printed, actual, tol, src in claims:
    present = text in tex
    ok = present and abs(float(printed) - float(actual)) <= tol
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {text[:60]:60s} printed={printed} recomputed={actual:.4f} [{src}]" + ("" if present else "  (text not found)"))
print(f"\n{len(claims) - fails}/{len(claims)} prose claims verified")
sys.exit(1 if fails else 0)
