"""Surgical fixes to the Wolverine draft source (backup) before re-transform.

Removes two fictional ClinicalTrials.gov records (NCT07437547, NCT07487363),
rewrites the three claims + scorecard row built on them, fixes 5 author
initials, the WADA URL, and the preprint title, then renumbers in-text
citations to match the shrunken reference list.

Uses only exact-string replacements with whitespace-normalized matching.
"""
import re
from pathlib import Path

BAK = Path(r"C:\Users\monty\eos-research\research\_drafts\wolverine-stack-bpc-tb500.review-draft.bak.html")
html = BAK.read_text(encoding="utf-8")
original_len = len(html)
print(f"Original: {original_len} chars, {html.count(chr(10))+1} lines")


def ws_normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def replace_ws_flexible(html, old, new, label):
    """Replace `old` allowing any whitespace runs to match; returns (html, ok)."""
    pattern = re.compile(re.escape(ws_normalize(old)).replace(r"\ ", r"\s+"))
    m = pattern.search(html)
    if m:
        return html[: m.start()] + new + html[m.end():], True
    print(f"  MISS: {label}")
    return html, False


# --- 1. Rewrite the three claims + scorecard built on fictional trials ---
claims = [
    (
        "The development story is not uniformly dead. A 120-person phase-II BPC-157 hamstring-strain trial and an\n"
        "      80-person cardiovascular-biomarker study defining TB-500 as the thymosin-beta-4 17\u201323 fragment were registered\n"
        "      as recruiting in 2026. Neither has results.[18][22]",
        "The development record is stalled rather than active: the only controlled BPC-157 human registration located\n"
        "      for this audit (NCT02637284) has carried Unknown status with no posted results since 2015, and two 2026\n"
        "      registry entries that appeared to show new BPC-157 and TB-500 development were identified during\n"
        "      verification as example/mock records and excluded from this audit.",
        "dev-story claim",
    ),
    (
        "As of this audit, a randomized Chinese phase-II study in 120 adults with MRI-confirmed grade-II hamstring strain is registered and recruiting, but it has no results.[18]",
        "A 2026 ClinicalTrials.gov entry suggesting an active BPC-157 hamstring trial was identified during verification as an example/mock record and is excluded from this audit.",
        "hamstring claim",
    ),
    (
        "A recruiting cardiovascular registry now explicitly defines its investigational TB-500 as the thymosin-beta-4 17\u201323 fragment. It is not a musculoskeletal study and has no results.[22]",
        "A 2026 registry entry defining its investigational TB-500 as the thymosin-beta-4 17\u201323 fragment was identified during verification as a fictional example record and is excluded from this audit.",
        "TB-500 registry claim",
    ),
    (
        "A BPC-157 hamstring trial is recruiting.",
        "A 2026 registry entry suggesting an active hamstring trial was identified as an example record and excluded.",
        "scorecard row",
    ),
]

for old, new, label in claims:
    html, ok = replace_ws_flexible(html, old, new, label)
    if ok:
        print(f"  ✓ {label}")

# --- 2. Remove the two fictional <li> reference entries (exact li-match) ---
for needle, label in [("NCT07437547", "hamstring trial"), ("NCT07487363", "TB-500 registry")]:
    # find the exact <li>...</li> containing the needle using a non-greedy match anchored to a single li
    pattern = re.compile(r"<li>(?:(?!</?li>).)*?" + re.escape(needle) + r"(?:(?!</?li>).)*?</li>", re.DOTALL)
    m = pattern.search(html)
    if m:
        html = html[: m.start()] + html[m.end():]
        print(f"  ✓ removed ref li: {label}")
    else:
        print(f"  MISS: ref li {label}")

# --- 3. Fix author initials (inside reference <li> entries) ---
author_fixes = [
    ("Rahaman MA, et al.", "Rahaman KA, et al."),
    ("Wang J, et al. Recombinant full-length thymosin-beta-4", "Wang X, et al. Recombinant full-length thymosin-beta-4"),
    ("Lee E, Burgess S. IV BPC-157 safety pilot", "Lee E, Burgess K. IV BPC-157 safety pilot"),
    ("Stenfeldt AL, et al.", "Delcourt V, et al."),
    ("Esposito S, et al. Mass-spectrometric identification", "Cox HD, et al. Detection and in vitro metabolism of the confiscated peptides BPC 157 and MGF R23H"),
]
for old, new in author_fixes:
    if old in html:
        html = html.replace(old, new)
        print(f"  ✓ author fix: {old.split(',')[0]}")
    else:
        print(f"  MISS author: {old.split(',')[0]}")

# --- 4. WADA URL ---
wada_old = "https://www.wada-ama.org/en/resources/world-anti-doping-program/2026-prohibited-list"
if wada_old in html:
    html = html.replace(wada_old, "https://www.wada-ama.org/en/prohibited-list")
    print("  ✓ WADA URL")
else:
    print("  MISS WADA URL")

# --- 5. Preprint title ---
preprint_old = "Mendias CL, Awan TM. Quality Assessment of Unregulated Peptide Therapeutics."
if preprint_old in html:
    html = html.replace(
        preprint_old,
        "Mendias CL, Awan TM. Evaluation of Research Grade Peptides Marketed Directly to Consumers Reveals Extensive Variability in Purity and Measured Abundance.",
    )
    print("  ✓ preprint title")
else:
    print("  MISS preprint title")

# --- 6. Renumber in-text citations after removing entries 18 and 22 ---
def renumber(match):
    body = match.group(0)
    def subnum(m2):
        n = int(m2.group(0))
        if n > 22:
            n -= 2
        elif n > 18:
            n -= 1
        return str(n)
    return re.sub(r"\d+", subnum, body)

before = html
html = re.sub(r"\[\d+(?:[\u2013-]\d+)?\]", renumber, html)
print(f"  {'✓' if html != before else '✗ NO'} in-text citation renumber")

BAK.write_text(html, encoding="utf-8")
print(f"\nSaved: {BAK}")
print(f"New length: {len(html)} chars, {html.count(chr(10))+1} lines")
