---
name: github-dependabot
description: "Configure, maintain, troubleshoot, and verify GitHub Dependabot version and security updates when a repository needs a dependabot.yml change, update-PR diagnosis, or dependency-update policy review."
---

# GitHub Dependabot

Use this skill for repository-level Dependabot configuration and diagnosis. Read [the official-source index](references/official-github-docs.md) before changing unfamiliar options or resolving ecosystem-specific behavior.

## Safety boundary

- Treat `.github/dependabot.yml` (or `.yaml`) on the default branch as repository configuration. Inspect the default branch, existing file, manifests, lockfiles, and repository conventions before proposing or editing it.
- Treat GitHub settings, enabling Dependabot alerts/security updates or other security features, permissions, organization policy, private-registry credentials, and Dependabot secrets as separate administrative actions. **Do not change them** or create/rotate secrets without explicit user authorization.
- Never place credential values in `dependabot.yml`, commits, logs, examples, or review output. If private access is needed, identify the required registry and credential mechanism, then request authorization and use GitHub's secret/registry workflow.
- Do not claim that YAML was locally validated or that Dependabot was dry-run; GitHub evaluates configuration and runs updates after it is on the default branch.

## Workflow

1. **Establish the requested outcome.** Distinguish version updates (scheduled dependency currency) from security updates (vulnerability remediation). Determine whether the request is to configure, adjust policy, diagnose, or verify. For security updates, inspect prerequisites and current repository settings; report missing settings rather than enabling them.
2. **Inspect before editing.** Identify the default branch; locate `.github/dependabot.yml` and `.yaml`; inventory supported package ecosystems from manifests and lockfiles; and note each manifest directory. Check existing update entries, schedules, open PRs, ignored/allowed dependencies, grouping, registry references, and relevant Dependabot logs/UI evidence.
3. **Map manifests to entries.** Create one `updates` entry per intended package ecosystem and manifest directory. Use `version: 2`, exact `package-ecosystem` values and directory syntax supported by GitHub. Do not assume a repository root, monorepo layout, or ecosystem is supported—confirm it in the supported-ecosystems reference.
4. **Start from a minimal, explicit configuration.** Preserve established repository policy where present. For a new version-update entry, use a conservative schedule agreed with the requester; specify `open-pull-requests-limit` only when a backlog/PR-volume policy warrants it.

   ```yaml
   version: 2
   updates:
     - package-ecosystem: "npm"
       directory: "/"
       schedule:
         interval: "weekly"
   ```

5. **Apply policy deliberately.** Use `allow` to narrow the candidates Dependabot may consider and `ignore` to suppress known-unwanted updates; check GitHub's documented precedence before combining them. Prefer narrowly scoped ignores with a reason and planned review over broad or permanent exclusions. Set PR limits, labels, assignees, reviewers, commit-message metadata, and target branch only when they match existing repository workflow. Use dependency groups when batching is requested and compatible with the ecosystem; use multi-ecosystem groups only for coordinated update schedules/policies, following its distinct syntax and constraints.
6. **Handle private dependencies safely.** Determine whether the manifest needs a private registry. Use the documented `registries` reference mechanism and GitHub-managed Dependabot secrets/credentials; request explicit authorization before any settings or secret action. Verify the repository/org policy can grant access without exposing a value.
7. **Review the resulting diff.** Confirm the file is on the default branch, validly structured as `version: 2` with intended `updates`, correct directories, supported ecosystems, and no credentials. Check that policy changes do not unintentionally exclude all desired updates, create excessive PRs, or alter unrelated update entries.
8. **Verify through GitHub after merge.** Use the Dependabot UI, update PRs, and Dependabot logs to confirm discovery, scheduling, grouping, and errors. Security-update verification also requires confirming the authorized repository settings/prerequisites are enabled. Record the observed PR/log URL or the absence/error and its timestamp; do not infer success merely from a merged YAML file.

## Diagnosis guide

- **No version-update PRs:** confirm the configuration is on the default branch, the ecosystem and directory match actual manifests, the schedule has elapsed/been triggered as documented, dependencies are eligible, and limits, `allow`, or `ignore` rules are not preventing PRs. Inspect Dependabot logs.
- **No security-update PRs:** distinguish this from scheduled version updates. Inspect dependency-graph/alert/security-update prerequisites and authorized GitHub settings, then inspect the affected manifest and logs. Request authorization before enabling anything.
- **Configuration rejected or ignored:** compare keys, values, directory paths, and grouping syntax with the options reference; use the exact log error rather than guessing.
- **Private-registry authentication failure:** identify the registry name/reference and GitHub's reported error. Do not add a token to YAML or output; request authorization to inspect or update the approved secret/registry configuration.
- **Unexpected, missing, or grouped PRs:** inspect `allow`/`ignore` interactions, PR limit, schedule, dependency groups, multi-ecosystem groups, target branch, and any existing repository policy before changing a rule.

## Completion evidence

Report: the requested distinction (version/security); inspected default branch, manifests, and directories; configuration diff or proposed diff; any settings/secret action explicitly left pending authorization; and GitHub UI/log evidence after merge. If GitHub has not yet run Dependabot, report verification as pending rather than successful.

## Reference use

- Use [Dependabot options](references/official-github-docs.md#configuration-and-supported-ecosystems) for option syntax, supported ecosystems, schedules, filters, limits, metadata, and groups.
- Use [security updates and prerequisites](references/official-github-docs.md#security-updates-and-prerequisites) when the task concerns alerts or remediation PRs.
- Use [private registries](references/official-github-docs.md#private-registries-and-troubleshooting) for authenticated dependencies and [errors](references/official-github-docs.md#private-registries-and-troubleshooting) for log-led troubleshooting.
