---
name: efficient-web-design
description: Design, document, evolve, or visually review product-focused web interfaces and design standards; use when a request needs visual hierarchy, a DESIGN.md, responsive composition, interaction-state intent, accessibility design, or perceptual UI critique rather than web implementation mechanics.
---

# Efficient Web Design

Own the product's visual direction and the evidence that supports it. Make the user's task, product-specific objects, and next action clear before adding decoration. Extend an established visual system when one exists; do not invent a new one to make a small change look redesigned.

Use this skill for web interface design, redesign, visual-system maintenance, `DESIGN.md` creation or revision, and visual/perceptual review. It specifies intent and acceptance criteria. `efficient-web-development` owns HTML, CSS, browser integration, performance implementation, and automated or manual implementation testing. Use `efficient-testing` for focused tests when an implementation change needs them.

## Workflow

1. **Establish the decision and its boundary.** Read the request, product brief, affected screens or flows, existing UI, and constraints. State the primary user, their goal, the one primary action or outcome, affected routes or surfaces, and the requested deliverable. Treat approved brand, content, legal, and accessibility requirements as constraints.
   - If the request is ambiguous but a small, reversible interpretation is possible, state that interpretation and design only the named surface.
   - If the primary task, audience, or required content is unknown and changes hierarchy materially, ask for it or mark it as an unresolved design decision. Do not substitute a fashionable layout or generic dashboard for product evidence.
   - Keep visual exploration separate from unrelated feature, content, or implementation changes.

2. **Discover the visual system before proposing changes.** Inspect existing `DESIGN.md` files, design tokens or themes, reusable patterns, representative screens, brand assets, and the closest related surface. Record an evidence ledger with each decision's source path or rendered observation, the inference, and any uncertainty.
   - Distinguish an explicit standard from a repeated convention, a vendor default, and a one-off exception.
   - If a coherent system exists, reuse its roles, components, density, and interaction language. Add a variant only when its task or state differs materially.
   - If evidence conflicts, preserve the more local, approved, or recently used pattern; flag the conflict instead of silently normalizing the product.
   - If no system exists, create only the small baseline needed for the requested surface. Mark unverified brand or product assumptions `UNCONFIRMED` rather than presenting them as established standards.

3. **Set information hierarchy and composition.** Order content by the user's task: orient, identify the relevant product object or status, expose the next action, then place supporting detail and secondary actions. Give the primary action a distinct but proportionate visual weight; do not make every panel, badge, and button compete.
   - Use grouping, alignment, spacing, type roles, and semantic color roles to communicate relationships. Prefer clear labels and real product terminology over decorative icons, vague copy, or color alone.
   - Preserve familiar web conventions unless product evidence justifies a departure. Keep reading order, visual order, and intended keyboard order aligned in the design.
   - Reduce competing elements before adding effects, gradients, shadows, animation, or a new component. Add a token, component, or variant only when it has repeated use or a meaningfully distinct state.

4. **Define or revise the visual standards.** Maintain `DESIGN.md` when the request asks for it or when a decision will govern multiple screens, components, or future work. Otherwise produce a scoped design brief and do not create a repository-wide standard by implication.

   When creating or updating `DESIGN.md`, keep it evidence-backed and scoped. The local product-focused template below is an extension, not a replacement for a token catalog. If adopting the upstream Google Labs format, optional machine-readable YAML frontmatter uses exact `---` delimiter lines and includes `name`; add only evidence-backed applicable standard properties (`version`, `description`, `omitted`, `colors`, `typography`, `rounded`, `spacing`, and `components`). Token values are normative; prose explains their product application and rationale. Use optional `{path.to.token}` references only for established tokens. The format is extensible, so retain relevant local sections and do not impose a fixed section order, but do not duplicate level-2 headings.

   Include only sections relevant to the product:

   ```markdown
   # Design: <product or surface>

   ## Scope and evidence
   - Surfaces and users covered:
   - Sources inspected:
   - Established decisions / `UNCONFIRMED` assumptions:

   ## Foundations
   - Color roles and contrast constraints:
   - Typography roles and readability rules:
   - Spacing, layout, shape, and elevation conventions:

   ## Patterns and states
   - Product-specific objects and component variants:
   - Default, hover, focus, active/selected, disabled, loading, empty, error,
     success, and recovery behavior as applicable:

   ## Responsive and accessible intent
   - Content priorities, composition changes, and overflow rules:
   - Keyboard, focus, labels, non-color cues, motion, and target-size criteria:

   ## Validation and ownership
   - Rendered review scenarios and acceptance criteria:
   - Design decisions versus implementation responsibilities:
   - Open questions and decisions that require evidence:
   ```

   Do not prescribe component code, CSS declarations, framework routing, data fetching, or test commands in `DESIGN.md`. Update the evidence and rationale when changing a standard; do not turn its prose or local extensions into a dump of raw values or inherited library defaults. When project-approved format or lint tooling already exists, it may be run before and after the update; an available token diff may likewise be used to review token changes. Neither is required. Read [DESIGN.md format and tooling](references/design-md-tooling.md) only when the repository has adopted the upstream Google Labs format or a request specifically needs format validation, comparison, or specification lookup.

5. **Make foundations deliberate and usable.** Use existing values and names where they express the intended system. When a new decision is necessary, define it by purpose and relation rather than a collection of unrelated visual values.
   - **Typography:** define roles for display, headings, body, labels, and supporting data as needed. Make hierarchy apparent through a restrained combination of size, weight, line length, line height, and spacing. Preserve readable text at narrow widths and enlarged text.
   - **Spacing and surfaces:** use a small, repeatable rhythm. Separate page regions, grouped controls, and dense data according to their relationship; avoid arbitrary per-element offsets and ornamental containers.
   - **Color and emphasis:** assign semantic roles for surfaces, text, borders, interactive emphasis, and status. Reserve strong color for meaning or priority, provide a non-color cue for status, and verify contrast for each text, icon, border, and focus pairing in its actual context.
   - **Components:** document the product-specific object, purpose, variants, and visual states. Reuse a primitive only when it preserves task clarity; resemblance alone is not a reason to force unrelated behavior into one component.

6. **Specify responsive, state, and inclusive behavior as design contracts.** Start with content priority rather than named devices. Define when a composition may reflow, stack, condense, scroll, or defer secondary information; do not hide the user's primary task merely to preserve a desktop layout. Use content- or container-driven thresholds in the handoff rather than device folklore.
   - Design for usable reflow at 320 CSS pixels and text resize at 200% without avoidable two-dimensional scrolling. Identify an intentional alternative for wide tables, dense data, or media rather than allowing clipping.
   - For every meaningful interaction, specify the relevant default, hover (when pointer input exists), keyboard focus, active or selected, disabled, loading, empty, error, success, and recovery states. State what changes, what feedback is conveyed, and what the user can do next. Do not make hover the only affordance or status color the only signal.
   - Target the applicable accessibility requirement, normally WCAG 2.2 AA unless the product requires another level. Make visible focus, logical heading and landmark intent, descriptive labels and link purpose, image alternative intent, keyboard operation, readable error/recovery feedback, reduced-motion behavior, and at least 24 by 24 CSS-pixel interactive targets explicit where applicable.

7. **Hand off an implementable design decision, not implementation mechanics.** Provide a concise inventory of changed foundations, affected patterns, state matrix, responsive rules, accessibility acceptance criteria, and unresolved assumptions. Name observable outcomes, for example: “At narrow width, the primary status and action remain before secondary metadata; each error explains recovery.”
   - Send semantic markup, CSS layout/query choices, browser behavior, performance work, and test execution to `efficient-web-development`. Route framework-specific composition and data/state ownership to the applicable installed framework skill, such as `efficient-react` or `efficient-tanstack`.
   - If a design requirement cannot be met with the existing platform, state the design constraint and user impact; do not prescribe an unverified workaround.

8. **Review the rendered experience and close the loop.** When a runnable interface is available, inspect the changed flow at a representative wide width, narrow width, 200% text size or zoom, and each material state. Navigate it by keyboard and inspect focus, labels, contrast, content order, target spacing, overflow, and reduced-motion behavior. Use an automated accessibility audit as supplemental evidence, not proof of conformance.
   - Compare the result to the documented hierarchy and system, not personal taste. Record viewport, state, interaction path, and observable evidence.
   - Report no more than three material findings, ordered by user impact. For each, state the evidence and the smallest concrete design correction. If no material issue is observed, say so and state the review limits.
   - If rendering, required states, or audit access is unavailable, complete a source-and-design review only, mark rendered claims unverified, and name the smallest prerequisite for confirmation. Do not claim visual, responsive, or accessibility success from an unrendered design alone.

## Design quality guardrails

- Favor the smallest coherent change that makes the task clearer. Preserve established behavior, content priority, and user expectations unless the requested decision changes them.
- Treat inconsistent repetition as a signal to investigate, not automatic justification for a system rewrite. Consolidate only after identifying the intended pattern and affected users.
- Measure a proposed density, hierarchy, or perceptual improvement in the relevant rendered state before calling it an improvement. Do not optimize for visual novelty, token count, or a generic “polished” look.
- Keep decisions conventional enough to be understood without explanation, then spend distinct visual treatment only on product-specific meaning, task priority, or feedback.

## Completion evidence

Report:

- the design decision, affected surfaces, and product task it supports;
- visual-system evidence reused or the bounded assumptions made;
- `DESIGN.md` or standards updated, if any, and its scope, including whether upstream-format frontmatter/tokens were adopted;
- hierarchy, responsive, state, and accessibility acceptance criteria handed off;
- rendered and accessibility review evidence actually obtained, plus skipped or blocked checks; separately report whether optional format validation, linting, or token diff ran—those checks are not rendered product evidence;
- remaining open decisions, risks, or implementation dependencies.
