# COSMOS Claim and Source Ledger

**Status:** Working verification ledger  
**Started:** 19 July 2026  
**Rule:** Research packets are discovery inputs. Public claims are admitted only after direct source verification. “Abstract verified” does not imply full-text verification of subgroup, multiplicity, adherence, or disclosure claims.

## Anchor-source registry

| ID | Primary source | Identifier | Verification depth | Material claims currently supported |
|---|---|---|---|---|
| C01 | Sesso HD et al. Effect of cocoa flavanol supplementation for prevention of cardiovascular disease events. *AJCN*. 2022. | PMID 35294962; DOI 10.1093/ajcn/nqac055 | Primary full text checked 19 Jul 2026 | Parent design; N=21,442; cocoa dose; median 3.6 y; total-CVD primary result; CVD-death secondary result; ITT/per-protocol distinction. |
| C02 | Sesso HD et al. Multivitamins in prevention of cancer and cardiovascular disease. *AJCN*. 2022. | PMID 35294969; DOI 10.1093/ajcn/nqac056 | Primary full text checked 19 Jul 2026 | Parent design; invasive-cancer primary result; lung-cancer secondary signal; total CVD; all-cause mortality. |
| C03 | Baker LD et al. Effects of cocoa extract and a multivitamin on cognitive function. *Alzheimer’s & Dementia*. 2023. | PMID 36102337; DOI 10.1002/alz.12767 | Primary full text checked 19 Jul 2026 | COSMOS-Mind N=2,262; primary cocoa cognition endpoint; prespecified secondary MVM endpoint; global-cognition estimate; subgroup caveat. |
| C04 | Sachs BC et al. Impact of MVM and cocoa extract on incidence of MCI and dementia. *Alzheimer’s & Dementia*. 2023. | PMID 37035889; DOI 10.1002/alz.13078 | Primary full text and Table 2 checked 19 Jul 2026 | Incident MCI and probable-dementia assessment; 110 MCI and 14 dementia cases; no significant incidence reduction; low power; converter-trajectory findings. Identical p=0.62 values for MCI and probable dementia confirmed directly from Table 2. |
| C05 | Yeung LK et al. Multivitamin Supplementation Improves Memory in Older Adults. *AJCN*. 2023. | PMID 37244291; DOI 10.1016/j.ajcnut.2023.05.011 | Primary full text checked 19 Jul 2026 | COSMOS-Web randomized N=3,960; ITT analysis N=3,562; one-year primary episodic-memory endpoint; no significant secondary outcomes; derived 3.1-y age-equivalence calculation. |
| C06 | Vyas CM et al. COSMOS-Clinic and meta-analysis of 3 cognition studies. *AJCN*. 2024. | PMID 38244989; DOI 10.1016/j.ajcnut.2023.12.011 | PubMed metadata and primary full text checked 19 Jul 2026 | Clinic N=573; 2-y episodic-memory result; global-cognition CI crossing zero in Clinic; pooled global/memory estimates; derived 2-y age-equivalence statement. |
| C07 | Rist PM et al. COSMOS trial design paper. *Contemporary Clinical Trials*. 2022. | PMID 35288332; DOI 10.1016/j.cct.2022.106728 | Primary metadata and design details checked 19 Jul 2026 | Factorial design; sex-specific age thresholds; placebo run-in; eligibility; original endpoints. |
| C08 | Brickman AM et al. Effects of cocoa extract on cognition in COSMOS-Web. *PNAS*. 2023. | PMID 37252983; DOI 10.1073/pnas.2216932120 | Primary metadata and results checked 19 Jul 2026 | Null cocoa result on prespecified Web immediate-recall endpoint; subgroup signals remain secondary. |
| C09 | Vyas CM et al. Effects of cocoa extract on cognition in COSMOS-Clinic. *AJCN*. 2024. | PMID 38070683; DOI 10.1016/j.ajcnut.2023.10.031 | Primary metadata and results checked 19 Jul 2026 | Null cocoa results for global cognition, episodic memory, and executive function/attention. |
| C10 | Crandall CJ et al. Cocoa/MVM supplementation and self-reported fractures. *J Bone Miner Res*. 2025. | PMID 39964350; DOI 10.1093/jbmr/zjaf030 | Primary full text checked 19 Jul 2026 | No fracture reduction; self-reported ascertainment; MVM estimates weakly adverse; multiplicity limits. |
| C11 | Christopher CN et al. Randomized MVM supplementation and carotenoids/α-tocopherol. *J Acad Nutr Diet*. 2026. | PMID 41587736; DOI 10.1016/j.jand.2026.156299 | Primary results checked 19 Jul 2026 | Selected serum nutrient-biomarker changes; exposure does not establish deficiency correction or cognitive mediation. |
| C12 | Li S et al. COSMOS supplementation and epigenetic aging clocks. *Nat Med*. 2026. | PMID 41803341; DOI 10.1038/s41591-026-04239-3 | Primary full text checked 19 Jul 2026 | Two nominal clock signals among five; no multiplicity survival; derived four-month framing. |
| C13 | Li S et al. MVM supplementation and metabolomic profiles. *GeroScience*. 2026. | PMID 41910928; DOI 10.1007/s11357-026-02197-9 | Primary full text checked 19 Jul 2026 | 168 metabolites, seven clocks, 24 modeled disease-risk scores; no signal survived FDR correction. |
| C14 | Grodstein F et al. Long-term MVM supplementation and cognition in men. *Ann Intern Med*. 2013. | PMID 24490265; DOI 10.7326/0003-4819-159-12-201312170-00006 | Primary full text checked 19 Jul 2026 | Null PHS II global-cognition and verbal-memory changes; 8.5-y average to final assessment; no prerandomization cognitive baseline. |

## Verified material claims

### Parent trial

- COSMOS used a randomized, double-blind, placebo-controlled 2×2 factorial design in 21,442 US adults. **Supported by C01/C02.**
- Cocoa extract did not significantly reduce the primary composite of total cardiovascular events: 410 vs 456 events; HR 0.90, 95% CI 0.78–1.02; p=0.11. **Supported by C01.**
- CVD death was a prespecified secondary cocoa result: 76 vs 104 deaths; HR 0.73, 95% CI 0.54–0.98; nominal p=0.04. Fourteen secondary outcomes were tested without multiplicity adjustment, and the authors label them hypothesis-generating. **Supported by C01.**
- The cocoa per-protocol analysis produced HR 0.85, 95% CI 0.72–0.99 for total CVD events. This does not replace the null ITT primary result. **Supported by C01.**
- The cocoa per-protocol major-CVD estimate was HR 0.76, 95% CI 0.62–0.93. The HR 0.84, 95% CI 0.71–0.99 estimate belongs to the ITT nonprespecified major-CVD composite. **Supported by C01.**
- Daily MVM did not significantly reduce total invasive cancer: 518 vs 535 events; HR 0.97, 95% CI 0.86–1.09; p=0.57. **Supported by C02.**
- Lung cancer was a positive secondary MVM signal: 41 vs 66 cases; HR 0.62, 95% CI 0.42–0.92. The paper did not adjust secondary outcomes for multiplicity and calls them hypothesis-generating. The raw cumulative difference is about 23 fewer cases per 10,000 randomized participants over follow-up; annualized reported rates differ by about 6 per 10,000 person-years. **Supported by C02.**
- MVM did not significantly affect total CVD (HR 0.98, 95% CI 0.86–1.12) or all-cause mortality (HR 0.93, 95% CI 0.81–1.08). **Supported by C02.**

### Cognition

- COSMOS-Mind enrolled 2,262 participants, not 2,282. **Supported by C03/C04.**
- Cocoa extract had no significant effect on the COSMOS-Mind global-cognition primary endpoint: mean z=0.03, 95% CI −0.02 to 0.08; p=0.28. **Supported by C03.**
- MVM was a prespecified secondary intervention in COSMOS-Mind and showed a global-cognition difference of 0.07 z units, 95% CI 0.02–0.12; p=0.007. **Supported by C03.**
- The larger MVM estimate among participants with CVD history had a confidence interval crossing zero (0.14, 95% CI −0.02 to 0.31), despite nominal interaction p=0.01. It is a subgroup signal, not a treatment recommendation. **Supported by C03.**
- COSMOS-Mind separately assessed incident MCI and all-cause probable dementia. Over 3 years, 110 MCI and 14 dementia cases were adjudicated; incidence did not significantly vary by treatment assignment and power was low. **Supported by C04.**
- For MVM vs placebo, incident MCI was HR 0.91, 95% CI 0.63–1.32, p=0.62; probable dementia was HR 0.76, 95% CI 0.27–2.20, p=0.62. The paper estimated only 22% power to detect a 20% MCI effect. **Supported by C04.**
- COSMOS-Web randomized 3,960 participants; 3,562 with baseline and at least one follow-up comprised the ITT analysis sample. MVM produced a favorable difference in change on the prespecified one-year immediate-recall endpoint (p=0.025) and average three-year immediate recall (p=0.011), but not secondary outcomes. **Supported by C05.**
- The Web one-year modeled treatment difference in change was 0.23 recalled words (standardized d=0.070); the average three-year difference in change was 0.15 words (d=0.048). Web did not measure a prespecified global-cognition endpoint. **Supported by C05.**
- The “3.1 years” COSMOS-Web language divides the modeled 0.23-word effect by a cross-sectional 0.074-word/year age association; it was not a directly observed delay in dementia or longitudinal aging. **Supported by C05.**
- COSMOS-Clinic enrolled 573 baseline-tested participants. The 2-y global-cognition difference in change was 0.06 SD units with 95% CI −0.003 to 0.13, while the episodic-memory difference in change was 0.12 SD units, 95% CI 0.002–0.23. **Supported by C06.**
- The within-COSMOS meta-analysis used nonoverlapping subsets (Clinic 573; Mind 2,158; Web 2,472), but Web contributed only to episodic memory. Global cognition included 2,731 participants; episodic memory included 5,203. The pooled estimates were 0.07 SD (95% CI 0.03–0.11; p=0.0009) and 0.06 SD (95% CI 0.03–0.10; p=0.0007), respectively. **Supported by C06.**
- The pooled paper Bonferroni-corrected its two coprimary outcomes at α=0.025; both passed. This does not retroactively correct component-study secondary outcomes and subgroups. **Supported by C06.**
- The “2 years of cognitive aging” statement is an age-equivalence translation, not a measured two-year delay in dementia, disability, or loss of independence. Mind separately derived 1.8 years and Web 3.1 years using different cross-sectional age-performance slopes, underscoring the model dependence. **Supported by C03/C05/C06.**

## Confirmed packet corrections

1. **Packet A incorrectly states that none of the COSMOS studies measured incident dementia.** C04 explicitly assessed all-cause probable dementia and adjudicated 14 incident cases. Correct framing: COSMOS-Mind measured incident probable dementia but found no significant treatment effect and had low power.
2. **Packet B contains an internal COSMOS-Mind sample-size inconsistency (2,262 vs 2,282).** C03 and C04 support 2,262 enrolled participants.
3. **Packet B gives cocoa as approximately 600 mg flavanols/day.** The tested dose was 500 mg/day.
4. **Packet A assigns HR 0.84 to a per-protocol major-CVD analysis.** That is the ITT nonprespecified estimate; the per-protocol estimate is HR 0.76.
5. **Packet A’s lung-cancer absolute-effect statement mixes cumulative risk with a person-year denominator.** Use approximately 23 fewer cases per 10,000 randomized participants over follow-up, or the reported annualized difference of about 6 per 10,000 person-years.
6. **Packet A calls a prospective cohort report a meta-analysis and includes a wrong PMID for PHS II.** Correct PMID: 23117775.
7. **Packet B overstates COSMOS-Web as a global-cognition study.** Its prespecified primary endpoint was one-year immediate word recall.
8. **Packet B implies 5,000+ participants supported pooled global cognition.** That count applies to episodic memory; pooled global cognition included 2,731 participants.
9. **Packet B overstates Clinic as an independent global-cognition confirmation.** Its primary confidence interval crossed zero; episodic memory was a nominally positive secondary result.
10. Statements that the trial “failed” should be rewritten as specific endpoint results: designated primary comparisons did not reach statistical significance. This preserves the hierarchy without rhetorical loading.
11. **Packet A's “other MVM ancillary endpoints” section misclassifies atrial-fibrillation and eye analyses.** Those reports tested cocoa, not MVM; the MVM eye result was not reported in the cited paper.
12. **Packet A's fracture citation is bibliographically wrong and “all null” is too simple.** The source is Crandall et al.; outcomes were self-reported, and MVM total/nonvertebral estimates leaned weakly adverse without familywise correction.
13. **Packet A's statement that no serum micronutrients were measured is too broad.** A 399-person ancillary sample measured baseline and follow-up carotenoids and α-tocopherol; this was not comprehensive deficiency testing in the main cognitive cohorts.
14. **The promoted four-month epigenetic-aging figure is a selective derived average.** Two of five clocks were nominally positive, neither survived multiplicity correction, and no clinical aging outcome was measured.
15. **The metabolomics paper is from 2026, not 2024.** None of its metabolite, aging-clock, or modeled disease-risk signals survived FDR correction.
16. **“PHS II was null on the same time scale” is false.** Its final cognitive assessment averaged 8.5 years after randomization, versus 2–3 years in COSMOS, and it lacked a prerandomization cognitive baseline.
17. **The USPSTF 2022 review did not include COSMOS.** Its search ended before the parent results appeared; claims that USPSTF judged COSMOS follow-up too short are misattributed.
18. **Funding rhetoric must be evidence-bounded.** Disclose mixed public/commercial support and paper-specific author relationships; do not infer distortion or transfer one investigator's trade-group relationships to another without evidence.

## Remaining verification work

- Compare the endpoint amendment against protocol versions and document its timing; the primary paper confirms expansion but not Packet A’s specific DSMB-approval wording.
- Verify any future post-intervention cognition results before using them; registry completion status is not an outcome.
- Recheck disclosures if the final brief adds papers beyond C01–C14.
- Do not carry broad claims about industry-funded null trials into the brief without a systematic source.
