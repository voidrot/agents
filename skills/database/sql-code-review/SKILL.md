---
name: sql-code-review
description: Use when reviewing SQL or database-access code for injection risk, permissions, data protection, maintainability, schema quality, and cross-database SQL anti-patterns.
---

# SQL Code Review

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Reviewing raw SQL, migrations, stored procedures, views, or query builders
- Checking SQL injection, least privilege, sensitive-data exposure, and audit behavior
- Finding maintainability problems such as unclear joins, SELECT *, weak constraints, or inconsistent naming
- Producing database-agnostic review findings across PostgreSQL, MySQL, SQL Server, Oracle, or similar SQL systems

## Quick Workflow

1. Identify the database dialect, execution path, and user-controlled inputs.
2. Check parameterization, privileges, sensitive columns, and audit requirements first.
3. Review schema constraints, data types, naming, joins, aggregation, and pagination.
4. Separate correctness/security findings from performance tuning suggestions.
5. Provide concrete SQL or application-code fixes with verification queries.

## Reference Routing

- Full review checklist and examples: [references/full-guidance.md](references/full-guidance.md)

## Boundaries

- Use `sql-optimization` for deep performance tuning after correctness and security are understood.
- Use `postgres-patterns` for PostgreSQL-specific implementation details.

## Expected Output

- Prioritized SQL review findings
- Security and data-protection risks
- Maintainability/schema recommendations
- Suggested fixes and validation checks
