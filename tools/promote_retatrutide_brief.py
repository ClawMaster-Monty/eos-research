"""Promote the Retatrutide review draft to the public research brief (Issue 007).

Creates research/retatrutide-evidence.html from the review draft with
production metadata (canonical, OG, JSON-LD, publish date 2026-08-01),
removes review-only state (noindex, draft labels, draft disclaimer),
and rewrites relative paths to absolute /eos-research/ site paths.
"""
import re
from pathlib import Path

SRC = Path(r"C:\Users\monty\eos-research\research\_drafts\retatrutide-evidence.html")
DST = Path(r"C:\Users\monty\eos-research\research\retatrutide-evidence.html")
BASE = "https://clawmaster-monty.github.io/eos-research"
PUBLISH_DATE = "2026-08-01"

html = SRC.read_text(encoding="utf-8")

# 1. Head: remove noindex, new title, canonical/OG/Twitter/JSON-LD
html = html.replace('<meta name="robots" content="noindex, nofollow, noarchive">\n', "")
html = html.replace(
    "<title>Retatrutide: The Trial Results Are Real. The Online Certainty Is Not. — EOS Research Review Draft</title>",
    "<title>Retatrutide: The Trial Results Are Real. The Online Certainty Is Not. · EOS Research</title>",
)
production_meta = f'''<link rel="canonical" href="{BASE}/research/retatrutide-evidence.html">
<meta property="og:title" content="Retatrutide: The Trial Results Are Real. The Online Certainty Is Not. · EOS Research">
<meta property="og:description" content="A claim-level audit of retatrutide: verified phase-2/3 trial results, the results-published-nowhere gap, and what online certainty about the triple agonist runs ahead of.">
<meta property="og:type" content="article">
<meta property="og:url" content="{BASE}/research/retatrutide-evidence.html">
<meta property="og:image" content="{BASE}/assets/images/eos-research-branded-landscape.png">
<meta property="og:image:width" content="1536">
<meta property="og:image:height" content="1024">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Retatrutide: The Trial Results Are Real. The Online Certainty Is Not.",
  "description": "A claim-level audit of retatrutide: verified phase-2/3 trial results, the results-published-nowhere gap, and what online certainty about the triple agonist runs ahead of.",
  "datePublished": "{PUBLISH_DATE}",
  "publisher": {{
    "@type": "Organization",
    "name": "EOS Research"
  }}
}}
</script>'''
html = html.replace(
    '<link rel="stylesheet" href="../../styles.css">',
    '<link rel="stylesheet" href="/eos-research/styles.css">\n' + production_meta,
)

# 2. Relative -> absolute site paths (promoted page lives at /eos-research/research/)
html = html.replace('<a href="../../index.html" class="nav-logo">', '<a href="/eos-research/" class="nav-logo">')
html = html.replace('<a href="../../research/">Archive</a>', '<a href="/eos-research/research/">Archive</a>')
html = html.replace('<a href="../../methodology/">Methodology</a>', '<a href="/eos-research/methodology/">Methodology</a>')

# 3. Eyebrow + byline: drop review-draft language
html = html.replace(
    "Incretin series · Review draft · Metabolic health",
    "Incretin series · Metabolic health",
)
html = html.replace(
    '<span class="byline">EOS Research · Unreviewed working draft</span>',
    '<span class="byline">EOS Research · Evidence audit</span>',
)

# 4. Publish date
html = html.replace(
    '<time datetime="2026-07-31">31 July 2026</time>',
    f'<time datetime="{PUBLISH_DATE}">1 August 2026</time>',
)

# 5. Remove review-draft status markers in footer / methods
html = html.replace(
    "This is a draft, not a published recommendation.",
    "All cited records were checked against live identifiers and registry/API records on 31 July 2026.",
)
html = html.replace(
    "<strong>Editorial disclaimer:</strong> This is an evidence audit, not medical advice.",
    "<strong>Editorial disclaimer:</strong> This is an evidence audit, not medical advice.",
)

DST.write_text(html, encoding="utf-8")
print(f"Published brief written: {DST} ({len(html)} chars)")
