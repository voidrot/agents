# Authentication and recovery

Read this reference before authenticating, using a PAT, changing access, or diagnosing session/key-storage failures.

## Authentication

Check status without revealing values:

```bash
pass-cli info
```

Use `pass-cli login` for browser-based login. Use `pass-cli login --interactive [USERNAME]` only where interactive account authentication is appropriate. Browser login is required for SSO or hardware-key flows.

For CI and other automation, use an already-provisioned, scoped, expiring PAT rather than account credentials:

```bash
PROTON_PASS_PERSONAL_ACCESS_TOKEN=... pass-cli login
pass-cli info
```

PAT sessions last two hours. Scope access to only the needed vault or item, usually with the `viewer` role. Do not create, reveal, renew, revoke, or expand PAT access without explicit authorization; a full PAT value is shown only when it is created or renewed.

## Recovery sequence

1. Run `pass-cli info` to verify session status.
2. Run `pass-cli vault list --output json` to confirm access and Share ID.
3. Run `pass-cli item list --share-id "$SHARE_ID" --output json` to confirm item ID.
4. Use `pass-cli item view --share-id "$SHARE_ID" --item-id "$ITEM_ID"` only as needed to verify the field name and section.
5. Retry the quoted, ID-based `pass://` URI.

Distinguish a malformed URI, expired session, missing vault/item access, and a missing field. Preserve diagnostics without exposing resolved stdout. Do not broaden sharing or PAT access merely to bypass an error.

Filesystem key storage may be needed in some headless environments, but it stores the key beside encrypted data. Treat it as a degraded-security option and do not enable it silently.

## Official sources

- [Login](https://protonpass.github.io/pass-cli/commands/login/)
- [Personal access tokens](https://protonpass.github.io/pass-cli/commands/personal-access-token/)
- [Configuration](https://protonpass.github.io/pass-cli/get-started/configuration/)
- [Troubleshooting](https://protonpass.github.io/pass-cli/help/troubleshoot/)
