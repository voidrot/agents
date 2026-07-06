---
name: workflow-orchestration-patterns
description: Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determinism constraints. Use when building long-running processes, distributed transactions, or microservice orchestration.
---

# Workflow Orchestration Patterns

Use this skill for workflow orchestration patterns tasks where platform-specific implementation, architecture, or operational guidance is needed.

## When to Use

- **Multi-step processes** spanning machines/services/databases.
- **Distributed transactions** requiring all-or-nothing semantics.
- **Long-running workflows** (hours to years) with automatic state persistence.
- **Failure recovery** that must resume from last successful step.

## Workflow

1. Decide whether the process needs durable workflow orchestration or simpler async jobs.
2. Separate workflow state, activities, retries, compensation, and external side effects.
3. Check determinism, idempotency, timeout, and versioning constraints before implementation.

## Constraints

- Prefer current official documentation for version-sensitive APIs, commands, deployment options, and configuration names.
- Keep generated guidance actionable and scoped to the user's project rather than restating broad background material.
- Preserve security, privacy, reliability, and rollback concerns when recommending platform changes.

## Supporting Material

- Read `references/full-guidance.md` for source guidance, examples, checklists, and detailed patterns.
- Read `references/details.md` when its focused details are relevant.

## Expected Output

- A concise recommendation, implementation plan, review, or diagnostic report with assumptions, tradeoffs, and verification steps.
