---
name: gdpr-compliant
description: Use when designing, implementing, or reviewing systems that process personal data, including user accounts, analytics, cookies, logs, retention, exports, deletion, breach response, DPIAs, subprocessors, or privacy-by-design questions.
---

# GDPR-Compliant Engineering

Use this skill as the activation and routing layer for gdpr-compliant engineering work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Map personal data, processing purposes, legal basis, data subjects, subprocessors, retention, and cross-border transfers.
2. Apply privacy by design: minimize fields, default collection off, separate DTOs, mask responses, and restrict access.
3. Verify data-subject rights: access, rectification, erasure, export, objection/restriction, and auditability.
4. Check security controls for encryption, hashing, secret handling, logging, pseudonymization/anonymization, and least privilege.
5. Return engineering requirements, evidence to retain, open compliance assumptions, and legal-review items when needed.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/full-guidance.md for detailed GDPR engineering rules and examples.
- references/data-rights.md for DSR workflows and rights endpoints.
- references/Security.md for security controls and privacy-preserving implementation patterns.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
