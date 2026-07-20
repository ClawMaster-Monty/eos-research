# EOS Research Source Verification Gate

Every published brief must have a sidecar registry:

```text
research/<brief-slug>.sources.json
```

Each in-text citation used by the brief must have one registry record containing:

- `citation` — the rendered reference number, numbered by first appearance
- `reference_id` — the matching rendered bibliography anchor, such as `ref1`
- `doi` and/or `pmid`
- `evidence_level` — e.g. Human RCT, systematic review, preclinical
- `claims` — a reader-facing summary of the claim(s) that source supports
- `claim_ids` — the exact rendered `data-claim-id` values supported by the source
- `verification_note` — confirmation that the primary source was checked

## Required publication command

Run this before publishing, committing, or describing a brief as verified:

```bash
python tools/verify_brief.py research/<brief>.html research/<brief>.sources.json
```

The command fails closed on missing registry fields or identifiers, partial claim mappings, unlinked numeric superscripts, citation numbering that does not follow first appearance, duplicate DOI/PMID or reference IDs, uncatalogued bibliography entries, and mismatches between rendered references and the registry.

## What the gate does not replace

The tool validates coverage and source-to-claim traceability. It does not infer whether a study design supports the wording. The editor must read the primary abstract—and the full paper when the claim depends on methods, adherence, subgroup analyses, or outcomes not represented in the abstract.

## Recent literature rule

For recent-year sources, resolve the DOI or PMID and verify the primary abstract before publication. Record that review in `verification_note`. If the interpretation is ambiguous, narrow the claim or escalate it for editorial review.
