---
name: mcp-server-patterns
description: Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API.
---

# MCP Server Patterns

Use this skill for mcp server patterns tasks where platform-specific implementation, architecture, or operational guidance is needed.

## When to Use

- Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP.

## Workflow

1. Decide whether the capability should be a tool, resource, prompt, or ordinary API.
2. Check the current MCP SDK and transport APIs before implementing server code.
3. Define schemas, error behavior, and client compatibility before wiring handlers.

## Constraints

- Prefer current official documentation for version-sensitive APIs, commands, deployment options, and configuration names.
- Keep generated guidance actionable and scoped to the user's project rather than restating broad background material.
- Preserve security, privacy, reliability, and rollback concerns when recommending platform changes.

## Supporting Material

- Read `references/full-guidance.md` for source guidance, examples, checklists, and detailed patterns.

## Expected Output

- A concise recommendation, implementation plan, review, or diagnostic report with assumptions, tradeoffs, and verification steps.
