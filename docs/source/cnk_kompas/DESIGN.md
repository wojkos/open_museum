# Open Museum — Design System

**Product**: Open Museum (Personalized Exhibit Matching)
**Type**: Internal/unofficial Django application  
**Design Direction**: Bauhaus-inspired interface system for practical exhibit discovery under real-world museum conditions.

---

## Brand Overview

Open Museum is a **personalized exhibit-matching web application** for visitors deciding what to explore next. The interface should feel like a practical, modern wayfinding tool: bold, structured, and immediate.

This system is based on a **clear, structured visual language**:

- **Function first**: every visual decision must support orientation or action.
- **Strong geometry**: sharp edges, clear borders, and block-based hierarchy.
- **High-legibility contrast**: dark text, bright action colors, and uncluttered surfaces.
- **Mobile reliability**: one-handed use, large tap targets, and predictable flow.

---

## Color System

### Core Palette

| Token | Hex | Usage |
| ----- | --- | ----- |
| **Background** | #EEF3F5 | Global page background |
| **Surface** | #FFFFFF | Cards, forms, and content blocks |
| **Text** | #17252D | Primary text and icon color |
| **Muted** | #52636C | Secondary metadata and hints |
| **Primary** | #176B87 | Primary CTA and high-priority action |
| **Accent** | #D66B3D | Active state and selection emphasis |
| **Border** | #B7C6CC | Structural outlines and separators |

### Semantic Use

- **Primary action**: use `Primary` fill with `Surface` text.
- **Selection/active**: use `Accent` as a strong differentiator.
- **Structure**: rely on `Border` for component hierarchy and grouping.
- **Neutral zones**: use `Background` + `Surface` layering for depth.

### Color Accessibility

- Maintain WCAG AA contrast at minimum for all text.
- Never rely on color alone to indicate meaning.
- Pair color states with text labels, control state, or iconography.

---

## Typography System

### Font Stack

| Element | Font Family | Weight | Notes |
| ------- | ----------- | ------ | ----- |
| **Headings** | Source Sans 3, Verdana, sans-serif | 800 | Compact, assertive hierarchy |
| **Body** | Source Sans 3, Verdana, sans-serif | 400-500 | Readable during fast scanning |
| **Labels/Buttons** | Source Sans 3, Verdana, sans-serif | 500-800 | Strong action affordance |

### Type Scale

- **xs**: 12px
- **sm**: 14px
- **base**: 16px
- **lg**: 20px
- **xl**: 24px
- **2xl**: 32px
- **3xl**: 48px

### Typography Rules

- Body copy should default to `16px` with `1.4` line-height.
- Use weight, not decorative effects, for hierarchy.
- Keep letter spacing at `0` unless explicitly needed for labels.

---

## Layout & Spacing

### Spacing Scale

Use a strict 4px rhythm:

- 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

### Layout Rules

- **Max width**: 1160px application frame.
- **Gutters**: 20px mobile, 40px desktop.
- **Reading width**: content rails should stay around 720px when possible.
- **Header**: stable and compact; no animated marketing chrome.

### Shape Language

- Prefer square corners (`0px`) and strong outlines.
- Avoid soft card shadows as primary separation.
- Build separation with blocks, borders, and spacing.

---

## Component Guidelines

### Choice Tiles (Intake)

- Full-width, high-contrast selectable rows.
- Visible form control (checkbox/radio) must remain present.
- Selected state must be visible even without color perception.

### Match Rows (Results)

- Structured list items, not marketing cards.
- Name is primary; location/meta is secondary.
- Use border accents to aid scan speed, not to encode meaning alone.

### Detail View

- Lead with exhibit name and factual summary.
- Keep image factual, not decorative.
- Keep AI handoff as a separate, clearly labeled action.

### Buttons and Links

- Primary buttons: min height 48px, strong color fill, high contrast text.
- Links: always underlined; hover changes underline thickness.
- Focus states: 3px outline plus visible offset/ring.

---

## Motion & Interaction

- Keep transitions short (around 160-220ms) and purposeful.
- Do not use parallax, autoplay, or decorative page transitions.
- Respect `prefers-reduced-motion` with near-instant transitions.

---

## Responsive Rules

| Device | Width | Layout |
| ------ | ----- | ------ |
| **Mobile** | < 640px | Single-column flow |
| **Tablet** | 640-1023px | Adaptive layout, optional side enhancements |
| **Desktop** | >= 1024px | Expanded layout with optional orientation rail |

Rules:

- Preserve reading order across all breakpoints.
- Maintain >=44px touch targets for all primary controls.
- Do not introduce desktop-only information that disappears without fallback.

---

## Accessibility

- Semantic HTML and logical heading order are mandatory.
- Every control needs an accessible name.
- Keep keyboard focus visible at all times.
- Announce dynamic content updates where needed (HTMX/state changes).
- Keep skip links present on primary visitor pages.

---

## Implementation Rules (Mandatory)

- **All styling must be in CSS files in static assets.**
- **Do not use inline styles in HTML** (`style="..."`) and do not add page-local `<style>` blocks in templates.
- Use shared tokens in `:root` and component classes; avoid one-off per-template styling.
- When introducing new UI, extend existing stylesheet structure first.

Current primary stylesheet locations:

- `exhibits/static/exhibits/visitor.css`
- `open_museum/static/open_museum/operator.css`

---

## Design Tokens (Canonical)

```css
:root {
  /* Colors */
  --color-bg: #eef3f5;
  --color-surface: #ffffff;
  --color-text: #17252d;
  --color-muted: #52636c;
  --color-primary: #176b87;
  --color-accent: #d66b3d;
  --color-border: #b7c6cc;

  /* Typography */
  --font-display: "Source Sans 3", Verdana, sans-serif;
  --font-sans: "Source Sans 3", Verdana, sans-serif;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 800;
  --line-height-base: 1.4;

  /* Type scale */
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 20px;
  --font-size-xl: 24px;
  --font-size-2xl: 32px;
  --font-size-3xl: 48px;

  /* Spacing */
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Radius */
  --radius-none: 0;
  --radius-sm: 0;
  --radius-md: 0;

  /* Focus */
  --focus-ring: 0 0 0 3px var(--color-surface), 0 0 0 6px var(--color-border);
}
```

---

## Originality Boundary

The system may be inspired by modernist principles, but it must remain an original, configurable museum interface. Do not replicate external layouts, brand marks, or page compositions from other products or institutions.

---

## References

- Product spec: `context/foundation/prd.md`
- Roadmap: `context/foundation/roadmap.md`
- Tech stack: `context/foundation/tech-stack.md`
- Active implementation styles: `exhibits/static/exhibits/visitor.css`, `open_museum/static/open_museum/operator.css`

---

*Design system for Open Museum, updated 2026-08-27.*
