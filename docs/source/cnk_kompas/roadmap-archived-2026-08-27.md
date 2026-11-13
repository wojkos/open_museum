---
project: "CNK Kompas"
version: 1
status: draft
created: 2026-08-04
updated: 2026-08-24
prd_version: 1
main_goal: speed
top_blocker: time
---

# Roadmap: CNK Kompas

> Derived from `context/foundation/prd.md` (v1) + auto-researched codebase baseline.
> Edit-in-place; archive when superseded.
> Slices below are listed in dependency order. The "At a glance" table is the index.

## Vision recap

Odwiedzający CNK nie mają świadomie przygotowanych przez instytucję ścieżek tematycznych, przez co mogą nie odnaleźć eksponatów odpowiadających ich zainteresowaniom. CNK Kompas ma przenieść personalizację na stronę gościa: zebrać jego preferencje i wskazać pasujące eksponaty bez zmieniania polityki eksploracji przyjętej przez CNK.

## North star

„North star” oznacza tutaj najmniejszy kompletny przepływ, który potwierdza, że główna obietnica produktu działa.

**S-01: Odwiedzający odpowiada na pytania, wybiera tagi i otrzymuje dopasowaną listę eksponatów** — ten przepływ bezpośrednio sprawdza podstawowe kryterium sukcesu i jest umieszczony najwcześniej, jak pozwalają jego warunki wstępne.

## At a glance

| ID | Change ID | Outcome (user can …) | Prerequisites | PRD refs | Status |
|---|---|---|---|---|---|
| F-01 | synthetic-exhibit-catalog | (foundation) minimalny kontrakt danych i syntetyczny katalog eksponatów są dostępne dla pierwszych przepływów | — | FR-003, FR-004, FR-008 | done |
| F-02 | minimal-public-deployment | (foundation) istnieje minimalna ścieżka publicznego uruchomienia i sprawdzenia aplikacji na telefonie poza siecią CNK | — | NFR: lista działa bez sieci CNK | done |
| S-01 | first-matched-exhibit-list | odwiedzający odpowiada na pytania, wybiera tagi i otrzymuje dopasowaną listę eksponatów posortowaną według części wystawy | F-01, F-02 | US-01, FR-001, FR-002, FR-003 | done |
| S-02 | exhibit-detail-and-location | odwiedzający otwiera eksponat i poznaje jego opis oraz lokalizację | S-01 | US-01, FR-004 | done |
| S-03 | trustworthy-ask-more-handoff | odwiedzający przechodzi z eksponatu do zewnętrznego dostawcy AI z przygotowanym kontekstem | S-02 | US-01, FR-005 | done |
| S-03 | trustworthy-ask-more-handoff | odwiedzający przechodzi z eksponatu do zewnętrznego dostawcy AI z przygotowanym kontekstem | S-02 | US-01, FR-005 | done |
| S-04 | sole-operator-exhibit-management | jedyny operator dodaje i edytuje dane wystaw bez obowiązkowego formalnego logowania w MVP | F-01, F-02 | FR-007, FR-008 | done |
| S-05 | bilingual-visitor-flow | odwiedzający przełącza język polski i angielski bez utraty bieżących odpowiedzi i tagów | S-01 | US-01, FR-006 | done |
| S-06 | anonymous-visit-recording | odwiedzający korzysta bez konta, a uzgodnione dane sesji i interakcji są rejestrowane dla CNK | S-01, S-02, S-03 | US-01, FR-011 | done |
| S-07 | visit-restart | odwiedzający zaczyna od nowa (czyści test i odpowiedzi) i sprawdza inne obszary zainteresowań, gdy nie ma już eksponatów do dodania | S-01 | US-01 | done |
| S-08 | visit-more | odwiedzający dodaje 3 kolejne dopasowane eksponaty do bieżącej listy, a przy braku wystarczającej liczby eksponatów zostaje o tym powiadomiony | S-01, S-07 | US-01, FR-001, FR-002 | done |
| S-09 | privacy-page | odwiedzający otwiera stronę `/privacy` z każdego ekranu i czyta w swoim języku (PL/EN), jakie anonimowe dane aplikacja zapisuje | S-06 | US-01, FR-011 | done |

## Streams

Navigation aid — groups items that share a Prerequisites chain. Canonical ordering still lives in the dependency graph below; this table is the proposed reading order across parallel tracks.

| Stream | Theme | Chain | Note |
|---|---|---|---|
| A | Dane eksponatów i obsługa operatora | `F-01` → `S-04` | Syntetyczny katalog usuwa zależność od bieżącego mapowania CNK. |
| B | Przepływ odwiedzającego | `F-02` → `S-01` → (`S-02` → `S-03` → `S-06` / `S-05`) | Łączy się ze strumieniem A w `S-01`; najkrótsza droga do publicznego sprawdzenia dopasowania. |
| C | Rozszerzanie listy odwiedzającego | `S-01` → `S-07` → `S-08` | „Zacznij od nowa" (S-07) jest warunkiem wstępnym dla „Dodaj 3 kolejne" (S-08): gdy brak dodatkowych eksponatów, przepływ wraca do restartu. |
| D | Transparentność i prywatność | `S-06` → `S-09` | Domyka lukę transparentności S-06: rejestrowanie anonimowych danych bez komunikatu w UI. Niezależny od strumienia C — może iść równolegle. |

## Baseline

What's already in place in the codebase as of `2026-08-04` (auto-researched + user-confirmed).
Foundations below assume these are present and do NOT re-scaffold them.

- **Frontend:** absent — brak interfejsu produktu; istnieje tylko trasa panelu admina (`cnk_kompas/urls.py:21`).
- **Backend / API:** partial — zgodnie z `tech-stack.md` wybrano Django; istnieje świeży szkielet bez obsługi funkcji produktu.
- **Data:** partial — ORM i SQLite są skonfigurowane, ale brak modeli domenowych, migracji projektu i danych startowych (`cnk_kompas/settings.py:75-80`).
- **Auth:** absent — zgodnie z `tech-stack.md` uwierzytelnianie jest celowo odroczone w MVP.
- **Deploy / infra:** partial — zgodnie z `tech-stack.md` wybrano Fly i GitHub Actions, ale ścieżka wdrożenia nie jest skonfigurowana.
- **Observability:** absent — brak konfiguracji logowania aplikacyjnego, śledzenia błędów, metryk i telemetrii.

## Foundations

### F-01: Syntetyczny katalog eksponatów

- **Outcome:** (foundation) minimalny kontrakt danych i syntetyczny katalog eksponatów są dostępne dla pierwszych przepływów.
- **Change ID:** synthetic-exhibit-catalog
- **PRD refs:** FR-003, FR-004, FR-008
- **Unlocks:** S-01, S-02, S-04; usuwa zależność pierwszej wersji od mapowania eksponatów na miejscu.
- **Prerequisites:** —
- **Parallel with:** F-02
- **Blockers:** —
- **Unknowns:**
  - Jaki minimalny przekrój części wystawy, tagów i lokalizacji powinien reprezentować syntetyczny katalog? — Owner: team. Block: no.
- **Risk:** Katalog musi wystarczyć do sprawdzenia dopasowania, ale nie może rozrosnąć się w zastępstwo późniejszego mapowania rzeczywistych eksponatów.
- **Status:** done

### F-02: Minimalne publiczne uruchomienie

- **Outcome:** (foundation) istnieje minimalna ścieżka publicznego uruchomienia i sprawdzenia aplikacji na typowym telefonie poza siecią CNK.
- **Change ID:** minimal-public-deployment
- **PRD refs:** NFR: lista działa bez sieci CNK; Success Criteria: przepływ odwiedzającego podczas wizyty
- **Unlocks:** S-01 i S-04 oraz mobilna ścieżka weryfikacji wszystkich kolejnych przepływów odwiedzającego.
- **Prerequisites:** —
- **Parallel with:** F-01
- **Blockers:** —
- **Unknowns:** —
- **Risk:** Przy celu szybkiego uruchomienia wdrożenie musi pozostać minimalnym kanałem weryfikacji, a nie osobnym projektem infrastrukturalnym.
- **Status:** done

## Slices

### S-01: Pierwsza dopasowana lista eksponatów

- **Outcome:** odwiedzający odpowiada na krótkie pytania, wybiera tagi i otrzymuje dopasowaną listę eksponatów posortowaną według części wystawy.
- **Change ID:** first-matched-exhibit-list
- **PRD refs:** US-01, FR-001, FR-002, FR-003
- **Prerequisites:** F-01, F-02
- **Parallel with:** S-04
- **Blockers:** —
- **Unknowns:**
  - Jak odpowiedzi na pytania wpływają na ranking poza prostym dopasowaniem tagów? — Owner: user. Block: no.
- **Risk:** To najwcześniejszy sprawdzian głównej obietnicy; reguła musi dawać zauważalnie spersonalizowany wynik, a nie pełny katalog w innej kolejności.
- **Status:** done

### S-02: Szczegół i lokalizacja eksponatu

- **Outcome:** odwiedzający otwiera pozycję z listy i widzi opis eksponatu oraz piętro lub galerię, gdzie może go znaleźć.
- **Change ID:** exhibit-detail-and-location
- **PRD refs:** US-01, FR-004
- **Prerequisites:** S-01
- **Parallel with:** S-04, S-05
- **Blockers:** —
- **Unknowns:** —
- **Risk:** Szczegół musi przełożyć rekomendację na działanie podczas wizyty bez wchodzenia w odłożoną na później nawigację.
- **Status:** done

### S-03: Wiarygodne przekazanie pytania do AI

- **Outcome:** odwiedzający wybiera „Zapytaj więcej” i trafia do zewnętrznego dostawcy AI z promptem zawierającym kontekst wybranego eksponatu.
- **Change ID:** trustworthy-ask-more-handoff
- **PRD refs:** US-01, FR-005
- **Prerequisites:** S-02
- **Parallel with:** S-04, S-05
- **Blockers:** —
- **Unknowns:**
  - Jak prompt, zweryfikowane notatki i komunikat dla użytkownika mają ograniczać prezentowanie zmyślonych faktów jako wiarygodnych? — Owner: user. Block: no. **Decyzja 2026-08-06:** aplikacja buduje prompt za użytkownika i otwiera `chatgpt.com/?q=<prompt>`. Prompt zawiera: kontekst wizyty (np. „zwiedzam CNK z rodziną"), nazwę i opis eksponatu, wybrane tagi z ankiety, instrukcję odpowiadania rzeczowo z faktami naukowymi.
- **Risk:** Zewnętrzny dostawca przyspiesza uruchomienie, lecz bez uzgodnionego mechanizmu wiarygodności narusza wyraźną barierę jakościową PRD.
- **Status:** done

### S-04: Zarządzanie eksponatami przez jedynego operatora

- **Outcome:** jedyny operator dodaje i edytuje nazwę, lokalizację, tagi, opis, notatki do promptu i opcjonalne zdjęcie bez obowiązkowego formalnego logowania w MVP.
- **Change ID:** sole-operator-exhibit-management
- **PRD refs:** FR-007, FR-008
- **Prerequisites:** F-01, F-02
- **Parallel with:** S-01, S-02, S-03, S-05
- **Blockers:** —
- **Unknowns:**
  - Jak ograniczyć dostęp do funkcji jedynego operatora bez wprowadzania formalnego logowania i bez wystawienia edycji publicznie? — Owner: user. Block: no. **Decyzja 2026-08-06:** hasło operatora przechowywane w zmiennej środowiskowej (env); panel admina dostępny tylko po jego podaniu.
- **Risk:** Formalne uwierzytelnianie jest odłożone, ale publicznie dostępna edycja danych byłaby nieakceptowalna; zakres ochrony wymaga jawnej decyzji.
- **Status:** done

### S-05: Dwujęzyczny przepływ odwiedzającego

- **Outcome:** odwiedzający korzysta z przepływu dopasowania po polsku lub angielsku i przełącza język bez utraty bieżących odpowiedzi oraz tagów.
- **Change ID:** bilingual-visitor-flow
- **PRD refs:** US-01, FR-006
- **Prerequisites:** S-01
- **Parallel with:** S-02, S-03, S-04
- **Blockers:** —
- **Unknowns:** —
- **Risk:** Dwujęzyczność jest konieczna, lecz musi rozszerzyć już działający przepływ zamiast opóźniać pierwszy test reguły dopasowania.
- **Status:** done

### S-06: Rejestrowanie anonimowej wizyty

- **Outcome:** odwiedzający korzysta bez konta, a jego odpowiedzi, tagi, rekomendacje, otwarcia eksponatów, użycia „Zapytaj więcej”, język i identyfikator czasu oraz sesji są rejestrowane zgodnie z uzgodnionymi zasadami.
- **Change ID:** anonymous-visit-recording
- **PRD refs:** US-01, FR-011
- **Prerequisites:** S-01, S-02, S-03
- **Parallel with:** S-04, S-05
- **Blockers:** —
- **Unknowns:**
  - Jaka zgoda jest pokazywana, jak długo dane są przechowywane i czy oraz w jaki sposób CNK je otrzymuje? — Owner: user. Block: no. **Decyzja 2026-08-06:** (1) Brak komunikatu zgody — dane w pełni anonimowe/zagregowane (brak PII, brak identyfikatora użytkownika). (2) Retencja: konfigurowalny parametr środowiskowy (domyślna wartość do ustalenia w implementacji). (3) Dostęp CNK: panel admina z eksportem CSV (rozszerza istniejący panel z S-04).
- **Risk:** Rejestrowanie wizyt daje wartość CNK, ale wdrożenie przed ustaleniem zgody, retencji i odbiorcy danych stworzyłoby ryzyko prywatności.
- **Status:** done

## Backlog Handoff

| Roadmap ID | Change ID | Suggested issue title | Ready for `/10x-plan` | Notes |
|---|---|---|---|---|
| F-01 | synthetic-exhibit-catalog | Przygotuj minimalny syntetyczny katalog eksponatów | yes | Odblokowuje pierwszy przepływ dopasowania. |
| F-02 | minimal-public-deployment | Uruchom minimalną publiczną ścieżkę weryfikacji | yes | Może powstawać równolegle z F-01. |
| S-01 | first-matched-exhibit-list | Dostarcz pierwszą dopasowaną listę eksponatów | no | Najpierw F-01 i F-02. |
| S-02 | exhibit-detail-and-location | Pokaż szczegół i lokalizację eksponatu | no | Najpierw S-01. |
| S-03 | trustworthy-ask-more-handoff | Przekaż wiarygodny kontekst eksponatu do AI | no | Blokuje decyzja o mechanizmie wiarygodności. |
| S-04 | sole-operator-exhibit-management | Udostępnij zarządzanie eksponatami jedynemu operatorowi | no | Blokuje decyzja o ochronie dostępu bez formalnego logowania. |
| S-05 | bilingual-visitor-flow | Dodaj polski i angielski przepływ odwiedzającego | no | Najpierw S-01. |
| S-06 | anonymous-visit-recording | Rejestruj uzgodnione dane anonimowej wizyty | no | Blokują zasady zgody, retencji i przekazania danych CNK. |

## Open Roadmap Questions

1. ~~**Visitor data consent, retention, and CNK as recipient**~~ — ✅ Resolved 2026-08-06. Decyzja: dane w pełni anonimowe (brak komunikatu zgody), retencja jako konfigurowalny parametr, dostęp CNK przez panel admina z eksportem CSV. Block: S-06 odblokowany → `proposed`.
2. ~~**How trustworthy AI is enforced with an external provider**~~ — ✅ Resolved 2026-08-06. Mechanizm: aplikacja buduje prompt (kontekst wizyty + eksponat + tagi) i otwiera `chatgpt.com/?q=<prompt>` z instrukcją odpowiadania rzeczowo z faktami naukowymi. Block: S-06 (nadal zależy od S-03).
3. **Exhibit data collection template and first mapping pass** — Owner: user. Still to prepare/execute on-site at CNK. Block: późniejsze użycie produkcyjne z rzeczywistą ekspozycją; nie blokuje syntetycznego MVP.
4. ~~**Jak chronić funkcje jedynego operatora bez obowiązkowego formalnego logowania w MVP?**~~ — ✅ Resolved 2026-08-06. Decyzja: hasło w zmiennej środowiskowej (env). Block: S-04 odblokowany.

## Parked

- **Rzeczywiste mapowanie eksponatów w CNK** — Why parked: użytkownik odkłada je na później; pierwsza wersja używa syntetycznego katalogu.
- **Zdjęcia eksponatów** — Why parked: FR-009 ma niższy priorytet i nie jest potrzebne do sprawdzenia dopasowania.
- **Uporządkowana trasa piesza** — Why parked: PRD §Non-Goals; MVP rekomenduje pozycje według części wystawy.
- **Nawigacja zakręt po zakręcie wewnątrz budynku** — Why parked: PRD §Non-Goals; wystarcza tekst piętra lub galerii.
</content>
