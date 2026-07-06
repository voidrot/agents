# AgentShield CI examples

## GitHub Actions gate

```yaml
name: agent-config-security

on:
  pull_request:
    paths:
      - '.claude/**'
      - 'CLAUDE.md'
      - '**/agents/*.md'
      - '.github/workflows/**'

jobs:
  agentshield:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Scan agent configuration
        run: npx ecc-agentshield scan . --min-severity medium --format markdown
```

The path globs above are examples for repositories that use those files. Adjust them to the actual local configuration layout.

## Marketplace action form

If using the AgentShield GitHub Action and the version supports these inputs:

```yaml
- uses: affaan-m/agentshield@v1
  with:
    path: '.'
    min-severity: 'medium'
    fail-on-findings: true
```

Pin action versions according to your organization's supply-chain policy.
