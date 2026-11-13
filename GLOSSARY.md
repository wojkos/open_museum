# Open Museum

A web app that helps a museum Visitor decide what to see: the Visitor states interests and context, and the app recommends Exhibits, grouped by where they are in the building. Open Museum is museum-agnostic; a specific museum is an Instance.

## Language

### People

**Visitor**:
An anonymous person using the app during a museum visit. Has no account. In Polish UI: *Odwiedzający*.
_Avoid_: user, guest, customer

**Operator**:
The single trusted person who maintains an Instance's catalog and configuration. In Polish UI: *Operator*.
_Avoid_: admin, editor, staff

### Catalog

**Instance**:
One deployment of Open Museum configured for one museum (name, languages, theme, catalog). In Polish UI: *Instancja*.
_Avoid_: tenant, site, fork

**Exhibit**:
One thing a Visitor can go and see, with a description and a location. In Polish UI: *Eksponat*.
_Avoid_: item, eksponat (outside Polish UI copy), installation

**Gallery**:
A named area of the museum that holds Exhibits, with a floor label and a place in the visiting order. In Polish UI: *Galeria*.
_Avoid_: exhibition part, exhibition, zone, section

**Audience**:
An optional restriction on a Gallery to a kind of Visitor (for example families with children under 6); a Gallery with an Audience yields no Matches for other Visits.
_Avoid_: age group, kids zone

**Interest**:
A topic a Visitor can pick (e.g. "engineering"); Exhibits are associated with Interests. In Polish UI: *Zainteresowanie*.
_Avoid_: tag, category, theme

**AI note**:
Operator-written, verified facts about an Exhibit that ground the Ask more prompt. In Polish UI: *Notatka AI*.
_Avoid_: AI notes, prompt notes

### The visit

**Intake**:
The short question flow at the start of a Visit that collects the Visitor's Interests and context (e.g. who they are with, how much time). In Polish UI: *Pytania startowe*.
_Avoid_: onboarding, quiz, wizard

**Visit**:
One anonymous session from Intake onward, recorded for the Instance's museum. In Polish UI: *Wizyta*.
_Avoid_: session (as a domain term), user session

**Match**:
An Exhibit recommended to a Visitor for a Visit because it fits their Intake answers. In Polish UI: *Dopasowanie*.
_Avoid_: result, recommendation (as a noun for a single Exhibit), hit

**Match list**:
The Matches for a Visit, ordered by relevance and then Gallery order. In Polish UI: *Lista dopasowań*.
_Avoid_: route, trasa, itinerary

**No-match state**:
What a Visitor sees when no Exhibit scores above zero: an explicit notice that no personalised selection could be made, followed automatically by the full list of Exhibits grouped by Gallery without ranking. In Polish UI: *brak dopasowań*.
_Avoid_: empty state, error

**Consent**:
The Visitor's explicit tick, required before Intake, allowing their Visit to be stored. Without it the Visitor cannot use the app.
_Avoid_: opt-in, cookie banner

**Ask more**:
The handoff from an Exhibit to an external AI provider with a prompt about that Exhibit. In Polish UI: *Zapytaj więcej*.
_Avoid_: AI chat, chatbot

### Reporting

**Visit export**:
A CSV the Operator downloads to share Visit data with the museum, raw and anonymous: one line per Visit, with no Visit id and a rounded time. A filterable dashboard is a later addition. In Polish UI: *Eksport wizyt*.
_Avoid_: report, analytics

## Out of scope by definition

- A **route** (ordered walking path) and turn-by-turn indoor navigation are not part of the product yet; a Match list is not a route.
- In-app AI chat, native app, offline/PWA, Visitor accounts, editable Intake questions a Visit dashboard (CSV export only at first) and CSV catalog import are outside the first version.
- The legal wording of the consent text and the legal basis for sharing Visit data with a museum are Instance policy, not decided here.
