# Workflow guidance

Use this reference for `.github/workflows/*.yml` edits and workflow-run failures. Consult the linked GitHub Docs for the exact syntax supported by the target service and runner.

## Design in dependency order

1. **Start with the event and required checks.** Choose the narrowest event and explicit activity `types` where behavior matters. `branches`/`tags` and `paths` filters constrain different dimensions; when both branch and path filters apply, both must match. A workflow skipped by branch or path filters can leave its required check pending and block a pull request. If the repository uses merge queues and a required check must run for queued PRs, include the appropriate `merge_group` trigger as well as the PR trigger.
   - Prefer `pull_request` for untrusted PR CI. It normally checks the PR merge result; use the documented event context when the head SHA is specifically required.
   - Do not choose `pull_request_target` to build or test PR code. Its base-repository context is for narrowly privileged interactions such as labeling or commenting; see [security guidance](security.md).
   - Source: [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

2. **Separate expression evaluation from runner execution.** Contexts and expressions are evaluated only where GitHub documents them as available; runner environment variables are consumed by the selected shell after a job starts. Use `if:` for workflow conditions and put dynamic values in a step `env:` mapping before a shell command. Quote and validate shell variables for that shell. Do not interpolate event-derived values directly into `run:`. `defaults.run` can set a shell and working directory but cannot use contexts or expressions.
   - Source: [Expressions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions), [contexts](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [script injections](https://docs.github.com/en/actions/concepts/security/script-injections).

3. **Declare the authorization and data graph.** Set the minimum `GITHUB_TOKEN` permissions at workflow scope, then narrow further at a job when its need differs. Once a `permissions` map is specified, unspecified permissions are `none`; add only the operation’s documented scope. Model cross-job ordering with `needs`; publish a job output deliberately and consume it through `needs.<job>.outputs.<name>`, not through filesystem state from another runner.
   - If a GitHub App installation token is needed, mint it in the consuming job and pass its step output only to the steps that need it; do not publish it as a job output by default. Apply the [GitHub API authentication decision rule](security.md#github-api-authentication).
   - Source: [workflow syntax: permissions and jobs](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication).

4. **Reuse at the right level.** Use a reusable workflow in `.github/workflows/` (`workflow_call`) only for an intentionally shared whole job or workflow, with a `.reusable.yml` suffix (project naming convention) and declared caller inputs, secrets, and outputs. A reusable workflow may contain one whole job or multiple jobs; it is not limited to multi-job units. Use a composite action for a reusable sequence of steps within a job. Do not replace a one-off or small step sequence with either merely for abstraction.
   - Source: [Reuse workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows), [custom-action guidance](actions.md).

5. **Preserve dispatch revision identity.** Unless the user explicitly requests an immutable commit or another explicit ref, target the branch or tag selected for manual dispatch—not the default branch and not a silently substituted SHA. Resolve that selected ref to a SHA before any security-sensitive or shared-environment operation. Preserve the selected dispatch ref, compare the actual run SHA with the resolved approved SHA before privileged side effects, and stop on a mismatch or ref movement rather than quietly running another revision. This verifies exact revision identity; it does not authorize the dispatch, so the existing explicit authorization boundary still applies.

6. **Bound parallelism and shared resources.** Add a matrix only for intended, named variations; decide fail-fast and continuation behavior explicitly. Use concurrency only where runs contend for the same resource (for example, a deployment target or preview); include a stable, appropriately scoped group key and choose cancellation behavior intentionally. GitHub does not guarantee concurrency-group ordering.
   - Source: [Matrix variations](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow), [concurrency](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs).

7. **Match data, environment, and runner to their purpose.** Use artifacts for build outputs or diagnostics that must be stored/shared; use dependency caches only for reusable dependency data, never as a security boundary. Environments apply deployment protection rules and scope environment secrets/variables, but do not isolate the runner. Select a runner whose OS, architecture, installed tooling, and trust boundary meet the job’s actual needs. GitHub documents clean, ephemeral isolation for GitHub-hosted runners; do not generalize that property to self-hosted or other offerings.
   - Source: [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments), [dependency caching](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows), [artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts), [self-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/about-self-hosted-runners).

## Diagnose a failed run

1. Identify the exact event, ref/SHA, actor, workflow revision, job, and first failed step. Confirm the event/filter selected the workflow before treating a missing run as a job failure.
2. Check YAML/schema errors, then expression/context availability, then `if:` and `needs` results, then checkout/ref, runner/OS/tool availability, and finally credentials or external service authorization.
3. For state transfer, distinguish a missing step output from a missing declared job output; use `GITHUB_OUTPUT` for step outputs and explicit job outputs for downstream jobs. `GITHUB_ENV` affects later steps in the same job only.
4. Use debug logging only when necessary and within repository policy. Do not log contexts, secrets, tokens, or untrusted payloads. Prefer annotations and `GITHUB_STEP_SUMMARY` for concise human-facing diagnostics.
   - Source: [Workflow commands and environment files](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands), [enabling debug logging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging).

## Sources

Official GitHub Docs reviewed 2026-09-06. The links above are source material, not a frozen compatibility promise; verify live documentation for service-specific syntax, runner images, and limits.
