---
name: security-scan
description: Use when scanning Claude Code or agent configuration for prompt-injection, permission, MCP, hook, secret, and config risks with AgentShield or similar tooling.
origin: ECC
---

# Security Scan

Use this skill for automated/security-tool inspection of agent configuration. For application code, product behavior, auth, APIs, or user-data security review, use `security-review` instead.

## When to activate

- Setting up or reviewing Claude Code / agent configuration.
- Changing `.claude/settings.json`, `.claude/mcp.json`, hooks, agent files, or project instruction files such as `CLAUDE.md` where present.
- Auditing permissive tool allowlists, MCP servers, shell hooks, hardcoded secrets, or prompt-injection surfaces.
- Adding AgentShield checks to local workflow or CI.

## Boundary

- **Use this skill** for configuration scanning and hardening agent/Claude Code surfaces.
- **Use `security-review`** for code-level and product-level security analysis.

## Scan workflow

1. Identify the config roots to scan: project root, `.claude/`, project instruction files, hooks, MCP config, and agent definitions if present.
2. Run the scanner in read-only mode first and capture severity, file, rule, and remediation.
3. Manually inspect high-risk findings before applying fixes.
4. Apply safe fixes only when the scanner marks them auto-fixable and the project owner accepts the behavior change.
5. Re-run the scan and report remaining findings, accepted risk, and CI follow-up.

## What to inspect

| Surface | Checks |
| --- | --- |
| Project instruction files | Hardcoded secrets, auto-run instructions, prompt-injection patterns |
| Claude settings | Overly broad allowlists, missing deny rules, bypass flags |
| MCP config | Risky servers, hardcoded env values, shell execution, supply-chain risk |
| Hooks | Command injection, unquoted interpolation, exfiltration, silent failures |
| Agent definitions | Unnecessary tool access, vague permissions, injection surface, missing routing boundaries |

## References

- [AgentShield usage](references/agentshield-usage.md) — install, local commands, output formats, auto-fix, and deep analysis.
- [CI examples](references/agentshield-ci.md) — GitHub Actions snippets and gating guidance.
- External: [AgentShield repository](https://github.com/affaan-m/agentshield), [npm package](https://www.npmjs.com/package/ecc-agentshield).

## Output

Return scan command used, scope, findings by severity, files affected, fixes applied or recommended, and any manual review needed. Do not present example paths like `CLAUDE.md` or `agents/*.md` as guaranteed local files unless they exist in the target repo.
