# Description optimization

Read this before drafting a description or responding to a routing failure.

## Write a routing contract

A description should answer two questions in one compact statement:

1. **What** outcome or task class does the skill handle?
2. **When** should an agent select it?

Use concrete intent and domain terms from real requests. Include implicit intent: a request may omit the skill's internal label while clearly needing its outcome. Prefer a bounded task class over a broad role claim, and avoid making the wording so narrow that routine paraphrases cannot match.

Good revisions change the description only when the evidence concerns discovery. Do not compensate for missing procedures, unsafe defaults, or poor tools with more keywords.

## Tune with labeled cases

Build roughly 8–10 positive prompts that should activate the skill and 8–10 near-miss negatives that should not. Include direct requests, paraphrases, realistic shorthand, adjacent domains, and ambiguous wording. Keep a fixed split of about 60% train and 40% validation. Change wording on train results; select only with validation results; then test genuinely unseen cases.

Run each case about three times when the routing mechanism is stochastic. A rough threshold near 0.5 can help identify a weak trigger, but it is a decision aid rather than a universal acceptance guarantee. Record the runtime, model, prompt, expected decision, observed decision, repetitions, and any loading signal.

## Diagnose the result

- **False negative:** add an accurate, concrete task or domain signal that appeared in the request; do not overgeneralize from one phrase.
- **False positive:** clarify the boundary or add a discriminator that distinguishes the near miss.
- **Unstable outcome:** repeat with the same environment and preserve the trace before changing text.
- **Correct selection but poor completion:** leave routing evidence separate and improve the skill body instead.

## Source basis

- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) (authoritative source supplied for this skill; checked 2026-09-01)
