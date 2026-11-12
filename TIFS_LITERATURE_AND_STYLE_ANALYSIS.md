# TIFS Literature & Writing Style Analysis

**Prepared For:** Alignment of *AAFV-Net: Age-Aware Face Verification with a Measured, Bounded False-Accept Rate*  
**Target Venue:** *IEEE Transactions on Information Forensics and Security* (TIFS)  
**Stage:** Phase 2 Deliverable (`Prompt-2.md`)  
**Date:** November 12, 2026

---

## 1. Access Scope and Methodology Disclosure

In strict accordance with the Phase 2 execution rules (`Prompt-2.md` line 560), we disclose the exact evidence scope used in this review:
- **Verified Authoritative Metadata & Technical Content:** All 14 selected *IEEE Transactions on Information Forensics and Security* (TIFS) articles were verified via indexed IEEE Xplore/Crossref/DBLP/ORCID metadata, official abstracts, institutional repositories (e.g., Idiap, Plymouth, ETH/KAIST/UNIBO), and publicly available full author preprints on arXiv (specifically Xu *et al.* `arXiv:2210.13905`, Razeghi *et al.*, Hu *et al.*, Huang *et al.*, Osorio-Roig *et al.*, Ahn *et al.*, and Poh *et al.*).
- **Paywall Limitation Disclosure:** Direct download of the proprietary publisher-typeset IEEE Xplore PDFs behind subscription paywalls (e.g., exact published figure typesetting of Wang *et al.* 2025, Mao & Li 2025, and Qin *et al.* 2022) was not available in this workspace. All writing-style analyses and technical claims below are grounded strictly in the verified metadata, full abstracts, open-access preprints, institutional technical reports, and documented IEEE Signal Processing Society structural standards—nothing is extrapolated from unread pages.

---

## 2. Selected TIFS Corpus & Domain Coverage (14 Papers: 2022–2026 + Landmarks)

We selected **14 peer-reviewed papers published in *IEEE Transactions on Information Forensics and Security*** spanning **10 recent papers (2022–2026)** and **4 foundational TIFS biometric pillars (2009–2021)** directly intersecting AAFV-Net's 12 target themes:

| # | Authors & Year | Vol. / Pages | DOI | Primary TIFS Domain Mapping |
|:---:|---|---|---|---|
| **P1** | Wang *et al.* (2025) | Vol. 20, pp. 8525–8540 | `10.1109/TIFS.2025.3597187` | Cross-age / Age-invariant face recognition (AIFR) |
| **P2** | Hu, Chen, & Zhu (2025) | Vol. 20, pp. 516–530 | `10.1109/TIFS.2024.3515834` | Neyman-Pearson risk control under adversarial evasion |
| **P3** | Mao & Li (2025) | Vol. 20, pp. 7257–7271 | `10.1109/TIFS.2025.3587917` | Face recognition / FAS under OOD distribution shift |
| **P4** | Razeghi, Rahimi, & Marcel (2026) | Vol. 21, pp. 5181–5192 | `10.1109/TIFS.2026.3692276` | Generative vs. discriminative identity-attribute privacy |
| **P5** | Xu, Zhang, & Zhou (2024) | Vol. 19, pp. 372–384 | `10.1109/TIFS.2023.3318957` | Probability calibration & uncertainty in face verification |
| **P6** | Ahn *et al.* (2024) | Vol. 19, pp. 7176–7186 | `10.1109/TIFS.2024.3426973` | Quality-linked uncertainty & open-set evaluation |
| **P7** | Zhou *et al.* (2024) | Vol. 19, pp. 7536–7547 | `10.1109/TIFS.2024.3435440` | Open-set unknown generative synthesis & domain shift |
| **P8** | Osorio-Roig *et al.* (2024) | Vol. 19, pp. 4835–4850 | `10.1109/TIFS.2024.3386310` | Multi-biometric fusion, workload vs. high-security FAR |
| **P9** | Otroshi Shahreza *et al.* (2024) | Vol. 19, pp. 4585–4600 | `10.1109/TIFS.2024.3381820` | Biometric embedding security (TMR @ FMR $=10^{-3}$, SAR) |
| **P10** | Qin, Peng, & Long (2022) | Vol. 17, pp. 3649–3662 | `10.1109/TIFS.2022.3212276` | Differential face comparison & look-alike blending defense |
| **P11** | Huang *et al.* (2021) | Vol. 16, pp. 2031–2045 | `10.1109/TIFS.2020.3047753` | Generative progressive face aging & identity preservation |
| **P12** | Paone *et al.* (2014) | Vol. 9, no. 2, pp. 285–295 | `10.1109/TIFS.2013.2296373` | Look-alike / twin hard impostor FAR & longitudinal drift |
| **P13** | Klare *et al.* (2012) | Vol. 7, no. 6, pp. 1789–1801 | `10.1109/TIFS.2012.2214212` | Demographic bias & subgroup error disparities in FR |
| **P14** | Poh *et al.* (2009) | Vol. 4, no. 4, pp. 849–866 | `10.1109/TIFS.2009.2034885` | Quality-dependent & missing-channel biometric score fusion |

*(Note: Selected 14 verified TIFS articles; Volumes 16–21 use IEEE continuous annual pagination without separate print issue numbers in standard IEEE Xplore citations.)*

---

## 3. Detailed Paper Profiles and Relevance to AAFV-Net

### P1. Cross-Age Representation Learning (2025)
- **Exact Title:** *From Age Estimation to Age-Invariant Face Recognition: Generalized Age Feature Extraction Using Order-Enhanced Contrastive Learning*
- **Authors:** Haoyi Wang, Victor Sanchez, Chang-Tsun Li, and Nathan Clarke
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 20, pp. 8525–8540, 2025. DOI: `10.1109/TIFS.2025.3597187`
- **Research Problem:** Deep age-estimation and age-invariant face recognition (AIFR) models degrade severely under cross-dataset domain shifts because standard losses ignore the continuous ordinal nature of human aging.
- **Main Contribution:** Proposes *OrdCon*, an order-enhanced contrastive learning formulation enforcing directional ordinality in latent aging vectors alongside proxy class clustering.
- **Methodology:** Combines paired direction-vector alignment (modeling forward/backward aging trajectories) with Soft Proxy Matching loss to tighten intra-age compactness while preserving proportional inter-age spacing.
- **Datasets & Protocol:** Cross-dataset evaluation across standard facial aging corpora (e.g., MORPH, AFAD, FG-NET protocols — exact fold breakdowns reside behind the IEEE Xplore full text).
- **Main Results:** Reduces cross-dataset age estimation MAE by ~1.38 on average and raises generalized AIFR verification accuracy by ~1.87% over compared SOTA baselines.
- **Limitations:** Optimizes uncalibrated feature separation and aggregate verification accuracy; provides no reject option or test-time upper confidence guarantee on random false accepts. Full per-dataset split breakdowns were restricted behind paywall.
- **Relationship to AAFV-Net:** Shows that contemporary TIFS AIFR research focuses on ordinal representation invariance rather than calibrated decision bounding. AAFV-Net operates orthogonally at the calibrated decision stage and explicitly models bidirectional forward/backward progression rather than embedding invariance alone.

### P2. Neyman-Pearson Security Under Strategic Evasion (2025)
- **Exact Title:** *Game-Theoretic Neyman-Pearson Detection to Combat Strategic Evasion*
- **Authors:** Yinan Hu, Juntao Chen, and Quanyan Zhu
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 20, pp. 516–530, 2025. DOI: `10.1109/TIFS.2024.3515834`
- **Research Problem:** Classical Neyman-Pearson (NP) detectors fix thresholds assuming stationary impostor/attack distributions, making them vulnerable to strategic, adaptive evasion.
- **Main Contribution:** Integrates Stackelberg/game-theoretic modeling with Neyman-Pearson hypothesis testing, introducing Equilibrium Receiver Operating Characteristic (EROC) curves and sequential i.i.d. detection analysis.
- **Methodology:** Derives minimax/equilibrium threshold policies constraining Type-I false-alarm rates while optimizing detection power against strategically perturbed adversary distributions.
- **Datasets & Protocol:** Analytical verification plus sequential intrusion-detection case studies (open preprint inspected).
- **Main Results:** Evasion-aware NP rules systematically outperform static NP thresholds along EROC envelopes under adversarial shift.
- **Limitations:** Assumes explicit parametric/game-theoretic adversary utilities; targets network intrusion rather than facial biometrics or reject-option human handoff.
- **Relationship to AAFV-Net:** Directly reinforces why AAFV-Net must strictly distinguish between random person-disjoint impostor guarantees ($\mathcal{D}_{\text{random}}$ satisfying analytical NP/Bernoulli bounds) and adversarially mined look-alike impostors ($\mathcal{D}_{\text{hard}}$, where strategic similarity selection alters the impostor tail distribution).

### P3. OOD Generalization in Face Biometrics (2025)
- **Exact Title:** *Hyperbolic Metric Learning for Generalizable Face Anti-Spoofing*
- **Authors:** Shiyun Mao and Huibin Li
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 20, pp. 7257–7271, 2025. DOI: `10.1109/TIFS.2025.3587917`
- **Research Problem:** Biometric classifiers overfit to source-domain sensors, lighting, and spoofing materials, failing on unseen target distributions.
- **Main Contribution:** Formulates out-of-distribution (OOD) facial representation in hyperbolic space (*HML-FAS*) using Stein variational adversarial augmentation and Hyperbolic Optimal Transport.
- **Methodology:** Maps multi-domain embeddings onto shared hyperbolic manifolds with kantorovich potentials to enforce domain invariance across hierarchical boundary relationships.
- **Datasets & Protocol:** Cross-domain leave-one-domain-out facial protocols (MSU-MFSD, CASIA-FASD, Replay-Attack, OULU-NPU context per indexed abstract; exact split tables behind paywall).
- **Main Results:** Consistently outperforms Euclidean metric learning baselines (*EML-FAS*) across cross-domain transfer benchmarks.
- **Limitations:** Evaluates binary spoof vs. live discrimination using AUC/HTER without human-in-the-loop abstention or calibrated false-accept upper bounds.
- **Relationship to AAFV-Net:** Illustrates TIFS's strict standard for testing OOD domain transfer across distinct acquisition regimes (analogous to AAFV-Net's MORPH-frozen evaluation on unconstrained FG-NET photographs).

### P4. Generative vs. Discriminative Attribute-Identity Privacy (2026)
- **Exact Title:** *Deep Privacy Funnel Model: From a Discriminative to a Generative Approach With an Application to Face Recognition*
- **Authors:** Behrooz Razeghi, Parsa Rahimi, and Sébastien Marcel
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 21, pp. 5181–5192, 2026. DOI: `10.1109/TIFS.2026.3692276`
- **Research Problem:** Soft biometric attributes (age, gender, ethnicity) leak inside facial embeddings, creating tension between utility and privacy/invariance.
- **Main Contribution:** Unifies Discriminative and Generative Privacy Funnel models via tractable variational bounds (*DVPF*) integrated with ArcFace/AdaFace pipelines.
- **Methodology:** Optimizes self-information (logarithmic) utility-privacy objectives to obfuscate nuisance/sensitive covariates while retaining identity verification accuracy.
- **Datasets & Protocol:** Tested on standard unconstrained face recognition and soft-attribute benchmarks with PyTorch implementation attached (verified via Idiap/arXiv abstract).
- **Main Results:** Suppresses sensitive attribute leakage (e.g., age/gender) while retaining competitive ArcFace/AdaFace matching rates.
- **Limitations:** Suppressing age features eliminates longitudinal temporal calibration cues; lacks deterministic verification thresholding guards.
- **Relationship to AAFV-Net:** Contrasts philosophically with AAFV-Net: whereas Privacy Funnel methods purge age covariates from embeddings, AAFV-Net explicitly measures age gap ($g$) and age-progressed counterfactuals as contextual inputs to calibrate risk.

### P5. Confidence Calibration in Face Verification (2024)
- **Exact Title:** *Confidence-Calibrated Face and Kinship Verification*
- **Authors:** Min Xu, Ximiao Zhang, and Xiuzhuang Zhou
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 372–384, 2024. DOI: `10.1109/TIFS.2023.3318957`
- **Research Problem:** Modern angular-margin face matchers (ArcFace, CosFace) produce uncalibrated similarity scores that exhibit severe overconfidence under distribution noise and kinship/look-alike ambiguity.
- **Main Contribution:** Introduces *Angular Scaling Calibration (ASC)*—a plug-and-play post-hoc calibration transforming angular cosine similarities into well-calibrated confidence probabilities with modeled prediction uncertainty.
- **Methodology:** Fits monotonic/angular scaling mappings on validation scores without altering deep backbones, plus uncertainty modeling over calibrated outputs.
- **Datasets & Protocol:** LFW, KinFaceW-I/II, and Families in the Wild (FIW) evaluated via Verification Accuracy, AUROC, and Expected Calibration Error (ECE) + Reliability Diagrams (`arXiv:2210.13905` inspected).
- **Main Results:** Substantially lowers ECE compared to uncalibrated baselines, Temperature Scaling, and Histogram Binning while preserving AUROC and accuracy.
- **Limitations:** Evaluates single-branch similarity calibration; does not address cross-age generative evidence fusion, three-way auto-accept/review/reject partitioning, or formal zero-failure upper bounds.
- **Relationship to AAFV-Net:** Closest calibration precedent in TIFS! Directly validates AAFV-Net's core empirical finding (Table III): high AUROC/AUC in Siamese or angular baselines fails under strict zero-FA thresholding without post-hoc calibration and reliability gating.

### P6. Quality-Driven Uncertainty in Open-Set Face Recognition (2024)
- **Exact Title:** *Uncertainty-Aware Face Embedding With Contrastive Learning for Open-Set Evaluation*
- **Authors:** Kyeongjin Ahn, SeungEon Lee, Sungwon Han, Cheng-Yaw Low, and Meeyoung Cha
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 7176–7186, 2024. DOI: `10.1109/TIFS.2024.3426973`
- **Research Problem:** Deterministic point embeddings misclassify degraded, blurry, or low-quality open-set probes into impostor false accepts.
- **Main Contribution:** Proposes *UCFace*, mapping face representations to probabilistic von Mises-Fisher (vMF) / Gaussian distributions whose concentration quantifies image-quality uncertainty under contrastive learning.
- **Methodology:** Predicts both mean direction and variance/concentration parameter inversely tied to sample quality; matches pairs using probability-density likelihood rather than raw cosine distance.
- **Datasets & Protocol:** Evaluated on LFW, CALFW, CPLFW, AgeDB, CFP-FP, and open-set IJB-C protocols measuring TAR at low FMR ($10^{-4}$ / $10^{-3}$) and open-set metrics.
- **Main Results:** Outperforms deterministic ArcFace and earlier PFE baselines on mixed-quality open-set matching and noisy probes.
- **Limitations:** Requires retraining backbone embeddings probabilistically; models input-image aleatoric blur/quality rather than generative synthesis variance or multi-look FAR confidence bounds.
- **Relationship to AAFV-Net:** Strong conceptual ally in TIFS: whereas UCFace embeds quality uncertainty into backbone latent space, AAFV-Net operationalizes quality ($Q$) and synthesis reliability ($R_{\text{sam}}$) as explicit thresholded guards feeding a calibrated three-way decision gate.

### P7. Open-Set Generative Forgery Adaptation (2024)
- **Exact Title:** *Fine-Grained Open-Set Deepfake Detection via Unsupervised Domain Adaptation*
- **Authors:** Xinye Zhou, Hu Han, Shiguang Shan, and Xilin Chen
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 7536–7547, 2024. DOI: `10.1109/TIFS.2024.3435440`
- **Research Problem:** Forensic models encounter unknown generative face synthesis manipulations in open-world settings outside closed training sets.
- **Main Contribution:** Combines Network Memorization-based Adaptive Clustering (NMAC) with pseudo-label matching for open-set attribution across domain shifts.
- **Datasets & Protocol:** Cross-dataset transfers across FaceForensics++, ForgerNet, and FakeAVCeleb using AUC and open-set accuracy.
- **Limitations:** Targets deepfake classification rather than genuine longitudinal biometric matching; lacks reject-option FAR guarantees.
- **Relationship to AAFV-Net:** Highlights TIFS readers' acute skepticism toward synthetic GAN/diffusion facial imagery—explaining why AAFV-Net's skepticism toward SAM synthesis (via explicit $R_{\text{sam}}$ gating and 12% branch dropout) is crucial for forensic credibility.

### P8. Multi-Biometric Fusion & Workload Reduction (2024)
- **Exact Title:** *Privacy-Preserving Multi-Biometric Indexing Based on Frequent Binary Patterns*
- **Authors:** Dailé Osorio-Roig, Lázaro J. González-Soler, Christian Rathgeb, and Christoph Busch
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 4835–4850, 2024. DOI: `10.1109/TIFS.2024.3386310`
- **Research Problem:** Exhaustive biometric verification/indexing across protected templates incurs severe workload and accuracy losses at strict high-security FMR thresholds.
- **Main Contribution:** Frequent binary-pattern multi-biometric indexing across cancelable templates (BioHashing, IoM Hashing).
- **Main Results:** Cuts computational workload down to ~53%–57% of exhaustive baseline while preserving/improving EER at strict operating thresholds.
- **Limitations:** Requires multi-modal traits (face + iris/fingerprint) rather than single-face longitudinal verification, and focuses on indexing efficiency rather than bounded pairwise verification.
- **Relationship to AAFV-Net:** Demonstrates TIFS's emphasis on explicitly reporting **computational workload vs. biometric error rate trade-offs**—mirroring AAFV-Net's manual-review workload vs. zero-FA automation curve and cascaded latency savings ($0.19\ \mu\text{s}$ MLP vs. $58.2\text{ ms}$ SAM).

### P9. Security Bounds of Deep Face Templates (2024)
- **Exact Title:** *Vulnerability of State-of-the-Art Face Recognition Models to Template Inversion Attack*
- **Authors:** Hatef Otroshi Shahreza, Vedrana Krivokuća Hahn, and Sébastien Marcel
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 4585–4600, 2024. DOI: `10.1109/TIFS.2024.3381820`
- **Research Problem:** Evaluates whether modern deep face embeddings (31 architectures/losses including ArcFace) leak reconstructible facial identity capable of bypassing fixed verification thresholds.
- **Datasets & Protocol:** MOBIO, LFW, and **AgeDB** evaluated strictly via **True Match Rate (TMR) at $\text{FMR} = 10^{-3}$** and **Success Attack Rate (SAR)**.
- **Limitations:** Examines template inversion security rather than cross-age matching or calibration bounds.
- **Relationship to AAFV-Net:** Establishes TIFS benchmark reporting standards (mandatory reporting at strict fixed FMR operating points, e.g., $10^{-3}$) and highlights security hazards of storing raw unconstrained deep face descriptors.

### P10. Differential Face Verification vs. Synthetic Blending (2022)
- **Exact Title:** *Face Morphing Attack Detection and Localization Based on Feature-Wise Supervision*
- **Authors:** Le Qin, Fei Peng, and Min Long
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 17, pp. 3649–3662, 2022. DOI: `10.1109/TIFS.2022.3212276`
- **Research Problem:** Conventional holistic score losses fail to distinguish differential face pairs involving subtle synthetic morphs or low-resolution probes.
- **Main Contribution:** Feature-wise classification and differential pair-similarity supervision across trusted ID references and live checkpoint probes.
- **Relationship to AAFV-Net:** Analogous pair-comparison setting (comparing a trusted older/document photo with a live probe), proving why combining multi-layer perceptual/structural cues alongside angular identity embeddings catches fine-grained impostors that global cosine matchers miss.

### P11. Generative Progressive Aging & Identity Preservation (2021)
- **Exact Title:** *PFA-GAN: Progressive Face Aging With Generative Adversarial Network*
- **Authors:** Zhizhong Huang, Shouzhen Chen, Junping Zhang, and Hongming Shan
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 16, pp. 2031–2045, 2021. DOI: `10.1109/TIFS.2020.3047753`
- **Research Problem:** Single-step conditional GANs suffer blurriness, ghost artifacts, and identity drift across wide age gaps.
- **Main Contribution:** Progressive multi-stage sub-network chaining across age groups with binary-gate skip connections, identity preservation loss, and age estimation loss.
- **Datasets & Protocol:** MORPH Album 2 and CACD evaluated via Face++ API v3 verification at fixed $\text{FAR} = 10^{-5}$ (threshold 76.5) and Age Estimation Error (AEE).
- **Limitations:** Uses generative synthesis primarily for visual photorealism/age-group translation rather than integrating bidirectional + shared-target counterfactual verification into a calibrated reject-option pipeline.
- **Relationship to AAFV-Net:** Key generative aging precedent in TIFS; contrasts directly with AAFV-Net's StyleGAN/SAM evidence extraction and shows why TIFS authors explicitly audit identity drift during synthetic age progression.

### P12. Look-Alike Hard Impostors & Longitudinal Drift (2014)
- **Exact Title:** *Double Trouble: Differentiating Identical Twins by Face Recognition*
- **Authors:** Jeffrey R. Paone, Patrick J. Flynn, P. Jonathon Phillips, Kevin W. Bowyer, Richard W. Vorder Bruegge, Patrick J. Grother, George W. Quinn, Matthew T. Pruitt, and Jason M. Grant
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 9, no. 2, pp. 285–295, Feb. 2014. DOI: `10.1109/TIFS.2013.2296373`
- **Research Problem:** Quantifies worst-case false-accept failure modes when genetic look-alikes / identical twins collide under cross-year elapsed time and illumination shifts.
- **Datasets & Protocol:** ND-Twins (same-day and cross-year sessions) evaluated across multiple NIST/commercial matchers via EER and FAR across covariates.
- **Main Results:** Demonstrates orders-of-magnitude FAR/EER spikes on look-alike impostors compared to general background populations, particularly across time lapses.
- **Relationship to AAFV-Net:** Provides authoritative historical justification in TIFS for why AAFV-Net evaluates **both random impostors ($\mathcal{D}_{\text{random}}$) and look-alike hard impostors ($\mathcal{D}_{\text{hard}}$, $\mathcal{D}_{\text{neutral}}$)**, and explains why AAFV-Net's 5 residual false accepts on physically indistinguishable look-alikes reflect a fundamental biometric boundary.

### P13. Demographic Disparities in Face Biometrics (2012)
- **Exact Title:** *Face Recognition Performance: Role of Demographic Information*
- **Authors:** Brendan F. Klare, Mark J. Burge, Joshua C. Klontz, Richard W. Vorder Bruegge, and Anil K. Jain
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 7, no. 6, pp. 1789–1801, Dec. 2012. DOI: `10.1109/TIFS.2012.2214212`
- **Research Problem:** Systemic verification accuracy disparities across gender, race/ethnicity, and age brackets (18–30 vs. older cohorts).
- **Main Results:** Showed lower verification accuracy for females, Black subjects, and young adults; demonstrated impact of demographic training balance and dynamic matcher routing.
- **Relationship to AAFV-Net:** The canonical TIFS citation anchoring our Demographic Parity Audit (Table VII) and explaining why pediatric/youthful cohorts and sex-disaggregated false-accept audits are mandatory in TIFS submissions.

### P14. Quality-Dependent & Missing-Data Multimodal Score Fusion (2009)
- **Exact Title:** *Benchmarking Quality-Dependent and Cost-Sensitive Score-Level Multimodal Biometric Fusion Algorithms*
- **Authors:** Norman Poh, Thirimachos Bourlai, Josef Kittler, *et al.*
- **Publication Details:** *IEEE Trans. Inf. Forensics Security*, vol. 4, no. 4, pp. 849–866, Dec. 2009. DOI: `10.1109/TIFS.2009.2034885`
- **Research Problem:** Score-level biometric fusion systems degrade sharply when auxiliary channels fail (failure-to-acquire/match) or input quality fluctuates across sensors.
- **Datasets & Protocol:** BioSecure DS2 benchmark (22 submitted algorithms across 24 score/quality channels), evaluated via fixed-threshold **HTER** on held-out evaluation sets and missing-observation masking (10%–40% dropout).
- **Relationship to AAFV-Net:** **Direct methodological ancestor in TIFS!** Poh *et al.* explicitly established quality-conditioned multimodal score fusion and training/evaluation under channel masking/missing observations—making it essential to cite alongside AAFV-Net's quality index $Q$, synthesis reliability $R_{\text{sam}}$, and 12% branch dropout!

---

## 4. Writing Style and Structural Analysis of TIFS Publications

Studying the structure and presentation of these TIFS exemplars reveals distinct, rigorous rhetorical norms:

### A. Introduction
1. **Risk-First Threat/Operational Framing:** TIFS papers do not open with generic deep learning hype; they immediately frame an *operational forensic or security vulnerability* (e.g., template inversion SAR in P9, uncalibrated overconfidence under noise in P5, worst-case twin FAR spikes in P12, strategic threshold evasion in P2).
2. **Critique Through Mathematical/Empirical Failure Modes:** Prior work is critiqued on *fundamental structural guarantees* (e.g., deterministic embeddings lacking variance bounds in P6, point thresholds failing under non-stationary distributions in P2, aggregate accuracy ignoring calibration ECE in P5).
3. **Methodological Bridge:** Before listing bullet contributions, TIFS introductions explain *why* the proposed paradigm resolves the failure mode conceptually, accompanied by an overview Figure 1 contrasting the flawed paradigm against the proposed security property.
4. **Measured Contribution Statements:** Contributions state exact theoretical, architectural, or empirical breakthroughs without promotional adjectives ("novel", "revolutionary", "dramatic").

### B. Related Work
1. **Problem-Driven Taxonomy:** Literature is organized by *technical paradigm* (e.g., discriminative embedding invariance vs. generative synthesis vs. uncertainty calibration vs. biometric fusion), rather than chronologically summarizing one paper per sentence.
2. **Synthesis & Contrast:** Each paragraph explicitly ends by identifying the *unsolved security or reliability limitation* shared by that cluster of papers and contrasting it directly against the proposed system.
3. **Domain Precision:** Cross-domain papers (e.g., general CV/NLP baselines) are integrated strictly to illuminate why naive transfer fails on high-assurance security tasks (like P5 explaining why standard Temperature Scaling underperforms ASC on angular embeddings).

### C. Methodology
1. **Formal Problem Setting First:** TIFS papers formally define input spaces, hypothesis spaces ($H_0$ vs. $H_1$), decision rules, and assumptions *before* drawing neural network diagrams (e.g., P2's Neyman-Pearson setup, P5's probabilistic calibration formulation, P14's channel masking definition).
2. **Design Rationale Coupled to Equations:** Equations are not dropped mechanically; each loss term, normalization formula, and guard condition is followed by its physical or statistical rationale (e.g., explaining *why* reliability $R_{\text{sam}}$ scales variance across shared targets and *why* guards $\rho$ prevent $T_{\text{acc}}$ collapse).
3. **Complete Reproducibility Specification:** Per TIFS Deep Learning Guidelines, successful TIFS methods explicitly report input normalization, architecture layer dims, initialization, optimizer, learning rate schedule, loss weights, and split stratification.

### D. Experimental Evaluation
1. **Strict Separation of Development/Calibration and Held-Out Evaluation:** Exemplified by P14 (fixing decision thresholds on a development set and testing generalization via HTER on an independent set) and P9 (evaluating strictly at fixed low FMR operating points such as $10^{-3}$ or $10^{-5}$).
2. **Multi-Scenario Stress Testing:** TIFS expects evaluation across (i) in-distribution splits, (ii) OOD cross-dataset transfer (P1, P3, P7), (iii) hard/adversarial cohorts (P2, P9, P12), and (iv) demographic or quality-degraded strata (P6, P13).
3. **Statistical Rigor:** Reporting both point performance and uncertainty (cluster confidence intervals, calibration error ECE, reliability diagrams, and variance across runs).

### E. Results, Discussion, and Limitations
1. **Observation vs. Interpretation Separation:** Tables present exact observations cleanly; prose explains causal mechanisms (especially **negative results**, such as why Siamese ViT hits high AUC yet collapses at zero-FA thresholding, or why pediatric growth breaks adult generative models).
2. **Transparent Boundary Conditions:** TIFS reviewers reward frank boundary disclosures (scope of statistical assumptions, failure cases on identical/look-alike pairs, computational latency bottlenecks).

### F. Figures and Tables
1. **Information-Dense Plots:** Trade-off plots (DET curves, ROC/EROC, calibration reliability diagrams, operating-point Pareto plots) and cleanly routed system schematics with explicit stage groupings.
2. **Self-Contained Captions:** Captions specify dataset, split, fixed operating constraint ($\beta$ or FMR), and main takeaway in crisp technical prose.
3. **Consistent Typographical Discipline:** Roman numerals for tables (`TABLE I`), `Fig. #.` below figures, explicit $N$ in headers, uniform decimal precision.

---

## 5. Patterns to Adopt vs. Key Differences in `AAFV-02.pdf`

| Dimension | Best Practices Observed in TIFS Exemplars | Current Gap / Difference in `AAFV-02.pdf` | Action Needed in Phases 3–7 |
|---|---|---|---|
| **Literature Positioning** | Deep integration of TIFS biometric fusion (Poh 2009), demographic error analysis (Klare 2012), look-alike FAR (Paone 2014), progressive aging (Huang 2021), confidence calibration (Xu 2024), UCFace (Ahn 2024), OrdCon AIFR (Wang 2025). | Current Related Work lacks *any* of these TIFS biometric calibration, fusion, uncertainty, twin/look-alike, or fairness studies (relying mainly on general CV conferences: CVPR/ECCV/ICLR). | Integrate these verified TIFS pillars into Related Work with a structured comparison matrix contrasting decision guarantees and calibration mechanisms. |
| **Statistical & Decision Framing** | Explicit separation of fixed-threshold generalization vs. rank AUC (Poh 2009, Xu 2024); explicit distinction between random background and adversarial evasion distributions (Hu 2025). | Bounds are introduced cleanly, but lack calibration diagnostics (**ECE / Reliability Diagram**, cf. Xu 2024) and could sharpen the comparison with quality-dependent score fusion (Poh 2009). | Compare explicitly against calibration/quality-fusion literature; check whether ECE/reliability can be computed offline from calibration/Look-1 audit scores without touching protected test budget! |
| **Deep Learning Method Disclosure** | Complete hyperparameter, optimizer, LR schedule, normalization, and loss weighting disclosure inside Methodology text. | `main.tex` omits MLP optimizer, learning rate, initialization, epoch count, input feature scaling, and exact gap-balanced BCE weighting formula. | Audit `scripts/p6_train.py`, `p5_vectors.py`, and `p78_calibrate_freeze.py` to report every training hyperparameter truthfully. |
| **Figure Citations & Visual Density** | Every figure and table is analytically integrated into the narrative with sequential `\ref{}` links. | 5 of 7 figures (`Fig. 2, 3, 4, 5, 7`) are never cited via `\ref{}` in the prose, leaving plots orphaned from explanation! | Cite every figure sequentially and weave quantitative takeaways directly into Results/Ablations. |
| **Tone & Terminology** | Measured forensic security prose ("establishes an empirical operating point...", "mitigates hard impostors..."); no promotional phrasing. | Occasional promotional phrasing ("catastrophic", "unprecedented", "complete collapse", "occupies the optimal quadrant") and informal bullets instead of cohesive TIFS paragraphs. | Refine academic prose to sober, technically disciplined IEEE Transactions register. |

---

## 6. Phase 2 Summary of Findings & Unresolved Questions

### Summary of Findings
1. Verified **14 authentic TIFS publications** (10 from 2022–2026 and 4 foundational 2009–2021 biometric security pillars) spanning cross-age AIFR, Neyman-Pearson detection under evasion, probability calibration (ASC), open-set quality uncertainty (UCFace), progressive aging (PFA-GAN), look-alike twins, demographic fairness, and quality-dependent missing-branch score fusion (Poh *et al.*).
2. Established that AAFV-Net's closest conceptual relatives inside TIFS are **Poh *et al.* (2009)** (quality-conditioned multimodal score fusion under missing channels), **Xu *et al.* (2024)** (confidence calibration in face verification), **Ahn *et al.* (2024)** (quality-linked uncertainty in open-set recognition), and **Wang *et al.* (2025) / Huang *et al.* (2021)** (AIFR and progressive generative aging).
3. Identified concrete stylistic and methodological gaps between `AAFV-02.pdf` and published TIFS norms (template class mismatch, missing DL hyperparameters, missing ECE/calibration comparison context, 5 unreferenced figures, promotional wording).

### Unresolved Questions for Subsequent Phases
1. **Exact Training Hyperparameters (Phase 5):** Need to inspect `Code/AAFV_Net/scripts/p6_train.py`, `p5_vectors.py`, and `p78_calibrate_freeze.py` to extract exact optimizer, LR, epochs, normalization, and gap-balancing weights required by TIFS Deep Learning guidelines.
2. **Offline Calibration Reliability Diagnostics (Phase 5/7):** Check whether existing saved calibration artifacts (`Code/AAFV_Net/ablations/variants/*/calibration.json` or `frozen.pkl`) allow computing calibration metrics (e.g., ECE) on the **calibration split** (without touching the exhausted test split) to align directly with Xu *et al.* (TIFS 2024).
3. **Paywalled Full-Text Details:** Full PDFs of Wang *et al.* (2025) and Mao & Li (2025) could not be retrieved behind the IEEE Xplore paywall; therefore, exact table cell numbers beyond their verified abstract gains remain unverified and will not be fabricated.

---

**Phase 2 Status:** **COMPLETE.** Ready to proceed to **Phase 3 — Reassess the Current AAFV-Net Literature Review** upon your confirmation.
