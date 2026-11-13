# Lessons

Index of lessons learned. Read before starting work; append after every bug fix, correction, or non-obvious finding.

- Keep this file short: one line per lesson, linking to a detail file in `.ai/lessons/` when more than a line is needed.
- Detail files: `.ai/lessons/YYYY-MM-DD-slug.md`.
- Promote a lesson into `AGENTS.md` only if it is a durable, repo-wide rule.

## Entry format

`- YYYY-MM-DD — <rule or finding, imperative> ([details](lessons/YYYY-MM-DD-slug.md))`

## Lessons

<!-- newest first -->
- 2026-11-13 — Administrate 1.0 + Mobility works but needs `administrate-field-active_storage`, Mobility `locale_accessors`, a custom field (partials in `fields/<field_class_underscored>/`) and an `i18n`-scope concern for sort/search; Administrate sort params are `exhibit[order]`, and request tests need `rails test`, not `rails runner` (spike: branch `prototype/administrate-spike`).
- 2026-11-13 — Polish for Exhibit is *Eksponat*, never *Ekspozycja* (exposition); check the glossary before translating domain terms.
- 2026-11-13 — Do not add an Exhibit draft/published state; every Exhibit is visible and may lack a description (user decision).
- 2026-11-13 — First Instance deploys to Fly.io, CI only, no auto-CD yet (issue #1, ADR 0007); the scaffold's Kamal is not the chosen path.
- 2026-11-13 — Host has no Ruby: run Rails via `docker run ruby:3.4` as host uid with a mounted `GEM_HOME` and an existing `HOME` (else gems vanish / rubocop fails).
- 2026-11-13 — Product source material from the Django prototype lives in `docs/source/cnk_kompas/`; it is input only, Rails decisions go in GLOSSARY/ADRs.
