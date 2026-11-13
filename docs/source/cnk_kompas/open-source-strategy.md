# Open-Museum / CNK Kompas Fork Strategy

## Decision

Move from a single CNK-only codebase to a two-repo model:

- **`open-museum`** — public, museum-agnostic core (this codebase, stripped of CNK content). The open-source project.
- **`cnk-kompas`** — a fork/downstream of `open-museum` that carries only Centrum Nauki Kopernik's branding, seed content, and deploy config, and periodically merges upstream changes.

This repo (`CNKkompas`) is currently both at once. The work below splits them.

## Why (from codebase audit, 2026-08-27)

The app is already largely museum-agnostic (~2.5–3k LOC):

- **Generic, no changes needed:** `exhibits/models.py` (taxonomy + anonymous `Visit`/`VisitClickEvent`), `exhibits/matching.py` (tag-scoring engine), `exhibits/intake.py` (HTMX multi-step forms), `exhibits/visits.py` (anonymous analytics lifecycle), operator password-gate pattern (`open_museum/admin_site.py`).
- **CNK-specific, must be extracted:**
  - Branding strings: `"CNK Kompas"` in the former project templates and admin module.
  - Design tokens: Bauhaus palette + Archivo font locked in `context/foundation/DESIGN.md`.
  - Content: `exhibits/seed_data.py` (real CNK exhibits, Polish names, "bzzz" kids-gallery concept, physical locations).
  - AI prompt: hardcoded `"Centrum Nauki Kopernik"` in `exhibits/ask_more.py`.
  - Defaults: `LANGUAGE_CODE = 'pl'`; the package is now `open_museum` and deployment values are generic templates.

## Target architecture

### `open-museum` (core, upstream)

- Package/app names genericized: the Django project package is `open_museum`; the `exhibits` app remains unchanged.
- All branding pulled from settings, not hardcoded:
  - `MUSEUM_NAME`, `MUSEUM_S
  - Theme values (colors, font stack) exposed as CSS custom properties sourced from a settings-driven theme file (e.g. `theme/default.css` vars), not hardcoded in `DESIGN.md`-derived CSS. `DESIGN.md` itself becomes a **template/example** design system doc, not CNK's locked palette.
- `exhibits/seed_data.py` content replaced with a small, clearly-fictional example catalog (2–3 sample exHORT_NAME` env-backed settings, used in admin titles, operator login, base template, AI prompt builder.hibits) demonstrating the data shape — not real museum content.
- `LANGUAGE_CODE` defaults to a neutral choice (e.g. `en`), with PL kept as a supported second language via existing `locale/` infra.
- Deploy config (`fly.toml`, `Dockerfile`, CI workflow) becomes a template others copy and customize; no CNK-specific values.
- README rewritten for `open-museum` as a generic OSS project: what it does, how to configure a new museum instance (env vars, seed data, theme, translations), license.
- License file added (OSS license — user to choose, e.g. MIT/Apache-2.0).

### `cnk-kompas` (fork, downstream)

- Git fork of `open-museum`. Overrides only:
  - `MUSEUM_NAME`/theme env vars or a small settings override module.
  - `exhibits/seed_data.py` (or equivalent pluggable seed source) with real CNK catalog.
  - `context/foundation/DESIGN.md` restored as CNK's actual locked Bauhaus palette.
  - AI prompt museum name.
  - Fly app name/deploy secrets.
- Everything else (models, matching, intake, admin, visit analytics, tests) tracks upstream via regular `git fetch upstream && git merge`.

## Genericization mechanism (to keep merges cheap)

To minimize future merge conflicts between `open-museum` and `cnk-kompas`, CNK-specific values should live in **as few, most-isolated files as possible**:

1. Settings-driven branding: one block of env-backed settings (`MUSEUM_NAME`, `MUSEUM_TAGLINE`, etc.) in `settings.py`, referenced everywhere via `{{ settings.MUSEUM_NAME }}` / `django.conf.settings`, not duplicated as literal strings in templates.
2. Seed data as a swappable module: keep `exhibits/seed_data.py` as the single file a fork replaces wholesale; don't scatter exhibit content elsewhere.
3. Theme as CSS custom properties in one file (e.g. `static/theme/tokens.css`), so a fork only overrides that file, not scattered class rules.
4. `DESIGN.md` split conceptually: generic "how to define a theme" guidance stays in `open-museum` docs; the actual CNK values move to a fork-only doc.

This is deliberately **not** a plugin/package system (too much overhead for a solo-maintained project) — it's "isolate the seams so a `git merge` from upstream rarely touches the same lines as a fork's overrides."

## Migration sequence (for a later implementation pass)

1. In this repo: genericize branding, theme tokens, AI prompt, default language, seed data — while it's still one repo and easy to test both "CNK mode" and "generic mode" side by side.
2. Verify the app runs correctly with only generic content (no CNK strings anywhere outside the fork-seam files).
3. Rename repo/package to `open-museum`, push as the new public OSS repo (new GitHub repo, license, README).
4. Create `cnk-kompas` as a fork of `open-museum`; apply CNK's overrides (restore real seed data, branding, DESIGN.md, Fly config) on top.
5. Point Fly deploy / GitHub Actions for `cnk-kompas` at the fork; `open-museum` gets its own (optional) demo deploy or none.
6. Update this repo's `AGENTS.md` and `context/foundation/*` once the split is real (this doc gets superseded/archived per foundation doc conventions).

## Open questions (resolve before implementation)

- Exact new package name for `open_museum` (affects imports across the codebase — sizable mechanical rename).
- OSS license choice.
- Whether `exhibits` app is renamed too, or kept (lower churn if kept).
- Where the two repos live (same GitHub org/user, visibility, who owns `open-museum` long-term).
- Default language for the generic core (`en` recommended vs keeping `pl`).
