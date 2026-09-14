---
name: efficient-web-development
description: Implement or repair browser-facing web application behavior across client and server boundaries, including semantic documents and forms, responsive and accessible interactions, browser/network behavior, security boundaries, performance delivery, and integration validation; use when a web feature or defect must work for real browser users beyond framework-specific component mechanics or visual design decisions.
---

# Efficient Web Development

Use this skill to deliver a small, working web vertical slice from browser entry point through its server boundary. Preserve the existing product intent and conventions; change the smallest boundary that establishes the required user-visible behavior.

Do not use this skill for React component/state mechanics, framework routing or server-state APIs, general code refactors, or choosing a product's visual direction. Ask the responsible framework workflow to handle its mechanics. Return visual hierarchy, content, component variants, and interaction-intent decisions to the design owner; implement their stated acceptance criteria rather than inventing them. Use `efficient-testing` for focused unit or regression tests when a changed contract warrants them.

## Workflow

1. **Establish the user contract and ownership.** Read the request, relevant screen or route, server endpoint, tests, product/design artifacts, and nearby conventions. State the user action, visible result, data/network effect, required states (loading, empty, error, success, disabled, and recovery where applicable), and completion evidence. Identify which layer owns each concern:
   - browser implementation owns document semantics, forms, interaction, responsive CSS, browser APIs, accessibility, and browser-to-server integration;
   - the server boundary owns authentication/authorization decisions, validation, durable mutation, response status, and error representation;
   - framework-specific rendering, routing, and server-state behavior remain with their responsible workflow.
   If a product decision, API contract, authentication model, or framework behavior is unknown, inspect the authoritative local source before editing. Do not fabricate it or add a compatibility path without evidence. **When adding, changing, or diagnosing an HTTP API contract, read [REST/API Contract Review](references/api-contract-review.md).**

2. **Trace the complete path before changing it.** Follow the user input from markup and event handling through request construction, server validation/authorization, response mapping, and rendered state. Record the expected method, URL/route, payload shape, credentials mode, success result, and user-safe failure result. Check direct entry, refresh, back/forward, slow/offline network, duplicate submission, and cancellation only when they affect the requested path. Keep the existing contract and ordering unless the requirement explicitly changes them.

3. **Choose the simplest platform-native implementation.** Start with semantic landmarks, headings in logical order, native links, buttons, inputs, labels, `fieldset`/`legend`, and browser validation where they express the need. Use ARIA only to fill a native semantic gap; when adding ARIA behavior, implement its keyboard, focus, name, state, and update requirements together. Prefer normal document flow, flexible layout, and a content-driven breakpoint. Use a media query for viewport or user-preference changes; use a container query only when a reusable component must react to its parent width. Avoid new abstractions, custom controls, client state, dependencies, or API layers unless the existing boundary cannot meet the contract.

4. **Implement forms and interactions as recoverable user operations.** Associate every control with a visible or programmatic label and expose required format or constraint information before submission. Preserve entered values after a recoverable failure. On submit, prevent accidental duplicate mutations, show an unambiguous pending state, and restore a usable control after completion or failure. Put focus where it helps the user continue: normally leave it stable for inline feedback; move it deliberately to a new context, summary, or actionable error when needed. Do not use placeholder text as the only label, rely on color alone, or make a clickable non-control behave like a control.

5. **Enforce the server security boundary.** Treat every browser-supplied value, including hidden fields and client-side validation results, as untrusted. Authenticate the request, authorize the specific action and resource on the server, validate shape/range/ownership there, and use parameterized data access or the established safe data layer. Apply the repository's existing session, CSRF, origin, cookie, upload, redirect, and content-handling controls; do not weaken them to make a browser flow work. Return only user-safe errors and avoid putting secrets, tokens, sensitive data, or internal diagnostics in markup, URLs, client logs, or responses. If a cross-origin, credential, redirect, upload, or HTML-rendering path lacks an established policy, stop and obtain the responsible security/API decision rather than guessing.

6. **Make responses explicit and browser-safe.** Map expected outcomes to stable response status and body contracts, then render each deliberately. Distinguish input errors the user can correct from authentication/authorization failures, conflicts, absent resources, and unexpected failures. Do not expose stack traces or silently convert a failed mutation into success. Make retried or repeated mutations safe according to the established server contract; if that contract is absent, preserve the failure and request a decision instead of introducing speculative idempotency behavior. Handle cancellation and stale responses so an older result cannot overwrite the current user intent.

7. **Implement responsive and accessible behavior.** Keep source, reading, and focus order aligned. Check the changed experience at narrow width, at 200% text zoom, and without avoidable horizontal scrolling; preserve usable targets, readable content, and access to every control. Ensure keyboard-only users can reach and operate each interaction, see a visible focus indicator, dismiss or escape transient UI when applicable, and return focus appropriately after a temporary context. Give images appropriate alternatives, make link purpose clear in context, announce meaningful asynchronous status/error changes without excessive interruption, and preserve contrast and non-color cues. Do not claim conformance from an automated score alone.

8. **Deliver only measured performance work.** First establish a comparable baseline for the changed flow using the available browser tooling and representative local conditions. Inspect network requests, payload sizes, render/blocking work, image/font/script delivery, and user-visible timing. Fix a measured bottleneck with the smallest change, then rerun the same measurement. Do not add caching, preloading, code splitting, compression, a service worker, or new telemetry merely because it is customary. Preserve cache correctness, privacy, and invalidation semantics when an existing delivery mechanism changes.

9. **Validate the integrated user journey.** Run the narrowest supported checks that reach the changed boundary, then exercise the browser journey with real rendering evidence. At minimum, verify the success path and every required failure/recovery state; for an accessible or responsive change, also perform keyboard traversal, inspect the accessibility tree or equivalent semantics, and check narrow/zoomed rendering. Use an automated accessibility or performance audit as a diagnostic, then investigate material findings manually. **When live browser tooling is available and integration evidence or failure diagnosis is needed, read [Browser Diagnostics](references/browser-diagnostics.md).** For a bug, reproduce the original symptom before the fix when practical and retain a focused regression test or durable reproduction that would fail without it.

10. **Diagnose failures with evidence, not retries.** Preserve the request/response details, browser console/network evidence, relevant server-safe logs, and exact steps without recording secrets. Reduce to the smallest reproducible path. Rank a few falsifiable hypotheses, change one variable per probe, and determine whether the cause is browser behavior, client integration, server contract, authorization/validation, test harness, or unavailable infrastructure. Remove temporary instrumentation after diagnosis. Do not weaken assertions, disable security controls, add blind retries, or hide the error to obtain a passing result.

## Completion evidence

Report only what was observed:

- changed user contract, browser/server boundaries, and intentionally excluded framework or design decisions;
- semantic, keyboard/focus, responsive, and state behavior exercised;
- server-side authentication, authorization, validation, and sensitive-data handling verified or explicitly outside the available evidence;
- targeted test and browser/integration commands or manual steps, their results, and environment prerequisites;
- baseline and follow-up performance evidence when performance changed, or why measurement was not relevant;
- skipped, blocked, inconclusive, or pre-existing failures, with the smallest safe next action.

Stop when the requested journey has direct evidence at the affected boundaries. Do not broaden the change into a framework migration, design redesign, generic cleanup, or unmeasured optimization.
