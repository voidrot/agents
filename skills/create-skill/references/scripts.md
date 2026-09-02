# Script design and safety

Read this before adding, changing, or approving a helper script.

## Use scripts sparingly

Write a helper only for a repeated deterministic operation—such as scaffolding, format conversion, static validation, or a stable extraction. Keep reasoning, choices, and task-specific adaptation in the instructions. Do not hide an interactive or judgment-heavy workflow behind a command.

## Required operating properties

A helper should:

- run noninteractively and document its inputs with `--help`;
- emit machine-readable results on stdout (or offer a JSON mode) and diagnostics on stderr;
- use actionable nonzero exit codes;
- resolve documented relative paths predictably;
- bound output and avoid printing sensitive data;
- be idempotent where practical and safe by default;
- provide dry-run behavior or require explicit confirmation for destructive work;
- document any non-stdlib dependency, its version expectation, and installation path.

Refuse to overwrite existing user files unless the caller makes an explicit, narrowly scoped choice. Validate inputs before writing. Do not make network access, package installation, or environment mutation an implicit side effect.

## Bundled helpers

The helpers in `../scripts/` require Python 3 and the standard library only. Run them from any working directory by passing an explicit skill path. `scaffold_skill.py` creates `SKILL.md` and `references/authoring.md` only in a nonexistent or empty target; it cleans up artifacts from a failed write and refuses a non-empty target. `validate_skill.py` reads the target without modifying it. Both provide `--help`, use `--json` for a structured stdout result, and send diagnostics to stderr.

Exit codes are `0` for success, `1` for validation or filesystem failure, `2` for command-line usage, `3` when scaffolding refuses an unsafe target, and `4` for an invalid scaffold name or description.

## Review checklist

- Is the task deterministic enough to automate?
- Can a caller learn usage without reading source?
- Does a failed invocation say what to fix?
- Does the default preserve existing work?
- Can automated callers parse success and failure output?
- Are filesystem paths contained in the intended root?
- Can the command be rerun safely?

## Source basis

- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts) (authoritative source supplied for this skill; checked 2026-09-01)
