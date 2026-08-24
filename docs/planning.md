# `skill-eval`: Portable, Multi-Model Skill Evaluation CLI

## Goal

Ship `skill-eval` as an installable Python CLI for evaluating, comparing, and
optionally improving agent skills. Its primary question is:

> Given the same task, capability profile, and model, does this skill improve
> task completion relative to an explicit baseline?

The CLI must evaluate portable skill instructions and approved resources without
requiring a provider-specific skill-routing harness. Separate native-routing
checks cover Claude Code, Codex, Pi, and OpenCode compatibility.

Persist experiment definitions, attempts, outputs, grades, candidate revisions,
and reports in SQLite—not a collection of unqueryable JSON result directories.

## Decisions

- **Distribution:** a normal Python package with the `skill-eval` console
  command. It is installable with `uv tool install skill-eval`, `pipx install
  skill-eval`, or `pip install skill-eval`.
- **Framework:** use **Pydantic AI** as the model and tool-execution layer. It
  provides typed agents, provider/model abstractions, tool schemas, structured
  results, retries, and first-party provider support. `skill-eval` owns the
  evaluation protocol, persistence, scheduling, grading, and configuration;
  it must not leak Pydantic AI types into the persisted experiment format.
- **CLI:** use Typer for a composable, documented command surface; use Rich only
  for terminal presentation. Commands must also offer machine-readable JSON
  output where useful.
- **Configuration:** load a validated global YAML config from the XDG config
  directory, with explicit configuration-file, suite-file, and CLI overrides.
  Secrets are referenced by environment-variable name, never stored in YAML or
  SQLite.
- **Schema evolution:** use versioned Alembic migrations. After configuration
  resolves the database path, every CLI startup migrates it to the packaged
  schema head before command dispatch; startup fails safely with an actionable
  error if migration cannot complete.
- **Safety:** enhancement is opt-in and never overwrites a user skill. It
  produces a reviewable candidate, evaluates it, and requires a separate
  explicit apply action.

## Review of upstream `skill-creator` scripts

The reviewed scripts are in Anthropic's
[`skill-creator/scripts`](https://github.com/anthropics/skills/tree/main/skills/skill-creator/scripts).

| Upstream behavior | Keep or change in `skill-eval` |
| --- | --- |
| `quick_validate.py` validates `SKILL.md` frontmatter and basic limits. | Keep and expand as `skill-eval validate`; use a typed frontmatter model, clear diagnostics, resource-path checks, and an optional strict mode. |
| `package_skill.py` validates then creates a `.skill` ZIP while excluding transient files. | Keep as `skill-eval package` with deterministic archive ordering, configurable exclusion rules, and validation before packaging. |
| `run_eval.py` retries positive/negative trigger prompts concurrently, using `claude -p` stream JSON to detect `Skill`/`Read`. | Keep the routing concept in runtime-specific `native-route` adapters. These are compatibility tests, not portable skill-quality evidence; key results by immutable case IDs and record failures distinctly. |
| `run_loop.py` does train/holdout description optimization and keeps a history/report. | Reuse its useful experimental discipline: seeded stratified train/holdout splits, a blinded holdout, iteration history, and selecting the best held-out candidate. Generalize it into the optional enhancement workflow. |
| `improve_description.py` asks `claude -p` to revise frontmatter description from failed trigger cases. | Generalize to a configured Pydantic AI **enhancement agent** that can propose a complete `SKILL.md` revision. Retain a metadata-only mode for native routing. |
| `aggregate_benchmark.py` summarizes filesystem results, but computes a delta from the first two discovered configurations. | Replace with SQL-backed, explicitly named paired comparisons by model/case/repetition/candidate. Report uncertainty and failures separately. |
| `generate_report.py` creates an HTML report. | Retain HTML and JSON reports, but render them from a selected SQLite experiment/candidate rather than ad-hoc result files. |

### Upstream limitations addressed by this plan

1. Evaluation and improvement are coupled to `claude -p`, Claude Code command
discovery, and its stream-event protocol.
2. A single model option is overloaded for execution and optimization; executor,
grader, and enhancer need independent configuration.
3. Trigger routing and task-quality evaluation are fundamentally different
measurements and should not be combined.
4. File-backed JSON results are difficult to query, resume, compare, or audit.
5. Failed calls are coerced toward a negative result instead of recorded as
provider, timeout, rate-limit, or invalid-response failures.
6. Aggregation depends on discovered directory order rather than a named,
paired baseline.
7. Reusing literal query text as an identifier risks duplicate-case collisions.

## Product surface

```text
skill-eval validate SKILL_DIR [--strict] [--format text|json]
skill-eval package SKILL_DIR [--output DIR]
skill-eval evaluate SKILL_DIR --suite SUITE.yaml [options]
skill-eval report EXPERIMENT_ID [--format text|json]
skill-eval resume EXPERIMENT_ID
skill-eval native-route {claude|codex|pi|opencode} SKILL_DIR --suite ROUTING.yaml
skill-eval enhance EXPERIMENT_ID [--apply CANDIDATE_ID --skill-dir SKILL_DIR]
skill-eval config init|show|validate|path
```

`evaluate` is the primary workflow. It accepts `--enhance` to ask the configured
enhancer to propose and evaluate a candidate after the initial experiment:

```bash
skill-eval evaluate ./my-skill --suite eval-suite.yaml --enhance
```

Current run-level options include `--database`, `--config`, `--enhance`, and
`--format json`. Model aliases, repetitions, and endpoints come from the suite
and global configuration. Future run-level overrides must affect only the
selected run and never rewrite global configuration.

`skill-eval enhance EXPERIMENT_ID` permits a later enhancement pass without
rerunning the original baseline. `--apply CANDIDATE_ID` is the only operation
that writes a selected candidate back to the target skill, and it must show a
diff and require an affirmative confirmation unless `--yes` is provided.

## Installation and package layout

The package uses a `src/` layout and exposes `skill_eval.cli:app` as the
`skill-eval` console command. Publish only after installation, `--help`, config
discovery, migrations, and a mock-provider smoke test pass in a clean
environment.

Current module boundaries:

```text
src/skill_eval/
  cli.py                 # Typer commands and exit-code mapping
  config.py              # YAML discovery, validation, and path resolution
  skills.py              # frontmatter validation, snapshots, and packaging
  suites.py              # suite and capability-profile contracts
  harness.py             # isolated workspaces and replay-source materialization
  executor.py            # Pydantic AI execution and normalized results
  providers.py           # config -> Pydantic AI model/provider factory
  grading.py             # deterministic graders
  evaluator.py           # scheduling, execution, resume, and candidate evaluation
  enhancement.py         # candidate proposal, validation, diff, and apply
  native_route.py        # runtime-specific native discovery checks
  persistence.py         # experiment repositories and artifact storage
  storage.py             # Alembic migration and SQLite backup lifecycle
  migrations/            # packaged schema revisions
```

## Global YAML configuration

### Discovery, precedence, and secrets

The default global path is:

- Linux and other XDG systems: `$XDG_CONFIG_HOME/skill-eval/config.yaml`,
  falling back to `~/.config/skill-eval/config.yaml`;
- macOS/Windows: the platform-appropriate `platformdirs.user_config_dir`
  location.

`skill-eval config init` creates a commented example with mode `0600` where the
platform permits it. `config path`, `config show`, and `config validate` make
configuration observable without exposing secrets.

Settings merge in this order (later wins): built-in defaults, global config,
`--config` YAML, suite YAML, and explicit CLI flags. The resolved, redacted
configuration and its hash are saved with the experiment. Secrets may be
supplied only through `api_key_env` (or a supported provider's ambient
environment variable); commands must reject literal API-key fields in YAML and
redact endpoint query credentials if encountered.

### Config shape

Use Pydantic discriminated models to validate providers, models, role defaults,
and provider-specific settings before making any network call. A global config
can configure multiple named endpoints—including more than one instance of the
same provider—and choose reusable role defaults:

```yaml
version: 1

defaults:
  executor: local-qwen
  grader: cloud-judge
  enhancer: cloud-editor
  database: ~/.local/share/skill-eval/skill-evals.db
  max_concurrency: 4
  timeout_seconds: 120

providers:
  anthropic:
    kind: anthropic
    api_key_env: ANTHROPIC_API_KEY
  openai:
    kind: openai
    api_key_env: OPENAI_API_KEY
  ollama-local:
    kind: ollama
    # Pydantic AI/Ollama's OpenAI-compatible endpoint includes /v1.
    base_url: http://localhost:11434/v1
    api_key_env: OLLAMA_API_KEY  # optional for a local server
  lab-gateway:
    kind: openai-compatible
    base_url: https://llm-gateway.example.internal/v1
    api_key_env: LAB_GATEWAY_API_KEY

models:
  local-qwen:
    provider: ollama-local
    model: qwen3:8b
    settings: { temperature: 0 }
  cloud-judge:
    provider: anthropic
    model: claude-sonnet-4-5
    settings: { temperature: 0 }
  cloud-editor:
    provider: openai
    model: gpt-5
    settings: { temperature: 0.2 }
```

`kind: openai-compatible` creates a Pydantic AI `OpenAIChatModel` with an
`OpenAIProvider(base_url=..., api_key=...)`. Named `kind: ollama` configurations
use Pydantic AI's Ollama support and allow a local or cloud endpoint override.
Named provider configuration takes precedence over provider-library defaults,
so self-hosted Ollama, gateways, proxies, and region-specific endpoints work
without code changes. Validate endpoint URLs, fail early when a required key
variable is unset, and issue only a warning for intentionally keyless local
endpoints.

A suite may refer only to model aliases from the global config, or define a
local named model/provider override. It must never duplicate secret material.
A future connectivity probe should remain explicit and opt-in rather than
making config inspection contact providers.

## Portable execution evaluation

### Conditions and controlled capability profiles

Every execution receives exactly the same task, fixtures, capability profile,
model settings, and sampling settings. Only the selected condition changes.

- `without_skill`: no skill context; the required baseline.
- `with_metadata_only`: name/description only; optional portable discoverability
  condition.
- `with_full_skill`: resolved `SKILL.md` plus allowlisted referenced resources;
  the primary quality condition.

A capability profile is versioned content that defines normalized tool schemas,
filesystem fixture/input and output behavior, network policy, CPU/wall-clock/
tool-call/output-size limits, prompt template and tool protocol versions, and
artifact collection rules. Its full normalized content hash is recorded with
every experiment.

The harness resolves the skill before scheduling. It rejects resource paths
outside the skill root, snapshots every allowed file, and deliberately measures
the value of that snapshot—not an unrepeatable mutable working tree or a
proprietary discovery system.

### Pydantic AI runtime

Build each executor, judge, and enhancer as a separate Pydantic AI agent from
the resolved model alias. `providers.py` converts validated config into the
correct Pydantic AI model/provider object; `executor.py` supplies the same
normalized tool definitions and capability dependencies to every executor.

Pydantic AI handles protocol-specific model calls and tool turns. `skill-eval`
wraps its output into a provider-neutral `RunResult` containing provider and
resolved model, condition, immutable case ID, repetition, status, transcript,
normalized tool calls, token usage, cost, duration, errors, and collected
artifacts. Preserve raw provider details as a bounded diagnostic artifact,
while reports use only the normalized representation.

Do not promise artificial tool parity where a provider cannot support the
profile. Validate each selected model against the requested capability profile
before scheduling and mark incompatible attempts as `unsupported` rather than
silently reducing the available tools.

### Suite example

```yaml
schema_version: 1
capability_profile: restricted-filesystem-v1
conditions: [without_skill, with_full_skill]
repetitions: 5
seed: 42
executors: [local-qwen, cloud-judge]
grader: cloud-judge

cases:
  - id: extract-release-notes
    prompt: Summarize the supplied release notes and write RELEASE.md.
    fixtures: [fixtures/release-notes.md]
    assertions:
      - id: output-exists
        type: file_exists
        path: RELEASE.md
      - id: mentions-breaking-change
        type: contains
        path: RELEASE.md
        text: "breaking"
```

The suite is also Pydantic-validated. Case IDs are required, immutable within
an experiment, and never derived from prompt text.

## Optional enhancement agent

The enhancement agent operationalizes the useful part of upstream description
optimization without conflating it with routing or permitting hidden edits.

### CLI behavior

- `skill-eval evaluate ... --enhance` runs the original experiment first,
  then queues enhancement only when the baseline results are complete enough
  to diagnose. `--enhancer MODEL_ALIAS` overrides the configured enhancer.
- `skill-eval enhance EXPERIMENT_ID` generates and holdout-evaluates a
  candidate later. Additional candidate-selection controls remain roadmap work.
- Enhancement is **off by default**. It never changes `SKILL.md` in place.
  Candidates live in an experiment workspace and SQLite artifacts, with a
  content hash and unified diff.
- `skill-eval enhance EXPERIMENT_ID --apply CANDIDATE_ID --skill-dir SKILL_DIR`
  validates and displays the diff, then requires confirmation (or `--yes`).

### Target candidate workflow

1. Snapshot the original skill, suite, profile, configuration, and immutable
   results. Select only relevant failed cases/transcripts and aggregate
   diagnostics; holdout labels and holdout scores are withheld from the
   enhancer.
2. Ask a Pydantic AI structured-output agent for a rationale and a proposed
   complete `SKILL.md` (metadata-only mode may propose just the description).
   Its prompt requires generalizable improvements, preserves the skill name,
   stays within frontmatter limits, and forbids changing the eval suite,
   profile, fixtures, or unrelated files.
3. Validate frontmatter, resource references, skill-root containment, and size
   limits. Persist invalid proposals and errors for audit, but do not evaluate
   them.
4. Evaluate each valid candidate under the identical profile and model matrix.
   Use the training subset only while generating candidates; select a winner by
   predeclared paired held-out uplift, with deterministic checks as gates.
5. Report original versus candidate metrics and confidence intervals. A
   candidate is merely *recommended* unless it meets the selection threshold
   and does not regress required assertions or budget/error-rate limits. The
   user still decides whether to apply it.

This supports full skill quality improvements while keeping native runtime
routing checks separate from portable evaluation.

## SQLite experiment backend

Create one SQLite database per user or configured workspace; isolate each
experiment by ID, enable foreign keys and WAL mode, and atomically claim queued
attempts. A concurrent scheduler will require a dedicated single-writer policy.

### Automatic migrations at startup

Manage schema history with Alembic revision files committed with the package.
After configuration resolves the database path, the CLI startup sequence must:

1. create the database parent directory when needed, open the database, and
   enable its required SQLite pragmas;
2. acquire an exclusive migration lock (`BEGIN IMMEDIATE` or equivalent) so
   concurrent CLI processes cannot race schema changes;
3. inspect the `alembic_version` table and run `alembic upgrade head` before
   any command handler, repository, report, or scheduler accesses the schema;
4. commit each transactional migration atomically, then release the lock; and
5. surface the current and required revision plus recovery guidance if a
   migration fails. Never continue against a partially migrated schema.

This happens on **every CLI startup**, not only during installation or on an
explicit `migrate` command. `--help`/`--version` may remain database-free; all
other commands—including `config`, `validate`, and `package`—run the startup
migration against the resolved default or `--database` path before dispatch.
The check is a no-op when the database is already at head.

Migrations must be forward-only in normal use, small, idempotence-tested from a
fresh database and every supported historical fixture, and reviewed for SQLite
limitations. Take an automatic timestamped backup before a migration that
cannot be wholly transactional or that rewrites/copies a populated table; do
not silently downgrade. Provide `skill-eval db status` for revision inspection
and `skill-eval db backup` for an explicit backup, but neither replaces the
mandatory startup upgrade.

The existing core data model remains appropriate—experiment, model, eval case,
condition, attempt, grade, and artifact—but add the following:

```sql
CREATE TABLE config_snapshot (
  id TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE,
  redacted_yaml TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE skill_snapshot (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL REFERENCES experiment(id),
  parent_snapshot_id TEXT REFERENCES skill_snapshot(id),
  sha256 TEXT NOT NULL,
  manifest_json TEXT NOT NULL,
  skill_md TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE candidate (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL REFERENCES experiment(id),
  source_snapshot_id TEXT NOT NULL REFERENCES skill_snapshot(id),
  candidate_snapshot_id TEXT NOT NULL REFERENCES skill_snapshot(id),
  enhancer_model_id TEXT NOT NULL REFERENCES model(id),
  mode TEXT NOT NULL,
  status TEXT NOT NULL,
  rationale TEXT,
  selection_json TEXT,
  created_at TEXT NOT NULL
);

ALTER TABLE experiment ADD COLUMN config_snapshot_id TEXT
  REFERENCES config_snapshot(id);
ALTER TABLE attempt ADD COLUMN skill_snapshot_id TEXT
  REFERENCES skill_snapshot(id);
ALTER TABLE attempt ADD COLUMN candidate_id TEXT REFERENCES candidate(id);
```

Store transcripts, metadata, grades, bounded outputs, snapshots, and proposed
skill text in SQLite with SHA-256 hashes. Reject oversized artifacts; a future
content-addressed object store may handle larger outputs while keeping
authoritative references and hashes in SQLite. Preserve every input
needed to reproduce a run: model alias and resolved provider endpoint (redacted
as needed), settings, config snapshot hash, suite, profile, prompt template,
rubric, skill snapshot, seed, and randomization settings.

## Grading, metrics, and reporting

Run deterministic graders first. If a judge is configured, run it as a separate
Pydantic AI role with a versioned rubric and model alias; keep judge score
separate from deterministic pass/fail. Never let an enhancement agent grade its
own candidate.

Report results by model, condition, and candidate rather than collapsing model
disagreement into one score:

- deterministic assertion pass rate and separate judge score;
- paired uplift: `with_full_skill - without_skill` for the same model, case,
  repetition, and snapshot;
- candidate uplift against its original snapshot using the same pairing;
- latency, input/output tokens, estimated cost, and tool-call count;
- timeout, rate-limit, unsupported-profile, provider, validation, and
  invalid-response rates as distinct statuses;
- per-case deltas and bootstrap confidence intervals over paired samples.

Reports require a named baseline condition and refuse ambiguous comparisons.
Text and JSON reports show sample counts and failed attempts. HTML output,
confidence intervals, hashes, and explicit train/holdout sections remain
roadmap reporting work.

## Execution hardening

- Use provider-specific concurrency limits, retry/backoff policies, request
timeouts, per-experiment cost ceilings, and cancellation propagation.
- Never coerce a provider failure into a task failure, trigger miss, or zero
score.
- Use isolated temporary workspaces per attempt; do not share mutable `.claude`
directories or output folders.
- Version prompt templates, Pydantic AI/tool schemas, model settings, profile,
skill snapshot, configuration schema, and grader rubric.
- Support resumable scheduling: queued/interrupted attempts are atomically
claimed and retried without overwriting completed attempts.
- Redact credentials from logs, database records, diagnostics, reports, and
exception messages. Test redaction explicitly.

## Implementation phases

1. **Ship the installable CLI foundation**
   - Move the console entry point to `skill_eval.cli:app` and add Typer,
     Pydantic AI, PyYAML, and platformdirs dependencies/extras.
   - Implement `--help`, stable exit codes, JSON output, `validate`, `package`,
     and clean-environment installation smoke tests.

2. **Implement global configuration and provider factory**
   - Add Pydantic YAML schema, XDG discovery, precedence/override rules,
     redaction, `config init/show/validate`, and no-network validation.
   - Build config-to-Pydantic-AI factories for Anthropic, OpenAI, Gemini,
     Ollama, and generic OpenAI-compatible endpoints; cover endpoint and
     key-environment overrides with mocked clients.

3. **Define portable protocol and SQLite foundation**
   - Specify capability profiles, skill resolver/snapshots, neutral request and
     result types, Alembic revisions, repositories, artifact ingestion, and
     isolated workspaces.
   - Implement mandatory startup `upgrade head`, SQLite migration locking,
     backup/error behavior, and upgrade tests from fresh and historical
     databases before any schema-dependent command.
   - Implement experiment creation, resume/claim semantics, and deterministic
     grading before adding LLM judging.

4. **Deliver the portable evaluation MVP**
   - Implement one Pydantic AI executor adapter, paired
     `without_skill`/`with_full_skill` runs, explicit failure statuses, basic
     SQL summaries, and `evaluate`/`report`.
   - Add integration tests with a mock model plus one opt-in live-provider
     smoke test guarded by environment credentials.

5. **Add the model matrix and reports**
   - Add remaining providers, tool/capability compatibility validation,
     quotas/retries/budgets, token/cost capture, judge grading, paired
     confidence intervals, and HTML/JSON reports.

6. **Add enhancement and native routing**
   - Implement structured candidate proposals, validation, train/holdout
     selection, candidate persistence/diffs, no-overwrite defaults, and
     explicit apply.
   - Add runtime-specific native routing adapters while keeping their results
     out of portable execution reports.

## Acceptance criteria

- A clean environment can install the package and run `skill-eval --help`.
- `skill-eval config init` produces a valid global YAML file; config precedence,
  endpoint overrides, environment-key lookup, and secret redaction are tested.
- A configured Ollama or generic OpenAI-compatible endpoint can be selected by
  model alias without code changes.
- Every database-using CLI invocation upgrades the resolved SQLite database
  to the packaged Alembic head before dispatch; concurrent startup, failed
  migration, and historical-upgrade paths are tested and never leave a usable
  partial schema.
- One command runs a reproducible paired experiment, persists it in SQLite,
  and emits a per-model report with a named baseline and explicit errors.
- `--enhance` produces an auditable, validated candidate and evaluates it, but
  never edits the source skill. Applying a candidate requires an explicit
  command and confirmation.
- Native Claude Code, Codex, Pi, and OpenCode routing measurements remain
  separate from portable skill-quality scores.

## Rough effort

- **Installable CLI, config, one provider, SQLite, paired evaluation:** 1–2
  engineering weeks.
- **Useful multi-provider evaluator with reports and judge grading:** 3–5 weeks.
- **Enhancement workflow, native compatibility mode, resumability, budget
  controls, local models, and CI gates:** 2–4 additional weeks.
