---
name: adr-writing
description: Create and maintain Markdown Architecture Decision Records (ADRs) when a repository needs a durable record of a significant architectural decision, its rationale, consequences, review, or supersession.
---

# ADR Writing

Use this skill for consequential, long-lived technical decisions—not routine implementation notes, task plans, or temporary experiments. The default is Michael Nygard's five-section ADR format at `<repo root>/docs/adrs/NNNN-kebab-case-title.md`.

## Normal workflow

1. **Discover the repository and record set.** Locate the repository root and inspect `docs/adrs/` (including filenames, statuses, and links). Follow an established repository ADR convention only when the user asks or it is clearly authoritative; otherwise use this skill's default. Do not place a new default ADR elsewhere.
2. **Decide whether an ADR is warranted.** Write one for a decision that constrains future work, has meaningful alternatives or trade-offs, or will need rediscovery. Do not create one merely to document an implementation detail. If uncertain, state the proposed decision, alternatives, and impact, then ask the responsible reviewer whether to record it.
3. **Generate a proposed record.** From the repository root, run:

   ```sh
   python3 skills/adr-writing/scripts/new_adr.py --title "Use PostgreSQL for application data"
   ```

   Or supply an explicit root when running elsewhere:

   ```sh
   python3 /path/to/skills/adr-writing/scripts/new_adr.py \
     --repo-root /path/to/repo --title "Use PostgreSQL for application data"
   ```

   The generator chooses the next number after the highest existing `NNNN-*.md`, creates no overwrite, and prints the created path. Read `scripts/new_adr.py --help` before using unfamiliar options.
4. **Write and review the proposal.** Preserve the generator's Nygard-style order: `# <title>`, then `## Status`, `## Context`, `## Decision`, and `## Consequences`. Explain forces, constraints, alternatives considered as needed in Context; make the Decision unambiguous; state positive, negative, and follow-up consequences. Keep the initial status **Proposed** while it is awaiting review. Request review from the decision owner or appropriate technical authority.
5. **Record the outcome.** Change the status to **Accepted** only after approval. Use **Rejected** when a proposal is declined; it is a useful outcome status, though the core lifecycle is `proposed` → `accepted` → `deprecated` or `superseded`. Use **Deprecated** when an accepted decision remains historically true but should no longer guide new work.
6. **Supersede without rewriting history.** When replacing an accepted decision, create a new proposed ADR that names and links the older ADR. After it is accepted, change the older ADR's status to **Superseded by the new ADR** with a relative Markdown link, and change the new ADR's status to **Accepted; supersedes the old ADR** with a relative Markdown link. Do not alter the accepted decision's rationale or outcome except for non-substantive corrections (for example, a typo or repaired link).
7. **Verify before finishing.** Check the title, filename, status, section order, relative links, and that the record is in `docs/adrs/`. Confirm the generated number was not reused and review the diff with the decision owner.

## Format boundary

Nygard is the default and the generator deliberately emits only its five sections. MADR is a richer, optional alternative for repositories that explicitly adopt it; do not blend MADR fields into the Nygard template. See the [Nygard format reference](references/nygard.md) and [MADR template reference](references/madr.md) before adopting or comparing formats.
