# MASTER RESEARCH PROMPT — AAFV-Net IEEE Publication Preparation

## 1. Your Role

Act as a senior research scientist, IEEE journal reviewer, machine-learning researcher, biometric-system specialist, statistical auditor, and LaTeX publication engineer.

You are assisting me in preparing a technically rigorous, reproducible research paper based on **AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate**.

Your objective is not merely to improve grammar or formatting. Your objective is to determine whether the research, methodology, experimental evidence, statistical claims, and contributions are sufficiently rigorous for submission to an appropriate IEEE publication venue.

Be critical. Treat this as a paper being evaluated by demanding reviewers.

Do not praise weak methodology. Identify weaknesses, explain why they matter, and propose technically defensible solutions.

---

## 2. Research Materials and Sources

You have access to the following materials.

### A. GitHub repository

Repository:
https://github.com/anuragnayak01/AAFV_Net

This repository contains the actual implementation, configurations, scripts, experimental pipeline, evaluation procedures, and potentially additional results.

You MUST inspect the repository thoroughly.

Examine:
- README.md
- src/
- scripts/
- configs/
- tests/
- ablations/
- baselines/
- audit/
- q/
- docs/
- Available results and experiment artifacts.

Understand the actual implementation before making claims about the methodology.

Do not assume the README accurately describes every implementation detail. Verify important claims against the source code.

### B. Existing manuscripts

1. `Initial_Paper-AAFV_Net.pdf`
   - Existing AAFV-Net manuscript.
   - Use it to understand the current research narrative and reported findings.

2. `paper.tex`
   - Existing LaTeX source.
   - Treat this as the editable manuscript, but independently verify its claims.

3. `BASE_Paper.pdf`
   - An additional manuscript/reference.
   - Investigate its relationship to AAFV-Net.
   - Do not automatically merge its methodology, contributions, results, or references into AAFV-Net.
   - Only reuse relevant material when technically justified and properly attributed.

### C. Experimental CSV files

Inspect every column, row, data type, missing value, and relevant experimental configuration in:

- ablation_calibration.csv
- decision_table_calibration.csv
- extended_calibration.csv
- extended_calibration_fg.csv
- extended_calibration_fg16.csv
- extended_test.csv
- gap_report_calibration.csv

### D. Existing visualization code

- `p11_figures.py`

Inspect this script, understand the figures it generates, and determine whether additional visualizations or corrections are required.

### E. Previous research discussion

Claude conversation:
https://claude.ai/share/ee314c24-80a1-451a-9a27-3cfc8b1f33af

Attempt to retrieve and examine this discussion if accessible.

If access is blocked, explicitly report that limitation and request an exported Markdown/text transcript. Do not pretend to have read it.

The previous discussion may contain research decisions, design rationale, implementation details, and experimental context that are absent from the current manuscript.

---

## 3. Absolute Research Integrity Rules

These rules are mandatory.

1. NEVER fabricate experimental results, numerical values, citations, datasets, experiments, or methodological details.

2. NEVER infer an experimental result simply because it would strengthen the paper.

3. Every numerical claim must be traceable to:
   - An experimental CSV;
   - A reproducible computation;
   - A repository artifact;
   - Or a clearly identified external source.

4. Distinguish between:
   - Measured results;
   - Calculated statistics;
   - Literature-reported results;
   - Hypotheses;
   - Proposed future experiments.

5. If a result is missing, label it MISSING.

6. If two sources disagree, identify the discrepancy and investigate its cause. Do not silently choose whichever number looks better.

7. Do not modify the original experimental CSVs or frozen thresholds.

8. Do not run experiments that consume a protected test-set access without first examining the audit protocol and obtaining explicit approval.

9. Preserve the existing experimental evidence, including negative results and limitations.

10. Never claim that the work is IEEE-compliant, novel, statistically significant, or publication-ready without supporting evidence.

11. Do not remove inconvenient results merely to improve the paper's presentation.

12. Preserve data privacy, dataset licensing requirements, and appropriate biometric research ethics.

---

# PHASE 1 — COMPLETE RESEARCH AUDIT

Do not rewrite the paper yet.

First, understand the complete research project.

## Task 1.1: Understand the methodology

Reconstruct the complete AAFV-Net architecture from the source code.

Investigate:

- Input preprocessing and face alignment.
- Image-quality assessment.
- Age estimation and age-gap categorization.
- SAM-based age transformation.
- Forward and backward age transformation.
- Shared target-age generation.
- ArcFace similarity.
- EfficientNet similarity.
- VGG similarity.
- LPIPS.
- SSIM.
- Branch-specific linear learners.
- Fusion MLP architecture.
- Context features.
- Reliability estimation.
- Branch masking.
- Platt calibration.
- Quality and reliability guards.
- Accept and reject thresholds.
- Three-way decision mechanism.
- Test-access restrictions and audit logging.

For every component, document:
- Its purpose.
- Mathematical formulation.
- Input and output.
- Implementation location.
- Hyperparameters.
- Training or inference behaviour.

Identify discrepancies between the mathematical description, paper, README, and actual code.

## Task 1.2: Reconstruct the experimental protocol

Investigate:

- Dataset composition.
- Identity-level splitting.
- Train, calibration, and test separation.
- Duplicate identity handling.
- Quarantined identities.
- Genuine pair generation.
- Impostor pair generation.
- Hard-negative mining.
- Neutral impostor generation.
- Age-gap categories.
- Random seeds.
- Model training procedures.
- Threshold selection.
- Test-access history.

Pay particular attention to possible identity leakage.

Verify that identities do not cross the training, calibration, and test boundaries.

Determine whether the reported evaluation genuinely supports the claim of person-disjoint generalization.

## Task 1.3: Build a source-of-truth matrix

Create a table with:

| Claim or parameter | Manuscript | Source code | CSV/artifact | Verified status |
|---|---|---|---|---|

Include all major architectural and experimental claims.

Use these statuses:

- VERIFIED
- PARTIALLY VERIFIED
- CONFLICTING
- UNVERIFIED
- MISSING

Every conflict must have an explanation and a recommended resolution.

---

# PHASE 2 — EXPERIMENTAL RESULTS AND STATISTICAL AUDIT

This is one of the most important phases.

Do not simply copy numbers from existing tables.

Independently calculate and verify the reported results.

## Task 2.1: Analyze all CSV files

For each CSV:

1. Identify its purpose.
2. Explain its columns.
3. Identify the experimental split.
4. Identify the model variants.
5. Identify missing or invalid values.
6. Check for duplicated observations.
7. Verify the reported metrics.
8. Identify results that could be used in the paper.
9. Identify results that require additional experimentation.

Generate a consolidated experimental-results report.

## Task 2.2: Verify the main results

Investigate the following reported MORPH test results for the full model at beta = 1%:

- Same-person auto-acceptance: approximately 70.07%.
- Random impostor false accepts: 0/1,149.
- Larger random impostor pool false accepts: 0/277,822.
- Hard-impostor false accepts: 5/35,735.
- Hard-impostor rejection: approximately 98.04%.

Verify every value independently.

Do not confuse zero false accepts on random impostors with zero false accepts on hard impostors.

## Task 2.3: Investigate external evaluation

Examine the FG-NET results carefully.

Distinguish between:

- All-age FG-NET evaluation.
- Adult-only FG-NET evaluation.
- Different age-gap categories.
- Random impostor evaluation.
- Any additional restricted evaluation subsets.

In particular, investigate the distinction between `extended_calibration_fg.csv` and `extended_calibration_fg16.csv`.

Explain why their pair counts and performance differ.

Do not report adult-only results as results on the complete FG-NET dataset.

## Task 2.4: Statistical validation

Independently investigate:

- FAR.
- FRR.
- TAR.
- TPR.
- FPR.
- ROC-AUC.
- EER.
- Confidence intervals.
- Cluster-bootstrap intervals.
- Neyman-Pearson operating points.
- Statistical upper bounds under zero observed false accepts.
- Calibration uncertainty.
- Test-set sampling uncertainty.

Verify the formula:

FAR upper bound = 1 - alpha^(1/N)

Examine whether the confidence level and alpha adjustment correctly account for the number of test-set accesses.

Determine whether the reported confidence bounds are justified by the actual sampling procedure.

Investigate whether pair-level independence assumptions are appropriate when multiple pairs share identities.

Where appropriate, recommend identity-clustered statistical analysis.

## Task 2.5: Ablation analysis

Investigate every available ablation.

Determine:

- Which components are genuinely necessary.
- Which components improve genuine-pair acceptance.
- Which components improve hard-impostor rejection.
- Which components improve calibration.
- Which components introduce additional complexity without measurable benefit.

Pay special attention to:

- Removing ArcFace.
- Removing LPIPS.
- Removing SSIM.
- Removing reliability inputs.
- Removing context inputs.
- Removing branch masking.
- Removing shared targets.
- Forward-only transformation.
- Direct-only architecture.
- SAM-only architecture.
- Removing guards.
- Alternative fusion strategies.

Do not describe an ablation as an improvement based on only one metric.

Evaluate the trade-off between genuine acceptance, false acceptance, manual-review rate, and hard-negative rejection.

---

# PHASE 3 — IDENTIFY WHAT IS MISSING

Act as an IEEE reviewer evaluating the current manuscript.

Identify everything preventing this work from becoming a strong research submission.

Organize findings into four categories.

### A. Critical deficiencies

Issues that could result in rejection.

Examples:
- Unsupported novelty claims.
- Experimental leakage.
- Incorrect statistical interpretation.
- Missing methodological details.
- Invalid comparisons.
- Insufficient external validation.
- Inadequate reproducibility.

### B. Major deficiencies

Issues that substantially weaken the contribution.

Examples:
- Missing baseline comparisons.
- Insufficient ablation studies.
- Weak generalization analysis.
- Inadequate confidence intervals.
- Missing sensitivity analysis.

### C. Minor deficiencies

Examples:
- Missing equations.
- Unclear figures.
- Poor table organization.
- Incomplete references.
- Inconsistent terminology.

### D. Publication improvements

Examples:
- Better architecture diagrams.
- Improved mathematical explanations.
- More informative plots.
- Stronger discussion.
- Better experimental presentation.

For every identified issue, provide:

| Issue | Why it matters | Required evidence | How to obtain it | Priority |
|---|---|---|---|---|

Do not suggest unnecessary experiments simply to increase the number of pages.

Prioritize experiments that materially strengthen the scientific contribution.

---

# PHASE 4 — LITERATURE REVIEW AND NOVELTY VALIDATION

Conduct a proper literature investigation.

Research relevant work in:

- Age-invariant face recognition.
- Cross-age face verification.
- Generative age progression and regression.
- SAM and StyleGAN-based face synthesis.
- Face-recognition embeddings.
- Multi-model score fusion.
- Selective classification and reject-option systems.
- Neyman-Pearson decision theory.
- Biometric false-accept guarantees.
- Statistical confidence bounds.
- Open-set and hard-negative evaluation.

Use authoritative sources:

- IEEE Xplore.
- ACM Digital Library.
- Springer.
- Elsevier.
- CVF Open Access.
- arXiv, where appropriate.
- Official dataset and model publications.

For every important paper, record:

- Title.
- Authors.
- Publication venue.
- Year.
- DOI or verified URL.
- Methodology.
- Dataset.
- Evaluation protocol.
- Main findings.
- Limitations.
- Relationship to AAFV-Net.

## Novelty assessment

Determine exactly what is novel in AAFV-Net.

Separate:

1. Novel architecture.
2. Novel combination of existing components.
3. Novel decision mechanism.
4. Novel experimental protocol.
5. Novel statistical evaluation.
6. Engineering or implementation contribution.

Do not claim that combining existing models is automatically a novel algorithm.

Compare the work against the closest existing approaches.

Prepare a comparison matrix showing the differences.

Identify whether the contribution is sufficiently strong for an IEEE journal or whether a conference/workshop would be a more realistic target.

Do not invent a publication venue or imply acceptance is guaranteed.

---

# PHASE 5 — RECOMMEND ADDITIONAL EXPERIMENTS

After the audit, prepare a prioritized experimental roadmap.

Consider experiments such as:

1. Cross-dataset generalization.
2. Additional age-gap-specific evaluation.
3. Sensitivity to the number of shared target ages.
4. Sensitivity to quality thresholds.
5. Sensitivity to reliability thresholds.
6. Sensitivity to the accept threshold.
7. Calibration robustness.
8. Alternative face-recognition backbones.
9. Comparison with stronger age-invariant recognition methods.
10. Computational cost and inference latency.
11. Memory requirements.
12. SAM transformation failure analysis.
13. Image-quality degradation analysis.
14. Demographic subgroup evaluation, where permitted by dataset documentation and sample sizes.
15. Manual-review workload analysis.
16. Robustness to missing or unavailable synthesis outputs.

For each experiment, provide:

- Research question.
- Hypothesis.
- Required data.
- Experimental procedure.
- Metrics.
- Expected scientific contribution.
- Estimated computational requirements.
- Whether existing code can support it.
- Whether additional implementation is required.
- Whether it requires protected test-set access.

Classify experiments:

- MUST PERFORM
- STRONGLY RECOMMENDED
- OPTIONAL
- NOT WORTH THE COMPUTATIONAL COST

Do not execute protected experiments without explicit approval.

If an experiment cannot be conducted, clearly identify the missing result and its implications.

---

# PHASE 6 — IEEE MANUSCRIPT RESTRUCTURING

Only after completing the research audit should you prepare a revised manuscript.

Use the appropriate IEEE publication template.

Prefer IEEEtran when suitable for the intended venue.

Do not assume every IEEE journal uses identical formatting or page limits.

Investigate the requirements of potential target venues before finalizing the formatting.

## Recommended paper structure

1. Title
2. Abstract
3. Index Terms
4. Introduction
5. Related Work
6. Problem Formulation
7. Proposed Methodology
8. Experimental Setup
9. Results and Comparative Evaluation
10. Ablation Studies
11. Statistical Reliability and Error Analysis
12. Discussion
13. Limitations
14. Conclusion
15. References

Adjust the structure according to the target venue's author guidelines.

## Writing requirements

- Use formal academic English.
- Avoid unnecessarily complicated sentences.
- Maintain technical precision.
- Avoid repetitive explanations.
- Use consistent mathematical notation.
- Define every symbol before or when it is used.
- Include equations where they improve methodological clarity.
- Explain the rationale behind design decisions.
- Distinguish training, calibration, and test procedures.
- Avoid unsupported superiority claims.
- Explain negative results.
- Discuss computational limitations.
- Clearly state the scope of the false-accept guarantee.

The manuscript must read like a coherent research contribution, not a collection of implementation details.

---

# PHASE 7 — FIGURES, TABLES, AND MATHEMATICAL PRESENTATION

Inspect all existing figures and tables.

Identify redundant, unclear, or scientifically weak visualizations.

Recommend a publication-quality figure set.

Potential figures:

1. Complete AAFV-Net architecture.
2. Direct and SAM-based evidence branches.
3. Three-way decision mechanism.
4. ROC curves.
5. FAR versus genuine acceptance.
6. Age-gap-wise performance.
7. Ablation comparison.
8. Calibration and threshold analysis.
9. Hard-negative rejection.
10. Failure-case visualization.
11. Computational-cost comparison.

Potential tables:

1. Dataset statistics.
2. Experimental configuration.
3. Main MORPH results.
4. FG-NET external evaluation.
5. Baseline comparison.
6. Ablation study.
7. Age-gap-specific results.
8. Confidence-bound analysis.
9. Computational complexity.

Every figure and table must have:

- Correctly computed values.
- Clear axis labels.
- Appropriate units.
- Meaningful captions.
- Consistent terminology.
- Appropriate references in the manuscript.

Do not generate decorative figures that add no scientific value.

Reuse and improve `p11_figures.py` where appropriate.

---

# PHASE 8 — LATEX IMPLEMENTATION

Work with the existing `paper.tex`, but preserve it as an original backup.

Create a separate publication-ready manuscript.

Suggested output:

publication/
    main.tex
    references.bib
    figures/
    tables/
    supplementary/
    README.md

Use IEEE-compatible LaTeX conventions.

Requirements:

- IEEEtran document class where appropriate.
- Correct citation and bibliography style.
- Proper equation numbering.
- Correct figure placement.
- Publication-quality tables.
- Consistent section numbering.
- No undefined references.
- No missing citations.
- No compilation warnings that materially affect publication.
- No broken image paths.

Compile the document and inspect the rendered PDF.

Check for:

- Overfull and underfull boxes.
- Figure overflow.
- Table overflow.
- Incorrect column breaks.
- Poor readability.
- Inconsistent spacing.
- Broken references.
- Incorrect bibliography formatting.

Do not merely generate LaTeX that looks correct in the source file. Verify the compiled document.

---

# PHASE 9 — FINAL REVIEW FROM THE PERSPECTIVE OF IEEE REVIEWERS

After preparing the revised manuscript, simulate three independent reviewers.

### Reviewer 1: Technical and methodological reviewer

Evaluate:
- Technical correctness.
- Methodological novelty.
- Architecture.
- Mathematical rigor.
- Experimental design.
- Reproducibility.

### Reviewer 2: Experimental and statistical reviewer

Evaluate:
- Dataset suitability.
- Statistical validity.
- Baseline fairness.
- Confidence intervals.
- Calibration.
- Generalization.
- False-accept claims.

### Reviewer 3: Critical IEEE journal reviewer

Evaluate:
- Research significance.
- Novelty.
- Related work.
- Presentation.
- Limitations.
- Scientific contribution.
- Publication suitability.

Each reviewer must provide:

- Strengths.
- Weaknesses.
- Major concerns.
- Minor concerns.
- Missing experiments.
- Specific revisions.
- Recommendation.

Use the following recommendation categories:

- Strong Accept
- Weak Accept
- Borderline
- Weak Reject
- Strong Reject

These are simulated assessments, not predictions of actual peer review.

Then produce a consolidated revision plan.

---

# PHASE 10 — FINAL DELIVERABLES

I expect the following deliverables.

### 1. Research audit

`research_audit.md`

Complete analysis of the methodology, code, datasets, and experimental results.

### 2. Results verification

`results_verification.md`

A consolidated record of all verified results, statistical calculations, inconsistencies, and missing values.

### 3. Missing experiments

`missing_experiments.md`

Prioritized experimental roadmap with implementation requirements.

### 4. Literature review

`literature_review.md`

Verified related work, comparison matrix, and novelty assessment.

### 5. Revised manuscript

`publication/main.tex`

Complete revised IEEE-compatible LaTeX manuscript.

### 6. References

`publication/references.bib`

Verified bibliographic references.

### 7. Figures and tables

Publication-quality figures and tables with reproducible generation scripts.

### 8. Final compiled paper

`publication/main.pdf`

Compiled and visually inspected manuscript.

### 9. Reviewer assessment

`reviewer_assessment.md`

Three independent simulated reviewer reports and a consolidated revision plan.

### 10. Reproducibility documentation

`publication/README.md`

Instructions for reproducing the reported experiments, generating figures, and compiling the paper.

---

# EXECUTION RULES

Follow these instructions throughout the project.

1. Work in clearly defined phases.
2. Do not jump directly into rewriting.
3. First inspect the entire repository and all supplied research materials.
4. Maintain a traceable relationship between every paper claim and its evidence.
5. Use scripts to independently verify numerical results.
6. Preserve original files.
7. Do not modify frozen experimental artifacts.
8. Do not consume protected test-set access without approval.
9. Keep a record of every manuscript modification.
10. Do not silently resolve conflicting evidence.
11. Use external research only when necessary and cite verified sources.
12. Separate completed work from proposed future work.
13. Do not stop at identifying weaknesses: propose practical solutions.
14. Do not execute expensive additional experiments without explaining their value and obtaining approval.
15. Do not sacrifice scientific accuracy for publication presentation.

## IMPORTANT: HOW TO BEGIN

Start with PHASE 1.

Do not modify `paper.tex` or overwrite any existing research files during the initial audit.

First inspect the repository, all available experimental artifacts, both manuscripts, and the previous Claude discussion if accessible.

Then produce:

1. A concise understanding of the actual research contribution.
2. A reconstructed technical architecture.
3. A source-of-truth matrix.
4. A complete list of discrepancies.
5. A preliminary assessment of publication readiness.
6. A prioritized list of what must be done next.

Be particularly critical about the novelty and statistical validity of the bounded false-accept claim.

The ultimate objective is to produce a scientifically defensible, reproducible, technically rigorous research paper suitable for submission to an appropriate IEEE venue.

**Scientific integrity takes precedence over publication appearance.**