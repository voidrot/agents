---
name: efficient-react
description: "Implement and review React component boundaries, local state, effects, rendering behavior, accessibility, performance, project structure, and focused tests; use for React UI changes or defects, excluding JavaScript fundamentals and TanStack APIs."
---

# Efficient React

Use this skill for React component work: adding or changing interactive UI, repairing component behavior, reviewing component boundaries, or investigating React rendering and performance. It owns component composition and local UI behavior, not product visual direction, JavaScript fundamentals, routing, or remote/server-state policy.

For language-level code concerns, use `efficient-javascript`. When the project uses TanStack, use `efficient-tanstack` for routing, URL state, loaders, remote data, caching, and server-state mutations. For other routing or remote-state libraries, follow the installed library or framework's established workflow. Use `efficient-testing` to scope and run the focused test evidence.

## Workflow

1. **Establish the local contract before editing.** Read the request, accepted design or UX criteria, the affected component and callers, nearby tests, package manifest and lockfile, build configuration, and existing component conventions. Identify the visible states, user actions, inputs, output or callbacks, error and recovery behavior, and whether rendering is client-only or crosses a server/client boundary. Preserve existing observable behavior, errors, side effects, ordering, and accessibility unless the request changes them.
   - If the requested behavior, ownership, or framework boundary is unclear, inspect the immediate caller and rendered use first. State the smallest bounded assumption if it remains unknown.
   - Do not invent visual hierarchy, tokens, copy, routes, data contracts, or a dependency. Return those decisions to their owner rather than encoding guesses in a component.

2. **Classify ownership and choose the smallest boundary.** Separate each value into a prop, local UI state, derived render value, shared UI state, or remote/server state. Keep local state in the component that owns the interaction; lift it only to the nearest common parent that must coordinate it. Pass data down and actions up through explicit props or callbacks.
   - Derive values from current props and state during render. Do not store a second copy merely to make rendering convenient.
   - Introduce shared context only for a stable cross-tree concern with multiple real consumers. Do not use it to avoid passing a few explicit props or to distribute frequently changing state across an unrelated subtree.
   - Model a multi-step or invalid transition explicitly only when the actual interaction has coordinated transitions. Otherwise, retain simple local state. Keep remote state and navigation at their assigned boundary.

3. **Define a component contract before implementation.** Name the component for its user-facing responsibility. Give it a small prop surface that states required data, optional variation, events, and ownership. Prefer composition when callers need independently arranged content or behavior; otherwise keep one direct component rather than creating a generic abstraction.
   - Use a stable domain identifier for each stateful list item. Do not use position as identity when items can be inserted, removed, reordered, or retain local state.
   - Keep a component focused on one coherent UI responsibility. Extract a child or custom hook only when it has an independently understandable contract, a real reuse need, or isolates a distinct browser/external-system concern.
   - If an existing abstraction forces unrelated flags, duplicated state, or unclear ownership, make the smallest behavior-preserving simplification in the touched area. Do not start a broad component-library rewrite.

4. **Keep render pure and make updates safe under interruption.** Treat rendering as a calculation of UI from its inputs. Do not mutate props, shared objects, the DOM, storage, or external systems while rendering. Produce new state values instead of mutating prior snapshots.
   - Use an updater based on the prior value when the next value depends on it. Do not depend on a particular number, timing, or order of renders and updates.
   - Keep urgent input feedback separate from expensive, deferrable presentation work when users can observe input lag. Make pending and stale presentation intentional and understandable; do not defer a value that must remain synchronous for correctness.
   - Place loading, empty, error, and recovery boundaries where a failure or wait should affect that part of the UI, not the whole page by default. Ensure a fallback has a useful next action when recovery is possible.
   - If a render mismatch, repeated render, lost local state, or stale result occurs, first reduce it to deterministic inputs. Check identity keys, prop/state ownership, render-time mutation, and server/client-dependent values. Do not suppress warnings or add timing delays as a fix.

5. **Use effects only to synchronize with an external system.** Put user-caused work directly in the event handler when it does not synchronize with an external system. Use an effect for subscriptions, imperative browser APIs, timers, or another external resource that must follow rendered state.
   - Name the external system and the value that controls synchronization before adding an effect. Include every reactive input the synchronization reads, and return cleanup that reverses subscriptions, listeners, timers, requests, or imperative setup.
   - Keep each effect responsible for one synchronization. If changing dependencies causes a loop, write down what the effect reads and writes; then remove derived state, move interaction work to its handler, or split the synchronization. Do not omit dependencies to hide the loop.
   - Make asynchronous completion safe when inputs change or the component unmounts: cancel when the API supports it or ignore obsolete results. Preserve cancellation and error semantics rather than treating every failure as success.

6. **Implement accessibility at the component boundary.** Start with semantic HTML and native controls. Give every interactive control an accessible name, every form control an associated label, and every informative image appropriate alternative text. Use ARIA only when native semantics cannot express the required behavior.
   - Preserve logical DOM, reading, and focus order. Do not add keyboard handlers that duplicate a native control's activation.
   - For dynamic errors, status, dialogs, menus, and focus movement, implement the required role, state, announcement, and focus restoration as one component contract. Include disabled, loading, validation-error, and recovery states where the interaction exposes them.
   - Honor the accepted responsive rules without choosing new visual direction. Check usable reflow at narrow widths, 200% text resize, visible focus, contrast, keyboard operation, and target size. If no design acceptance criteria exist, record that limit rather than claiming conformance.

7. **Organize files by the existing project boundary.** Keep a component, its styles, test, and tightly coupled helper together when the repository does so. Put reusable primitives only where several confirmed consumers need the same stable contract. Keep feature-specific components inside their feature rather than creating a catch-all shared directory.
   - Follow the installed React and framework conventions after inspecting them; version- or framework-specific APIs are not assumed by this skill.
   - Keep a change narrow. Separate a behavior change from an unrelated refactor, migration, or package upgrade unless they are inseparable and explicitly justified.

8. **Measure before optimizing.** Start from a reproducible user-visible symptom: slow input, expensive update, excessive work, layout instability, or bundle cost. Record a baseline with the repository's available profiler, browser performance tooling, or build report. Change one plausible cause at a time and remeasure the same interaction.
   - First remove unnecessary work, incorrect state placement, repeated external synchronization, or needless rendering. Add memoization, deferral, code splitting, or virtualization only when measurement shows the changed boundary benefits and the added invalidation or loading behavior is correct.
   - If the symptom cannot be reproduced or the measurement is inconclusive, do not claim an optimization. Retain the baseline facts, remove temporary instrumentation, and report the smallest next diagnostic step.

9. **Prove the observable component contract.** Add or update the smallest focused test for changed behavior. Render with only the production-relevant providers, act through accessible controls, and assert visible output, accessible state, or an externally observable callback. Cover an error, empty, loading, disabled, or recovery state only when the requirement or confirmed defect requires it.
   - Read [React component test decisions](references/react-component-testing.md) only when adding or revising a React component test; it supplies the React-specific query, interaction, network, provider, and environment decisions. Follow the installed runner, libraries, exact versions, and local test conventions rather than assuming a stack.
   - Use a real browser-level check when layout, focus behavior, scrolling, CSS, browser APIs, or hydration is material; a DOM-only test is not evidence for those conditions.
   - Run the narrowest supported formatter, type check, lint, and targeted test command that reaches the change. Then manually inspect the rendered affected states and keyboard path when the environment permits. Do not install a runner or test library merely to satisfy this workflow.
   - If a defect is reported, reproduce it with a deterministic failing signal before changing code when practical. Test falsifiable causes one at a time, retain the smallest regression test or durable reproduction, and remove temporary probes.

10. **Classify failures and finish with evidence.** Treat a failed check as either a product defect, incorrect expectation, component-test setup problem, build/configuration issue, unavailable environment, or upstream boundary problem. Preserve the output and relevant inputs, fix the identified cause, then rerun only checks affected by that cause. Do not weaken assertions, add retries, mute warnings, or silently fall back to a different behavior.

## Completion evidence

Report only what was observed:

- changed component boundaries, state owner, effect/external-system contract, and any intentional rendering or recovery boundary;
- accessibility states and keyboard/rendered checks performed, plus any unverified acceptance criterion;
- focused tests and commands run, their results, and relevant test or browser limits;
- performance baseline and post-change measurement when optimization was requested; otherwise state that no performance claim was made;
- skipped or blocked validation, the exact missing prerequisite or failure output, and the smallest next action.

Stop when the requested React behavior has direct evidence. Do not turn a local UI change into a new state architecture, visual redesign, routing change, or performance project.
