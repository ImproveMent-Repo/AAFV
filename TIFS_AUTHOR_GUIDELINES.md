# Official Author Guidelines Audit: IEEE Transactions on Information Forensics and Security (TIFS)

**Prepared For:** Alignment of *AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate*  
**Target Venue:** *IEEE Transactions on Information Forensics and Security* (TIFS), published by the IEEE Signal Processing Society (SPS) (`punumber=10206`)  
**Audited Manuscript Baseline:** `AAFV-02.pdf` and [`publication/main.tex`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/main.tex)  
**Stage:** Phase 1 Deliverable (`Prompt-2.md`)  
**Date:** November 12, 2026

---

## 1. Authoritative Sources Consulted

All requirements in this report were investigated against authoritative IEEE Signal Processing Society (SPS), IEEE Xplore, and IEEE Author Center resources:

1. **IEEE Signal Processing Society — TIFS Publication Portal:**  
   `https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security`
2. **IEEE Xplore — TIFS Journal Homepage (`punumber=10206`):**  
   `https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206`
3. **IEEE Signal Processing Society — Publications & Resources / Information for Authors:**  
   `https://signalprocessingsociety.org/publications-resources`
4. **IEEE Signal Processing Society — Unified EDICS Classification:**  
   `https://signalprocessingsociety.org/publications-resources/unified-edics`
5. **IEEE Author Center — Authoring Tools, Templates, Graphics, ORCID, & Policies:**  
   `https://ieeeauthorcenter.ieee.org/`

> [!NOTE]
> **Disclosure on Portal Access & Unverified Live Items:** Direct authenticated login to the TIFS ScholarOne / IEEE Author Portal manuscript submission wizard and the downloadable Unified EDICS Excel file were not accessed in this offline environment. Where SPS policy schedules or portal UI constraints cannot be verified without active submission credentials (e.g., whether the 2026 fee schedule remains exactly \$220 USD/page or has been indexed, exact current EDICS string codes, and whether the optional single-column review PDF slot is enforced in the submission form), these items are explicitly flagged in **Section 6** for manual confirmation before submission.

---

## 2. Executive Summary of Critical Misalignments Found

Auditing [`publication/main.tex`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/publication/main.tex) and [`AAFV-02.pdf`](file:///c:/Users/piyus/New%20Volumne%20(P)/7Th/Project/AAFV-02.pdf) against official TIFS/SPS rules identified **six immediate structural and compliance misalignments**:

1. **Wrong IEEEtran Class Option (`compsoc` vs. SPS `journal`):** Line 1 of `publication/main.tex` currently specifies `\documentclass[10pt,journal,compsoc]{IEEEtran}`, which applies **IEEE Computer Society** typography (Palatino body fonts, sans-serif Helvetica headings, `\IEEEtitleabstractindextext`, and non-standard citation styling). TIFS is published by the **IEEE Signal Processing Society**, not the Computer Society, and uses standard `\documentclass[journal]{IEEEtran}` (Times Roman, 10-pt two-column).
2. **Abstract Overlength & Prohibited Inline LaTeX Math:** The current abstract contains **~259–273 words** (exceeding the 150–250 word IEEE/TIFS limit) and embeds inline equations and set notation (`$\{\text{Auto-Accept}, \dots\}$`, `$N=1{,}149$`, `$\text{FAR} \le 0.320\%$`, `$\beta=1.0\%$`), violating IEEE plain-text abstracting rules.
3. **Incomplete Author Metadata, Placeholders, & Missing ORCID:** The author block contains placeholders (`and~Collaborators`, generic `Department of Computer Science and Engineering` without university/city/country, placeholder email `contact@anuragnayak.dev`), lacks mandatory **ORCID** iDs, and lacks a bio/photo plan for the final stage.
4. **Loading Incompatible `caption` Package & Unreferenced Figures:** `publication/main.tex` loads `\usepackage{caption}` (triggering an `IEEEtran` compiler warning overriding IEEE caption formatting), and **5 of 7 figures** (`fig:architecture`, `fig:results`, `fig:outcomes`, `fig:gap_neutral`, `fig:beta_sweep`) are never referenced via `\ref{}` in the manuscript text.
5. **Missing Mandatory Declarations & TIFS Deep Learning Reproducibility Details:** The manuscript lacks dedicated **Funding**, **Conflict of Interest**, **Human Subjects / Biometric Data Ethics**, **AI-Tool Disclosure**, and explicit **TIFS Guidelines for Deep Learning Submissions** training details (optimizer, LR schedule, batch size, initialization, exact gap-balanced weighting formula).
6. **Page Budget Tightness Under Class Transition:** Currently `AAFV-02.pdf` is exactly **10 pages** under `compsoc`. Switching to standard SPS `\documentclass[journal]{IEEEtran}`, adding missing literature comparisons, Deep Learning reproducibility details, and required declarations will alter pagination—remaining well within the **13-page initial submission limit**, but potentially entering the **11–16 page overlength-charge bracket** at camera-ready unless carefully budgeted.

---

## 3. Detailed Investigation of Official TIFS Requirements

### A. Manuscript Categories & Formatting Requirements

| Aspect | Official TIFS / IEEE SPS Requirement | Source Reference |
|---|---|---|
| **Journal Scope** | Information forensics, watermarking, cryptography, information security, **biometrics**, surveillance, and integrated forensic/security systems. **Single-blind peer review** (authors' names and affiliations remain visible to reviewers). | [SPS TIFS Portal](https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security); [SPS Reviewing Policy](https://signalprocessingsociety.org/publications-resources) |
| **Manuscript Categories** | 1. **Regular Papers:** Complete disclosure of original technical research.<br>2. **Overview Articles:** Authoritative survey/tutorial articles; require prior submission and Editor-in-Chief approval of a **2-page white-paper proposal**.<br>3. **Comment Correspondences:** Concise commentary on previously published papers (strictly **$\le 2$ pages**, 9-pt or 10-pt double-column). | [SPS Information for Authors](https://signalprocessingsociety.org/publications-resources) |
| **Initial Submission Format** | Single PDF compiled in **IEEE standard double-column, single-spaced format** using $\ge 10$-pt Times Roman type and $\ge 1$-inch margins (`\documentclass[journal]{IEEEtran}`). Authors may optionally/are encouraged in some SPS portals to also upload a **single-column, double-spaced PDF (11-pt+)** for reviewer readability, though page limits are governed strictly by the double-column version. | [SPS Information for Authors](https://signalprocessingsociety.org/publications-resources); [IEEE Author Center](https://ieeeauthorcenter.ieee.org/) |
| **Revised Submission Format** | Updated double-column PDF (matching initial template rules up to the revision ceiling), accompanied by a point-by-point Response to Reviewers and marked/highlighted manuscript changes. | [SPS Information for Authors](https://signalprocessingsociety.org/publications-resources) |
| **Final Camera-Ready Format** | Editable LaTeX source (`IEEEtran.cls` without `compsoc`), individual vector/high-DPI graphic files, verified BibTeX/bibliography, and **author biographies with portraits** ($1'' \times 1.25''$ grayscale/color). | [IEEE Author Center](https://ieeeauthorcenter.ieee.org/); [SPS Information for Authors](https://signalprocessingsociety.org/publications-resources) |
| **Font & Template Rules** | Standard `IEEEtran.cls` (`journal` mode; **no `compsoc`**). Body text 10-pt Times Roman; captions formatted natively by `IEEEtran` (do **not** load `\usepackage{caption}`). | [IEEE Author Center Templates](https://ieeeauthorcenter.ieee.org/) |
| **Abstract Requirements** | **Single paragraph**, **150–250 words** (aim for $\le 200$ words to ensure safe compliance across all ScholarOne/SPS portal bounds). Self-contained plain text: **no equations, math symbols, undefined acronyms, footnotes, tables, or bibliographic citations**. | [SPS Information for Authors](https://signalprocessingsociety.org/publications-resources); [IEEE Author Center](https://ieeeauthorcenter.ieee.org/) |
| **Index Terms** | Mandatory immediately following the abstract (`\begin{IEEEkeywords}`), sorted in **alphabetical order**, drawn from IEEE Taxonomy / Unified EDICS keywords. | [IEEE Author Center](https://ieeeauthorcenter.ieee.org/) |
| **Mathematical Notation** | Italic scalar variables, bold upright vectors/matrices, numbered equations punctuated grammatically as part of prose, and every symbol formally defined before or upon first appearance. | [IEEE Author Center](https://ieeeauthorcenter.ieee.org/) |
| **Figures & Tables** | **Vector PDF/EPS/PS preferred** (fonts embedded); raster color/grayscale $>300$ dpi; monochrome line art $>600$ dpi. No GIF/BMP/low-res JPEG. Figure captions **below** figure (`Fig. 1.`); Table titles **above** table using Roman numerals (`TABLE I`). Column widths: 3.5 in (1-col) or 7.16 in (2-col). Every figure/table must be explicitly cited in text. | [IEEE Author Center Graphics Guide](https://ieeeauthorcenter.ieee.org/) |
| **Reference Formatting** | IEEE numbered bracket style (`[1]`), generated via `\bibliographystyle{IEEEtran}`. Standard IEEE journal/conference abbreviations, full author list (use *et al.* only when $>6$ authors per IEEE style), complete year, volume, pages, and verified DOIs. | [IEEE Author Center](https://ieeeauthorcenter.ieee.org/) |
| **Supplementary Material & DL Guidelines** | External supplementary archives (code, extended proofs, datasets, audio/video multimedia) hosted separately on IEEE Xplore / repository. Must stay concise. TIFS **Guidelines for Deep Learning Submissions** mandate written specification of topology, layers, activations, normalization formulas, initialization, optimizer, LR schedule, batch size, and split stratification inside the paper itself. | [SPS TIFS Portal](https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security); [SPS Reproducible Research](https://signalprocessingsociety.org/publications-resources) |

---

### B. Page Limits and Overlength Charge Rules (Regular Papers)

| Page Limit Dimension | Official TIFS / IEEE SPS Rule | Implications for `AAFV-Net` (`AAFV-02.pdf`) |
|---|---|---|
| **Initial Submission Page Limit** | **Maximum 13 pages** (double-column, single-spaced, 10-pt font). Initial submissions exceeding 13 pages are returned without review. | Current `AAFV-02.pdf` is **10 pages** (under `compsoc`). Switching to standard `journal` mode plus adding literature, DL reproducibility specs, and declarations gives up to **3 pages of safe headroom** at initial submission. |
| **Do References Count Toward Limits?** | **YES.** Title, author names/affiliations, abstract, main text, all figures/tables, appendices, and **all references** count toward every page limit (13 initial, 16 revision, 10 free). | Adding verified TIFS references (~10–15 citations) directly impacts total page count and must be budgeted carefully. |
| **Do Appendices Count Toward Limits?** | **YES.** Appendices and mathematical proofs included in the main PDF count toward the 13-page initial, 16-page revision, and 10-page fee-free limits. | Current Appendix A (`Table IX` CIs) counts inside the main PDF page budget. Moving bulky secondary logs to external `supplementary/` saves space if needed. |
| **Supplementary Material Treatment** | **Excluded from page count.** External supplementary PDFs, code capsules, and multimedia files submitted as supporting files do not count against the 13/10/16-page caps, though excessive supplementary text may trigger editorial screening. | Code repository (`AAFV_Net`), frozen artifact checksums, and extended experimental audit tables can reside in external supplementary materials if camera-ready length exceeds 10 pages. |
| **Complimentary (Fee-Free) Limit** | **10 published pages** double-column (no overlength charge). | If we target zero publication cost at final acceptance, final camera-ready PDF **including author biographies/photos** should not exceed **10 pages**. |
| **Mandatory Overlength Charges** | Mandatory, non-negotiable charge for every published page beyond page 10 (archived SPS rate: **$220 USD per excess page**; applies equally to hybrid Open Access papers). *(Confirm exact 2026 fee on portal at acceptance.)* | Pages 11–16 carry \$220/page charges upon acceptance. |
| **Revision & Final Maximum Ceiling** | During peer review revisions, papers may expand up to **16 double-column pages**. Manuscripts exceeding 16 pages in final form cannot be published until shortened. | Provides essential room to answer reviewer comments in Round 1/2 without editorial desk rejection. |
| **Initial vs. Final Differences** | Initial submission omits/makes optional author biographies and portrait photos (13-page max). Final accepted submission **must include author biographies & photos** ($1'' \times 1.25''$), which occupy ~0.3–0.6 pages inside the final page count (10 free / 16 hard cap). | Switching to 10 pages at initial submission leaves **no room for biographies** unless 0.5 pages are trimmed or overlength charge is accepted at camera-ready. |

---

### C. Submission, Authorship, Ethics, and Disclosure Declarations

1. **Author Metadata & Affiliations:** Full names, valid institutional affiliations (Department, Institution, City, State/Country), and institutional emails for all co-authors. Single-blind reviewing requires real identity metadata on the manuscript.
2. **ORCID Mandate:** Mandatory **ORCID iD** for **every listed author** linked in the IEEE Author Portal / ScholarOne Manuscripts prior to final submission and recommended in the LaTeX author block via `\orcidlink`.
3. **Author Contribution Criteria (IEEE Three-Part Test):** All named authors must satisfy intellectual conception/design, drafting/critical revision, and final approval. Contributors not meeting all three criteria belong in Acknowledgments.
4. **Conflict of Interest (COI) & Funding Disclosures:** Explicit declaration of grants/funding support and financial/non-financial conflicts of interest (required both in ScholarOne metadata and recommended in the Acknowledgments section).
5. **Reproducible Research & Data/Code Availability:** Strong TIFS policy requiring clear data/code availability statements detailing access conditions (e.g., licensed MORPH academic access via UNCW/Cranfield vs. open GitHub code release `github.com/anuragnayak01/AAFV_Net`).
6. **Ethical & Biometric Privacy Compliance:** Research using human facial datasets (MORPH, FG-NET) requires an explicit Ethics / Human-Subjects Compliance statement confirming secondary use of established, access-controlled/publicly documented biometric benchmarks, non-collection of new subjects, privacy safeguards, and explicit pediatric deployment exclusions ($a < 16$).
7. **Plagiarism & Originality (CrossCheck / iThenticate):** Strict originality screening; any overlap with preprints, theses, or prior conference papers must be disclosed and cited cleanly.
8. **IEEE PSPB Generative AI / LLM Disclosure:** Authors assume 100% accuracy and ownership responsibility; any AI-assisted text/figure/code generation beyond standard copyediting/grammar checking must be transparently declared in Acknowledgments.
9. **Unified EDICS Classification:** Submission requires selecting appropriate Unified SPS EDICS category codes (e.g., Information Forensics & Security — Biometrics).

---

## 4. TIFS Guidelines Compliance Matrix

| Requirement | Official TIFS / IEEE SPS Requirement | Current Manuscript Status (`publication/main.tex` & `AAFV-02.pdf`) | Required Correction |
|---|---|---|---|
| **Document Class Option** | `\documentclass[journal]{IEEEtran}` (SPS Times Roman 10-pt two-column; no `compsoc`). | Uses `\documentclass[10pt,journal,compsoc]{IEEEtran}` (Computer Society Palatino/Helvetica style). | Switch to `\documentclass[journal]{IEEEtran}`, remove `\IEEEtitleabstractindextext` / `\IEEEdisplaynontitleabstractindextext`, use standard `\maketitle`. |
| **Caption Package Conflict** | Use native `IEEEtran` caption handler (`Fig. 1.` below figures; `TABLE I` above tables). | Loads `\usepackage{caption}`, causing compiler warning and overriding IEEE spacing. | Remove `\usepackage{caption}` from preamble; verify native `IEEEtran` formatting. |
| **Initial Submission Page Limit** | $\le 13$ double-column pages (including title, abstract, text, figures, tables, appendices, references). | Currently **10 pages** (under `compsoc`). | Re-measure exact length after removing `compsoc`; keep strictly $\le 13$ pages (target **10–12 pages** at initial submission; prepare trimming plan to $\le 10$ if avoiding overlength charges). |
| **Free Page Limit & Overlength Fee** | $\le 10$ published pages free (including author bios/photos); pages 11–16 incur \$220/page fee; $>16$ prohibited. | Currently **10 pages without bios/photos**. | Account for ~0.5 page bio/photo footprint in final submission budget; decide whether to keep camera-ready $\le 10$ pages or pay overlength fees. |
| **Abstract Word Limit & Content** | Single paragraph, **150–250 words** (ideally $\le 200$); **no math symbols, equations, or citations**. | **~259–273 words**; contains inline LaTeX math (`$\{\text{Auto-Accept} \dots\}$`, `$\text{FAR} \le 0.320\%$`, `$\beta=1.0\%$`). | Rewrite abstract to **180–210 words** in crisp plain prose without `$...$` LaTeX math delimiters or symbols. |
| **Index Terms** | Alphabetically ordered IEEE taxonomy keywords (`\begin{IEEEkeywords}`). | Present (7 terms), **not alphabetically ordered**. | Sort terms alphabetically and align with IEEE Taxonomy / Unified EDICS Biometrics terms. |
| **Author Metadata & Placeholders** | Real names, complete institutional affiliations (Univ., City, Country), verified emails; single-blind review. | Contains placeholders: `and~Collaborators`, incomplete affiliation (`Department of Computer Science and Engineering`), placeholder email `contact@anuragnayak.dev`. | Flag author placeholders for user completion prior to submission; retain non-fabricated markers `[CO-AUTHOR NAMES / INSTITUTIONAL AFFILIATION NEEDED]` or clear instructions in revision roadmap. |
| **ORCID Integration** | Mandatory for all co-authors on portal and recommended in LaTeX header. | Missing entirely. | Add `\usepackage{orcidlink}` support with documented placeholder slots for authors to populate real ORCIDs. |
| **Deep Learning Reproducibility (TIFS)** | Mandatory written description of normalization, initialization, optimizer, LR schedule, batch size, weighting formula. | MLP width (`11->32->16->1`), dropout (`0.10`), 5 seeds, and "gap-balanced weighted BCE" named, but **optimizer, LR, epochs, exact normalization, and weight formula missing**. | Verify exact code implementation in `scripts/p6_train.py` and `p78_calibrate_freeze.py` (in Phase 5/7) and document every hyperparameter in Methodology. |
| **Figure & Table Citations** | Every figure and table must be explicitly referenced via `\ref{}` in sequential order. | **5 of 7 figures** (`fig:architecture`, `fig:results`, `fig:outcomes`, `fig:gap_neutral`, `fig:beta_sweep`) have **0 in-text citations**. | Add explicit `\ref{}` references and contextual analysis for every figure and table in text. |
| **Figure Resolution & Formats** | Vector PDF/EPS recommended (embedded fonts) or $>300$ dpi / $>600$ dpi raster. | All 7 figures generated as vector `.pdf` in `publication/figures/`. | Verify font embedding (`pdffonts`) and ensure figure labels match TIFS style (e.g., Fig. 1, bold titles, consistent fonts). |
| **References Style** | `\bibliographystyle{IEEEtran}` with standard IEEE abbreviations and DOIs. | Uses `IEEEtran.bst`, but `references.bib` uses un-abbreviated conference/journal titles (`Proceedings of...`). | Standardize `references.bib` venues to official IEEE abbreviations (`Proc.`, `IEEE Trans. Inf. Forensics Security`, etc.) and integrate relevant TIFS papers. |
| **Acknowledgment, COI, Funding & Ethics** | Explicit COI, Funding, Ethics/IRB (human biometric data), and AI-Tool Disclosure statements. | Absent from `publication/main.tex`. | Add dedicated **Ethical & Privacy Considerations** subsection/paragraph and formal **Acknowledgment / Funding / COI / Reproducibility** subsection. |
| **Author Biographies & Photos** | Required at final acceptance ($1'' \times 1.25''$); omitted/optional at initial submission. | Absent from `publication/main.tex`. | Prepare commented `\begin{IEEEbiography}` templates ready for final acceptance stage without consuming initial-submission space prematurely. |

---

## 5. Verification Status & Open Questions Requiring Manual Confirmation

Per the Phase 1 execution rules, the following items remain **unverified without live authenticated portal access** and must be confirmed directly by the submitting author inside the TIFS IEEE Author Portal / ScholarOne form prior to clicking *Submit*:

1. **Exact 2026 Overlength Fee Rate:** Archived SPS policy specifies **$220 USD per published page** beyond page 10. Confirm on the TIFS ScholarOne fee acknowledgment screen whether the 2026 fee remains \$220/page or has been adjusted.
2. **Optional Single-Column Upload Requirement:** While SPS policy states initial submissions are evaluated in double-column 10-pt format (13-page max), some SPS journal submission wizards ask for a second double-spaced single-column PDF for reviewer convenience. Confirm whether the TIFS IEEE Author Portal displays a dual-PDF upload requirement during initial submission.
3. **Live Portal Abstract Character/Word Hard Cap:** ScholarOne submission boxes sometimes impose a strict character limit (e.g., 1,500–2,000 characters or 200 words) separate from the PDF text. Keeping our revised abstract between **180–200 words** guarantees compliance across both the PDF and web form.
4. **Exact Unified EDICS Code Selection:** Download the latest Excel table at `https://signalprocessingsociety.org/publications-resources/unified-edics` during submission to select the exact 2026 EDICS descriptor codes under Biometrics / Forensic Authentication.
5. **Co-Author Details, ORCID iDs, Funding Grant Numbers, & AI Disclosure Status:** Confirm exact co-author names, institutional affiliations (University, City, Country), ORCID identifiers, funding grants, and whether any LLM assistance requires disclosure under IEEE PSPB rules.

---

**Phase 1 Status:** **COMPLETE.** Ready to proceed to **Phase 2 — Study Published TIFS Papers** (`TIFS_LITERATURE_AND_STYLE_ANALYSIS.md`).

