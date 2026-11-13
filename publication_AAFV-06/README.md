# AAFV-06: *AAFV-Net: Reliability-Gated Three-Way Decisions for Adult Cross-Age Face Verification With Audited Random-Impostor False-Accept Risk*

**Status:** complete draft, **not submitted**. It compiles to 13 pages (IEEEtran journal format).
The text was drafted with an AI assistant and **must be revised by the authors** before submission (see `SUBMISSION_CHECKLIST.md`).

## What changed from AAFV-05 (as requested)
1. **Title restored** to the AAFV-Net title used in AAFV-04.
2. **Architecture added.**
   - Fig. 2 is the AAFV-Net architecture, regenerated from the AAFV-04 generator. Its ensemble size is corrected from 5 to 3 networks, as in the evaluated checkpoint.
   - Section IV gives the full method with equations: alignment, quality, similarity measures, SAM evidence, reliability, fusion, masking, calibration, guards and thresholds.
   - Fig. 11 is the proposed redesigned architecture.
3. **Image results added:**
   - Fig. 1 concept;
   - Fig. 3 outcome shares;
   - Fig. 5 MORPH audit examples;
   - Fig. 7 SAM outputs for two persons;
   - Fig. 8 change maps (where the generator edits the face);
   - Fig. 10 the FG-NET false accepts;
   - Fig. 11 the proposed architecture ("what could be done").
4. **References restored and analysed.** There are 90 entries, all cited. `REFERENCE_ANALYSIS.md` covers every prior list (BASE_Paper, AAFV-01 to AAFV-05), including the fabricated or misattributed entries in earlier versions that must not come back.
   The venue does not change the paper's content; it changes format and length only. The earlier cut was a length decision.
5. **Paper expanded from 7 to 13 pages.** New sections: problem formulation and threat model, full method, data and protocol (with chronology), results as reported (test, FG-NET, ablations), the re-analysis, image results, and "What Could Be Done" (proposed architecture, ablation plan, pre-registered test, long-gap datasets).

## Folder contents
| Path | What |
|---|---|
| `main.tex`, `main.pdf` | Manuscript and compiled PDF (**the PDF embeds face images: local only, git-ignored**) |
| `references.bib` | 90 entries (68 from AAFV-04, 19 newly verified, 3 standard); built by `scripts/build_bib.py` |
| `REFERENCE_ANALYSIS.md`, `reference_sources.txt` | Analysis of every prior reference list, and the raw extracted lists |
| `tables/*.tex` | 12 tables, generated from logged files by `scripts/build_assets.py` and `scripts/build_tables_06.py` |
| `figures/fig*` | Plots and diagrams (no faces; safe to commit) |
| `figures/faces_*` | Face images from MORPH and FG-NET (**git-ignored: licensed data, public repository**) |
| `scripts/make_figures.py` | Regenerates every figure, including the corrected architecture and the face composites |
| `scripts/check_claims.py` | Checks 44 numbers in the prose against their source files (44/44) |
| `scripts/collect_references.py` | Extracts the reference lists of all prior versions |
| `build.sh` | One command: tables → figures → bibliography → claim check → LaTeX |
| `CLAIMS_LEDGER.md`, `CHANGES_FROM_AAFV-05.md`, `SUBMISSION_CHECKLIST.md`, `supplementary/` | Provenance, change log, remaining work, pre-registration |

## Rebuild
```bash
bash build.sh
```
This needs Python 3 (pandas, matplotlib, Pillow) and LaTeX (MiKTeX was used). The face figures need `Result_Images/`, `CVPR_redesign/image_audit/out/` and `Code/AAFV_Net/q/audit/`, which are local only.
