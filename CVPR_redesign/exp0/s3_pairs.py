"""Step 3: person folds, genuine pairs, age-matched-swap impostor pairs, and the generation job list.
Inputs: images.csv and align.csv (only aligned images are used).
Outputs: <out>/pairs.csv, <out>/jobs.csv, <out>/pairs_summary.txt
Rules: PREREGISTRATION.md Section 2. Usage: python s3_pairs.py [--config config.yaml]"""
import argparse
from collections import defaultdict
from itertools import combinations

import numpy as np
import pandas as pd

from common import gap_bin, gen_key, load_config, out_dir


def assign_folds(persons, n_folds, rng):
    p = np.array(sorted(persons))
    rng.shuffle(p)
    return {q: i % n_folds for i, q in enumerate(p)}


def genuine_pairs(imgs, edges, cap, rng):
    rows = []
    for pid, g in imgs.groupby("person_id"):
        g = g.sort_values(["age", "img_id"])
        cand = defaultdict(list)
        for (_, r1), (_, r2) in combinations(g.iterrows(), 2):
            if r1.age > r2.age:
                r1, r2 = r2, r1
            cand[gap_bin(r2.age - r1.age, edges)].append((r1, r2))
        for b, lst in cand.items():
            take = rng.permutation(len(lst))[:cap]
            for k in sorted(take):
                r1, r2 = lst[k]
                rows.append(dict(person_1=pid, person_2=pid, img_1=r1.img_id, img_2=r2.img_id, a1=int(r1.age), a2=int(r2.age),
                                 age_2=int(r2.age), sex=r1.sex, fold=int(r1.fold), gap_bin=b, label=1))
    return pd.DataFrame(rows)


def impostor_pairs(gen, imgs, m, tol, tol_max, rng):
    """For each genuine (I1, I2) pick up to m images I2' of distinct other persons in the same fold, |age - a2| <= tol
    (widened by 1 year at a time up to tol_max), same sex when both are known. Impostors inherit gap_bin, a1, a2."""
    by = defaultdict(list)                                     # (fold, age) -> rows
    for r in imgs.itertuples(index=False):
        by[(r.fold, r.age)].append(r)
    rows, short = [], 0
    for g in gen.itertuples(index=False):
        chosen, used = [], {g.person_1}
        t = tol
        while len(chosen) < m and t <= tol_max:
            pool = [r for a in range(g.a2 - t, g.a2 + t + 1) for r in by.get((g.fold, a), [])
                    if r.person_id not in used and (g.sex == "U" or r.sex == "U" or r.sex == g.sex)]
            order = rng.permutation(len(pool))
            for k in order:
                r = pool[k]
                if r.person_id in used:
                    continue
                chosen.append(r)
                used.add(r.person_id)
                if len(chosen) == m:
                    break
            t += 1
        short += len(chosen) < m
        for r in chosen:
            rows.append(dict(person_1=g.person_1, person_2=r.person_id, img_1=g.img_1, img_2=r.img_id, a1=g.a1, a2=g.a2,
                             age_2=int(r.age), sex=g.sex, fold=g.fold, gap_bin=g.gap_bin, label=0))
    return pd.DataFrame(rows), short


def build(imgs, cfg):
    pc = cfg["pairs"]
    rng = np.random.default_rng(cfg["seed"])
    folds = assign_folds(imgs.person_id.unique(), pc["n_folds"], rng)
    imgs = imgs.assign(fold=imgs.person_id.map(folds))
    gen = genuine_pairs(imgs, pc["gap_edges"], pc["max_genuine_per_person_per_bin"], rng)
    imp, short = impostor_pairs(gen, imgs, pc["impostors_per_genuine"], pc["impostor_age_tol"], pc["impostor_age_tol_max"], rng)
    pairs = pd.concat([gen, imp], ignore_index=True)
    ages = dict(zip(imgs.img_id, imgs.age))
    # adult stratum: every image in the pair (I1, I2 or I2') is at least adult_min_age
    pairs["adult"] = [(ages[i] >= pc["adult_min_age"]) and (ages[j] >= pc["adult_min_age"]) for i, j in zip(pairs.img_1, pairs.img_2)]
    pairs["t_fwd"] = pairs.a2                                  # I1 -> genuine a2 (shared by the genuine pair and its impostors)
    pairs["t_bwd"] = pairs.a1                                  # I2 (or I2') -> a1
    pairs["dataset"] = pairs.person_1.str.split(":").str[0]
    pairs.insert(0, "pair_id", [f"p{i}" for i in range(len(pairs))])
    jobs = pd.concat([pairs[["img_1", "t_fwd"]].set_axis(["img_id", "t"], axis=1), pairs[["img_2", "t_bwd"]].set_axis(["img_id", "t"], axis=1)])
    jobs = jobs.drop_duplicates().sort_values(["img_id", "t"]).reset_index(drop=True)
    jobs["job_id"] = [gen_key(i, t) for i, t in zip(jobs.img_id, jobs.t)]
    jobs = jobs.merge(imgs[["img_id", "age", "sex", "fold", "person_id"]], on="img_id")
    return pairs, jobs, short


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    a = ap.parse_args()
    cfg = load_config(a.config)
    out = out_dir(cfg)
    imgs = pd.read_csv(out / "images.csv")
    al = pd.read_csv(out / "align.csv")
    imgs = imgs[imgs.img_id.isin(al[al.ok == 1].img_id)].reset_index(drop=True)
    pairs, jobs, short = build(imgs, cfg)
    pairs.to_csv(out / "pairs.csv", index=False)
    jobs.to_csv(out / "jobs.csv", index=False)
    tab = pairs.groupby(["dataset", "adult", "gap_bin", "label"]).size().unstack("label", fill_value=0).rename(columns={0: "impostor", 1: "genuine"})
    lines = [f"config_hash={cfg['_hash']}", f"images used: {len(imgs)}, persons: {imgs.person_id.nunique()}",
             f"pairs: {len(pairs)} ({int(pairs.label.sum())} genuine)", f"genuine pairs with fewer impostors than requested: {short}",
             f"generation jobs per generator: {len(jobs)} on {jobs.img_id.nunique()} images", "", tab.to_string()]
    (out / "pairs_summary.txt").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
