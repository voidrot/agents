---
name: terraspace-terrafile
description: Use when declaring Terraspace Terrafile modules, running terraspace bundle/update, managing vendor/modules, Terrafile.lock, Git/registry sources, or module lookup conflicts.
---

# Terraspace Terrafile

Use this skill when adding or updating external modules managed by Terraspace `Terrafile`.

## Workflow

1. Declare external modules in the project `Terrafile` with `mod`.

   ```ruby
   mod "vpc", source: "terraform-aws-modules/vpc/aws", version: "~> 5.0"
   mod "eks", source: "git@github.com:terraform-aws-modules/terraform-aws-eks.git", tag: "v19.0.0"
   mod "sg", source: "git@github.com:org/repo.git//modules/security-group?ref=v1.2.3"
   mod "sg_alt", source: "git@github.com:org/repo.git", subfolder: "modules/security-group", ref: "v1.2.3"
   ```

2. Fetch modules after editing `Terrafile`:

   ```sh
   terraspace bundle
   ```

   Terraspace downloads modules to `vendor/modules` and writes `Terrafile.lock`.
3. Update all modules or one selected module with:

   ```sh
   terraspace bundle update
   terraspace bundle update NAME
   ```

4. Reference modules from stacks through the shared modules path:

   ```hcl
   module "network" {
     source = "../../modules/vpc"
   }
   ```

   Terraspace looks in `app/modules` and `vendor/modules`; `app/modules` wins on name conflicts.
5. If using `export_to "app/modules"`, verify the target carefully. `export_purge` can delete folders.
6. For cache cleanup, use:

   ```sh
   terraspace clean all
   ```

## Constraints

- Pin registry and Git modules with versions, tags, or refs for reproducible environments.
- Keep heavily customized internal modules in `app/modules` instead of repeatedly patching vendored modules.
- Do not use `terraspace clean cache`; use the documented `terraspace clean all` command.
