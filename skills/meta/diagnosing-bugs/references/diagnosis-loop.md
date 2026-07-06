# Diagnosis Loop Reference

## Phase 1 — Build a Feedback Loop

If you have a tight pass/fail signal for the bug, bisection, hypotheses, and instrumentation can consume it. If you do not, code reading will usually turn into guessing.

Try these loop types in roughly this order:

1. Failing test at the seam that reaches the bug.
2. Curl or HTTP script against a running dev server.
3. CLI invocation with fixture input and expected output.
4. Headless browser script that asserts DOM, console, or network behavior.
5. Replay of a captured request, payload, trace, or event log.
6. Throwaway harness that exercises the bug path through one function or service.
7. Property or fuzz loop for intermittent wrong output.
8. Bisection harness for commit, dataset, or version regressions.
9. Differential loop comparing old vs new version or config.
10. Human-in-the-loop script using `scripts/hitl-loop.template.sh`.

Tighten the loop until it is:

- **Red-capable** — catches the user's exact symptom.
- **Deterministic** — same verdict every run, or a high reproduction rate for flakes.
- **Fast** — seconds, not minutes.
- **Agent-runnable** — unattended unless the HITL script is explicitly used.

If no loop can be built, stop and list what you tried. Ask for access, a captured artifact, or permission for temporary instrumentation.

## Phase 2 — Reproduce and Minimize

Run the loop and confirm the failure matches the user's report. Capture the exact symptom: error, wrong output, timing, or visible behavior.

Then shrink the scenario one variable at a time. Remove inputs, config, callers, data, and steps while rerunning the loop. Stop when every remaining element is load-bearing.

## Phase 3 — Hypothesize

Write 3–5 ranked hypotheses before testing. Each one must be falsifiable:

> If `<cause>` is true, then `<probe or change>` will make `<observable result>` happen.

Share the ranked list when user domain knowledge could re-rank it, but do not block if they are unavailable.

## Phase 4 — Instrument

Map every probe to one hypothesis. Change one variable at a time.

Prefer:

1. Debugger or REPL inspection when practical.
2. Targeted logs at boundaries that distinguish hypotheses.
3. Never broad "log everything" instrumentation.

Tag temporary logs with a unique prefix such as `[DEBUG-a4f2]` so cleanup is mechanical.

For performance regressions, establish a baseline measurement or profile before changing code.

## Phase 5 — Fix and Regression Test

When a truthful seam exists, turn the minimized repro into a failing regression test before the fix. A truthful seam exercises the real bug pattern as it happens in production, not a shallower coincidence.

If no truthful seam exists, document that as an architecture finding, apply the fix, and keep the original loop as evidence.

After the fix:

1. Watch the regression test pass, if one exists.
2. Rerun the original unminimized loop.
3. Confirm the user's reported symptom is gone.

## Phase 6 — Cleanup and Postmortem

Before declaring done:

- Original repro no longer reproduces.
- Regression test passes, or the absence of a seam is documented.
- Temporary `[DEBUG-...]` instrumentation is removed.
- Throwaway harnesses are deleted or clearly marked.
- The proven cause is stated in the handoff, commit, or PR notes.

Then ask what would have prevented the bug. If the answer is architectural, hand the evidence to an architecture-improvement workflow after the fix is in.
