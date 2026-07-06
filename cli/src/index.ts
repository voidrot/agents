#!/usr/bin/env node

import { Command, InvalidArgumentError } from "commander";
import { existsSync } from "node:fs";
import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";

type ItemType = "skills" | "agents" | "hooks" | "plugins";

type RegistryItem = {
  name: string;
  description: string;
  source: string;
};

type Registry = Record<ItemType, RegistryItem[]>;

type InstallOptions = {
  scope: "global" | "project";
  projectDir: string;
  dryRun?: boolean;
  force?: boolean;
};

const REPO_ROOT = path.resolve(__dirname, "..");
const REGISTRY_PATH = path.join(REPO_ROOT, "registry.json");
const TYPES: ItemType[] = ["skills", "agents", "hooks", "plugins"];
const TYPE_ALIASES: Record<string, ItemType> = {
  skill: "skills",
  skills: "skills",
  agent: "agents",
  agents: "agents",
  hook: "hooks",
  hooks: "hooks",
  plugin: "plugins",
  plugins: "plugins",
};

async function main() {
  const program = new Command();

  program
    .name("@voidrot/agents")
    .description("Install Voidrot opencode skills, agents, hooks, and plugins.")
    .version("0.1.0");

  program
    .command("list")
    .argument("[type]", "skills, agents, hooks, or plugins", parseType)
    .description("List all registry items or only one type.")
    .action(async (type?: ItemType) => {
      const registry = await loadRegistry();
      const types = type ? [type] : TYPES;

      for (const itemType of types) {
        console.log(`${itemType}:`);
        for (const item of registry[itemType] ?? []) {
          console.log(`  ${item.name} - ${item.description}`);
        }
      }
    });

  program
    .command("install")
    .argument("<type>", "skill(s), agent(s), hook(s), or plugin(s)", parseType)
    .argument("<name>", "registry item name")
    .description("Install one registry item into an opencode config directory.")
    .option("--scope <global|project>", "install scope", parseScope, "project")
    .option("--project-dir <path>", "project directory for project installs", process.cwd())
    .option("--dry-run", "print planned operations without writing")
    .option("--force", "overwrite an existing installed asset")
    .action(async (type: ItemType, name: string, options: InstallOptions) => {
      await installItem(type, name, options);
    });

  await program.parseAsync(process.argv);
}

function parseType(value: string): ItemType {
  const type = TYPE_ALIASES[value.toLowerCase()];
  if (!type) {
    throw new InvalidArgumentError(
      `Unknown type '${value}'. Use one of: skills, agents, hooks, plugins.`,
    );
  }
  return type;
}

function parseScope(value: string): "global" | "project" {
  if (value !== "global" && value !== "project") {
    throw new InvalidArgumentError("Scope must be 'global' or 'project'.");
  }
  return value;
}

async function loadRegistry(): Promise<Registry> {
  if (!existsSync(REGISTRY_PATH)) {
    throw new Error(`Missing registry at ${REGISTRY_PATH}`);
  }

  return JSON.parse(await readFile(REGISTRY_PATH, "utf8")) as Registry;
}

async function installItem(type: ItemType, name: string, options: InstallOptions) {
  const registry = await loadRegistry();
  const item = registry[type]?.find((candidate) => candidate.name === name);
  if (!item) {
    throw new Error(`Unknown ${singular(type)} '${name}'. Run 'npx @voidrot/agents list ${type}'.`);
  }

  const sourcePath = path.join(REPO_ROOT, item.source);
  if (!existsSync(sourcePath)) {
    throw new Error(`Missing source for ${type}/${name}: ${sourcePath}`);
  }

  const baseDir = getBaseDir(options);
  const configPath = path.join(baseDir, "opencode.json");
  const targetPath = getTargetPath(baseDir, type, name);
  const operations = [
    `ensure directory ${baseDir}`,
    existsSync(configPath) ? `keep existing config ${configPath}` : `create config ${configPath}`,
    `${options.force ? "copy/overwrite" : "copy"} ${sourcePath} -> ${targetPath}`,
  ];

  if (options.dryRun) {
    console.log("Dry run. Planned operations:");
    for (const operation of operations) console.log(`- ${operation}`);
    return;
  }

  if (existsSync(targetPath) && !options.force) {
    throw new Error(`Refusing to overwrite ${targetPath}. Re-run with --force to replace it.`);
  }

  await mkdir(baseDir, { recursive: true });
  if (!existsSync(configPath)) {
    await writeFile(
      configPath,
      `${JSON.stringify({ $schema: "https://opencode.ai/config.json" }, null, 2)}\n`,
      "utf8",
    );
  }

  await mkdir(path.dirname(targetPath), { recursive: true });
  if (existsSync(targetPath) && options.force) {
    await rm(targetPath, { recursive: true, force: true });
  }
  await cp(sourcePath, targetPath, { recursive: type === "skills" });

  console.log(`Installed ${singular(type)} '${name}' to ${targetPath}`);
}

function getBaseDir(options: InstallOptions): string {
  if (options.scope === "global") {
    return path.join(homedir(), ".config", "opencode");
  }
  return path.join(path.resolve(options.projectDir), ".opencode");
}

function getTargetPath(baseDir: string, type: ItemType, name: string): string {
  if (type === "skills") return path.join(baseDir, "skills", name);
  if (type === "agents") return path.join(baseDir, "agents", `${name}.md`);
  return path.join(baseDir, "plugins", `${name}.ts`);
}

function singular(type: ItemType): string {
  return type.slice(0, -1);
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Error: ${message}`);
  process.exitCode = 1;
});
