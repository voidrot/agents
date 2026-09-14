---
name: efficient-planning
description: "Create, review, or revise implementation plans with risk-proportionate scope, verification, rerun, and evidence requirements; use when a task needs a plan or plan review that must control planning and validation cost without reducing required outcomes."
---

# Efficient Planning

Use this skill for implementation plans and plan reviews. Preserve product outcomes, security requirements, and required evidence; reduce only work that has no distinct value.

## Workflow

1. Before selecting steps, perform a minimal read-only discovery pass: inspect relevant specifications and code boundaries, established conventions, dependencies, risks, and unknowns.
2. State the outcome and completion conditions before choosing implementation or verification work. Make each condition observable.
3. Separate **product requirements** from **implementation suggestions**. Preserve required behavior, constraints, security, and acceptance conditions. Treat proposed files, tools, tests, commands, architecture, and sequence as changeable unless they are explicitly required.
4. Bound the plan to affected behavior and risk. Add detail where mistakes would be costly, irreversible, security-relevant, or hard to detect. Divide large work into vertical, independently verifiable functional slices, not chat-session or time boundaries; establish shared contracts or dependency foundations before work that depends on them. Do not prescribe a universal planning depth, test-to-code ratio, or time limit.
5. For each material unknown, state a bounded assumption, the least evidence that could update it, and a trigger to continue, change, or stop. Investigate irreversible decisions more deeply. For a non-blocking unknown, use a stated bounded assumption rather than automatically seeking clarification.
6. Choose the least expensive reliable evidence for every completion condition. Prefer targeted inspection, a focused check, or a narrow reproduction when it establishes the condition reliably. For empirical uncertainty, state the hypothesis and retain what the check learned, including informative failures or intermediate signals; learning does not justify blanket extra testing.
7. For every expensive check, state its distinct benefit and the risk it covers. Reuse existing tests and tools first; treat new testing infrastructure as a separate cost that needs its own concrete benefit. Remove duplicates; do not require a full matrix or full suite unless the requirement, affected surface, or risk specifically needs it.
8. Define reruns by impact. Rerun only checks whose assumptions, inputs, or covered behavior changed, including changes to code, dependencies, builds, configuration, or the environment. Diagnose and classify a failure as a product defect, test-harness defect, infrastructure problem, or missing access before repeating the same check; change the investigation or check only when the diagnosis supports it.
9. Preserve concise, durable evidence: commands or observations, relevant result, environment or inputs when material, and known limits. Assert only behavior actually reached and strongly supported by the evidence.
10. Review the plan for simplification and stop conditions. Remove work that cannot change the decision, keep required outcomes intact, and stop when all completion conditions have reliable evidence.

## Plan output

Write the plan in this shape so an implementer can act on the rerun and diagnosis rules rather than infer them from discussion.

```markdown
## Outcome and completion
- Outcome:
- Observable completion conditions:

## Requirements and choices
- Product requirements and constraints:
- Implementation suggestions that may be replaced with an equivalent approach:
- Scope and affected boundaries:
- Discovery: relevant specifications/code boundaries, conventions, dependencies, risks, and unknowns:
- Material unknowns: bounded assumption; least updating evidence; trigger to continue, change, or stop:

## Steps
- Verb-first atomic change: [affected boundary and independently verifiable functional slice]

## Verification
| Condition or risk | Hypothesis or what the check learned | Least-expensive reliable evidence | Why this evidence is sufficient | Rerun when | If it fails |
| --- | --- | --- | --- | --- | --- |
| | | | | | Diagnose the cause before rerunning or expanding checks. |

## Baseline, limits, and record
- Known baseline failures and their relevance:
- Evidence to retain, including informative failures or intermediate signals:
- Unreached conditions or limits on assertions:
- Stop when:
```

Make the verification rows specific. Name the affected boundary and trigger for each rerun, rather than saying to rerun tests after every change. Order steps so shared contracts or dependency foundations precede dependent slices; make each step verb-first and one atomic logical unit.

## Evidence and exceptions

- Do not use a test or code-volume ratio as a quality target. Choose evidence by the behavior and risk at hand.
- Do not use a blanket time limit as a substitute for completion conditions. Timebox exploration only when the plan identifies what decision the limit protects and what to do when it expires.
- Cover the relevant combinations, platforms, permissions, configurations, or integrations when impact requires them. A full matrix is not automatic evidence of proportional care.
- Record baseline failures separately. Do not treat a pre-existing failure as caused by the change, silently ignore it, or call the validation clean without its context. Do not require a deliberately failing baseline for every feature; when it is explicitly agreed, keep it binding.
- For a bug fix, include a regression test or equally durable reproduction that would fail for the reported defect. If that is infeasible, state why and retain the strongest practical evidence.
- Treat documentation, runbooks, configuration guidance, and operational instructions as potentially operationally risky when people or automation will act on them. Verify the affected instruction or workflow proportionately.
- Do not claim an outcome from a check that did not reach the relevant assertion. Mark skipped, blocked, inconclusive, or weak evidence plainly; reserve strong assertions for directly reached conditions with strong evidence. When an unreached or weak assertion is corrected, check the affected behavior again.
- When measuring success rates, retain initial failures. Report retries and recoveries separately; do not convert a failed first attempt into an initial success.

## Plan review

Check that the plan identifies the outcome, protects each product requirement, and makes each expensive action earn its cost. Confirm that discovery was read-only and sufficient to identify the relevant boundaries, conventions, dependencies, risks, and unknowns. Confirm that material unknowns have a bounded assumption, least updating evidence, and a continue/change/stop trigger, with greater investigation for irreversible decisions. Replace implementation suggestions with equivalent cheaper approaches when they preserve the same completion conditions. Reject reductions that silently weaken required behavior, security, or evidence.

Is it clear when the implementation is finished?
Does every expensive requirement provide a distinct benefit?
Can the implementing agent choose an equivalent, less expensive approach?
