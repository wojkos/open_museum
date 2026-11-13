# Open Museum

A web app that helps a museum Visitor decide what to see: the Visitor states interests and context, and the app recommends Exhibits, grouped by where they are in the building. Open Museum is museum-agnostic; a specific museum is an Instance.

## Language

### People

**Visitor**:
An anonymous person using the app during a museum visit. Has no account.
_Avoid_: user, guest, customer

**Operator**:
The single trusted person who maintains an Instance's catalog and configuration.
_Avoid_: admin, editor, staff

### Catalog

**Instance**:
One deployment of Open Museum configured for one museum (name, languages, theme, catalog).
_Avoid_: tenant, site, fork

**Exhibit**:
One thing a Visitor can go and see, with a description and a location.
_Avoid_: item, eksponat (outside Polish UI copy), installation

**Gallery**:
A named area of the museum that holds Exhibits, with a floor label and a place in the visiting order.
_Avoid_: exhibition part, exhibition, zone, section

**Interest**:
A topic a Visitor can pick (e.g. "engineering"); Exhibits are associated with Interests.
_Avoid_: tag, category, theme

**AI note**:
Operator-written, verified facts about an Exhibit that ground the Ask more prompt.
_Avoid_: AI notes, prompt notes

### The visit

**Intake**:
The short question flow at the start of a Visit that collects the Visitor's Interests and context (e.g. who they are with, how much time).
_Avoid_: onboarding, quiz, wizard

**Visit**:
One anonymous session from Intake onward, recorded for the Instance's museum.
_Avoid_: session (as a domain term), user session

**Match**:
An Exhibit recommended to a Visitor for a Visit because it fits their Intake answers.
_Avoid_: result, recommendation (as a noun for a single Exhibit), hit

**Match list**:
The Matches for a Visit, ordered by relevance and then Gallery order.
_Avoid_: route, trasa, itinerary

**Ask more**:
The handoff from an Exhibit to an external AI provider with a prompt about that Exhibit.
_Avoid_: AI chat, chatbot

### Reporting

**Visit export**:
A CSV of anonymised Visit data the Operator downloads to share with the museum. A filterable dashboard is a later addition.
_Avoid_: report, analytics

## Out of scope by definition

- A **route** (ordered walking path) and turn-by-turn indoor navigation are not part of the product yet; a Match list is not a route.
- In-app AI chat, native app, offline/PWA, Visitor accounts, editable Intake questions a Visit dashboard (CSV export only at first) and CSV catalog import are outside the first version.
- Consent wording, retention period, and how a museum receives Visit data are Instance policy, not decided here.
