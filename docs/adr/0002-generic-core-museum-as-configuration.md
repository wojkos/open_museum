# Open Museum is a museum-agnostic core; a museum is an Instance

The prototype was CNK-only and later planned a split into a generic core plus a CNK fork. Here we start generic: museum name, tagline, theme tokens, languages, AI prompt museum name and catalog are configuration or data, never literals in code. CNK is just the first Instance. This avoids a future package-rename and fork-merge churn.

Consequence: no museum-specific strings, galleries or gating rules in code. The "kids under 6" gating of a kids-only gallery is a generic Gallery audience attribute.
