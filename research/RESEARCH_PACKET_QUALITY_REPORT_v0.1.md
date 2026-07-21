# EOS Research Packet Quality Report — v0.1

**Status:** Internal editorial standard  
**Effective:** 19 July 2026  
**Purpose:** Evaluate provisional AI-assisted research packets after a brief’s material claims have been independently verified. Scores guide future verification effort; they do not establish provider loyalty or substitute for editorial judgment.

## Evaluation protocol

1. Preserve each submitted packet unchanged and record its SHA-256 fingerprint.
2. Assign neutral packet IDs before scoring. Keep provider attribution outside the assessor’s working copy.
3. Build the final verified claim/source ledger independently of packet reputation.
4. Check every material claim and all recent sources. Sample minor claims only if the sampling rule is recorded.
5. Score packets against the verified ledger, not against one another.
6. Unblind provider names only after scores and correction notes are frozen.
7. Preserve the original score and rubric version. Never silently back-score after a rubric revision.

## Research Quality Score — 100 points

| Dimension | Weight | Full-credit standard |
|---|---:|---|
| Source integrity | 15 | Identifiers resolve and match the cited title, authors, journal, and year. |
| Primary-source quality | 15 | Material claims rely on primary papers, protocols, registries, or authoritative guidance rather than recycled coverage. |
| Claim–source alignment | 20 | Sources support the exact wording, population, comparator, endpoint, and direction of effect. |
| Study-design understanding | 15 | Correct treatment of randomization, primary/secondary outcomes, multiplicity, ITT/per-protocol analysis, subgroups, and ancillary studies. |
| Completeness and counterevidence | 10 | Null findings, limitations, relevant comparator trials, and credible counterevidence are represented. |
| Calibration | 10 | Evidence, inference, mechanism, and opinion are clearly separated; certainty matches design and results. |
| Numerical fidelity | 10 | Sample sizes, effect estimates, confidence intervals, p-values, dates, and event counts are accurate. |
| Provenance and recency | 5 | Source origin is clear and recent evidence is included and directly checked. |
| **Total** | **100** | |

## Integrity caps

These caps prevent polished writing from averaging away material research failures:

- Fabricated or non-resolving citation supporting a material claim: **maximum 49**.
- Material numerical claim contradicted by its cited source: **maximum 59**.
- Repeated secondary-source laundering presented as primary evidence: **maximum 64**.
- Unmarked speculation presented as a trial result: record an **integrity flag** and apply the relevant dimension deductions.

A prompt limitation, inaccessible source, or missing tool is recorded separately from a packet error. Transparent uncertainty is not penalized as fabrication.

## Score bands

| Score | Classification | Intended use |
|---:|---|---|
| 90–100 | Exceptional | Prioritize for future deep-research synthesis. |
| 80–89 | Strong | Use regularly with targeted verification. |
| 70–79 | Useful | Good research input; verify reasoning carefully. |
| 55–69 | Mixed | Mine selectively for sources and questions. |
| Below 55 | High correction burden | Use only for unique coverage. |
| Integrity failure | Quarantined | Reconstruct independently before use. |

## Separate Research Utility assessment

Quality and usefulness must not be collapsed into one number. Record:

- unique useful sources introduced;
- material claims accepted after verification;
- useful analytical insights or framings;
- contradictions or missing questions surfaced;
- material corrections required;
- estimated verification/correction burden;
- net research leverage: **High, Medium, or Low**.

## Required packet report

```markdown
### Packet [ID] — provider withheld during scoring
- SHA-256:
- Quality score: /100
- Classification:
- Material claims checked: / 
- Verified contributions accepted:
- Unique primary sources introduced:
- Material corrections required:
- Integrity flags:
- Estimated correction burden:
- Research leverage:

#### Dimension scores
| Dimension | Score | Weight | Evidence |
|---|---:|---:|---|

#### Best contribution

#### Corrections and limitations

#### Recommended future role
```

## Provider attribution after unblinding

After scores are frozen, add a concise attribution note explaining what the provider earned credit for and what work it imposed. Do not declare a permanent “best model” from one brief. Compare providers across multiple briefs, model versions, prompts, tool access, and rubric versions.

## Rubric changelog

- **v0.1 — 19 July 2026:** Initial EOS standard. Separates quality, utility, and correction burden; introduces blind scoring and integrity caps.
