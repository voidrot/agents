---
name: bats-testing-patterns
description: Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities.
---

# Bats Testing Patterns

Use this skill when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities.

## Workflow

1. Identify the target environment, tool version, and operational constraints.
2. Inspect existing repository configuration before proposing new files or commands.
3. Apply the smallest safe change or produce a concrete implementation plan.
4. Validate with the relevant non-interactive command, linter, dry run, or review checklist.
5. Report assumptions, risks, and follow-up tasks clearly.

## Safety Rules

- Prefer official documentation for version-specific syntax and behavior.
- Keep generated configuration minimal, reproducible, and project-specific.
- Call out destructive commands, credential handling, and production-impacting changes before use.

## Supporting Material
- `references/details.md` — detailed details guidance.
- `references/source-guide.md` — detailed source guide guidance.
