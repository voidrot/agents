---
name: diagnosing-bugs
description: Use a tight feedback-loop workflow to diagnose bugs, regressions, flakes, crashes, or slow behavior before fixing them.
---

# Diagnosing Bugs

A disciplined route for hard bugs. Keep the working loop in `SKILL.md`; load [references/diagnosis-loop.md](references/diagnosis-loop.md) when you need the full phase checklist.

## When to Use

- The user asks to diagnose, debug, reproduce, or investigate a bug.
- A crash, regression, flaky behavior, wrong output, or performance symptom has an unclear cause.
- Previous fixes guessed at the cause or did not prove the symptom is gone.

## Workflow

1. **Build a red-capable loop.** Create one command or script that drives the exact symptom and can fail on this bug.
2. **Reproduce and minimize.** Run the loop, confirm it matches the user's report, then shrink inputs and steps until only load-bearing pieces remain.
3. **Rank hypotheses.** Write 3–5 falsifiable causes with predictions before changing code.
4. **Instrument one variable at a time.** Prefer debugger or targeted probes; tag temporary logs with a unique `[DEBUG-...]` prefix.
5. **Fix at the right seam.** Turn the minimal repro into a regression test when a truthful seam exists, apply the fix, and rerun the original loop.
6. **Clean up and explain.** Remove temporary probes, keep useful regression coverage, and state the cause that proved true.

## Constraints

- Do not form a code-change plan until a red-capable loop exists, unless you explicitly report why it cannot be built.
- For nondeterministic bugs, raise the reproduction rate instead of waiting for a perfect repro.
- For performance regressions, establish a measurement baseline before proposing optimizations.
- Use `scripts/hitl-loop.template.sh` only when a human must perform manual steps.

## Output

- Reproduction command and current red/green result.
- Minimal cause or ranked hypotheses, with evidence.
- Fix summary, regression coverage, and cleanup notes.

## Supporting Material

- [references/diagnosis-loop.md](references/diagnosis-loop.md) — full phase checklist and loop-building options.
- [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh) — template for unavoidable human-in-the-loop reproduction.
- Review references and assets with candidate material merged from `debugging-strategies` when the request overlaps that source's specialized workflow.
  - `references/debugging-strategies-merge-notes.md`
