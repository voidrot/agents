---
name: manage-agents-md
description: Create, update, prune, and organize repository AGENTS.md guidance when an agent needs scoped, evidence-backed instructions for coding work, including reconciling nearby CLAUDE.md or similar instruction files.
---

# Manage AGENTS.md Guidance

Use this skill for repository instruction maintenance, not for writing a generic project overview or changing implementation. Its outcome is a small, accurate instruction hierarchy that helps an agent work safely in the relevant paths.

## Non-negotiable rules

- Discover repository evidence before writing. Do not infer commands, versions, ownership, precedence, or local rules from file names alone.
- Determine the scope and effective precedence of every applicable instruction source. `CLAUDE.md`, editor rules, and other nearby files may be related, but do **not** assume they share `AGENTS.md` precedence or apply to the same tools.
- Preserve human-authored intent. Update narrowly; never replace a file, remove a rule, or synchronize parallel instruction files merely because another file differs.
- Keep root `AGENTS.md` a concise map and put only genuinely local rules in nested `AGENTS.md` files. Do not create a nested file to duplicate the root.
- Record unresolved facts as `UNCONFIRMED` (with the needed source or owner), rather than inventing a command, version, rule, or guarantee.
- If instructions conflict, scope or precedence cannot be established, or a necessary fact cannot be verified, stop before a destructive edit and report the blocker and evidence needed.

## Workflow

### 1. Discover evidence

1. Establish the requested paths and the allowed write boundary. If it excludes a necessary instruction file, do not edit outside it; report that constraint.
2. Locate candidate guidance in and above the affected directory: `AGENTS.md`, nested agent files, `CLAUDE.md`, editor/IDE rules, contributor documentation, and task or build configuration that may be the source of a claimed command.
3. Read applicable existing guidance before drafting. Inspect representative source, tests, configuration, automation, and documentation only as needed to verify proposed statements.
4. Build a short evidence ledger: each proposed rule or command, its source path and line/section, its affected scope, and whether it is verified or `UNCONFIRMED`. Read [content and structure guidance](references/content-and-structure.md) when choosing what belongs in a file.

### 2. Decide the hierarchy

1. Identify which instruction sources apply to the target paths and whether they state an ordering. Treat explicit platform, repository, or user policy as evidence; do not manufacture a universal ordering.
2. Choose the fewest files that preserve clarity. Keep cross-repository navigation, shared safety boundaries, and pointers at the root. Add a nested `AGENTS.md` only when a subtree materially differs in scope, conventions, safety constraints, or workflow.
3. Select approximately one to three relevant existing skills or workflow pointers for a task when that information is verified; avoid overlapping directories of instructions or an exhaustive tool catalog.
4. For parallel guidance such as `CLAUDE.md`, decide whether to leave it independent, add a limited cross-reference, or propose a human decision. Do not copy it wholesale or claim it has identical precedence. Read [hierarchy and maintenance guidance](references/hierarchy-and-maintenance.md) for split, reconciliation, and pruning decisions.

### 3. Draft or update narrowly

1. Preserve useful wording, headings, attribution, and local detail in existing files. Make the smallest change that corrects, adds, moves, or removes a verified instruction.
2. Use a concise, adaptable root structure: purpose/scope; repository map and where to look; verified workflows and validation; non-obvious shared invariants; and pointers to materially different local guidance. Omit empty sections and adapt names to repository practice.
3. State actions, prerequisites, paths, expected evidence, and failure boundaries where they are non-obvious. Put exact commands only when their source and applicable directory are verified; retain required arguments and prerequisites.
4. Keep specific procedures and rationale in the file that owns the scope, or in a linked repository reference when that is the established pattern. Prefer a pointer over repeating the same policy in several files.
5. Mark missing evidence `UNCONFIRMED`; do not turn a guess into guidance. Do not add generated dates, broad technology inventories, generic coding advice, or speculative future workflows.

### 4. Reconcile and maintain

1. Compare nearby instruction files rule by rule only where their scopes overlap. Classify each as compatible, complementary, duplicated, stale, or conflicting, with evidence.
2. Remove or revise stale content only after confirming that the path, command, tool, workflow, or rule no longer applies. Preserve historical context if a human-authored statement's status is unclear and flag it instead of deleting it.
3. For a real conflict, retain the authoritative source when known and document only a precise, non-misleading pointer or distinction. When authority is unknown, stop and ask the owner; do not silently choose a winner.

### 5. Verify actual output

1. Re-read every changed file and every target reached by a new local link. Confirm headings, relative paths, filenames, scope statements, and referenced commands against the evidence ledger.
2. Run each documented command only when it is safe, in its documented working directory, and supported by repository evidence. Confirm the command and the claimed result from actual output; otherwise label it `UNCONFIRMED` or omit it. Do not run destructive, production, credential, or network actions merely to validate documentation.
3. Run the repository's available Markdown, link, or instruction-file checks if their invocation is itself verified. Inspect the final diff to ensure no unrelated guidance or human context was changed.
4. If validation fails, correct the documentation or report the exact failure. Never claim a command, link, or hierarchy is valid without that evidence.

### 6. Report

Report changed files; the chosen hierarchy and why; evidence and validation run (including exact commands and results); skipped validation and why; `UNCONFIRMED` facts; and any conflict requiring a human decision.

## Conditional references

- [Content and structure](references/content-and-structure.md) — evidence ledger, concise baseline sections, and writing rules.
- [Hierarchy and maintenance](references/hierarchy-and-maintenance.md) — applicability analysis, nested-file decisions, reconciliation, and stale-content review.
