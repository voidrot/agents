---
name: memory-safety-patterns
description: Use when designing, reviewing, or debugging code for memory-safety risks such as ownership errors, lifetime bugs, use-after-free, double-free, buffer overflow, unsafe pointer use, resource leaks, or concurrency-related memory hazards.
---

# Memory Safety Patterns

Use this skill as the activation and routing layer for memory safety patterns work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Identify the language/runtime memory model, unsafe boundaries, FFI, concurrency, and resource ownership points.
2. Trace allocation, ownership transfer, borrowing, mutation, cleanup, and error paths.
3. Prefer language-level safety constructs, RAII/defer/finalizers as appropriate, bounds-checked APIs, defensive copies, and explicit lifetime ownership.
4. Review unsafe blocks, manual memory management, pointer arithmetic, buffer sizes, and aliasing assumptions with extra evidence.
5. Return concrete risks, safer patterns, tests/fuzzing targets, and residual unsafe assumptions.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for cross-language examples and pattern details.
- references/quick-reference.md for the original concept overview.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
