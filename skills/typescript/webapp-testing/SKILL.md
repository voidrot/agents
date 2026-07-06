---
name: webapp-testing
description: Use when testing or debugging web applications with Playwright or browser automation, including user flows, screenshots, console logs, forms, and regression checks.
---

# Web Application Testing

Use when testing or debugging web applications with Playwright or browser automation, including user flows, screenshots, console logs, forms, and regression checks.

## Workflow

1. Confirm the framework, package manager, runtime versions, and constraints before applying patterns.
2. Open only the supporting reference that matches the task; avoid loading the whole reference set by default.
3. Prefer the smallest idiomatic change that preserves existing architecture and public behavior.
4. Validate with the project’s relevant type checks, tests, linting, build, or browser checks.

## Supporting Material

- Read `references/full-guidance.md` for the migrated long-form guidance, examples, and checklists from the source skill.
- Read `references/browser-qa.md` for focused browser qa guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/playwright-generate-test.md` for focused playwright generate test guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/playwright-explore-website.md` for focused playwright explore website guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/playwright-automation-fill-in-form.md` for focused playwright automation fill in form guidance; related prefixed files in `references/` contain deeper examples.
- Use templates or static support files in `assets/` when the workflow calls for them.

Keep this `SKILL.md` as the concise activation and routing entry point; put long examples, matrices, and reusable snippets in `references/`.
