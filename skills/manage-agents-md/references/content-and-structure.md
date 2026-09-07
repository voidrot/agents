# Content and Structure for AGENTS.md

Use this reference after discovery, when deciding what an instruction file should say or whether a proposed statement is supported. It does not replace the main skill's pre-action safety rules.

## Build an evidence ledger before drafting

For each candidate instruction, record enough evidence to make a later edit reviewable:

| Candidate statement | Evidence source | Applies under | Status | Action |
| --- | --- | --- | --- | --- |
| Exact command and required directory | Script, CI job, package task, or existing maintained documentation | Relevant path or repository root | Verified / `UNCONFIRMED` | Add, correct, omit, or escalate |
| Local convention or invariant | Representative implementation, test, configuration, or explicit maintainer guidance | Defined subtree | Verified / `UNCONFIRMED` | State with scope or keep out |
| Instruction-file relationship | Explicit platform/repository policy or file text | Named agents and paths | Verified / `UNCONFIRMED` | Cross-reference, preserve, or ask |

A source is not proof merely because it exists. For example, a package manifest entry may establish a command name but not its expected outcome in every directory. A stale README may not establish the current workflow. Keep the source location and the limitation with the claim.

## Choose content by task value

Include information an agent is unlikely to learn safely from the immediate task:

- the file or subsystem map needed to begin work;
- non-obvious invariants, safety boundaries, ownership boundaries, or generated-file rules;
- a verified workflow command with the directory, prerequisite, and evidence it supplies;
- a decision point, such as when a change needs a migration, a specific test layer, or a maintainer decision;
- a pointer to a local `AGENTS.md`, workflow skill, or detailed canonical document when its scope is known.

Do not fill the file with generic language advice, an exhaustive technology inventory, a prose copy of the README, all available tools, or rules that can be derived reliably from nearby configuration. A root file is navigation and shared constraints, not a giant manual.

## Concise baseline, adapted rather than copied

Use only the sections that the repository evidence supports. Existing human-authored headings take precedence over this shape.

```markdown
# Repository guidance

## Scope and map
- State the paths this file covers and point to key source, test, and documentation locations.

## Verified workflows
- For each action, give the exact command, working directory, prerequisite, and what result to inspect.

## Shared non-obvious rules
- State only cross-cutting invariants, safety boundaries, and decisions that apply here.

## More specific guidance
- Link to a nested instruction file or canonical reference, naming the subtree or task it covers.
```

A nested file can omit the map and repeat only the minimum parent context needed to avoid ambiguity. A focused file may instead begin with a warning, a verification sequence, or an exception to a shared rule. Do not force empty headings or a generated timestamp.

## Write claims so they can be checked

Prefer bounded language tied to evidence:

- Name the affected path: “Under `path/to/subtree`, …” rather than “always …”.
- Name the source of truth: “Use the command defined in `<source>` …” when that source is verified.
- Include the condition and failure boundary: “If this check fails, stop before …” when supported by project policy.
- Preserve exact command syntax. Record its working directory, required environment or generated inputs, and expected artifact or exit condition when known.

If any of those facts are missing, use `UNCONFIRMED: <fact>; verify with <source or owner>` or leave the statement out. Do not invent version numbers, defaults, test coverage, supported platforms, or success guarantees.

## Keep procedure detail discoverable

The root can point to a stable, scoped reference instead of duplicating it. A pointer is useful only when an agent can identify when to follow it and reach the target locally. Before adding one, verify:

1. the target exists and its path is relative to the document that links it;
2. its owner and scope are clear enough to avoid implying universal applicability; and
3. it adds material local procedure, rationale, or safety detail rather than restating the parent.

For tasks that benefit from reusable workflow skills, point to the smallest verified set—normally about one to three. Do not make several skills appear mandatory when their task boundaries overlap.

## Review questions

Before retaining a paragraph, ask:

- What decision or mistake does this prevent?
- What evidence establishes it, and for which files or agents?
- Is this the narrowest scope that remains true?
- Is another file the canonical owner of the detail?
- Can an agent validate the path and command without guessing?

If those questions cannot be answered, label the fact `UNCONFIRMED` or escalate instead of adding confident prose.
