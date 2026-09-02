# Authoring workflow

Read this before turning a task area into instructions, examples, references, or templates.

## Start from evidence

Collect representative tasks and artifacts: inputs, desired outputs, existing successful examples, error traces, user corrections, and project-specific constraints. Define one coherent job for the skill. If the job contains distinct workflows that activate independently, split them rather than making activation load unrelated material.

## Turn evidence into usable instructions

Prioritize information an otherwise capable agent is unlikely to infer correctly:

- local conventions, prerequisites, and required evidence;
- decision rules and safe defaults;
- known failure modes and recovery actions;
- exact commands, templates, or checklists that prevent recurring errors.

Use imperative steps in execution order. State when to read a reference or run a helper, and keep the normal path visible. Make strict rules explicit where error is costly; allow judgment where tasks genuinely vary. A short, realistic example is useful only when it disambiguates a decision.

Do not restate generic domain knowledge, add unverified promises, or bury a critical constraint in an optional reference. Keep heavyweight or rare detail out of `SKILL.md` until a task condition requires it.

## Improve with failures

Review traces and final artifacts, not just a passing exit status. Convert repeated failures into a focused instruction, guardrail, example, or deterministic check. Preserve a regression case for each confirmed failure. Remove instructions that agents do not need or that conflict with observed successful practice.

## Source basis

- [Skill creation best practices](https://agentskills.io/skill-creation/best-practices) (authoritative source supplied for this skill; checked 2026-09-01)
