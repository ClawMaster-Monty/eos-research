"""Generate the Wolverine campaign image via MiniMax image-01 (v2).

EOS Research brand spec: split-composition layout, 30% dark navy sidebar
with cyan 'E' logo + 'Look closer. Claim less.' tagline, 70% dawn scene.
1536x1024 for OG images. v2: stronger explicit layout instructions,
simpler composition for cleaner text rendering.
"""
import json, urllib.request
from pathlib import Path

HOME = Path.home()
env = {}
for line in (HOME / "AppData/Local/hermes/.env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k] = v
key = env.get("MINIMAX_API_KEY", "").strip().strip('"').strip("'")

PROMPT = (
    "Vertical split-screen editorial magazine cover, two distinct panels. "
    "LEFT PANEL (30% of width): solid deep navy background, a clean minimal "
    "uppercase cyan letter 'E' centered near the top, below it the words "
    "'LOOK CLOSER.' then 'CLAIM LESS.' in small crisp white sans-serif text. "
    "RIGHT PANEL (70% of width): photorealistic dawn landscape, a hiker with "
    "a backpack standing on a rocky mountain overlook, warm orange sunrise "
    "breaking over layered ridges, soft mist in the valley below, long "
    "shadows, cinematic golden-hour light. "
    "The two panels are divided by a thin straight vertical line. "
    "Crisp focus, high detail, professional editorial photography style. "
    "Text appears ONLY in the left panel."
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
    req = urllib.request.Request(image_urls[0], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    tmp = HOME / "AppData/Local/hermes/cache/wolverine_campaign_raw_v2.jpg"
    tmp.write_bytes(data)
    print(f"Saved raw: {tmp} ({len(data):,} bytes)")
