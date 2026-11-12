"""Lists every decimal number in the revised manuscript that does NOT match a value derivable from the logged artifacts
(rounded to 2 or 3 decimals, as fraction or percent). Unmatched numbers are then reviewed by hand."""
import re, glob, os, json, pandas as pd, numpy as np
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(R, "..", "..", "Code", "AAFV_Net"); M = os.path.join(R, "..", "manuscript")
vals = set()
def add(x):
    try: x = float(x)
    except: return
    if not np.isfinite(x): return
    for v in (x, 100 * x):
        for d in (0, 1, 2, 3, 4):
            vals.add(round(v, d))
for f in glob.glob(os.path.join(C, "ablations", "*.csv")) + glob.glob(os.path.join(C, "ablations", "results_subset", "*.csv")) + glob.glob(os.path.join(R, "out", "*.csv")) + glob.glob(os.path.join(C, "audit", "*.csv")):
    d = pd.read_csv(f)
    for c in d.columns:
        if d[c].dtype.kind in "fi": [add(v) for v in d[c].to_numpy()]
for f in (os.path.join(C, "q/thresholds/thresholds.json"), os.path.join(C, "q/report/test_report_look1.json")):
    def walk(o):
        if isinstance(o, dict): [walk(v) for v in o.values()]
        elif isinstance(o, list): [walk(v) for v in o]
        else: add(o)
    walk(json.load(open(f)))
txt = open(os.path.join(M, "main.tex")).read() + "".join(open(f).read() for f in glob.glob(os.path.join(M, "tables", "*.tex")))
txt = re.sub(r"(?m)^%.*$", "", txt)
nums = sorted(set(re.findall(r"(?<![\w.])\d[\d,]*\.\d+", txt)))
un = [n for n in nums if round(float(n.replace(",", "")), 4) not in vals and round(float(n.replace(",", "")), 2) not in vals]
print(len(nums), "decimal numbers;", len(un), "not directly matched:"); print(" ".join(un))
