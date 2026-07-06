---
name: react-audit-grep-patterns
description: Use when auditing React codebases with targeted search patterns for deprecated APIs, React 18/19 migration risks, dependency issues, or test modernization work.
---

# React Audit Grep Patterns

Use when auditing React codebases with targeted search patterns for deprecated APIs, React 18/19 migration risks, dependency issues, or test modernization work.

## Workflow

1. Confirm the framework, package manager, runtime versions, and constraints before applying patterns.
2. Open only the supporting reference that matches the task; avoid loading the whole reference set by default.
3. Prefer the smallest idiomatic change that preserves existing architecture and public behavior.
4. Validate with the project’s relevant type checks, tests, linting, build, or browser checks.

## Supporting Material

- Read `references/full-guidance.md` for the migrated long-form guidance, examples, and checklists from the source skill.

Keep this `SKILL.md` as the concise activation and routing entry point; put long examples, matrices, and reusable snippets in `references/`.
