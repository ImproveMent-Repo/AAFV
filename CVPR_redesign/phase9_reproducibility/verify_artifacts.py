"""Phase 9 verification. Reads only; changes nothing.
(1) Frozen-artifact hashes against the freeze ledgers.
(2) AAFV-04's stated numbers re-derived from the logged files.
(3) Seed counts in the frozen models.
Writes verification_report.csv and verification_report.txt next to this script.
Usage: python verify_artifacts.py"""
import hashlib
import json
import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
A = HERE.parent.parent / "Code" / "AAFV_Net"
rows = []


def check(group, item, stated, computed, tol=0.0, source=""):
    if isinstance(stated, (str, bool)) or isinstance(computed, (str, bool)):
        ok = str(stated) == str(computed)
    else:
        ok = abs(float(stated) - float(computed)) <= tol
    rows.append(dict(group=group, item=item, stated=stated, recomputed=computed, tolerance=tol,
                     result="PASS" if ok else "FAIL", source=source))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- 1. hashes
ledger = json.load(open(A / "ablations/ablation_freeze.json"))
for v, h in ledger.items():
    p = A / "ablations/variants" / v / "frozen.pkl"
    check("hash", f"frozen.pkl {v}", h, sha(p) if p.exists() else "missing", source="ablations/ablation_freeze.json")
tj = A / "q/thresholds/thresholds.json"
lf = hashlib.sha256(tj.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
check("hash", "thresholds.json (LF-normalised) vs thresholds.sha256",
      (A / "q/thresholds/thresholds.sha256").read_text().split()[0], lf, source="q/thresholds/thresholds.sha256")
log = (A / "q/logs/test_access.log").read_text()
check("hash", "Look-1 thresholds hash recorded in test_access.log", True, lf in log, source="q/logs/test_access.log")
check("hash", "number of logged test looks", 2, sum(1 for l in log.splitlines() if "look=" in l), source="q/logs/test_access.log")

# ---------------------------------------------------------------- 2. numbers
z = pd.read_csv(A / "q/report/test_pair_zones_look1.csv")
g = z[z.set == "same"]
src = "q/report/test_pair_zones_look1.csv"
check("Look 1 test", "genuine test pairs", 24305, len(g), source=src)
check("Look 1 test", "genuine auto-accept %", 79.74, round(100 * (g.zone == "accept").mean(), 2), 0.005, src)
check("Look 1 test", "D_random n/FA", "1149/0", f"{(z.set == 'D_random').sum()}/{((z.set == 'D_random') & (z.zone == 'accept')).sum()}", source=src)
check("Look 1 test", "D_hard FA", 3, int(((z.set == "D_hard") & (z.zone == "accept")).sum()), source=src)
check("Look 1 test", "male genuine accept %", 81.07, round(100 * (g[g.gender == "M"].zone == "accept").mean(), 2), 0.005, src)
check("Look 1 test", "female genuine accept %", 71.93, round(100 * (g[g.gender == "F"].zone == "accept").mean(), 2), 0.005, src)
check("Look 1 test", "male/female genuine n", "20774/3531", f"{(g.gender == 'M').sum()}/{(g.gender == 'F').sum()}", source=src)
check("Look 1 test", "share of genuine in G1 %", 97.2, round(100 * (g.gap_bin == "G1").mean(), 1), 0.05, src)
check("Look 1 test", "genuine n in G2..G6", "266,184,75,137,12",
      ",".join(str((g.gap_bin == b).sum()) for b in ["G2", "G3", "G4", "G5", "G6"]), source=src)

e = pd.read_csv(A / "ablations/extended_test.csv")


def r(v, b=0.01):
    return e[(e.variant == v) & np.isclose(e.beta, b)].iloc[0]


src = "ablations/extended_test.csv"
f = r("full")
check("Look 2 test", "full: genuine auto-accept %", 70.07, round(100 * f.same_acc, 2), 0.005, src)
check("Look 2 test", "full: accept 95% CI", "[66.52, 73.11]", f"[{100 * f.same_acc_lo:.2f}, {100 * f.same_acc_hi:.2f}]", source=src)
check("Look 2 test", "full: genuine false reject %", 0.54, round(100 * f.same_rej, 2), 0.005, src)
check("Look 2 test", "full: D_hard FA/n", "5/35735", f"{int(f.D_hard_FA)}/{int(f.D_hard_n)}", source=src)
check("Look 2 test", "full: D_hard auto-reject %", 98.04, round(100 * f.D_hard_rej, 2), 0.005, src)
check("Look 2 test", "full: neutral auto-reject %", 57.49, round(100 * f.D_by_both_rej, 2), 0.005, src)
check("Look 2 test", "full: neutral n", 2790, int(f.D_by_both_n), source=src)
check("Look 2 test", "full: D_random auto-reject %", 34.03, round(100 * f.D_random_rej, 2), 0.005, src)
for v, s in [("arcface_only", 89.45), ("arcface_only_noguard", 93.58), ("direct5_logreg", 87.10),
             ("agg_no_shared_targets", 83.91), ("direct_only_mlp", 0.0)]:
    check("Look 2 test", f"{v}: genuine auto-accept %", s, round(100 * r(v).same_acc, 2), 0.005, src)
check("Look 2 test", "arcface_only: D_random auto-reject %", 63.53, round(100 * r("arcface_only").D_random_rej, 2), 0.005, src)
check("Look 2 test", "full: D_hard reject at beta 0.005/0.02", "96.33/98.75",
      f"{100 * r('full', 0.005).D_hard_rej:.2f}/{100 * r('full', 0.02).D_hard_rej:.2f}", source=src)

c = pd.read_csv(A / "ablations/extended_calibration.csv")
cf = c[(c.variant == "full") & np.isclose(c.beta, 0.01)].iloc[0]
src = "ablations/extended_calibration.csv"
check("calibration", "full: genuine auto-accept % (full split)", 73.26, round(100 * cf.same_acc, 2), 0.005, src)
check("calibration", "D_random n", 1170, int(cf.D_random_n), source=src)
check("calibration", "genuine pairs (full split)", 23838, int(sum(cf[f"n_same_G{i}"] for i in range(1, 7))), source=src)

dt = pd.read_csv(A / "ablations/decision_table_calibration.csv")


def d(v):
    return dt[(dt.variant == v) & np.isclose(dt.beta, 0.01)].iloc[0]


src = "ablations/decision_table_calibration.csv"
check("calibration subset", "full: accept %", 74.13, round(100 * d("full").same_acc, 2), 0.005, src)
check("calibration subset", "drop_eff: accept %", 81.27, round(100 * d("drop_eff").same_acc, 2), 0.005, src)
check("calibration subset", "no_branch_masking: accept %", 3.60, round(100 * d("no_branch_masking").same_acc, 2), 0.005, src)
check("calibration subset", "agg_no_shared_targets: accept %", 84.80, round(100 * d("agg_no_shared_targets").same_acc, 2), 0.005, src)
check("calibration subset", "drop_arc: accept %", 0.73, round(100 * d("drop_arc").same_acc, 2), 0.005, src)

fg = pd.read_csv(A / "ablations/extended_calibration_fg16.csv")


def q(v):
    return fg[(fg.split == "fgnet") & (fg.variant == v) & np.isclose(fg.beta, 0.01)].iloc[0]


src = "ablations/extended_calibration_fg16.csv"
check("FG-NET adults", "full: accept %", 51.92, round(100 * q("full").same_acc, 2), 0.005, src)
check("FG-NET adults", "full: accept 95% CI", "[44.47, 58.41]", f"[{100 * q('full').same_acc_lo:.2f}, {100 * q('full').same_acc_hi:.2f}]", source=src)
check("FG-NET adults", "full: false reject %", 18.20, round(100 * q("full").same_rej, 2), 0.005, src)
check("FG-NET adults", "full: impostor FA/n", "0/3670", f"{int(q('full').FG_random_FA)}/{int(q('full').FG_random_n)}", source=src)
check("FG-NET adults", "arcface_only: accept %", 40.38, round(100 * q("arcface_only").same_acc, 2), 0.005, src)

for n, dl, s in [(1170, 0.05, 0.256), (1170, 0.05 / 3, 0.349), (1149, 0.05, 0.260), (1149, 0.025, 0.320)]:
    check("statistics", f"1 - delta^(1/n) %, n={n}, delta={dl:.4f}", s, round(100 * (1 - dl ** (1 / n)), 3), 0.0006, "arithmetic")
check("statistics", "1/(n+1) %, n=1170", 0.085, round(100 / 1171, 3), 0.0006, "arithmetic")


# ---------------------------------------------------------------- 3. seeds (restricted unpickler)
class Dummy:
    def __init__(self, *a, **k):
        pass

    def __setstate__(self, s):
        self.__dict__.update(s if isinstance(s, dict) else {"state": s})


ALLOW = {("collections", "OrderedDict"), ("torch._utils", "_rebuild_tensor_v2"), ("torch.storage", "_load_from_bytes"),
         ("numpy._core.multiarray", "_reconstruct"), ("numpy", "ndarray"), ("numpy", "dtype"),
         ("numpy._core.multiarray", "scalar"), ("sklearn.linear_model._logistic", "LogisticRegression")}


class U(pickle.Unpickler):
    def find_class(self, m, n):
        if (m, n) in (("__main__", "Scorer"), ("p10_ablations", "Scorer"), ("aafv.calib", "Calibrator")):
            return Dummy
        if (m, n) in ALLOW:
            return super().find_class(m, n)
        raise pickle.UnpicklingError(f"blocked {m}.{n}")


fz = U(open(A / "ablations/variants/full/frozen.pkl", "rb")).load()
check("model", "seeds in Look-2 'full' ensemble (AAFV-04 says 5)", 5, len(fz["scorer"].p), source="ablations/variants/full/frozen.pkl")
check("model", "fusion models listed for Look 1", 5, len(json.load(open(tj))["model_sha256"]), source="q/thresholds/thresholds.json")

out = pd.DataFrame(rows)
out.to_csv(HERE / "verification_report.csv", index=False)
summary = out.groupby(["group", "result"]).size().unstack(fill_value=0)
fails = out[out.result == "FAIL"][["group", "item", "stated", "recomputed", "source"]]
txt = summary.to_string() + f"\n\nTOTAL: {int((out.result == 'PASS').sum())} PASS, {int((out.result == 'FAIL').sum())} FAIL\n\nFAILURES:\n" + fails.to_string(index=False)
(HERE / "verification_report.txt").write_text(txt, encoding="utf-8")
print(txt)
