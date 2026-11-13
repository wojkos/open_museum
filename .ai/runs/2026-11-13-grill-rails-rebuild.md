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
- Operator dashboard + CSV, min group size 5, retention per Instance via Solid Queue job; no API.
- SQLite single machine + Kamal (ADR 0007); MIT public core (ADR 0008); seeds-only fictional catalog; English docs/code, Polish only in locales; v1 non-goals listed in GLOSSARY.
- Open: consent/legal wording, backup tool choice, exact retention default.
