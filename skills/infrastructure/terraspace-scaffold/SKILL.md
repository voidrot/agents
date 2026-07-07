---
name: terraspace-scaffold
description: Use when creating Terraspace stacks or modules, choosing app/stacks versus app/modules, inspecting terraspace list, or preserving generated starter Terraform files.
---

# Terraspace Scaffold

Use this skill when adding a new Terraspace stack or reusable module.

## Workflow

1. Inspect existing project components first:

   ```sh
   terraspace list
   ```

   Also check the project-local `app/stacks` and `app/modules` directories for naming and layout conventions.
2. Create a stack for a deployable, business-specific root module:

   ```sh
   terraspace new stack NAME
   ```

   Terraspace creates it under `app/stacks/NAME` with starter Terraform files such as `main.tf`, `variables.tf`, and `outputs.tf`.
3. Create a reusable module for shared infrastructure building blocks:

   ```sh
   terraspace new module NAME
   ```

   Terraspace creates it under `app/modules/NAME` with starter Terraform files.
4. Keep reusable modules environment-agnostic. Pass environment, account, region, and naming differences through variables or Terraspace layering.

## Constraints

- Do not use an unverified `--project` flag in generator examples.
- Do not duplicate an existing stack or module name without checking `terraspace list` and the local directories.
