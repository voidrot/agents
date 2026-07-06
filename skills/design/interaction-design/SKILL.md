---
name: interaction-design
description: Use when designing or implementing microinteractions, feedback, motion, transitions, gestures, loading states, empty states, or interaction polish for user-facing interfaces.
---

# Interaction Design

Use this skill for focused design work in this task family. Keep the active guidance concise, and open supporting references only when their detail is needed.

## When to use

- Adding or reviewing motion, transitions, feedback, gesture, or microinteraction behavior.
- Improving loading, empty, error, success, hover, focus, drag/drop, or notification states.
- Balancing delight, usability, performance, and accessibility in interaction design.

## Workflow

1. Identify the user intent, state change, input method, platform conventions, and accessibility needs.
2. Decide what feedback is needed: confirmation, progress, affordance, continuity, or recovery.
3. Choose motion and timing that clarifies cause/effect without blocking task completion.
4. Check reduced motion, keyboard/screen-reader paths, performance, interruption, and edge states.
5. Specify implementation guidance and validation scenarios for the interaction states.

## Constraints

- Do not add motion that obscures information, delays tasks, or ignores reduced-motion preferences.
- Always preserve keyboard, focus, screen-reader, and non-pointer interaction paths.
- Prefer purposeful feedback over decorative animation.

## References

Read only the sections needed for the task:

- [references/microinteraction-patterns.md](references/microinteraction-patterns.md) — Feedback, state, affordance, and microinteraction patterns.
- [references/animation-libraries.md](references/animation-libraries.md) — Library choices and implementation trade-offs for motion.
- [references/scroll-animations.md](references/scroll-animations.md) — Scroll-linked and reveal animation guidance.
- [references/full-guidance.md](references/full-guidance.md) — Source guidance preserved from the original skill.

## Output

Return an interaction plan with states, timing, accessibility constraints, implementation notes, and validation scenarios.
