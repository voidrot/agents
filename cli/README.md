# Agents CLI

Bare-bones installer for Voidrot opencode assets.

Package command:

```sh
npx @voidrot/agents --help
```

## Build

```sh
npm install
npm run build
```

## Usage

```sh
npx @voidrot/agents list [skills|agents|hooks|plugins]
npx @voidrot/agents install <type> <name> [--scope project|global] [--project-dir <path>] [--dry-run] [--force]
```

`type` accepts singular or plural aliases, such as `skill` and `skills`.

Examples:

```sh
npx @voidrot/agents list skills
npx @voidrot/agents install skill skill-authoring --dry-run
npx @voidrot/agents install plugin sample-plugin --scope global
```

Project installs create `.opencode/opencode.json` only when it is missing. Global installs do the same at `~/.config/opencode/opencode.json`. Existing configs are never overwritten.

Restart opencode after installing assets so it reloads new or changed files.
