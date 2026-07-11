# EOS Research — Complete Handoff Document

> **For:** ChatGPT (or any AI assistant) helping design and build this site
> **Date:** July 11, 2026
> **Owner:** Monty (founder, EOS Commons)
> **AI Operator:** Nox (Hermes Agent, MiniMax-M3 default)

---

## 1. Governance: Who Maintains, Updates, Contributes

### Roles

| Role | Person / Entity | Responsibility |
|------|----------------|----------------|
| **Owner / Editor-in-Chief** | Monty | Final approval on every published brief. Reviews all long-form content before it goes live. Owns brand voice and direction. |
| **Primary Author / AI Operator** | Nox (Hermes Agent) | Drafts briefs, researches sources, structures arguments, extracts snippets for Commons. Pushes directly to the repo. |
| **Visual Designer / Front-end** | ChatGPT (this session, ongoing) | Owns the visual design, CSS, page templates, and UX. Doesn't write content. |
| **Reviewer / Cross-checker** | TBD (human, future) | When community grows, a member with relevant expertise can be invited to peer-review specific briefs in their domain (e.g., a sleep researcher for a sleep brief). |
| **Future Contributors** | Invited members | A submission form and review pipeline is a future feature. Not built yet. |

### Publishing Workflow

```
Research trigger (scanner, member question, Nox initiative)
    ↓
Nox: literature review → draft long-form brief (in `drafts/`)
    ↓
Nox: self-review against methodology checklist
    ↓
Nox: hands draft to Monty via Telegram (paste + link)
    ↓
Monty: edits, approves, or requests revisions (in chat)
    ↓
Nox: moves from `drafts/` to `research/`, adds card to `index.html`
    ↓
Nox: extracts 200-300 word snippet
    ↓
Nox: posts snippet to EOS Commons Discord (sister channel)
    ↓
Nox: posts short version to BlueSky with link to full brief
```

### Cadence Targets

- **Minimum:** 1 brief / week
- **Comfortable:** 1 brief / 2 weeks
- **Stretch:** 2 briefs / week (only if backlog supports it)

### Contribution Rules

1. **No medical advice.** Every brief carries the standard EOS Commons disclaimer.
2. **Cite everything.** PubMed IDs, DOIs, arXiv references — no "studies show" without a citation.
3. **Distinguish evidence levels.** Preclinical vs. RCT vs. anecdotal — clearly labeled.
4. **Acknowledge what we don't know.** "What we don't know" section is mandatory.
5. **Anti-billboard.** No affiliate links, no product pitches, no vendor mentions.
6. **Anti-dogma.** Multiple valid perspectives are fine. "This is what the evidence says" not "this is what you should do."
7. **Plain language.** If a 5th grader can't follow the TL;DR, simplify it.
8. **Monty's review is final.** No auto-publish. Ever.

### Maintenance Plan

| Task | Frequency | Who |
|------|-----------|-----|
| Broken link check | Monthly | Nox (cron job TBD) |
| Citation verification | Quarterly | Nox + Monty spot-check |
| Visual refresh | Annually | ChatGPT session |
| Domain migration (if/when) | One-time | Nox |
| SEO / sitemap refresh | Quarterly | Nox |

---

## 2. Site Architecture

### Current State (live)

```
eos-research/
├── index.html              # Landing page — hero + latest brief card
├── research/
│   └── index.html          # Archive landing — methodology + chronological list
├── README.md               # The "one work, two surfaces" model explanation
├── _config.yml             # Jekyll config (minimal theme, ready to upgrade)
├── .gitignore
└── HANDOFF.md              # This file
```

**Live URL:** https://clawmaster-monty.github.io/eos-research/

**Tech stack:**
- Plain HTML + CSS (no JavaScript)
- GitHub Pages hosting
- Jekyll-compatible (could upgrade later without breaking existing pages)

### Pages That Need To Be Built

#### Priority 1 (this week)
1. **Brief template (`research/<slug>/index.html`)** — the actual article page. Most important. Without it, no briefs can be published.
2. **Archive grid view** — replace the placeholder single card on `research/index.html` with a real grid of all published briefs.

#### Priority 2 (next 2 weeks)
3. **Pillar filter / search** — filter by longevity, fitness, mindfulness, nutrition, precision protocols
4. **RSS feed (`feed.xml`)** — so subscribers can follow new briefs
5. **About page** — who runs this, how to cite, contact

#### Priority 3 (when there's content)
6. **Submission / contribution page** — for future invited contributors
7. **Citation graph view** — visual map of how briefs reference each other
8. **Methodology page** — separate from archive landing, dedicated deep-dive on how briefs are produced

### URL Plan

| Page | Path | Notes |
|------|------|-------|
| Landing | `/` | Hero + 3 latest briefs |
| Archive | `/research/` | All briefs, filterable |
| Individual brief | `/research/<slug>/` | e.g., `/research/bpc-157-evidence/` |
| About | `/about/` | Team, methodology, contact |
| RSS | `/feed.xml` | Standard feed |
| Sitemap | `/sitemap.xml` | For SEO |

**Slug convention:** lowercase, hyphenated, descriptive. Example: `bpc-157-evidence`, `cosmos-multivitamin-trial`, `wolverine-stack-mechanism`.

### Shortlink / Custom Domain Plan

**Current:** `clawmaster-monty.github.io/eos-research/`

**Target (if/when domain is purchased):** `eosresearch.org`

**When migrating:**
1. Buy `eosresearch.org` (~$12/yr, Cloudflare Registrar recommended)
2. Add `CNAME` file at repo root containing `eosresearch.org`
3. Configure DNS: `eosresearch.org` → `clawmaster-monty.github.io` (apex) + `www` → `clawmaster-monty.github.io`
4. Enable HTTPS in Pages settings (auto via Let's Encrypt)
5. Set up 301 redirects from old GitHub URLs to new domain
6. **Do not migrate until at least 3 briefs are published.** Validate the workflow before buying the domain.

---

## 3. Brand & Visual Direction

### The Brand

**EOS Commons** is the community. Warm, anti-billboard, science-aware. "Dawn is the reset."

**EOS Research** is the long-form publication. Same parent brand, different register:
- Slightly more academic
- More citation-forward
- Less "hey friend," more "let's look at what the evidence actually says"
- Same anti-billboard / anti-dogma stance

**Relationship line:** "One work, two surfaces. Long version here. Discussion there."

### Color Palette (current — feel free to evolve)

```
Background:    #0d1117  (deep navy-black)
Surface:       #161b22  (slightly lighter card)
Border:        #21262d  (subtle dividers)
Text primary:  #e6edf3  (off-white)
Text muted:    #8b949e  (secondary)
Accent:        #58a6ff  (blue — links, highlights)
Green:         #7ee787  (success, "what we know")
Purple:        #d2a8ff  (special)
Yellow:        #ffdf5d  (warnings, "what we don't know")
Red:           #ff7b72  (errors, contradictions)
```

These are GitHub's palette. They work, but ChatGPT may want to evolve them. EOS Commons uses a warm orange (`#ff8c42`); EOS Research should stay cooler / more clinical to differentiate. **Suggestion: keep the navy/blue base, but consider:**

- **Editorial direction:** warm cream background option (`#f6f3ea`) for brief pages, dark for landing — light/dark mode toggle
- **Lab notebook direction:** yellow accents (`#ffdf5d`), monospace fonts, paper texture
- **Journal direction:** strict palette (white/black/one accent), no gradients

### Typography (current)

- System font stack only: `-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif`
- **Opportunity:** ChatGPT should propose serif/sans pairing for brief pages. Recommended pairings:
  - **Serif body, sans headings:** `Charter, Bitstream Charter, 'Sitka Text', Cambria, serif` + system sans
  - **Modern sans:** `Inter` (variable, free) for both
  - **Editorial:** `'IBM Plex Serif'` + `'IBM Plex Sans'` (both free, npm/google fonts)

### Tone Guidelines for Visual Decisions

- **Avoid:** gradients, glass-morphism, neon glows, heavy animations, "AI-y" looks
- **Lean into:** whitespace, clear hierarchy, readable line lengths (60-70ch), generous margins
- **Required:** mobile-responsive, fast load (no JS frameworks), accessible (color contrast AA+)

---

## 4. Content Architecture

### Brief Template (proposed structure)

```markdown
---
title: "BPC-157: What 30 Years of Preclinical Evidence Actually Shows"
authors: "Nox (AI operator), Reviewed by Monty"
date: 2026-07-14
pillar: longevity  # longevity | fitness | mindfulness | nutrition | precision
tags: [bpc-157, peptides, healing, angiogenesis]
tl_dr:
  - 1-2 sentence summary of what the brief concludes
  - Second bullet — the key actionable insight
  - Third bullet — the main caveat
disclaimer: "This brief summarizes published research for educational purposes. Not medical advice."
---

## The Question
What are we actually trying to answer?

## What the Evidence Says
Cite studies (PMID), explain mechanisms, give confidence levels.

## What We Don't Know
Mandatory section. The gaps. The bro-science zones. The overclaimed findings.

## Takeaway
Actionable, anti-dogma, no medical advice. "This is what the evidence suggests, here's what to do with that."

## Methodology Notes
How we searched, what we included/excluded, conflicts of interest.

## References
Numbered. PubMed IDs, DOIs, arXiv IDs. Full citations.

## Related Briefs
- [BPC-157 + TB-500 Wolverine Stack](/research/wolverine-stack-mechanism/)
- [BPC-157 + Ipamorelin](/research/bpc-157-ipamorelin/)

## Discuss in EOS Commons
[Join the discussion in #longevity-science →](https://discord.com/channels/...)
```

### Content Types (planned)

| Type | Length | Cadence | Example |
|------|--------|---------|---------|
| **Research Brief** | 1,500-2,500 words | Weekly | "BPC-157: What 30 Years..." |
| **Synthesis Essay** | 2,500-4,000 words | Monthly | "The peptide evidence landscape: 2026 review" |
| **Methodology Note** | 500-1,000 words | As needed | "How we grade evidence" |
| **Quick Brief** | 500-1,000 words | Bi-weekly | "What the COSMOS trial actually said" |

---

## 5. Technical Specs

### Performance Budget
- First contentful paint: < 1s
- Total page weight: < 200KB
- No JavaScript required to read content
- Lighthouse score: 95+ on all categories

### Accessibility
- WCAG AA compliance minimum
- All text contrasts checked
- Semantic HTML (no div-soup)
- Skip-to-content link
- Keyboard navigable

### SEO
- Per-page `<title>` and `<meta description>`
- Open Graph tags for social sharing
- Twitter Card tags
- JSON-LD structured data (Article schema on brief pages)
- `sitemap.xml` generated
- `robots.txt` allows all

### Browser Support
- Modern evergreen browsers (Chrome, Firefox, Safari, Edge — last 2 versions)
- Mobile Safari iOS 15+
- Graceful degradation (no essential JS)

---

## 6. Sister Sites & Integration

| Property | URL | Relationship |
|----------|-----|--------------|
| EOS Commons (landing) | https://clawmaster-monty.github.io/eos-commons/ | Community signup |
| EOS Commons custom domain | https://eoscommons.org/ | Marketing |
| EOS Research | https://clawmaster-monty.github.io/eos-research/ | Long-form science |
| BlueSky | https://bsky.app/profile/eoscommons.bsky.social | Distribution |
| Discord | (invite-only) | Discussion |

**Cross-linking rules:**
- Every brief ends with a "Discuss in EOS Commons" CTA → Discord channel
- EOS Commons Discord posts that reference research → link to brief
- EOS Commons landing page → "Read the research" link
- BlueSky posts → "Full piece at eosresearch.org" (when domain is live)

---

## 7. Suggested ChatGPT Session Flow

When you open the ChatGPT session, here's the conversation flow I recommend:

### Step 1: Context setting (paste this verbatim)

> "I'm building EOS Research, a long-form science publication that's the research arm of EOS Commons (a private longevity community). The site is live at clawmaster-monty.github.io/eos-research/ — please visit it. The community is warm and anti-billboard; the research site should be calmer, more academic, citation-forward. Same anti-billboard / anti-dogma stance. Audience: curious health optimizers, longevity-interested scientists, future community members. The current site is dark-themed (GitHub palette). I want you to propose 2-3 visual directions, walk me through trade-offs, then help me build out the architecture. Read the README.md and HANDOFF.md in the repo for full context."

### Step 2: Ask ChatGPT to fetch the files

> "Can you read the current index.html, research/index.html, and HANDOFF.md from the repo at github.com/ClawMaster-Monty/eos-research?"

### Step 3: Get a direction proposal

> "Propose 2-3 visual directions. For each, give me: (a) the typography pairing, (b) color palette evolution if any, (c) what stays dark vs what becomes light, (d) sample CSS, (e) one paragraph on what reading this site feels like."

### Step 4: Pick a direction

Then iterate. Don't try to do everything in one session — visual design is iterative.

### Step 5: Build the brief template

Once a direction is locked, ask ChatGPT to build the brief template (`research/<slug>/index.html`).

---

## 8. Asset Inventory

**Already have:**
- 5 EOS Commons Protocol Deep Dives (markdown, in Obsidian vault)
- 1 Biomarker Breakdown (HRV, markdown)
- 1 Daily Multivitamin snippet (Discord post, can be expanded)
- Brand voice: "Science you can feel. Warm community, not cold corporate. Shared discovery, not prescriptive dogma."

**Don't have yet:**
- Citation format standard
- Author bio template
- Featured image / OG image design
- Logo / favicon (currently using 🔬 emoji)

---

## 9. Open Questions for ChatGPT

1. **Dark vs light primary?** GitHub-style dark is current. Editorial sites often go light. What serves the content best?
2. **Brief page width?** 60ch is readable. 70ch is more efficient. 80ch fits more but less readable. ChatGPT's pick?
3. **Citation style?** Vancouver (numbered, [1], [2])? APA inline? Chicago footnotes? Pick one and standardize.
4. **Typography loading strategy?** System fonts (current, fast) vs Google Fonts (more choice, slight load cost)?
5. **Should the archive be a grid or list?** Grid = visual, scannable. List = dense, chronological.

---

## 10. What To Do Right Now

1. **Open ChatGPT** with the prompt in Step 1 above
2. **Have ChatGPT fetch the repo** to read current state
3. **Iterate on visual direction** — don't commit until you've seen at least 2 directions
4. **Build the brief template** (Step 5 above) — that's the highest-value deliverable
5. **When happy**, save files locally in `C:\Users\monty\eos-research\`, then I'll commit and push them

---

*This document is the canonical handoff. Update it whenever the workflow or architecture changes.*

— Maintained by Nox (Hermes Agent)