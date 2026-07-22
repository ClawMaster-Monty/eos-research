#!/usr/bin/env python
"""Build the EOS supervised-browsing handoff for a given date.

Reads:
  research/_drafts/wolverine-sources/access-barrier-ledger.jsonl
  research/_drafts/wolverine-sources/reddit-screening-ledger.jsonl
  research/_drafts/wolverine-sources/reddit-document-recovery-queue.jsonl
  research/_drafts/wolverine-sources/youtube-acquisition-manifest.jsonl
  research/_drafts/wolverine-sources/reddit/*.comments.json (queue completeness)

Writes:
  research/_drafts/wolverine-sources/supervised-browsing-handoff-YYYY-MM-DD.md

Hard rules:
  - No usernames appear in the handoff (only post_id/permalink).
  - Only public-source references; no private groups.
  - Each line item explains "what to save, where, and what to tell EOS."
"""

import json, datetime
from pathlib import Path
from collections import Counter

ROOT = Path("research/_drafts/wolverine-sources")

def read_jsonl(p):
    if not p.exists(): return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

def main():
    barriers = read_jsonl(ROOT / "access-barrier-ledger.jsonl")
    screened = read_jsonl(ROOT / "reddit-screening-ledger.jsonl")
    queue    = read_jsonl(ROOT / "reddit-document-recovery-queue.jsonl")
    yt       = read_jsonl(ROOT / "youtube-acquisition-manifest.jsonl")

    today = datetime.date.today().isoformat()
    out = ROOT / f"supervised-browsing-handoff-{today}.md"

    # 1. Top unresolved barriers that authenticated browsing would change
    bar_top = [b for b in barriers if b.get("evidence_status") in ("unresolved","partial")][:5]

    # 2. Top Reddit queue items
    queue_top = queue[:10]

    # 3. Top YouTube documentation gaps (no outbound URL map OR no comment snapshot)
    yt_top = sorted(yt, key=lambda r: (not r.get("documentation_claim_in_description_or_transcript"), r["video_id"]))[:5]

    # 4. Top comment-capture queue items still pending (empty archive or absent)
    captured = set(p.stem.replace(".comments","") for p in (ROOT / "reddit").glob("*.comments.json"))
    pending = []
    for q in queue:
        pid = q["post_id"]
        f = ROOT / "reddit" / f"{pid}.comments.json"
        if pid in captured and f.exists() and f.stat().st_size >= 200:
            continue  # captured OK
        pending.append(q)
    pending_top = pending[:10]

    md = []
    md.append(f"# EOS Supervised-Browsing Handoff — {today}")
    md.append("")
    md.append("Window: 19:00–22:00 PDT. Plan ~30 minutes; pick what is useful.")
    md.append("")
    md.append("> You drive the browser. EOS never sees your login screen, password manager, or 2FA. Public material only.")
    md.append("> After each item, **save the relevant file to the path shown** and paste a short note back to me.")
    md.append("")

    md.append("## 1. Top 5 unresolved barriers where authenticated browsing would help")
    if not bar_top:
        md.append("_No barrier records found. EOS queue may be empty._")
    for b in bar_top:
        md.append(f"### {b['source_id']} — {b['platform']}")
        md.append(f"- **Status:** `{b['evidence_status']}` / `{b['access_class']}`")
        md.append(f"- **What is behind the barrier:** {', '.join(b.get('likely_material', []))}")
        md.append(f"- **Suggested action:** {b.get('next_route','')}")
        md.append(f"- **Save to:** `research/_drafts/wolverine-sources/access-barriers/{b['source_id']}.md`")
        md.append(f"- **Then tell me:** what you saw, what was open vs closed, any links that resolved, any new leads.")
        md.append("")

    md.append("## 2. Top 10 Reddit posts to recover (comment trees + media + follow-up)")
    if not queue_top:
        md.append("_Reddit recovery queue empty._")
    for q in queue_top:
        md.append(f"### {q['post_id']} — {q['subreddit']}")
        md.append(f"- **Permalink:** {q['permalink']}")
        md.append(f"- **Reason queued:** {', '.join(q.get('reason', []))}")
        md.append(f"- **Save the page snapshot to:** `research/_drafts/wolverine-sources/reddit/{q['post_id']}.live-snapshot.txt`")
        md.append(f"- **Save any linked images/files to:** `research/_drafts/wolverine-sources/reddit/{q['post_id']}/`")
        md.append(f"- **Then tell me:** outcome direction, any quoted objective record, any later updates, any adverse reports, any usernames the OP referenced.")
        md.append("")

    md.append("## 3. Top 5 YouTube videos with documentation gaps")
    if not yt_top:
        md.append("_YouTube manifest empty._")
    for r in yt_top:
        urls = r.get("outbound_urls") or []
        title = (r.get("metadata") or {}).get("title","")[:80]
        md.append(f"### {r['video_id']} — {title}")
        md.append(f"- **Video URL:** https://www.youtube.com/watch?v={r['video_id']}")
        md.append(f"- **Channel:** {(r.get('metadata') or {}).get('uploader','?')}")
        md.append(f"- **Doc-claim in description/transcript:** {r.get('documentation_claim_in_description_or_transcript')}")
        md.append(f"- **Outbound links (description):** {', '.join(urls[:5]) if urls else 'none'}")
        md.append(f"- **Save comments snapshot to:** `research/_drafts/wolverine-sources/youtube/{r['video_id']}-comments-snapshot.txt` (only if not already present)")
        md.append(f"- **Then tell me:** any pinned comment from creator, any first-person viewer reports, any links to MRI/lab/surgical material, any explicit product label or vendor.")
        md.append("")

    md.append("## 4. Top 10 Reddit posts whose archive was empty (auth may help)")
    if not pending_top:
        md.append("_No empty-archive posts in the queue right now._")
    for q in pending_top:
        md.append(f"- **{q['post_id']}** — {q['subreddit']} — {q['permalink']}")

    md.append("")
    md.append("## 5. After the session")
    md.append("- Paste back a short paragraph describing what you saw.")
    md.append("- Save any image or PDF under `research/_drafts/wolverine-sources/reddit/<post_id>/` or `youtube/<video_id>/`.")
    md.append("- I will integrate the new observations into the documented-cases ledger and the access-barrier ledger, then propose article-level changes.")
    md.append("- I will not write names into tracked files. Internal usernames stay in `names-internal/`.")
    md.append("")

    out.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"barriers_top={len(bar_top)} queue_top={len(queue_top)} yt_top={len(yt_top)} pending_top={len(pending_top)}")

if __name__ == "__main__":
    main()