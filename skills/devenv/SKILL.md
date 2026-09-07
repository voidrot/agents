---
name: devenv
description: "Configure, migrate, debug, and verify devenv.sh development environments. Use when a request involves devenv.nix, devenv.yaml, devenv.lock, devenv shell/test/up, languages.*, services.*, processes, tasks, profiles, git hooks, inputs, or SecretSpec; use Nix-specific guidance separately for general Nix syntax, flakes, overlays, and NixOS."
---

# Devenv

Build and maintain devenv.sh environments without confusing devenv modules with general Nix or NixOS configuration.

## Workflow

1. **Establish the project state.**
   - Read repository instructions and inspect `devenv.nix`, `devenv.yaml`, `devenv.lock`, imported modules, and the current diff.
   - Run `devenv --version` and use that installed version as the compatibility target unless the user specifies another.
   - Treat `.devenv/` as generated state, not configuration to copy or edit.
   - For a new project, confirm the destination does not already contain conflicting configuration before running `devenv init`.

2. **Verify changing interfaces before editing.**
   - Query current documentation with Context7 library `/cachix/devenv`, or use the official devenv option reference and changelogs when Context7 is unavailable.
   - Check exact `languages.*`, `services.*`, `git-hooks.*`, profiles, process-manager, and SecretSpec option shapes instead of recalling them from memory.
   - For migrations or lock updates, inspect `devenv changelogs` and state the source and target versions. Mark behavior `UNCONFIRMED` if it cannot be verified.

3. **Put each concern in the correct file.**
   - Use `devenv.yaml` for inputs and repository-level Nix policy such as explicitly approved unfree or insecure packages.
   - Use `devenv.nix` or imported devenv modules for packages, `languages.*`, `services.*`, scripts, tasks, processes, profiles, hooks, tests, and shell behavior.
   - Change inputs with `devenv inputs` or the smallest YAML edit, then run `devenv update <input-name>` for each intended input. A bare `devenv update` refreshes every input; use it only when that is deliberate. Do not hand-edit `devenv.lock`.
   - Use `packages` for binaries only. Prefer the relevant `languages.*` module when toolchain integration, version selection, or language-specific tooling is required.
   - Use `scripts.<name>` for commands exposed in the shell, `tasks.<name>` for dependency-ordered work, and `processes.<name>` for long-running programs started by `devenv up`.
   - Keep `enterShell` fast, deterministic, and offline-capable. Do not hide slow, networked, or stateful setup in shell entry.

4. **Make the smallest compatible change.**
   - Preserve existing inputs, imports, platform conditions, profiles, and project naming conventions.
   - Prefer built-in devenv modules over hand-written service wrappers when the module supports the requirement.
   - When behavior depends on a process manager or devenv release, configure it explicitly only after verifying the installed version's option name.
   - Do not add profiles, custom outputs, containers, or extra inputs unless the current task needs them.

5. **Keep secrets out of evaluation.**
   - Treat `env.*` values as public configuration; Nix expressions and evaluated values may be copied into the Nix store, cache, logs, or derivations.
   - Do not place credentials in `devenv.nix`, `devenv.yaml`, Nix strings, or dotenv-backed evaluation. Current devenv documentation deprecates dotenv for secrets.
   - Prefer devenv's current SecretSpec integration or pass secret file paths/runtime environment values without interpolating their contents into Nix.
   - Never print secret values while diagnosing the environment. Do not enable unfree or insecure packages without explicit project or user approval.

6. **Validate in increasing-cost order.**
   - Run `devenv info` to evaluate the environment and inspect the resulting configuration.
   - Run `devenv test` when the project defines `enterTest` or git hooks; use `devenv test --override-dotfile` when validation should not reuse local `.devenv` state.
   - Run the affected command through `devenv shell -- <command>` and execute the project's focused tests or checks.
   - For tasks, use `devenv tasks run <task>`. For processes, start `devenv up` only when runtime verification is necessary, observe readiness or logs, and stop what was started with `devenv down` or the applicable process command.
   - If inputs changed, confirm the lockfile diff is limited to the intended inputs. Report every check run and any runtime or platform checks skipped.

## Failure handling

- For an unknown option or type mismatch, compare the installed version with the current option reference; do not guess a renamed path or add an implicit fallback.
- For a missing package, use `devenv search` and verify the selected input exposes it on every supported system.
- For a migration failure, separate evaluation errors from service/runtime errors and apply one documented migration at a time.
- For state-sensitive failures, reproduce with `devenv test --override-dotfile` before deleting generated state. Do not remove project data or service volumes as a troubleshooting shortcut.
- If validation requires unavailable credentials, network access, services, or another platform, stop at the strongest safe check and state the exact unverified requirement.

## Boundary

Use a Nix-focused skill for Nix language syntax, flakes, overlays, derivations, or NixOS modules. Use this skill when devenv's CLI, module options, lifecycle, or generated environment is the subject.
