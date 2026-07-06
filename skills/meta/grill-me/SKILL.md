---
name: grill-me
description: Stress-test a plan or design through a focused one-question-at-a-time interview before implementation.
---

# Grill Me

## When to Use

- The user asks to be grilled, challenged, or interviewed about a plan.
- A design has unresolved decisions, hidden dependencies, or risky assumptions.
- The next step should be clarity, not implementation.

## Workflow

1. Restate the plan in one or two sentences.
2. Identify the riskiest open decision or assumption.
3. Ask exactly one question at a time.
4. Give a recommended answer with the trade-off behind it.
5. Use codebase exploration instead of asking when the answer is discoverable from files.
6. Continue down dependent branches until the plan is coherent or the user stops.

## Question Style

- Be direct and specific.
- Prefer decisions over abstract discussion.
- Expose trade-offs, constraints, reversibility, and failure modes.
- Do not ask multiple questions in one turn.

## Stop Conditions

- The plan has a sequenced set of decisions with no obvious blockers.
- The remaining uncertainty requires external evidence or implementation feedback.
- The user asks to stop or switch to execution.

## Output

- Current decision map.
- Recommended next step.
- Open questions that remain genuinely unresolved.
