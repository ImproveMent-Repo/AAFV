AAFV-01 → AAFV-03: Research progression and remaining publication gaps
The important distinction here is that AAFV-03 is not simply a better-formatted version of AAFV-01. It represents a change in the research positioning, methodology description, and statistical claims of AAFV-Net.

I have the following materials to compare:
- AAFV-01 Report and manuscript.
- AAFV-02 manuscript.
- AAFV-03 manuscript.
- IEEE Transactions Expert Review.
- Two reference research papers:
  - From Age Estimation to Age-Invariant Face Recognition: Generalized Age Feature Extraction Using Order-Enhanced Contrastive Learning (IEEE TIFS, 2025).
  - Towards Age-Invariant Face Recognition (IEEE TPAMI, 2022).
- Main repository README.
- publication_tifs/README.md.
One important limitation: the expert review evaluates an earlier version of the research. We should not blindly treat every criticism as unresolved. Each point needs to be checked against AAFV-03 and, where necessary, the actual implementation and experimental records.
1. What changed from AAFV-01 to AAFV-03?
The most visible changes are:
Area	AAFV-01 / AAFV-02	AAFV-03
Research positioning	Age-aware face verification with bounded FAR	Guarded three-way verification with empirically bounded random false-accept risk
Architecture description	Direct and SAM-generated evidence	Explicit bidirectional and five-year-grid shared-target counterfactuals
Fusion	Calibrated MLP	947-parameter ensemble perceptron
Reliability	Quality and synthesis guards	Explicit quality, reliability, branch probability and age-gap context
Evaluation	Random and hard impostor evaluation	Explicitly reports same-sex bipartite random impostor construction
Authors	Incomplete placeholder author list in early manuscripts	Five named authors, including Dr. Swati Hira
Statistical reporting	Two-look FAR bound	Retains the 0.320% bound with two-look Bonferroni adjustment

AAFV-03 reports:
- 1,149 random impostor pairs with zero observed false accepts.
- 24,305 genuine pairs with 70.07% auto-acceptance.
- 35,735 hard impostors with 98.04% rejection and five residual false accepts.
- 57.49% neutral hard-impostor rejection.
- 51.92% external FG-NET adult auto-acceptance, compared with 40.38% for ArcFace.
These are manuscript-reported results, not independently verified experimental findings. 
AAFV-03.pdf

The biggest issue to investigate: AAFV-03 has improved the description of the system, but that alone does not establish that the methodological novelty, statistical validity, and external generalization criticisms have been resolved.
2. Expert review: what has actually been addressed?
This is the most important section. I have compared the review's criticisms with the actual contents of AAFV-03, rather than assuming that a newly added section resolves a criticism.
Addressed or substantially improved
Expert review criticism	AAFV-03 status	Evidence
3.1 Methodological novelty unclear	Partially addressed	Four explicit contributions, more formal architecture and counterfactual design
3.2 FAR statistical assumptions	Substantially improved	Disjoint bipartite sampling, 2,298 unique subjects, scoped Clopper–Pearson bound
3.3 Two-look evaluation leakage	Partially addressed	Two evaluation timestamps, checkpoint hashes and reconciliation table
3.4 Calibration quality	Partially addressed	Platt calibration and bin-wise calibration deviation
3.5 SAM identity preservation	Partially addressed	Explicit synthesis reliability score and identity-consistency component
3.6 External generalization	Partially addressed	Zero-shot FG-NET evaluation and pediatric failure disclosure
3.7 Baseline comparisons	Partially addressed	ArcFace, Siamese CNN, Siamese ViT, Qwen2-VL and internal ablations
3.8 Hard-impostor analysis	Partially addressed	Separate ArcFace-mined and neutral hard-impostor pools
3.9 Age-gap performance	Still a major concern	MORPH age-gap performance remains below ArcFace

The distinctions below explain why I have not marked these criticisms completely resolved.
2.1 Methodological novelty — still needs work
What improved:

AAFV-03 now identifies four contributions:
1. Guarded three-way decision architecture.
2. Empirical resolution of minimax threshold collapse.
3. Scoped statistical risk auditing.
4. External generalization, fairness and negative-result transparency.
The five-year shared-target SAM counterfactuals, branch masking, probability guards and 947-parameter fusion architecture make the methodology more specific.

What remains true from the review:

The reviewer questioned whether AAFV-Net is fundamentally novel or simply an integration of established components.

AAFV-03 cites several age-invariant approaches, including OE-CNN, DAL, MTLFace and OrdCon. However, citation alone does not establish methodological superiority or a distinct research contribution.

The two supplied papers are particularly relevant:
- Towards Age-Invariant Face Recognition: proposes jointly learning age-invariant representations and age synthesis.
- From Age Estimation to Age-Invariant Face Recognition: proposes order-enhanced contrastive learning to explicitly model the ordinal progression of age.
AAFV-03 needs a stronger comparison explaining why its risk-controlled verification objective is different from these age-invariant representation-learning approaches.

How to improve it:
- Create a methodology comparison table.
- Explain the difference between age-invariant representation learning and risk-controlled age-aware verification.
- Identify precisely what the proposed three-way policy contributes beyond conventional reject-option classification.
- Explain what shared-target counterfactual evidence provides that ordinary age-progression matching does not.
- Support each claimed contribution with an experiment or mathematical argument.
Do not claim that your architecture is fundamentally new just because it combines more components.
2.2 Statistical FAR guarantee — improved, but not fully settled
AAFV-03 makes an important improvement here.

It explicitly describes:
- 1,149 random impostor pairs.
- 2,298 unique subjects.
- Same-sex bipartite pairing without replacement.
- Two-look Bonferroni correction.
- Separate treatment of correlated and hard-impostor pools.
It also explicitly restricts the 0.320% confidence bound to the random-impostor evaluation set.

This is much better than making a blanket FAR guarantee.

However, there are still questions.

Problem A: Independence and population representativeness

Unique identities prevent identity reuse between pairs. That is useful.

But the statistical argument also needs to establish that the sampling procedure represents the intended deployment impostor population. Pairwise disjointness alone does not establish that.

The manuscript should justify the sampling design, conditional independence assumptions and target population.

Problem B: The bound is not sufficiently stringent for high-security applications
Important unresolved limitation
Your current bound is:
\[
FAR_{\text{upper}} \approx 0.320\%
\]

That does not establish a FAR of 0.1%, 0.01% or 0.001%.

For zero observed failures, the approximate number of independent impostor trials needed for a one-sided 95% bound is:
Desired upper FAR	Approximate independent trials
0.320%	1,149
0.1%	2,995
0.01%	29,956
0.001%	299,572

These are approximate sample-size requirements without the additional two-look adjustment.

With two-look Bonferroni correction, the required counts increase.

How to improve it:
1. Explain the target operational FAR.
2. Justify the sampling unit and independence assumptions.
3. Report identity-clustered confidence intervals for correlated evaluation pools.
4. Include sample-size calculations for operational FAR targets.
5. Avoid describing the random-impostor bound as a guarantee against look-alikes.
2.3 Two-look evaluation and adaptive leakage — partially addressed
AAFV-03 now includes a reconciliation table.

It reports:
Measurement	Look 1	Look 2
Genuine auto-accept	79.74%	70.07%
Genuine auto-reject	0%	0.54%
Hard-impostor rejection	0%	98.04%
Hard-impostor false accepts	3	5
Random impostor false accepts	0	0

It also identifies the checkpoint timestamps and SHA-256 hashes.

This is useful, but it creates an important question:

What exactly happened between the two test accesses?

The reviewer was concerned that the first test evaluation might have influenced later model or threshold decisions.

The Bonferroni correction accounts for multiple statistical looks under its assumptions. It does not automatically eliminate adaptive test-set leakage.

How to improve it:

Create a chronological audit table containing:
- Model development completion.
- Calibration completion.
- Threshold selection.
- First test access.
- Changes made after the first test.
- Second test access.
- Whether any test observations influenced those changes.
The existing test-access log and frozen artifacts should support this.

If the first test influenced subsequent design choices, disclose that explicitly. Do not retrospectively describe both evaluations as fully independent confirmatory experiments.
2.4 Calibration quality — still incomplete
AAFV-03 reports Platt scaling and a maximum absolute calibration-bin deviation of 0.0011 across G1–G3.

This is useful, but it is not a complete calibration evaluation.

The reviewer specifically requested:
- Expected Calibration Error (ECE).
- Brier score.
- Negative Log-Likelihood (NLL).
- Calibration slope and intercept.
- Reliability diagrams.
- Subgroup-specific calibration.
- Cross-dataset calibration.
These are not all demonstrated by the reported bin-deviation statistic.

How to improve it:

Add a dedicated calibration evaluation:
Metric	Purpose
ECE	Measures calibration error
Brier score	Measures probabilistic prediction error
NLL	Measures probabilistic confidence quality
Calibration slope	Detects overconfidence or underconfidence
Calibration intercept	Detects systematic probability bias
Reliability diagram	Visually compares predicted and observed probabilities

Evaluate calibration on MORPH and FG-NET separately, and compare the effect of distribution shift without recalibration.
2.5 SAM identity preservation — partially addressed
This is an important improvement in AAFV-03.

Your reliability score now includes:
- Identity consistency.
- Age accuracy.
- Generated-image quality.
- Inter-target embedding consistency.
However, the identity consistency component uses ArcFace, which is also part of the verification system.

That creates a circularity concern: the generator's identity preservation is being assessed using a model whose similarity evidence also contributes to the final decision.

How to improve it:
- Evaluate SAM-generated faces with an independent face-recognition model not used in fusion.
- Report identity similarity before and after generation.
- Evaluate different age-gap categories.
- Report failed or identity-drifted generations.
- Compare SAM against another suitable age-progression generator if technically feasible.
- Consider blinded human evaluation.
The objective is to demonstrate that SAM preserves identity independently, not merely that its output receives a high internal reliability score.
2.6 External generalization — improved, but limited
AAFV-03 has made a significant improvement by evaluating on FG-NET without retraining.

However, there is an important qualification.

The manuscript reports four false accepts among 20,000 all-age impostor pairs, all involving children aged 0–4.

It then restricts its adult evaluation to ages 16 and above.

The manuscript transparently acknowledges that this age restriction was selected after inspecting the pediatric failures.

This is good disclosure, but it does not establish broad generalization.

How to improve it:
- Add another independent adult cross-age dataset, such as AgeDB or CACD, subject to access and licensing.
- Keep the model and thresholds frozen.
- Do not tune on the new dataset.
- Report genuine acceptance, impostor rejection, manual-review rate and confidence intervals.
- Report dataset composition and age-gap distribution.
The key is a genuinely independent cross-dataset evaluation, not simply another evaluation on the same data source.
2.7 Baseline comparison — partially addressed
AAFV-03 now includes:
- ArcFace.
- Siamese CNN.
- Siamese ViT.
- Qwen2-VL-2B.
- Direct-only and multi-metric internal baselines.
- Multiple component ablations.
However, the expert reviewer specifically requested comparisons with:
- AdaFace.
- MagFace.
- OE-CNN.
- DAL.
- MTLFace.
- Selective classification baselines.
- Uncertainty-aware verification methods.
These are not all present as experimental baselines in AAFV-03.

There is another important problem: the manuscript acknowledges that the Siamese ViT training was limited to three epochs and did not fully converge.

You cannot use an inadequately trained baseline as strong evidence that your method is superior.

How to improve it:

Prioritize:
1. AdaFace.
2. MagFace.
3. One or more reproducible age-invariant approaches.
4. A conventional reject-option baseline.
5. A quality-aware fusion baseline.
Use identical identity-disjoint partitions, calibration data and operating conditions.

If a baseline cannot be reproduced, explain why and avoid claiming superiority over it.
2.8 Hard-impostor analysis — partially addressed
AAFV-03 now distinguishes:
- Random impostors.
- ArcFace-mined hard impostors.
- Model-neutral hard impostors.
This is a strong improvement.

However, five false accepts remain among 35,735 ArcFace-mined hard impostors.

The manuscript explicitly says these five failures were not visually inspected.

The reviewer specifically requested failure analysis.

How to improve it:

Investigate the five residual errors using privacy-preserving records.

Classify them by:
- Facial similarity characteristics.
- Image quality.
- Age gap.
- SAM reliability.
- Direct versus synthesized evidence.
- Demographic subgroup, where available.
Also document the hard-negative mining procedure and establish that the final hard-impostor evaluation set was not used for model or threshold tuning.
2.9 Age-gap performance — still a major concern
This is arguably the most important performance-related criticism.

Your AAFV-03 manuscript acknowledges that ArcFace exceeds AAFV-Net across every MORPH age-gap bin.
Unresolved performance concern
Age-gap category	AAFV-Net	ArcFace
0–4 years	71.03%	90.49%
5–9 years	56.39%	80.08%
10–14 years	45.65%	69.01%
15–19 years	1.33%	2.67%
20–29 years	2.19%	2.19%
30+ years	50.00%	50.00%

The extreme age-gap bins are also sparse, so their percentages require confidence intervals and careful interpretation.

The problem is that your method accepts fewer genuine pairs on MORPH than ArcFace.

You do have a different advantage: the ability to reject difficult impostors while routing uncertain cases to manual review.

That is a legitimate research direction, but it needs to be evaluated as a risk-coverage trade-off, not presented as universal improvement in cross-age recognition.

How to improve it:
- Report genuine auto-acceptance.
- Report genuine manual-review rate.
- Report genuine auto-rejection.
- Report impostor auto-rejection.
- Compare these at matched security operating points.
- Include risk-coverage curves.
- Explain the operational benefit of rejecting difficult impostors when accepting fewer genuine pairs.
Your research should demonstrate why this trade-off is valuable, rather than hide the lower acceptance rate.

2.10 Fairness and demographic evaluation — still incomplete
AAFV-03 has made the fairness problem visible instead of ignoring it.

It reports:
Group	Genuine auto-acceptance
Male	81.07%
Female	71.93%
Difference	9.14 percentage points

But there is a significant limitation:
- These results come from Look 1.
- Look 2 does not retain per-pair sex information.
- Racial subgroup analysis has not been performed.
- Intersectional fairness analysis is missing.
How to improve it:
1. Preserve demographic labels in the next evaluation pipeline.
2. Re-evaluate all fairness metrics on a frozen evaluation set.
3. Calculate confidence intervals for each subgroup.
4. Report acceptance, rejection and manual-review rates separately.
5. Investigate whether the difference comes from image quality, age distribution or model behavior.
Do not claim demographic fairness merely because you report demographic statistics.
2.11 Security evaluation — still incomplete
AAFV-03 improves its evaluation of look-alike impostors, but its security assessment is still narrower than the security claims suggest.

The expert reviewer requested a threat model covering:
- Look-alikes.
- Low-resolution and degraded images.
- Image manipulation.
- Face morphing.
- Presentation attacks.
AAFV-03 primarily addresses random and mined impostor comparisons.

How to improve it:

Define the threat model first.

Separate ordinary identity mismatch from adversarial manipulation and presentation attacks. You do not necessarily need to implement every possible attack, but you must clearly state which attacks your system has and has not been tested against.
2.12 Computational complexity — partially addressed
AAFV-03 reports:
- 947 trainable parameters per seed.
- 4,741 parameters across the five-seed ensemble and calibration components.
- 0.18 μs batched fusion inference.
- 77.2 μs unbatched fusion inference.
However, these measurements concern the learned fusion stage, not the complete verification pipeline.

SAM generation, face alignment and feature extraction are not represented by that fusion latency.

How to improve it:

Report:
- Complete end-to-end inference latency.
- SAM generation time.
- Face preprocessing time.
- Feature extraction time.
- CPU and GPU performance.
- Peak memory consumption.
- Throughput.
- p95 latency.
- Direct-only versus direct-plus-SAM cascade performance.
Your proposed cascade strategy is particularly worth investigating: run direct verification first and invoke SAM only for uncertain cases.

This could provide a meaningful operational contribution.

3. What the two reference papers mean for your research
Your instructor's instruction to study papers from the target journal is not just about copying their writing style.

You need to understand how their research contributions are constructed and how they establish their claims.










Paper 1: OrdCon (2025)

From Age Estimation to Age-Invariant Face Recognition: Generalized Age Feature Extraction Using Order-Enhanced Contrastive Learning

IEEE TIFS, 2025

Core contribution: Explicitly models the ordinal progression of age through directional contrastive learning and soft proxy matching.

Read the published paper













Paper 2: AIM (2022)

Towards Age-Invariant Face Recognition

IEEE TPAMI, 2022

Core contribution: Jointly learns age-invariant identity representations and cross-age face synthesis.

Read the published paper



What you should learn from OrdCon
OrdCon is particularly relevant because it is published in your target journal and addresses generalized age-feature extraction.

Study:
1. How the authors identify a limitation in conventional age-feature learning.
2. How they formulate their research hypothesis.
3. How they mathematically define their proposed losses.
4. How they compare against existing approaches.
5. How they structure homogeneous and cross-dataset experiments.
6. How they discuss limitations without overstating their results.
What AAFV-Net should learn from it: A contribution needs to be mathematically and experimentally distinguishable from the existing literature.
What you should learn from AIM
AIM is relevant because it combines face synthesis and recognition.

Study:
1. How the joint architecture is motivated.
2. How synthesis and recognition improve each other.
3. How identity preservation is demonstrated.
4. How the authors establish the usefulness of their generated faces.
5. How they validate their model across multiple datasets.
What AAFV-Net should learn from it: You need to establish why SAM-based evidence improves verification rather than merely adding another source of similarity scores.
How to use these papers in your manuscript
Create a dedicated comparison table:
Research dimension	AIM	OrdCon	AAFV-Net
Primary objective	Age-invariant recognition	Generalized age features	Risk-controlled cross-age verification
Age modelling	Joint face aging and recognition	Ordinal feature progression	Explicit age-gap context and SAM counterfactuals
Main learning strategy	Joint deep architecture	Order-enhanced contrastive learning	Multi-metric fusion and guarded decisions
Explicit manual-review decision	Not the central objective	Not the central objective	Yes
Statistical FAR bound	Not the central contribution	Not the central contribution	Central contribution

This table is a starting point, not a substitute for a detailed literature comparison. The claims about the previous methods should be checked against their full experimental sections.

4. Additional problems discovered in the manuscript and repository
There are several issues that deserve attention independently of the expert review.
Fix before submission
A. Your GitHub manuscript still contains author placeholders
This is a particularly important inconsistency.

The uploaded AAFV-03 PDF lists:
- Anurag Nayak
- Sujal Chondhekar
- Sumit Kumar
- Piyush Jain
- Swati Hira
However, the currently accessible publication_tifs/main.tex in your supplied GitHub repository still contains:
\author{Anurag~Nayak,~\IEEEmembership{Graduate Student Member,~IEEE,}
        [Co-Author~Names~To~Be~Completed]%


It also contains placeholders for institutional affiliations, ORCID IDs, funding and corresponding-author information. 

GitHub+1

Required changes:
- Include all five authors.
- Include Dr. Swati Hira as a co-author.
- Verify author order.
- Add institutional affiliations.
- Add verified institutional email addresses.
- Add ORCID IDs.
- Identify the corresponding author.
- Complete funding and author contribution statements.
Do not assume that fixing the PDF automatically fixes the LaTeX source.
B. Your manuscript and repository URLs are inconsistent
The uploaded AAFV-03 PDF and the currently published LaTeX source do not consistently identify the repository.

The GitHub repository you supplied is:
ImproveMent-Repo/AAFVBut the manuscript source points to a different repository address. Correct this throughout the manuscript and supplementary material. 
AAFV-03.pdf+1

C. Your reproducibility package is not the same as your complete research implementation
Your main README explicitly states that the training/evaluation code, raw datasets and large model checkpoints are maintained separately and excluded from the repository.

The publication README describes frozen CSVs, SHA-256 checksums, figure generators, tables and supplementary material. 
README.md+1

This means the publication package may be reproducible at the figure/table generation level without providing enough information for an independent researcher to reproduce the entire training and evaluation pipeline.

You should distinguish:
- Manuscript reproducibility.
- Figure and table reproducibility.
- Model inference reproducibility.
- Full training and evaluation reproducibility.
Do not claim complete end-to-end reproducibility unless the required artifacts and instructions actually make it possible.
D. Your negative results need stronger presentation
AAFV-03 has done something important: it acknowledges pediatric failures, the MORPH acceptance deficit, residual hard-impostor errors and incomplete fairness information.

Keep this.

However, negative findings should be analyzed rather than simply placed in a limitations section.

The strongest improvement would be to explain exactly which operating conditions cause AAFV-Net to outperform ArcFace and which conditions cause it to underperform.
E. Your calibration and ablation evidence needs clearer separation
The manuscript reports ablation results using the calibration common subset, while its primary results come from the MORPH test evaluation.

These should not be presented as though they have the same evidential strength.

Clearly distinguish:
- Training-set results.
- Validation results.
- Calibration-set results.
- Test-set results.
- External-dataset results.
Ablation choices made using calibration data should not be described as independent test confirmation.

5. What should you actually change? Prioritized action plan
Do not attempt to address all reviewer comments by adding paragraphs. Several require experiments, not writing.

Here is the order I would follow.
Priority 1 — Critical research issues
Must address

1. Establish methodological novelty.
   
   Clearly distinguish AAFV-Net from AIM, OrdCon, conventional score fusion and reject-option classifiers.
2. Strengthen statistical validity.
   
   Justify the FAR sampling assumptions, explain the two-look history and provide sensitivity/sample-size analysis.
3. Resolve the MORPH age-gap performance problem.
   
   Explain the lower genuine acceptance relative to ArcFace using matched operating points and risk-coverage curves.
4. Strengthen external validation.
   
   Add an independent dataset with frozen model parameters and thresholds.
5. Independently validate SAM identity preservation.
   
   Use a recognition model outside the fusion architecture.

Priority 2 — Experimental completeness
High priority

1. Implement ECE, Brier score, NLL, calibration slope/intercept and reliability diagrams.
2. Evaluate stronger baselines such as AdaFace and MagFace, and suitable age-invariant methods.
3. Inspect and categorize the five residual hard-impostor false accepts.
4. Repeat fairness evaluation with retained demographic metadata on the final frozen evaluation.
5. Report end-to-end inference cost, not just MLP inference time.
6. Evaluate image degradation and relevant biometric attack scenarios under a defined threat model.

Priority 3 — Manuscript quality
Publication preparation

1. Complete author metadata and corresponding-author information.
2. Reconcile all manuscript numbers with frozen experimental records.
3. Improve the related-work section using the supplied TIFS and TPAMI papers.
4. Improve figure quality, captions, mathematical notation and experimental explanations.
5. Ensure LaTeX source, compiled PDF and supplementary material are consistent.

6. My recommended research direction
I would not position AAFV-Net as a face-recognition model that universally outperforms ArcFace.

Your current MORPH results do not support that claim.

Instead, position it as:

A risk-controlled cross-age biometric verification framework that uses auxiliary age-progression evidence and guarded selective decisions to balance genuine-user automation against difficult-impostor rejection.

This is a more defensible contribution.

Your central research question should become:
Can auxiliary age-progression counterfactuals, quality-aware multimodal fusion and guarded three-way decisions improve the operational handling of difficult cross-age biometric comparisons under explicitly quantified random-impostor risk?

This positioning has three advantages:
1. It acknowledges that ArcFace can have higher genuine acceptance.
2. It focuses attention on your hard-impostor rejection and manual-review mechanism.
3. It makes statistical risk control a central contribution rather than an additional metric.
But you still need to demonstrate that the operational trade-off is genuinely better under matched conditions.
7. Final status: what remains true from the original expert report?
Original criticism	Still true in AAFV-03?
Insufficient methodological novelty	Yes, partially
Weak statistical justification	Yes, partially
Potential adaptive test leakage	Not conclusively resolved
Incomplete calibration analysis	Yes
Inadequate SAM identity validation	Yes
Limited external generalization	Yes
Insufficient baseline comparisons	Yes
Weak hard-impostor failure analysis	Yes
Poor MORPH age-gap performance relative to ArcFace	Yes
Incomplete fairness analysis	Yes
Incomplete security evaluation	Yes
Incomplete computational profiling	Yes
Reproducibility and numerical reconciliation	Partially

8. Important limitation of this repository analysis
I inspected the supplied manuscripts, README files and the accessible GitHub publication source.

The repository explicitly excludes the underlying Code/ implementation, raw datasets and large checkpoints. Therefore, I can assess what AAFV-03 claims and whether its documentation addresses the review, but I cannot independently certify that the implementation produces those results.

There is also a version discrepancy between your uploaded publication README and the currently accessible GitHub README and main.tex. Resolve that before treating the repository as the definitive publication package. 
README(1).md+2


My final recommendation
Do not spend the next week polishing sentences, changing fonts or adding more references.

Your next revision should focus on three things:
1. Research novelty: Prove why AAFV-Net is more than an integration of existing techniques.
2. Experimental credibility: Strengthen risk validation, calibration, baselines and external testing.
3. Scientific honesty: Explain the MORPH performance deficit and demonstrate the actual operational advantage of the three-way decision policy.
These are the changes most likely to improve the scientific quality of the manuscript.

The current AAFV-03 is a meaningful improvement over AAFV-01, but it is not yet evidence that the expert review's central objections have been resolved. The remaining work is primarily research and experimentation, not copyediting.