# Open Museum — Design System (Rails)

Visual and interaction rules for the Visitor app and the Operator panel. Product terms follow `GLOSSARY.md`. Inherited from the Django prototype (`docs/source/cnk_kompas/DESIGN.md`); this file is the source of truth for the Rails build. It is the default theme, and an Instance may override the tokens in one file.

## Principles

- Function first: every visual decision supports orientation or action.
- Bauhaus-inspired: sharp edges, clear borders, block hierarchy, no decorative chrome.
- Mobile first, one-handed: single column, large tap targets, predictable flow.
- High contrast, WCAG 2.2 AA minimum; never rely on colour alone (pair with text, control state or icon).
- Original interface: do not copy layouts or marks from other institutions.

## Tokens (canonical)

Plain CSS custom properties in `:root`, served by Propshaft. No Tailwind, no Node.

```css
:root {
  --color-bg: #eef3f5;        --color-surface: #ffffff;
  --color-text: #17252d;      --color-muted: #52636c;
  --color-primary: #176b87;   --color-accent: #d66b3d;
  --color-border: #b7c6cc;
  --font-sans: "Source Sans 3", Verdana, sans-serif;
  --font-weight-normal: 400;  --font-weight-medium: 500;  --font-weight-bold: 800;
  --line-height-base: 1.4;
  --font-size-xs: 12px; --font-size-sm: 14px; --font-size-base: 16px;
  --font-size-lg: 20px; --font-size-xl: 24px; --font-size-2xl: 32px; --font-size-3xl: 48px;
  --space-2xs: 4px; --space-xs: 8px; --space-sm: 12px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px; --space-3xl: 64px;
  --radius: 0;
  --focus-ring: 0 0 0 3px var(--color-surface), 0 0 0 6px var(--color-text);
}
```

Colour roles: Primary fills for the main action (surface-coloured text); Accent for selection and active state; Border for structure. Check contrast of every token pair in tests; `--color-muted` on `--color-bg` must stay at 4.5:1 or better. The prototype's focus ring used the Border colour and is too faint, so the focus ring uses Text colour.

## Typography

Source Sans 3 served locally (no external CDN); Verdana fallback. Body 16px at line-height 1.4; hierarchy by weight and size, not effects. Headings weight 800.

## Layout

4px rhythm using the spacing tokens. Application frame max 1160px; gutters 20px mobile, 40px desktop; reading rail about 720px. Square corners, outlines instead of shadows. Breakpoints: below 640px single column; 640–1023px adaptive; 1024px and up expanded, with the reading order preserved.

## Components

- **Choice tile (Intake):** full-width selectable row with a visible checkbox or radio; the selected state is visible without colour (check mark plus border thickness). Minimum height 48px.
- **Consent checkbox:** same tile style, label links to the full notice; the Intake start button is disabled until ticked and the server rejects submissions without it.
- **Match row:** list item, Exhibit name primary, location secondary. Rows are grouped under a Gallery heading (Gallery order) with its floor label. Border accents aid scanning but never carry meaning alone.
- **No-match notice:** a bordered notice block with text ("no personalised selection could be made"), followed by the full list grouped by Gallery.
- **Exhibit detail:** name and factual description first; photo is factual with alt text; location block (Gallery, floor, text location). **Ask more** is a separate, clearly labelled block with the provider link and a **Copy prompt** button.
- **Buttons and links:** primary buttons at least 48px high with high-contrast fill; links always underlined, hover thickens the underline; focus shows the 3px ring plus offset.
- **Language switch:** always in the header; switching keeps the Visit's answers.
- **Operator panel:** functional, same tokens, denser; language tabs per translated field.

## Motion

Transitions 160–220ms and purposeful; no parallax, autoplay or decorative transitions; `prefers-reduced-motion` reduces to near-instant. Turbo page navigation only.

## Accessibility (mandatory)

- Semantic HTML, logical heading order, one `h1` per page, `lang` attribute follows the UI language.
- Every control has an accessible name; touch targets 44px or larger.
- Visible keyboard focus everywhere; skip link on every Visitor page.
- Dynamic updates (Turbo, copy confirmation) are announced via `aria-live`.
- axe-core runs in system specs for the key screens and fails CI on AA violations.

## Implementation rules

- All styling lives in stylesheet files under `app/assets/stylesheets`; no inline `style=` attributes and no page-local `<style>` blocks. Use tokens and shared component classes; extend the existing stylesheet before adding one-off CSS.
- Scripts and fonts are served locally; no third-party CDNs.
- Visitor and Operator surfaces use separate stylesheets (`visitor.css`, `operator.css`) that share `tokens.css`.
