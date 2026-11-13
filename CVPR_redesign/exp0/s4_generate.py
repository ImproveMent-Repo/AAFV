"""Step 4: run one generator on every job in jobs.csv. Restartable: outputs that already exist are skipped.
Output: <out>/gen/<generator>/<img_id>__<t>.png (256x256) and <out>/gen/<generator>/status.csv
Backends:
  sam       official SAM repo (yuval-alaluf/SAM), run once per target age on a folder of crops
  command   any CLI (used for FADING), run once per source image with all its target ages; see config.yaml
  identity  copies the input; for testing the pipeline only
Usage: python s4_generate.py --generator sam [--config config.yaml] [--limit N]"""
import argparse
import shutil
import subprocess
import sys
import tempfile
import time
from glob import glob
from pathlib import Path

import pandas as pd
from PIL import Image

from common import REPO, gen_key, load_config, out_dir

SAM_WRAPPER = REPO / "Code" / "AAFV_Net" / "scripts" / "run_sam_inference.py"   # torch>=2.6 loading shim for the official script


def clip_age(t, rng):
    return int(min(max(int(t), rng[0]), rng[1]))


def save_256(src, dst):
    im = Image.open(src).convert("RGB")
    if im.size != (256, 256):
        im = im.resize((256, 256), Image.LANCZOS)
    im.save(dst)


def run_identity(todo, crops, dst, g):
    for r in todo.itertuples():
        save_256(crops / f"{r.img_id}.png", dst / f"{r.job_id}.png")


def run_sam(todo, crops, dst, g):
    for t, grp in todo.groupby("t_gen"):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            inp = tmp / "in"
            inp.mkdir()
            for i in grp.img_id.unique():
                shutil.copy(crops / f"{i}.png", inp / f"{i}.png")
            cmd = [sys.executable, str(SAM_WRAPPER), g["sam_dir"], "--exp_dir", str(tmp / "exp"), "--checkpoint_path", g["checkpoint"],
                   "--data_path", str(inp), "--test_batch_size", str(g.get("batch_size", 16)), "--test_workers", "4",
                   "--resize_outputs", "--target_age", str(t)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"[sam] age {t} failed: {(r.stdout + r.stderr)[-500:]}", flush=True)
                continue
            for row in grp.itertuples():
                f = tmp / "exp" / "inference_results" / str(t) / f"{row.img_id}.png"
                if f.exists():
                    save_256(f, dst / f"{row.job_id}.png")
        print(f"[sam] age {t}: {len(grp)} jobs", flush=True)


def run_command(todo, crops, dst, g):
    for img_id, grp in todo.groupby("img_id"):
        with tempfile.TemporaryDirectory() as tmp:
            r0 = grp.iloc[0]
            gw = {"M": "male", "F": "female"}.get(r0.sex, g.get("unknown_gender_word", "person"))
            ph = dict(fading_dir=g.get("fading_dir", ""), specialized_path=g.get("specialized_path", ""), src=str(crops / f"{img_id}.png"),
                      img_id=img_id, age_init=str(int(r0.age)), gender_word=gw, tmp_out=tmp)
            cmd = []
            for tok in g["command"]:
                if tok == "{targets}":
                    cmd += [str(t) for t in sorted(grp.t_gen.unique())]
                else:
                    cmd.append(tok.format(**ph))
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"[cmd] {img_id} failed: {(r.stdout + r.stderr)[-500:]}", flush=True)
                continue
            for row in grp.itertuples():
                hits = sorted(glob(g["output_pattern"].format(tmp_out=tmp, t=row.t_gen, img_id=img_id)))
                if len(hits) == 1:
                    save_256(hits[0], dst / f"{row.job_id}.png")
                elif len(hits) > 1:
                    print(f"[cmd] {row.job_id}: pattern matched {len(hits)} files, skipped (fix output_pattern)", flush=True)


BACKENDS = {"identity": run_identity, "sam": run_sam, "command": run_command}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--generator", required=True)
    ap.add_argument("--limit", type=int, default=0, help="only the first N pending jobs (smoke test)")
    a = ap.parse_args()
    cfg = load_config(a.config)
    g = cfg["generators"][a.generator]
    out = out_dir(cfg)
    crops = out / "crops"
    dst = out_dir(cfg, "gen", a.generator)
    jobs = pd.read_csv(out / "jobs.csv")
    jobs["t_gen"] = [clip_age(t, g["age_range"]) for t in jobs.t]
    jobs["job_id"] = [gen_key(i, t) for i, t in zip(jobs.img_id, jobs.t)]          # file named by the *requested* age
    todo = jobs[[not (dst / f"{j}.png").exists() for j in jobs.job_id]]
    if a.limit:
        todo = todo.head(a.limit)
    print(f"{a.generator}: {len(jobs)} jobs, {len(todo)} pending, {int((jobs.t != jobs.t_gen).sum())} clipped to {g['age_range']}", flush=True)
    t0 = time.time()
    BACKENDS[g["backend"]](todo, crops, dst, g)
    jobs["ok"] = [(dst / f"{j}.png").exists() for j in jobs.job_id]
    jobs.to_csv(dst / "status.csv", index=False)
    print(f"done in {time.time() - t0:.0f}s; ok {int(jobs.ok.sum())}/{len(jobs)}; failure rate by requested age decile:")
    print(jobs.assign(dec=(jobs.t // 10) * 10).groupby("dec").ok.apply(lambda s: round(1 - s.mean(), 4)).to_string())


if __name__ == "__main__":
    main()
