---
name: Kinetic Glass AI
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#45dfa4'
  on-secondary: '#003825'
  secondary-container: '#00bd85'
  on-secondary-container: '#00452e'
  tertiary: '#ffb873'
  on-tertiary: '#4b2800'
  tertiary-container: '#e89337'
  on-tertiary-container: '#5b3200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#68fcbf'
  secondary-fixed-dim: '#45dfa4'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005137'
  tertiary-fixed: '#ffdcbf'
  tertiary-fixed-dim: '#ffb873'
  on-tertiary-fixed: '#2d1600'
  on-tertiary-fixed-variant: '#6a3b00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.03em
  display-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 0.75rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system targets an intelligent, high-velocity civic tech landscape: an AI-driven youth policy analysis engine. It bridges governmental institutional weight with next-generation algorithmic precision. The personality is authoritative yet radically modern, predictive, and luminous.

The interface evokes focus, high-dimensional clarity, and frictionless navigation through deep policy datasets. The design direction unites **Dark Mode Precision** with refined **Glassmorphism**:
- Deep atmospheric dark canvases that minimize visual strain during complex data exploration.
- Translucent, frosted glass layers that establish depth hierarchy without feeling heavy or skeuomorphic.
- High-vibrancy electric accents that serve strictly as cognitive focal points—guiding analysts toward high-priority policy signals, AI confidence scores, and real-time trends.

## Colors

The palette operates on calibrated contrast ratios compliant with WCAG AAA for text content against dark canvases.

### Primary Canvas & Layering
- **Base Canvas:** Deep space navy (`#0b1120`) grounds the application viewport.
- **Surface Elevation 1 (Default Card Base):** Charcoal slate (`#0f172a`) mixed with opacity values between `40%` and `70%`.
- **Surface Elevation 2 (Raised Modals & Flyouts):** Midnight obsidian (`#1e293b`) at `80%` opacity for focused contextual states.

### Accents & Intelligence Indicators
- **Primary Cyber Cyan (`#06b6d4`):** Primary interactions, system state focal points, live predictive AI telemetry, and hyperlinked metadata.
- **Secondary Kinetic Emerald (`#34d399`):** Verification tags, positive metric delta indicators, AI confidence indices over 90%, and active execution states.

### Neutral & Alpha Borders
- **Border Ambient:** Pure white at 10% opacity (`rgba(255, 255, 255, 0.10)`) for structural delineation.
- **Border Kinetic:** Neon Cyan at 20% opacity (`rgba(6, 182, 212, 0.20)`) for active, focused, or high-scoring elements.
- **Text Primary:** `#f8fafc` (Slate 50) for maximum clarity and scan speed.
- **Text Secondary:** `#94a3b8` (Slate 400) for metadata, labels, and secondary context.
- **Text Muted:** `#64748b` (Slate 500) for disabled states and auxiliary hints.

## Typography

The typographic hierarchy utilizes a tripartite strategy:
1. **Headlines (`Plus Jakarta Sans`):** Modern, geometric, and forward-leaning. High-weight display headers lend optimistic punch to policy impact projections and product summaries.
2. **Body (`Inter`):** Systematic, highly neutral, and legibility-optimized across variable density screens. Handles long-form legislation text, policy summaries, and multi-paragraph telemetry.
3. **Labels & Data Points (`JetBrains Mono`):** Fixed-width engineering clarity for model versions, percentage deltas, timestamp metadata, and AI pipeline statuses.

### Text Contrast Discipline
All headlines utilize crisp `#f8fafc` text. Data values paired with labels must prioritize the metric in primary white or neon accent colors, keeping structural descriptors in muted tones (`#94a3b8`).

## Layout & Spacing

The system runs on a strict **8-point spatial rhythm** anchored to a 12-column adaptive fluid grid.

### Breakpoints & Fluid Grid Behavior
- **Desktop (>= 1280px):** 12-column grid, `margin: 2rem` (32px), `gutter: 1.5rem` (24px). Maximum content containment width is `1440px`.
- **Tablet (768px - 1279px):** 8-column grid, `margin: 1.5rem` (24px), `gutter: 1rem` (16px).
- **Mobile (< 768px):** 4-column grid, `margin: 1rem` (16px), `gutter: 0.75rem` (12px). Side-by-side policy cards collapse cleanly into single-column vertical stacks.

### Rhythm & Density
Inner component padding conforms strictly to the `space-*` scale:
- Tight metadata clusters (chips, status toggles) use `space-xs` and `space-sm`.
- Form inputs, list rows, and interactive buttons use `space-md`.
- Content cards and AI reasoning breakdowns use `space-lg` to ensure comfortable breathing room around frosted boundaries.

## Elevation & Depth

This system departs from traditional drop shadows in favor of **Translucent Frosted Layers** and **Photon Glows**. 

### Glassmorphism Specifications
1. **Primary Frosted Surface (Tier 1):**
   - Background: `rgba(15, 23, 42, 0.65)`
   - Backdrop Filter: `blur(16px) saturate(180%)`
   - Border: `1px solid rgba(255, 255, 255, 0.08)`
2. **Elevated Frosted Surface (Tier 2 - Overlays, Modals, Drawers):**
   - Background: `rgba(30, 41, 59, 0.75)`
   - Backdrop Filter: `blur(24px) saturate(200%)`
   - Border: `1px solid rgba(6, 182, 212, 0.25)`
   - Soft Ambient Shadow: `0 20px 40px -15px rgba(0, 0, 0, 0.6)`

### Luminous Accent Lighting
Interactive elements and high-relevance intelligence nodes discard hard shadows in favor of localized neon glows:
- **Cyan Signal Glow:** `box-shadow: 0 0 20px -2px rgba(6, 182, 212, 0.35)`
- **Emerald Signal Glow:** `box-shadow: 0 0 20px -2px rgba(52, 211, 153, 0.35)`

Avoid combining heavy dark drop shadows with glass surfaces; depth is conveyed through refraction blur and subtle border luminosity.

## Shapes

The design system establishes a cohesive roundedness profile (`level 2` / 0.5rem base radius):
- Standard control elements (buttons, inputs, status tags) feature `0.5rem` (8px) corners to preserve functional precision.
- Structural surface panels, data cards, and dialogue containers use `rounded-lg` (`1rem` / 16px) to frame glass blurs cleanly without clipping internal content.
- Hero modules and persistent modal sheets employ `rounded-xl` (`1.5rem` / 24px).
- Status dots, avatar enclosures, and inline metric pills use pill structures (`rounded-full`).

## Components

### Buttons
- **Primary Action:** Solid glowing fill. Background `bg-cyan-500` (`#06b6d4`), text color deep charcoal (`#080e1a`) with `Plus Jakarta Sans` font weight 600. Subtle photon aura (`box-shadow: 0 0 16px rgba(6, 182, 212, 0.4)`).
- **Secondary (Glass) Action:** Frosted surface `rgba(255, 255, 255, 0.04)`, backdrop-blur-md, border `1px solid rgba(255, 255, 255, 0.12)`, text `#f8fafc`. Hover triggers border transition to `rgba(6, 182, 212, 0.5)` and surface tint.
- **Ghost Action:** Transparent background, text `#94a3b8`, hover state brings text `#06b6d4` with zero canvas displacement.

### Glass Cards
- Foundation of all intelligence streams. Backdrop blur `16px`, background `rgba(15, 23, 42, 0.6)`.
- Default stroke: `1px solid rgba(255, 255, 255, 0.08)`.
- Focus / Highlight stroke: `1px solid rgba(6, 182, 212, 0.3)`.
- Optional top accent: hairline gradient border running from `rgba(6, 182, 212, 0.6)` to `transparent`.

### Chips & Policy Badges
- Compact height (`24px` - `28px`). Text set in `JetBrains Mono` at `label-sm`.
- AI verified status: Emerald background at `12%` opacity (`rgba(52, 211, 153, 0.12)`), text `#34d399`, border `1px solid rgba(52, 211, 153, 0.3)`.
- Metric categorization tag: Slate surface (`rgba(255, 255, 255, 0.05)`), border `1px solid rgba(255, 255, 255, 0.1)`, text `#94a3b8`.

### Input Fields & Query Consoles
- Inputs feature sunken translucent styling: background `rgba(11, 17, 32, 0.8)`, border `1px solid rgba(255, 255, 255, 0.12)`.
- Focus ring: zero native browser outline; dynamic border transition to `#06b6d4` coupled with a subtle cyan ambient aura (`0 0 0 3px rgba(6, 182, 212, 0.15)`).
- Placeholder text in `#64748b`. Monospace font option for AI prompt parameters.

### Checkboxes & Radio Buttons
- Square (`checkbox`) and circular (`radio`) elements with `rgba(15, 23, 42, 0.8)` fill and `1px solid rgba(255, 255, 255, 0.2)`.
- Selected state: background `#06b6d4` with deep charcoal tick indicator and faint outer cyan aura.

### Lists & Data Feed Rows
- Borderless table items separated by single-pixel hairline dividers (`rgba(255, 255, 255, 0.06)`).
- Row hover produces subtle glass luminance shift: background smoothly shifts to `rgba(255, 255, 255, 0.03)`.

### Intelligence Specific: Confidence Meter
- Linear or radial telemetry bar with track `rgba(255, 255, 255, 0.08)` and active fill utilizing an energetic gradient from `#06b6d4` to `#34d399`. Accompanied by fixed-width numeric score formatted in `JetBrains Mono`.