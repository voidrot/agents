---
name: home-manager
description: "Configure, migrate, debug, and safely activate Home Manager user environments. Use when a request involves home.nix, homeConfigurations, home-manager.users, home-manager build/switch, home.stateVersion, programs.*, services.*, home.file, xdg.configFile, dotfiles, activation, generations, backups, or file collisions; use NixOS guidance for system-wide configuration and general Nix guidance for language, flakes, and packaging."
---

# Home Manager

Manage user packages, programs, services, and dotfiles declaratively without overwriting personal data or confusing standalone and module-based activation.

## Workflow

1. **Identify the integration mode and target.**
   - Read repository instructions and inspect the Home Manager import tree, `flake.nix` and lockfile when present, `home.nix`, host/user modules, and the current diff.
   - Determine whether Home Manager is standalone, a NixOS module, or a nix-darwin module. Record the configuration output name, username, home directory, target platform, and pinned nixpkgs/Home Manager revisions.
   - Preserve the repository's module structure. Do not edit files under a generated Home Manager profile or Nix store path; locate the declarative source that owns them.

2. **Verify current options and release compatibility.**
   - Query the official manual and option reference for the pinned Home Manager release. Context7 library `/nix-community/home-manager` provides current project documentation.
   - Confirm `programs.*`, `services.*`, `home.*`, and `xdg.*` option names, types, platform support, defaults, and release notes before editing.
   - Keep the Home Manager release compatible with the selected nixpkgs branch. Follow the repository's pinning convention and mark unresolved version-specific behavior `UNCONFIRMED`.

3. **Use the narrowest declarative option.**
   - Prefer a dedicated `programs.<name>` or `services.<name>` module over manually writing the same application's files or service units.
   - Use `home.packages` for user-visible packages that have no needed Home Manager module integration.
   - Use `xdg.configFile` for XDG configuration and `home.file` for other files under the user's home. Keep templates and source files inside the repository when they are intended to be versioned.
   - Use activation scripts only when no declarative option can express the requirement. Make them idempotent, ordered through Home Manager's activation DAG, and explicit about failures.
   - Keep system packages, system services, boot, networking, hardware, users, groups, and machine-wide policy in NixOS or nix-darwin rather than Home Manager.

4. **Protect compatibility, personal files, and secrets.**
   - Do not change `home.stateVersion` merely because Home Manager is upgraded. It preserves compatibility with the release used when the configuration was first established; change it only for a reviewed state migration.
   - Treat an activation collision as protection for an unmanaged file. Inspect ownership and content before choosing to import, move, or back it up.
   - Do not use `force`, `overwriteBackup`, `-b`, or a backup command as a generic way to make activation pass. Obtain explicit approval for overwriting or relocating personal files, and choose a non-colliding backup destination.
   - Do not interpolate passwords, tokens, private keys, or secret contents into Nix expressions because evaluated values may enter the Nix store, cache, or logs. Use the repository's established secret manager or runtime credential/file mechanism.
   - Never print secrets while debugging. Require explicit authorization for account, authentication, security, privacy, destructive, or production-control changes.

5. **Build with the correct owner.**
   - For standalone Home Manager, run `home-manager build` first, adding the repository's `--flake .#<configuration>` selector when required.
   - For a Home Manager flake without the CLI, build the selected `homeConfigurations.<name>.activationPackage` output using the repository's established command.
   - For the NixOS module, validate through the owning `nixosConfigurations.<host>` output and `nixos-rebuild build`; do not run standalone `home-manager switch` against a configuration owned by the system generation.
   - For the nix-darwin module, validate through the owning Darwin configuration and repository command.
   - Run repository checks that cover formatting, evaluation, assertions, and platform-specific configuration. A successful build does not prove activation will preserve unmanaged files or that user services will start correctly.

6. **Inspect and activate deliberately.**
   - Review the generated result and activation warnings, especially changed symlinks, removed files, package changes, and service definitions.
   - For standalone mode, run `home-manager switch` only after a successful build and authorization to alter the user's home. Use an explicit flake selector when multiple configurations exist.
   - For NixOS or nix-darwin module mode, activate through the owning system command so Home Manager and the system generation remain consistent.
   - After activation, verify affected files resolve to the intended source, programs load the configuration, and user services are healthy with the platform's service manager.
   - Report the output built, integration mode, commands run, activation performed, backup or collision decisions, runtime checks, and anything skipped.

## Failure handling

- For an unknown option or type mismatch, inspect the option definitions for the pinned release; do not guess a renamed path or hide the error with a forced value.
- For an assertion failure, read the complete assertion and fix the incompatible settings rather than disabling the guard.
- For a file collision, stop before mutation, compare the existing file with the proposed managed source, and ask for a disposition when ownership is ambiguous.
- For activation failures, use the activation log to identify the failing DAG step. Fix idempotency, ordering, permissions, or platform assumptions at the source; do not delete unrelated home files.
- For regressions, inspect `home-manager generations` in standalone mode, verify the rollback target, then use `home-manager switch --rollback` or the pinned release's documented prior-generation activation procedure. In module mode, roll back through the owning NixOS or nix-darwin generation.
- If the target user, home directory, output name, integration mode, or backup disposition is unknown, stop after a non-activating build and state what must be confirmed.

## Boundary

Use NixOS guidance for machine-wide operating-system modules and system activation. Use general Nix guidance for language syntax, flakes, nixpkgs packaging, overlays, and derivations. Use this skill for Home Manager's user-scoped modules, files, programs, services, activation, and generations.
