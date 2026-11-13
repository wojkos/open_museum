---
project: "CNK Kompas"
version: 2
status: draft
created: 2026-08-27
updated: 2026-08-27
prd_version: 1
main_goal: open-source split
top_blocker: package/repo rename churn
---

# Roadmap: Open-Museum / CNK Kompas Split

> Derived from `context/foundation/open-source-strategy.md`. Supersedes the v1 MVP roadmap, archived at `context/foundation/archive/2026-08-27-roadmap.md` (all MVP slices there are `done`).
> Edit-in-place; archive when superseded.
> Slices below are listed in dependency order. The "At a glance" table is the index.

## Vision recap

CNK Kompas started as a single-museum MVP for Centrum Nauki Kopernik. The codebase turned out to be largely museum-agnostic (matching engine, anonymous visit analytics, bilingual intake flow), so the project is splitting in two: **`open-museum`**, a public museum-agnostic core anyone can deploy, and **`cnk-kompas`**, a thin fork carrying only CNK's branding, content, and deploy config. See `context/foundation/open-source-strategy.md` for the full rationale.

## North star

The smallest complete flow that proves the split works: the app runs correctly with **zero CNK-specific content**, driven entirely by settings/theme/seed-data seams — while CNK Kompas itself keeps working unchanged as a fork on top of those seams.

**M-02: The app runs in fully generic mode (no CNK strings anywhere outside fork-seam files)** — this is the checkpoint that proves genericization is complete and safe to fork from.

## At a glance

| ID | Change ID | Outcome (user can …) | Prerequisites | PRD refs | Status |
|---|---|---|---|---|---|
| M-01 | genericize-branding-and-theme | (foundation) branding, theme colors/fonts, AI prompt museum name, and default language are settings-driven instead of hardcoded | — | open-source-strategy.md §Genericization mechanism | done |
| M-02 | verify-generic-mode | a deployer confirms the app runs correctly with only generic/example content, no CNK strings leak outside fork-seam files | M-01 | open-source-strategy.md §Migration sequence step 2 | done |
| M-03 | extract-open-museum-core | the generic core is published as its own `open-museum` public repo (new name, README, license) | M-02 | open-source-strategy.md §Target architecture (core) | done |

## Streams

Navigation aid — groups items that share a Prerequisites chain. All migration work is a single linear chain (`M-01` → `M-06`); there's no parallel track since each step's output is the next step's input (genericize → verify → extract core → fork → deploy → document).

| Stream | Theme | Chain | Note |
|---|---|---|---|
| A | Genericize in place | `M-01` → `M-02` | Done inside this repo while it's still one codebase, so "generic mode" and "CNK mode" can be compared side by side before any split. |

## Baseline

What's already in place as of `2026-08-27` (see `context/foundation/open-source-strategy.md` §Why for the full audit).

- **Domain logic:** done — matching engine, anonymous visit models, bilingual intake flow, operator password-gate are already museum-agnostic; no changes needed.
- **Branding/theme:** not started — "CNK Kompas" strings and the Bauhaus palette are hardcoded in templates and `DESIGN.md`, not settings-driven.
- **Seed content:** not started — `exhibits/seed_data.py` holds real CNK exhibits, not swappable example data.
- **AI prompt:** not started — `exhibits/ask_more.py` hardcodes "Centrum Nauki Kopernik".
- **Repo/package naming:** complete — package is `open_museum`; the generic core keeps `LANGUAGE_CODE` defaulting to `pl`.
- **Two-repo split:** not started — only one repo exists today.

## Foundations

### M-01: Genericize branding and theme

- **Outcome:** (foundation) branding strings, theme colors/fonts, the AI prompt's museum name, and the default language are all settings-driven instead of hardcoded, while CNK Kompas keeps working unchanged via those same settings.
- **Change ID:** genericize-branding-and-theme
- **PRD refs:** `open-source-strategy.md` §Genericization mechanism
- **Unlocks:** M-02; everything downstream depends on the seams existing first.
- **Prerequisites:** —
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:**
  - Exact new settings names (`MUSEUM_NAME`, theme token file location) — Owner: user. Block: no.
  - Whether `exhibits/seed_data.py` becomes fully swappable now or only at fork time — Owner: user. Block: no.
- **Risk:** Doing this in-place, one repo, makes it easy to verify nothing broke for CNK Kompas before any repo split happens.
- **Status:** done

## Slices

### M-02: Verify generic mode

- **Outcome:** a deployer can run the app configured with only generic/example content (no seed data, branding, or prompt text tied to CNK) and confirm every flow still works.
- **Change ID:** verify-generic-mode
- **PRD refs:** `open-source-strategy.md` §Migration sequence step 2
- **Prerequisites:** M-01
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:** —
- **Risk:** This is the checkpoint that proves the seams are actually clean; skipping it risks discovering leftover CNK strings only after the repo split, when fixing them means touching two repos instead of one.
- **Status:** done

### M-03: Extract open-museum core

- **Outcome:** the generic core is published as its own public `open-museum` repo — new package/repo name, generic README, OSS license, template deploy config.
- **Change ID:** extract-open-museum-core
- **PRD refs:** `open-source-strategy.md` §Target architecture (core)
- **Prerequisites:** M-02
- **Parallel with:** —
- **Blockers:** OSS license choice; exact new package name — both open questions in `open-source-strategy.md`.
- **Unknowns:**
  - Final package name for `open_museum` (mechanical rename across imports) — Owner: user. Block: yes.
  - License choice — Owner: user. Block: yes.
- **Risk:** Package rename is the largest mechanical change in the whole migration; doing it once, after M-02 proves the seams work, avoids redoing it.
- **Status:** done

## Backlog Handoff

| Roadmap ID | Change ID | Suggested issue title | Ready for `/10x-plan` | Notes |
|---|---|---|---|---|
| M-01 | genericize-branding-and-theme | Genericize branding, theme, AI prompt, and default language | yes | Can start immediately; no prerequisites. |
| M-02 | verify-generic-mode | Verify the app runs correctly in fully generic mode | no | Needs M-01 first. |
| M-03 | extract-open-museum-core | Extract `open-museum` as its own public repo | no | Blocked on license + package-name decisions. |

## Parked

- **Real CNK exhibit mapping, exhibit photos, guided walking route, in-building turn-by-turn navigation, in-app AI chat, native mobile app, expanded observability** — carried over unchanged from the v1 roadmap; see `context/foundation/archive/2026-08-27-roadmap.md` §Parked for full rationale. None of these are affected by the open-source split.

## Done (pre-split MVP)

All S-01…S-09 and F-01…F-02 slices from the original CNK Kompas MVP roadmap are `done` and archived at `context/foundation/archive/2026-08-27-roadmap.md`. They are not repeated here since this roadmap covers the open-source split, not the MVP feature set.

- **M-01: (foundation) branding, theme colors/fonts, AI prompt museum name, and default language are settings-driven instead of hardcoded** — Archived 2026-08-27 → `context/archive/2026-08-27-genericize-branding-and-theme/`. Lesson: —.
- **M-02: a deployer confirms the app runs correctly with only generic/example content, no CNK strings leak outside fork-seam files** — Archived 2026-08-27 → `context/archive/2026-08-27-verify-generic-mode/`. Lesson: —.

