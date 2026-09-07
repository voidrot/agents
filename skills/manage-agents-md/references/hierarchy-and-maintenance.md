# Hierarchy and Maintenance

Use this reference when instruction files overlap, a subtree may need its own `AGENTS.md`, or existing guidance may be stale. The main skill's rules still apply: establish applicability from evidence, preserve human intent, and stop when authority is unclear.

## Map applicability before changing files

For each candidate source, record:

| Source | Location | Claimed audience/tool | Path scope | Explicit ordering or override text | Overlap | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `AGENTS.md` or nested file | Actual path | What the file itself says | Directory/subtree it names, if any | Exact statement, if present | Named related files | Verified / `UNCONFIRMED` |
| `CLAUDE.md` or analogous file | Actual path | What the file itself says | Directory/subtree it names, if any | Exact statement, if present | Named related files | Verified / `UNCONFIRMED` |
| Platform, repository, or user policy | Actual source | Named agent/runtime | Declared scope | Exact statement | Affected files | Verified / `UNCONFIRMED` |

Search for recognizable instruction files and repository policy, but do not treat every match as active guidance. The filename alone does not prove precedence, audience, scope, or compatibility. If an agent runtime defines resolution rules, use its documented behavior; otherwise report the uncertainty rather than asserting a hierarchy.

## Decide whether to add a nested AGENTS.md

Keep a single root file when the proposed nested file would only repeat shared commands, conventions, or repository map entries. Add or retain a nested file only when at least one material difference is established:

| Material difference | Suitable local content |
| --- | --- |
| Scope | A limited directory map or local ownership boundary |
| Convention | A format, naming, generation, or architecture rule that differs from the parent |
| Safety | A local prohibition, sensitive boundary, or required review/validation step |
| Workflow | A distinct verified command sequence, prerequisite, or failure handling procedure |

Place it at the narrowest directory that truly owns the difference. State the subtree it covers and link to parent or sibling guidance only when the actual resolution model makes that safe. Do not create one file per package, language, or tool just for symmetry.

## Reconcile parallel instruction files

`AGENTS.md`, `CLAUDE.md`, editor-rule files, contributor guidance, and tool configuration can all contain useful context. They need not serve the same audience or resolve conflicts in the same order.

For overlapping statements, classify before editing:

- **Compatible:** both say the same thing within their own declared scopes. Preserve them unless duplication creates a maintenance burden.
- **Complementary:** each supplies different, non-conflicting detail. Keep the canonical detail with its owner and add a narrow pointer only if it helps an applicable agent.
- **Duplicated:** wording or commands are materially the same. Prefer one verified canonical source and a pointer, but do not delete human-authored duplicate text without confirmation that the other source is intended to govern the same audience.
- **Stale:** the path, command, version, workflow, or claim is disproved by current repository evidence. Correct it narrowly and retain any necessary rationale elsewhere.
- **Conflicting:** statements cannot both be followed for the same target. Apply an explicit documented ordering only if it exists and applies. Otherwise stop and ask the owner which source governs.

Never bulk-copy, bulk-delete, or “sync” parallel files. A cross-reference should say what it covers, not imply equal precedence: for example, “For the documented release workflow, see `<relative path>`; applicability to this agent is `UNCONFIRMED`.” Use that form only when the target and scope are verified.

## Prune stale guidance safely

Pruning is a content decision, not a formatting pass.

1. List each candidate removal and its stated purpose.
2. Verify the referenced path, command, tool, configuration, or policy against current repository evidence. Check whether another instruction file depends on the text or points to it.
3. Decide whether to remove, update, relocate, retain with `UNCONFIRMED`, or escalate. Preserve human explanations where their factual status or intended audience cannot be established.
4. Re-read links and nearby sections after the edit. Removing a command may also remove the only validation route; do not leave an unusable workflow.
5. Report every material deletion or conflict resolution with its evidence.

Do not remove a rule because it is inconvenient, generic-looking, or unused in a small sample. Absence of evidence is not proof of staleness.

## Maintenance checks

Use this checklist for creation and updates:

- Each `AGENTS.md` has a clear scope and only rules that apply there.
- The root remains a short map of shared constraints, verified workflows, and pointers.
- Nested files justify their existence with a material local difference.
- Parent and child files do not silently contradict on an overlapping path.
- Parallel instruction files are compared without assuming shared precedence.
- Commands, working directories, paths, links, and prerequisites have repository evidence and were safely checked when possible.
- Unresolved matters say `UNCONFIRMED` and name the needed evidence or owner.
- The final diff preserves unrelated and human-authored context.

## Escalation record

When stopping, provide a bounded record: the target path; the conflicting or missing statements quoted or located precisely; each source's known scope and audience; the evidence checked; the decision needed; and the files intentionally left unchanged. This lets a maintainer resolve intent without asking the next agent to rediscover the conflict.
