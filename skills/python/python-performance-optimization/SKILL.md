---
name: python-performance-optimization
description: Profile Python bottlenecks and apply measured CPU, memory, and I/O optimizations.
---

# Python Performance Optimization

## When to use

- diagnosing slow Python code, high memory use, or production performance symptoms
- choosing profiling tools and benchmark methods before optimizing
- reviewing proposed optimizations for evidence and regressions

## Workflow

1. Define the user-visible performance goal and baseline.
2. Measure before changing code; separate CPU, memory, I/O, database, and concurrency symptoms.
3. Make one optimization at a time and keep correctness tests green.
4. Re-measure with the same workload and record the delta.
5. Prefer algorithmic/data-access fixes before micro-optimizations.

## Constraints

- Do not optimize from intuition alone.
- Keep benchmark commands reproducible and non-interactive.
- Move profiling recipes and tool matrices to references.

## References

- [profiling examples](references/details.md)
- [advanced optimization patterns](references/advanced-patterns.md)
- [moved performance guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
