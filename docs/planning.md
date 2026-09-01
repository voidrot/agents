# Portable, Multi-Model Skill Evaluation

## Goal

Evaluate a skill as portable instruction and resource content, independently of a provider's native skill-routing harness. The primary question is:

> Given the same task and capabilities, does this skill improve task completion for each tested model?

Persist experiment definitions, attempts, outputs, grades, and reports in SQLite instead of directory trees containing JSON files.

## Review of the upstream `skill-creator` evaluator scripts

The reviewed scripts are in Anthropic's [`skill-creator/scripts`](https://github.com/anthropics/skills/tree/main/skills/skill-creator/scripts).

| Area | Current feature |
| --- | --- |
| Trigger evaluation | `run_eval.py` tests whether a skill is invoked for positive/negative prompts, retries prompts, applies a trigger-rate threshold, and evaluates cases concurrently. |
| Claude model selection | `--model` is forwarded to `claude -p`, allowing one configured Claude model ID per run. It is not a provider-agnostic multi-model suite. |
| Trigger detection | A temporary `.claude/commands/<unique>.md` is created and `claude -p` stream JSON is inspected for `Skill` or `Read` use. |
| Description optimization | `run_loop.py` creates train/holdout splits, iteratively evaluates descriptions, calls `improve_description.py`, chooses the best held-out result, saves logs, and generates a live HTML report. |
| Benchmark aggregation | `aggregate_benchmark.py` discovers configurations such as `with_skill` and `without_skill`, then reports mean/stddev/min/max for pass rate, time, and token counts. |
| Skill hygiene | `quick_validate.py` validates frontmatter and schema limits; `package_skill.py` validates and zips a `.skill` package. |

Relevant upstream files:

- [`run_eval.py`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/run_eval.py)
- [`run_loop.py`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/run_loop.py)
- [`aggregate_benchmark.py`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/aggregate_benchmark.py)
- [`SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

### Upstream limitations

1. **Claude CLI coupling.** Evaluation and optimization shell out to `claude -p`; there is no provider abstraction for OpenAI, Gemini, or local models.
2. **Claude-Code-specific triggering.** Evaluation relies on Claude Code command discovery, stream-event format, and `Skill`/`Read` tools. Other providers do not expose this protocol.
3. **Single model role.** The loop's `--model` is used for both model-under-test and description improvement. Executor, optimizer, and grader should be independently configurable.
4. **Weak comparison semantics.** The aggregator supports arbitrary configuration folders, but its delta is based on the first two discovered configurations, rather than a named, paired baseline.
5. **Basic flake handling.** Retries and thresholds exist, but timeout/provider failures become `False`; there are no provider-aware retry policies, rate limits, confidence intervals, or paired significance tests.
6. **Potential false negatives.** Trigger detection returns false if an unexpected tool starts before `Skill`/`Read`; an agent may use a valid tool before consulting a skill.
7. **Duplicate-query collision.** Trigger results are keyed by literal query text rather than immutable evaluation IDs.
8. **File-backed experiment state.** Results are distributed across directories and JSON files (`grading.json`, `timing.json`, `eval_metadata.json`), which makes querying, resuming, and cross-model comparisons harder.

## Evaluation modes

### 1. Portable execution evaluation (primary)

Use this to assess skill quality across models.

- Give every run the same task, capability profile, tool definitions, working directory, and model settings.
- `with_full_skill`: inject the resolved `SKILL.md` plus allowed referenced resources into a standardized skill context.
- `without_skill`: omit skill context while preserving every other input.
- Grade task outputs, generated artifacts, tool use, cost, and latency.
- Run through provider adapters for Claude, OpenAI, Gemini, local models, and OpenAI-compatible endpoints.

The evaluator must resolve the skill upfront. This intentionally measures the value of the skill's instructions and resources, without conflating results with proprietary/native skill discovery.

### 2. Native routing evaluation (optional compatibility test)

Keep the existing Claude Code trigger evaluator as a distinct compatibility check. It measures whether Claude Code routes a request to a skill; it must not be mixed into portable execution-quality results.

### Optional conditions

- `without_skill`: baseline.
- `with_metadata_only`: only name/description is available; measures discoverability/routing under an explicitly versioned portable harness.
- `with_full_skill`: resolved skill body and approved resources are available; primary quality condition.

## Controlled harness: capability profiles

A harness cannot disappear entirely: models need a message format, tools, filesystem access, and resource limits. Make it controlled, versioned, and identical for all model and condition runs.

Each run receives:

```text
System: standardized agent policy + capability profile version
Task: evaluation-case prompt
Skill context:
  - omitted for the baseline
  - resolved SKILL.md + permitted referenced resources for with-skill conditions
Tools: identical normalized filesystem/shell/network tools for every model
```

A capability profile should define at least:

- allowed tools and their normalized schemas;
- filesystem input fixture and output directory behavior;
- network policy;
- CPU/wall-clock/tool-call/output-size limits;
- prompt template and tool protocol versions;
- artifact collection rules.

Record its exact version and content hash with every experiment.

## Provider abstraction

Define a provider-neutral adapter interface:

```python
class ModelAdapter(Protocol):
    def run(
        self,
        case: EvalCase,
        skill_context: SkillContext | None,
        capability_profile: CapabilityProfile,
        config: ModelConfig,
    ) -> RunResult: ...
```

Initial adapters:

- `claude-code`: optional native-routing compatibility adapter.
- `anthropic-api`: Messages API and normalized tool-use capture.
- `openai-responses`: Responses API and normalized function/tool-call capture.
- `gemini`: function-call capture.
- `openai-compatible`: local or hosted compatible endpoints.

Every adapter returns the same normalized result: provider, resolved model/version, evaluation-case ID, condition, repetition, outcome/status, tool calls, transcript, timing, token use, cost, error details, and generated artifacts.

## Model-matrix configuration

Replace a single `--model` argument with a versioned YAML/JSON experiment configuration:

```yaml
executors:
  - id: claude-sonnet
    provider: anthropic-api
    model: claude-sonnet
    settings:
      temperature: 0
  - id: gpt-5
    provider: openai
    model: gpt-5
    settings:
      temperature: 0

conditions:
  - without_skill
  - with_full_skill

repetitions: 5
capability_profile: restricted-filesystem-v1
grader:
  provider: anthropic-api
  model: claude-sonnet
```

Keep these roles independent:

- **executor model(s):** perform the task;
- **optimizer model:** optionally revises a skill or its description;
- **grader/judge model:** evaluates subjective qualities;
- **deterministic graders:** validate objective assertions.

## SQLite experiment backend

Store one portable SQLite database per experiment suite, for example `skill-evals.db`. During execution, adapters may use isolated temporary workspaces; ingest all final outputs and metadata into SQLite.

Enable foreign keys and WAL mode. Use a single writer queue for high-concurrency scheduling.

### Core schema

```sql
CREATE TABLE experiment (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  skill_name TEXT NOT NULL,
  skill_sha256 TEXT NOT NULL,
  eval_set_sha256 TEXT NOT NULL,
  capability_profile TEXT NOT NULL,
  harness_version TEXT NOT NULL
);

CREATE TABLE model (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  model_name TEXT NOT NULL,
  settings_json TEXT NOT NULL
);

CREATE TABLE eval_case (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL REFERENCES experiment(id),
  prompt TEXT NOT NULL,
  assertions_json TEXT NOT NULL,
  input_artifacts_json TEXT NOT NULL
);

CREATE TABLE condition (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL REFERENCES experiment(id),
  name TEXT NOT NULL,
  skill_context_json TEXT NOT NULL
);

CREATE TABLE attempt (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL REFERENCES experiment(id),
  eval_case_id TEXT NOT NULL REFERENCES eval_case(id),
  model_id TEXT NOT NULL REFERENCES model(id),
  condition_id TEXT NOT NULL REFERENCES condition(id),
  repetition INTEGER NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT,
  finished_at TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  cost_usd REAL,
  duration_ms INTEGER,
  error_json TEXT,
  transcript TEXT
);

CREATE TABLE grade (
  id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL REFERENCES attempt(id),
  grader_id TEXT NOT NULL,
  assertion_id TEXT NOT NULL,
  passed INTEGER NOT NULL,
  score REAL,
  evidence TEXT NOT NULL
);

CREATE TABLE artifact (
  id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL REFERENCES attempt(id),
  path TEXT NOT NULL,
  media_type TEXT,
  sha256 TEXT NOT NULL,
  content BLOB NOT NULL
);

CREATE INDEX attempt_by_case ON attempt(experiment_id, eval_case_id);
CREATE INDEX attempt_by_model_condition ON attempt(model_id, condition_id);
CREATE INDEX attempt_by_status ON attempt(status);
```

### Storage policy

- Store transcripts, metadata, grades, and small generated outputs in SQLite.
- Store generated artifacts as compressed BLOBs with SHA-256 deduplication.
- Enforce artifact-size limits. For large artifacts, either reject them or add a content-addressed object-store backend while retaining authoritative result metadata in SQLite.
- Preserve all experiment inputs: skill snapshot/hash, evaluation corpus, model configuration, capability profile, prompts, grader rubric, and randomization settings.

## Metrics and analysis

Report results per model and per condition. Do not hide divergent model behavior behind one cross-model score.

Metrics:

- deterministic assertion pass rate;
- judge score, kept distinct from deterministic grading;
- paired uplift: `with_full_skill - without_skill` for the same model, case, and repetition;
- latency, token use, estimated cost, and tool-call count;
- error, timeout, and rate-limit rates as separate statuses;
- per-case deltas;
- confidence intervals, preferably bootstrap intervals over paired samples.

Use immutable evaluation-case IDs instead of prompt text as join keys.

## Script migration

| Existing upstream script | Proposed replacement or retained role |
| --- | --- |
| `run_eval.py` | `run_experiment.py`: schedules model adapters against the capability profile and writes attempts to SQLite. |
| `run_loop.py` | `optimize_skill.py`: reads aggregate SQLite results; optimizer is configured separately from executor models. |
| `aggregate_benchmark.py` | SQL-backed aggregation with explicit condition baselines and paired per-model comparisons. |
| `generate_report.py` | Query an experiment ID from SQLite and render HTML/JSON reports. |
| `improve_description.py` | Retain for optional native-routing/metadata optimization only; it is not the primary portable evaluator. |
| `grading.json`, `timing.json`, `eval_metadata.json` | SQLite records and immutable experiment snapshots. |

## Execution hardening

- Apply provider-specific concurrency limits, retry/backoff policies, and experiment budgets.
- Store timeout, rate-limit, invalid-response, and adapter failures explicitly; never coerce them to a failed trigger or failed task result.
- Use isolated temporary workspaces per attempt; do not share a mutable `.claude` directory.
- Version prompt templates, tool schemas, model settings, capability profiles, skill snapshots, and grader rubrics.
- Add resumable scheduling: queued and interrupted attempts can be safely claimed/retried without overwriting completed records.

## Implementation phases

1. **Define portable protocol**
   - Specify capability profiles and resolved skill-context format.
   - Define normalized adapter request/result types.
   - Choose baseline and skill conditions.

2. **Create SQLite foundation**
   - Add migrations, repository/query layer, experiment creation, artifact ingestion, and import tooling for existing JSON workspaces.

3. **Build portable evaluator MVP**
   - Implement a single API adapter using the portable protocol.
   - Execute paired `with_full_skill`/`without_skill` runs.
   - Add deterministic graders and basic SQL summaries.

4. **Add model matrix and reporting**
   - Implement multiple provider adapters.
   - Add provider-aware quotas/retries, paired aggregation, cost accounting, and HTML/JSON reporting.

5. **Retain native compatibility testing separately**
   - Preserve the Claude Code trigger evaluator under a clearly named native-routing mode.
   - Do not combine routing scores with execution-quality scores.

## Rough effort

- **MVP (one API provider, SQLite, paired evaluation):** 3–5 engineering days.
- **Useful multi-provider platform (three providers, reports, grading, quotas):** 2–3 weeks.
- **Production-grade system (resumability, cost controls, local models, CI gates, statistics):** 4–6 weeks.
