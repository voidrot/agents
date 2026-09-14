# DESIGN.md format and tooling

Read this only when the repository has adopted the upstream Google Labs `DESIGN.md` format, or when a request specifically asks to validate, compare, or look up that format. The format is currently alpha; verify the installed tool and upstream specification before relying on version-sensitive details.

## Latest specification

- Canonical specification: <https://github.com/google-labs-code/design.md/blob/main/docs/spec.md>
- CLI-rendered specification for the resolved package version:

  ```bash
  npx @google/design.md spec
  npx @google/design.md spec --rules
  ```

The GitHub specification tracks upstream `main`; the CLI output describes the package version that `npx` resolves. Record which source was consulted when its difference could affect a decision.

## Optional checks

Run these only when the project already permits this CLI or explicitly asks for upstream-format validation. They can download or execute a package through `npx`; do not make them a prerequisite for ordinary visual/design review.

```bash
# Check one file; output is JSON and a nonzero status means errors.
npx @google/design.md lint DESIGN.md

# Make the intended JSON output explicit.
npx @google/design.md lint --format json DESIGN.md

# Compare a prior copy with the revised design system.
npx @google/design.md diff DESIGN-before.md DESIGN.md
```

On Windows shells where the `.md` executable name collides with file associations, use the documented alias:

```bash
npx -p @google/design.md designmd lint DESIGN.md
```

Treat lint or diff output as format/token evidence, not evidence that a rendered interface serves users well. Resolve errors before claiming format validity; investigate warnings in the product context rather than mechanically adding tokens, sections, or components.
