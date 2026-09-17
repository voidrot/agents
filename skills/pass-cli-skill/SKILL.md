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

## Standard workflow

1. Check the installed interface before executing a version-sensitive command:

   ```bash
   pass-cli --version
   pass-cli <command> --help
   pass-cli info
   ```

2. For a `pass://` reference, obtain the intended vault Share ID and item ID using JSON output; then construct the field-qualified URI:

   ```bash
   pass-cli vault list --output json
   pass-cli item list --share-id "$SHARE_ID" --output json
   REF="pass://$SHARE_ID/$ITEM_ID/$FIELD"
   ```

   Read [secret references](references/secret-references.md) before selecting a field, using names rather than IDs, or handling TOTP.

3. Choose the least-exposing resolution path:
   - Need a value only in a noninteractive child process: use `pass-cli run`.
   - Need secrets rendered in a configuration file: use `pass-cli inject` with a restrictive output mode.
   - Need a raw field value: use `pass-cli item view "$REF"` only when the user explicitly requested it and the output sink is safe.

   Read [resolution and automation](references/resolution-and-automation.md) before using `run`, `inject`, dotenv files, TOTP URIs, or a TTY application.

4. If authentication is needed, prefer normal browser login for people and an already-provisioned scoped, expiring PAT for automation. Read [authentication and recovery](references/authentication-and-recovery.md) before login in automation, changing access, enabling headless key storage, or troubleshooting.

5. On failure, check session status, re-list vaults/items by ID, inspect the item only as needed to confirm the field, and retry the quoted ID-based reference. Do not broaden sharing or PAT access without authorization.

## Completion evidence

Report the unresolved reference or that injection succeeded—not the secret value—unless the user expressly requested disclosure and it is appropriate. State which identifiers were used, whether anything was written or executed, and the validation performed.
