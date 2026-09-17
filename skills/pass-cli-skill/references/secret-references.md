# Secret references

Read this reference before constructing a `pass://` URI, selecting an item field, or resolving a TOTP value.

## Canonical form

```text
pass://<vault-identifier>/<item-identifier>/<field-name>
```

- The vault identifier is a vault Share ID or name.
- The item identifier is an item ID or title.
- The field is a standard, custom, or section-qualified field name.

Prefer Share ID plus item ID in scripts. Duplicate names can resolve unpredictably. Quote the complete URI in the shell:

```bash
REF="pass://$SHARE_ID/$ITEM_ID/$FIELD"
pass-cli item view "$REF"
```

Names with spaces are supported. Proton does not document escaping rules for separator characters in names or fields; do not guess. Use IDs and inspect the item to confirm the field instead.

## Find identifiers and fields

```bash
pass-cli vault list --output json
pass-cli item list --share-id "$SHARE_ID" --output json
pass-cli item view --share-id "$SHARE_ID" --item-id "$ITEM_ID"
```

The final command can display secrets. Use it only when necessary to identify an exact field and never use `item list --show-secrets` merely to locate an item.

Common login fields include `username`, `password`, `email`, `url`, `note`, and `totp`. Custom field names work. Use the exact spelling and case shown by the item: the official documentation has conflicting case-sensitivity statements, so exact casing is the safe choice.

## Sections and TOTP

For duplicate field names in named sections, use `SectionName.fieldname`, for example `Production.password`. An unqualified name can select the first matching section field.

TOTP references resolve to the current code by default. Request the underlying `otpauth://` URI only when explicitly required:

```bash
pass-cli item view "pass://$SHARE_ID/$ITEM_ID/totp?totp=uri"
```

A field-qualified URI is the safe form for a secret value. Although `item view` supports viewing a whole item, do not use an item-level URI as an input to `run` or `inject`.

## Official sources

- [Secret references](https://protonpass.github.io/pass-cli/commands/contents/secret-references/)
- [Item command](https://protonpass.github.io/pass-cli/commands/item/)
- [Item object](https://protonpass.github.io/pass-cli/objects/item/)
