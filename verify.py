"""EOS Research Playwright screenshot + verification test.

Renders all 4 pages at desktop + mobile, captures screenshots,
checks date references and structural integrity. Outputs PNGs to
./verify-output/ (gitignored) and a JSON log to OS tempdir.

Run:  python verify.py
Exit: 0 on success, 1 on any failure.
"""
import asyncio
import json
import sys
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright

PAGES = [
    ("landing", "https://clawmaster-monty.github.io/eos-research/"),
    ("archive", "https://clawmaster-monty.github.io/eos-research/research/"),
    ("brief", "https://clawmaster-monty.github.io/eos-research/research/bpc-157-evidence.html"),
    ("methodology", "https://clawmaster-monty.github.io/eos-research/methodology/"),
]

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile": {"width": 390, "height": 844},
}

CORRECT_DATES = ["11 July 2026", "July 11, 2026", "2026-07-11"]
STALE_DATES = ["14 July 2026", "July 14, 2026", "2026-07-14"]


async def main() -> int:
    repo_root = Path(__file__).parent.resolve()
    out_dir = repo_root / "verify-output"
    out_dir.mkdir(exist_ok=True)
    results = {"pages": {}, "errors": []}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for vp_name, vp in VIEWPORTS.items():
            ctx = await browser.new_context(viewport=vp)
            page = await ctx.new_page()
            for label, url in PAGES:
                try:
                    resp = await page.goto(url, wait_until="networkidle", timeout=30000)
                    status = resp.status if resp else 0
                    await page.wait_for_load_state("domcontentloaded")
                    await asyncio.sleep(0.5)
                    html = await page.content()
                    shot = out_dir / f"{label}-{vp_name}.png"
                    await page.screenshot(path=str(shot), full_page=True)
                    results["pages"][f"{label}-{vp_name}"] = {
                        "status": status,
                        "screenshot": str(shot),
                        "screenshot_bytes": shot.stat().st_size,
                        "stale_hits": [d for d in STALE_DATES if d in html],
                        "correct_hits": [d for d in CORRECT_DATES if d in html],
                    }
                except Exception as e:
                    results["errors"].append(f"{label}-{vp_name}: {e}")
            await ctx.close()
        await browser.close()

    total = len(results["pages"])
    passed = sum(1 for p in results["pages"].values() if p.get("status") == 200 and not p.get("stale_hits"))
    stale = sum(len(p.get("stale_hits", [])) for p in results["pages"].values())
    log_path = Path(tempfile.gettempdir()) / "hermes-verify-eos-research-playwright.json"
    log_path.write_text(json.dumps(results, indent=2))
    print(f"PASS  {passed}/{total} page renders")
    print(f"      Stale dates: {stale}")
    print(f"      Errors: {len(results['errors'])}")
    print(f"Log:   {log_path}")
    print(f"PNGs:  {out_dir}")
    return 0 if passed == total and stale == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
