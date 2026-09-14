---
name: anti-slop
description: Critique and revise code, prose, or implemented web/visual design to remove unsupported complexity, generic filler, redundant artifacts, and speculative additions; use when a requested change or review should become smaller, more specific, and evidence-backed without discarding intentional constraints.
---

# Anti-Slop

Use this skill to make a requested artifact more direct and intentional. “Slop” is an editorial diagnosis, not evidence of authorship or incompetence. Preserve requirements, established conventions, and constraints that have a demonstrated purpose.

Use it for a review-only request or a requested revision of code, prose, or an implemented web interface. Do not use it to invent a product direction, replace a design system, rewrite an unfamiliar subsystem, or prescribe a universal style. Use `efficient-testing` when a changed code contract needs focused test coverage; use a design-focused skill when the task is to create visual direction rather than critique or reduce an existing implementation.

## Workflow

1. **Establish the artifact and requested outcome.** Read the request, target files or rendered result, applicable repository guidance, and nearby examples. Identify the audience or user task, observable contract, explicit constraints, and allowed write boundary. For code, identify callers, tests, errors, side effects, ordering, and performance-sensitive paths. For prose, identify source, audience, required facts, author voice, and protected quotations or structured content. For web work, identify the product brief, existing components and tokens, required states, and interaction intent.
   - If the contract or a material constraint is unknown, inspect the smallest relevant evidence. If it remains unknown and removal could change behavior, meaning, accessibility, security, or a product decision, do not remove it; report the missing evidence.
   - Treat a requirement, compatibility boundary, measured optimization, accessibility support, or established component pattern as intentional until evidence shows otherwise.

2. **Collect observable evidence before judging.** Compare the artifact with its contract and local conventions. Prefer a focused test, deterministic reproduction, rendered interface, concrete reader-facing claim, duplication that is actually maintained twice, or measured timing over an intuition that something feels generic.
   - For a reported defect, first produce the smallest deterministic failing signal and reduce the case. Test one falsifiable hypothesis at a time; do not guess through a bug.
   - For web work, render or inspect the existing result when practical. Check task hierarchy, product-specific content, overflow and narrow widths, loading/empty/error/success/disabled/recovery states that the product requires, keyboard and focus behavior, labels, contrast, text resize, and visible interaction feedback.
   - If rendering, reproduction, or measurement is unavailable, state that limit. Restrict findings to directly inspectable artifacts and do not claim runtime or visual outcomes.

3. **Classify only material candidates.** Name the concrete evidence and the smallest correction for each candidate. Common candidates are:
   - code that duplicates a maintained responsibility, obscures control flow, adds an unused abstraction or configuration surface, retains dead artifacts, or optimizes without a measured need;
   - prose that buries the point, repeats itself, uses generic transitions or conclusions, makes an unsupported claim, leaks a placeholder, or substitutes vague language for a needed fact;
   - web/visual work that ignores the existing system, hides the product task behind generic decoration, introduces arbitrary effects or controls, fails a meaningful state, or has observable responsive or accessibility breakage.

   A smell is a prompt to investigate, not an automatic defect. Do not flag a familiar pattern, a concise sentence, deliberate repetition, or a visual choice solely because it is common. In review-only mode, return no more than three material findings, ordered by user impact; if none are supported, say so.

4. **Choose the smallest complete revision.** Remove first. Then consolidate, clarify, or replace only when removal would leave a broken contract. Keep changes within the requested scope and avoid opportunistic cleanup elsewhere.
   - **Code:** preserve inputs, outputs, errors, side effects, ordering, security properties, and required performance. Prefer conventional, readable local patterns over clever compression or a new abstraction. Change behavior only when the request explicitly requires it; isolate a behavior fix from unrelated cleanup when feasible.
   - **Prose:** lead with the concrete point. Use specific actors, actions, evidence, and verification where the source supports them. Preserve voice, facts, stance, citations, quotations, headings, and required terminology. Never invent a fact, citation, example, authority, personality, or stronger conclusion to make text sound better.
   - **Web/visual design:** extend established tokens, components, and interaction conventions. Make the product’s objects, priorities, and next action clear rather than applying a generic visual recipe. Use semantic structure and native controls where they meet the need; do not add ARIA or decoration without a concrete gap. Do not impose a preferred palette, typography, density, animation, or layout absent product evidence.

5. **Make one coherent diff and inspect it.** Keep only edits necessary to address the supported finding and remove artifacts made obsolete by that edit. Re-read the changed context and inspect the diff for accidental rewrites, duplicated alternatives, unused imports/assets/configuration, altered protected content, and scope expansion.
   - If a proposed correction requires a new dependency, API, configuration flag, component system, data model, or performance optimization, reject it by default. Add it only when the request and evidence establish a concrete need that the smaller diff cannot meet.
   - If a revision makes the artifact less clear, less accessible, changes an unrequested contract, or cannot be supported by the evidence, revert that revision and report the constraint instead.

6. **Verify the claimed outcome proportionately.** Rerun the narrowest existing check that reaches the changed contract, and broaden only when shared boundaries or project policy require it. For a bug fix, retain a regression test or equally durable reproduction that distinguishes the defect. For prose, compare every changed claim against its source and read the result as its intended audience would. For web work, inspect the changed result at relevant narrow widths and text zoom, operate it by keyboard, verify focus and required states, and run available automated checks as partial evidence rather than proof of conformance.
   - Verify that a code test would fail for the broken behavior, not merely that it passes afterward. Verify that a performance claim has before-and-after measurements on comparable inputs.
   - If a check fails, classify it as a product defect, incorrect revision, test or tooling problem, unavailable prerequisite, or baseline failure. Preserve the result, fix the identified cause, and rerun only checks affected by that cause. Do not weaken assertions, add retries, or silently treat an unavailable check as passing.

7. **Report the decision and evidence.** State the artifact reviewed, supported findings or why no change was justified, intentional constraints preserved, and the smallest diff made. State exact validation run and result, skipped or blocked checks with their prerequisite, and remaining risk. For review-only work, distinguish required corrections from optional observations.

## Safe defaults

- Leave a working artifact unchanged when no concrete evidence supports a net improvement.
- Prefer deletion and local clarification to new layers, options, assets, visual motifs, or generalized frameworks.
- Preserve externally observable behavior and authorial/product intent unless an explicit requirement changes it.
- Make uncertainty visible rather than filling it with plausible detail.
- Stop when the requested outcome has direct, proportionate evidence; do not polish merely to make a diff look more substantial.
