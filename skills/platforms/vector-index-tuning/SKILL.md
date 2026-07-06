---
name: vector-index-tuning
description: Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure.
---

# Vector Index Tuning

Use this skill for vector index tuning tasks where platform-specific implementation, architecture, or operational guidance is needed.

## When to Use

- Tuning HNSW parameters.
- Implementing quantization.
- Optimizing memory usage.
- Reducing search latency.

## Workflow

1. Establish baseline latency, recall, memory, and indexing costs before changing parameters.
2. Tune HNSW, quantization, payload indexes, and replicas with one variable at a time.
3. Document rollback criteria and measurement methodology for every tuning change.

## Constraints

- Prefer current official documentation for version-sensitive APIs, commands, deployment options, and configuration names.
- Keep generated guidance actionable and scoped to the user's project rather than restating broad background material.
- Preserve security, privacy, reliability, and rollback concerns when recommending platform changes.

## Supporting Material

- Read `references/full-guidance.md` for source guidance, examples, checklists, and detailed patterns.
- Read `references/details.md` when its focused details are relevant.

## Expected Output

- A concise recommendation, implementation plan, review, or diagnostic report with assumptions, tradeoffs, and verification steps.
