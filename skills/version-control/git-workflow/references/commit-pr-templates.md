# Commit and PR templates

## Conventional Commit shape

```text
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `revert`.

## Commit examples

```bash
git commit -m "fix(api): retry requests on 503 Service Unavailable"
git commit -m "feat(auth): add OAuth2 login"
git commit -m "docs(readme): update installation steps"
```

Avoid vague messages like `update`, `fix`, `WIP`, or `stuff` in shared history.

## `.gitmessage` template

```text
# <type>(<scope>): <subject>
#
# Why:
#
# Notes:
#
# Footer: closes #issue, BREAKING CHANGE: details
```

Enable with:

```bash
git config commit.template .gitmessage
```

## PR description template

```markdown
## What

Briefly describe the change.

## Why

Explain the motivation, user impact, or issue.

## How

Call out implementation details reviewers need.

## Testing

- [ ] Unit/integration tests updated
- [ ] Manual checks performed
- [ ] CI passes

## Risk

Migration, rollback, security, performance, or UX risks.

Closes #123
```

## Review checklist

For authors:

- [ ] Scope is focused and reviewable.
- [ ] CI passes.
- [ ] Tests/docs were updated when needed.
- [ ] Secrets and generated artifacts were not committed.

For reviewers:

- [ ] The change solves the stated problem.
- [ ] Edge cases and failure paths are covered.
- [ ] Security, data integrity, and maintainability risks were considered.
