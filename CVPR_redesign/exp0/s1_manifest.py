"""Step 1: list the images of every configured dataset -> <out>/images.csv
Columns: img_id, dataset, person_id, age, sex (M/F/U), path. Person ids are prefixed with the dataset name.
Usage: python s1_manifest.py [--config config.yaml]"""
import argparse
import re
from pathlib import Path

import pandas as pd

from common import load_config, out_dir

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
FGNET_RE = re.compile(r"^(\d{3})A(\d{2})[a-zA-Z]?$")


def parse_agedb(name):
    """'0_MariaCallas_35_f.jpg' -> (person 'MariaCallas', age 35, sex 'F'). Returns None if the name does not match."""
    stem = Path(name).stem
    parts = stem.rsplit("_", 2)
    if len(parts) != 3 or "_" not in parts[0]:
        return None
    head, age, sex = parts
    person = head.split("_", 1)[1]
    if not age.isdigit() or sex.lower() not in ("m", "f"):
        return None
    return person, int(age), sex.upper()


def parse_fgnet(name):
    """'001A02.JPG' / '001A43a.JPG' -> (person '001', age 2, sex 'U')."""
    m = FGNET_RE.match(Path(name).stem)
    if not m:
        return None
    return m.group(1), int(m.group(2)), "U"


def scan(root, parser, dataset):
    rows, bad = [], []
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMG_EXT:
            continue
        r = parser(p.name)
        if r is None:
            bad.append(p.name)
            continue
        person, age, sex = r
        rows.append(dict(img_id=f"{dataset}__{p.stem}", dataset=dataset, person_id=f"{dataset}:{person}", age=age, sex=sex, path=str(p)))
    return rows, bad


def from_csv(csv, dataset):
    d = pd.read_csv(csv)
    if "sex" not in d:
        d["sex"] = "U"
    return [dict(img_id=f"{dataset}__{Path(r.path).stem}", dataset=dataset, person_id=f"{dataset}:{r.person_id}", age=int(r.age),
                 sex=str(r.sex).upper()[:1] if str(r.sex).upper()[:1] in "MF" else "U", path=str(r.path)) for r in d.itertuples()], []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    a = ap.parse_args()
    cfg = load_config(a.config)
    rows = []
    for name, d in cfg["datasets"].items():
        if not d.get("use"):
            continue
        if d["kind"] == "agedb":
            r, bad = scan(d["root"], parse_agedb, name)
        elif d["kind"] == "fgnet":
            r, bad = scan(d["root"], parse_fgnet, name)
        elif d["kind"] == "csv":
            r, bad = from_csv(d["csv"], name)
        else:
            raise ValueError(f"unknown dataset kind {d['kind']}")
        if not r:
            raise SystemExit(f"{name}: no images parsed under {d.get('root') or d.get('csv')}")
        if d.get("sex_overrides"):
            ov = pd.read_csv(d["sex_overrides"], dtype=str)
            m = {f"{name}:{p}": s.strip().upper()[:1] for p, s in zip(ov.person, ov.sex) if s.strip().upper()[:1] in ("M", "F")}
            for x in r:
                x["sex"] = m.get(x["person_id"], x["sex"])
            print(f"{name}: sex set for {len(m)} persons from {d['sex_overrides']}")
        print(f"{name}: {len(r)} images, {len({x['person_id'] for x in r})} persons, {len(bad)} unparsed names (e.g. {bad[:3]})")
        rows += r
    df = pd.DataFrame(rows)
    dup = df.img_id.duplicated()
    if dup.any():
        raise SystemExit(f"duplicate img_id values, e.g. {df.img_id[dup].head(3).tolist()}")
    p = out_dir(cfg) / "images.csv"
    df.to_csv(p, index=False)
    print(f"wrote {p}: {len(df)} images; ages {df.age.min()}-{df.age.max()}; sex {df.sex.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
