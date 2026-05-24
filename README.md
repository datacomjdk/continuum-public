# Continuum (Work)

A persistent context system for Justin Kintzele (Senior Sales Engineer, Datacom Systems) and SEV, his synthetic SE partner. Solves two gaps at once:

1. **Volatile memory** in LLMs: rules, preferences, and project state don't survive session boundaries reliably.
2. **Specialized synthetic workforce**: one generalist AI stretched across every domain produces thin output; specialized personas with tight voice and scope produce better work.

## How Continuum works: Semantic Compression

Continuum is a semantic compression system. Dense, high-signal source material (persona cards, rules, rituals, roadmap) gets expanded by the AI into execution artifacts (proposals, emails, decks, code). The compression ratio is deliberate: persona cards are terse so the rules are legible, rituals are short so they're actually followed, rules are explicit so violations are catchable.

Failure mode to name explicitly: **expansion without validation = slop.** The yellow-arrow incident on April 21, 2026 was this failure mode. AI expanded a weak context (memory summary instead of the actual template file) into execution (a deck), and nobody validated before declaring done. Every ritual in this system exists in part to prevent that.

## Scope

This Continuum is **work-only**. It is owned by Datacom Systems and scoped to Justin's role as Senior Sales Engineer. It does not contain personal projects, personal financial planning, or any non-work domain content. A separate personal Continuum, if built, lives in its own repo under personal ownership with no cross-contamination.

## The two-tier architecture

Continuum is split into two physically separate directories on the local machine:

```
~/DatacomWorkspace/
├── continuum/           ← GIT-TRACKED, pushed to Datacom-owned repo
└── continuum-local/     ← LOCAL-ONLY, never initialized as git, never pushed
```

### What goes in `continuum/` (git-tracked)

The *system* of Continuum: patterns, rules, and reusable structure.

- Persona cards (SEV, future synths): voice, rules, rituals, scope
- Brand rules (colors, logo, typography, public Datacom branding)
- General product rules (ORION vs VS-AFS category boundary, SKU decoding format, writing conventions)
- Rituals (behavior protocols)
- North Star roadmap (aspirational missions, no deal specifics)
- Templates (spec files only; actual template assets stay local)

### What goes in `continuum-local/` (local-only)

The *content* flowing through Continuum: specifics, sensitive material, work product.

- Active state with customer names, deal progress, BOM specifics
- Collaborator cards (informal color on real colleagues)
- Open product questions waiting on Tomy or other internal sources
- Competitive intel specifics (pricing, win/loss details, un-sourced intel)
- Internal codenames and pre-release product info
- In-flight roadmap with deal names
- Session scratchpads
- Actual template assets (.pptx, .docx files themselves)

### Why physical separation instead of .gitignore

Physical separation means `git add .` in the tracked directory can never accidentally commit sensitive content. No gitignore rules to maintain, no cognitive overhead of "is this file tracked or not." The separation is a directory-level boundary, not a filename pattern.

See `SANITIZATION.md` at the root of `continuum/` for the detailed contract.

## Trigger phrases (v1)

Start small. Add more only when real need emerges.

| Phrase | What SEV does |
|---|---|
| `Run POST` or `POST check` | Verify git identity, repo remote, local directory presence, workspace health. See `rituals/post_check.md`. |
| `Load Continuum` | Run POST, then read persona, shared rules, current roadmap, relevant collaborator cards. Acknowledge load. |
| `Call in [name]` | Switch active persona (Speaker's Podium rule: only one mic at a time). Read that persona's files. Respond in that voice. |
| `Back to SEV` | Switch back to default. |
| `Commit this` | Propose a changeset summary. Justin reviews, edits, commits. |
| `Build mode` | Leave planning, start producing the deliverable. |
| `Update the roadmap` | Propose updates to roadmap files based on current session and in-flight work. |
| `Hire a new synth` | Start the persona creation ritual. |
| `Frame this problem` | Apply the three-part problem frame (see `rituals/problem_frame.md`). |
| `OOB audit` | Invoke out-of-band validation for a high-stakes deliverable (see `rituals/oob_audit.md`). |
| `Run calibration` | Monthly or quarterly check on autonomy, complacency, drift (see `rituals/calibration.md`). |

## Workflow

**Session start:** Justin says "Load Continuum." SEV runs POST, reads the relevant files, acknowledges.

**During session:** Work happens. SEV maintains running notes in `continuum-local/scratchpad/YYYY-MM-DD_session.md`.

**Session close:** Justin says "Commit this." SEV produces a diff proposal separated by tier. Justin reviews, edits, runs `git commit` and `git push` on the tracked tier; saves the local tier through whatever backup mechanism he uses.

## What Continuum is NOT

- Not automatic. SEV proposes; Justin commits.
- Not a substitute for Justin's judgment. SEV is a multiplier, not a replacement.
- Not an impersonation system. Collaborator cards are context, not roleplay scripts.
- Not a personal-life system. Work-scoped only.
- Not a microservices platform yet. File-based v1, iterate from there.

## Version

v1.1 — April 22, 2026. Folded in eight updates from review: AFT source classification, OOB audit ritual, Speaker's Podium rule, Signal Check / codec framing, Autonomy Check via calibration ritual, explicit state-sync language, semantic compression framing, Agent Smith boundary statement.

## Parallel system: Agent Smith

A personal Continuum called Agent Smith exists, owned by Justin personally, scoped to personal projects. Agent Smith and this work Continuum share patterns (two-tier architecture, rituals, sanitization approach) through a separate pattern library repo, but they do not share content. Never. The SANITIZATION.md contract makes this explicit. If Justin mentions Agent Smith, context is noted and we proceed with whatever work Continuum task is at hand — no content crosses the boundary.

## Pattern library (future infrastructure)

A third repo, `continuum-patterns/`, exists as a pattern library containing only the generic Continuum architecture: ritual definitions, sanitization contract format, two-tier structure, persona card template, trigger phrase conventions. Owned neutrally (not by Datacom, not personally under Justin's name as work-related — more like a personal project with permissive licensing).

**Current practice:** tactically, both this Continuum and Agent Smith each maintain their own copy of the patterns. The pattern library repo exists as infrastructure but is not yet referenced as a live submodule or dependency. This is intentional Option B (duplicated patterns) riding on top of Option C (shared repo as backstop) so we can extract and publish stable patterns later without retrofit.

**Decision cadence:** once a ritual or pattern has been stable and used for 3+ months across both Continuums without modification, it becomes a candidate for promotion into the shared library. Until then it lives in each Continuum independently.

## Source of Truth (AFT) classification

Every file in the tracked tier carries a source classification at the top:

- `Source: user-authored` — Justin wrote or explicitly directed this content
- `Source: public-documented` — Sourced from publicly-available Datacom marketing, product documentation, or competitor public websites
- `Source: AI-generated, user-reviewed` — SEV drafted, Justin reviewed and accepted

This makes audit trivial and prevents AI-generated content from silently becoming "truth" without review. The rule: **AI-generated content never lives in the tracked tier without the user-reviewed stamp.**
