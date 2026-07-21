# COSMOS Research Packet Quality Report — Provisional Blind Assessment

**Rubric:** EOS Research Packet Quality Report v0.1  
**Assessment date:** 19 July 2026  
**Status:** Provisional. Final scoring occurs after the reader-facing brief and claim registry are complete.  
**Bias control:** Packets were scored as Packet A and Packet B. Provider identity was not considered by the scoring reviewer.

## Overall result

| Packet | Raw score | Integrity-adjusted score | Classification | Correction burden | Research utility |
|---|---:|---:|---|---|---|
| Packet A | 77/100 | **59/100 provisional** | Mixed after integrity cap; otherwise Useful | Moderate–high | High after correction |
| Packet B | **56/100** | 56/100 | Mixed | High | Medium |

Packet A is the stronger research input: broader, more numerically specific, and more sophisticated about endpoint hierarchy, ITT, multiplicity, ancillary analyses, and clinical interpretation. Its adjusted score is capped by EOS v0.1 because a material absolute-effect calculation is inconsistent with the source data and denominator. Packet B’s compact cognition framing is useful, but its source architecture and study-design reconstruction require substantially more work.

## Packet A

- SHA-256: `8614c7be6b40943b0113d26e349f0688c9ebced08fe92ac7c1adb7799496d526`
- Material strengths: endpoint hierarchy; parent-trial nulls; ITT versus per-protocol distinctions; multiplicity warnings; cognition effect-size interpretation; broad ancillary landscape.
- Best contribution: the conclusion–data alignment framework and identification of where secondary, post hoc, per-protocol, and derived outcomes entered the public narrative.
- Research leverage: **High after correction**.

| Dimension | Score | Weight | Evidence |
|---|---:|---:|---|
| Source integrity | 11 | 15 | Many primary papers and the registry are present, but one PMID is wrong, some references are mismatched or vague, and several claims rely on press releases or commentary. |
| Primary-source quality | 13 | 15 | Strong parent/cognition coverage; some recent claims use incomplete or secondary records. |
| Claim–source alignment | 15 | 20 | Major endpoint/effect claims are mostly aligned; deductions for a cohort labeled as a meta-analysis, categorical null language, and unsupported industry generalizations. |
| Study-design understanding | 13 | 15 | Strong handling of endpoint hierarchy and analysis type; some pooled cognition wording is imprecise. |
| Completeness/counterevidence | 9 | 10 | Broad and balanced overall, although critical-reception material is overweighted. |
| Calibration | 7 | 10 | Usually cautious; industry-funding sections become more prosecutorial than the cited evidence supports. |
| Numerical fidelity | 6 | 10 | Most estimates match; material errors remain in lung-cancer absolute-effect arithmetic, per-protocol labeling, and a publication year. |
| Provenance/recency | 3 | 5 | Current coverage but no reproducible search record, preparation date, or verification status. |
| **Raw total** | **77** | **100** | |
| **Integrity-adjusted** | **59** | **100** | Material numerical inconsistency activates the v0.1 maximum-59 cap. |

### Confirmed corrections

1. Cocoa per-protocol major-CVD estimate is **HR 0.76 (95% CI 0.62–0.93)**. Packet A assigns **0.84 (0.71–0.99)**, which is the ITT nonprespecified result.
2. Lung-cancer events were **41 versus 66**. The raw cumulative difference is about **0.233 percentage points**, or approximately **23 fewer cases per 10,000 randomized participants over median 3.6-y follow-up**. Annualized reported rates differ by about **6 per 10,000 person-years**. The packet’s denominator/time-scale statement is incorrect.
3. The main parent paper does not report the packet’s quoted lung-cancer **p=0.016** in the checked figure/text; do not present it as directly quoted without a documented source.
4. PMID `23117760` does not resolve to the intended PHS II paper; the correct PMID is **23117775**.
5. The cited “meta-analysis” at reference 11 is a prospective cohort study.
6. The metabolomics report is a **2026**, not 2024, publication.
7. “Fourteen secondary cancer outcomes” is wrong; the paper reports **14 secondary outcomes total**, mostly cancer or cardiovascular outcomes.
8. Claims that industry-funded null supplement trials are rare or that funding structures caused narrative inflation require systematic evidence or narrower wording.
9. Recent fracture, atrial-fibrillation, biomarker, epigenetic-clock, metabolomics, and disclosure claims remain outside the frozen score until directly verified.

## Packet B

- SHA-256: `fa5158fdc8058fe02ee57567e668eb5b2740e3e47e7dd443f517b35ca3e35be3`
- Material strengths: concise distinction between cognitive-test changes and disease prevention; emphasizes short follow-up and small effect sizes; identifies MCI/dementia incidence as important.
- Best contribution: a focused question map for whether the cognition narrative outruns measured outcomes.
- Research leverage: **Medium**.

| Dimension | Score | Weight | Evidence |
|---|---:|---:|---|
| Source integrity | 10 | 15 | Recognizable links, but incomplete citations and weak claim-level traceability. |
| Primary-source quality | 7 | 15 | Includes several primary sources but omits direct Mind and Web RCT citations and relies on press/secondary material. |
| Claim–source alignment | 10 | 20 | Core interpretation is sound; Web/global-cognition and safety claims exceed their cited support. |
| Study-design understanding | 8 | 15 | Understands the ancillary structure but misstates dose, eligibility, endpoint hierarchy, and Web outcomes. |
| Completeness/counterevidence | 6 | 10 | Good limitations discussion; omits several parent estimates, multiplicity details, and newer evidence. |
| Calibration | 8 | 10 | Generally careful; “safe” and vascular-mechanism conclusions require narrowing. |
| Numerical fidelity | 4 | 10 | Wrong cocoa dose; conflicting Mind sample sizes; overbroad age threshold. |
| Provenance/recency | 3 | 5 | Visible URLs but no search, access, or verification record; coverage largely ends in 2024. |
| **Total** | **56** | **100** | Dose error qualifies for a maximum-59 cap, but raw score is already lower. |

### Confirmed corrections

1. Cocoa provided **500 mg/day flavanols**, not approximately 600 mg/day.
2. Eligibility was women **≥65** and men **≥60**, not simply all adults ≥60.
3. COSMOS-Mind enrolled **2,262**, not 2,282.
4. Mind’s primary intervention/outcome comparison was cocoa on global cognition; MVM global cognition was prespecified secondary. MCI/dementia incidence came from a subsequent prespecified-secondary analysis.
5. COSMOS-Web’s primary endpoint was one-year **ModRey immediate recall**, not global cognition.
6. Clinic’s own global-cognition primary result was not significant: **0.06 SD, 95% CI −0.003 to 0.13**.
7. The pooled global-cognition estimate used **2,731**, not 5,000+ participants. The **5,203** total applied to episodic memory.
8. Only the pooled paper clearly Bonferroni-corrected its two coprimary outcomes. This did not retroactively correct component-study outcomes or subgroups.
9. COSMOS assessed incident probable dementia, but only 14 cases occurred and no treatment effect was significant.
10. Reconstruct the bibliography with complete primary citations before using the packet as a source-ready document.

## Cross-packet verified interpretation

Daily Centrum Silver produced small pooled differences in global cognition (**0.07 SD**) and episodic memory (**0.06 SD**). Both pooled coprimary results survived the paper’s two-test Bonferroni threshold. However:

- global cognition pooled only Mind and Clinic; Web had no global-cognition endpoint;
- Clinic’s own global-cognition primary result was not significant;
- component-study secondary outcomes and subgroup analyses were generally not multiplicity-adjusted;
- COSMOS-Mind found no significant reduction in incident MCI or probable dementia;
- “two years of cognitive aging” is a cross-sectional age-equivalence translation, not an observed two-year delay in decline, disability, MCI, or dementia.

## Post-verification addendum — 19 July 2026

The blind provisional scores above remain frozen as the historical first-pass assessment. Subsequent primary-source verification found additional Packet A problems that will be considered when the final score is locked:

- atrial-fibrillation and eye results were grouped under MVM even though the cited analyses tested cocoa;
- the fracture citation misidentified the lead author, and “all null” concealed weakly adverse MVM estimates plus nonadjudicated ascertainment;
- “no serum micronutrients were measured” became too broad after verification of the 399-person nutritional-biomarker substudy;
- the four-month epigenetic-aging figure selectively averages two nominally positive clocks, neither surviving correction across five clocks;
- the USPSTF 2022 review did not include COSMOS, so claims that it judged COSMOS follow-up too short are false;
- “PHS II was null on the same time scale” is false; its final cognition assessment averaged 8.5 years after randomization;
- disclosure rhetoric transferred some of Sesso's broader sector relationships to Manson and inferred narrative distortion more strongly than the primary disclosures support.

### Contributions accepted into the EOS brief

- Packet A: endpoint hierarchy; ITT versus per-protocol distinctions after correction; multiplicity cautions; small-effect interpretation; prompt to examine ancillary outcomes and disclosures.
- Packet B: concise distinction between test-score changes and dementia prevention; emphasis on short follow-up and clinical-outcome uncertainty; question map for the cognition narrative.

### Contributions excluded or materially rewritten

- causal or loaded “trial failure” language;
- lung-cancer absolute-effect arithmetic and unsupported p-value;
- the uncorrected “two years younger” interpretation;
- MVM attribution for cocoa-only ancillary findings;
- proof-of-slower-aging language for epigenetic and metabolomic surrogates;
- unsupported causal claims that commercial support distorted reporting;
- the claim that USPSTF reviewed COSMOS.

## Finalization requirements

- Recheck every accepted claim against the final registry.
- Complete independent scientific and editorial review of the fourteen-source brief.
- Freeze dimension notes and correction burden.
- Unblind provider attribution only after final scores are locked.
- Preserve this provisional report and create a final version rather than silently rewriting the historical score.
