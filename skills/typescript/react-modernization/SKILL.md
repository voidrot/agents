---
name: react-modernization
description: Use when modernizing React applications, upgrading React versions, migrating class components or legacy APIs, adopting React 18/19 features, or resolving upgrade regressions.
---

# React Modernization

Use when modernizing React applications, upgrading React versions, migrating class components or legacy APIs, adopting React 18/19 features, or resolving upgrade regressions.

## Workflow

1. Confirm the framework, package manager, runtime versions, and constraints before applying patterns.
2. Open only the supporting reference that matches the task; avoid loading the whole reference set by default.
3. Prefer the smallest idiomatic change that preserves existing architecture and public behavior.
4. Validate with the project’s relevant type checks, tests, linting, build, or browser checks.

## Supporting Material

- Read `references/full-guidance.md` for the migrated long-form guidance, examples, and checklists from the source skill.
- Read `references/details.md` for additional details guidance.
- Read `references/react18-batching-patterns.md` for focused react18 batching patterns guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react18-dep-compatibility.md` for focused react18 dep compatibility guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react18-enzyme-to-rtl.md` for focused react18 enzyme to rtl guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react18-legacy-context.md` for focused react18 legacy context guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react18-lifecycle-patterns.md` for focused react18 lifecycle patterns guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react18-string-refs.md` for focused react18 string refs guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react19-concurrent-patterns.md` for focused react19 concurrent patterns guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react19-source-patterns.md` for focused react19 source patterns guidance; related prefixed files in `references/` contain deeper examples.
- Read `references/react19-test-patterns.md` for focused react19 test patterns guidance; related prefixed files in `references/` contain deeper examples.

Keep this `SKILL.md` as the concise activation and routing entry point; put long examples, matrices, and reusable snippets in `references/`.
