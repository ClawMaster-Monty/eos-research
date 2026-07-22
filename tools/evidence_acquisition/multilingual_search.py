#!/usr/bin/env python
"""EOS Phase B multilingual Reddit + OAI search.

For each language in {en, es, pt, de, hr, ru, tr, pl, zh}, run a small
set of concept queries against Arctic Shift's public Reddit archive.
Output is a JSONL ledger of candidate posts and a per-language summary.

Each query is a (lang, query, intent) tuple. Intent values:
  outcome_first_person
  outcome_adverse
  outcome_documentation
  sourcing_intent (we keep these to spot *community size*, but exclude them
                     from outcome coding per EOS rules)

This script does NOT log in. It does NOT bypass anti-bot rules.
Output is local-only and excluded from Git.
"""

import json, time, requests, datetime, hashlib, sys
from pathlib import Path
from collections import defaultdict, Counter

OUT = Path("research/_drafts/wolverine-sources/multilingual-search.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "EOS-research/1.0 (academic; investigation)"}
ARCTIC = "https://arctic-shift.photon-reddit.com/api/posts/search"

# (lang, query, intent, target_subreddits)
QUERIES = [
    # English (already partially covered, but explicit terms)
    ("en", "BPC-157 TB-500 update", "outcome_first_person", ["Peptides","bpc_157"]),
    ("en", "Wolverine stack MRI", "outcome_documentation", ["Peptides","bpc_157"]),
    ("en", "Wolverine stack side effects", "outcome_adverse", ["Peptides","bpc_157"]),

    # Spanish
    ("es", "BPC-157 TB-500 recuperación", "outcome_first_person", ["Peptides","bpc_157"]),
    ("es", "Wolverine stack efectos secundarios", "outcome_adverse", ["Peptides","bpc_157"]),

    # Portuguese
    ("pt", "BPC-157 TB-500 recuperação tendão", "outcome_first_person", ["Peptides","bpc_157"]),
    ("pt", "Wolverine stack efeitos colaterais", "outcome_adverse", ["Peptides","bpc_157"]),

    # German
    ("de", "BPC-157 TB-500 Erfahrung Sehne", "outcome_first_person", ["Peptides","bpc_157"]),
    ("de", "Wolverine Stack Nebenwirkungen", "outcome_adverse", ["Peptides","bpc_157"]),

    # Croatian / Serbian (the patent-developer footprint is mostly here)
    ("hr", "BPC-157 pentadekapeptid iskustvo", "outcome_first_person", ["Peptides","bpc_157"]),
    ("hr", "TB-500 timozin beta-4", "outcome_first_person", ["Peptides","bpc_157"]),

    # Russian
    ("ru", "BPC-157 TB-500 восстановление", "outcome_first_person", ["Peptides","bpc_157"]),
    ("ru", "Wolverine stack побочные эффекты", "outcome_adverse", ["Peptides","bpc_157"]),

    # Turkish
    ("tr", "BPC-157 TB-500 tendon deneyim", "outcome_first_person", ["Peptides","bpc_157"]),

    # Polish
    ("pl", "BPC-157 TB-500 ścięgno doświadczenie", "outcome_first_person", ["Peptides","bpc_157"]),

    # Chinese
    ("zh", "BPC-157 TB-500 恢复 体验", "outcome_first_person", ["Peptides","bpc_157"]),
]

def fetch(arctic_params, timeout=30):
    try:
        r = requests.get(ARCTIC, params=arctic_params, headers=HEADERS, timeout=timeout)
        return r.status_code, r.content, r.url
    except Exception as e:
        return "EXC", str(e).encode(), ""

def main(per_query_limit: int = 50):
    seen_ids = set()
    counts_by_lang = defaultdict(Counter)
    out_records = []
    with OUT.open("w", encoding="utf-8") as f:
        for lang, query, intent, subs in QUERIES:
            for sub in subs:
                # Search by title then selftext
                for field in ["title", "selftext"]:
                    params = {"subreddit": sub, field: query, "limit": per_query_limit}
                    status, content, url = fetch(params)
                    if status == 200 and len(content) > 32:
                        try:
                            data = json.loads(content).get("data") or []
                        except Exception:
                            data = []
                        for x in data:
                            pid = x.get("id")
                            if not pid or pid in seen_ids: continue
                            seen_ids.add(pid)
                            body = (x.get("title") or "") + " " + (x.get("selftext") or "")
                            f.write(json.dumps({
                                "post_id": pid,
                                "lang": lang,
                                "intent": intent,
                                "subreddit": sub,
                                "query": query,
                                "field": field,
                                "title": x.get("title"),
                                "selftext_excerpt": (x.get("selftext") or "")[:1000],
                                "created_utc": x.get("created_utc"),
                                "permalink": "https://www.reddit.com" + (x.get("permalink") or ""),
                                "sha256": hashlib.sha256(body.encode("utf-8", "ignore")).hexdigest()[:12],
                                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            }, ensure_ascii=False) + "\n")
                            counts_by_lang[lang][intent] += 1
                    time.sleep(2)
    print("counts_by_lang:", json.dumps({k: dict(v) for k, v in counts_by_lang.items()}, indent=2))
    print("total_unique_posts:", len(seen_ids))
    print("output:", OUT, OUT.stat().st_size, "bytes")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 50)