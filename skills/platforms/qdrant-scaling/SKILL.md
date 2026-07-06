---
name: qdrant-scaling
description: Guides Qdrant scaling decisions. Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node', 'need more throughput', 'cluster is slow', 'too many tenants', 'vertical or horizontal', 'how to shard', or 'need to add capacity'.
---

# Qdrant Scaling

Use this skill for qdrant scaling tasks where platform-specific implementation, architecture, or operational guidance is needed.

## When to Use

- Guides Qdrant scaling decisions.

## Workflow

1. Clarify the concrete goal, constraints, and current project context.
2. Choose the smallest platform-specific pattern that solves the task.
3. Route to supporting references only when detailed guidance is needed.

## Constraints

- Prefer current official documentation for version-sensitive APIs, commands, deployment options, and configuration names.
- Keep generated guidance actionable and scoped to the user's project rather than restating broad background material.
- Preserve security, privacy, reliability, and rollback concerns when recommending platform changes.

## Supporting Material

- Read `references/minimize-latency.md` when its focused details are relevant.
- Read `references/scaling-data-volume/horizontal-scaling.md` when its focused details are relevant.
- Read `references/scaling-data-volume/sliding-time-window.md` when its focused details are relevant.
- Read `references/scaling-data-volume/tenant-scaling.md` when its focused details are relevant.
- Read `references/scaling-data-volume/vertical-scaling.md` when its focused details are relevant.
- Read `references/scaling-data-volume.md` when its focused details are relevant.
- Read `references/scaling-qps.md` when its focused details are relevant.
- Read `references/scaling-query-volume.md` when its focused details are relevant.

## Expected Output

- A concise recommendation, implementation plan, review, or diagnostic report with assumptions, tradeoffs, and verification steps.
