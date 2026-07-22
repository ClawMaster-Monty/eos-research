#!/usr/bin/env python
"""EOS Reddit screening pass.

Inputs:
  C:/Users/monty/reddit_crawl_candidates.json
  C:/Users/monty/reddit_candidates.json
  research/_drafts/wolverine-sources/reddit-coded-ledger.json (already-coded)

Output:
  research/_drafts/wolverine-sources/reddit-screening-ledger.jsonl
  research/_drafts/wolverine-sources/reddit-document-recovery-queue.jsonl

Privacy:
  Usernames are recorded only in a separate local-only file
  research/_drafts/wolverine-sources/names-internal/<run-id>.jsonl
  which is excluded from Git.

Disposition classes (machine-stable):
  included_first_person
  possible_first_person
  hearsay
  question_only
  sourcing_only
  promotional
  wrong_compound
  removed_or_empty
  duplicate_of_existing
  irrelevant

Outputs are deterministic given the same input. Re-runs are idempotent.
"""

import json, re, datetime, hashlib, sys
from pathlib import Path

IN_CRAWL = Path("C:/Users/monty/reddit_crawl_candidates.json")
IN_QUERY = Path("C:/Users/monty/reddit_candidates.json")
IN_CODED = Path("research/_drafts/wolverine-sources/reddit-coded-ledger.json")

OUT_SCREEN = Path("research/_drafts/wolverine-sources/reddit-screening-ledger.jsonl")
OUT_RECOV  = Path("research/_drafts/wolverine-sources/reddit-document-recovery-queue.jsonl")
OUT_NAMES  = Path("research/_drafts/wolverine-sources/names-internal")

# Compound terms (case-insensitive). Use both common spellings.
COMPOUND = [
    r"\bbpc[-\s]?157\b",
    r"\btb[-\s]?500\b",
    r"\btb500\b",
    r"\bwolverine\b",
    r"\bthymosin\s*beta[-\s]?4\b",
    r"\btβ4\b",
    r"\bt[-_]?beta[-\s]?4\b",
    r"\bac[-\s]?l?k?k?t?e?t?q?\b",  # Ac-LKKTETQ or fragments
    r"\bpentadekapeptid\w*\b",
    r"\bpl[-\s]?14736\b",
    r"\bklow\b",
    r"\bglow\b",
    r"\bghk[-\s]?cu\b",
    r"\bkpv\b",
]

DOC_TERMS = [
    r"\bmri\b", r"\bultrasound\b", r"\bx[-\s]?ray\b", r"\bcat[-\s]?scan\b",
    r"\bscan\b", r"\bpathology\b", r"\bbloodwork\b", r"\bblood\s*work\b",
    r"\bbiopsy\b", r"\bsurgery\b", r"\boperat\w+\b", r"\bdoctor\b",
    r"\brange\s+of\s+motion\b", r"\bvalidated\s+scale\b", r"\b(function|strength)\s+test",
]
OUTCOME_TERMS = [
    r"\bhealed\b", r"\brecovered\b", r"\brecovery\b", r"\bimproved\b",
    r"\bno\s+(effect|change|improvement)\b", r"\bdidn['’]?t\s+work\b",
    r"\bno\s+noticeable\b", r"\bworse\w*\b", r"\brecurr\w+\b",
    r"\breturn(ed)?\s+to\s+(sport|activity|gym|training|running)\b",
]
ADVERSE_TERMS = [
    r"\bside\s+effect\w*\b", r"\badverse\b", r"\bhive\w*\b", r"\bursh\b",
    r"\bswelling\b", r"\binsomnia\b", r"\bheadache\w*\b", r"\bacne\b",
    r"\bhypersensiti\w+\b", r"\bbruise\w*\b", r"\bnights?\s*sweats?\b",
    r"\bmuscle\s+tension\b", r"\babdominal\s+pressure\b", r"\banxiety\b",
    r"\bhospital\b", r"\ber\b",
]

RX = [re.compile(p, re.I) for p in COMPOUND + DOC_TERMS + OUTCOME_TERMS + ADVERSE_TERMS]

QUESTION_RX = re.compile(r"\?\s*$|\b(dose|dosage|how\s+much|where\s+to\s+buy|source|sourcing|vendor|recommend|stack)\b", re.I)
PROMO_RX = re.compile(r"\b(affiliate|use\s+code|discount|promo|sale|check\s+my\s+bio|telegram\s+channel|t\.me/|@)\b", re.I)
REQUEST_RX = re.compile(r"^(how|where|what|when|which|can\s+i|should\s+i|is\s+it|any\s+recommend|anyone|looking\s+for|wtf|lol)\b", re.I)

def norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def doc_signal(t: str) -> bool:
    return any(rx.search(t) for rx in [re.compile(p, re.I) for p in DOC_TERMS])

def first_person_signal(t: str) -> bool:
    # rough heuristic: narrator present in body
    return bool(re.search(r"\b(i|my|me|i've|i've|i\s+took|i\s+did|i\s+started|i\s+use)\b", t, re.I))

def classify(post) -> tuple[str, list[str]]:
    title = norm_text(post.get("title", ""))
    body  = norm_text(post.get("selftext", ""))
    full  = f"{title} {body}".strip()
    if not full or len(full) < 8:
        return ("removed_or_empty", ["empty_body"])
    if any(rx.search(full) for rx in [re.compile(p, re.I) for p in COMPOUND]) is False:
        return ("wrong_compound", ["no_compound_term"])
    if PROMO_RX.search(full):
        return ("promotional", ["promo_marker"])
    if REQUEST_RX.search(full) and QUESTION_RX.search(full) and not first_person_signal(full):
        return ("question_only", ["request_or_question_only"])
    flags = []
    if doc_signal(full): flags.append("doc_claim")
    if any(re.search(p, full, re.I) for p in ADVERSE_TERMS): flags.append("adverse_term")
    if any(re.search(p, full, re.I) for p in OUTCOME_TERMS): flags.append("outcome_term")
    if first_person_signal(full):
        return ("included_first_person", flags)
    if any(re.search(p, full, re.I) for p in OUTCOME_TERMS + ADVERSE_TERMS):
        return ("possible_first_person", flags)
    return ("question_only", ["first_person_absent"])

def main():
    posts = []
    if IN_CRAWL.exists(): posts += json.loads(IN_CRAWL.read_text(encoding="utf-8"))
    if IN_QUERY.exists(): posts += json.loads(IN_QUERY.read_text(encoding="utf-8"))
    print(f"loaded: {len(posts)} candidates")

    # dedupe by post id (string + numeric)
    seen = {}
    for p in posts:
        pid = str(p.get("id") or p.get("post_id") or "")
        if not pid: continue
        # also dedupe by body hash when ids collide or are missing
        body = norm_text((p.get("title") or "") + " " + (p.get("selftext") or ""))
        h = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
        key = (pid, h)
        if key in seen: continue
        seen[key] = p
    uniq = list(seen.values())
    print(f"unique: {len(uniq)} candidates")

    # mark those already in coded ledger (12 records)
    already = set()
    if IN_CODED.exists():
        try:
            c = json.loads(IN_CODED.read_text(encoding="utf-8"))
            for r in c.get("records", []):
                already.add(str(r.get("post_id")))
        except Exception as e:
            print("coded-ledger read failed:", e, file=sys.stderr)

    OUT_SCREEN.parent.mkdir(parents=True, exist_ok=True)
    OUT_RECOV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NAMES.mkdir(parents=True, exist_ok=True)

    counts = {}
    with OUT_SCREEN.open("w", encoding="utf-8") as fs, \
         OUT_RECOV.open("w", encoding="utf-8") as fr:
        for p in uniq:
            pid = str(p.get("id"))
            disposition, flags = classify(p)
            if pid in already:
                disposition = "duplicate_of_existing"
            counts[disposition] = counts.get(disposition, 0) + 1
            # body-hash for dedupe of analytics
            body = norm_text((p.get("title") or "") + " " + (p.get("selftext") or ""))
            h = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
            rec = {
                "post_id": pid,
                "date": p.get("date") or (datetime.datetime.fromtimestamp(p.get("created_utc", 0), datetime.timezone.utc).date().isoformat() if p.get("created_utc") else ""),
                "subreddit": p.get("subreddit", ""),
                "disposition": disposition,
                "flags": flags,
                "permalink": p.get("permalink", ""),
                "body_hash": h,
                "title_hash": hashlib.sha256((p.get("title") or "").encode("utf-8")).hexdigest()[:12],
            }
            # record high-value queues (do NOT include username in tracked file)
            if "doc_claim" in flags or "adverse_term" in flags or "outcome_term" in flags:
                recov = {
                    "post_id": pid,
                    "permalink": p.get("permalink", ""),
                    "subreddit": p.get("subreddit", ""),
                    "reason": [f for f in flags],
                    "fetch_comments": True,
                    "fetch_media": True,
                    "search_followup_phrases": True,
                    "private_only_username_path": f"names-internal/{pid}.jsonl",
                }
                fr.write(json.dumps(recov, ensure_ascii=False) + "\n")
            fs.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # internal-only usernames — strictly local
    for p in uniq:
        pid = str(p.get("id"))
        if p.get("author"):
            (OUT_NAMES / f"{pid}.jsonl").write_text(
                json.dumps({"post_id": pid, "author": p.get("author"), "permalink": p.get("permalink", "")}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    print("counts:", json.dumps(counts, sort_keys=True))

if __name__ == "__main__":
    main()