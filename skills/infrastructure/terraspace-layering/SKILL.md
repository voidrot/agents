---
name: terraspace-layering
description: Use when configuring Terraspace tfvars precedence, environment-specific variables, config/stacks layering, backend expansion, or multi-region/account layering modes.
---

# Terraspace Layering

Use this skill when placing or debugging Terraspace tfvars and environment/account/region overrides.

## Workflow

1. Prefer current stack tfvars locations under `config/stacks/MOD/tfvars`:
   - `config/stacks/MOD/tfvars/base.tfvars`
   - `config/stacks/MOD/tfvars/dev.tfvars`, `prod.tfvars`, or another `TS_ENV` file
2. Treat `app/stacks/MOD/tfvars` as still valid but no longer the recommended primary location.
3. Put project-wide tfvars under `config/terraform/tfvars`, not an unverified `config/stacks/base.tfvars` path.
4. Use `base.tfvars` for shared defaults and `TS_ENV` files such as `dev.tfvars` and `prod.tfvars` for environment-specific values.
5. For Terraspace v2+ multi-region/account behavior, start with the default `simple` layering mode. Use `namespace` or `provider` modes only when the project needs wider account/provider layering.
6. For backend variables, use documented uppercase expansion tokens such as:

   ```ruby
   expansion(":REGION")
   ```

## Constraints

- Do not commit secrets or unique deployment overrides unless that matches the project policy.
- Keep tfvars placement consistent across stacks before adding new layering paths.
- Avoid implying backend expansion helpers are general tfvars helpers unless the project docs verify that context.
