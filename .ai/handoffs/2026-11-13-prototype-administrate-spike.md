# Handoff: prototype administrate-spike

## Goal
Answer the Round 7 prerequisite (ADR 0004/0011): does Administrate work for the Operator panel with Mobility translated fields (language tabs) and Active Storage photos on Rails 8 in this repo?

## Decisions (with why)
- **GO: Administrate + Mobility** (human confirmed). The spike passes 5 integration tests: login gate, PL/EN tabs, create/edit per locale, photo upload/show/delete, validation, sort, search.
- ADR 0011 (Mobility) unchanged: awkwardness is limited to small glue code.
- ADR 0004 updated: Administrate confirmed, gaps listed. Fallbacks (Avo, hand-built Exhibits form) not needed.
- Gaps to carry into the spec as tasks:
  1. Add `administrate-field-active_storage` (1.0.6); Administrate 1.0 has no built-in field.
  2. Enable Mobility `locale_accessors` (languages from Instance config, ADR 0010) so `name_pl`/`name_en` exist.
  3. Custom `TranslatedField` + partials in `app/views/fields/translated_field/` (partial dir must match the field class name).
  4. Translated sort/search needs a controller concern using `i18n` scope; Administrate sort params are namespaced (`exhibit[order]`); search matches current locale only.
  5. N+1 on the index (9 queries for 3 Exhibits): add `.includes`.
  6. Custom code to maintain alongside Administrate.

## Artifacts
- Branch `prototype/administrate-spike` (throwaway app in `prototype/administrate-spike/`; key files `app/fields/translated_field.rb`, `app/controllers/concerns/translated_admin.rb`, `test/spike_test.rb`, `config/initializers/mobility.rb`).
- `docs/adr/0004-single-operator-authentication.md` (updated), `.ai/runs/2026-11-13-prototype-administrate-spike.md`, `.ai/lessons.md`.

## Open questions
- The language-tab JS (inline toggle) was not exercised in a real browser; the Selenium system spec in the build should cover it.
- Accessibility of the tabs (axe, ADR: key screens) not checked.

## Next session
`/to-spec`: fold the gaps above into the spec; the real implementation uses Rails 8 auth with the single Operator from env/credentials (spike seeded a User row).

## Status
settled
