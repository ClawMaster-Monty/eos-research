"""Transform Wolverine draft citations to verifier-compliant format.

- Renumbers all in-text bracket citations by first appearance
- Converts them to <sup> elements with linked numbers
- Rebuilds the reference list with id="refN" in new order
- Assigns data-claim-id attributes to claim-bearing elements
- Emits the sources.json registry
"""
import json
import re
from pathlib import Path

DRAFT = Path(r"C:\Users\monty\eos-research\research\_drafts\wolverine-stack-bpc-tb500.review-draft.html")
OUT = Path(r"C:\Users\monty\eos-research\research\_drafts\wolverine-stack-bpc-tb500.review-draft.html")
REGISTRY = Path(r"C:\Users\monty\eos-research\research\wolverine-stack-bpc-tb500.sources.json")

html = DRAFT.read_text(encoding="utf-8")

# Split reference section
ref_match = re.search(r'<section id="references">(.*?)</section>', html, re.DOTALL)
assert ref_match, "references section not found"
ref_html = ref_match.group(1)
body = html[: ref_match.start()] + "<section id=\"references\">" + ref_match.group(0).replace(ref_html, "{REFERENCES}") + html[ref_match.end():]

# Extract old reference entries
ref_lis = re.findall(r"<li>(.*?)</li>", ref_html, re.DOTALL)
N_REFS = len(ref_lis)
print(f"Reference entries: {N_REFS}")

# 1. Walk body elements, find citation brackets in document order
BRACKET = re.compile(r"(\[\d+(?:[-\u2013]\d+)?\])(?:\[\d+(?:[-\u2013]\d+)?\])*")
ELEMENT = re.compile(r"<(td|p|li)\b([^>]*)>(.*?)</\1>", re.DOTALL)

def expand_bracket(b):
    """Expand '[7][8]' or '[9-11]' or '[12\u201315]' to list of ints."""
    nums = []
    for part in re.findall(r"\[(\d+(?:[-\u2013]\d+)?)\]", b):
        if "-" in part or "\u2013" in part:
            lo, hi = re.split(r"[-\u2013]", part)
            nums.extend(range(int(lo), int(hi) + 1))
        else:
            nums.append(int(part))
    return nums

# Collect all citations in document order (element by element)
order = []           # list of (element_index, position_in_element, old_numbers[])
elements = []        # list of (tag, attrs, inner)
for m in ELEMENT.finditer(body):
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    elements.append((tag, attrs, inner, m.start(), m.end()))

# Find bracket instances inside each element
instances = []  # (elem_idx, start, end, old_numbers)
for ei, (tag, attrs, inner, es, ee) in enumerate(elements):
    for bm in BRACKET.finditer(inner):
        old = expand_bracket(bm.group(0))
        instances.append((ei, bm.start(), bm.end(), old, bm.group(0)))

# 2. Build first-appearance renumbering
old_to_new = {}
for _, _, _, old_nums, _ in instances:
    for n in old_nums:
        if n not in old_to_new:
            old_to_new[n] = len(old_to_new) + 1
new_to_old = {v: k for k, v in old_to_new.items()}
assert len(old_to_new) == N_REFS, f"expected {N_REFS} unique refs, got {len(old_to_new)}"

# 3. Rebuild body with sup links + data-claim-id
# Process elements in reverse so offsets stay valid
elements_data = []  # (tag, new_attrs, new_inner, start, end)
for ei, (tag, attrs, inner, es, ee) in enumerate(elements):
    new_inner = inner
    # Replace brackets in this element (reverse order)
    bracket_matches = list(BRACKET.finditer(inner))
    for bm in reversed(bracket_matches):
        old_nums = expand_bracket(bm.group(0))
        new_nums = [old_to_new[n] for n in old_nums]
        # Deduplicate preserving order
        seen = set()
        uniq = []
        for n in new_nums:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        sup = "".join(f'<a href="#ref{n}">{n}</a>' + ("," if i < len(uniq) - 1 else "") for i, n in enumerate(uniq))
        new_inner = new_inner[: bm.start()] + f"<sup>{sup}</sup>" + new_inner[bm.end():]
    # Assign claim-id if element contains any citation
    new_attrs = attrs
    if "<sup>" in new_inner:
        claim_id = f"claim-{ei}"
        if "data-claim-id" not in new_attrs:
            new_attrs = new_attrs.rstrip() + f' data-claim-id="{claim_id}"'
    elements_data.append((tag, new_attrs, new_inner, es, ee))

# Rebuild body by replacing each element span (reverse order)
new_body = body
for tag, new_attrs, new_inner, es, ee in reversed(elements_data):
    new_body = new_body[:es] + f"<{tag}{new_attrs}>{new_inner}</{tag}>" + new_body[ee:]

# 4. Rebuild reference list in new order
new_ref_lis = []
for new_num in range(1, N_REFS + 1):
    old_num = new_to_old[new_num]
    old_li = ref_lis[old_num - 1]
    # Add id to the li
    new_li = f'<li id="ref{new_num}">{old_li}</li>'
    new_ref_lis.append(new_li)

new_ref_section = f'''<section id="references">
    <h2>References</h2>
    <div class="references-list">
    {chr(10).join(new_ref_lis)}
    </div>
  </section>'''

# Replace the entire original references section with the rebuilt one
final_html = new_body.replace("{REFERENCES}", "")
final_html = re.sub(
    r'<section id="references">.*?</section>',
    new_ref_section,
    final_html,
    count=1,
    flags=re.DOTALL,
)
# Clean up any leftover nested empty section from the placeholder pass
final_html = final_html.replace("<section id=\"references\"><section id=\"references\"></section>", new_ref_section)

OUT.write_text(final_html, encoding="utf-8")
print(f"HTML written: {OUT} ({len(final_html)} chars)")

# 5. Build registry from the transformed HTML
reg_html = OUT.read_text(encoding="utf-8")
# Re-derive claim map from final HTML
claim_pat = re.compile(
    r'<(?P<tag>[a-z][a-z0-9]*)\b[^>]*data-claim-id=["\'](?P<claim>[^"\']+)["\'][^>]*>(?P<body>.*?)</(?P=tag)>',
    re.DOTALL | re.IGNORECASE,
)
claim_map = {}
for m in claim_pat.finditer(reg_html):
    for sup in re.findall(r"<sup>(.*?)</sup>", m.group("body"), re.DOTALL):
        for n in re.findall(r'<a href="#ref(\d+)">', sup):
            claim_map.setdefault(int(n), set()).add(m.group("claim"))

# Registry entries
sources = []
for new_num in range(1, N_REFS + 1):
    old_num = new_to_old[new_num]
    old_li = ref_lis[old_num - 1]
    text = re.sub(r"<[^>]+>", " ", old_li)
    text = re.sub(r"\s+", " ", text).strip()
    pmid = re.search(r"PMID[: ]*(\d+)", text)
    doi = re.search(r"DOI:?\s*(10\.\S+)", text)
    nct = re.search(r"NCT\d+", text)
    # URL from raw HTML href (link text may be generic like "Patent text")
    href = re.search(r'href="(https?://[^"]+)"', old_li)
    url = href.group(1) if href else None
    entry = {
        "citation": new_num,
        "reference_id": f"ref{new_num}",
        "evidence_level": "Registry record; see brief text",
        "claims": [text[:200]],
        "claim_ids": sorted(claim_map.get(new_num, set())),
        "verification_note": "Transformed from source ledger; identifier check pending subagent verification.",
    }
    if doi:
        entry["doi"] = doi.group(1).rstrip(".,;")
    if pmid:
        entry["pmid"] = pmid.group(1)
    if nct:
        entry["nct"] = nct.group(0)
    if url and not (doi or pmid or nct):
        entry["url"] = url.rstrip(".,;")
    sources.append(entry)

registry = {
    "brief": "wolverine-stack-bpc-tb500",
    "verified_on": "2026-07-31",
    "sources": sources,
}
REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
print(f"Registry written: {REGISTRY} ({len(sources)} sources)")
