---
name: k8s-manifest-generator
description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations.
---

# Kubernetes Manifest Generator

Use this skill when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations.

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
- `references/deployment-spec.md` — detailed deployment spec guidance.
- `references/details.md` — detailed details guidance.
- `references/service-spec.md` — detailed service spec guidance.

## Assets
- `assets/configmap-template.yaml` — template or static resource to copy and adapt.
- `assets/deployment-template.yaml` — template or static resource to copy and adapt.
- `assets/service-template.yaml` — template or static resource to copy and adapt.
