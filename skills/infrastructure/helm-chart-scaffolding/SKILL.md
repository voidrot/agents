---
name: helm-chart-scaffolding
description: Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments.
---

# Helm Chart Scaffolding

Use this skill when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments.

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
- `references/chart-structure.md` — detailed chart structure guidance.
- `references/details.md` — detailed details guidance.

## Assets
- `assets/Chart.yaml.template` — template or static resource to copy and adapt.
- `assets/values.yaml.template` — template or static resource to copy and adapt.

## Scripts
- `scripts/validate-chart.sh` — helper script; inspect header/options before running.
