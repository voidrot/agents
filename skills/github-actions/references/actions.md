# Custom-action guidance

Use this reference when creating or modifying `action.yml` or `action.yaml`. Treat the metadata, documented inputs/outputs, compatibility, and release behavior as the action’s public contract.

## Action reference and extraction policy

- Resolve action refs in this order: an explicit user ref, a documented repository convention, then a clear majority among comparable external action refs in workflows and local composite actions. Exclude local action uses and reusable-workflow refs from the tally. A SHA majority means use a verified full-length upstream commit for the latest stable release; a moving-tag majority means use `@vN`. If no convention is clear, including in a mixed repository, default to the latest stable moving major tag and explain that choice; do not normalize unrelated refs.
- For convention-selected SHA refs, verify the commit belongs to the intended upstream release; do not use `main` HEAD or retain an old runtime solely because it is already pinned. Moving tags are not immutable or security-equivalent to SHAs, though they reduce upkeep. When adding or updating an action, verify and use the latest stable major in official upstream releases. When determining the latest stable version or a release SHA, prefer the `gh` CLI or GitHub MCP if available; if neither is available, fall back to available search tooling. Verify release/commit provenance. If it is incompatible, tell the user and propose the required adoption changes; never silently retain the old major. If the latest release cannot be verified, do not guess. Honor an explicit user version override and do not auto-update unrelated actions.
- Extract a stable repeated sequence of steps into a composite action at `.github/actions/<action-name>/action.yml` only when doing so reduces duplication. Keep inputs minimal; prefer job-scoped environment variables for secrets where suitable, never store literal secrets, and do not broaden a secret’s job scope merely for convenience.

## Choose and define the action

1. **Select the narrowest action type.** Use a composite action for transparent orchestration of existing `run`/`uses` steps. Use a JavaScript action for portable program logic, API use, structured validation, or action lifecycle hooks. Use a Docker action only when the required toolchain genuinely needs a container boundary. Use a reusable workflow when intentionally sharing a whole job or workflow, not merely a small step sequence.
   - Source: [About custom actions](https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions), [reusable workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows).

2. **Make metadata a complete interface.** Use `action.yml` (GitHub’s preferred filename) with required `name`, `description`, and `runs`. Give every accepted input/output a stable identifier and clear description; declare a default only when it is safe for all callers. Declare only outputs a caller must consume. For JavaScript actions, verify the selected `runs.using` runtime against the live metadata reference and supported runner compatibility rather than copying an old version. The reference reviewed for this skill lists `node20` and `node24`, but that is not a reason to freeze either version.
   - Source: [Metadata syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax). The moving-major and extraction rules above are project conventions, not claims from that official reference.

3. **Validate inputs in implementation.** `required: true` describes an input but does not automatically fail when the caller omits it. Reject missing, empty, malformed, or unsupported values before any side effect, with an actionable error. In a composite action, read inputs through the `inputs` context; do not assume automatic `INPUT_*` environment variables. Keep input-derived shell values in `env:` and quote/validate them for the chosen shell.
   - Source: [Metadata syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax), [script injections](https://docs.github.com/en/actions/concepts/security/script-injections).

4. **Use supported runner communication.** Set step outputs through `GITHUB_OUTPUT` (or the matching toolkit API); set later-step environment values through `GITHUB_ENV`; reserve `GITHUB_STATE` for an action’s pre/post communication. Outputs are not a secret transport. Consult the live metadata and workflow-command references for output semantics and limits before sending large or multiline data.
   - Source: [Workflow commands and environment files](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands), [metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax).

5. **Package and release deliberately.** A published JavaScript action must include or bundle the runtime dependencies its entrypoint needs; a workflow caller should not need to install them first. For Docker and composite actions, include every referenced entrypoint/script and document required tools. Preserve executable permissions on directly executed scripts. Self-hosted runners for Docker container actions must run Linux and have Docker installed. Check out the repository before invoking a local action with `uses: ./path`. Document supported OS/runner and runtime assumptions, required permissions, inputs, outputs, side effects, failure behavior, and any cleanup contract. Do not claim portability not exercised by the action’s tests.
   - Source: [Create a JavaScript action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-javascript-action), [create a composite action](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action), [create a Docker container action](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-docker-container-action).

## Verify the contract

- Check metadata paths, entrypoints, declared inputs, outputs, and action type against the live metadata reference.
- Exercise success, missing/invalid input, expected failure, output, and cleanup paths. Run on every OS/runtime that the action claims to support; otherwise state the untested compatibility.
- Test from a minimal calling workflow or the project’s existing action test setup so that metadata-to-runtime behavior is covered. Static metadata/YAML checks cannot prove hosted runners, credentials, Docker availability, or event behavior.
- When debugging, use `core.debug`/documented debug facilities and error annotations without printing inputs that could contain sensitive data.
  - Source: [Testing and debugging actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/testing-and-debugging-your-actions), [workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).

## Sources

Official GitHub Docs reviewed 2026-09-06. Verify live documentation before relying on runtime names, metadata fields, output limits, or platform behavior.
