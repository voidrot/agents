---
name: repo-scan
description: Use when auditing a large or legacy repository to classify source assets, embedded third-party code, build artifacts, dead weight, and module-level ownership risks.
origin: community
---

# Repo Scan

Use this skill to perform a cross-stack source asset audit: what code is first-party, what is vendored or generated, what is build artifact noise, and which modules should be kept, extracted, rebuilt, or deprecated.

## Workflow

1. Confirm the scan scope and whether external scanner installation is allowed.
2. Prefer local evidence first: file tree, manifests, licenses, vendored directories, generated artifacts, and module ownership clues.
3. If using the upstream scanner, install only a reviewed, pinned source revision and document the command used.
4. Classify findings by module and produce actionable verdicts, not just inventory counts.
5. Return a compact summary plus report path or artifacts if generated.

## Constraints

- Do not fetch or execute remote scanner code unless the user approves the source and pinned revision.
- Do not mistake declared dependencies for embedded third-party source; verify by inspecting repository contents.
- Do not commit generated HTML reports unless requested.

## Supporting Material

- Read `references/scanner-guidance.md` for upstream source, capabilities, depth levels, examples, and best practices.
