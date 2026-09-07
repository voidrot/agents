# Shared trust and security guidance

Read this reference before every GitHub Actions workflow or custom-action edit. A workflow is privileged automation: its event, code, data, credentials, network access, and runner must be compatible with the same trust level.

## Apply these controls in order

1. **Separate untrusted code from privilege.** Treat pull-request content, branch names, commit messages, issue/PR bodies and titles, labels, email addresses, and other event/context values as untrusted. Do not place them directly in `run:`; move them to an environment variable and quote and validate them in the chosen shell, or pass them as a non-shell action input. Do not assume a context is safe because it came from GitHub.
   - Source: [Script injections](https://docs.github.com/en/actions/concepts/security/script-injections), [contexts](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).

2. **Keep privileged triggers away from PR-controlled code and data.** Prefer `pull_request` for untrusted PR CI. Avoid `pull_request_target` and `workflow_run` unless a privileged context is necessary. In either privileged context, do not check out or execute PR/fork-controlled code, and treat artifacts from an upstream/untrusted workflow as untrusted input. Do not share a cache across the untrusted-to-privileged boundary without a documented safe design. `pull_request_target` is not a safe way to test a PR.
   - Source: [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), [`pull_request_target` event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target).

3. **Grant only the authorization each job needs.** Declare minimal `GITHUB_TOKEN` permissions at workflow or job scope. Add a write scope only for the specific operation that requires it; do not use `write-all` to resolve an authorization error. Keep secrets out of source, logs, output values, summaries, and diagnostic context dumps. Remember that automatic masking is not a guarantee after a value is transformed.
   - Source: [Workflow syntax: `permissions`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions), [secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).

4. **Apply the distinct action and reusable-workflow ref policies.** For action refs, an explicit user ref takes precedence, followed by a documented repository convention, then a clear majority among comparable external action refs in workflows and local composite actions. Exclude local action uses and reusable-workflow refs from that tally. Use a verified full-length upstream commit for the latest stable release when SHAs are the clear convention; use the latest stable moving major such as `@vN` when moving tags are standard. With no clear convention, including in a mixed repository, default to the moving major and explain the choice rather than normalizing unrelated refs. Moving tags can change and are not immutable or security-equivalent to SHAs; a convention-selected SHA must be the verified stable-release commit, not `main` HEAD or an old runtime retained for convenience. For separately referenced third-party reusable workflows, retain full-length SHA pinning and verify the SHA belongs to the intended upstream repository rather than a fork.
   - Source: [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use). The action-ref precedence and moving-major fallback are project policy, not an official GitHub recommendation.

### GitHub API authentication

5. **Choose GitHub API authentication deliberately.** Use the automatic `GITHUB_TOKEN` for operations it supports. When additional GitHub API authentication is required, prefer a narrowly scoped, short-lived GitHub App installation token minted by [`actions/create-github-app-token`](https://github.com/actions/create-github-app-token) over a PAT. Limit the App installation to the required repositories and permissions, then scope the action invocation to the task with `owner`/`repositories` targeting only the needed repositories and explicit `permission-*` inputs; pass the token output only to the steps that need it. Keep the App private key in approved secret storage and never log the key or token. The action's current README documents one-hour expiry and default post-job revocation; retain that default and do not set `skip-token-revoke` without a justified requirement. A PAT is an exception only when an explicit, justified user or project constraint requires it—never silently fall back to one. Creating or installing the App, changing its installation/repository permissions, or changing repository authentication/secrets remains authorization-gated.
   - Sources: [GitHub Docs: authenticate in an Actions workflow](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow), [GitHub Docs: generate an installation access token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app), and the [`actions/create-github-app-token` README](https://github.com/actions/create-github-app-token#readme).

6. **Verify dispatch revision before privilege.** Unless an explicit immutable commit or other explicit ref was requested, preserve the branch/tag selected for manual dispatch rather than using the default branch or silently substituting a SHA. Resolve the selected ref to a SHA before security-sensitive or shared-environment operations; compare the actual run SHA with that approved SHA before privileged side effects and stop on mismatch or ref movement. This verifies exact revision identity, not dispatch authorization; keep the existing explicit authorization boundary.

7. **Prefer short-lived cloud authentication where supported.** When a cloud provider supports GitHub Actions OIDC, prefer it to a long-lived cloud credential. Grant `id-token: write` only to the job that requests it and restrict the cloud-side trust policy to the appropriate repository, ref, environment, and other provider-supported claims. Do not add a broad trust policy or long-lived secret as a convenience fallback. OIDC authenticates to a cloud provider; it does not replace a GitHub API App installation token.
   - Source: [OIDC security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/about-security-hardening-with-openid-connect), [workflow syntax: permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions).

8. **Treat runner selection as access control.** GitHub documents clean, ephemeral isolation for GitHub-hosted runners. Self-hosted runners do not have that guarantee and can be persistently compromised by untrusted workflow code. Do not run public or untrusted PR code on self-hosted runners. If self-hosting is necessary, isolate runner groups by repository/trust boundary, minimize host secrets and network access, and use clean/one-job infrastructure where the deployment can support it. Environment approvals protect deployment policy; they do not isolate a self-hosted runner.
   - Source: [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), [self-hosted runner access](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access).

## Stop and escalate

Do not implement without an explicit design/authorization decision when a change would:

- run PR-controlled code, artifacts, or cache data in a job with secrets, write permissions, cloud access, or a trusted runner;
- broaden `GITHUB_TOKEN`, secret, OIDC, runner-group, or network access beyond a stated operation;
- use a PAT without an explicit, justified user or project constraint, or silently substitute one when App authentication is unavailable;
- add `pull_request_target`, `workflow_run`, a self-hosted runner, a third-party action whose requested ref or upstream cannot be verified, or a separately referenced third-party reusable workflow that cannot be verified and fully SHA-pinned; or
- log, transmit, or store a secret in an output, artifact, cache, summary, or source file.

## Sources

Official GitHub Docs reviewed 2026-09-06. The GitHub App authentication sources above and the `actions/create-github-app-token` README were verified 2026-09-07. Recheck these live sources when changing security-sensitive behavior; provider-specific OIDC claim syntax and repository policy can vary.
