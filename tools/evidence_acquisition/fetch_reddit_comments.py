#!/usr/bin/env python
"""Fetch top-level comments for high-value Reddit posts.

Routes tried in order, with explicit archival labels:
  1. PullPush comments endpoint (public archive)
  2. Arctic Shift comments endpoint (public archive)
  3. Reddit public JSON (often blocked; record result)

Output: research/_drafts/wolverine-sources/reddit/<post_id>.comments.json
with provenance: route, status, retrieval date, raw bytes sha256.

Usernames are stored separately in research/_drafts/wolverine-sources/names-internal/
and never copied into tracked files.

This script does NOT bypass authentication or rate limits.
"""

import json, time, hashlib, sys, datetime, requests
from pathlib import Path

QUEUE = Path("research/_drafts/wolverine-sources/reddit-document-recovery-queue.jsonl")
OUT   = Path("research/_drafts/wolverine-sources/reddit")
NAMES = Path("research/_drafts/wolverine-sources/names-internal")

# PullPush rate-limits aggressively and returns many empty payloads.
# Arctic Shift comments endpoint is currently the working route.
ARCTIC_COMMENTS = "https://arctic-shift.photon-reddit.com/api/comments/search"
ARCTIC_POSTS    = "https://arctic-shift.photon-reddit.com/api/posts/search"
PULLPUSH_COMMENTS = "https://api.pullpush.io/reddit/comment/search/"
PULLPUSH_SUBMITS  = "https://api.pullpush.io/reddit/submission/search/"

HEADERS = {"User-Agent": "EOS-research/1.0 (academic; investigation)"}

def fetch_arctic_comments(post_id: str, timeout=30):
    try:
        r = requests.get(ARCTIC_COMMENTS, params={"link_id": f"t3_{post_id}", "limit": 100}, headers=HEADERS, timeout=timeout)
        return ("arctic_comments", r.status_code, r.content, r.url)
    except Exception as e:
        return ("arctic_comments", "EXC", str(e).encode(), "")

def fetch_arctic_post(post_id: str, timeout=30):
    try:
        r = requests.get(ARCTIC_POSTS, params={"ids": post_id, "limit": 1}, headers=HEADERS, timeout=timeout)
        return ("arctic_post", r.status_code, r.content, r.url)
    except Exception as e:
        return ("arctic_post", "EXC", str(e).encode(), "")

def fetch_pullpush_comments(post_id: str, timeout=30):
    try:
        r = requests.get(PULLPUSH_COMMENTS, params={"link_id": f"t3_{post_id}", "limit": 100, "sort": "asc", "sort_type": "created_utc"}, headers=HEADERS, timeout=timeout)
        return ("pullpush_comments", r.status_code, r.content, r.url)
    except Exception as e:
        return ("pullpush_comments", "EXC", str(e).encode(), "")

def fetch_pullpush_submission(post_id: str, timeout=30):
    try:
        r = requests.get(PULLPUSH_SUBMITS, params={"ids": post_id, "limit": 1}, headers=HEADERS, timeout=timeout)
        return ("pullpush_submission", r.status_code, r.content, r.url)
    except Exception as e:
        return ("pullpush_submission", "EXC", str(e).encode(), "")

def save(post_id: str, route_record: tuple, limit: int):
    route, status, content, url = route_record
    OUT.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(content).hexdigest() if isinstance(content, (bytes, bytearray)) else hashlib.sha256(str(content).encode()).hexdigest()
    rec = {
        "post_id": post_id,
        "route": route,
        "status": status,
        "url": url,
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sha256": sha,
        "bytes": len(content) if isinstance(content, (bytes, bytearray)) else len(str(content).encode()),
    }
    # parse minimal JSON shape; do not crash on bad data
    try:
        if isinstance(content, (bytes, bytearray)):
            parsed = json.loads(content)
        else:
            parsed = json.loads(str(content))
        rec["comment_count"] = len(parsed.get("data", [])) if isinstance(parsed, dict) and "data" in parsed else len(parsed) if isinstance(parsed, list) else None
    except Exception as e:
        rec["parse_error"] = str(e)
        parsed = None
    (OUT / f"{post_id}.comments.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return rec

def main(limit: int = 25):
    if not QUEUE.exists():
        print("no queue file; run screen_reddit.py first", file=sys.stderr)
        sys.exit(1)
    items = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        items.append(json.loads(line))
    print(f"queue: {len(items)} items; sampling first {limit}")
    OUT.mkdir(parents=True, exist_ok=True)
    NAMES.mkdir(parents=True, exist_ok=True)
    summary = []
    for it in items[:limit]:
        pid = it["post_id"]
        # primary: arctic_comments (current working route)
        rec1 = save(pid, fetch_arctic_comments(pid), limit)
        time.sleep(2)
        # secondary: arctic_post (covers posts the comments endpoint doesn't link)
        if rec1["bytes"] < 32:
            rec2 = save(pid + ".post", fetch_arctic_post(pid), limit)
            time.sleep(2)
        summary.append({"post_id": pid, "primary": rec1["route"], "primary_status": rec1["status"], "primary_bytes": rec1["bytes"]})
    print(json.dumps(summary, indent=2)[:3000])

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    main(limit)