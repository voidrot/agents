---
name: efficient-e2e-testing
description: Implement and diagnose behavior-focused browser end-to-end tests for critical user journeys when browser integration, isolation, artifacts, CI boundaries, or flakes need focused evidence; excludes runner installation, broad coverage goals, unit/API test design, and bulk suite rewrites.
---

# Efficient E2E Testing

Use this skill to add, update, run, or diagnose a small number of browser-level tests that prove a critical user journey through real rendered application boundaries. Test what a user can do and observe, not component internals, implementation sequencing, or runner behavior.

Do not use this skill to install or select a runner, add dependencies, set broad coverage targets, design unit or API tests, or rewrite a suite wholesale. Use `efficient-testing` for focused non-browser regression evidence. Use `efficient-web-development` when the browser-facing behavior itself needs implementation or repair, and `efficient-react` for React component ownership or rendering work.

## Workflow

1. **Establish the journey and existing harness.** Read the request, acceptance criteria or defect report, affected route and user-visible states, closest browser tests, test configuration, CI definition, and documented local prerequisites. State the actor, entry condition, meaningful user actions, expected visible outcomes, and the server effects that the browser must reach. Select the smallest critical path that proves the requested behavior; include an error, recovery, authorization, or alternate-browser case only when the requirement, incident, or changed boundary requires it. Follow the repository's installed runner and supported browser matrix; do not introduce a runner, a dependency, or runner-specific conventions.

2. **Make test identity, authentication, and data safe.** Use a dedicated non-production environment and accounts created for automated testing. Obtain credentials from the established secret mechanism; never commit, print, screenshot, or encode passwords, session cookies, tokens, personal data, or production identifiers. Prefer API-, database-, or fixture-based setup only through existing test-only, authorized boundaries; otherwise create data through the same UI path when setup behavior is itself under test. Give every test unique, traceable disposable data and isolate tenant, user, storage, cookie, download, and server-side state from concurrent tests. Clean up with an authorized test-only mechanism even after failure when possible. Do not use production accounts, services, or data; do not run destructive mutations against production, shared staging data, or resources not created by the test. If safe isolation is unavailable, stop and report the missing boundary rather than weakening safeguards.

3. **Interact as a user with resilient locators.** Prefer accessible role plus accessible name, associated labels, visible text when it is the intended product contract, and stable domain identifiers where accessibility cannot distinguish equivalent controls. Assert locator uniqueness before relying on it. Avoid CSS classes, DOM position, generated IDs, implementation-only attributes, and broad text matching that can select unrelated content. Request a small, semantic test hook only when the UI has no stable accessible or domain-level identity; keep it stable and scoped to the user-facing element, not a component implementation detail. Drive the journey through navigation, keyboard, pointer, form, and browser behavior that a user would use. Assert visible content, accessible state, URL/history behavior, downloaded result, or durable authorized outcome—not private state or arbitrary request counts.

4. **Synchronize on observable state, never elapsed time.** Before each action and assertion, identify the condition that makes the next step valid: a page/route has rendered, a control is enabled, a dialog is exposed, a request-backed status is resolved, navigation has completed, or the expected result is visible. Use the installed runner's condition-aware navigation, locator, assertion, network-idle, or event primitives where they express that condition. Tie waits to the specific user operation and its observable result; do not use fixed sleeps, blind polling, unconditional retries, or oversized global time limits. When an external dependency makes the journey nondeterministic, use the existing test environment's controlled substitute only if the product contract at that boundary remains represented; otherwise classify the dependency as a blocker or integration failure.

5. **Keep browser boundaries explicit.** Run locally only against the supported application command, base URL, browser binaries, services, and environment variables; record each prerequisite. Treat browser permissions, multiple tabs/windows, downloads, uploads, cross-origin redirects, email/SMS/payment providers, third-party widgets, and native dialogs as distinct boundaries. Exercise them only when required by the journey and use established test environment mechanisms rather than real external accounts or irreversible actions. Do not bypass authentication, authorization, CSRF, origin, or browser security controls merely to make a test pass. If browser behavior differs by engine, viewport, operating system, headless mode, or CI network policy, identify the supported matrix and target the affected boundary rather than assuming local behavior proves CI or every browser.

6. **Run proportionately and preserve evidence.** First run the narrowest supported test or project selection for the changed journey in the relevant browser mode. Rerun after a relevant change. Run the required browser projects or a broader relevant group only when repository policy, shared harness changes, or the affected browser boundary warrants it. On failure, retain the runner report and relevant trace, screenshot, video, console output, browser/network logs, response metadata, and server-safe logs according to project retention policy. Redact or restrict artifacts that could contain credentials, tokens, personal data, or sensitive business data. Do not claim a browser or CI result that was not run.

7. **Diagnose from the failing artifact and classify flakes.** Reproduce with the same test, browser project, commit, data setup, and environment when safe. Compare the expected and actual visible state, the action timeline, console errors, network requests/responses, trace timing, and screenshot rather than adding retries. Classify the result before changing code:
   - **Product defect:** the application reaches an incorrect user-visible or authorized outcome under valid test conditions.
   - **Incorrect test expectation or locator:** the product contract differs from the assertion, or the locator selects the wrong/ambiguous element.
   - **Test-data or isolation leak:** shared, stale, missing, unauthorized, or cleanup-failed data changes the precondition.
   - **Synchronization defect:** the test advances before its specific observable readiness condition, or the application exposes a genuine race that users can encounter.
   - **Environment or infrastructure failure:** unavailable browser binary, application/service startup, DNS/network, certificate, resource exhaustion, CI permission, or third-party sandbox failure prevents a valid run.
   - **Browser/CI-specific incompatibility:** the same supported journey differs by browser engine, headless/CI execution, viewport, OS, or configured policy.
   - **Unclassified flake:** intermittent failure without enough repeatable evidence; preserve the artifacts and conditions, quarantine only under established policy, and report it without masking it with retries or relaxed assertions.

   Change one falsifiable cause at a time, then rerun the smallest affected journey. Fix product, isolation, locator, or synchronization causes at their owning boundary. Do not hide a failure with arbitrary delays, blanket retries, selector broadening, disabled assertions, or a production-only exception.

## Completion evidence

Report only observations obtained:

- journey, actor, preconditions, user actions, and visible/durable outcomes covered, plus intentionally excluded states;
- test location, supported runner/browser project used, exact command, and pass/fail result;
- test account and data-isolation approach, cleanup result, and any safe setup boundary used;
- synchronization conditions and locator strategy for material interactions;
- browser/CI prerequisites, projects actually run, and boundaries not exercised;
- retained diagnostic artifacts and any redaction or access restriction applied;
- for a failure or flake, its classification, supporting evidence, rerun result if obtained, and smallest safe next action.

Stop when the requested critical journey has direct browser evidence. Do not expand it into coverage maximization, a runner migration, a test-suite rewrite, or destructive production verification.
