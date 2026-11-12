"""Post-hoc DESCRIPTIVE analyses of already-logged outputs. Changes no model, threshold or guard.
Inputs : Code/AAFV_Net/q/report/test_pair_zones_look1.csv  (Look-1 per-pair P, zone, set, gap_bin, gender)
         Code/AAFV_Net/ablations/extended_test.csv, extended_calibration*.csv (aggregated Look-2 / calibration / FG-NET rates)
Outputs: AAFV-04_revision/analysis/out/*.csv, *.txt
NOTE: Look-1 test outputs were already revealed in 2026-11; re-reading them is NOT a new test look, but every number produced
here is post hoc and must be reported as descriptive, non-confirmatory evidence. No quantity here is used to choose anything."""
import numpy as np, pandas as pd, math, json, os
R = os.path.dirname(os.path.abspath(__file__)); P0 = os.path.join(R, "..", "..", "Code", "AAFV_Net")
OUT = os.path.join(R, "out"); os.makedirs(OUT, exist_ok=True)
L = pd.read_csv(os.path.join(P0, "q/report/test_pair_zones_look1.csv"))
rep = open(os.path.join(OUT, "a1_report.txt"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s); rep.write(s + "\n")

# ---------- 0. sanity: reproduce Look-1 report
say("== 0. Look-1 reproduction (must equal test_report_look1.json)")
say(L.groupby(["set", "zone"]).size().unstack(fill_value=0).to_string())
say("genuine pairs by gap bin:", L[L.label == 1].gap_bin.value_counts().sort_index().to_dict())

# ---------- 1. calibration metrics
EPS = 1e-12
def logit(p): p = np.clip(p, 1e-7, 1 - 1e-7); return np.log(p / (1 - p))
def slope_intercept(p, y, it=50):
    x = logit(p); X = np.c_[np.ones_like(x), x]; b = np.zeros(2)
    for _ in range(it):
        m = 1 / (1 + np.exp(-X @ b)); W = m * (1 - m) + 1e-12
        H = X.T @ (X * W[:, None]) + 1e-9 * np.eye(2); g = X.T @ (y - m); b = b + np.linalg.solve(H, g)
    return b  # intercept, slope (perfect: 0, 1)
def calib(p, y, nb=15):
    p = np.asarray(p, float); y = np.asarray(y, float)
    brier = float(np.mean((p - y) ** 2)); pc = np.clip(p, 1e-7, 1 - 1e-7)
    nll = float(-np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc)))
    edges = np.linspace(0, 1, nb + 1); idx = np.clip(np.digitize(p, edges) - 1, 0, nb - 1); ece = 0.0; mce = 0.0; rows = []
    for b in range(nb):
        m = idx == b
        if m.sum() == 0: continue
        gap = abs(p[m].mean() - y[m].mean()); ece += m.mean() * gap; mce = max(mce, gap)
        rows.append(dict(bin_lo=edges[b], bin_hi=edges[b + 1], n=int(m.sum()), mean_p=p[m].mean(), frac_pos=y[m].mean()))
    a, s = slope_intercept(p, y) if 0 < y.mean() < 1 else (np.nan, np.nan)
    return dict(n=len(p), prev=float(y.mean()), ECE15=ece, MCE15=mce, Brier=brier, NLL=nll, cal_intercept=a, cal_slope=s), pd.DataFrame(rows)
say("\n== 1. Calibration of Look-1 posterior P on MORPH test (post hoc). P is a Platt posterior fitted on train_val;")
say("   its absolute calibration depends on the class prior of each evaluation pool, so pools are reported separately.")
pools = {"all_logged_pairs": L,
         "genuine+D_random": L[L.set.isin(["same", "D_random"])],
         "genuine+D_all_random": L[L.set.isin(["same", "D_all_random"])],
         "genuine+D_hard": L[L.set.isin(["same", "D_hard"])]}
rows = []
for k, d in pools.items():
    m, rel = calib(d.P.to_numpy(), d.label.to_numpy()); m["pool"] = k; rows.append(m); rel.to_csv(os.path.join(OUT, f"a1_reliability_{k}.csv"), index=False)
for g in ["M", "F"]:
    d = L[L.set.isin(["same", "D_all_random"]) & (L.gender == g)]; m, _ = calib(d.P.to_numpy(), d.label.to_numpy()); m["pool"] = f"genuine+D_all_random|sex={g}"; rows.append(m)
cm = pd.DataFrame(rows)[["pool", "n", "prev", "ECE15", "MCE15", "Brier", "NLL", "cal_intercept", "cal_slope"]]
cm.to_csv(os.path.join(OUT, "a1_calibration_metrics.csv"), index=False); say(cm.round(5).to_string(index=False))
say("Class-conditional view (prior-free): mean P on genuine and on each impostor pool")
say(L.groupby("set").P.describe(percentiles=[.01, .05, .5, .95, .99]).round(5).to_string())

# ---------- 2. Where do impostor pools sit relative to the later Look-2 reject threshold?
say("\n== 2. Share of each pool with Look-1 P below T values (descriptive; T_rej(0.01)=0.007541 is the Look-2 calibration threshold)")
for t in [0.0040942, 0.007541, 0.0168158]:
    say(f"  P < {t:.6f}:", {s: round(float((d.P < t).mean()), 4) for s, d in L.groupby("set")})

# ---------- 3. Risk-coverage curve of the Look-1 scorer (accept side), descriptive
say("\n== 3. Accept-side risk-coverage (Look-1 P only; guards are NOT re-applied because guard inputs were not logged per pair)")
same = L[L.label == 1].P.to_numpy(); hard = L[L.set == "D_hard"].P.to_numpy(); rnd = L[L.set == "D_random"].P.to_numpy(); allr = L[L.set == "D_all_random"].P.to_numpy()
ts = np.unique(np.r_[np.quantile(same, np.linspace(0, 1, 201)), 0.9565746784210205])
rc = pd.DataFrame(dict(thr=ts, genuine_cov=[(same >= t).mean() for t in ts], FA_hard=[int((hard >= t).sum()) for t in ts],
                       FA_random=[int((rnd >= t).sum()) for t in ts], FA_all_random=[int((allr >= t).sum()) for t in ts]))
rc.to_csv(os.path.join(OUT, "a1_risk_coverage_look1.csv"), index=False)
say(rc[rc.index % 20 == 0].round(5).to_string(index=False)); say(rc[(rc.thr - 0.9565746784210205).abs() < 1e-9].round(5).to_string(index=False))
say("Note: at T=0.95657 without guards, genuine coverage =", round(float((same >= 0.9565746784210205).mean()), 4),
    "vs logged guarded accept 0.7974 -> guards account for the difference.")

# ---------- 4. Hard false accepts of Look 1
say("\n== 4. Look-1 hard-impostor false accepts (only metadata logged per pair: gap bin, sex, P)")
say(L[(L.set == "D_hard") & (L.zone == "accept")].to_string(index=False))

# ---------- 5. Sex x gap genuine acceptance (pair-level Wilson CI; identity clustering not available in this log)
def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return (c - h, c + h)
say("\n== 5. Genuine auto-accept by sex x gap bin (Look 1). Wilson CIs are pair-level and UNDERSTATE uncertainty (pairs share people).")
rows = []
for (g, b), d in L[L.label == 1].groupby(["gender", "gap_bin"]):
    k = int((d.zone == "accept").sum()); n = len(d); lo, hi = wilson(k, n); rows.append(dict(sex=g, gap_bin=b, n=n, accept=k / n, lo=lo, hi=hi))
sg = pd.DataFrame(rows); sg.to_csv(os.path.join(OUT, "a1_sex_by_gap.csv"), index=False); say(sg.round(4).to_string(index=False))

# ---------- 6. Zero-failure sample-size requirements and dependence sensitivity
def cp_upper(k, n, a):
    """Exact one-sided Clopper-Pearson upper bound: largest p with P(X<=k | n,p) >= a (bisection, log-space binomial cdf)."""
    def cdf(p):
        if p <= 0: return 1.0
        if p >= 1: return 0.0 if k < n else 1.0
        lp, lq = math.log(p), math.log1p(-p); s = 0.0
        for i in range(k + 1): s += math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
        return s
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) >= a: lo = mid
        else: hi = mid
    return lo
say("\n== 6a. FAR upper bounds for the observed D_random result (0/1149)")
for a in (0.05, 0.025):
    say(f"  alpha={a}: CP upper = {cp_upper(0, 1149, a):.6f}  (closed form 1-a^(1/N) = {1 - a ** (1 / 1149):.6f})")
say("== 6b. Independent impostor comparisons needed to certify FAR <= target with k observed false accepts (one-sided, exact CP)")
rows = []
for tgt in (1e-3, 1e-4, 1e-5):
    for a in (0.05, 0.025):
        for k in (0, 1, 2):
            n0 = int(math.ceil((-math.log(a)) / tgt * 0.5)); n = max(n0, k + 1)
            # monotone search
            step = max(1, n // 50)
            while cp_upper(k, n, a) > tgt: n += step
            while n > k + 1 and cp_upper(k, n - 1, a) <= tgt: n -= 1
            rows.append(dict(target_FAR=tgt, alpha=a, k=k, N_required=n, persons_if_disjoint=2 * n))
ss = pd.DataFrame(rows); ss.to_csv(os.path.join(OUT, "a1_sample_size.csv"), index=False); say(ss.to_string(index=False))
say("== 6c. Dependence sensitivity: bound if the 1,149 pairs carry only N/DEFF effective independent trials (alpha=0.025)")
dd = pd.DataFrame([dict(design_effect=de, N_eff=1149 / de, FAR_upper=1 - 0.025 ** (de / 1149)) for de in (1, 1.25, 1.5, 2, 3, 5)])
dd.to_csv(os.path.join(OUT, "a1_design_effect.csv"), index=False); say(dd.round(6).to_string(index=False))

# ---------- 7. Operational workload under impostor mixtures (arithmetic on verified aggregate rates, Look 2, beta=0.01)
say("\n== 7. Expected outcome shares per 10,000 transactions (Look-2 aggregate rates, beta=0.01).")
E = pd.read_csv(os.path.join(P0, "ablations/extended_test.csv")); E = E[E.beta == 0.01].set_index("variant")
rows = []
for v in ("full", "arcface_only", "agg_no_shared_targets"):
    r = E.loc[v]
    for pi in (0.001, 0.01, 0.05):            # share of impostor transactions
        for h in (0.0, 0.1, 1.0):              # share of impostors that are ArcFace-mined look-alikes
            rej_imp = (1 - h) * r.D_all_random_rej + h * r.D_hard_rej
            rev = (1 - pi) * r.same_rev + pi * (1 - rej_imp)
            rows.append(dict(variant=v, impostor_share=pi, lookalike_share=h, review_per_10k=10000 * rev,
                             genuine_auto_accept_per_10k=10000 * (1 - pi) * r.same_acc, genuine_false_reject_per_10k=10000 * (1 - pi) * r.same_rej))
wl = pd.DataFrame(rows); wl.to_csv(os.path.join(OUT, "a1_workload.csv"), index=False); say(wl.round({'review_per_10k':1,'genuine_auto_accept_per_10k':1,'genuine_false_reject_per_10k':1}).to_string(index=False))

# ---------- 8. FG-NET false-reject transfer (aggregate, verified CSV)
say("\n== 8. Does the beta false-reject budget transfer? Genuine auto-reject (false-reject) rate, beta=0.01 set on MORPH calibration")
for f, name in (("extended_calibration_fg16.csv", "FG-NET adults"), ("extended_calibration_fg.csv", "FG-NET all ages")):
    F = pd.read_csv(os.path.join(P0, "ablations", f)); F = F[(F.beta == 0.01) & (F.split == "fgnet")]
    say(name); say(F[["variant", "same_acc", "same_rev", "same_rej", "FG_random_FA", "FG_random_rej", "FG_random_rev"]].round(4).to_string(index=False))
rep.close()
