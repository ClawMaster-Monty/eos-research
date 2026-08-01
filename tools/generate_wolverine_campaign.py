"""Generate the Wolverine campaign image via MiniMax image-01.

EOS Research brand spec: split-composition layout, 30% dark navy sidebar
with cyan 'E' logo + 'Look closer. Claim less.' tagline, 70% dawn scene.
1536x1024 for OG images.
"""
import json, urllib.request, time
from pathlib import Path

HOME = Path.home()
env = {}
for line in (HOME / "AppData/Local/hermes/.env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k] = v
key = env.get("MINIMAX_API_KEY", "").strip().strip('"').strip("'")

PROMPT = (
    "Split-composition brand image for a longevity science publication. "
    "Left 30%: dark navy geometric sidebar with a minimalist cyan 'E' logo at top "
    "and the tagline 'Look closer. Claim less.' in small clean cyan type below it. "
    "Right 70%: a dramatic dawn landscape at a rugged mountain trail overlook, "
    "warm orange sunrise light breaking over ridges, mist in the valley, "
    "a lone figure with a backpack standing at the viewpoint looking out. "
    "Photorealistic, cinematic, clean editorial aesthetic, high detail. "
    "No text anywhere except the sidebar logo and tagline."
)

payload = {
    "model": "image-01",
    "prompt": PROMPT,
    "aspect_ratio": "3:2",
    "response_format": "url",
    "n": 1,
}

url = "https://api.minimax.io/v1/image_generation"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as r:
    result = json.loads(r.read())

image_urls = result.get("data", {}).get("image_urls", [])
print(f"Generated {len(image_urls)} image(s)")
if image_urls:
    out = HOME / "eos-research/assets/images/wolverine-campaign-1536x1024.png"
    # download
    req = urllib.request.Request(image_urls[0], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    # MiniMax returns jpeg; save raw and convert path note
    tmp = HOME / "AppData/Local/hermes/cache/wolverine_campaign_raw.jpg"
    tmp.write_bytes(data)
    print(f"Saved raw: {tmp} ({len(data):,} bytes)")
    print(f"Target: {out}")
