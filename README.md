# EOS Research

Long-form science at the intersection of longevity, fitness, and mindful living.

**Live at:** `clawmaster-monty.github.io/eos-research/` (once GitHub Pages is enabled)

## The model

**One work, two surfaces.**

A research finding is produced once. It publishes in long form here on EOS Research — with citations, methodology, and full context. A distilled 200-300 word version is posted to EOS Commons Discord to spark member discussion. The community's questions and pushback then feed back into the next revision.

```
Research work
     │
     ▼
[Long-form brief]
     │
     ├──→ EOS Research (this site, full piece)
     │
     └──→ EOS Commons (snippet, discussion driver)
```

## Structure

```
eos-research/
├── index.html           # Landing page — latest briefs, archive link
├── research/            # Archive of all briefs
│   └── index.html
├── assets/
│   └── css/             # (optional, for future)
└── drafts/              # In-progress briefs (gitignored)
```

## Adding a new brief

1. Write the long-form piece in `drafts/<slug>.md`
2. Convert to `research/<slug>.html` when ready
3. Update `index.html` to include the new card
4. Extract 200-300 word snippet → post to EOS Commons Discord

## Stack

- Plain HTML + CSS (no JS frameworks)
- GitHub Pages for hosting
- Manual publishing (intentional — quality > speed)

## Sister sites

- **EOS Commons** — the community: `clawmaster-monty.github.io/eos-commons/`
- **EOS Research** — long-form science (this site)

Both are independent projects under the EOS Commons umbrella.