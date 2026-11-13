# Spec: Open Museum Rails rebuild

- Status: draft, settled by grilling rounds 1–8 (`.ai/runs/2026-11-13-grill-rails-rebuild.md`); one gate open (Administrate spike)
- Terms: `GLOSSARY.md`. Decisions: `docs/adr/0001`–`0012`. Design: `DESIGN.md`. Source material: `docs/source/cnk_kompas/`.
- Next: `/to-tickets` on this file.

## Problem Statement

A museum Visitor facing a large exhibition with no thematic path does not know where to start and leaves feeling nothing fitted them. The museum has no insight into what Visitors look for. The Django prototype proved the idea but lacks an open, reusable core: its admin was open or password-shared, content was not museum-agnostic, and it was not built for a maintainer who wants to keep it long-term.

## Solution

Rebuild Open Museum on Rails 8 as a museum-agnostic core (ADR 0001, 0002). A Visitor ticks Consent, answers a short Intake (Interests, who they are with, time, kids under 6 where relevant) and gets a Match list grouped by Gallery. Opening an Exhibit shows its description and location, and **Ask more** hands a grounded prompt to an external AI provider. One Operator maintains the catalog and Instance content in a panel and downloads a Visit export for the museum. The first Instance (CNK) runs on Fly.io.

## User Stories

Visitor
1. As a Visitor, I want to read what the app stores and tick one checkbox before I start, so that I know what I agree to.
2. As a Visitor, I cannot continue without ticking Consent, so that every stored Visit has consent.
3. As a Visitor, I want to choose Polish or English at any point, so that I can use the app in my language.
4. As a Visitor, I want switching language not to lose my answers, so that I do not start over.
5. As a Visitor, I want to pick several Interests, so that the list reflects what I care about.
6. As a Visitor, I want to say who I am with (alone, couple, family, group), so that suggestions fit my company.
7. As a Visitor with a family, I want to say whether there are children under 6, so that I am shown suitable Galleries.
8. As a Visitor, I want to say how much time I have (short, medium, long), so that the list suits my visit.
9. As a Visitor, I want a Match list grouped by Gallery in visiting order with floor labels, so that I can plan where to walk.
10. As a Visitor, I want the most relevant Exhibits first within a Gallery, so that I see the best ones early.
11. As a Visitor, I want a clear notice and the full Exhibit list when nothing matches, with no extra click, so that I am never at a dead end.
12. As a Visitor, I want to open an Exhibit and see its description, photo and location, so that I can find it.
13. As a Visitor, I want an Exhibit without a description to still open with its name and location, so that incomplete data is not a broken page.
14. As a Visitor, I want missing translations to show the default language, so that nothing appears blank.
15. As a Visitor, I want **Ask more** to open an AI provider with a prompt about the Exhibit, so that I can learn more.
16. As a Visitor, I want a **Copy prompt** button, so that I can paste it if the link does not prefill.
17. As a Visitor, I want to resume my Visit within 48 hours, so that a reload or return does not lose my list.
18. As a Visitor, I want **Start over** on the start screen, so that I can begin a fresh Visit.
19. As a Visitor, I want the app usable one-handed on a phone with large targets, so that I can use it while walking.
20. As a Visitor using assistive technology, I want semantic structure, visible focus, skip links and AA contrast, so that I can use the app.
21. As a Visitor, I want the app to load without third-party scripts or fonts, so that nothing external tracks me.

Operator
22. As the Operator, I want to sign in with credentials set in the environment, so that the panel is not open on a public URL.
23. As the Operator, I want recovery to be changing credentials and restarting, so that there is no email reset to maintain.
24. As the Operator, I want to create, edit and delete Galleries with floor label, order and optional Audience, so that the building is modelled.
25. As the Operator, I want to restrict a Gallery to kids under 6 as an Audience, so that it appears only for such Visits.
26. As the Operator, I want to manage Interests with per-language names, so that Visitors pick topics in their language.
27. As the Operator, I want to manage Exhibits with per-language name and description, Gallery, text location, optional viewing time, family-friendly flag and Interests, so that matching has data.
28. As the Operator, I want to upload an Exhibit photo (JPEG/PNG/WebP up to 5 MB) with alt text, so that Visitors see the object.
29. As the Operator, I want an AI note per Exhibit, so that Ask more is grounded in verified facts.
30. As the Operator, I want to edit museum name, tagline, privacy notice text, Ask more prompt template and provider link, so that I adapt the Instance without a deploy.
31. As the Operator, I want the prompt template to require the AI note placeholder, so that I cannot ground nothing by accident.
32. As the Operator, I want to enter CNK data manually from my sheet, so that no import tool is needed.
33. As the Operator, I want to download a Visit export CSV, so that I can share it with the museum.
34. As the Operator, I want the export raw and anonymous with times rounded to the hour, so that no Visitor is identifiable.
35. As the Operator, I want Visits deleted after the retention period, so that data is not kept forever.

Maintainer
36. As a maintainer, I want the Matcher as a pure Ruby object with unit tests, so that I can tune scoring safely.
37. As a maintainer, I want CI (RSpec, RuboCop, Brakeman, bundler-audit), so that regressions are caught.
38. As a maintainer, I want a fictional seeded catalog, so that the public core ships no real museum data.
39. As a maintainer, I want to add a language through configuration without a migration, so that Instances can grow.

## Implementation Decisions

**Stack.** Rails 8.1, SQLite (Solid Queue, Cache, Cable), Propshaft, importmap, Hotwire, plain CSS tokens (`DESIGN.md`), no Tailwind or Node. Fly.io with a volume for SQLite and uploads; CI only, manual deploys; auto-CD and backups stay in issue #1 (ADR 0007). The scaffold's Kamal files and the Minitest `test/` directory are removed in the skeleton ticket. Rails commands run via Docker (see lessons).

**Domain modules.**
- *Matcher* (pure Ruby, `spec/domain`, no Rails): inputs are a Visit's Intake answers plus Exhibit data as plain values; output is Matches. An Exhibit matches only with score above zero; order is score descending, then Gallery order, then slug. Interest overlap dominates; viewing time (time budget) and family-friendly (companion = family) add small bonus constants. Exact numbers are fixed by tests that assert: ranking spread, the three-level order, and a non-empty list for each single Interest. Audience Galleries are excluded unless the Visit has kids under 6, both from Matches and the no-match list.
- *Match list presenter*: groups Matches by Gallery in Gallery order, then score, then slug.
- *No-match state*: when no Exhibit scores above zero, show the notice and the full Exhibit list grouped by Gallery, unranked; record a no-match event on the Visit.
- *Prompt builder*: renders the Operator template with museum, Exhibit, Gallery, description and AI note, in the UI language; the AI note placeholder is required (ADR 0005). Provider link is one template with a placeholder for the encoded prompt; default ChatGPT.

**Data.** Models: Gallery, Exhibit, Interest, Exhibit–Interest join, Visit, Visit event, Instance settings (single row). Text location is free text. Translated fields (Exhibit name/description, Gallery name, Interest name) use Mobility (ADR 0011); missing translation falls back to the default locale. An Exhibit needs a name but no description; there is no draft state. Photos use Active Storage with image_processing variants.

**Intake.** Fixed in code (i18n), not editable: Interests (multi), companion (alone, couple, family, group), time budget (short, medium, long), kids under 6 (asked only for family). Instance Interests are Operator data; the fictional seed has about six.

**Visit and Consent.** Consent checkbox before Intake is mandatory; the server refuses Intake without it. The Visit id lives in the signed session cookie; a Visit younger than 48 hours resumes, otherwise a new one starts; Start over always offered (ADR 0003, 0009). Events recorded: Intake submitted, Match list shown, no-match shown, Exhibit opened, Ask more (link or copy), language switched, each with a timestamp. No IP, user agent or fingerprint stored. Rate limits (Rails 8 `rate_limit`) start near 30 Visit creations and 120 events per minute per IP, tuned after measurement. Visit screens are `noindex`; input validated server side; no CAPTCHA.

**Operator.** One account from env or credentials, using Rails' built-in authentication with the password-reset flow removed (ADR 0004). Panel under `/operator` built with Administrate (provisional), language tabs for translated fields, Active Storage upload. Instance configuration split per ADR 0010: languages, default language and retention in Rails config; museum name, tagline, privacy notice, prompt template and provider link in the database.

**Visit export.** CSV, one line per Visit, raw and anonymous: no Visit id, time rounded to the hour, Intake answers, Matches count, opened Exhibits, Ask more count, language. No aggregated mode, no minimum group size. A filterable dashboard is later.

**Retention.** Instance-configured, default 12 months; a daily Solid Queue job deletes older Visits with their events.

**Photos and rights.** JPEG/PNG/WebP up to 5 MB; rights are the Operator's responsibility; alt text required.

**Accessibility and performance.** `DESIGN.md` rules are mandatory. No response-time number is set: measure after the first slice, then add a budget.

**Repository.** MIT public core, Instance data private (ADR 0008). English docs and code; Polish only in locales. A fictional seeded catalog only.

**Vertical slices (order, from Q45).**
1. Skeleton: Rails app, RSpec toolchain, CI, design tokens and layout, Instance settings, seeds.
2. Visitor flow: Consent, Intake, Matcher, Match list, no-match, Exhibit detail, Ask more.
3. Operator panel: authentication, catalog and settings CRUD, photos. **Gated on the Administrate spike** (see Open items).
4. Visit events and Visit export.
5. Retention job.
Slices 2 and 3 can start before 3's gate if the seeds are enough for the Visitor flow; each slice ends in a working, tested flow.

## Default copy (PL/EN)

Translation keys live in `config/locales/{en,pl}.yml`; the default locale is `en`. Starting copy (Operator-editable parts marked *):

| Key | EN | PL |
|---|---|---|
| consent notice* | To give you recommendations, Open Museum saves your answers and the exhibits you open during this visit. We store no name, email or IP address. The museum receives this data only in anonymous form to improve the visit, and it is deleted after 12 months. You can't use the app without agreeing. | Aby podpowiadać Ci eksponaty, Open Museum zapisuje Twoje odpowiedzi i otwierane eksponaty podczas tej wizyty. Nie zapisujemy imienia, adresu e-mail ani adresu IP. Muzeum otrzymuje te dane wyłącznie w formie anonimowej, aby ulepszać zwiedzanie; są usuwane po 12 miesiącach. Bez zgody nie można korzystać z aplikacji. |
| consent checkbox | I agree to my visit being stored. | Zgadzam się na zapisanie mojej wizyty. |
| start button | Start | Zaczynamy |
| start over | Start over | Zacznij od nowa |
| intake: interests | What are you interested in? Pick as many as you like. | Co Cię interesuje? Wybierz dowolnie wiele. |
| intake: companion | Who are you visiting with? (Alone / As a couple / With family / With a group) | Z kim zwiedzasz? (Sam(a) / We dwoje / Z rodziną / W grupie) |
| intake: time | How much time do you have? (Short / Medium / Long) | Ile masz czasu? (Mało / Średnio / Dużo) |
| intake: kids | Are there children under 6 with you? | Czy z Tobą są dzieci poniżej 6 lat? |
| match list title | Your matches | Twoja lista dopasowań |
| no-match notice | We couldn't make a personalised selection. Here is everything, by gallery. | Nie udało się dopasować eksponatów. Oto wszystkie, według galerii. |
| exhibit location | Where to find it | Gdzie to znaleźć |
| ask more | Ask more | Zapytaj więcej |
| copy prompt | Copy prompt | Skopiuj pytanie |
| copy confirmation | Prompt copied | Skopiowano |
| ask more caveat | An external AI answers; check important facts. | Odpowiada zewnętrzna AI; ważne fakty sprawdź. |
| missing description | No description yet. | Brak opisu. |
| language switch | Polski / English | Polski / English |
| default prompt template* | You are a guide at {museum}. Answer about the exhibit "{exhibit}" in gallery "{gallery}". Description: {description}. Verified facts: {ai_note}. Rely only on these facts, and say you don't know when they do not cover the question. Answer in English. | Jesteś przewodnikiem w {museum}. Odpowiadaj o eksponacie „{exhibit}” w galerii „{gallery}”. Opis: {description}. Sprawdzone fakty: {ai_note}. Opieraj się wyłącznie na tych faktach, a gdy nie wystarczają do odpowiedzi, powiedz, że nie wiesz. Odpowiadaj po polsku. |

Legal wording is the Instance's responsibility (ADR 0003). Polish uses *Eksponat*, *Galeria*, *Dopasowanie*; never *Ekspozycja* (see lessons).

## Testing Decisions

- Good tests assert external behaviour (what a Visitor or Operator sees and gets), not implementation details.
- **Three seams:**
  1. A system spec of the Visitor flow (Consent → Intake → Match list → Exhibit → Ask more), run with Selenium; includes axe-core-rspec for the key screens (fails CI on AA violations).
  2. `spec/domain` for the Matcher (and prompt builder), no Rails loaded, test-first (AGENTS.md).
  3. Request specs for the Operator panel (authentication, catalog CRUD, settings) and the Visit export (anonymity, hour rounding, retention deletion).
- Tooling: RSpec, FactoryBot, shoulda-matchers, rubocop-rspec, i18n-tasks (missing PL/EN keys fail CI), SimpleCov informational; no VCR or WebMock. CI on GitHub Actions: RSpec, RuboCop, Brakeman, bundler-audit.
- Prior art: none in the repo yet; the Django prototype's `docs/source/cnk_kompas/test-plan.md` lists scenarios to port.

## Out of Scope

Route or turn-by-turn navigation; in-app AI chat; native app; offline/PWA; Visitor accounts; editable Intake questions; Visit dashboard (CSV only); CSV catalog import; multi-operator roles; automatic translation; auto-CD and backups (issue #1); horizontal scaling; a "do not store my Visit" path (Consent is mandatory).

## Further Notes

**Open items**
- **Administrate spike** (sibling task `84afb07c`, handoff expected at `.ai/handoffs/2026-11-13-prototype-administrate-spike.md`) had not reported when this spec was written. Slice 3 is gated on it. If Administrate with Mobility language tabs and Active Storage is no-go, fall back per ADR 0004 (Avo free tier, or a hand-built form for Exhibits only) and update ADR 0004/0011.
- Response-time budget: after the first slice.
- Deployment automation and backups: issue #1.
- Exact Matcher constants: fixed by tests in slice 2.
- CNK catalog data: Operator enters it by hand from a sheet.
