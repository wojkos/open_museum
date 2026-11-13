# Run: bootstrap Rails app and engineering standards

- **Date:** 2026-11-13
- **Goal:** Create the `open_museum` Rails application; save the Rails "Getting Started" (Store) guide, distilled, as `.ai/docs/engineering-standards.md`.
- **Spec used:** none (scaffold-only task, no feature behavior).

## Plan
1. Ruby/Rails not installed on host (Docker available) ⇒ generate with `ruby:3.4` image as host uid.
2. `rails new open_museum --skip-bundle --skip-git` in `/tmp/gen`, `bundle install` for `Gemfile.lock`, copy into repo root.
3. Add `.gitignore` (skipped by `--skip-git`), write standards doc.

## Decisions
- Rails 8.1.4.1 (guide requires 8.1+), Ruby 3.4 (`.ruby-version` from image), default SQLite/Propshaft/importmap/Solid*.
- App generated in repo root (not a subfolder) so `AGENTS.md`/`.ai/` sit beside the Rails code.
- `.gitignore` written by hand from the Rails template, plus `/.ai/cezar/` (local tooling state).
- Standards doc is a distilled rule set, not a verbatim copy of the guide; the tutorial's `store` app name is replaced by this repo's conventions.

## Verification (inside `ruby:3.4` container)
- `bin/rails db:create db:migrate` — ok
- `bin/rails test` — 0 runs (no tests yet), 0 failures
- `bin/rubocop` — 23 files, no offenses
- `bin/brakeman` — 0 security warnings

## Outcome
App scaffold + standards doc in place; nothing committed (user did not ask).

## Open questions
- Host has no Ruby; run commands via Docker (or install Ruby via mise/rbenv) — user's choice.
- Does "Store" mean the guide's example app should also be built? Assumed no: only used as input for standards.
