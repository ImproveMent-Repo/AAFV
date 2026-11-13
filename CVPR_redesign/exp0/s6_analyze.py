"""Step 6: scores, cross-fitted fusion, per-bin metrics with person-cluster bootstrap, controls, and the GO / NO-GO decision.
Implements PREREGISTRATION.md Sections 4-6. Reads every recognizer under <out>/emb and every generator under <out>/gen.
Outputs (in <out>/results): metrics.csv, deltas.csv, identity_preservation.csv, generation_failures.csv, decision.json, REPORT.md
Usage: python s6_analyze.py [--config config.yaml] [--bootstrap N]"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import ClusterBootstrap, auc_w, bin_labels, gap_bin, gen_key, load_config, out_dir, percentile_ci, tar_at_fmr


def load_emb(edir, group):
    E = np.load(edir / f"{group}.npy")
    idx = pd.read_csv(edir / f"{group}.csv")
    return E, {f: k for k, f in enumerate(idx.face_id)}


def lookup(E, pos, keys):
    k = np.array([pos.get(x, -1) for x in keys])
    out = np.full((len(keys), E.shape[1]), np.nan, np.float32)
    out[k >= 0] = E[k[k >= 0]]
    return out


def cosine(a, b):
    return (a * b).sum(1)                       # rows are L2-normalised; NaN rows stay NaN


def age_only_control_keys(jobs, seed):
    """job_id -> job_id of a *different person's* generated face with the same target age in the same fold."""
    rng = np.random.default_rng(seed)
    m = {}
    for _, g in jobs.groupby(["fold", "t"]):
        ids, persons = g.job_id.to_numpy(), g.person_id.to_numpy()
        for k in range(len(g)):
            cand = np.nonzero(persons != persons[k])[0]
            if len(cand):
                m[ids[k]] = ids[rng.choice(cand)]
    return m


def crossfit(X, y, fold):
    s = np.full(len(y), np.nan)
    for f in np.unique(fold):
        tr, te = fold != f, fold == f
        clf = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000))
        clf.fit(X[tr], y[tr])
        s[te] = clf.decision_function(X[te])
    return s


def metrics_for(scores, y, w, fmr):
    g, i = y == 1, y == 0
    return {name: (tar_at_fmr(s[g], w[g], s[i], w[i], fmr)[0], auc_w(s[g], w[g], s[i], w[i])) for name, s in scores.items()}


def evaluate_cell(df, score_cols, cfg, n_boot, seed):
    """df: complete-case pairs of one stratum. Returns rows of per-bin metrics and deltas vs s0 with 95% and adjusted CIs."""
    an = cfg["analysis"]
    adj = 1 - an["alpha"] / an["n_decision_tests"]
    y = df.label.to_numpy()
    bins = df.gap_bin.to_numpy()
    scores = {c: df[c].to_numpy() for c in score_cols}
    fmr_bin = {}
    for b in np.unique(bins):
        n_imp = int(((bins == b) & (y == 0)).sum())
        fmr_bin[b] = an["fmr_primary"] if n_imp >= an["min_impostor_weight_for_primary"] else an["fmr_fallback"]
    point, boot = {}, {b: [] for b in fmr_bin}
    for b, fmr in fmr_bin.items():
        m = bins == b
        point[b] = metrics_for({k: v[m] for k, v in scores.items()}, y[m], np.ones(m.sum()), fmr)
    bs = ClusterBootstrap(df.person_1.to_numpy(), df.person_2.to_numpy(), n_boot, seed)
    for w in bs.weights():
        for b, fmr in fmr_bin.items():
            m = bins == b
            boot[b].append(metrics_for({k: v[m] for k, v in scores.items()}, y[m], w[m], fmr))
    rows, drows = [], []
    for b, fmr in fmr_bin.items():
        m = bins == b
        n_g, n_i = int((m & (y == 1)).sum()), int((m & (y == 0)).sum())
        for c in score_cols:
            tars = [r[c][0] for r in boot[b]]
            aucs = [r[c][1] for r in boot[b]]
            rows.append(dict(bin=b, score=c, n_genuine=n_g, n_impostor=n_i, fmr=fmr, tar=point[b][c][0],
                             tar_ci95=percentile_ci(tars, 0.95), auc=point[b][c][1], auc_ci95=percentile_ci(aucs, 0.95)))
            if c == "s0":
                continue
            dt = [r[c][0] - r["s0"][0] for r in boot[b]]
            da = [r[c][1] - r["s0"][1] for r in boot[b]]
            drows.append(dict(bin=b, score=c, n_genuine=n_g, n_impostor=n_i, fmr=fmr,
                              d_tar=point[b][c][0] - point[b]["s0"][0], d_tar_ci95=percentile_ci(dt, 0.95), d_tar_ci_adj=percentile_ci(dt, adj),
                              d_auc=point[b][c][1] - point[b]["s0"][1], d_auc_ci95=percentile_ci(da, 0.95)))
    return rows, drows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--bootstrap", type=int, default=None)
    a = ap.parse_args()
    cfg = load_config(a.config)
    out = out_dir(cfg)
    res = out_dir(cfg, "results")
    n_boot = a.bootstrap or cfg["analysis"]["bootstrap"]
    pairs = pd.read_csv(out / "pairs.csv")
    jobs = pd.read_csv(out / "jobs.csv")
    edges = cfg["pairs"]["gap_edges"]
    gens = [g.name for g in sorted((out / "gen").glob("*")) if g.name in cfg["generators"]]
    recs = [r.name for r in sorted((out / "emb").glob("*")) if r.name in cfg["recognizers"]]
    decision_gens = [g for g in gens if cfg["generators"][g].get("decision")]
    fwd = [gen_key(i, t) for i, t in zip(pairs.img_1, pairs.t_fwd)]
    bwd = [gen_key(i, t) for i, t in zip(pairs.img_2, pairs.t_bwd)]
    ctrl = age_only_control_keys(jobs, cfg["seed"] + 1)
    all_m, all_d, idp, fails, cells = [], [], [], [], []

    for r in recs:
        edir = out / "emb" / r
        pf = json.load(open(edir / "preflight.json")) if (edir / "preflight.json").exists() else {"pass": False}
        Er, pr = load_emb(edir, "real")
        e1, e2 = lookup(Er, pr, pairs.img_1), lookup(Er, pr, pairs.img_2)
        base = pairs.assign(s0=cosine(e1, e2))
        per_gen = {}
        for g in gens:
            if not (edir / f"{g}.npy").exists():
                continue
            Eg, pg = load_emb(edir, g)
            gf, gb = lookup(Eg, pg, fwd), lookup(Eg, pg, bwd)
            cf, cb = lookup(Eg, pg, [ctrl.get(k, "") for k in fwd]), lookup(Eg, pg, [ctrl.get(k, "") for k in bwd])
            per_gen[g] = dict(s_fwd=cosine(gf, e2), s_bwd=cosine(e1, gb), c_fwd=cosine(cf, e2), c_bwd=cosine(e1, cb))
            # identity preservation and failures, per generated face
            st = pd.read_csv(out / "gen" / g / "status.csv")
            src = lookup(Er, pr, st.img_id)
            gen_e = lookup(Eg, pg, st.job_id)
            st = st.assign(id_cos=cosine(gen_e, src), detected=np.isfinite(gen_e[:, 0]), shift=(st.t - st.age).abs())
            st["shift_bin"] = gap_bin(st["shift"].to_numpy(), edges)
            for (sb, adult), q in st.assign(adult=st.age >= cfg["pairs"]["adult_min_age"]).groupby(["shift_bin", "adult"]):
                idp.append(dict(recognizer=r, generator=g, age_shift_bin=sb, adult_source=adult, n=len(q),
                                id_cos_mean=q.id_cos.mean(), id_cos_q10=q.id_cos.quantile(0.1), id_cos_median=q.id_cos.median()))
            if r == recs[0]:
                for sb, q in st.groupby("shift_bin"):
                    fails.append(dict(generator=g, age_shift_bin=sb, n=len(q), not_generated=float((~q.ok).mean()),
                                      not_detected_after_generation=float((q.ok & ~q.detected).mean())))
        if not per_gen:
            continue
        complete = np.isfinite(base.s0.to_numpy())
        for g in decision_gens:
            if g in per_gen:
                complete &= np.isfinite(per_gen[g]["s_fwd"]) & np.isfinite(per_gen[g]["s_bwd"])
        for g, sc in per_gen.items():
            ok = complete & np.isfinite(sc["s_fwd"]) & np.isfinite(sc["s_bwd"])
            d = base[ok].assign(s_fwd=sc["s_fwd"][ok], s_bwd=sc["s_bwd"][ok])
            d["s_bridge"] = (d.s_fwd + d.s_bwd) / 2
            y, fold = d.label.to_numpy(), d.fold.to_numpy()
            d["fused"] = crossfit(d[["s0", "s_fwd", "s_bwd"]].to_numpy(), y, fold)
            cok = np.isfinite(sc["c_fwd"][ok]) & np.isfinite(sc["c_bwd"][ok])
            Xc = np.column_stack([d.s0, sc["c_fwd"][ok], sc["c_bwd"][ok]])
            d["control_fused"] = np.nan
            d.loc[cok, "control_fused"] = crossfit(Xc[cok], y[cok], fold[cok])
            for (lab, strat) in (("adult", d.adult.to_numpy()), ("all_ages", np.ones(len(d), bool))):
                dd = d[strat & d.control_fused.notna().to_numpy()]
                rows, drows = evaluate_cell(dd, ["s0", "s_bridge", "fused", "control_fused"], cfg, n_boot, cfg["seed"])
                for x in rows:
                    all_m.append(dict(recognizer=r, generator=g, stratum=lab, **x))
                for x in drows:
                    all_d.append(dict(recognizer=r, generator=g, stratum=lab, **x))
                # mean bridge shift by label and bin (descriptive)
                for (b, yy), q in dd.groupby(["gap_bin", "label"]):
                    idp.append(dict(recognizer=r, generator=g, stratum=lab, gap_bin=b, label=int(yy), n=len(q),
                                    mean_sfwd_minus_s0=float((q.s_fwd - q.s0).mean()), mean_sbwd_minus_s0=float((q.s_bwd - q.s0).mean())))
            print(f"{r} x {g}: {ok.sum()} complete-case pairs", flush=True)

        # decision cells for this recognizer
        indep = cfg["recognizers"][r].get("independent", False)
        for g in decision_gens:
            for b in cfg["analysis"]["decision_bins"]:
                f = [x for x in all_d if x["recognizer"] == r and x["generator"] == g and x["stratum"] == "adult" and x["bin"] == b]
                fz = next((x for x in f if x["score"] == "fused"), None)
                cz = next((x for x in f if x["score"] == "control_fused"), None)
                if fz is None:
                    cells.append(dict(recognizer=r, generator=g, bin=b, available=False))
                    continue
                go = bool(indep and pf.get("pass") and fz["d_tar_ci_adj"][0] > 0 and (cz is None or cz["d_tar_ci_adj"][0] <= 0))
                cells.append(dict(recognizer=r, generator=g, bin=b, available=True, independent=indep, preflight_pass=bool(pf.get("pass")),
                                  n_genuine=fz["n_genuine"], fmr=fz["fmr"], d_tar=fz["d_tar"], d_tar_ci_adj=fz["d_tar_ci_adj"],
                                  control_d_tar=cz["d_tar"] if cz else None, control_d_tar_ci_adj=cz["d_tar_ci_adj"] if cz else None, go=go))

    def flat(rows):
        df = pd.DataFrame(rows)
        for c in [c for c in df.columns if c.endswith(("ci95", "ci_adj"))]:
            df[c + "_lo"], df[c + "_hi"] = df[c].str[0], df[c].str[1]
            df = df.drop(columns=c)
        return df

    flat(all_m).to_csv(res / "metrics.csv", index=False)
    flat(all_d).to_csv(res / "deltas.csv", index=False)
    pd.DataFrame(idp).to_csv(res / "identity_preservation.csv", index=False)
    pd.DataFrame(fails).to_csv(res / "generation_failures.csv", index=False)
    go_cells = [c for c in cells if c.get("go")]
    verdict = "GO" if go_cells else "NO-GO"
    if go_cells and (len({c["bin"] for c in go_cells}) == 1 or len({c["generator"] for c in go_cells}) == 1):
        verdict = "GO (narrow)"
    dec = dict(verdict=verdict, config_hash=cfg["_hash"], bootstrap=n_boot, adjusted_level=1 - cfg["analysis"]["alpha"] / cfg["analysis"]["n_decision_tests"],
               cells=cells, note="Decision rule: PREREGISTRATION.md Section 6. Secondary metrics never override it.")
    json.dump(dec, open(res / "decision.json", "w"), indent=1, default=float)
    lines = [f"# Experiment 0 result: **{verdict}**", "", f"config hash `{cfg['_hash']}`, bootstrap {n_boot}", "",
             "| recognizer | generator | bin | n genuine | FMR | dTAR fused-s0 | adj. CI | control dTAR | control adj. CI | GO |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in cells:
        if not c.get("available"):
            lines.append(f"| {c['recognizer']} | {c['generator']} | {c['bin']} | – | – | not available | | | | no |")
            continue
        ci = c["d_tar_ci_adj"]
        cc = c["control_d_tar_ci_adj"] or (np.nan, np.nan)
        lines.append(f"| {c['recognizer']} | {c['generator']} | {c['bin']} | {c['n_genuine']} | {c['fmr']:g} | {c['d_tar']:+.4f} | [{ci[0]:+.4f}, {ci[1]:+.4f}] | "
                     f"{(c['control_d_tar'] if c['control_d_tar'] is not None else np.nan):+.4f} | [{cc[0]:+.4f}, {cc[1]:+.4f}] | {'yes' if c['go'] else 'no'} |")
    lines += ["", "Full tables: metrics.csv, deltas.csv, identity_preservation.csv, generation_failures.csv."]
    (res / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
