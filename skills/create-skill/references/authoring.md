# Authoring workflow

Read this before turning a task area into instructions, examples, references, or templates.

## Start from evidence

Collect representative tasks and artifacts: inputs, desired outputs, existing successful examples, error traces, user corrections, and project-specific constraints. Inspect adjacent skill names and descriptions before defining one coherent job; adding a new skill is not automatically the right answer.

## Set the right boundary

Treat the skill like a well-scoped function:

- **Split** when workflows are useful independently and materially differ in triggers, safety boundaries, tools, or validation.
- **Merge** when trigger descriptions substantially overlap, the steps are normally used together, or separation repeatedly makes agents load several skills for one task.
- Keep variants and rare branches in conditional references instead of creating top-level skills solely for each variant.
- Keep atomic operations as tools or scripts; a skill explains when, why, and how to combine operations into an outcome.
- Keep broad universal policy in the harness's global instruction layer; a skill should not become a second system prompt.

Optimize for a small plausible candidate set at runtime. The research favors roughly one to three relevant skills for an ordinary task, but this is directional evidence—not a universal numerical rule. A large installed library needs retrieval or hierarchy so the model does not discriminate among many semantically similar descriptions at once.

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
