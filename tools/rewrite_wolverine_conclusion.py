"""Rewrite the Wolverine honest-conclusion section.

The previous conclusion read as dismissal ("interesting—but not proven") to a
community that has actually used the stack at scale, and it retained a claim
("returned to phase-II study") built on a fictional trial record. New version
takes the scale of real-world use seriously as a signal, is precise about what
that signal can and cannot establish, and frames the evidence gap as a failure
of the research system, not of the people using it.
"""
import re
from pathlib import Path

DRAFT = Path(r"C:\Users\monty\eos-research\research\_drafts\wolverine-stack-bpc-tb500.review-draft.html")
html = DRAFT.read_text(encoding="utf-8")

OLD_SECTION_START = "<section>\n    <h2>The honest conclusion</h2>"

NEW_SECTION = """<section>
    <h2>The honest conclusion</h2>
    <p>
      The Wolverine stack is not an obscure experiment. It is one of the most
      widely used unapproved recovery protocols in the peptide community, and
      this audit found a large, heterogeneous public-experience record behind
      that adoption — people reporting real functional gains, people reporting
      nothing, people reporting setbacks and adverse events. That scale is
      itself evidence: evidence of attention, of perceived benefit, and of a
      question the community has effectively been running at population scale
      for years. It is not, by itself, evidence of efficacy. Both things are
      true at once, and a credible audit has to hold them together.
    </p>
    <p>
      The controlled record is thin, and it must be described accurately:
      BPC-157 has repeated positive animal models but no published randomized
      human healing trial; the only published human musculoskeletal report is
      one uncontrolled knee-pain series; TB-500 is a chemically distinct
      fragment, not full-length thymosin beta-4; and no controlled study has
      tested the blend itself or demonstrated synergy. Those are gaps in
      <em>controlled</em> evidence, not a finding that nothing is happening.
      The single most important correction this audit makes to the marketing
      narrative is narrower than "it doesn't work": it is that nobody has yet
      run the study that would let anyone say, with a straight face, how well
      this works, for which injuries, at what dose, with which product, and at
      what risk.
    </p>
    <p>
      The absence of that study is not the community's fault, and it is not a
      verdict on the people using the stack. It is a structural feature of the
      market: an unapproved peptide that cannot justify pivotal-trial capital
      while unregulated sales reward marketing instead of verification. The
      people sharing their results in forums, YouTube, and recovery groups are
      doing the work the research system has not done — but self-reports, even
      in large numbers, cannot substitute for a trial that controls for
      rehabilitation, time, placebo, and product identity. The community's
      reports are the reason this question deserves a real study, not the
      reason to pretend one already exists.
    </p>
    <p>
      What would move this from "widely used, not yet tested" to "tested" is
      specific and achievable: a controlled trial of a characterized product
      against placebo with standardized rehabilitation, structural endpoints
      where possible, and honest adverse-event collection. Until that exists,
      the evidence-honest position is not dismissal and not endorsement. It is
      respect for what the community has documented, precision about what that
      documentation can and cannot prove, and an insistence that the next step
      is a better study — not a better argument.
    </p>
    <p><strong>Widely used. Not yet tested. The people are ahead of the research. Look closer. Claim less.</strong></p>
  </section>"""

start = html.find(OLD_SECTION_START)
assert start >= 0, "conclusion section start not found"
end = html.find("</section>", start)
assert end >= 0, "conclusion section end not found"
end += len("</section>")

new_html = html[:start] + NEW_SECTION + html[end:]
DRAFT.write_text(new_html, encoding="utf-8")
print(f"Conclusion rewritten: {len(NEW_SECTION)} chars -> {len(new_html)} total")
