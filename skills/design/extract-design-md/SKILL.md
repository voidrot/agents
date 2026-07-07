---
name: extract-design-md
description: >-
  Use this skill to extract a DESIGN.md design system directly from frontend
  source code when a user wants to audit, document, migrate, or understand an
  app's visual language without relying on a rendered build. Works for React,
  Vue, Svelte, Angular, plain HTML/CSS, Tailwind, CSS-in-JS, and component-library
  themes such as MUI, Chakra, Ant Design, Vuetify, Mantine, and shadcn/ui.
---

# Extract Design System from Frontend Code

Analyze frontend source code to extract a comprehensive design system document
(DESIGN.md) that captures the project's visual language — colors, typography,
spacing, component patterns, and layout principles — directly from the source
files, without needing to build or render the application.

## Why This Exists

The `design-md` skill works from rendered HTML. But often you have a codebase
and want to understand its design system before you can even run the app —
maybe dependencies are missing, the build is broken, or you just want a quick
audit. This skill reads the source files themselves: stylesheets, component
files, theme configs, and Tailwind setups. It's faster and works anywhere.

## When to Use

- User has a frontend codebase and wants to extract or document its design system
- User wants to migrate a project's visual identity into DESIGN.md
- User asks to "audit the styling" or "understand the design language" of a repo
- User wants to create a DESIGN.md from existing source code
- The app can't be built/rendered but the source is available
- User wants to unify or reconcile inconsistent styles across a codebase

## Prerequisites

- Access to the frontend project's source directory
- No build or runtime dependencies needed for extraction — this skill reads source files only
- Node/npm access is needed for final DESIGN.md validation with `npx @google/design.md lint DESIGN.md`

---

## Workflow

### Phase 1: Project Discovery

Start by understanding what you're working with. This determines which
extraction patterns to use.

#### 1. Detect the Framework and Stack

Scan the project root for telltale files:

| Signal File                               | Framework / Tool   |
| :---------------------------------------- | :----------------- |
| `package.json` with `react`               | React / Next.js    |
| `package.json` with `vue`                 | Vue / Nuxt         |
| `package.json` with `svelte`              | Svelte / SvelteKit |
| `package.json` with `@angular/core`       | Angular            |
| `tailwind.config.js/ts`                   | Tailwind CSS       |
| `postcss.config.js`                       | PostCSS pipeline   |
| `styled-components` or `@emotion` in deps | CSS-in-JS          |
| `@mui/material` or `@mui/system` in deps  | Material UI / MUI  |
| `@chakra-ui/react` in deps                | Chakra UI          |
| `antd` in deps                            | Ant Design         |
| `vuetify` in deps                         | Vuetify            |
| `@mantine/core` in deps                   | Mantine            |
| `components.json`                         | shadcn/ui          |
| `.css` / `.scss` / `.less` files only     | Plain CSS / SASS   |
| `theme.js` / `theme.ts` / `tokens.js`     | Design token files |

Read `package.json` first — it reveals the framework, CSS tooling, and any
design-token libraries (e.g., `style-dictionary`, `@tokens-studio`,
`@chakra-ui/react`, `@mui/material`, `antd`, `vuetify`, `@mantine/core`). This context tells you _where_ to look for
styling information.

#### 2. Map the Source Tree

Identify the key directories and files you'll analyze:

```
src/
├── components/     ← Component-level styles
├── styles/         ← Global stylesheets
├── theme/          ← Theme definitions, tokens
├── assets/         ← Fonts, images
├── app.css         ← Root styles
└── index.css       ← Entry CSS
```

Also check for:

- `tailwind.config.js` / `tailwind.config.ts` — Custom colors, fonts, spacing
- `globals.css` / `global.css` — CSS custom properties (variables)
- Any `theme.*` or `tokens.*` files
- Component library config (e.g., `theme.ts`, `mui-theme.ts`, `createTheme.ts`,
  `chakra-theme.ts`, `vuetify.config.ts`, `mantine-theme.ts`, `components.json`)

#### 3. Read Framework-Specific Guidance

Consult the appropriate reference for extraction patterns:

- **React / Next.js / Tailwind** → [references/react-tailwind.md](references/react-tailwind.md)
- **Vue / Nuxt** → [references/vue.md](references/vue.md)
- **Svelte / SvelteKit** → [references/svelte.md](references/svelte.md)
- **Angular** → [references/angular.md](references/angular.md)
- **Plain CSS / SASS / Less** → [references/plain-css.md](references/plain-css.md)

These references contain framework-specific patterns for locating colors,
typography, spacing, and component styles. Read the one that matches before
proceeding.

#### 4. Identify Component-Library Source of Truth

If the project uses a UI component library, separate **library defaults** from
**project-specific overrides**. DESIGN.md should emphasize the custom visual
language, not restate a vendor's generic baseline.

| Library                  | High-Signal Files / APIs                                                                 | What to Extract                                                                                                  |
| :----------------------- | :--------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| **MUI / Material UI**    | `createTheme()`, `ThemeProvider`, `CssBaseline`, `sx` props, `styled()`, `components.*.styleOverrides`, `palette`, `typography`, `shape`, `spacing`, `breakpoints` | Palette roles, typography variants, spacing multiplier, border radius, shadows/elevation, component overrides, custom `sx` idioms |
| **Chakra UI**            | `extendTheme()`, `ChakraProvider`, `semanticTokens`, `components`, `layerStyles`, `textStyles` | Semantic tokens, color mode behavior, text styles, layer styles, component variants                              |
| **Ant Design**           | `ConfigProvider theme`, `token`, `components`, Less variables                            | Seed/map tokens, component tokens, radius, control height, color algorithms, compact/dark mode choices           |
| **Vuetify**              | `createVuetify()`, `theme`, `defaults`, SASS variables                                   | Theme colors, density, defaults, aliases, component defaults                                                     |
| **Mantine**              | `createTheme()`, `MantineProvider`, `theme.components`, `variantColorResolver`           | Color scales, primary shade, font families, radius, spacing, component defaults                                  |
| **shadcn/ui**            | `components.json`, `globals.css`, `tailwind.config.*`, copied component files            | CSS variable tokens, radius, Tailwind theme mapping, local component variants                                    |

For **MUI specifically**, look for both centralized theme configuration and
distributed styling:

- `createTheme({ palette, typography, spacing, shape, shadows, breakpoints, components })`
- `components.MuiButton.styleOverrides`, `variants`, and `defaultProps`
- `sx={{ ... }}` usage patterns that repeat across screens
- `styled(Button)` / `styled(Box)` wrappers that create project-specific primitives
- CSS variables from `experimental_extendTheme` / `CssVarsProvider`, if present

Only document vendor defaults when they materially affect the product and have
not been overridden; label them as inherited defaults rather than project tokens.

---

### Phase 2: Deep Extraction

Work through each design dimension systematically. For each one, gather raw
data from the source files, then synthesize it into descriptive language.

The goal isn't to dump every CSS property — it's to understand the _intent_
behind the styling choices and describe them in human, editorial language that
another designer (or Stitch) can use to recreate the same visual feel.

#### 1. Visual Theme & Atmosphere

Read the broadest styling first to understand the overall mood:

- **Root background**: What's the `body` or root element background? Light
  cream (#f-range) signals airy/clean; dark (#0-#2 range) signals moody/dramatic.
- **Whitespace philosophy**: Are spacing values generous (32px+) or tight?
  Check padding/margin values on root containers, section wrappers, and card components.
- **Density**: Count the components per page/section. Few with space = minimal;
  many packed tight = information-dense.
- **Color temperature**: Are the neutrals warm (creams, tans) or cool (blue-grays, slates)?
- **Overall feel**: Synthesize into 1-2 rich sentences that capture the mood.

Look for these signals in the source:

| Source Location                                       | What It Tells You                          |
| :---------------------------------------------------- | :----------------------------------------- |
| Root `background-color` or Tailwind `bg-*` on layouts | Overall lightness/darkness                 |
| Spacing scale in Tailwind config or CSS vars          | Whitespace philosophy                      |
| Number of components vs. wrapper padding              | Density                                    |
| Custom property naming (`--warm-*` vs `--cool-*`)     | Color temperature intent                   |
| Comments in theme files                               | Design intent in the developer's own words |

#### 2. Color Palette & Roles

Extract every unique color from the codebase and assign functional roles.
Search across all layers:

**Where to find colors:**

| Layer                   | What to Search                              |
| :---------------------- | :------------------------------------------ |
| CSS custom properties   | `--color-*`, `--primary`, `--bg-*`          |
| Tailwind config         | `theme.extend.colors`                       |
| Theme/token files       | Color objects, palettes                     |
| Component styles        | `background-color`, `color`, `border-color` |
| Inline/scoped styles    | `bg-*`, `text-*` classes in templates       |
| CSS-in-JS theme objects | `colors`, `palette` keys                    |

**How to organize:** Group colors by function, not by hue:

1. **Primary Foundation** — Background and surface colors
2. **Accent & Interactive** — CTA buttons, active states, links
3. **Typography & Text Hierarchy** — Primary, secondary, tertiary text
4. **Functional States** — Success, error, warning, info

For each color, create a descriptive name that evokes the color's character
rather than its raw hex value:

- ❌ `#294056` → "Blue"
- ✅ `#294056` → **"Deep Muted Teal-Navy"** — Primary CTA, active navigation

**Deduplication matters.** Codebases often have near-duplicate colors (e.g.,
`#333` and `#2C2C2C`). Consolidate them under one name that best represents
the intended color.

#### 3. Typography Rules

Extract the complete typographic system:

**Font families:**

- Check CSS `font-family`, Tailwind `fontFamily`, Google Fonts links, or
  local `@font-face` declarations.
- Note the **character** of each font: geometric vs humanist, serif vs sans,
  the feeling it evokes.

**Type scale (hierarchy):**

- Find every heading level (H1-H6) and body text, noting:
  - `font-size` (in rem or px)
  - `font-weight` (numeric value + descriptive name)
  - `letter-spacing` (and why — elegance? compactness?)
  - `line-height` (generous for readability? tight for display?)
- Map component usage: Which heading level do product cards use? What about
  hero sections?

**Spacing principles:**

- How does text spacing relate to the overall spacing scale?
- Letter-spacing patterns on headings vs body
- Line-height philosophy (generous/relaxed for body, tighter for display)

#### 4. Component Stylings

Analyze the 4-5 most important UI primitives:

**Buttons:**

- Corner radius (and what it communicates — playful? professional? minimal?)
- Color scheme for primary, secondary, and ghost variants
- Hover/focus/active states and transition timing
- Padding ratios (horizontal vs vertical)

**Cards / Containers:**

- Corner radius (often different from buttons — slightly rounder)
- Shadow strategy: flat, subtle hover shadows, or always elevated?
- Border treatment: hairline borders, colored accents, or none?
- Internal padding (generous or compact?)
- Image treatment within cards (full-bleed, padded, rounded?)

**Navigation:**

- Layout pattern (horizontal bar, vertical sidebar, drawer)
- Typography treatment (uppercase, letter-spacing, weight)
- Active/hover state indicators (underline, color, background)
- Mobile behavior (hamburger, bottom nav, drawer)

**Inputs & Forms:**

- Border style and focus state behavior
- Corner style consistency with buttons
- Padding and touch-target sizing

**Domain-Specific Components:**

- Identify 1-2 components unique to this project (e.g., product cards,
  dashboard widgets, chat bubbles) and describe their styling patterns.

#### 5. Layout Principles

Extract the structural system:

**Grid & Structure:**

- Max content width (from `max-width` on containers)
- Column system (CSS Grid, Flexbox patterns, defined breakpoints)
- Responsive breakpoints (from media queries or Tailwind config)

**Whitespace Strategy:**

- Base spacing unit (8px grid? 4px? custom?)
- Section margins (how much space between major sections)
- Edge padding (page margins at different breakpoints)

**Alignment & Visual Balance:**

- Text alignment patterns (centered heroes, left-aligned body)
- Image-to-text ratios
- Visual weight distribution

**Responsive Behavior:**

- Mobile-first or desktop-first?
- How do grids collapse? Padding scale?
- Touch target sizing

#### 6. Stitch Generation Notes

Synthesize the extraction into actionable prompts for Stitch:

- **Atmosphere language**: Translate the mood into natural descriptors
- **Color references**: List colors by descriptive name + hex
- **Component prompts**: Write 2-3 example prompts that would recreate
  key components in Stitch
- **Iteration guidance**: Tips for refining screens in this design system

---

### Phase 3: Write the DESIGN.md

Assemble everything into the standard DESIGN.md format. Place it at
`./DESIGN.md` in the project directory.

> [!IMPORTANT]
> You **MUST** include the YAML frontmatter at the top of the file with `name` and `colors` mapping, exactly as shown in the example at [examples/DESIGN.md](examples/DESIGN.md). This structured data is required for other skills to parse the design system.
>
> Failure to include this YAML block with at least the core color tokens is a failure to use this skill correctly.

Use the format from the example at [examples/DESIGN.md](examples/DESIGN.md) as your template. The file must start with the YAML block, followed by the markdown sections:

```markdown
# Design System: [Project Name]

**Project ID:** [If known, otherwise omit]

## 1. Visual Theme & Atmosphere

[Rich 2-paragraph description of mood, philosophy, and key characteristics]

## 2. Color Palette & Roles

### Primary Foundation

### Accent & Interactive

### Typography & Text Hierarchy

### Functional States

## 3. Typography Rules

### Hierarchy & Weights

### Spacing Principles

## 4. Component Stylings

### Buttons

### Cards & [Domain-Specific Containers]

### Navigation

### Inputs & Forms

### [Domain-Specific Components]

## 5. Layout Principles

### Grid & Structure

### Whitespace Strategy

### Alignment & Visual Balance

### Responsive Behavior & Touch

## 6. Design System Notes for Stitch Generation

### Language to Use

### Color References

### Component Prompts

### Incremental Iteration
```

---

### Phase 4: Lint and Fix DESIGN.md

After writing `DESIGN.md`, validate it with the Google design.md linter from the
same directory as the file:

```sh
npx @google/design.md lint DESIGN.md
```

If the linter reports errors, fix `DESIGN.md` and rerun the exact command. Repeat
until the command returns with no lint errors. Do not deliver the skill output
while lint errors remain.

If the command cannot run because npm/network/package access is unavailable,
state that validation was blocked and include the exact failure. Still manually
check that the frontmatter contains parseable YAML and the required design-token
sections.

---

## Quality Checklist

Before delivering the DESIGN.md, verify:

- [ ] Every color has a descriptive name, hex code, and functional role
- [ ] Typography includes font family, character description, and full hierarchy
- [ ] Component styles describe shape, color, states, and transitions
- [ ] Layout includes max-width, grid, breakpoints, and spacing strategy
- [ ] Stitch generation notes use natural language, not CSS syntax
- [ ] The atmosphere section reads like editorial copy, not technical docs
- [ ] Near-duplicate colors are consolidated
- [ ] The document captures the _intent_ behind styling, not just raw values
- [ ] Component-library defaults are distinguished from project-specific overrides
- [ ] `npx @google/design.md lint DESIGN.md` returns no lint errors, or the exact validation blocker is reported

## Tips for Better Extraction

- **Read comments and commit messages.** Developers often document design
  intent in code comments (`/* hero section — breathable */`) and commit
  messages. These are gold for understanding the _why_.
- **Check for design-token libraries.** If the project uses `style-dictionary`,
  `@tokens-studio`, or similar, these files are the most authoritative
  source of design values.
- **Theme files are higher-signal than component styles.** A `theme.ts` that
  defines a palette tells you the intended design system; scattered inline
  styles in components tell you what actually shipped. Both matter, but
  start from the theme.
- **Tailwind config is a design system.** If a project has a customized
  `tailwind.config.js`, that _is_ the design system — extract from it first,
  then spot-check components for overrides.
- **CSS custom properties are intentional.** If a developer defined
  `--brand-primary`, they're telling you this is a design token. Respect that.
