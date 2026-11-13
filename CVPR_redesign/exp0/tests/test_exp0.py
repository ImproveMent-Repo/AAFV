"""Tests for Experiment 0. No GPU, images or model weights are needed.
Run: python tests/test_exp0.py   (or pytest)
The end-to-end tests simulate embeddings in which generated faces either DO or do NOT carry person-specific ageing
information, and check that steps 3 and 6 give GO in the first case and NO-GO in the second."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from common import ClusterBootstrap, auc_w, gap_bin, gen_key, tar_at_fmr  # noqa: E402
from s1_manifest import parse_agedb, parse_fgnet  # noqa: E402
import s3_pairs  # noqa: E402


# ---------------------------------------------------------------- unit tests
def test_parsers():
    assert parse_agedb("0_MariaCallas_35_f.jpg") == ("MariaCallas", 35, "F")
    assert parse_agedb("16101_DustinHoffman_61_m.jpg") == ("DustinHoffman", 61, "M")
    assert parse_agedb("notes.jpg") is None
    assert parse_fgnet("001A02.JPG") == ("001", 2, "U")
    assert parse_fgnet("069A43a.JPG") == ("069", 43, "U")
    assert parse_fgnet("001B02.JPG") is None


def test_gap_bins():
    e = [0, 5, 15, 30]
    assert list(gap_bin([0, 4, 5, 14, 15, 29, 30, 60], e)) == ["0-4", "0-4", "5-14", "5-14", "15-29", "15-29", "30+", "30+"]
    assert gen_key("agedb__x", 41.0) == "agedb__x__41"


def test_tar_at_fmr():
    imp = np.arange(1000) / 1000.0                    # impostors 0.000 ... 0.999
    gen = np.array([0.9985, 0.5, 0.9995])
    tar, t = tar_at_fmr(gen, np.ones(3), imp, np.ones(1000), 1e-3)
    assert abs(t - 0.998) < 1e-12 and abs(tar - 2 / 3) < 1e-12      # one impostor (0.999) above t is allowed
    tar0, t0 = tar_at_fmr(gen, np.ones(3), imp, np.ones(1000), 0.0)
    assert t0 == 0.999 and tar0 == 1 / 3
    # weights act like repeated rows
    tar_w, _ = tar_at_fmr(gen, np.array([2, 1, 0]), imp, np.ones(1000), 1e-3)
    assert abs(tar_w - 2 / 3) < 1e-12


def test_auc():
    from sklearn.metrics import roc_auc_score
    rng = np.random.default_rng(0)
    g, i = rng.normal(1, 1, 300), rng.normal(0, 1, 500)
    g[:20] = i[:20]                                   # ties
    ref = roc_auc_score(np.r_[np.ones(300), np.zeros(500)], np.r_[g, i])
    assert abs(auc_w(g, np.ones(300), i, np.ones(500)) - ref) < 1e-12


def test_bootstrap_weights():
    # pairs: genuine (a,a), impostor (a,b), genuine (b,b): impostor weight must be count(a) * count(b)
    bs = ClusterBootstrap(np.array(["a", "a", "b", "c"]), np.array(["a", "b", "b", "c"]), 500, 0)
    ws = np.array(list(bs.weights()))
    assert (ws[:, 1] == ws[:, 0] * ws[:, 2]).all()
    assert (ws[:, [0, 2, 3]].sum(1) == 3).all()                      # three persons resampled three times
    assert abs(ws[:, 0].mean() - 1) < 0.1                            # E[count] = 1


# ---------------------------------------------------------------- simulated end-to-end
def _norm(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def simulate(root, signal, n_persons=240, imgs_per_person=8, dim=64, seed=0):
    """Real embedding: identity u_p + person-specific ageing drift w_p * age/25 + noise.
    Generated G(I -> t): with signal, u_p + w_p * t/25 (knows the person's drift); without, u_p + w_q * t/25 for a random q."""
    rng = np.random.default_rng(seed)
    U, W = _norm(rng.normal(size=(n_persons, dim))), _norm(rng.normal(size=(n_persons, dim)))
    rows = []
    for p in range(n_persons):
        a0 = int(rng.integers(16, 30))
        ages = np.sort(np.r_[a0, a0 + rng.integers(0, 50, imgs_per_person - 1)])
        for k, a in enumerate(ages):
            rows.append(dict(img_id=f"sim__{p}_{k}", dataset="sim", person_id=f"sim:{p}", age=int(a), sex="M" if p % 2 else "F", path=""))
    imgs = pd.DataFrame(rows)
    imgs.to_csv(root / "images.csv", index=False)
    pd.DataFrame(dict(img_id=imgs.img_id, ok=1, stage="sim")).to_csv(root / "align.csv", index=False)
    cfg = yaml.safe_load(open(HERE / "config.yaml"))
    cfg["out_dir"] = str(root)
    cfg["pairs"]["impostors_per_genuine"] = 6
    cfg["pairs"]["max_genuine_per_person_per_bin"] = 6
    cfg["analysis"]["min_impostor_weight_for_primary"] = 10 ** 9      # use FMR = 1e-2 everywhere (small simulation)
    cfg["recognizers"] = {"sim_rec": {"backend": "none", "independent": True}}
    cfg["generators"] = {"simgen": {"backend": "identity", "decision": True, "age_range": [0, 120]}}
    yaml.safe_dump(cfg, open(root / "cfg.yaml", "w"))
    subprocess.run([sys.executable, str(HERE / "s3_pairs.py"), "--config", str(root / "cfg.yaml")], check=True, capture_output=True)
    jobs = pd.read_csv(root / "jobs.csv")
    pidx = {pid: int(pid.split(":")[1]) for pid in imgs.person_id}
    noise = 0.55
    real = np.stack([_norm(U[pidx[r.person_id]] + W[pidx[r.person_id]] * r.age / 25 + noise * rng.normal(size=dim))
                     for r in imgs.itertuples()])
    gen = []
    for r in jobs.itertuples():
        p = pidx[r.person_id]
        q = p if signal else int(rng.integers(n_persons))
        gen.append(_norm(U[p] + W[q] * r.t / 25 + noise * rng.normal(size=dim)))
    ed = root / "emb" / "sim_rec"
    ed.mkdir(parents=True)
    np.save(ed / "real.npy", real.astype(np.float32))
    pd.DataFrame(dict(face_id=imgs.img_id, det_ok=True, det_score=1.0)).to_csv(ed / "real.csv", index=False)
    np.save(ed / "simgen.npy", np.stack(gen).astype(np.float32))
    pd.DataFrame(dict(face_id=jobs.job_id, det_ok=True, det_score=1.0)).to_csv(ed / "simgen.csv", index=False)
    json.dump({"pass": True, "as_configured": 0.99}, open(ed / "preflight.json", "w"))
    gd = root / "gen" / "simgen"
    gd.mkdir(parents=True)
    jobs.assign(t_gen=jobs.t, ok=True).to_csv(gd / "status.csv", index=False)
    r = subprocess.run([sys.executable, str(HERE / "s6_analyze.py"), "--config", str(root / "cfg.yaml"), "--bootstrap", "200"],
                       check=True, capture_output=True, text=True)
    return json.load(open(root / "results" / "decision.json")), r.stdout


def test_pairs_invariants():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        simulate(root, signal=True, n_persons=60)
        P = pd.read_csv(root / "pairs.csv")
        imgs = pd.read_csv(root / "images.csv").set_index("img_id")
        g, i = P[P.label == 1], P[P.label == 0]
        assert (g.person_1 == g.person_2).all() and (i.person_1 != i.person_2).all()
        assert (g.a1 <= g.a2).all()
        fold_of = P.groupby("person_1").fold.nunique()
        assert (fold_of == 1).all()                                            # a person lives in one fold
        f2 = dict(zip(P.person_1, P.fold))
        assert all(f2.get(b, f) == f for b, f in zip(i.person_2, i.fold))      # impostor partners come from the same fold
        assert ((imgs.loc[i.img_2, "age"].to_numpy() - i.a2.to_numpy()).__abs__() <= 4).all()
        assert (imgs.loc[i.img_2, "sex"].to_numpy() == i.sex.to_numpy()).all()
        # every impostor shares its forward job with a genuine pair
        gk = set(zip(g.img_1, g.t_fwd))
        assert all(k in gk for k in zip(i.img_1, i.t_fwd))


def test_decision_go_with_signal():
    with tempfile.TemporaryDirectory() as d:
        dec, out = simulate(Path(d), signal=True)
        assert dec["verdict"].startswith("GO"), out


def test_decision_nogo_without_signal():
    with tempfile.TemporaryDirectory() as d:
        dec, out = simulate(Path(d), signal=False)
        assert dec["verdict"] == "NO-GO", out


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                fails += 1
                print("FAIL", name, type(e).__name__, str(e)[:2000])
    sys.exit(1 if fails else 0)
