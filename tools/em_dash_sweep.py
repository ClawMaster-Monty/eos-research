"""Em-dash sweep, v2: whitespace-tolerant matching.

The HTML wraps prose across lines, so exact-string match fails. Each needle
is normalized to a regex where any run of whitespace matches \s+; the
em-dash (—) is matched literally. Replacement text is joined to single
spaces (HTML renders identically).
"""
import re
from pathlib import Path

RETA = Path(r"C:\Users\monty\eos-research\research\_drafts\retatrutide-evidence.html")
WOLV = Path(r"C:\Users\monty\eos-research\research\wolverine-stack-bpc-tb500-evidence.html")

RETA_FIXES = [
    ("Retatrutide: The Trial Results Are Real. The Online Certainty Is Not. — EOS Research Review Draft",
     "Retatrutide: The Trial Results Are Real. The Online Certainty Is Not. | EOS Research Review Draft"),
    ("Moderate Confidence — Short-term Adult Trial Results",
     "Moderate Confidence: Short-term Adult Trial Results"),
    ("produced unusually large weight and glycaemic changes in randomized trials — including phase-3 data now reported at conference and press-release level.",
     "produced unusually large weight and glycaemic changes in randomized trials, including phase-3 data now reported at conference and press-release level."),
    ("tell us about retatrutide — and what claims circulating online run ahead of the evidence?",
     "tell us about retatrutide, and what claims circulating online run ahead of the evidence?"),
    ("1. The phase-2 obesity result was large — and bounded",
     "1. The phase-2 obesity result was large, and bounded"),
    ("at the time — and it remains a phase-2 result, not a long-term outcomes or active-comparator result.",
     "at the time, and it remains a phase-2 result, not a long-term outcomes or active-comparator result."),
    ("similar to other obesity treatments — not that lean mass was unchanged or that muscle-preservation questions are solved.",
     "similar to other obesity treatments, not that lean mass was unchanged or that muscle-preservation questions are solved."),
    ("4. Phase-3 obesity data exist — as conference and press-release results",
     "4. Phase-3 obesity data exist as conference and press-release results"),
    ("These are substantive results — and they are not yet peer-reviewed or posted to ClinicalTrials.gov.",
     "These are substantive results, and they are not yet peer-reviewed or posted to ClinicalTrials.gov."),
    ("the completed phase-3 retatrutide programs — TRIUMPH-1 (obesity), TRIUMPH-2 (obesity with type 2 diabetes), TRIUMPH-3 (severe obesity with cardiovascular disease), and TRIUMPH-4 (knee osteoarthritis) — all carry",
     "the completed phase-3 retatrutide programs (TRIUMPH-1 obesity, TRIUMPH-2 obesity with type 2 diabetes, TRIUMPH-3 severe obesity with cardiovascular disease, and TRIUMPH-4 knee osteoarthritis) all carry"),
    ("cited for lack of sterility assurance — a US-wide recall of unapproved product initiated 30 July 2025.",
     "cited for lack of sterility assurance, a US-wide recall of unapproved product initiated 30 July 2025."),
    ("It is a signal and a research question — not an established causal finding.",
     "It is a signal and a research question, not an established causal finding."),
    ("None of these is a verified causal reaction — product identity, dose, and concurrent medications varied.",
     "None of these is a verified causal reaction; product identity, dose, and concurrent medications varied."),
    ('The "triple agonist" mechanism story — glucagon driving energy expenditure, GIP partitioning fuel, "GLP-3" marketing — was reproduced nearly verbatim across platforms',
     'The "triple agonist" mechanism story (glucagon driving energy expenditure, GIP partitioning fuel, "GLP-3" marketing) was reproduced nearly verbatim across platforms'),
    ("substantial enough to take seriously — including phase-3 numbers now disclosed at conference and press-release level.",
     "substantial enough to take seriously, including phase-3 numbers now disclosed at conference and press-release level."),
    ("Drugs@FDA could not be queried directly (access challenge) — an honest gap; approval status was assessed via openFDA drug-registration search (no match) and registry records.",
     "Drugs@FDA could not be queried directly (access challenge), an honest gap; approval status was assessed via openFDA drug-registration search (no match) and registry records."),
]

WOLV_FIXES = [
    ("measuring self-reported pain—not tissue repair.",
     "measuring self-reported pain, not tissue repair."),
    ("The brief keeps the two apart throughout — evidence for one does not transfer to the other.",
     "The brief keeps the two apart throughout; evidence for one does not transfer to the other."),
    ("short-term safety questions (with a cardiac-regeneration development context)—not commercial TB-500 or musculoskeletal recovery.",
     "short-term safety questions (with a cardiac-regeneration development context), not commercial TB-500 or musculoskeletal recovery."),
    ("EOS therefore treats published research as one evidence lane—not the boundary of discovery.",
     "EOS therefore treats published research as one evidence lane, not the boundary of discovery."),
    ("Thymosin-beta-4 attracted real capital—and still stalled repeatedly",
     "Thymosin-beta-4 attracted real capital, and still stalled repeatedly"),
    ('identified "TB-500" as Ac-LKKTETQ—the acetylated seven-amino-acid fragment, not full-length thymosin beta-4.',
     'identified "TB-500" as Ac-LKKTETQ, the acetylated seven-amino-acid fragment, not full-length thymosin beta-4.'),
    ("formulation identity, sterility, purity, abundance, and endotoxin are part of the intervention—not side issues.",
     "formulation identity, sterility, purity, abundance, and endotoxin are part of the intervention, not side issues."),
    ("The familiar explanation—that BPC-157 works locally while TB-500 recruits repair cells systemically—is a market narrative",
     "The familiar explanation (that BPC-157 works locally while TB-500 recruits repair cells systemically) is a market narrative"),
    ('be described as hypotheses—not demonstrated outcomes.',
     'be described as hypotheses, not demonstrated outcomes.'),
    ("overwhelmingly animal, bee, review, or in-vitro projects—not hidden human treatment datasets.",
     "overwhelmingly animal, bee, review, or in-vitro projects, not hidden human treatment datasets."),
    ("Positive reports existed—but attribution was weak",
     "Positive reports existed, but attribution was weak"),
    ("a large, heterogeneous public-experience record behind that adoption — people reporting real functional gains, people reporting nothing, people reporting setbacks and adverse events.",
     "a large, heterogeneous public-experience record behind that adoption (people reporting real functional gains, people reporting nothing, people reporting setbacks and adverse events)."),
    ("are doing the work the research system has not done — but self-reports, even in large numbers, cannot substitute for a trial",
     "are doing the work the research system has not done, but self-reports, even in large numbers, cannot substitute for a trial"),
    ("an insistence that the next step is a better study — not a better argument.",
     "an insistence that the next step is a better study, not a better argument."),
]


def ws_regex(needle):
    """Normalize needle to a regex: literal em-dash, whitespace runs -> \s+."""
    out = []
    for ch in needle:
        if ch == "—":
            out.append(r"—")
        elif ch.isspace():
            out.append(r"\s+")
        else:
            out.append(re.escape(ch))
    return re.compile("".join(out))


def apply(fname, fixes):
    p = Path(fname)
    html = p.read_text(encoding="utf-8")
    applied = 0
    missed = []
    for old, new in fixes:
        rx = ws_regex(old)
        m = rx.search(html)
        if m:
            html = html[: m.start()] + new + html[m.end():]
            applied += 1
        else:
            missed.append(old[:60])
    p.write_text(html, encoding="utf-8")
    remaining = len(re.findall(r"—", html.split('<div class="references-list">')[0]))
    print(f"{p.name}: applied {applied}/{len(fixes)}, remaining prose em-dashes: {remaining}")
    if missed:
        print(f"  MISSED ({len(missed)}):")
        for m in missed:
            print(f"    - {m}...")


apply(RETA, RETA_FIXES)
apply(WOLV, WOLV_FIXES)
