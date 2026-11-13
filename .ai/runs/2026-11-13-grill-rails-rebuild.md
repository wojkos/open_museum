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

## Round 4 answers (Q36-Q45) - recommended answers adopted (user: proceed autonomously)
Q36 FactoryBot; Q37 spec/domain without Rails, request + system specs; Q38 Cuprite; Q39 axe-core-rspec fails CI on AA; Q40 shoulda-matchers, rubocop-rspec, i18n-tasks, SimpleCov informational, no VCR/WebMock; Q41 domain test-first, rule added to AGENTS.md; Q42 retention 12 months; Q43 Visit export two modes (aggregated >=5, raw anonymous); Q44 editable prompt template with required AI note placeholder, UI language; Q45 first release as thin vertical slice; order: skeleton+RSpec+CI+seeds, Visitor flow, Operator panel, Visit events+export, retention (tickets later via /to-tickets after /to-spec).
Remaining open: consent/legal wording, admin gem spike, response-time budget, deployment (#1).

## Round 5 gaps (user: proceed autonomously) - defaults chosen, refine in /to-spec
- Intake: Interests (multi), companion (alone/couple/family/group), time budget (short/medium/long), kids under 6 (shown only for family). Starter Interests are Instance data; the fictional seed uses about 6.
- Matcher weights: Interest overlap dominates; bonuses are small constants; exact numbers fixed in spec by tests (spread, 3-level order, non-empty per single Interest).
- Audience (new glossary term): Gallery optional audience `kids under 6`; excluded from Matches unless the Visit says kids under 6; excluded from the no-match full list too unless kids under 6. Set by the Operator.
- Operator account: credentials from env/credentials, no email password reset (remove the Rails auth reset flow); recovery = change credentials and restart. 
- Photos: JPEG/PNG/WebP up to 5 MB, resized variants via image_processing; rights are the Operator's responsibility.
- rate_limit: starting values about 30 Visit creations and 120 events per minute per IP, tuned after measuring.
- AI providers: ChatGPT link by default; others by editing the provider link template.
- Naming: product/repo stays Open Museum; museum name and tagline are Instance data. DESIGN.md for Rails and default PL/EN copy are written at /to-spec.
- Lessons added to .ai/lessons.md for user corrections.

## Round 6 (answered via ask-user card)
Confirmed: Administrate, Mobility, retention 12 months, four Intake questions, hidden Audience Galleries, no email reset, single AI link + copy.
Changed: export is raw-anonymous only (no aggregated mode, no minimum group size setting); system specs use Selenium (not Cuprite); consent is an explicit checkbox before Intake (ADR 0003 amended, glossary term Consent) - without consent the Visit is not stored but Matches still work.

## Round 7 (ask-user card)
- Consent is mandatory: no access without ticking the checkbox (supersedes the optional-consent variant); legal text is an Instance concern with a neutral default.
- First Instance on Fly.io; CI only for now, manual deploys; auto-CD and backups stay open in #1 (ADR 0007).
- Response-time budget: measure after the first slice, no number in the spec.
- CNK data: collected in a sheet, entered manually through the Administrate panel; no CSV import.
- Prerequisite before /to-spec: spike Administrate with Mobility language tabs and Active Storage (not yet done).

## Round 8 (session 8ec65b60, grill+spec, answered via card)
- Consent default text approved as drafted (PL/EN, with the 12-month figure, neutral; Instance edits it).
- Test seams: three (Visitor-flow system spec, domain Matcher spec, Operator and export request specs).
- Visit export time is rounded to the hour.
- Spike: wait for the Administrate spike handoff before writing the spec. At 2026-11-13 the sibling (84afb07c) had written no handoff and no findings.
- Human then told the session to proceed autonomously; spec written to `.ai/specs/2026-11-13-rails-rebuild.md` with slice 3 gated on the spike. DESIGN.md written at repo root. Handoff in `.ai/handoffs/`. Spec is not published to the issue tracker (task order scopes it to a file).
