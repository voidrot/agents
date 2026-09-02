---
name: create-skill
description: Design, author, validate, evaluate, and iterate on Agent Skills when creating a new skill, improving an existing skill, or assessing its discoverability and task quality.
---

# Create Agent Skills

Build a small, evidence-based instruction package that helps an agent complete a coherent class of tasks. Treat routing and task completion as separate problems.

## Workflow

1. **Ground the scope.** Inspect representative user tasks, inputs, outputs, failures, and existing project conventions. Define the skill's audience, trigger boundary, required tools, risks, and completion evidence. Exclude generic knowledge and unrelated workflows.
2. **Choose the smallest useful structure.** Before creating or changing a skill directory or frontmatter, read [the structure reference](references/specification.md). Keep activation instructions in `SKILL.md`; put detailed material in one-level-deep `references/`, reusable deterministic operations in `scripts/`, and non-instruction artifacts in `assets/`.
   - To start a *new* child skill safely, run `python3 scripts/scaffold_skill.py --help`, then use it only with an empty or nonexistent destination. Do not use it to revise an existing skill.
3. **Write for execution.** Give the agent an ordered, imperative procedure with decision points, safe defaults, verification, failure handling, and only the examples or templates that prevent likely mistakes. Calibrate how prescriptive it is to the cost of error. Read [authoring guidance](references/authoring.md) when selecting procedures, examples, or resource boundaries.
4. **Engineer discovery deliberately.** Before writing or revising `description`, read [description optimization](references/descriptions.md). State both what the skill does and when it applies, using concrete task and domain terms—including likely implicit requests. Do not use the description as a keyword dump.
5. **Add helpers only when justified.** Read [script design](references/scripts.md) before adding a helper. Use a script only for repeated deterministic work; otherwise give direct instructions. Keep it noninteractive, bounded, safe by default, and independently usable with `--help`.
6. **Validate structure and links.** After every material edit, run `python3 scripts/validate_skill.py PATH_TO_SKILL`; use `--json` for automation. It is a conservative bundled check, not a replacement for a full YAML implementation or an official validator. Read [the structure reference](references/specification.md) for its limits. Where this repository's CLI is available, also run `uv run skill-eval validate PATH_TO_SKILL --strict` before packaging or evaluation.
7. **Evaluate the right outcome.** Read [evaluation guidance](references/evaluation.md) before making discoverability or quality claims. Use routing cases to test whether a native runtime selects/loads the skill; use paired, controlled task cases to measure whether the full skill improves completion. Keep train/validation cases separate, run multiple trials, inspect traces and failures, then confirm on unseen cases. Use `uv run skill-eval native-route RUNTIME PATH_TO_SKILL --suite ROUTING.yaml` only for runtime routing, and `uv run skill-eval evaluate PATH_TO_SKILL --suite SUITE.yaml` for task quality.
8. **Iterate without overclaiming.** Change the description for routing failures; change instructions, references, or tools for execution failures. Add regressions for observed failures, revalidate, and retain the smallest revision supported by holdout evidence. If using `skill-eval enhance`, review its candidate and evaluation record; it does not justify overwriting a skill without the separate explicit apply step.

## Completion checklist

- [ ] The directory and frontmatter meet the formal requirements.
- [ ] The description says what and when, with a bounded scope.
- [ ] Instructions cover real task decisions, verification, and meaningful failure modes.
- [ ] Resources are necessary, relative, and reachable without leaving the skill root.
- [ ] Helpers are deterministic and safe, or have been removed.
- [ ] Static validation passes; routing and task-quality evidence are reported separately when evaluated.
- [ ] Claims identify the evidence used and any untested runtime or model assumptions.

## References

- [Formal structure and validation limits](references/specification.md) — read before layout/frontmatter work or interpreting the bundled validator.
- [Description optimization](references/descriptions.md) — read before designing or tuning discovery text.
- [Authoring workflow](references/authoring.md) — read before drafting detailed procedures, examples, and resource boundaries.
- [Evaluation design](references/evaluation.md) — read before defining suites or reporting effectiveness.
- [Script design and safety](references/scripts.md) — read before adding or reviewing helper scripts.
