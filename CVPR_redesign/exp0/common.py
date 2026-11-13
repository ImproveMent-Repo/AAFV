"""Shared helpers for Experiment 0: config, paths, gap bins, weighted verification metrics, person-cluster bootstrap."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
AAFV_SRC = REPO / "Code" / "AAFV_Net" / "src"          # reuse aafv.align (FFHQ alignment) from the existing pipeline


def load_config(path=None):
    with open(path or HERE / "config.yaml") as f:
        cfg = yaml.safe_load(f)
    cfg["_hash"] = hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode()).hexdigest()[:12]
    return cfg


def out_dir(cfg, *parts):
    p = Path(cfg["out_dir"]).joinpath(*parts)
    p.mkdir(parents=True, exist_ok=True)
    return p


def add_aafv_to_path():
    if str(AAFV_SRC) not in sys.path:
        sys.path.insert(0, str(AAFV_SRC))


# ---------------------------------------------------------------- gap bins
def bin_labels(edges):
    labs = [f"{lo}-{hi - 1}" for lo, hi in zip(edges[:-1], edges[1:])]
    return labs + [f"{edges[-1]}+"]


def gap_bin(gap, edges):
    """edges [0,5,15,30] -> '0-4', '5-14', '15-29', '30+'."""
    labs = bin_labels(edges)
    idx = np.searchsorted(np.asarray(edges), np.asarray(gap), side="right") - 1
    idx = np.clip(idx, 0, len(labs) - 1)
    return np.asarray(labs, dtype=object)[idx]


def gen_key(img_id, t):
    """Identifier of one generated face: source image, target age."""
    return f"{img_id}__{int(t)}"


# ---------------------------------------------------------------- weighted metrics
def tar_at_fmr(gs, gw, ims, iw, fmr):
    """Weighted TAR at FMR. Accept iff score > t, where t is the smallest impostor score such that the impostor
    weight strictly above t is <= fmr * total impostor weight. Returns (tar, threshold)."""
    gs, gw, ims, iw = map(np.asarray, (gs, gw, ims, iw))
    W = iw.sum()
    if W <= 0 or gw.sum() <= 0:
        return np.nan, np.nan
    o = np.argsort(-ims, kind="mergesort")
    s, w = ims[o], iw[o]
    # weight strictly above each distinct score
    uniq, first = np.unique(-s, return_index=True)           # descending distinct scores
    above = np.concatenate([[0.0], np.cumsum(w)])[first]     # weight of scores strictly greater than uniq[k]
    ok = above <= fmr * W
    t = -uniq[np.nonzero(ok)[0].max()]                       # lowest score whose 'strictly above' weight is within budget
    return float((gw * (gs > t)).sum() / gw.sum()), float(t)


def auc_w(gs, gw, ims, iw):
    """Weighted AUC = P(genuine > impostor) + 0.5 P(tie)."""
    gs, gw, ims, iw = map(np.asarray, (gs, gw, ims, iw))
    if gw.sum() <= 0 or iw.sum() <= 0:
        return np.nan
    o = np.argsort(ims, kind="mergesort")
    s, cw = ims[o], np.concatenate([[0.0], np.cumsum(iw[o])])
    lo = cw[np.searchsorted(s, gs, side="left")]
    hi = cw[np.searchsorted(s, gs, side="right")]
    return float((gw * (lo + 0.5 * (hi - lo))).sum() / (gw.sum() * iw.sum()))


# ---------------------------------------------------------------- person-cluster bootstrap
class ClusterBootstrap:
    """Two-way person-cluster bootstrap. Persons are resampled with replacement; a pair's weight is the product
    of its persons' multiplicities (genuine pairs have one person, so weight = its multiplicity)."""

    def __init__(self, person_1, person_2, n_boot, seed):
        persons = np.unique(np.concatenate([person_1, person_2]))
        ix = {p: i for i, p in enumerate(persons)}
        self.i1 = np.array([ix[p] for p in person_1])
        self.i2 = np.array([ix[p] for p in person_2])
        self.same = self.i1 == self.i2
        self.n_persons, self.n_boot, self.seed = len(persons), n_boot, seed

    def weights(self):
        rng = np.random.default_rng(self.seed)
        for _ in range(self.n_boot):
            c = rng.multinomial(self.n_persons, np.full(self.n_persons, 1.0 / self.n_persons)).astype(float)
            yield np.where(self.same, c[self.i1], c[self.i1] * c[self.i2])


def percentile_ci(x, level):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan
    a = (1 - level) / 2
    return float(np.quantile(x, a)), float(np.quantile(x, 1 - a))


def cos_rows(a, b):
    a = a / np.linalg.norm(a, axis=1, keepdims=True)
    b = b / np.linalg.norm(b, axis=1, keepdims=True)
    return (a * b).sum(1)
