# Phase 7: Turnitin Report and Academic Originality

> Brief Section 7: analyse the report accurately. Distinguish similarity from AI-writing indicators, from real plagiarism or attribution problems, and from legitimate technical phrasing. Identify passages that need genuine rewriting, better attribution or clearer original explanation. Do not try to evade detectors, and do not drop necessary citations to lower a score.
> Prepared 2026-11-13. Inputs: `AAFV-04_Report.pdf`, `Report/AAFV-01_Report.pdf`, AAFV-04 text and bibliography, and the AIM and OrdCon PDFs in the repository.

## 1. What the reports actually measure
| Report | Type | Result | What it does **not** contain |
|---|---|---|---|
| `AAFV-04_Report.pdf` (12 pp., 11,551 words, submitted 13 Nov 2026) | **AI-writing detection only** ("AI Writing Overview") | **31%** "likely AI-generated or AI-generated and AI-revised"; 44 segments | No similarity / text-matching score, no source list |
| `Report/AAFV-01_Report.pdf` (10 pp., 6,867 words, 12 Nov 2026) | **AI-writing detection only** | **55%** AI; 52 segments | No similarity score |

**Correction to the project record.** `comprehensive_context.md` (Section 3, Stage 1) describes the AAFV-01 report as a "Turnitin plagiarism report, 55% similarity index". It is an AI-writing report. **No similarity check has been run on any version of the paper.** Nothing in the project's files shows whether text overlaps with published sources.

**What an AI-writing percentage means.**
- It is a classifier's estimate that text was produced or revised by a language model.
- It is not evidence of copying, and Turnitin's own page says it "should not be used as the sole basis for adverse actions".
- It is also not meaningless here. AAFV-03 and AAFV-04 were largely drafted and revised by AI assistants (AAFV-04 by Claude cowork), so the flags are plausibly accurate. The issue is authorship and disclosure, not plagiarism.

## 2. Which text was flagged (recovered from the report pages)
`extract_flagged.py` matches the report's cyan highlight to each text line. Output: `flagged_lines.csv`, `flagged_passages.md` (66 passages).
It is approximate. About 23% of full-width body-prose words are detected as flagged, against Turnitin's 31% of its own "qualifying" text, so some flagged text is missed.

Where the flags fall:
| Region | Examples (from `flagged_passages.md`) | Nature of the text |
|---|---|---|
| Abstract, second half | The certificate and audit numbers; the "results are mixed… guarded ArcFace accepts 89.45%…" sentences | Interpretive summary |
| Introduction | The opening motivation (passport photograph, credential renewal, forensic examiner); "We do not claim…"; the paper-organization paragraph | Framing and boilerplate |
| Related work | Synthesis paragraphs on aging generators, calibration, reject option and risk control, error-rate estimation | Literature synthesis |
| Table I and III text | Component-positioning phrases | Positioning prose |
| Protocol and results | Chronology, workload, age-gap analysis | Interpretation of results |
| Discussion, limitations, conclusion | Most of these sections | Interpretation and hedging |

Tables of numbers, equations and the reference list are largely unflagged.
**Pattern:** the flags sit on the prose that explains, frames and hedges, which is exactly the prose an assistant wrote.

## 3. Real attribution and accuracy problems (found by reading, independent of any detector)
| # | Where | Problem | Fix |
|---|---|---|---|
| A1 | AAFV-04 abstract ("We show that this rule gives a distribution-free, finite-sample FAR certificate") and contribution 1 | Reads as a new result. The argument is the standard order-statistic/conformal one (Vovk et al. 2005; Hanley & Lippman-Hand 1983; Clopper–Pearson). §II-E already says "we use these results rather than claim them", but the abstract and contribution list contradict it | Attribute in the same sentence ("Following standard order-statistic arguments [..]…"). In the CVPR paper the certificate is a supporting statement only (Phase 4) |
| A2 | AAFV-04 §V-C, R_sam / branch masking | The reliability-weighted auxiliary channel follows Poh et al. (2009); this is cited only in related work | Cite at the point of use. Moot if R_sam is removed (Phase 4) |
| A3 | AAFV-01 (historical) | DAL expanded as "Attention-guided Latent identity representation". DAL is *Decorrelated Adversarial Learning* (Wang et al., CVPR 2019) | Already corrected in AAFV-04; record it in the changelog as a past error |
| A4 | AAFV-04 §II-A on AIM and OrdCon | **Checked against the PDFs, correct.** AIM has a 25-volunteer user study, the CAFR benchmark (1,446,500 images, 25,000 subjects), and IJB-C/CACD/FG-NET evaluation. OrdCon covers MORPH II, FG-NET and AgeDB with cross-dataset experiments and concedes some homogeneous results | None. Keep, and cite page or section when quoting |
| A5 | AAFV-04 §I, "These works … do not address how a deployed system should choose its operating points" | An interpretive claim about the whole AIFR literature | Phrase it as the authors' reading ("none of the methods we reviewed reports …"), backed by the Phase 5 table |
| A6 | Dataset statistics | Sources disagree: AgeDB is 16,488 images / 568 subjects (Moschoglou et al., as summarised) vs 16,516 / 570 (OrdCon §IV). MORPH sizes are quoted from the AAFV pipeline | Quote the dataset paper's own numbers and state the count *used* after filtering |
| A7 | AAFV-04 bibliography | Several entries are not used for any claim in a CVPR framing: deepfake detection, biometric indexing, template inversion, privacy funnel, strategic evasion. They look like padding | Remove any reference the text does not genuinely use (Phase 5 §11). Never remove one the text relies on |
| A8 | `comprehensive_context.md` | "55% similarity index" is wrong (Section 1 above) | Correct the record |

No passage was found that reproduces a published source. That cannot be confirmed without a similarity check (Section 5).

## 4. Legitimate technical phrasing (no action needed)
Standard terms and formula statements are expected to recur across papers and are not an originality problem. Examples: "three-way decision", "reject option", "selective classification", "false-accept rate", "person-disjoint", "Clopper–Pearson", "Platt scaling", "exchangeability", the zero-failure bound 1 − δ^{1/n}, and dataset descriptions such as "1,002 images of 82 persons".

## 5. What the authors should do
1. **Run a Turnitin *similarity* report** (or iThenticate, which IEEE and CVF venues commonly use) on the next draft. It is the only way to check text overlap. The AI-writing score cannot answer that question.
2. **Write the new paper's prose yourselves.** The CVPR manuscript describes a different method (Phase 4), so almost no AAFV-04 prose should survive anyway.
   - Each author drafts the sections they understand best, from the evidence files (`log_analyses/`, `architecture_review/`, experiment outputs).
   - Assistants may check grammar, consistency and numbers, but should not generate the explanatory text.
   - The aim is a paper whose reasoning the authors can defend in a rebuttal, not a lower detector score.
3. **Disclose AI assistance** exactly as the target venue requires (Phase 8 §1 records the CVPR 2027 policy as far as it could be checked).
4. **Do not paraphrase to dodge the detector.** Do not remove citations to change a score. Do not use "humanizer" tools. All of these would themselves be misconduct risks.
5. **Fix A1–A8** in the first author-written draft.
6. **Keep a short provenance note** in the repository recording which sections were drafted by whom and where assistants were used. It answers questions from the advisor or institution directly.
