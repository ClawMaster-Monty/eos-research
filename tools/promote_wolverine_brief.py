"""Promote the Wolverine review draft to the public research brief.

Creates research/wolverine-stack-bpc-tb500-evidence.html from the review
draft with production metadata (canonical, OG, JSON-LD, publish date),
removes review-only state (noindex, draft labels, draft disclaimer).
"""
import re
from pathlib import Path

SRC = Path(r"C:\Users\monty\eos-research\research\_drafts\wolverine-stack-bpc-tb500.review-draft.html")
DST = Path(r"C:\Users\monty\eos-research\research\wolverine-stack-bpc-tb500-evidence.html")
BASE = "https://clawmaster-monty.github.io/eos-research"
PUBLISH_DATE = "2026-07-31"

html = SRC.read_text(encoding="utf-8")

# 1. Head: remove noindex, new title/description, add canonical/OG/Twitter/JSON-LD
html = html.replace(
    '<meta name="robots" content="noindex, nofollow, noarchive">\n',
    "",
)
html = html.replace(
    "<title>Wolverine Stack: BPC-157 + TB-500 Evidence Audit — EOS Research Review Draft</title>",
    "<title>Wolverine Stack: BPC-157 + TB-500 Under Audit · EOS Research</title>",
)
html = html.replace(
    '<meta name="description" content="Withdrawn review draft: a claim-level audit of BPC-157, TB-500 identity, blend evidence, and a bounded public-experience sample.">',
    '<meta name="description" content="A claim-level audit of the BPC-157 + TB-500 Wolverine stack: 38 verified sources, TB-500 identity, product quality, and the human-evidence gap.">',
)
production_meta = f'''<link rel="canonical" href="{BASE}/research/wolverine-stack-bpc-tb500-evidence.html">
<meta property="og:title" content="The Wolverine Stack: BPC-157 + TB-500 Under Audit · EOS Research">
<meta property="og:description" content="Widely used. Not yet tested. A claim-level audit of the BPC-157 + TB-500 stack across 38 verified sources — identity, quality, and the human-evidence gap.">
<meta property="og:type" content="article">
<meta property="og:url" content="{BASE}/research/wolverine-stack-bpc-tb500-evidence.html">
<meta property="og:image" content="{BASE}/assets/images/eos-research-branded-landscape.png">
<meta property="og:image:width" content="1536">
<meta property="og:image:height" content="1024">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Wolverine Stack: BPC-157 + TB-500 Under Audit",
  "description": "A claim-level audit of the BPC-157 + TB-500 Wolverine stack: 38 verified sources, TB-500 identity, product quality, and the human-evidence gap.",
  "datePublished": "{PUBLISH_DATE}",
  "publisher": {{
    "@type": "Organization",
    "name": "EOS Research"
  }}
}}
</script>'''
html = html.replace(
    '<link rel="stylesheet" href="/eos-research/styles.css">',
    '<link rel="stylesheet" href="/eos-research/styles.css">\n' + production_meta,
)

# 2. Eyebrow + byline: drop review-draft language
html = html.replace(
    "Peptide blends series · Review draft · Healing and recovery",
    "Peptide blends series · Healing and recovery",
)
html = html.replace(
    '<span class="byline">EOS Research · Unreviewed working draft</span>',
    '<span class="byline">EOS Research · Evidence audit</span>',
)

# 3. Publish date
html = html.replace(
    '<time datetime="2026-07-21">21 July 2026</time>',
    f'<time datetime="{PUBLISH_DATE}">31 July 2026</time>',
)

# 4. Remove the draft-status disclaimer block
draft_status = re.search(
    r'<p class="disclaimer">\s*<strong>Draft status:</strong>.*?</p>',
    html,
    re.DOTALL,
)
if draft_status:
    html = html[: draft_status.start()] + html[draft_status.end():]
    print("Removed draft-status disclaimer")
else:
    print("WARN: draft-status disclaimer not found")

# 5. Fix relative asset/nav paths if any reference ../ (nav uses absolute /eos-research/, fine)
DST.write_text(html, encoding="utf-8")
print(f"Published brief written: {DST} ({len(html)} chars)")
