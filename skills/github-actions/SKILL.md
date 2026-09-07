---
name: github-actions
description: "Create, modify, and debug GitHub Actions workflows and custom actions. Use for workflow triggers, jobs, permissions, runners, reusable workflows, action.yml metadata, action inputs or outputs, and Actions security failures."
---

# GitHub Actions

Create and repair GitHub Actions configuration with a deliberate trust boundary, minimal permissions, and evidence from the affected workflow or action.

Choose action refs in this order: an explicit user ref takes precedence; otherwise follow a documented repository convention; otherwise follow a clear majority among comparable external action refs in workflows and local composite actions. Exclude local action uses and reusable-workflow refs from that tally. If the majority uses full-length SHAs, use a verified upstream commit for the latest stable release; if moving major tags are standard, use `@vN`. With no clear convention, including a mixed repository, default to the moving latest stable major tag and explain the choice rather than normalizing unrelated refs. A moving tag can change and is not an immutable security guarantee; a convention-selected SHA must be the verified stable-release commit, not `main` HEAD or a stale runtime.

When adding or updating an action, verify and use its latest stable major from the official upstream releases. If the current workflow is incompatible, tell the user and propose the required adoption changes; never silently retain the old major or guess when the latest release is unavailable. An explicit user version override is honored, and unrelated actions are not auto-updated.

## Workflow

1. **Establish scope and preserve the boundary.**
   - Read repository instructions, the affected `.github/workflows/*.yml` and/or `action.yml`, adjacent actions, relevant project checks, and the current diff. Do not expose secrets or print token-bearing environment values while debugging.
   - Before *any* workflow or action edit, read [shared security guidance](references/security.md). Treat the triggering event, checked-out code, downloaded artifacts/caches, credentials, and runner as one authorization boundary. Stop and ask for a design decision if the request would execute untrusted code with secrets, write permission, cloud credentials, or a trusted/self-hosted runner.
   - For GitHub API authentication choices, apply the [GitHub API authentication decision rule](references/security.md#github-api-authentication); cloud-provider OIDC is a separate mechanism.
   - Classify the work: read [workflow guidance](references/workflows.md) for a workflow change or failure, and [custom-action guidance](references/actions.md) for an `action.yml`/`action.yaml` change. Read both when a workflow calls an action being changed.

2. **Choose the smallest documented design.**
   - State the trigger, trust level, required outcome, runner/OS, data flow, and exact permission or external access needed before editing. Preserve existing repository conventions unless they conflict with the security boundary.
   - Use a workflow for orchestration; use a reusable workflow from `.github/workflows/` only for an intentionally shared whole job or workflow (with a `.reusable.yml` suffix); use a composite action for a reusable sequence of steps. Extract stable repeated step sequences only when this reduces duplication, with minimal inputs and without broadening secret scope. Choose JavaScript or Docker actions only when their distinct runtime or toolchain needs justify them.
   - Consult the linked GitHub reference for keys, contexts, event semantics, runtime support, or limits that affect the change. Do not infer current support from examples or pin a runtime/version merely because another repository uses it.

3. **Make the change explicit and reviewable.**
   - Keep event filters, job dependencies, conditionals, concurrency, permissions, inputs, outputs, shells, and runner labels narrow and visible. Do not add secrets, broad tokens, self-hosted runners, caches, matrices, reusable components, or deployment gates without a current need. For manual dispatch, preserve the selected branch/tag and verify its resolved commit before security-sensitive or shared-environment side effects; do not silently substitute the default branch or another SHA.
   - Give unsupported, missing, or invalid action input an explicit failure path. Do not rely on metadata alone to enforce it.
   - Keep diagnostic output targeted. Use documented annotations, summaries, and environment files rather than dumping contexts or event payloads.

4. **Validate from syntax to execution.**
   - Inspect the resulting YAML and metadata against the relevant official reference, including expression placement and declared input/output paths.
   - Run existing focused repository checks that cover the changed workflow or action. If `actionlint` is already available, it is an optional static check; do not install it solely for this task. Static checks do not prove hosted execution, permissions, runner availability, event delivery, or cloud authorization.
   - For an action, exercise its documented success and invalid-input paths in the project’s available test or minimal workflow mechanism. For a workflow failure, use the failing run’s job/step, event, resolved ref, `needs` state, permissions, and runner logs to isolate the first failure; do not enable broad debug logging or retry a privileged workflow as a substitute for diagnosis.
   - If runtime validation needs unavailable credentials, event delivery, runner labels, platform access, approvals, or cloud policy, stop at the strongest safe local check and report exactly what remains unverified.

## Failure handling

- A required check stuck in **Pending** after a change may mean an event, branch, path, or commit-message filter skipped the workflow; review required-check and merge-queue implications before widening filters.
- For `pull_request_target` or `workflow_run`, stop execution of PR-controlled code in a privileged job. Review upstream artifact provenance and handling before consumption; never execute untrusted artifact contents or treat them as trusted instructions.
- For authorization failures, identify the specific API/cloud operation and add only its required job-level permission or narrowly scoped OIDC trust condition; never switch to `write-all` or long-lived credentials as a workaround.
- For cache/artifact or runner failures, distinguish missing data/tooling from a trust-boundary violation. Do not bypass a failure by reusing untrusted data in a privileged job.

## Boundary

Use this skill for GitHub Actions workflows and custom actions. It does not authorize remote workflow dispatches, releases, deployments, credential changes, or repository setting changes; obtain explicit authorization and use the applicable skill/process for those operations.
