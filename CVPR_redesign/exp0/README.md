# Experiment 0: does age-progressed evidence carry identity information?

This is the go/no-go probe from `../STAGE1_ASSESSMENT.md`, Section D.0.
The question, metrics and decision rule are fixed in **`PREREGISTRATION.md`**. Commit that file before step 5 is run on generated faces.

## Pipeline

| Step | Script | Needs | Output (under `out_dir`) |
|---|---|---|---|
| 1 | `s1_manifest.py` | dataset folders | `images.csv` |
| 2 | `s2_align.py` | dlib + 68-landmark predictor; InsightFace as fallback | `crops/*.png` (256×256 FFHQ), `align.csv` |
| 3 | `s3_pairs.py` | – | `pairs.csv`, `jobs.csv`, `pairs_summary.txt` |
| 4 | `s4_generate.py --generator sam` (then `fading`) | GPU, generator repo and weights | `gen/<generator>/*.png`, `status.csv` |
| 5 | `s5_embed.py --recognizer adaface` (then `magface`, `arcface`) | GPU, recognizer repo and weights | `faces112/`, `emb/<recognizer>/`, `preflight.json` |
| 6 | `s6_analyze.py` | CPU | `results/REPORT.md`, `decision.json`, CSV tables |

Run every script from this folder: `cd CVPR_redesign/exp0`. Each script takes `--config` (default `config.yaml`).
Steps 2, 4 and 5 are restartable.

Recommended order:
1. Run steps 1–3.
2. Read `pairs_summary.txt`. If the adult `15-29` and `30+` bins have too few genuine pairs, stop and reconsider the datasets before spending GPU time.
3. Run `s4_generate.py --generator identity --limit 50` as a smoke test, then step 5 for one recognizer, and check `preflight.json`.
4. Commit `PREREGISTRATION.md`.
5. Run steps 4–6 in full.

## What must be filled in or checked on the compute machine
- `config.yaml` → `datasets.*.root`, `align.dlib_predictor`.
- **SAM-age:** clone `yuval-alaluf/SAM` and download its FFHQ-aging checkpoint (`pretrained_models/sam_ffhq_aging.pt`). The existing `Code/AAFV_Net/scripts/run_sam_inference.py` shim is reused, as is `patch_sam_ops.py` if the CUDA ops need it.
- **FADING:** clone it and apply `Code/AAFV_Net/scripts/patch_fading.py`. Then **check the `command` and `output_pattern` entries** against the FADING commit you use. I wrote them from memory of its interface and could not test them. Run `--limit 5` first.
- **AdaFace:** clone `mk-minchul/AdaFace`, set `repo` and `checkpoint` (IR-101). Its preprocessing (BGR, (x/255 − 0.5)/0.5) follows that repository's README.
- **MagFace:** clone `IrvingMeng/MagFace`, set `repo` and `checkpoint`. **Check the loader (`inference.network_inf.builder_inf`) and the input normalisation.** Both were written from memory.
- **The preflight catches preprocessing mistakes.** If the s₀ AUC on real 0–4-year pairs is below 0.95, step 5 stops. It also reports whether swapping the colour channels would score higher.

## Design notes
- **All recognizer inputs, real and generated, go through the same steps:** 256 FFHQ crop → SCRFD → five landmarks → `norm_crop` 112×112.
  The old pipeline (`Code/AAFV_Net/scripts/p5_faces.py`) fed ArcFace the 256 FFHQ crop resized to 112×112, which is not the ArcFace alignment. That may have weakened every ArcFace-based number in AAFV-01 to AAFV-04, and it is worth checking separately.
- **Impostors are age-matched swaps of the older image.** I₁ is aged by exactly the same generator call for the genuine pair and for all its impostors, so any gain cannot come from treating the two classes differently.
- **Age-only control.** Each generated face is replaced by a different person's generated face at the same target age. A real identity effect must disappear under this control.
- **Fusion is cross-fitted over person-disjoint folds**, with no gap or age features.

## Cost estimate
`s3_pairs.py` prints the number of generation jobs. With SAM at about 0.06 s per face on a modern GPU `[REPORTED in Code/AAFV_Net/src/aafv/manifest.py]`, 100k jobs take roughly 2 GPU-hours plus I/O. FADING inverts each source image with a diffusion model and is far slower: about 90 s per image plus about 26 s per target age `[REPORTED, same file]`. For FADING, consider capping `max_genuine_per_person_per_bin`, or running it on the adult long-gap subset only. Any such restriction must be decided before the pre-registration commit.

## Tests
`python tests/test_exp0.py` needs no GPU, images or weights. It covers the filename parsers, gap bins, the weighted TAR@FMR, AUC and bootstrap, the pair invariants (person-disjoint folds, age and sex matching, shared forward jobs), and two simulated end-to-end runs. The simulation must give **GO** when the generated faces carry person-specific ageing and **NO-GO** when they do not. All 8 tests pass (about 50 s on CPU).
Steps 2, 4 and 5 have not been executed, because they need dlib, InsightFace, the generator and recognizer code, and a GPU.
