#!/usr/bin/env python
"""Summarize multilingual Reddit search coverage.

Writes research/_drafts/wolverine-sources/multilingual-summary.json
that can be cited in the article (counts only, no PII).
"""
import json
from pathlib import Path
from collections import defaultdict, Counter

IN = Path("research/_drafts/wolverine-sources/multilingual-search.jsonl")
OUT = Path("research/_drafts/wolverine-sources/multilingual-summary.json")

records = [json.loads(l) for l in IN.read_text(encoding="utf-8").splitlines() if l.strip()]
by_lang = defaultdict(Counter)
by_intent = defaultdict(Counter)
by_lang_subreddit = defaultdict(Counter)
unique_ids = set()
for r in records:
    unique_ids.add(r["post_id"])
    by_lang[r["lang"]][r["intent"]] += 1
    by_intent[r["intent"]][r["lang"]] += 1
    by_lang_subreddit[r["lang"]][r["subreddit"]] += 1

summary = {
    "retrieved_at": records[0]["retrieved_at"] if records else None,
    "queries_run": 15,
    "languages_targeted": ["en","es","pt","de","hr","ru","tr","pl","zh"],
    "total_unique_posts": len(unique_ids),
    "by_language": {k: dict(v) for k,v in by_lang.items()},
    "by_intent": {k: dict(v) for k,v in by_intent.items()},
    "languages_returning_zero_hits": sorted({"es","pt","de","hr","ru","tr","pl","zh"} - set(by_lang.keys())),
    "interpretation": (
        "Arctic Shift's public Reddit archive returned Wolverine-relevant posts only in English "
        "and (single) Spanish in this concept set. This does NOT mean those communities do not exist "
        "— it means the public Reddit archive is English-dominant for these compounds. Non-English "
        "discussion lives in country-specific forums, Telegram, Discord, bodybuilder communities, "
        "veterinary channels, and clinical/practitioner networks, none of which are exposed through "
        "this route. EOS treats non-English coverage as a known access gap, not as evidence of absence."
    ),
}
OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))