---
name: sentry-setup-releases
description: Set up Sentry release and deploy tracking with consistent event tags, CI release creation, and commit association. Use when issues lack release or suspect-commit context.
license: Apache-2.0
---
# Set Up Sentry Releases

Releases must be configured in the SDK and the deployment pipeline. Do not modify CI, create releases, upload artifacts, or access remote Sentry data without explicit authorization.

## Workflow

1. Inspect existing SDK initialization, build configuration, and CI workflows. Determine whether events already carry a release value and whether CI already creates releases.
2. Choose one version scheme with the user (for example, an immutable build version or commit-derived version). Derive it once and pass the exact same value to the SDK, artifact upload, release creation, and deploy notification. Include the deployment environment consistently.
3. Use the platform's local Sentry skill for SDK-side release tagging. If the platform is not covered locally, consult current official Sentry documentation.
4. Extend the deployment CI job—not a separate competing pipeline—to create/finalize the release, associate commits when supported, and record the deploy. Ensure the job has the necessary repository history and uses an approved secret for any auth token. Never commit that token.
5. If an authenticated Sentry MCP capability is available, capability-check its tool schemas before authorized reads or writes. It is optional; repository inspection and CI configuration must not depend on it.
6. Verify with an authorized real deployment: confirm a new event's release exactly matches the created release, then confirm the release records the intended deploy and commits. Diagnose mismatches in version derivation, environment, CI inputs, and credentials before rerunning.

Use `sentry-fix-stack-traces` if artifact matching is the blocker and `sentry-debug-issue` to investigate a specific failure.
