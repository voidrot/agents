---
description: Create per-skill update plans for newly added skills before integration.
---

# Integrate New Skills

Audit newly added skills and create implementation plans. Do not move, delete,
merge, or rewrite skill files during this command.

## Input

- Default source directory: `skills/.to-sort/`
- User-provided source or scope: $ARGUMENTS

If the user-provided source or scope is non-empty, use it instead of the default.
Otherwise, audit every skill directory under `skills/.to-sort/`.

## Repository Standards to Inspect

Before writing plans, inspect:

- `SKILLS.md`, if present
- `README.md`, especially skills-related sections
- Existing skills under `skills/`
- Existing support files under each skill's `references/`, `scripts/`, and
  `assets/` directories

Use this repository's current structure and conventions as the source of truth.

## Objective

For each candidate skill, create one plan file:

```text
docs/plans/update-<skill-name>.md
```

Use kebab-case for `<skill-name>`.

Each plan must describe the changes required to make the skill compliant,
correctly categorized, non-duplicative, and ready for use.

## Evaluation Criteria

For each candidate skill, evaluate whether it:

- Meets the repository's skill specification and standards.
- Meets the skills guidance documented in `README.md`.
- Keeps `SKILL.md` small, focused, and informational.
- Uses `SKILL.md` as a routing and overview layer.
- Moves dense guidance, long examples, large tables, detailed procedures, or
  verbose documentation into `references/` when appropriate.
- Has a short, clear activation-oriented description.
- Has intact internal references.
- Has external references that are correct and still valid.
- Removes or updates incorrect, missing, stale, or broken references.
- Uses reference links that point to the correct local skill, local file, or
  external source.
- Is categorized under the appropriate `skills/<category>/` directory.
- Proposes a new category only when no existing category fits.
- Does not duplicate an existing skill.
- Merges useful unique content into an existing skill when there is substantial
  overlap.
- Marks duplicate source skills for removal when they add no unique value.
- Checks claims, APIs, CLIs, configs, and workflows against official
  documentation when they may be stale or uncertain.

## Duplicate and Merge Rules

When a candidate overlaps with an existing skill:

- If it is a true duplicate with no useful new information:
  - Set proposed action to `remove_duplicate`.
  - Identify the canonical existing skill.
  - Explain why no merge is required.
- If it duplicates an existing skill but contains useful content:
  - Set proposed action to `merge_into_existing`.
  - Identify the canonical existing skill.
  - List the specific content, references, scripts, or assets to merge.
  - Include required updates to keep the canonical skill compliant.
- If it is distinct:
  - Set proposed action to `new_skill`.
  - Identify the target category and final path.
- If it belongs in a category that does not exist:
  - Set proposed action to `new_skill_new_category`.
  - Propose the new category name and explain why existing categories do not fit.

## Plan File Template

Each plan must use this structure:

```md
# Update Plan: <Skill Name>

## Source

- Source path: `<path>`
- Proposed action: `<new_skill | new_skill_new_category | merge_into_existing | remove_duplicate | needs_manual_review>`
- Proposed final path: `<path or n/a>`
- Canonical existing skill: `<path or n/a>`

## Summary

Briefly describe what the skill does and what needs to happen.

## Standards Review

- `SKILLS.md` compliance: `<pass | needs changes | fail>`
- `README.md` skills guidance compliance: `<pass | needs changes | fail>`
- `SKILL.md` size and focus: `<pass | needs changes | fail>`
- Description quality: `<pass | needs changes | fail>`
- Reference integrity: `<pass | needs changes | fail>`
- Category placement: `<pass | needs changes | fail>`
- Duplicate status: `<unique | partial overlap | duplicate>`

## Required Changes

List the specific changes required.

## Reference Updates

| Reference | Current Status | Required Action | Notes |
| --- | --- | --- | --- |
| `<reference>` | `<valid | missing | stale | incorrect | unknown>` | `<keep | update | move | remove | verify>` | `<notes>` |

## Content Movement

| Content | Current Location | Target Location | Reason |
| --- | --- | --- | --- |
| `<content summary>` | `<path>` | `<path>` | `<reason>` |

## Official Documentation Checks

| Topic | Official Source To Check | Why |
| --- | --- | --- |
| `<topic>` | `<URL or docs name>` | `<reason>` |

## Merge Plan

If this skill should be merged into an existing skill, describe exactly what
should be merged.

- Target skill: `<path>`
- Content to merge:
  - `<item>`
- References to merge:
  - `<item>`
- Scripts/assets to merge:
  - `<item>`
- Duplicate content to discard:
  - `<item>`

If not applicable, write `Not applicable.`

## Removal Plan

If this skill should be removed as a duplicate, explain why.

- Duplicate of: `<path>`
- Unique information found: `<yes | no>`
- Required canonical skill updates before removal:
  - `<item>`

If not applicable, write `Not applicable.`

## Final Implementation Checklist

- [ ] Update or create the target skill directory.
- [ ] Update `SKILL.md` description and routing information.
- [ ] Move dense content into `references/`.
- [ ] Update local references.
- [ ] Update or remove broken references.
- [ ] Verify technical claims against official documentation.
- [ ] Merge useful duplicate content where applicable.
- [ ] Remove duplicate source skill where applicable.
- [ ] Confirm final category placement.
- [ ] Confirm the final skill follows repository standards.

## Verification Requirements

- Inspect the candidate skill's full directory.
- Inspect likely duplicate or related existing skills.
- Check all local links and relative paths mentioned by the skill.
- Check whether referenced files actually exist.
- Identify references that point to missing files, renamed skills, incorrect
  categories, or stale external documentation.
- Do not assume a reference is valid only because it looks plausible.
- Do not preserve duplicate content unless it adds meaningful value.
```

## Final Report

After all plan files are written, respond with a concise report using this
structure:

```md
# Skill Import Planning Report

## Summary

- Input directory: `<path>`
- Total skills reviewed: `<number>`
- New skills: `<number>`
- New skills requiring new categories: `<number>`
- Skills contributing updates to existing skills: `<number>`
- Skills to merge into existing skills: `<number>`
- Duplicate skills marked for removal: `<number>`
- Skills needing manual review: `<number>`

## Skills by Category

| Category | New Skills | Merge Into Existing | Duplicate Removal | Manual Review |
| --- | ---: | ---: | ---: | ---: |
| `<category>` | `<number>` | `<number>` | `<number>` | `<number>` |

## Planned Skill Actions

| Skill | Proposed Action | Target Category | Target Path | Plan File |
| --- | --- | --- | --- | --- |
| `<skill>` | `<action>` | `<category>` | `<path>` | `<plan path>` |

## Duplicates and Merges

| Source Skill | Canonical Skill | Action | Notes |
| --- | --- | --- | --- |
| `<source>` | `<canonical>` | `<merge/remove>` | `<notes>` |

## New Categories Proposed

| Category | Skills | Reason |
| --- | --- | --- |
| `<category>` | `<skills>` | `<reason>` |

## Manual Review Items

List anything that could not be safely resolved from repository context alone.
```

## Constraints

- Do not apply the plans.
- Do not delete files.
- Do not move skill directories.
- Do not rewrite skill files.
- Do not invent missing standards.
- Prefer existing repository conventions over generic assumptions.
- Keep plans specific enough that a later implementation pass can execute them
  without rediscovery.
