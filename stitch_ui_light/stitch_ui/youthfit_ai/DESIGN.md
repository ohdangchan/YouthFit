---
name: YouthFit AI
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006c4a'
  on-secondary: '#ffffff'
  secondary-container: '#82f5c1'
  on-secondary-container: '#00714e'
  tertiary: '#006242'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d55'
  on-tertiary-container: '#bdffdb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#85f8c4'
  secondary-fixed-dim: '#68dba9'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005137'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 3rem
    fontWeight: '700'
    lineHeight: 3.75rem
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: 2.5rem
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.5rem
    fontWeight: '700'
    lineHeight: 2rem
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.375rem
    fontWeight: '600'
    lineHeight: 1.875rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.625rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
    letterSpacing: -0.01em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
    letterSpacing: -0.005em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.375rem
    letterSpacing: 0em
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.025em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes an institutional yet approachable digital identity tailored to young Korean adults (ages 19–34) navigating national and regional welfare policies, housing subsidies, and employment stipends. The emotional response aims for immediate clarity, fiscal optimism, and algorithmic transparency—stripping away bureaucratic friction in favor of proactive, actionable diagnosis.

The style operates as a **Clean Modern / Fintech-Grade Civic Service**:
- **Clarity over ornament:** Structured information architecture, prominent outcome metrics, and low-cognitive-load layouts.
- **Tone:** Crisp, transparent, validating, and reliable.
- **Visual demeanor:** Precision-engineered micro-surfaces, subtle hairline borders, and targeted color accents indicating monetary grants, qualification scores, and required actions.

## Colors

The palette leverages high-trust civic tech standards paired with modern fintech vibrancy:

- **Primary Electric Blue (`#2563EB`)**: Applied to primary CTAs, active diagnostic states, navigation highlights, and verified algorithmic indicators. It communicates procedural legitimacy and technological accuracy.
- **Secondary Emerald (`#059669`) & Tertiary Light Emerald (`#10B981`)**: Dedicated exclusively to positive states—direct cash payouts, accepted eligibility, matched subsidies, and completion badges.
- **Neutral Slate Family**:
  - Background Canvas: `#F8FAFC` (Slate-50), offering a soft, paper-like surface that avoids stark pure white glare.
  - Surface Containers: Pure White `#FFFFFF` for content cards and modular tiles.
  - Borders & Dividers: Hairline `#E2E8F0` (Slate-200) for sharp boundary containment.
  - Text: `#0F172A` (Slate-900) for headlines, `#334155` (Slate-700) for body, and `#64748B` (Slate-500) for tertiary labels and metadata.
- **State Semantics**: Warning and notice badges utilize `#F59E0B` (Amber-500) with `#FEF3C7` (Amber-50) backgrounds, while disqualifications use `#EF4444` (Rose-500).

## Typography

The type system prioritizes balanced vertical rhythm and high legibility across multilingual environments. In implementation, the primary font maps directly to **Pretendard** or system sans-serif for Korean characters (Hangul), paired harmoniously with **Plus Jakarta Sans** for Latin numerals, monetary symbols (₩), percentages, and diagnostic IDs.

- **Numerals & Metrics**: Large monetary numbers use `font-variant-numeric: tabular-nums` to maintain tabular stability in comparative calculation grids.
- **Hangul Optimization**: Set line height slightly more generous (minimum 1.5× for body copy) with negative letter spacing (`-0.01em` to `-0.025em`) to counter natural optical sprawl in Korean glyphs.
- **Hierarchy Rules**: Display weights are reserved exclusively for quantitative summary totals (e.g., "총 240만원 수령 가능"). Section headers leverage `headline-md` at `600` weight to maintain an authoritative, non-distracting visual structure.

## Layout & Spacing

The layout is built around a predictable, 12-column responsive grid engineered for multi-step diagnosis forms, outcome dashboards, and dense welfare card listings:

- **Breakpoints**:
  - **Mobile (<768px)**: 4 columns, `margin: 1rem` (`16px`), `gutter: 1rem` (`16px`). Layout single-stacks with full-width action drawers.
  - **Tablet (768px–1023px)**: 8 columns, `margin: 1.5rem` (`24px`), `gutter: 1.5rem` (`24px`).
  - **Desktop (≥1024px)**: 12 columns, max-width bounded at `1200px`, centered on the canvas with `margin: 2rem` (`32px`), `gutter: 1.5rem` (`24px`).
- **Rhythm**: All vertical and horizontal spatial tokens derive from a strict 4px/8px incremental base. Diagnostic steps use `space-xl` (`40px`) between logical calculation blocks, while interactive form controls retain `space-md` (`16px`) internal padding.

## Elevation & Depth

This design system avoids heavy shadows, leaning instead on **structured surface separation and subtle ambient diffusion**:

- **Borders over Shadows**: Every floating surface or container possesses a crisp 1px hairline border in `#E2E8F0`. This anchors content against the `#F8FAFC` slate canvas.
- **Resting Layer (Surface Cards)**:
  - Border: `1px solid #E2E8F0`
  - Shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.02)`
- **Hover & Interactive Layer**:
  - Border: `1px solid #CBD5E1`
  - Shadow: `0 8px 16px -4px rgba(37, 99, 235, 0.06), 0 4px 6px -2px rgba(15, 23, 42, 0.03)`
  - Translation: `-1px` on the Y-axis for actionable welfare cards.
- **Floating Modals & Dynamic Drawers**:
  - Border: `1px solid #E2E8F0`
  - Shadow: `0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04)`
  - Backdrop: `#0F172A` at 40% opacity with `backdrop-filter: blur(4px)`.

## Shapes

A balanced geometry (Level 2: Rounded) provides a friendly yet structured look appropriate for civic-financial applications:

- **Base Radius (`0.5rem` / `8px`)**: Applied to input fields, regular buttons, tooltips, and tabular rows.
- **Large Radius (`1rem` / `16px`)**: Applied to benefit recommendation cards, summary statistics blocks, and filter panels.
- **Pill Radius (`9999px`)**: Reserved strictly for categorization badges (e.g., "월세지원", "취업장려금"), status tags ("신청가능", "D-5"), and round iconography nodes.

## Components

### Buttons
- **Primary CTA**: Deep electric blue (`#2563EB`), text `#FFFFFF`, font-weight 600, height 48px, radius 8px. Hover state deepens to `#1D4ED8`. Active state uses scale `0.99`.
- **Secondary / Action**: Pure white background, `1px solid #E2E8F0`, text `#1E293B`. Hover state shifts border to `#CBD5E1` and background to `#F8FAFC`.
- **Success / Grant Claim**: Emerald green (`#059669`), text `#FFFFFF`. Reserved for final application submission or external government linkouts.

### Welfare Cards
- Background `#FFFFFF`, border `1px solid #E2E8F0`, border-radius 16px, padding 24px.
- Internal layout split: Top header houses category pill and application deadline (`D-day`); center displays benefit title (`headline-sm`) and monetary outcome highlighted in `#059669`; footer contains institutional logo/issuer (e.g., "서울특별시", "고용노동부") and diagnosis match rate gauge.

### Badges & Chips
- Compact dimensions: height 24px, horizontal padding 8px, font size 12px (`label-md`), full pill shape (`9999px`).
- **Benefit / Eligible Badge**: `#ECFDF5` background, `#047857` text, optional 1px border `#A7F3D0`.
- **Status / In-Progress Badge**: `#EFF6FF` background, `#1D4ED8` text, border `#BFDBFE`.
- **Urgent / D-Day Badge**: `#FEF2F2` background, `#B91C1C` text, border `#FECACA`.

### Diagnostic Form Inputs & Selectors
- Height 48px, border `1px solid #CBD5E1`, background `#FFFFFF`, radius 8px, padding 12px 16px.
- Focus state: `border-color: #2563EB`, outer focus ring `0 0 0 3px rgba(37, 99, 235, 0.15)`.
- Numeric inputs for income/assets feature right-aligned monetary affix ("원") and auto-formatting commas.

### Selection Controls (Checkboxes & Segmented Toggles)
- Custom square checkboxes (radius 4px) and circular radios (18px) with `#2563EB` fill on checked state with crisp white vector marks.
- Multi-choice welfare categories use interactive filter chips: white background with `#E2E8F0` border when unselected; transitioning to `#EFF6FF` fill, `#2563EB` border, and `#1D4ED8` text when active.

### AI Fit-Score Progress Indicator
- Horizontal micro-gauge bar with a track of `#F1F5F9` (height 6px, radius 9999px) and animated fill in `#10B981` transitioning to `#2563EB` based on qualification match percentage.