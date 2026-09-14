---
name: problem-solving
description: Diagnose a concrete software failure, unexpected behavior, performance regression, or problem-specific algorithm choice through reproduction, falsifiable experiments, and root-cause evidence; use when the cause or correct approach is uncertain, not for routine implementation or generic planning.
---

# Problem Solving

Use this skill to establish why an observed system outcome differs from its required outcome, or to select an algorithm when the problem's constraints make the correct approach uncertain. Own the diagnosis through evidence, then make the smallest justified correction. Do not use it for routine implementation with an already-established approach, generic coding style, project planning, language instruction, or broad refactoring.

## Workflow

1. **Observe the discrepancy and boundary.** Record the desired observable behavior, actual observable behavior, affected inputs, timing, impact, and material environment, version, and deployment facts. Record relevant recent code, configuration, dependency, and deployment changes. Separate facts from interpretations. Read the relevant contract, callers, tests, configuration, and operational artifacts before modifying code. Preserve secrets: use environment-variable names and redact values, tokens, headers, and sensitive payload fields in retained evidence.

2. **Choose a decisive signal.** Create or locate the narrowest unattended check that can distinguish the reported outcome from the required one: an existing focused test, a minimal command with fixture data, a trace replay, a controlled request, or a benchmark/profiler for performance. Assert the symptom rather than merely checking that execution completes. Run it and retain the command, inputs, environment facts that matter, and result.
   - If it reproduces reliably, use it as the working signal.
   - If it is intermittent, control time, randomness, ordering, shared state, and external dependencies; measure reproduction rate and preserve a representative artifact. Continue only when the signal is informative enough to compare probes.
   - If it cannot be reproduced safely, do not claim a cause or implement a speculative fix. Request the smallest missing artifact or access, or obtain approval for bounded temporary instrumentation.

3. **Minimize without changing the symptom.** Remove inputs, setup, dependencies, and steps one at a time, rerunning the signal after each removal. Keep only conditions that change the result. Contrast a failing case with the nearest passing case when one exists. Stop minimizing when further removal no longer improves the decision or would discard a necessary production condition.

4. **Model the relevant system.** Trace data, control, state, and error flow across the smallest affected boundary. Identify ownership, preconditions, invariants, side effects, ordering, concurrency or lifecycle edges, and external contracts. Prefer direct evidence from source, tests, logs, traces, metrics, query plans, or documentation over assumptions. Treat a suspicious pattern or code smell as a lead, not proof.

5. **Hypothesize competing, falsifiable causes.** Write two to five ranked causes. For each, state the predicted observation and the smallest reversible probe that distinguishes it from the alternatives. Include an environmental or contract misunderstanding when the evidence permits it. Do not bundle probes or change production behavior just to make a theory fit.

   | Hypothesis | Prediction | Discriminating, reversible probe | Result |
   | --- | --- | --- | --- |
   | | | | |

6. **Discriminate with one-variable probes.** Prefer inspection, debugger state, a controlled fixture, a temporary local override, or narrowly scoped tagged instrumentation. Run the decisive signal after every material probe. Measure performance before changing it; compare like workloads and record the baseline, elapsed time or resource measure, and variance. Remove temporary instrumentation and probes once they have answered their question.
   - Reject a hypothesis whose predicted observation does not occur.
   - If results contradict all hypotheses, revisit the model, inputs, and signal; then create new hypotheses rather than reinterpreting evidence.
   - If a probe exposes security, data-loss, or production-safety risk, stop it, restore the safe state, and escalate with the evidence.

7. **Analyze the root cause and correction boundary.** Name the smallest condition that explains the reproduced symptom and why the evidence excludes the nearest alternatives. Select the narrowest correction at the owner of that condition. Preserve unrelated outputs, errors, side effects, ordering, compatibility, and public contracts. Do not fold in cleanup, redesign, speculative abstraction, or unmeasured optimization. For implementation mechanics, use `efficient-coding`; for focused regression coverage, use `efficient-testing`.

8. **Make problem-specific algorithm decisions deliberately.** When the uncertainty is algorithmic rather than a defect:
   - Define inputs, outputs, correctness properties, data-size bounds, update/query mix, ordering, memory limit, and unacceptable failure modes. Do not optimize against an invented scale.
   - Compare only plausible approaches, including the simplest direct one. State their time and space costs in terms of the actual variables and their operational trade-offs, such as determinism, numerical error, latency tail, or mutation requirements.
   - Choose the simplest approach that meets measured or stated constraints. Use a more complex data structure, cache, parallelism, or approximation only when a named constraint and evidence require it.
   - Establish a correctness oracle: small known cases, boundary cases, invariants, a reference implementation, or differential results. Benchmark only with representative workload and baseline; retain the measurement that justified an optimization.

9. **Implement after evidence.** First add or preserve the minimal durable regression at the seam that reaches the real failure, when practical. Confirm it fails before the correction if the baseline is available; otherwise record why that proof was not possible. Apply one coherent change that addresses the identified cause. If the correction invalidates the diagnosis, revert it and return to the hypotheses rather than stacking fixes.

10. **Verify the resolution and stop.** Rerun the original unminimized reproduction, the regression or oracle, and the smallest affected checks. For a performance change, repeat the representative measurement and compare it with the baseline; do not infer improvement from a single noisy run. Inspect the diff for temporary instrumentation, fixture contamination, unrelated changes, and weakened behavior. Stop when the required outcome is directly demonstrated and no unresolved material risk remains.

## Failure handling and escalation

Escalate rather than guess when any of these prevents a safe conclusion:

- the original symptom cannot be reproduced or artifacts are insufficient;
- multiple causes remain consistent with available evidence and choosing one would be irreversible or high-impact;
- a required environment, credential, dataset, device, or production observation is unavailable;
- the failure crosses an ownership boundary or depends on an external service whose contract cannot be verified;
- the proposed correction risks data integrity, security, compatibility, or unacceptable performance.

Report the desired and actual behavior, exact signal and result, minimized conditions, rejected and remaining hypotheses, root-cause evidence (or why it is not established), changes made, verification run and skipped, and the smallest next decision or artifact needed. Do not label a workaround, correlation, or passing unrelated test as a root cause.
