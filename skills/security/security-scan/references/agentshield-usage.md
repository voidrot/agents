# AgentShield usage

AgentShield scans Claude Code and agent configuration for risky permissions, prompt-injection surfaces, hardcoded secrets, MCP risk, and hook issues.

## Local usage

```bash
# Check availability
npx ecc-agentshield --version

# Scan the current project
npx ecc-agentshield scan .

# Scan a specific configuration path when present
npx ecc-agentshield scan --path .claude

# Filter by severity
npx ecc-agentshield scan --min-severity medium
```

## Output formats

```bash
# Terminal report
npx ecc-agentshield scan .

# JSON for automation
npx ecc-agentshield scan . --format json

# Markdown report
npx ecc-agentshield scan . --format markdown

# HTML report
npx ecc-agentshield scan . --format html > security-report.html
```

## Auto-fix

```bash
npx ecc-agentshield scan . --fix
```

Use auto-fix only after reviewing the proposed changes. Expected safe fixes may include replacing hardcoded secrets with environment references or tightening broad permissions. Manual-only findings still need human review.

## Deep analysis

If supported by the installed AgentShield version and configured credentials, deeper adversarial analysis may be available:

```bash
ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" npx ecc-agentshield scan . --opus --stream
```

Never paste real secrets into examples or prompts. Use environment variables supplied by the shell or CI secret store.

## Severity interpretation

- **Critical**: hardcoded secrets, unrestricted shell access, hook command injection, high-risk MCP execution.
- **High**: unsafe auto-run instructions, missing deny rules, excessive agent Bash access.
- **Medium**: silent hook failures, missing security hooks, auto-installing unpinned tools.
- **Info**: documentation or hygiene suggestions.
