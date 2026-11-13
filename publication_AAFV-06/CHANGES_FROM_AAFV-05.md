# Changes from AAFV-05 to AAFV-06

| Area | AAFV-05 | AAFV-06 |
|---|---|---|
| Title | "Does Synthetic Age Progression Help Cross-Age Face Verification? …" | AAFV-04 title restored: "AAFV-Net: Reliability-Gated Three-Way Decisions for Adult Cross-Age Face Verification With Audited Random-Impostor False-Accept Risk" |
| Length | 7 pages | 13 pages |
| Architecture | One paragraph | Full Section IV with equations (2)–(9); Fig. 2 (AAFV-Net, ensemble size corrected to 3); Fig. 11 (proposed redesign) |
| Problem formulation | – | Section III: decision rule, objective, zero-failure proposition, scope of the threat model |
| Original results | Summarised in prose | Section VI: Table VIII (test, 8 methods), Table IX (FG-NET by gap), Table X (19 ablations), Fig. 3 (outcome shares) |
| Protocol | Prose | Table XI (chronology, including the draft calibration and the post-hoc quarantine) |
| Image results | None | Fig. 5 (MORPH audit), Fig. 7 (SAM outputs), Fig. 8 (change maps), Fig. 10 (FG-NET false accepts) |
| Future work | Protocol paragraph | Section VIII: proposed architecture with loss and score, ablation ladder (Table XII), pre-registered test, long-gap datasets |
| References | 48 | 90, all cited; analysis of every prior list in `REFERENCE_ANALYSIS.md` |
| Threat model and ethics | Short | Discussion of strategic impostors, morphing and presentation attacks, synthetic forgeries, template inversion, privacy and demographics |
| Claim check | 33 prose numbers | 44 prose numbers (44/44 pass) |

**Unchanged:** every re-analysis result and number from AAFV-05, and the position that the synthetic branch adds no evidence on MORPH, that the operating point depends on the post-hoc exclusion, and that MORPH long-gap labels are unreliable.
