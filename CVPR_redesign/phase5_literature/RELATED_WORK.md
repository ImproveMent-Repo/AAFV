# Phase 5: Research Literature and Related Work

> Brief Section 5: identify what existing approaches have solved, what remains open, where AAFV-derived work can contribute, which methods must be baselines, and which papers are essential. Use only verifiable references.
> Prepared 2026-11-13. Nothing was installed or run.

**How references were checked.**
- **[B]:** already in `AAFV-04_revision/manuscript/references.bib` (audited in AAFV-03/04).
- **[V]:** title, authors and venue confirmed today on the publisher page, CVF open access or arXiv (source links in Section 9).
- **[R]:** abstract and method sections read today, so the technical claim made here was checked.
- **[?]:** not yet verified. Must not be cited until checked.

No claim below goes beyond what the cited abstract or method section states.

---

## 1. Age-invariant face recognition (AIFR): discriminative representations
| Work | Venue | What it does | Status |
|---|---|---|---|
| Li, Park & Jain, *A Discriminative Model for Age Invariant Face Recognition* | IEEE TIFS 2011 | Discriminative subspace model, pre-deep-learning | [B] |
| Wang et al., *Orthogonal Deep Features Decomposition for AIFR* (OE-CNN) | ECCV 2018 | Splits deep features into orthogonal identity and age components | [B] |
| Wang et al., *Decorrelated Adversarial Learning for AIFR* (DAL) | CVPR 2019 | Adversarially decorrelates identity and age features | [B] |
| Hou, Li & Wang, *Disentangled Representation for AIFR: A Mutual Information Minimization Perspective* | ICCV 2021 | Disentangles identity and age by minimising mutual information | [V] |
| Dahan & Keller, *Age-Invariant Face Embedding using the Wasserstein Distance* | arXiv 2023 | Separate identity and age encoders with a Wasserstein discriminator; AgeDB-30 98.4–98.6% | [V][R] |
| Wang, Sanchez, Li & Clarke, *From Age Estimation to AIFR: Order-Enhanced Contrastive Learning* (OrdCon) | IEEE TIFS 2025 | Aligns feature differences with the ordinal ageing direction; cross-dataset results | [B] |

**Solved:** strong age-invariant embeddings when trained end-to-end; AgeDB-30 near saturation (≈98%).
**Open:**
- All of these *retrain the backbone* to remove age. None adapts a frozen modern recognizer.
- Evaluation is mostly fixed-threshold accuracy on balanced protocols (AgeDB-30, CALFW), not TAR at low FMR per gap bin or risk–coverage.
- Whether age invariance survives at gaps beyond the training distribution is seldom reported separately.

## 2. Joint age synthesis and recognition
| Work | Venue | What it does | Status |
|---|---|---|---|
| Zhao, Yan & Feng, *Towards Age-Invariant Face Recognition* (AIM) | IEEE TPAMI 2022 | Joint cross-age synthesis and recognition; introduces the CAFR benchmark | [B] |
| Huang, Zhang & Shan, MTLFace | CVPR 2021 | Attention-based identity/age decomposition plus age synthesis | [B] |
| Huang, Zhang & Shan, MTLFace journal version | IEEE TPAMI 2022 (arXiv 2210.09835) | Adds **FT-Sel**: fine-tunes on synthesized faces *selected by a two-component GMM over face-quality scores*. Introduces the **ECAF** child–adult benchmark | [V][R] |

**Solved:** synthesis and recognition can regularise each other, and selecting good synthetic faces helps.
**Open:**
- Selection is a hard filter on a *quality* score, not an *identity-preservation* score measured independently.
- The recognizer is retrained.
- There is no per-gap uncertainty and no reject option.

**This is the closest prior art to direction D.1, and FT-Sel must be a baseline.**

## 3. Face age progression and identity preservation (generators)
| Work | Venue | Relevance | Status |
|---|---|---|---|
| Zhang, Song & Qi, CAAE | CVPR 2017 | Early conditional autoencoder aging | [B] |
| Tang et al., IPCGANs | CVPR 2018 | Identity-preserving conditional GAN | [B] |
| Huang et al., PFA-GAN | IEEE TIFS 2021 | Progressive aging GAN | [B] |
| Alaluf, Patashnik & Cohen-Or, **SAM** (age transformation) | ACM TOG 2021 | Generator used by AAFV-Net (not "Segment Anything") | [B] |
| Karras et al., StyleGAN2 | CVPR 2020 | SAM's generator | [B] |
| Chen & Lathuilière, **FADING** | BMVC 2023 | Diffusion aging via null-text inversion and attention control; second generator in Experiment 0 | [V] |
| Banerjee et al., *Identity-Preserving Aging of Face Images via Latent Diffusion Models* | IJCB 2023 | DreamBooth-style aging; **fine-tunes ArcFace on about 3,400 age-edited images** after a quality threshold; checks identity with a recognizer different from its loss's | [V][R] |
| Luevano, Korshunov & Marcel, *Identity-Preserving Aging and De-Aging of Faces in the StyleGAN Latent Space* | IJCB 2025 | Linear SVR age direction in W space; two recognizers for identity checks; releases synthetic set | [V][R] |
| Qi et al., *MyTimeMachine: Personalized Facial Age Transformation* | ACM TOG 2025 (SIGGRAPH) | Learns *person-specific* aging from 10–50 photos of the same person | [V] |
| Su et al., *TimeBooth* | ICCV 2025 | Disentangled age prompt for diverse, personalized aging | [V] (method details not read) |
| Zou et al., *DiverAge* | arXiv 2026 | Diffusion aging guided by a real-data, per-age-bin cross-age identity-similarity prior | [V][R] |

**Solved:** photorealistic aging, with growing attention to identity, diversity and personalization.
**Open:**
- Identity preservation is usually reported as one average cosine, often from a recognizer tied to the training loss, and rarely per facial region or per age direction.
- Generated faces are seldom tested as *verification evidence* at matched FMR.
- Our own audit (`image_audit/IMAGE_AUDIT.md`) shows SAM edits concentrated on eyes and brows, which is exactly the cue recognizers use.

## 4. Face-recognition backbones and quality
| Work | Venue | Role | Status |
|---|---|---|---|
| Wang et al., CosFace | CVPR 2018 | Margin loss | [B] |
| Deng et al., ArcFace | CVPR 2019 | Baseline backbone | [B] |
| Deng et al., *Sub-center ArcFace: Boosting Face Recognition by Large-scale Noisy Web Faces* | ECCV 2020 | Training robust to **label noise**; relevant to the MORPH label-noise finding | [V] |
| Meng et al., MagFace | CVPR 2021 | Backbone; feature magnitude doubles as quality | [B] |
| Kim, Jain & Liu, AdaFace | CVPR 2022 | Primary frozen backbone; feature norm as quality | [B] |
| Terhörst et al., SER-FIQ | CVPR 2020 | Unsupervised quality from embedding robustness | [V] |
| Boutros et al., CR-FIQA | CVPR 2023 | Quality as relative classifiability | [V] |

**Solved:** strong generic verification; built-in quality signals.
**Open:** these models' behaviour as a function of *age gap*, with per-gap uncertainty, is not characterised. Their quality signals measure capture quality, not the reliability of a *synthetic* face.

## 5. Uncertainty and learning from unreliable targets
| Work | Venue | Relevance | Status |
|---|---|---|---|
| Shi & Jain, Probabilistic Face Embeddings (PFE) | ICCV 2019 | Gaussian embeddings on a fixed backbone. **Closest structural analogue to a frozen-backbone head with uncertainty** | [B] |
| Chang et al., *Data Uncertainty Learning in Face Recognition* (DUL) | CVPR 2020 | Learns embedding mean and variance; uncertainty reduces the impact of noisy samples | [V] |
| Kendall & Gal, *What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?* | NeurIPS 2017 | Input-dependent aleatoric uncertainty as learned loss attenuation: the mechanism D.1 uses to weight synthetic targets | [V] |
| Ahn et al., UCFace | IEEE TIFS 2024 | Uncertainty-aware embeddings for open-set evaluation | [B] |
| Xu, Zhang & Zhou, *Confidence-Calibrated Face and Kinship Verification* | IEEE TIFS 2024 | Post-hoc score calibration | [B] |

**Solved:** per-sample uncertainty for face embeddings; learned attenuation of noisy targets.
**Open:** uncertainty *conditioned on age gap*, and learned attenuation applied to *synthetic aging supervision* and validated against independent identity preservation.

## 6. Synthetic data for face recognition
| Work | Venue | Relevance | Status |
|---|---|---|---|
| Bae et al., DigiFace-1M | WACV 2023 | Rendered synthetic identities for FR training | [V] |
| Boutros et al., IDiff-Face | ICCV 2023 | Identity-conditioned diffusion for synthetic FR training data | [V] |

**Solved:** synthetic identities can train competitive recognizers.
**Open:** synthetic *intra-identity aging* as supervision, and how much of it to trust per sample.

## 7. Selective verification, reject option and risk control
Chow 1970 [B]; Herbei & Wegkamp 2006 [B]; El-Yaniv & Wiener 2010 [B]; Geifman & El-Yaniv 2017 [B]; Vovk et al. 2005 [B]; Angelopoulos et al., *Conformal Risk Control* (ICLR 2024) [B]; *Learn Then Test* (arXiv 2021) [B]; Tibshirani et al., *Conformal Prediction Under Covariate Shift* (NeurIPS 2019) [B]; Platt 1999, Zadrozny & Elkan 2002, Guo et al. 2017, Naeini et al. 2015, Brier 1950 [B].

**Solved:** finite-sample guarantees under exchangeability, weighted variants under covariate shift, and calibration diagnostics.
**Open (for us):** applying them correctly when impostor comparisons share identities (needs subset/cluster methods: Bolle et al. 2004 [B], Schuckers 2010 [B]), and under dataset shift (the FG-NET false-reject failure).
In the CVPR paper this is a supporting *application layer*, not the contribution.

## 8. Data, evaluation practice, demographics
**Datasets:**
- MORPH (Ricanek & Tesafaye 2006) [B]
- FG-NET (Lanitis et al. 2002) [B]
- AgeDB (Moschoglou et al. 2017) [B]
- CACD / CARC (Chen et al. 2014) [B]
- CALFW (Zheng et al. 2017) [B]
- IJB-C (Maze et al. 2018) [B]
- ECAF (in MTLFace TPAMI) [V]
- LAG: Bianco, *Large Age-Gap Face Verification by Feature Injection in Deep Networks*, Pattern Recognition Letters 90, 2017 [V]

**Longitudinal studies:** Best-Rowden & Jain, TPAMI 2018 [B]; Deb et al., child faces, ICB 2018 [B].

**Practice and demographics:** ISO/IEC 19795-1 [B]; Klare et al., TIFS 2012 [B]; Grother et al., NISTIR 8280 [B]; Krishnapriya et al., IEEE TTS 2020 [B]; Buolamwini & Gebru 2018 [B]; Phillips et al., PNAS 2018 [B]; Paone et al. (twins), TIFS 2014 [B].

---

## 9. Synthesis

### 9.1 What existing work has already solved
1. Age-invariant embeddings trained end-to-end (Sections 1 and 2) that perform near ceiling on balanced cross-age protocols.
2. Photorealistic, increasingly identity-aware aging generators (Section 3).
3. Training recognizers on selected synthetic aged faces (MTLFace FT-Sel; Banerjee et al. 2023).
4. Per-sample embedding uncertainty and learned attenuation of noisy targets (Section 5).
5. Distribution-free risk control and calibration (Section 7).

### 9.2 What remains open (each item checked against the papers above)
1. **No method adapts a *frozen* recognizer to age gap in embedding space with gap-dependent uncertainty.** Prior AIFR retrains the backbone; PFE and DUL model uncertainty but not age.
2. **The trust placed in synthetic aging supervision is decided by quality filters** (FT-Sel's GMM; Banerjee's threshold), not by a learned, continuous reliability that is checked against identity preservation under an *independent* recognizer.
3. **Long-gap behaviour is under-measured.** Benchmarks report pooled accuracy, and AgeDB-30 is saturated. TAR at low FMR per gap bin (≥ 15 y, ≥ 20 y) is rarely reported.
4. **Generated faces as verification evidence** have not been tested at matched FMR against the recognizer alone. AAFV's own logs show no measurable value on MORPH (`log_analyses/LOG_FINDINGS.md`).
5. **Data hygiene in longitudinal sets.** Our analysis indicates that MORPH long-gap genuine pairs in this pipeline are dominated by label errors. We found no paper reporting this, but a targeted search is still needed before claiming it as new.

### 9.3 Where AAFV-derived work can contribute
- **Primary, conditional on Experiment 0 = GO:** gaps 1–3. A frozen-backbone age-transport head with gap-dependent uncertainty, trained with reliability-weighted synthetic aging validated against an independent recognizer, and evaluated at low FMR per gap bin with a reject option.
- **Supporting:** gap 5, as a data-hygiene finding with a reproducible audit.
- **Supporting:** the three-way decision with cluster-aware, shift-checked thresholds, as the application section.
- **Not a contribution any more:** the five-score fusion, test-time SAM, R_sam, guards and the zero-FA certificate (`architecture_review/ARCHITECTURE_REVIEW.md`).

### 9.4 Positioning risk for a CVF venue
Searches of the CVF open-access index found AIFR papers at CVPR 2019 (DAL), CVPR 2021 (MTLFace) and ICCV 2021 (Hou et al.). They found **none at CVPR 2024/2025 or ICCV 2023** (the search was not exhaustive). Recent AIFR work appears mainly in TIFS, TPAMI and IJCB.
A CVPR-style submission should therefore be framed around the *general vision problem*: learning from unreliable generative supervision to handle a distribution shift (age gap) on a frozen foundation model, with cross-age verification as the testbed. That framing must be supported by the experiments, not just asserted.

## 10. Baselines (Phase 6 uses this list)
| Priority | Baseline | Why | Availability |
|---|---|---|---|
| Must | ArcFace (correctly aligned), AdaFace IR-101, MagFace iResNet-100, plain cosine | Strong generic recognizers; the backbone of every variant | Public weights (loaders checked, Stage-1 Section L) |
| Must | Gap-aware selective verifier (architecture review 3.1) | Our own simplest system; ablation base | Ours |
| Must | MTLFace (CVPR 2021 / TPAMI) incl. FT-Sel | Closest prior art | Public code at hzzone.github.io/MTLFace per the abstract; **weights [?]** |
| Must | Fine-tuning the recognizer on quality-filtered synthetic aged faces (Banerjee et al. style) | Closest prior art for synthetic supervision | Reimplementation |
| Should | PFE-style uncertainty head on the frozen backbone (no age conditioning) | Separates "uncertainty" from "age-conditioned transport" | Reimplementation |
| Should | OrdCon or another recent AIFR model, if weights are public | Recent AIFR comparison | **[?] availability** |
| Should | AAFV-Net (logged results only) | Continuity with AAFV-04 | Logs only; descriptive |
| Optional | Sub-center ArcFace, if MORPH label noise is used in training | Noise-robust training | Public |
| Drop | Siamese ResNet-18 / ViT (unconverged), Qwen2-VL-2B | Weak strawmen, flagged by the review | – |

## 11. Essential related-work list for the paper (about 30 entries)
- **Intro and problem:** Best-Rowden & Jain 2018; Grother et al. 2019; Deb et al. 2018.
- **AIFR:** OE-CNN 2018; DAL 2019; Hou et al. 2021; AIM 2022; MTLFace 2021 + TPAMI 2022; OrdCon 2025; Dahan & Keller 2023 (preprint; cite as such).
- **Aging:** SAM 2021; FADING 2023; Banerjee et al. 2023; Luevano et al. 2025; MyTimeMachine 2025; TimeBooth 2025; PFA-GAN 2021.
- **Backbones and quality:** ArcFace; Sub-center ArcFace; MagFace; AdaFace; SER-FIQ; CR-FIQA.
- **Uncertainty and noisy targets:** PFE; DUL; Kendall & Gal 2017.
- **Synthetic data:** DigiFace-1M; IDiff-Face.
- **Decision layer:** Chow 1970; Geifman & El-Yaniv 2017; Angelopoulos et al. 2024; Tibshirani et al. 2019; Bolle et al. 2004.
- **Data:** MORPH; FG-NET; AgeDB; CALFW; CACD; ECAF.

**Drop from the AAFV-04 bibliography** for a CVPR paper (unrelated or tied to removed components):
- EfficientNet, VGG-Face, LPIPS, SSIM (removed components);
- Qwen2-VL, LoRA, Siamese/ViT (dropped baselines);
- zhou2024openset (deepfake detection), osorioroig2024indexing (biometric indexing), otroshi2024inversion (template inversion), razeghi2026privacy (privacy funnel), hu2025neyman (strategic evasion), Kittler 1998, Ross & Jain 2003, Nandakumar 2008, Poh 2009 (score fusion, no longer the method).

Each can be kept only if the text genuinely uses it.

## 12. Still to verify before writing
1. MTLFace public **weights**; OrdCon code and weights.
2. ECAF size and availability on the MTLFace project page.
3. Exact DigiFace-1M composition (sources differ).
4. *Cross-Age Contrastive Learning for AIFR* (Wang et al., 2024): venue not confirmed. Do not cite yet.
5. The search snippet claiming a "10–40% improvement on cross-age verification without retraining" from synthesized faces: source not identified. Do not cite.
6. A systematic pass over CVPR/ICCV/ECCV 2023–2026 and TIFS/TBIOM 2024–2026 for "cross-age", "age-invariant", "longitudinal face", "synthetic aging" and "MORPH label noise".

**Sources checked today:**
[DUL](https://openaccess.thecvf.com/content_CVPR_2020/html/Chang_Data_Uncertainty_Learning_in_Face_Recognition_CVPR_2020_paper.html) ·
[SER-FIQ](https://openaccess.thecvf.com/content_CVPR_2020/papers/Terhorst_SER-FIQ_Unsupervised_Estimation_of_Face_Image_Quality_Based_on_Stochastic_CVPR_2020_paper.pdf) ·
[CR-FIQA](https://arxiv.org/pdf/2112.06592) ·
[IDiff-Face](https://arxiv.org/abs/2308.04995) ·
[DigiFace-1M](https://openaccess.thecvf.com/content/WACV2023/html/Bae_DigiFace-1M_1_Million_Digital_Face_Images_for_Face_Recognition_WACV_2023_paper.html) ·
[Sub-center ArcFace](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/1445_ECCV_2020_paper.php) ·
[FADING](https://arxiv.org/abs/2309.11321v1) ·
[TimeBooth](https://openaccess.thecvf.com/content/ICCV2025/html/Su_TimeBooth_Disentangled_Facial_Invariant_Representation_for_Diverse_and_Personalized_Face_ICCV_2025_paper.html) ·
[MyTimeMachine](https://arxiv.org/abs/2411.14521v2) ·
[Hou et al. ICCV 2021](https://openaccess.thecvf.com/content/ICCV2021/html/Hou_Disentangled_Representation_for_Age-Invariant_Face_Recognition_A_Mutual_Information_Minimization_ICCV_2021_paper.html) ·
[Kendall & Gal](https://papers.nips.cc/paper/2017/hash/2650d6089a6d640c5e85b2b88265dc2b-Abstract.html) ·
[MTLFace TPAMI](https://arxiv.org/abs/2210.09835) ·
[Banerjee et al.](https://arxiv.org/abs/2307.08585) ·
[Luevano et al.](https://arxiv.org/abs/2508.08808) ·
[DiverAge](https://arxiv.org/abs/2606.04881) ·
[Dahan & Keller](https://arxiv.org/abs/2305.02745) ·
[LAG](https://arxiv.org/pdf/1602.06149.pdf)
