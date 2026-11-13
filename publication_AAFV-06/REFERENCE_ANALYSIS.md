# Reference analysis across all versions (BASE_Paper → AAFV-06)

**Does changing the target venue change the paper?** No, not the science. The evidence, the methods, the results and what may be claimed are the same for any venue.
The venue changes only:
- the format (template, page limit, anonymity);
- the required statements (AI use, ethics, data);
- how much space related work gets.

AAFV-05 had cut the bibliography to fit a short paper. That was a length decision, not a judgement that the other references were irrelevant. AAFV-06 restores every prior reference that the expanded text genuinely uses.

Sources compared (extracted by `scripts/collect_references.py` into `reference_sources.txt`):

| Version | References |
|---|---|
| BASE_Paper.pdf | 44 numbered |
| AAFV-01.pdf | ≈ 26 |
| AAFV-02.pdf | ≈ 26 |
| AAFV-03 (`publication_tifs/references.bib`) | 41 |
| AAFV-04 (`AAFV-04_revision/manuscript/references.bib`) | 69 |
| AAFV-05 | 48 |
| **AAFV-06** | **90** (68 from AAFV-04, 19 newly verified, 3 standard) |

## 1. Reused from AAFV-04 (68 entries, all cited in AAFV-06)
AAFV-04's bibliography was audited in AAFV-03/04 (corrupted DOIs fixed; the fabricated ICASSP entry removed). Every entry below is cited for a specific statement in AAFV-06:
- **Age-invariant recognition and aging:** Li 2011, OE-CNN, DAL, MTLFace (CVPR), OrdCon, AIM, Best-Rowden & Jain, Deb (children), CAAE, IPCGAN, PFA-GAN, SAM, StyleGAN2.
- **Recognition and similarity measures used by AAFV-Net:** CosFace, ArcFace, MagFace, AdaFace, VGG-Face, EfficientNet, LPIPS, SSIM; Siamese networks (Chopra), ViT, LoRA, Qwen2-VL (the comparators in the original results).
- **Fusion, quality, uncertainty, calibration:** Kittler, Ross & Jain, Nandakumar, Poh, PFE, UCFace, Xu (ASC), Platt, Zadrozny & Elkan, Guo, Naeini, Brier.
- **Reject option and risk control:** Chow, Herbei & Wegkamp, El-Yaniv & Wiener, Geifman & El-Yaniv, Vovk, conformal risk control, Learn-then-Test, Tibshirani (covariate shift), Hanley & Lippman-Hand, Clopper–Pearson, Bolle (subsets bootstrap), Schuckers, ISO/IEC 19795-1.
- **Threat model, demographics, attacks, privacy:** Paone (twins), Klare, Grother (FRVT Part 3), Krishnapriya, Buolamwini & Gebru, Phillips (PNAS), Scherhag (morphing), ISO/IEC 30107-3, Otroshi (template inversion), Razeghi (privacy funnel), Zhou (open-set deepfake detection), Hu (Neyman–Pearson under strategic evasion).
  The last four were the entries Phase 7 called "padding". In AAFV-06 they are cited where they support a real statement: the threat-model and ethics discussion (attacks on templates, synthetic-face detection, strategic impostors). Each was audited in AAFV-03/04, and none is used for a claim it does not make.
- **Datasets:** MORPH, FG-NET, AgeDB, CACD, CALFW, IJB-C.

**Dropped from AAFV-04 (1):** Osorio-Roig et al., multi-biometric indexing. Nothing in AAFV-06 concerns biometric indexing.

## 2. New, verified on 2026-11-13/14 (19 entries)
| Entry | Why it is needed | Checked against |
|---|---|---|
| Richardson et al., pSp, CVPR 2021 | SAM is built on the pSp encoder (architecture section) | CVF open access |
| Rothe et al., DEX, IJCV 2018 | Age estimator inside R_sam | IJCV listing |
| Guo et al., SCRFD, ICLR 2022 | Fallback face detector | ICLR / InsightFace |
| Immerkær, CVIU 1996 | Noise term of the quality score Q | Journal listing (vol. 64(2), pp. 300–302) |
| Or-El et al., Lifespan, ECCV 2020 | Alternative aging generator | ECVA open access |
| Chen & Lathuilière, FADING, BMVC 2023 | Second generator in the protocol | BMVC / arXiv |
| Banerjee et al., IJCB 2023 | Closest prior work (synthetic aging as training data, independent-recognizer check) | arXiv, read |
| Luevano et al., IJCB 2025 | Identity-preserving StyleGAN aging | arXiv, read |
| Huang et al., MTLFace TPAMI | FT-Sel and the ECAF benchmark | arXiv, read |
| Qi et al., MyTimeMachine, TOG 2025 | Personalized aging | arXiv |
| Su et al., TimeBooth, ICCV 2025 | Recent aging representation | CVF open access (listing) |
| Dahan & Keller, arXiv 2023 | AgeDB-30 saturation | arXiv, read |
| Chang et al., DUL, CVPR 2020 | Data uncertainty | CVF open access |
| Kendall & Gal, NIPS 2017 | Learned loss attenuation (proposed model) | NeurIPS proceedings |
| Deng et al., Sub-center ArcFace, ECCV 2020 | Label-noise-tolerant training | ECVA |
| Terhörst et al., SER-FIQ, CVPR 2020 | Recognizer-based quality | CVF open access |
| Boutros et al., CR-FIQA, CVPR 2023 | Recognizer-based quality | arXiv / CVPR listing |
| Boutros et al., IDiff-Face, ICCV 2023 | Synthetic data for face recognition | arXiv |
| Bianco, LAG, PRL 2017 | Large-age-gap dataset | Publisher repository listing |

Fields not confirmed (some page numbers) were left out, not guessed.

## 3. Standard references, not re-looked-up online (3) — re-check before submission
He et al., ResNet (CVPR 2016); King, Dlib-ml (JMLR 2009); Efron & Tibshirani, *An Introduction to the Bootstrap* (1994). Their details match the BASE_Paper list and are widely known, but they were not checked against a source in this session.

## 4. Prior references that must NOT be reused (fabricated, corrupted or misattributed)
| Version | Entry as printed | Problem |
|---|---|---|
| AAFV-01 [7] | J. Liu, Y. Tu, S. Yan, "DAL: Dual-attention-guided latent identity representation…", ACM MM 2019 | DAL is Wang et al., *Decorrelated Adversarial Learning*, CVPR 2019. This entry is misattributed and probably fabricated |
| AAFV-01 [10] | Y. He et al., "Deep cross-age face verification with residual age progression," ICASSP 2019 | Removed in AAFV-03 as corrupted (`he2019defrcn`); no such paper was found |
| BASE [26] | J. Chen et al., "FADING: Facial aging and identity preservation for age-invariant face recognition," IEEE T-BIOM 2023 | The real FADING is Chen & Lathuilière, *Face Aging via Diffusion-based Editing*, BMVC 2023 (different title, authors and venue) |
| BASE [35] | H. Huang et al., "AIM: Appearing for identity manipulation in face ageing…," ICCV 2019 | AIM is Zhao, Yan & Feng, *Towards Age-Invariant Face Recognition*, TPAMI 2022; this entry is misattributed |
| BASE [27] | Z. Chen et al., "DiffAge: Lifespan age transformation via diffusion models…," CVPR 2024, pp. 1–10 | Not found; "pp. 1–10" is a placeholder pattern |
| BASE [44] | W. Li et al., "Aging-diffusion…," ECCV 2024 | Not found |
| BASE [21]/[22] | AdaFace twice: once missing an author; once as a TPAMI 2024 "extended journal version" | The CVPR 2022 paper is Kim, Jain & Liu; the TPAMI version could not be confirmed |
| BASE [23] | CurricularFace "and its extensions," IJCV 2023 | Journal version not confirmed (the CVPR 2020 paper is real) |
| BASE [30] | "Zi, J., al.: TransFace," ICCV 2023 | Author list garbled; not used |
| BASE [29] | TopoFR, NeurIPS 2023 | Venue/year not confirmed; not used |

The rule for any future version: a reference enters the bibliography only after its title, authors and venue have been checked against the publisher, CVF/ECVA open access or arXiv, and only if the text cites it for a statement the reference actually makes.
