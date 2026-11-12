# AAFV-04 — Research Novelty Assessment

## Short answer

As it stands, AAFV-Net is **not yet a sufficient methodological contribution for IEEE TIFS or TPAMI**. Its components are pre-existing. The two elements that are new in this combination have weak or negative evidence:

- the shared-target age grid;
- reliability-gated synthetic evidence.

The strongest defensible contribution is at the **decision and evaluation-protocol level**:

- a three-way verification policy;
- a finite-sample FAR certificate obtained from calibration data;
- the empirical finding that branch-probability guards are needed to make a zero-false-accept threshold attainable on a fused score;
- an unusually transparent audit.

That is a reasonable paper for a biometrics venue if E1–E3 are completed. It is unlikely to clear TIFS on novelty without one of the directions in Section 4 below.

## 1. Component-by-component (mirrors manuscript Table I)

| Component | Existing technique | Adopted in AAFV-Net | AAFV-Net modification | Novel? | Evidence |
|---|---|---|---|---|---|
| Identity / perceptual similarity | ArcFace, VGG-Face, EfficientNet, LPIPS, SSIM | Yes, frozen | None | No | EfficientNet redundant; ArcFace indispensable (ablations) |
| Age progression | SAM; AIM couples synthesis and recognition | Yes, frozen | Used as an auxiliary channel, not a replacement | Framing only | Identity preservation **not measured** |
| Shared-target 5-year grid | Endpoint progression | — | Both faces rendered at common intermediate ages | New design choice | Lowers test accept 83.91 → 70.07%; neutral rejection +3.5 pp with overlapping CIs. **Not supported** as beneficial |
| R_sam reliability and branch masking | Quality-dependent fusion with missing channels (Poh et al. 2009); modality dropout | Partly | Reliability score built from identity, age, quality, and spread terms; masking at p = 0.12 | Adaptation | Masking necessary (3.60% without); R_sam as fusion input ~no effect; as guard, part of the guard family |
| Fusion MLP + Platt | Learned score fusion; Platt | Yes | Small MLP with context inputs | No | Context inputs necessary (0% without) |
| Accept rule (max impostor + margin) with guards | Selective classification; conformal / order statistics | Yes | Guards folded into the score; applied to cross-age verification | Application | Prop. 1 is a known result applied correctly; guard necessity is an empirical finding |
| Reject rule (β-quantile) | Chow; conformal quantile | Yes | — | No | Fails under shift (FG-NET 18.20% false rejects) |
| Audit protocol | ISO/IEC 19795-1, subset bootstrap, look budgets | Partly | Hash-sealed artifacts, look log, quarantine | Practice, not method | Adaptivity between looks not excluded |

## 2. Answers to the specific questions

1. **What is novel about the guarded three-way framework?** The three-way rule is Chow's reject option. Setting the accept threshold at the calibration impostor maximum is a conformal or order-statistic construction. What is specific here is folding quality, reliability, and branch-probability guards into the score before taking the maximum. Without the guards, the fused score's impostor tail reaches ~1.0 and the zero-FA threshold becomes unattainable (every guard ablation gives 0% acceptance). This is a useful, verified empirical observation, but it is not a new method.
2. **How does the fusion differ from conventional multimodal score fusion?** It differs mainly in that one "modality" is synthetic: generated faces are compared with the same five measures and weighted by a reliability score. Structurally, it is a learned combiner with quality context, in the line of Poh et al. and Nandakumar et al.
3. **What is the contribution of age-progression evidence?** It is unproven. The direct-only MLP fails to produce a usable accept threshold, and the full model succeeds, but that comparison also changes the guard set. No experiment isolates the information content of the generated faces at matched FAR. E2, E4, and E14 are needed.
4. **How does the decision policy differ from reject-option, selective prediction, and risk-controlled verification?** It is an instance of them, applied with biometric-specific sampling (person-disjoint pools) and biometric-specific guards. It does not control FRR under shift, and it does not optimize coverage subject to a certified FAR (Learn-then-Test would).
5. **Relationship between FAR auditing, calibration, and decisions.** The FAR certificate depends only on score ordering and exchangeability. Calibration (Platt) cannot change it. Calibration matters for the ρ floors and for presenting probabilities to humans, and there it is poor at intermediate scores. The audit on test data independently checks the certificate on new persons.
6. **Which contributions are formal plus empirical, and which are engineering choices?**
   - Formal and empirical: Prop. 1 together with the 0/1,149 audit.
   - Empirical: guard necessity; FG-NET adult coverage gains (with large false-reject cost).
   - Engineering: the 5-measure set, the grid, R_sam weights (0.7/0.3, thirds), the margin rule, and the four placeholder slots.

## 3. Comparison with the two reference papers

| Dimension | AIM (TPAMI 2022) | OrdCon (TIFS 2025) | AAFV-Net |
|---|---|---|---|
| Methodological core | New joint synthesis–recognition architecture with new losses | New contrastive objective (direction alignment + soft proxy matching) and a new generalization metric | Decision policy over frozen components |
| Evidence breadth | CAFR (new), MORPH, CACD-VS, FG-NET, LFW, YTF, IJB-C, MegaFace; user study for synthesis | MORPH (3 settings), FG-NET (3 protocols), AgeDB; homogeneous and cross-dataset; ablation of each loss; age-granularity study | MORPH (short-gap dominated), FG-NET (82 persons) |
| Honest negative results | Error cases | States where IEFP and MCGRL win, and limitations of its metric | Extensive (this revision) |

Both reference papers contribute a learning method whose components are each ablated, on several standard protocols. AAFV-Net does not contribute a learning method. To be comparable, it must make the decision layer itself the methodological contribution and test it with the same breadth.

## 4. Recommended research directions (pick at least one)

- **N1. Shift-robust, cluster-aware risk control for three-way biometric verification (recommended).**
  - Replace the max-impostor and β-quantile rules with a joint procedure that certifies FAR ≤ ε and FRR ≤ β simultaneously while maximizing coverage. Learn-then-Test with multiple testing over a threshold grid is one option.
  - Treat persons, not pairs, as the exchangeable unit, by deriving the guarantee for clustered genuine pairs.
  - Handle dataset shift with weighted conformal calibration or with a small labelled target calibration set.
  - FG-NET's 18.20% false-reject rate is the motivating failure. This would be a genuine, testable methodological contribution.
- **N2. Principled fusion with explicit uncertainty sources.** Replace the MLP with a likelihood-ratio or probabilistic model in which identity evidence, age gap, image quality, and generator reliability enter as separate, interpretable terms. For example: quality-conditioned density ratios, or probabilistic embeddings (PFE / MagFace magnitude) combined with a generator-reliability likelihood. The guards would then follow from the model rather than being hand-set floors.
- **N3. Validated counterfactual evidence.** If age progression is to remain central, establish with E4 that generated faces carry identity information beyond the direct pair, at matched FAR (E2/E14). Compare at least two generators. Otherwise drop the synthetic branch and present a cheaper, direct-only decision system. That would also remove the ~16 generations per pair.

## 5. What not to do

- Do not rename existing components (for example, "minimax collapse resolution" or "counterfactual sensor") to suggest novelty.
- Do not present Prop. 1 as a new theorem. It is a standard order-statistic and conformal argument, and is cited as such.
- Do not claim cross-age superiority on MORPH. The evidence contradicts it.
