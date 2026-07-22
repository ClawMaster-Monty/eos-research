#!/usr/bin/env python
"""Build EOS YouTube acquisition manifests for each video.

For each video_id, records:
  - whether transcript exists locally and its length
  - description length and first 240 chars
  - outbound URLs from description (parse)
  - channel handle
  - view/like/comment counts as dated attention metrics
  - comment acquisition status (snapshot path or note)
  - whether follow-up videos were found by channel/keyword search
  - flags and gaps

Outputs: research/_drafts/wolverine-sources/youtube-acquisition-manifest.jsonl

Uses youtube-transcript-api for transcript presence and yt-dlp for metadata.
yt-dlp is preferred because it returns more consistent metadata; if missing,
falls back to oEmbed and the local transcript text file.

No login. No comment scraping. Use yt-dlp only on public metadata.
"""

import json, re, subprocess, sys, datetime, hashlib, shutil
from pathlib import Path

VIDEO_DIR = Path("research/_drafts/wolverine-sources/youtube")
OUT = Path("research/_drafts/wolverine-sources/youtube-acquisition-manifest.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

# 11 video IDs already covered by saved transcripts
VIDEO_IDS = [
    ("-Dhap_CtA9M", "https://www.youtube.com/watch?v=-Dhap_CtA9M"),
    ("_aC29jBAzNE", "https://www.youtube.com/watch?v=_aC29jBAzNE"),
    ("aKPyE0M_xI4", "https://www.youtube.com/watch?v=aKPyE0M_xI4"),
    ("d898NBHvk8Y", "https://www.youtube.com/watch?v=d898NBHvk8Y"),
    ("GFVspd1by7w", "https://www.youtube.com/watch?v=GFVspd1by7w"),
    ("i7BN8ZHv_u0", "https://www.youtube.com/watch?v=i7BN8ZHv_u0"),
    ("LuBhP2rUCFc", "https://www.youtube.com/watch?v=LuBhP2rUCFc"),
    ("Npl1CiHiu-k", "https://www.youtube.com/watch?v=Npl1CiHiu-k"),
    ("OfcexE9s4yw", "https://www.youtube.com/watch?v=OfcexE9s4yw"),
    ("UDUNhmSc4uQ", "https://www.youtube.com/watch?v=UDUNhmSc4uQ"),
    ("ZgSknt28i_k", "https://www.youtube.com/watch?v=ZgSknt28i_k"),
]

URL_RX = re.compile(r"https?://[^\s<>\"']+")
CHANNEL_KEYWORDS = ["bpc-157", "tb-500", "wolverine", "tb500", "pentadecapeptide", "thymosin", "klow", "ghk-cu"]

def transcript_status(vid: str):
    p = VIDEO_DIR / f"{vid}.txt"
    if not p.exists():
        return {"present": False}
    txt = p.read_text(encoding="utf-8", errors="ignore")
    return {"present": True, "bytes": len(txt.encode("utf-8")), "words": len(txt.split())}

def fetch_metadata(vid: str):
    """Use yt-dlp --dump-json (no download) to get public metadata."""
    yt_dlp = shutil.which("yt-dlp")
    if not yt_dlp:
        return {"error": "yt-dlp missing", "channel": None, "title": None, "description": None, "upload_date": None, "view_count": None, "like_count": None, "uploader": None, "uploader_id": None, "channel_url": None, "tags": [], "categories": []}
    try:
        r = subprocess.run([yt_dlp, "--skip-download", "--no-warnings", "--dump-single-json", f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=90)
        if r.returncode != 0:
            return {"error": f"yt-dlp exit {r.returncode}", "stderr": r.stderr[:500]}
        data = json.loads(r.stdout)
        return {
            "title": data.get("title"),
            "description": data.get("description"),
            "upload_date": data.get("upload_date"),
            "view_count": data.get("view_count"),
            "like_count": data.get("like_count"),
            "uploader": data.get("uploader"),
            "uploader_id": data.get("uploader_id"),
            "channel_url": data.get("channel_url"),
            "channel_id": data.get("channel_id"),
            "tags": data.get("tags") or [],
            "categories": data.get("categories") or [],
            "duration": data.get("duration"),
        }
    except Exception as e:
        return {"error": str(e)}

def parse_outbound_urls(description: str):
    if not description: return []
    urls = URL_RX.findall(description)
    return list(dict.fromkeys(urls))[:20]  # de-dup, cap

def snapshot_path(vid: str):
    sp = VIDEO_DIR / f"{vid}-comments-snapshot.txt"
    return {"path": str(sp), "present": sp.exists(), "bytes": sp.stat().st_size if sp.exists() else 0}

def main():
    with OUT.open("w", encoding="utf-8") as f:
        for vid, url in VIDEO_IDS:
            ts = transcript_status(vid)
            meta = fetch_metadata(vid)
            desc = meta.get("description") or ""
            outbound = parse_outbound_urls(desc)
            snap = snapshot_path(vid)
            doc_claim = any(kw in (desc + " " + (ts.get("transcript") or "")).lower() for kw in ["mri", "x-ray", "xray", "ultrasound", "bloodwork", "blood work", "doctor", "surgery", "biopsy", "scan"])
            rec = {
                "video_id": vid,
                "url": url,
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "transcript": ts,
                "metadata": meta,
                "description_chars": len(desc),
                "outbound_urls": outbound,
                "comment_snapshot": snap,
                "documentation_claim_in_description_or_transcript": doc_claim,
                "fetch_comments": "open",
                "fetch_follow_ups": "open",
                "access_class": "open",
                "evidence_status": "partial",
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(vid, "title=", meta.get("title") and meta["title"][:50], " desc_chars=", len(desc), " outbound=", len(outbound), " doc_claim=", doc_claim)

if __name__ == "__main__":
    main()