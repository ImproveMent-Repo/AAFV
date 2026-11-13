# AAFV-05 submission checklist

Nothing below has been done unless it is ticked. Do not submit until every **Required** item is ticked.

## Authorship and metadata (Required; from `Authorship.md`)
- [ ] All five authors confirm the author order: Anurag Nayak, Sujal Chondhekar, Sumit Kumar, Piyush Jain, Swati Hira (provisional).
- [ ] Corresponding author designated.
- [ ] Institutional e-mail addresses (`[to be confirmed]` in `main.tex`).
- [ ] ORCID iDs for every author.
- [ ] Funding statement (`[to be confirmed]`).
- [ ] CRediT contribution statement, written from confirmed information only. Do not invent roles.
- [ ] Enrollment numbers are **not** in the byline (already satisfied).

## Authorship of the text (Required)
- [ ] **Each section is rewritten or substantively revised by an author** who can explain and defend it. The current text was drafted by an AI assistant (see `ORIGINALITY_REVIEW.md`, Phase 7).
- [ ] The "Use of AI Tools" section in `main.tex` is updated to describe exactly what was AI-assisted in the final version.
- [ ] A **similarity (text-matching) report** is run on the final text. The earlier Turnitin reports were AI-writing reports only.
- [ ] `python scripts/check_claims.py` passes after any edit to numbers in the prose.

## Scientific items (Required)
- [ ] Decide how to present the four hand-quarantined identities. Ideally, look at their crops (`artifacts/p1/` on the Drive) with scores hidden, and state whether they are duplicate records or look-alikes.
- [ ] Optional but strengthens §IV-F: visually check a random sample (e.g. 50) of 15+-year MORPH "same-person" pairs, by two annotators blind to scores.
- [ ] The advisor agrees with the framing: a re-analysis paper with negative results, for a biometrics venue.
- [ ] Choose the venue and re-check its author guidelines (format, page limit, AI-use and ethics statements, data rules).

## Ethics and data (Required)
- [ ] Institutional review status (`[to be confirmed]` in the Ethics Statement).
- [ ] Confirm the MORPH and FG-NET licence terms allow the analyses and the aggregate figures. No face images are included.
- [ ] If a face image is ever added (e.g. the SAM qualitative panels in `CVPR_redesign/image_audit/`), confirm that the licence permits publication first.
- [ ] Repository URL for the Data and Code Availability statement (`[repository to be confirmed]`). Deposit the analysis scripts and aggregate CSVs, not raw data.

## Security (Required before sharing anything)
- [ ] Remove `.ssh/`, `.kaggle/` and `.bash_history` from the public Drive folder, and replace the SSH keys and Kaggle token (`CVPR_redesign/DRIVE_FINDINGS.md` §1).

## Formatting (checked 2026-11-14)
- [x] Compiles with no undefined references or citations, and no overfull boxes.
- [x] All tables generated from source files; 33/33 prose numbers verified.
- [x] Bibliography: only cited, verified entries.
