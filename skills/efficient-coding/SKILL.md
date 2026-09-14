---
name: efficient-coding
description: Make the smallest correct maintainable code change; use when implementing, modifying, or behavior-preservingly refactoring a bounded feature, fix, or integration without needing broad planning, language mechanics, or test-framework setup.
---

# Efficient Coding

Use this skill to turn a bounded code request into the smallest change that satisfies its observable contract. Keep correctness and maintainability together: clear conventional code is a delivery requirement, not optional polish.

Do not use this as the primary workflow for architecture exploration, a multi-slice implementation plan, language or framework instruction, test-framework setup, or broad test-suite work. Use `efficient-planning` when the work needs a risk-proportionate plan. Use `efficient-testing` to choose and run focused unit or regression evidence. If a reported failure has no known cause or reliable reproduction, use `problem-solving` before choosing a fix.

## Workflow

1. **Set the change envelope.** Read the request, the owning code path, its callers or consumers, nearby tests, and applicable local instructions and configuration. State the intended input, observable result, errors, side effects, ordering, compatibility constraints, and acceptance evidence. Name the files or boundaries that must change. Treat everything else as out of scope unless evidence makes it necessary.
   - For a behavior-preserving refactor, preserve all observable results, errors, side effects, ordering, and supported interfaces.
   - If the contract is missing, contradictory, or depends on unavailable access, do not guess. Ask for the smallest clarifying fact or report the exact blocker and the safe unchanged state.

2. **Adopt the local shape.** Inspect the closest analogous implementation rather than importing a personal pattern. Match established names, module boundaries, error handling, data ownership, and validation style when they serve the same responsibility. Keep existing invariants explicit. Do not alter an interface solely to make the implementation look uniform.

3. **Choose the direct design.** Put the change at the narrowest boundary that owns the behavior. Prefer one straightforward path with named intermediate values, clear guard clauses, and explicit error handling over indirection or compressed cleverness.
   - Keep a helper only when it names a stable concept, removes meaningful repeated logic, or isolates a real boundary.
   - Add a type, layer, configuration option, callback, or generalization only for a present requirement that the direct code cannot express cleanly. State that requirement before adding it.
   - Reuse an existing dependency or platform capability when it fits. Add a dependency only when it supplies a required capability unavailable locally and its operational, security, upgrade, and maintenance cost is justified by that requirement.

4. **Make one cohesive change.** Edit only the code, configuration, or documentation required by the envelope. Retain validation, authorization, resource cleanup, error propagation, and observable sequencing unless the request explicitly changes them. Keep closely coupled readability cleanup only when it makes the changed behavior easier to understand; leave unrelated cleanup out of the diff.
   - When a proposed edit expands ownership, changes a public contract, duplicates a rule, or crosses a new subsystem, stop and re-evaluate the envelope. Split it, obtain approval, or use the existing boundary instead.
   - When changing a bug with a confirmed cause, modify the cause rather than masking its symptom. Do not add retries, suppress errors, or introduce a fallback merely to make a check pass.

5. **Optimize only from evidence.** Do not trade clarity for hypothetical performance. When performance is an acceptance condition or a regression is observed, record a baseline for a representative workload and environment, identify the measured bottleneck, and change one relevant factor. Compare the same measurement after the change, including any memory, latency, throughput, or write-cost trade-off that matters. Revert an optimization that lacks a demonstrated benefit or makes the code materially harder to maintain.

6. **Verify the actual contract.** Review the diff against the envelope: check normal results, required failures, side effects, ordering, compatibility, and local conventions. Run the least expensive existing check that directly reaches the changed behavior, then broader relevant checks only when shared code, configuration, dependencies, or project policy make them necessary. For changed behavior or a confirmed defect, use `efficient-testing` for focused evidence.
   - If a check fails, classify it before editing again: product defect, incorrect expectation, regression, environment or access problem, or unrelated baseline failure. Preserve the useful output. Fix the identified cause; do not weaken assertions or repeatedly rerun an unchanged failing command.
   - If a required check is blocked, report the command, blocker, affected acceptance condition, and smallest safe next action. Do not report it as passed.

7. **Finish with inspectable evidence.** Report the completed acceptance conditions, changed files and their purpose, commands run and results, checks skipped or blocked, and remaining risks or assumptions. Stop when every in-scope condition has direct evidence; do not add speculative cleanup, abstraction, dependency, or optimization work.

## Decision checks

Before accepting the change, answer these questions from the diff and evidence:

- Does each changed line support a stated acceptance condition, safety requirement, or necessary local convention?
- Is the control flow understandable without reconstructing hidden state or future extension points?
- Does every new interface, abstraction, configuration surface, or dependency solve a present problem better than direct code?
- Did verification reach the behavior changed, including required error and side-effect paths?
- If performance changed, does an equivalent before-and-after measurement show that the trade-off is worthwhile?

If any answer is no or unknown, reduce the change, gather the missing evidence, or leave the affected part unchanged and report the limit.
