---
name: chezmoi-skill
description: Manage, migrate, and troubleshoot chezmoi dotfile source states, including templates, machine-specific data, scripts, encrypted files, externals, and safe deployment. Use when a request involves chezmoi commands, a chezmoi-managed dotfiles repository, or deploying dotfiles with chezmoi; not for generic Git or unrelated configuration management.
---

# Chezmoi dotfile management

Manage the desired dotfile state in chezmoi's source directory and deploy it safely to the destination directory (normally `$HOME`). Treat `apply` as a filesystem-changing operation; inspect the computed target state before it.

## Choose the workflow

1. Inspect the repository and effective configuration before changing anything:
   ```sh
   chezmoi source-path ~/.example
   chezmoi target-path dot_example
   chezmoi status
   chezmoi diff
   chezmoi cat-config
   ```
   `source-path` and `target-path` are optional when the requested path is already unambiguous. Use `chezmoi cd` to work in the source state; it opens a subshell and cannot change the caller's directory.
2. For an existing local file, add it, edit the source representation, preview, then apply:
   ```sh
   chezmoi add ~/.config/example/config
   chezmoi edit ~/.config/example/config
   chezmoi diff ~/.config/example/config
   chezmoi --dry-run --verbose apply ~/.config/example/config
   chezmoi apply ~/.config/example/config
   ```
3. For a clone/bootstrap request, initialize first, then preview before applying:
   ```sh
   chezmoi init REPOSITORY
   chezmoi diff
   chezmoi apply --verbose
   ```
   Use `chezmoi init --apply --verbose REPOSITORY` only when the user has explicitly authorized deployment.
4. For changes received from the source repository, use `chezmoi update --apply=false`, inspect `diff`, then apply. `chezmoi update` otherwise pulls and applies by default.
5. After source-state edits, use the repository's normal Git workflow to review and commit only the intended source changes.

Read [core operations](references/core-operations.md) for command semantics, startup, and daily operations.

## Preserve the source-state model

- The source state stores ordinary files and directories. Source names encode target names, target types, and attributes: e.g. `dot_gitconfig` → `~/.gitconfig`; `private_`, `executable_`, `readonly_`, `template_`, `encrypted_`, `create_`, `modify_`, and `exact_` change behavior.
- Prefer `chezmoi add --template`, `chezmoi add --encrypt`, and `chezmoi chattr` over manually renaming source entries. Attribute ordering is target-type dependent.
- Do **not** manually create `exact_`, `remove_`, `run_`, `run_once_`, or `run_onchange_` entries without explaining their effect and obtaining appropriate authorization. They can delete files or run programs during an apply.
- Use `chezmoi add --follow` when migrating a dotfile manager that uses symlinks and the desired result is the symlink target's content.

Read [source state and file types](references/source-state.md) before editing attributes, symlinks, exact directories, or managed scripts.

## Template and configuration work

1. Model stable, non-secret machine differences as data. Put shared data in `.chezmoidata.*`; use config-file `[data]` for per-machine values. Check `chezmoi data` and test a template with `chezmoi execute-template` before applying.
2. Turn a managed file into a template with `chezmoi add --template PATH` or `chezmoi chattr +template PATH`. Use `.chezmoiignore` for conditionally excluded targets.
3. Put initialization prompts only in a config template (`.chezmoi.toml.tmpl`, or JSON/YAML equivalent), and use the `*Once` prompt functions when a previously collected value should be reused.
4. Do not put plaintext credentials in source data or configuration. Choose a password-manager template function or encryption instead.

Read [templates, data, and configuration](references/templates-data-config.md) for data precedence, safe testing, config locations, and template execution boundaries.

## Secrets, externals, and scripts

- For a secret that must be rendered into a target file, prefer a password-manager template function. Keep secret lookup identifiers and CLI prerequisites separate from values.
- For a file that must be stored in source state, encrypt it with chezmoi's configured encryption mechanism and modify it through `chezmoi edit-encrypted`.
- For downloaded or cloned managed content, use `.chezmoiexternal.*`; pin it with a checksum or immutable release/version where possible. Preview and refresh deliberately.
- Scripts execute as part of application and are not run by a dry run. Give each script a shebang, make it idempotent, and never have it mutate source or destination state during the same chezmoi execution.

Read [secrets and encryption](references/secrets-encryption.md) and [externals and scripts](references/externals-scripts.md) before adding either capability.

## Verify and recover

1. Before a nontrivial deployment, run `chezmoi diff` and `chezmoi --dry-run --verbose apply`; inspect every unexpected deletion, permission change, script, external fetch, or secret prompt.
2. After an authorized apply, run `chezmoi status` and, where a clean target state is expected, `chezmoi verify` (exit code 0 means target matches; 1 means it does not).
3. Diagnose with `chezmoi doctor`, `chezmoi managed`, `chezmoi unmanaged`, `chezmoi ignored`, `chezmoi cat PATH`, and `chezmoi --debug ...`. For template errors, reproduce with `chezmoi execute-template`; for conflicts, use `chezmoi merge`.
4. Never run `destroy`, `purge`, `remove`/`rm`, or `--force` without explicit user authorization and a reviewed backup/recovery plan. `forget` stops managing without removing the destination, which is usually the safer operation.

Read [safety, verification, and recovery](references/safety-recovery.md) for destructive-operation boundaries and troubleshooting.

## Completion evidence

Report: the source files changed, the target paths affected, any attributes/scripts/externals/secrets added, the exact preview/verification commands run and their outcome, and whether deployment was actually performed. Do not claim a target was deployed if only a dry run was performed.
