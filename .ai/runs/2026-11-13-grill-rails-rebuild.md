# Run: grill Open Museum Rails rebuild
- Goal: grill-with-docs on rebuilding the visitor app on Rails; output GLOSSARY.md + ADRs. No code, no /to-spec.
- Input: docs/source/cnk_kompas/*, AGENTS.md, .ai/lessons.md, docs/agents/*.
- Plan: ask frontier round (Q1-Q8), record answers.
- Decisions: user confirmed all recommended answers Q1-Q8 (Q2 reason: maintainer is a former Rails developer refreshing the skill; full replacement). Matching = score>0, score desc, Gallery order, slug, as a pure Ruby object.
- Outcome: GLOSSARY.md and ADRs 0001-0006 written.
- Open questions: consent/retention/data sharing per Instance; Gallery-grouped vs flat display in the spec; open-source licence; photo storage (assumed Active Storage later).

## Round 2 (Q9-Q21, in Polish)
User asked to expand the questions; then told the run to proceed autonomously, so recommended answers were adopted:
- Intake questions fixed in code (i18n); Instance configures Interests, Galleries, Exhibits and text only.
- Matcher weights are code constants with unit tests (ranking spread, 3-level order, non-empty per single Interest); optional Exhibit attributes: viewing time, family friendly.
- Match list displayed grouped by Gallery (Gallery order), sorted by score then slug within a group.
- Catalog: Gallery, Exhibit, Interest, Exhibit-Interest join; text location only; photos via Active Storage.
- Own simple CRUD under /operator (no admin gem), language tabs.
- Propshaft + plain CSS tokens (DESIGN.md Bauhaus as default theme), Hotwire via importmap, no Tailwind/Node; a11y rules mandatory.
- Visit identified by URL token (ADR 0009); events recorded: Intake, Match list shown, Exhibit opened, Ask more (link or copy), language, time.
- Visit export CSV (dashboard later), min group size 5, retention per Instance via Solid Queue job; no API.
- SQLite single machine + Kamal (ADR 0007); MIT public core (ADR 0008); seeds-only fictional catalog; English docs/code, Polish only in locales; v1 non-goals listed in GLOSSARY.
- Open: consent/legal wording, backup tool choice, exact retention default.

## Round 2 answers from the user
Q9-Q12, Q14 yes. Corrections: Q13 use a ready-made admin gem (ADR 0004 updated); Q15 option (a) signed session cookie (ADR 0009 rewritten, Visit link term removed); Q16 CSV export now, filterable dashboard later (glossary: Visit export); Q17 keep SQLite but leave deployment/CD open, issue #1 created (ADR 0007 rewritten, Kamal/VPS dropped). Q18-Q21 not answered: recommended answers kept.

## Round 3 (Q22-Q35, Polish) - recommended answers adopted (user: proceed autonomously)
- Q22-Q25 confirmed: MIT public core, seeds only, English docs, v1 non-goals.
- Q26 config split (ADR 0010); Q27 Exhibits have published flag, matcher ignores drafts; Q28 explicit no-match state + browse-all (logged as Visit event); Q29 resume Visit < 12h (ADR 0009); Q30 Administrate provisional, spike first (ADR 0004); Q31 Mobility (ADR 0011).
- Q32 Rails 8 rate_limit on Visit/event creation, noindex on Visit screens, server-side input validation, no CAPTCHA.
- Q33 editable privacy notice, no consent button; "do not store my Visit" outside v1 (Instance question).
- Q34 Minitest, Capybara system test for Intake->Ask more, RuboCop, Brakeman, bundler-audit on GitHub Actions CI (no deploy; see #1). Rails run through Docker (see lessons).
- Q35 axe-core in system tests for key screens, local fonts/scripts, no external CDNs; response-time budget set in spec after a measurement.

## Round 3 user answers (Q22-Q29)
Q22-Q25 yes; Q26 option (c). Corrections: Q27 no draft/published state - every Exhibit is visible, an Exhibit without a description is valid (name still required; missing translations fall back to the default language); Q28 no-match shows an explicit notice that personalised matching failed and automatically lists all Exhibits (no extra click; the event is still recorded on the Visit); Q29 Visit resume window is 48 hours (ADR 0009). Q30-Q35: recommended answers stand.

## Round 4
User chose RSpec over Minitest (Q34 revised; ADR 0012). Round 4 questions asked on RSpec toolchain; scaffold currently has test/ and CI running `rails test`.
