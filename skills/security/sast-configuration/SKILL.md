---
name: sast-configuration
description: Use when selecting, configuring, tuning, or reviewing Static Application Security Testing for application code, including Semgrep, CodeQL, SonarQube, custom rules, CI integration, SARIF output, and false-positive triage.
---

# SAST Configuration

Use this skill as the activation and routing layer for sast configuration work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Identify languages, frameworks, build steps, repository size, compliance needs, and CI constraints.
2. Choose tools and rule sets that match the stack; start with maintained standard rules before custom rules.
3. Configure CI to run at the right cadence with reproducible versions, useful severity thresholds, and SARIF/report output.
4. Tune ignores, baselines, and custom rules with evidence; do not hide findings only to make the pipeline pass.
5. Document remediation ownership, review cadence, and tests for rules that protect high-risk patterns.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/full-guidance.md for detailed tool setup, examples, and tuning guidance.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
