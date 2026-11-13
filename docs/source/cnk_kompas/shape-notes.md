---
project: "CNK Kompas"
context_type: greenfield
created: 2026-08-04
updated: 2026-08-04
product_type: web-app
target_scale:
  users: medium
  qps: low
  data_volume: small
timeline_budget:
  mvp_weeks: 3
  hard_deadline: null
  after_hours_only: true
checkpoint:
  current_phase: 8
  phases_completed: [1, 2, 3, 4, 5, 6, 7]
  gray_areas_resolved:
    - topic: context_type
      decision: greenfield
    - topic: pain_category
      decision: missing capability — thematic path institution will not provide
    - topic: insight
      decision: visitor-side tool fills demand without changing CNK policy
    - topic: primary_persona_scope
      decision: individual visitors (families, adults, teens) — one odwiedzający model
    - topic: primary_cost_v1
      decision: interest miss ("nie znalazłem nic dla siebie") — matching → route; not visit memory
    - topic: access_model
      decision: Visitor no account; session visit data stored for CNK; Admin sole-operator without mandatory login in MVP
    - topic: mvp_scope
      decision: questions + tags → matching exhibit list + item detail + AI provider link; navigation after MVP; ~3 weeks after-hours
    - topic: i18n
      decision: Polish and English are must-have
    - topic: socrates_fr007
      decision: formal admin login deferred — sole operator for MVP
    - topic: socrates_fr010
      decision: dropped remember-last-tags on device; superseded by must-have server-side visit data for CNK
    - topic: product_type
      decision: web-app (native mobile later if ever)
    - topic: target_scale
      decision: medium (dozens to a hundred); same matching rule at 100x unless revisited
    - topic: non_goals
      decision: no ordered trasa; no indoor nav; no in-app AI chat
    - topic: visitor_data
      decision: must-have store answers/tags, recommendations, opens/Ask more, language, timestamp/session id for CNK
  frs_drafted: 10
  quality_check_status: accepted
---

# Seed idea (verbatim capture)

Koncept aplikacji – personalizowane trasy w CNK

Cel aplikacji: Aplikacja proponuje użytkownikowi trasę zwiedzania Centrum Nauki Kopernik dopasowaną do jego zainteresowań (np. "samochody" → trasa do eksponatów związanych z motoryzacją/mechaniką). Dodatkowo aplikacja umożliwia zadawanie pytań do AI chatu, żeby pogłębić temat wykraczający poza krótkie opisy przy eksponatach.

Kontekst / problem: CNK nie prowadzi obecnie ścieżek tematycznych i świadomie nie chce ich wprowadzać. Użytkownicy mimo to dopytują o takie trasy – jest tu realna, niezaspokojona potrzeba. Opisy przy eksponatach są krótkie – brakuje głębszej wiedzy na miejscu. Instalacje w CNK rzadko się zmieniają, więc jednorazowe zmapowanie eksponatów ma sens.

Przewaga: żona pracuje w CNK → swobodny, powtarzalny dostęp do budynku; osobiste mapowanie eksponatów.

Ryzyka: zależność od jakości mapy; filozofia instytucji (eksploracja vs ścieżki); wiarygodność AI chatu.

Kluczowe funkcje: wybór tematu; generowanie trasy z lokalizacją; AI chat przy eksponacie.

Dane: nazwa, piętro/galeria, kategorie, opis własny, notatki/materiały do AI — do zebrania w CNK.

Finaliści nazwy: Pytaj Kopernika; CNK Kompas. (pozostałe rozważane wymienione w seed).

Otwarte decyzje: nazwa; zebranie danych; forma pierwszego efektu; kontrola treści AI.

## Vision & Problem Statement

Odwiedzający CNK brakuje ścieżki tematycznej, której instytucja świadomie nie daje. W trakcie wizyty nie filtrują ekspozycji pod swoje zainteresowania i wychodzą z poczuciem, że nic ich nie trafiło — zmarnowana lub rozmyta wizyta.

Insight: narzędzie po stronie odwiedzającego może zaspokoić popyt na trasy tematyczne bez zmiany polityki CNK (eksploracja zostaje po stronie instytucji; personalizacja — po stronie gościa).

Scale note: at ~100× visitors (thousands), the matching rule stays the same unless revisited — answers/tags → recommended items sorted by exhibition part.

## User & Persona

**Primary:** Odwiedzający CNK — osoba (dorosły, nastolatek, członek rodziny) w trakcie wizyty, która chce zobaczyć coś zgodnego ze swoimi zainteresowaniami, a nie tylko błądzić po galeriach. Moment sięgnięcia po produkt: gdy stają przed bogatą ekspozycją bez oficjalnej ścieżki i nie wiedzą, od czego zacząć „pod siebie”.

## Access Control

Two roles:

- **Visitor** — no account; opens the app and completes preference flow without sign-up. Session visit data is still stored (for CNK value) without requiring a visitor login.
- **Admin** — sole operator for MVP; can manage exhibitions without mandatory account login. Formal admin login deferred (Socrates on FR-007).

No member/guest tiers. Keep the model thin: anonymous visitor + sole operator admin (formal admin login deferred for MVP).

## Success Criteria

### Primary
- Visitor completes questions + tag selection and receives a list of exhibits matching their interests, sorted by exhibition part.
- Opening an exhibit shows description and where to find it (floor/gallery); “Ask more” opens an AI provider chat with a prompt about that exhibit.
- Visit session data valuable to CNK is stored: answers/tags, recommended items, opens/Ask more, language, timestamp/session id.
- No turn-by-turn navigation in MVP (explicitly after MVP).

### Secondary
- Exhibit photos on item detail.
- Polish/English (also must-have via FR-006).
- Admin can add/edit exhibitions in-app.

### Guardrails
- AI ask/answer about an exhibit must be trustworthy — no unchecked invented scientific “facts” presented as reliable.

## Functional Requirements

### Visitor preference & matching
- FR-001: Visitor can answer a short set of preference questions. Priority: must-have
  > Socrates: Counter-argument considered: tags alone / arbitrary scoring. Resolution: kept as written.
- FR-002: Visitor can select interest tags (e.g. engineering). Priority: must-have
  > Socrates: Counter-argument considered: free-text vs taxonomy burden. Resolution: kept as written.
- FR-003: Visitor can see a list of exhibits matching their answers/tags, sorted by exhibition part. Priority: must-have
  > Socrates: Counter-argument considered: static theme paths / bad matching trust risk. Resolution: kept as written.

### Exhibit detail & deepening
- FR-004: Visitor can open an exhibit and see description and where to find it (floor/gallery). Priority: must-have
  > Socrates: Counter-argument considered: name-only / lost without map. Resolution: kept as written.
- FR-005: Visitor can open “Ask more” and land in an AI provider chat with a prompt about that exhibit. Priority: must-have
  > Socrates: Counter-argument considered: external link weakens control vs trustworthy-AI guardrail. Resolution: kept as written (MVP shape); trustworthiness remains a guardrail to resolve in content/prompt design.
- FR-006: Visitor can use the app in Polish or English. Priority: must-have
  > Socrates: Counter-argument considered: Polish-only MVP / auto-translate. Resolution: kept as written.

### Admin
- FR-007: Admin (sole operator) can access exhibition management without a mandatory account login in MVP. Priority: must-have
  > Socrates: Counter-argument considered: “Login is premature if only you are admin.” Resolution: revised — formal login deferred; sole-operator access for MVP.
- FR-008: Admin can add/edit exhibition data (name, location, tags/categories, description, notes for AI prompt, optional photo). Priority: must-have
  > Socrates: Counter-argument considered: offline seed / CMS scope risk. Resolution: kept as written.

### Visit data (for CNK)
- FR-011: System can store visitor session data for CNK without a visitor account — answers and selected tags, recommended items, items opened and Ask-more actions, language, and timestamp/session id. Priority: must-have
  > Socrates: Counter-argument considered: storing visit data creates privacy/consent obligations and may require CNK agreement as data recipient; shipping storage without a consent/legal path can hurt the product. Resolution: kept as must-have for CNK value; consent, retention, and CNK data-sharing terms left as Open Questions.

### Nice-to-have
- FR-009: Visitor can see a photo on exhibit detail. Priority: nice-to-have
  > Socrates: Counter-argument considered: drop for rights/time vs promote to must-have. Resolution: kept as nice-to-have.

### Dropped after Socrates
- ~~FR-010: App can remember last selected tags.~~ Priority: was nice-to-have
  > Socrates: Counter-argument considered: contradicts one-shot visitor. Resolution: dropped as on-device “remember tags”; visit analytics storage covered by FR-011 instead.

## User Stories

### US-01: Visitor gets a matched exhibit list and can ask more via AI provider

- **Given** a visitor opens the app with no account
- **When** they answer preference questions, select interest tags, and view the results
- **Then** they see a list of matching exhibits sorted by exhibition part; opening one shows description and floor/gallery location; “Ask more” opens an AI provider chat with a prompt about that exhibit; the session’s answers/tags, recommendations, opens/Ask more, language, and timestamp/session id are stored for CNK

#### Acceptance Criteria
- Matching list reflects selected tags/answers (not a generic full catalog dump)
- Location is shown as floor/gallery text (no turn-by-turn navigation)
- UI language can be Polish or English
- “Ask more” uses an external AI provider with a prompt about the selected exhibit
- Visit session fields above are recorded without requiring visitor login

## Business Logic

Given the visitor’s answers at the start, the app decides which items are worth seeing and returns a list sorted by exhibition part.

Inputs are the answers collected at the beginning of the session. Output is a recommended list of items worth seeing, ordered by exhibition part (not an ordered walking trasa). The visitor encounters this decision immediately after intake, as the main results screen before opening item detail or “Ask more.”

Ordered trasa generation is explicitly after MVP; MVP is a matched items catalog with recommendation, not path planning.

## Non-Functional Requirements

- Matched item list appears within a few seconds on a typical phone; no access to the CNK network is required.
- Switching between Polish and English does not lose the visitor’s current answers/tags.
- “Ask more” opens the AI provider with exhibit context already present in the prompt.
- AI answers about an exhibit must not invent unchecked scientific facts presented as reliable.

## Non-Goals

- Ordered walking trasa / path planning — MVP recommends items sorted by exhibition part; trasa comes later.
- Indoor turn-by-turn navigation — floor/gallery text only.
- In-app AI chat or custom model hosting — external AI provider link + prompt only.

## Open Questions

1. **Visitor data consent, retention, and CNK as recipient** — Owner: user. What consent copy is shown, how long data is kept, and whether/how CNK receives it. Block: yes for production sharing with CNK.
2. **How trustworthy AI is enforced with an external provider** — Owner: user. Prompt grounding, disclaimers, verified notes per exhibit. Block: partial (guardrail exists; mechanism TBD downstream).
3. **Exhibit data collection template and first mapping pass** — Owner: user. Still to prepare/execute on-site at CNK.

## Forward: tech-stack

- Builder has Python experience; has not built a native mobile app; chose web app for MVP.
- Native Android (if ever) is after web MVP — not a PRD commitment.

## Forward: technical-roadmap

- After MVP: ordered trasa generation; indoor navigation; possibly native mobile shell.

## Quality cross-check

Status: **accepted** (2026-08-04). All soft-gate elements present for greenfield:

- Access Control: present
- Business Logic: present (one-sentence rule)
- Project artifacts: present
- Timeline-cost ack: present (`mvp_weeks: 3`)
- Non-Goals: present
- Preserved behavior: n/a (greenfield)

Open Questions (consent/CNK data sharing, AI trustworthiness mechanism, exhibit mapping) remain for `/10x-prd` to mirror — not treated as cross-check gaps.
