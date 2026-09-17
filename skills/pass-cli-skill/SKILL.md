---
name: pass-cli-skill
description: "Use Proton Pass CLI safely for authentication, vault and item lookup, pass:// secret-reference construction, and controlled secret injection or retrieval when a task requires Proton Pass data."
---

# Proton Pass CLI

Use this skill for requests that operate Proton Pass through `pass-cli`, including creating a `pass://` reference, retrieving an item field, injecting configuration secrets, or using a scoped token in automation. Do not use it for unrelated password-manager CLIs or general credential design.

## Safety boundary

- Treat authentication credentials, PATs, item fields, TOTP codes, and resolved `pass://` values as secrets. Do not print, log, commit, or put them in a command line unless the user has explicitly requested that disclosure and the destination is safe.
- Prefer emitting an unresolved `pass://…` reference over retrieving its value. If a task needs a value, inject it into the target process or file rather than returning it in chat.
- Before destructive or access-changing operations (delete, share, transfer, PAT grant/revoke/renew/delete, changing settings, or logout), explain the effect and obtain explicit user authorization.
- Use a least-privilege, expiring personal access token (PAT) for CI and noninteractive automation. Do not create or reveal a PAT unless the user has explicitly authorized it.

## Establish the local interface

1. Verify the installed version and exact flags before executing a command; the local executable is authoritative for its version:

   ```bash
   pass-cli --version
   pass-cli --help
   pass-cli <command> --help
   ```

2. Confirm an authenticated session without exposing secrets:

   ```bash
   pass-cli info
   ```

   If login is required, use `pass-cli login` for browser-based login. Use `pass-cli login --interactive [USERNAME]` only when interactive account authentication is appropriate. For automation, supply an already-provisioned scoped PAT through `PROTON_PASS_PERSONAL_ACCESS_TOKEN` and run `pass-cli login`; then run `pass-cli info`.

3. Never change persistent defaults just to simplify a one-off operation. If defaults are already configured, remember that `default-vault` and `default-format` can affect omitted arguments and output. Prefer explicit `--share-id` and `--output json` for automation.

## Create a reliable `pass://` reference

The field-qualified secret-reference form is:

```text
pass://<vault-identifier>/<item-identifier>/<field-name>
```

A vault identifier is a vault Share ID or name. An item identifier is an item ID or title. The field is a standard, custom, or section-qualified field name.

### Resolve identifiers safely

1. List accessible vaults and select the intended vault:

   ```bash
   pass-cli vault list --output json
   ```

   Capture its Share ID as `SHARE_ID`. Do not rely on a name if more than one vault can share that name.

2. List only that vault's items:

   ```bash
   pass-cli item list --share-id "$SHARE_ID" --output json
   ```

   Capture the intended item ID as `ITEM_ID`. Prefer the ID over a title because duplicate titles may resolve unpredictably.

3. Inspect the item to discover its actual field names, taking care that this may display secret contents:

   ```bash
   pass-cli item view --share-id "$SHARE_ID" --item-id "$ITEM_ID"
   ```

   Use the minimum necessary inspection. Do not use `item list --show-secrets` merely to locate an item.

4. Construct and shell-quote the reference:

   ```bash
   REF="pass://$SHARE_ID/$ITEM_ID/$FIELD"
   pass-cli item view "$REF"
   ```

   Prefer the ID-based form in scripts. Names containing spaces are supported, but quote the entire URI. Proton's documentation does not specify escaping rules for separator characters in names or field names; do not guess. Use IDs and verify the exact field with `item view` instead.

### Field rules

- Common login fields include `username`, `password`, `email`, `url`, `note`, and `totp`. Custom field names also work.
- For duplicate field names in named sections, use `SectionName.fieldname`, for example `Production.password`. An unqualified name can select the first matching section field, so do not use it when the section matters.
- Use the exact field spelling and case shown by the item. The official secret-reference page has conflicting case-sensitivity statements; exact casing is the safe portable choice.
- A TOTP field resolves to the current code by default. Request the stored `otpauth://` URI only when explicitly needed:

  ```bash
  pass-cli item view "pass://$SHARE_ID/$ITEM_ID/totp?totp=uri"
  ```

- A field-qualified URI is required when the goal is a secret value. Although `item view` also supports an item-level URI in current documentation, do not treat an item-level URI as a secret reference for `run` or `inject`.

## Use a reference without exposing it

### Run a noninteractive command

Set environment variables to bare references, then use `run`. It resolves them only for the child process and masks resolved values in stdout/stderr by default.

```bash
export DB_PASSWORD="pass://$SHARE_ID/$ITEM_ID/password"
pass-cli run -- ./my-app
```

For dotenv files, keep references—not values—in the file and use:

```bash
pass-cli run --env-file .env.secrets -- ./my-app
```

- Keep `.env` files containing references out of version control when they reveal sensitive metadata.
- Do not use `--no-masking` unless the user explicitly requires output disclosure and the output sink is controlled.
- `run` is for scripts and noninteractive programs; use a direct `item view`-based workflow only when a full TTY application requires it and the user accepts the exposure risk.

### Render a template

`inject` resolves only references wrapped in double braces:

```text
password: {{ pass://<vault>/<item>/password }}
```

For a file destination, keep restrictive permissions (the CLI default is `0600`):

```bash
pass-cli inject --in-file config.yaml.template --out-file config.yaml
```

Do not overwrite an existing output with `--force`, relax `--file-mode`, or write a generated secret-bearing file to a repository without explicit authorization.

## Retrieval and troubleshooting

If a reference fails, diagnose without revealing values:

1. Run `pass-cli info` to check session status.
2. Re-list vaults to confirm the Share ID and access.
3. Re-list the selected vault's items to confirm the item ID.
4. View the item by explicit IDs to confirm the exact field spelling and section.
5. Retry the quoted ID-based reference.
6. If access is denied, distinguish missing vault/item access from a bad reference. Do not broaden PAT access or alter sharing without authorization.
7. For local keyring, headless, or session-storage failures, consult the installed command help and the official troubleshooting/configuration documentation. Filesystem key storage is a degraded mode because its key is stored beside encrypted data; do not enable it silently.

When returning a result to the user, return the unresolved reference (for example, `pass://$SHARE_ID/$ITEM_ID/password`) or a statement that injection succeeded—not the secret value—unless they expressly asked for the value and doing so is appropriate.

## Source basis

This procedure is based on the official Proton Pass CLI documentation, especially [secret references](https://protonpass.github.io/pass-cli/commands/contents/secret-references/), [items](https://protonpass.github.io/pass-cli/commands/item/), [`run`](https://protonpass.github.io/pass-cli/commands/contents/run/), [`inject`](https://protonpass.github.io/pass-cli/commands/contents/inject/), [login](https://protonpass.github.io/pass-cli/commands/login/), [PATs](https://protonpass.github.io/pass-cli/commands/personal-access-token/), and [troubleshooting](https://protonpass.github.io/pass-cli/help/troubleshoot/). Consult current local help before relying on flags or aliases.
