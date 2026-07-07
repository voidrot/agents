---
description: Extract a DESIGN.md design system from frontend source code and validate it with the design.md linter.
model: opencode-go/glm-5.2
---

# Extract DESIGN.md

Create or update a `DESIGN.md` file from the current project's frontend source code.

## Relevant Skills

- Use @extract-design-md for source-only design-system extraction, component-library theme analysis, DESIGN.md structure, and lint/fix requirements.

## Requirements

$ARGUMENTS

## Instructions

1. Load and follow @extract-design-md.
2. Inspect the project source for frontend framework, styling system, component library, theme files, tokens, global styles, and representative components.
3. Generate a complete `DESIGN.md` at the project root unless the user specifies another output path.
4. Prefer extracted source evidence over assumptions. Document inherited library defaults separately from project-specific overrides.
5. Validate the result from the directory containing `DESIGN.md`:

   ```sh
   npx @google/design.md lint DESIGN.md
   ```

6. Fix all lint errors and rerun the exact command until it returns no lint errors.
7. If linting cannot run because npm, network, or package access is unavailable, report the exact blocker and manually verify the DESIGN.md frontmatter and required sections.

## Output

Return a terse summary containing:

- `DESIGN.md` path
- source areas inspected
- detected frontend/styling/component-library stack
- lint result
