---
name: bash-defensive-patterns
description: Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety.
---

# Bash Defensive Patterns

Use this skill when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety.

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
