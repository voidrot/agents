---
name: handoff
description: Create a concise handoff artifact so a fresh agent can continue work without rereading the whole session.
argument-hint: "What will the next session be used for?"
---

# Handoff

## When to Use

- The user asks to prepare a fresh agent, next session, or continuation note.
- Work is midstream and context would be expensive or risky to reconstruct.
- The session produced decisions, evidence, or partial changes that are not fully captured elsewhere.

## Workflow

1. Identify the intended next-session focus from the user's arguments, if provided.
2. Summarize only the context needed to continue safely.
3. Reference existing artifacts by path, URL, commit, branch, or issue instead of copying them.
4. Record current state, blockers, validation results, and exact next steps.
5. Redact secrets, credentials, tokens, and unnecessary personal data.
6. Save outside the workspace in the OS temp directory unless the user requests another location.

## Artifact Format

Use this structure:

```md
# Handoff: <topic>

## Goal
## Current State
## Key Decisions
## Evidence and Links
## Open Questions / Blockers
## Suggested Next Steps
## Suggested Skills
## Relevant Files
## Validation
```

## Boundaries

- Keep it concise; this is a continuation map, not a transcript.
- Do not duplicate PRDs, plans, ADRs, issues, diffs, or generated reports.
- Do not invent decisions that were not made.
- Call out uncertainty explicitly.

## Output

- Path to the handoff document.
- One-sentence summary of what the next agent should do first.
