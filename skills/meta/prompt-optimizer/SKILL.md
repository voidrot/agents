---
name: prompt-optimizer
description: Use when the user asks to improve, rewrite, critique, or optimize a prompt; output an optimized prompt and rationale without executing the underlying task.
origin: community
metadata:
  author: YannJY02
  version: "1.0.0"
---

# Prompt Optimizer

Analyze a draft prompt, identify missing context, recommend workflow components, and return a ready-to-paste optimized prompt. Advisory role only.

## When to Use

- User asks to optimize, improve, rewrite, critique, or draft a prompt.
- User asks how to prompt an agent/tool for a task.
- User provides a prompt and asks for feedback or a better version.
- Chinese triggers include `优化prompt`, `改进prompt`, `怎么写prompt`, and `帮我优化这个指令`.

## Do Not Use When

- The user wants the task executed directly, says `just do it`, or says `直接做`.
- The user asks to optimize code, performance, or an implementation rather than a prompt.
- The user needs an inventory, configuration fix, or implementation plan instead of prompt text.

## Workflow

1. Detect project context only from available local files and note uncertainty when the prompt is abstract.
2. Classify intent, scope, lifecycle stage, missing context, risks, and acceptance criteria.
3. Recommend relevant commands, skills, agents, or model choices only when they are grounded in the available ecosystem.
4. Ask up to three clarification questions if critical missing information would materially change the optimized prompt.
5. Output diagnosis, recommended components, full optimized prompt, quick version, and rationale in the user’s language.

## Constraints

- Do not execute the underlying task, write files, or run commands as part of this skill’s output.
- Do not reference missing local files such as `CLAUDE.md` as required inputs; detect them opportunistically if present.
- Do not hardcode stale component catalogs when the current project can be inspected.

## Supporting Material

- Read `references/optimization-pipeline.md` for the full phased pipeline, tables, examples, and output format.
