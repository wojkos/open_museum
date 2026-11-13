# Visits are anonymous and store only the product-defined fields

A Visit is keyed by a random id with no Visitor account. It stores Intake answers/Interests, the Match list, Exhibits opened, Ask more clicks, language and timestamps, for the museum's benefit. No IP address, user agent or fingerprinting is collected. Consent copy, retention and how a museum receives the data are Instance-level policy and are deliberately not decided in the core (open question carried from the prototype).

Switching language must not lose in-progress answers, so answers persist on the Visit.

Default retention is 12 months (configurable per Instance, ADR 0010); a daily job deletes older Visits with their events.

Amended: before Intake the Visitor sees an editable notice with a consent checkbox. Without consent the Visitor still gets Matches, but the Visit and its events are not stored (answers live only in the signed session for the running flow). Legal wording and basis remain Instance policy. A consent banner for cookies is still not needed because only the strictly necessary session cookie is used.

Superseded detail: consent is mandatory, not optional. A Visitor who does not tick the checkbox cannot proceed to Intake, so every stored Visit has consent and no consent-less code path exists. The consent text is an editable Instance notice with a neutral default; its legal wording is the Instance's responsibility.
