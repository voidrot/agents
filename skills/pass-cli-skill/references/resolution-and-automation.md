# Resolution and automation

Read this reference before resolving a secret into a process, template, terminal, or output file.

## Direct field retrieval

Use this only when raw output is explicitly needed and safe:

```bash
pass-cli item view "pass://$SHARE_ID/$ITEM_ID/password"
```

Avoid putting the value in chat, logs, shell history, a command line, or version control. Return the unresolved reference rather than its value whenever possible.

## Run a noninteractive program

Use bare references in inherited environment variables or dotenv files, then run the child after `--`:

```bash
export DB_PASSWORD="pass://$SHARE_ID/$ITEM_ID/password"
pass-cli run -- ./my-app

pass-cli run --env-file .env.secrets -- ./my-app
```

`run` resolves values for the child process and masks them in stdout/stderr by default. Do not use `--no-masking` unless explicit disclosure is needed and the output sink is controlled. Later `--env-file` values override earlier files. Keep dotenv files with references out of version control when their metadata is sensitive.

`run` is intended for scripts and noninteractive programs, not full TTY applications. For a TTY-required process, use a direct retrieval workflow only with an accepted secret-exposure risk.

## Render a template

`inject` resolves only double-braced references:

```text
password: {{ pass://<vault>/<item>/password }}
```

```bash
pass-cli inject --in-file config.yaml.template --out-file config.yaml
```

The default file mode is `0600`. Do not use `--force`, relax `--file-mode`, or write generated secret-bearing output into version control without explicit authorization.

## Official sources

- [`item view`](https://protonpass.github.io/pass-cli/commands/item/#view)
- [`run`](https://protonpass.github.io/pass-cli/commands/contents/run/)
- [`inject`](https://protonpass.github.io/pass-cli/commands/contents/inject/)
