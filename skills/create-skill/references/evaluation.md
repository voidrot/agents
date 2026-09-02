# Evaluation design

Read this before creating a suite, interpreting results, or claiming a skill is effective.

## Measure two different things

**Routing evaluation** asks whether a runtime discovers or loads a skill for a prompt. It is suited to the description and native runtime behavior. In this repository, use `uv run skill-eval native-route RUNTIME SKILL_DIR --suite ROUTING.yaml` for that narrow question. A routing result is not evidence that the skill improves task completion.

**Task-quality evaluation** asks whether the full skill improves a task outcome compared with an explicit baseline. Hold task, fixtures, capability profile, model settings, limits, and grader constant; vary only the skill condition. Use paired cases and record successes, failures, traces, and grades. In this repository, use `uv run skill-eval evaluate SKILL_DIR --suite SUITE.yaml` when a suitable suite and configured execution environment exist.

`docs/planning.md` describes the repository's intended distinction: `native-route` is runtime compatibility/discovery testing, while `evaluate` is the primary portable paired task-quality workflow.

## Build credible evidence

1. Add deterministic checks first: frontmatter, paths, required outputs, schema validity, and other stable artifact checks.
2. Build cases from real tasks and failures. Separate approximately 60% train cases from 40% validation cases; keep the holdout blinded while revising.
3. Run multiple repetitions for non-deterministic models or graders. Pair conditions by case and repetition rather than comparing unrelated aggregates.
4. Inspect traces to explain failures, then add focused regressions.
5. Select a candidate on validation evidence and confirm it on unseen cases. Report the suite, baseline, conditions, repetitions, failures, and limits alongside any result.

Do not convert infrastructure failures, timeouts, invalid outputs, or unavailable tools into ordinary negative grades. Preserve and report them separately.

## Iterate safely

Route failures point first to the description and runtime integration; task failures point first to instructions, references, examples, or tools. `skill-eval enhance` may produce a reviewable candidate after an experiment, but safe application remains separate and explicit. Never imply general performance from one model, one runtime, or training cases alone.

## Source basis

- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) (authoritative source supplied for this skill; checked 2026-09-01)
- `docs/planning.md` (repository guidance inspected for this skill)
