---
name: k8s-security-policies
description: Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when securing Kubernetes clusters, implementing network isolation, or enforcing pod security standards.
---

# Kubernetes Security Policies

Use this skill when securing Kubernetes clusters, implementing network isolation, or enforcing pod security standards.

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
- `references/rbac-patterns.md` — detailed rbac patterns guidance.
- `references/source-guide.md` — detailed source guide guidance.

## Assets
- `assets/network-policy-template.yaml` — template or static resource to copy and adapt.
