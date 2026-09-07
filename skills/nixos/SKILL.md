---
name: nixos
description: "Configure, migrate, debug, and safely activate NixOS systems. Use when a request involves configuration.nix, nixosConfigurations, NixOS modules or options, hardware-configuration.nix, nixos-rebuild, systemd services, boot, networking, users, system.stateVersion, generations, rollbacks, or NixOS tests; use general Nix guidance for language, flakes, and packaging, and Home Manager for user-scoped configuration."
---

# NixOS

Maintain declarative NixOS systems without treating a successful evaluation as proof that activation is safe.

## Workflow

1. **Establish scope and target.**
   - Read repository instructions and inspect the module/import tree, `flake.nix` and `flake.lock` when present, host definitions, `configuration.nix`, and relevant hardware modules.
   - Identify the NixOS release or nixpkgs revision, target architecture, hostname, deployment method, and whether the machine is local, remote, or production.
   - Preserve unrelated changes. Treat `/etc/nixos/hardware-configuration.nix` as machine-derived input; do not regenerate or edit filesystems, boot, kernel, LUKS, RAID, or hardware settings unless the task requires it and the target facts are known.

2. **Verify current options.**
   - Use the official manual and option search for the target NixOS release. For current unstable documentation, Context7 library `/websites/nixos_manual_nixos_unstable` is available.
   - Confirm option names, types, defaults, renamed or removed options, service behavior, and release notes before relying on them.
   - Use the repository's pinned nixpkgs as the authority when it differs from online documentation. Mark unresolved version-dependent behavior `UNCONFIRMED`.

3. **Place policy in narrow modules.**
   - Extend the existing host and role structure instead of moving unrelated configuration into a new framework.
   - Keep reusable modules independent of a specific host; pass explicit data through module arguments only when an existing interface requires it.
   - Prefer NixOS service options over hand-written systemd units. Add custom units only for behavior the module cannot express.
   - Use `lib.mkIf` for conditional configuration and `lib.mkDefault` for overridable defaults. Use `lib.mkForce` only when deliberately resolving a known priority conflict and explain why.
   - Keep general Nix expressions, package derivations, overlays, and flake mechanics in their existing general-purpose modules rather than teaching them through NixOS policy.

4. **Protect compatibility and secrets.**
   - Do not change `system.stateVersion` merely because NixOS or nixpkgs is upgraded. It records the release whose persistent-state defaults the installation follows; change it only as part of a reviewed state migration.
   - Do not interpolate passwords, tokens, private keys, or secret contents into Nix expressions: evaluated strings can enter the world-readable Nix store or logs.
   - Use the repository's established secret manager or runtime credential/file mechanism. Never print secret values during evaluation or service debugging.
   - Do not silently enable unfree or insecure packages, open firewall ports, weaken authentication, add users or trusted keys, or broaden privileges. Require explicit authorization for account, authentication, security, privacy, destructive, or production-control changes.

5. **Validate before activation.**
   - For flakes, run the repository's focused checks and `nix flake check` when its outputs are intended to pass on the current system.
   - Build without activation first: `nixos-rebuild build --flake .#<host>` for a flake host, or the repository's documented non-flake command. A successful build verifies evaluation and derivation construction, not runtime behavior.
   - Inspect the closure or activation impact when material, for example with `nix store diff-closures /run/current-system ./result` and `nixos-rebuild dry-activate`; note that dry activation may not list every change.
   - Use `nixos-rebuild test` only when temporary activation is authorized. It activates the generation without making it the boot default, but it can still restart services, change networking, disrupt access, or alter runtime state.
   - Use `nixos-rebuild boot` when the change should apply only after reboot. Use `nixos-rebuild switch` only after build/test evidence and explicit authorization; it activates immediately and makes the generation the boot default.
   - For remote systems, use the repository's deployment tool or explicit build/target host options. Preserve a working recovery path and never experiment first on production.

6. **Verify the running system.**
   - Check the affected systemd units, sockets, mounts, network listeners, users, permissions, or application health rather than relying only on the rebuild exit code.
   - Confirm the active generation and boot expectation, and verify that remote access still works before ending a remote change.
   - Report the exact host/output built, commands run, activation level reached (`build`, `test`, `boot`, or `switch`), runtime checks, and anything skipped.

## Failure handling

- For an unknown option or type conflict, inspect the full module error and definitions for the pinned revision; do not guess a replacement or mask the conflict with `mkForce`.
- For evaluation failures, reduce to the smallest relevant module and distinguish syntax, missing arguments, infinite recursion, and option-definition conflicts.
- For build failures, separate evaluation from fetch, sandbox, disk-space, and package-build failures before changing configuration.
- For activation or service failures, keep the current shell and recovery access open. Inspect `systemctl status`, `journalctl`, and the failed unit before another rebuild.
- If temporary activation is unhealthy, return to a known generation with the bootloader or `nixos-rebuild --rollback switch` when appropriate and authorized. Do not garbage-collect generations until recovery is confirmed.
- If the target hardware, host output, credentials, or recovery path is uncertain, stop after a non-activating build and state what must be confirmed.

## Boundary

Use general Nix guidance for language syntax, flakes, nixpkgs packaging, overlays, and derivations. Use Home Manager for user packages and dotfiles. Use this skill for NixOS system modules, operating-system services, activation, generations, and recovery.
