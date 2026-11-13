# Phase 8: Manuscript Redesign Blueprint (deliverable F)

> Brief Section 8: propose a revised CVPR paper structure built around **one** central contribution, with sections, equations, tables, figures and related-work positioning. Verify the target edition's real requirements.
> **What this file is:** a blueprint, a paragraph-by-paragraph plan of what each part must say and which evidence supports it.
> **What it is not:** finished prose. Phase 7 explains why the authors should write the text themselves.
> **No result in this file exists yet.** Every number is a slot `[E#]` pointing to the Phase 6 experiment that will produce it.
> Prepared 2026-11-13.

## 1. Venue requirements (official CVPR 2027 Author Guidelines, read today)
| Rule | Requirement | Consequence for us |
|---|---|---|
| Length | 8 pages **including figures and tables**. References and the LLM Usage Statement go on extra pages | Page budget in §4 |
| **LLM Usage Statement** | Mandatory, after the main text and before the references. Name the tools, the affected parts (text, figures, code, experiments, related work) and the extent of use. Omitting it means desk rejection. Camera-ready: disclose AI-generated content in the Acknowledgments | Draft in §7. Must truthfully cover the AI assistance used in this project |
| Responsibility | "Authors … are fully responsible for everything they submit, and must be able to explain, reproduce and defend their work." Non-existent citations or factual fabrication lead to rejection | Matches the Phase 5 [V]/[R] rule and the Phase 7 advice |
| Template, anonymity | Official template. Double-blind. No identifying links; "code will be made publicly available" is allowed | Remove the GitHub URL, IIIT Nagpur and author names from the submission |
| Ethics | IRB statement or explanation; consent statement or explanation for human subjects; check existing datasets' consent; discuss negative societal impacts. **Withdrawn datasets (MS-Celeb-1M named) should not be used, or their use explained in detail** | Ethics paragraph (§3.9). **Backbone choice:** prefer AdaFace trained on WebFace4M/12M. MagFace's released model and AdaFace's MS1MV2 checkpoints are trained on MS1MV2 (derived from MS-Celeb-1M) and need explicit justification, or a non-MS1M alternative |
| Dual submission | No concurrent submission; arXiv allowed | – |
| Contemporaneous work | Public on or after 15 Sep 2026: cite and discuss | Re-run the Phase 5 search before submission |
| Findings Track | A separate track for technically sound papers with incremental novelty (piloted at CVPR 2026) | A realistic outlet if gains are modest |
| Dates | CVPR 2027 abstract deadline was 10 Nov 2026 (passed); paper deadline 16 Nov 2026 | **This blueprint targets ICCV 2027 or CVPR 2028.** Re-check that venue's guidelines; they are usually near-identical across CVF events |

## 2. One paper, two possible versions (decided by the Phase 6 gates)
| | **Paper A**: Gate A and Gate B pass (E0 = GO; E4 beats E2 at long gaps) | **Paper B**: a gate fails |
|---|---|---|
| Contribution | A learning method: reliability-weighted age transport on a frozen recognizer | An evaluation and analysis paper: what generated aging does and does not add to cross-age verification, with a data-hygiene finding |
| Venue | ICCV/CVPR main track (or the Findings track) | Biometrics venue (T-BIOM / IJCB / WACV) or a CVPR workshop |

The rest of this file details **Paper A**. Paper B is outlined in §9.

## 3. Paper A, section by section

**Working titles** (choose after results; none may overclaim):
1. *Trusting Synthetic Aging Selectively: Reliability-Weighted Age Transport for Long-Gap Face Verification*
2. *Learning How Faces Age in Embedding Space from Unreliable Synthetic Supervision*
3. *Age Transport on Frozen Face Recognizers*

**Central research question.** Can a frozen face recognizer be adapted to long age gaps by learning an age-conditioned transport in its embedding space? And can synthetic aged faces help train it, if each synthetic sample is weighted by a learned, independently validated reliability?

**Main hypothesis.**
- Long-gap verification fails mainly because genuine embeddings drift along person-dependent directions that real data cover too sparsely.
- A transport head trained on real pairs, plus synthetic pairs down-weighted by their identity reliability, recovers TAR at low FMR for gaps of 15 years or more without retraining the backbone.
- Unweighted synthetic data helps less or hurts.

**Contributions** (at most three; each tied to an experiment that must succeed before it is claimed):
1. **Method:** reliability-weighted age transport (RAT). A frozen-backbone head with gap-dependent vMF uncertainty, trained with a learned per-sample reliability on synthetic aging targets [E4, E6].
2. **Evidence:** a controlled study showing *when* generated aging carries identity information under independent recognizers, across two generators. This includes evidence that test-time synthesis does not help [E0, E5; AAFV logs].
3. **Protocol:** long-gap evaluation at low FMR per pre-registered gap bin, with person-disjoint folds, cluster-bootstrap intervals and a reject option. It comes with an audit showing that a widely used longitudinal set has unreliable long-gap labels [E1, E2, E3].

Each contribution is dropped if its experiment fails.

### 3.1 Abstract (150–200 words; written last)
Five sentences, in this order:
1. The problem: long-gap verification at low FMR.
2. Why existing approaches fall short: they retrain backbones; synthetic aging is trusted or filtered by quality; long gaps are rarely measured.
3. The idea (RAT).
4. The key evidence, as `[E4]` numbers at a stated FMR and gap bin.
5. One limitation.

### 3.2 Introduction (about 1 page)
| ¶ | Content | Evidence |
|---|---|---|
| 1 | Long-gap verification matters (passport renewal, missing persons). Genuine similarity decays with gap | Best-Rowden & Jain 2018; Fig. 1 left: TAR@FMR vs gap for AdaFace [E2] |
| 2 | Two existing routes and their limits: retrain for age invariance (OE-CNN, DAL, MTLFace, OrdCon), or synthesize the missing ages (SAM, FADING), with synthetic data trusted or quality-filtered (FT-Sel, Banerjee et al.) | Phase 5 §1–3 |
| 3 | **Probe (the SliderEdit-style observation):** generated aging moves the recognizer's embedding toward the true older face for some samples and away for others. Identity reliability varies per sample and is not captured by image quality | Fig. 2 [E0, E6]; qualitative panel (image audit: eye and brow edits) |
| 4 | The idea: learn the transport in embedding space and learn how much to trust each synthetic target. No generation at test time | Fig. 3 |
| 5 | Contributions (the three above) and a one-line summary of results `[E4]` | – |

### 3.3 Related work (about 0.75 page)
Four short paragraphs, each ending with how we differ (Phase 5 §9):
1. Age-invariant recognition.
2. Face aging and identity preservation.
3. Uncertainty and learning from unreliable targets (PFE, DUL, Kendall & Gal).
4. Synthetic data for face recognition, including the FT-Sel and Banerjee et al. contrast.

The selective-verification and risk-control literature appears only in §3.7.

### 3.4 Problem formulation (about 0.4 page)
Notation, used everywhere:
- Recognizer f (frozen); embedding e = f(I) ∈ 𝕊^{d−1}; ages a₁ ≤ a₂; gap Δ = a₂ − a₁.
- Generator G(I, t); independent recognizer h ≠ f.
- Transport T_θ; concentration κ_θ; reliability w_ψ.

**(1) Verification target:** decide y = 1[same identity] for (I₁, a₁, I₂, a₂) and report TAR at fixed FMR per gap bin.

**(2) Drift model** (motivates the method and is tested empirically):
 e(a₂) ≈ normalize(e(a₁) + δ(e(a₁), a₁, a₂)) + ε, where δ is person- and age-dependent and ε has a gap-dependent spread.

### 3.5 Method: Reliability-weighted Age Transport (about 1.75 pages)
**(3) Transport:** T_θ(e, a, t) = normalize(e + g_θ([e, γ(a), γ(t)])), with γ a sinusoidal age encoding.

**(4) Uncertainty:** κ_θ(e, a, t) > 0. The vMF likelihood is p(e′ | T, κ) ∝ C_d(κ) exp(κ · T⊤e′).

**(5) Real-pair loss:** L_real = −log C_d(κ) − κ · T_θ(e_y, a_y, a_o)⊤ e_o, symmetrised over the two directions.

**(6) Synthetic-pair loss with learned reliability** (heteroscedastic attenuation, following Kendall & Gal 2017):
 L_syn = Σ_s [ w_ψ(φ_s) · ℓ(T_θ(e_s, a_s, t_s), f(G(I_s, t_s))) − λ_w log w_ψ(φ_s) ].
 φ_s are reliability features of the generated face, computed with h: identity agreement h(G(I, t))⊤h(I), age error from an age estimator, and quality.
 Without the log term the trivial solution w = 0 would be optimal. **Check:** the exact form must be derived and stated, not copied from this sketch.

**(7) Impostor margin:** L_imp = Σ max(0, T(e_i, a_i, a_j)⊤ e_j − m) over gap-matched impostors, so the transport cannot collapse identities.

**(8) Objective:** L = L_real + β L_syn + η L_imp.

**(9) Score:** S = ½[κ₁₂ T(e₁, a₁, a₂)⊤ e₂ + κ₂₁ e₁⊤ T(e₂, a₂, a₁)], with ages estimated when unknown [E14].

**Training and inference:**
- Precompute f embeddings for real and generated faces once. Train the heads (5 seeds).
- Inference = two backbone passes + one MLP, with no generation.
- Report parameter count, FLOPs and latency [E11].

**What the method is not:** no backbone fine-tuning; no image-space fusion of similarity measures; no test-time synthesis. A sentence contrasting it with AAFV-04 goes in the supplement, not the main paper.

### 3.6 Experimental setup (about 0.6 page)
- **Datasets and strata:** Phase 6 §0. Long-gap evidence from AgeDB and FG-NET (plus ECAF as a child stratum). MORPH for short-gap training only, after the E1 audit.
- **Splits:** person-disjoint folds; a fresh calibration fold; one confirmatory look per external set.
- **Baselines:** Phase 5 §10.
- **Metrics:** TAR@FMR 10⁻³ and 10⁻⁴ per gap bin; ROC/DET; risk–coverage and AURC; AgeDB-30 accuracy for comparability only.
- **Statistics:** two-way person-cluster bootstrap; Holm correction within declared families.

### 3.7 Results (about 2 pages)
| Element | Content | Source |
|---|---|---|
| **Table 1 (main)** | Rows: cosine (ArcFace, AdaFace, MagFace), gap-calibrated cosine (E2), PFE-style head, MTLFace / FT-Sel, Banerjee-style fine-tune, RAT. Columns: TAR@FMR 10⁻³ per gap bin (0–4, 5–14, 15–29, 30+) on AgeDB and FG-NET-adult; AgeDB-30 accuracy | E2, E4, E7 |
| **Fig. 4** | TAR@FMR vs gap (line plot with CIs), RAT vs best baseline | E4 |
| **Fig. 5** | Risk–coverage at matched FAR; review workload vs automation | E2, E4, E3 |
| Short paragraph | The certified operating point: k-error order-statistic threshold, its assumptions, observed held-out FAR | E3 |

### 3.8 Ablations (about 1 page)
- **Table 2:** cumulative ablation ladder, rows 1–8 of Phase 6 §4. This is the SAM 3D Table-4 style: each row adds one component.
- **Table 3:** generator swap (SAM-age, FADING) × backbone swap.
- **Fig. 6:** learned reliability vs independent identity preservation (scatter plot with Spearman ρ), plus the harm/benefit flip rate by reliability decile [E6].

### 3.9 Qualitative analysis, limitations, ethics (about 0.75 page)
- **Fig. 7:** synthetic targets with high and low learned reliability, and where they change the face (eye and brow edits). Also successes and failures of RAT at long gaps [E10]. Only images whose licence allows publication.
- **Limitations:** dependence on age estimates; generator bias (infants and children); dataset demographics [E9]; recognizer pretraining overlap with celebrity test sets; scale of external sets.
- **Ethics and impact:**
  - IRB statement: existing datasets only; state whether review was obtained or why it was not.
  - Dataset consent and licences; MS1MV2-trained backbones justified or avoided.
  - Misuse risk (surveillance across decades) and mitigations; demographic findings [E9].

### 3.10 Conclusion (4–5 sentences)
What was shown, at which gaps and FMR, the main limitation, and one concrete next step.

### 3.11 LLM Usage Statement (outside the page limit; mandatory)
Must truthfully list:
- The AI tools used: the assistants used in this project (e.g. Claude, and any others the team used).
- The parts affected: literature search and verification, code for analysis scripts, consistency checks, and any text editing.
- The extent of use.

The authors write it; it is not filled in here. **The statement must match what actually happened.**

### 3.12 Supplementary material
- Full per-bin tables with CIs.
- Pre-registration files and deviations log.
- E0 report, E1 audit protocol, calibration diagnostics [E8], fairness [E9], runtime [E11], degradation [E12].
- The AAFV-04 → RAT history and the MORPH test-look chronology.
- Code statement ("will be made publicly available").

## 4. Page budget (8 pages)
| Section | Pages |
|---|---|
| Intro incl. Fig. 1 | 1.0 |
| Related work | 0.75 |
| Problem | 0.4 |
| Method incl. Fig. 2–3 | 1.75 |
| Setup | 0.6 |
| Results incl. Table 1, Fig. 4–5 | 2.0 |
| Ablations incl. Tables 2–3, Fig. 6 | 1.0 |
| Qualitative, limitations, ethics, conclusion incl. Fig. 7 | 0.5 |
| **Total** | **8.0** |

## 5. Figures (what each must show; drawn only after results exist)
| Fig. | Purpose | Lesson taken from the exemplars |
|---|---|---|
| 1 (teaser) | Left: TAR@FMR collapsing with gap for strong recognizers. Right: RAT recovering it at 15–29 / 30+ years | One image states the problem and the result (SAM 3D Fig. 1) |
| 2 (probe) | Generated targets help some samples and hurt others; reliability is not image quality | Show the observation before the method (SliderEdit Fig. 2) |
| 3 (method) | Training path (real + synthetic + reliability) vs test path (no generation) | One clean architecture figure with a clear train/test split (SliderEdit Fig. 3) |
| 4–6 | Results, risk–coverage, reliability validation | Metrics designed for the claimed property (SliderEdit continuity, disentanglement) |
| 7 | Qualitative successes and failures | Qualitative and quantitative evidence side by side |

## 6. Consistency rules for the writing
- One symbol per concept (§3.4 notation table); define every symbol before first use.
- Every number carries its denominator and source experiment ID in the draft. IDs are removed only at camera-ready.
- No claim without an experiment that supports it. Contributions are pruned if their experiment fails.
- Use "certified" only with the exact assumptions next to it.
- Never present an observed zero false accepts as a general guarantee.

## 7. Material from AAFV-04 that may be reused (after rewriting by the authors)
| Reuse | Do not reuse |
|---|---|
| The data hygiene and quarantine idea; person-disjoint protocol; cluster-bootstrap reporting; logged test budget; sample-size table (as supplement) | The five-score fusion, R_sam, guards and test-time SAM; the 0.349% headline; MORPH long-gap results; the Siamese/VLM baselines |

## 8. Writing order and ownership (suggested)
1. Problem and method (§3.4–3.5), by the person who implements E4.
2. Setup and results, by the people who run E2/E4.
3. Related work, by the person who did the Phase 5 verification.
4. Introduction, abstract and conclusion, last, by the lead author, with advisor review.
5. LLM statement and ethics: whole team.

## 9. Paper B outline (fallback)
**Working title:** *Does Synthetic Aging Help Cross-Age Face Verification? A Controlled Study with Independent Recognizers.*

**Contributions:**
1. A controlled study: E0 plus the AAFV ablation logs show no measurable identity value from generated aging at matched FMR.
2. A long-gap evaluation protocol with a reject option, and strong baselines [E2, E3].
3. A label-reliability audit of MORPH long-gap pairs [E1].

**Sections:** Intro, Related, Protocol, Generated-evidence study, Baselines, MORPH audit, Discussion.
**Venue:** biometrics (T-BIOM, IJCB, WACV) or a CVPR workshop.
