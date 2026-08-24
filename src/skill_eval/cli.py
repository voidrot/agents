"""The installable `skill-eval` command-line interface."""

# pyright: reportMissingImports=false
from __future__ import annotations

import asyncio
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal, NoReturn

import typer

from .config import (
    AppConfig,
    ConfigurationError,
    load_config,
    resolve_database_path,
    write_config_template,
)
from .enhancement import (
    EnhancementError,
    apply_skill_markdown,
    propose_skill_revision,
    skill_markdown_diff,
)
from .evaluator import EvaluationRunner
from .executor import PydanticAIExecutor
from .harness import HarnessError, snapshot_skill
from .native_route import NativeRouteError, run_native_route_check
from .persistence import ExperimentRepository, PersistenceError
from .providers import create_model
from .skills import SkillValidationError, package_skill, validate_skill
from .storage import (
    DatabaseMigrationError,
    backup_database,
    database_status,
    migrate_database,
)
from .suites import load_suite

app = typer.Typer(
    name="skill-eval",
    help="Evaluate portable agent skills across configured models.",
    no_args_is_help=True,
)
config_app = typer.Typer(help="Inspect and create global YAML configuration.")
db_app = typer.Typer(help="Inspect and back up the local experiment database.")
app.add_typer(config_app, name="config")
app.add_typer(db_app, name="db")


@dataclass(frozen=True)
class AppState:
    """Resolved settings available to every database-using command."""

    config: AppConfig
    config_path: Path
    database_path: Path
    schema_revision: str | None


def _fail(message: str) -> NoReturn:
    typer.secho(f"Error: {message}", fg=typer.colors.RED, err=True)
    raise typer.Exit(code=2)


def _validate_output_format(output_format: str) -> None:
    if output_format not in {"text", "json"}:
        _fail("--format must be text or json")


def _state(ctx: typer.Context) -> AppState:
    state = ctx.obj
    if not isinstance(state, AppState):
        raise TypeError("application state was not initialized")
    return state


@app.callback()
def initialize_application(
    ctx: typer.Context,
    config: Annotated[
        Path | None,
        typer.Option("--config", help="Path to global YAML configuration."),
    ] = None,
    database: Annotated[
        Path | None,
        typer.Option("--database", help="SQLite database path for this invocation."),
    ] = None,
) -> None:
    """Resolve configuration and migrate the selected database before dispatch."""
    try:
        loaded_config, config_path = load_config(config)
        database_path = resolve_database_path(loaded_config, database)
        revision = migrate_database(database_path)
    except (ConfigurationError, DatabaseMigrationError) as error:
        _fail(str(error))
    ctx.obj = AppState(
        config=loaded_config,
        config_path=config_path,
        database_path=database_path,
        schema_revision=revision,
    )


@app.command()
def validate(
    ctx: typer.Context,
    skill_directory: Annotated[
        Path, typer.Argument(help="Directory containing SKILL.md.")
    ],
    strict: Annotated[
        bool,
        typer.Option(
            "--strict",
            help="Reject relative Markdown references escaping the skill root.",
        ),
    ] = False,
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: text or json."),
    ] = "text",
) -> None:
    """Validate a skill's frontmatter and optional resource references."""
    _validate_output_format(output_format)
    try:
        skill = validate_skill(skill_directory, strict=strict)
    except SkillValidationError as error:
        _fail(str(error))

    payload = {
        "valid": True,
        "name": skill.name,
        "description": skill.description,
        "path": str(skill.directory),
        "schema_revision": _state(ctx).schema_revision,
    }
    if output_format == "json":
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    else:
        typer.echo(f"Valid skill: {skill.name} ({skill.directory})")


@app.command()
def package(
    skill_directory: Annotated[
        Path, typer.Argument(help="Directory containing SKILL.md.")
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", help="Directory where the .skill archive is written."),
    ] = None,
) -> None:
    """Validate then create a deterministic .skill archive."""
    try:
        archive = package_skill(skill_directory, output)
    except SkillValidationError as error:
        _fail(str(error))
    typer.echo(archive)


@config_app.command("path")
def config_path(ctx: typer.Context) -> None:
    """Print the configured YAML path and selected database path."""
    state = _state(ctx)
    typer.echo(
        json.dumps(
            {"config": str(state.config_path), "database": str(state.database_path)}
        )
    )


@config_app.command("init")
def config_init(
    ctx: typer.Context,
    force: Annotated[
        bool, typer.Option("--force", help="Replace an existing configuration file.")
    ] = False,
) -> None:
    """Create a safe commented global configuration template."""
    path = _state(ctx).config_path
    try:
        write_config_template(path, force=force)
    except ConfigurationError as error:
        _fail(str(error))
    typer.echo(path)


@config_app.command("show")
def config_show(ctx: typer.Context) -> None:
    """Show resolved non-secret settings as JSON."""
    state = _state(ctx)
    payload = state.config.model_dump(mode="json")
    payload["resolved_database"] = str(state.database_path)
    payload["schema_revision"] = state.schema_revision
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@config_app.command("validate")
def config_validate(ctx: typer.Context) -> None:
    """Confirm configuration is valid without contacting model providers."""
    state = _state(ctx)
    typer.echo(f"Valid configuration: {state.config_path}")


@db_app.command("status")
def db_status(ctx: typer.Context) -> None:
    """Show current and packaged schema revisions."""
    state = _state(ctx)
    current, head = database_status(state.database_path)
    typer.echo(
        json.dumps(
            {
                "database": str(state.database_path),
                "current_revision": current,
                "head_revision": head,
                "at_head": current == head,
            },
            indent=2,
            sort_keys=True,
        )
    )


@db_app.command("backup")
def db_backup(
    ctx: typer.Context,
    output: Annotated[
        Path | None,
        typer.Option("--output", help="Destination for a consistent SQLite backup."),
    ] = None,
) -> None:
    """Create an explicit consistent backup of the migrated database."""
    try:
        backup = backup_database(_state(ctx).database_path, output)
    except DatabaseMigrationError as error:
        _fail(str(error))
    typer.echo(backup)


@app.command()
def evaluate(
    ctx: typer.Context,
    skill_directory: Annotated[
        Path, typer.Argument(help="Directory containing the skill to evaluate.")
    ],
    suite_path: Annotated[
        Path,
        typer.Option("--suite", help="Versioned YAML evaluation suite."),
    ],
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: text or json."),
    ] = "text",
    enhance_after: Annotated[
        bool,
        typer.Option(
            "--enhance",
            help="Propose and holdout-evaluate a candidate after baseline evaluation.",
        ),
    ] = False,
) -> None:
    """Run paired portable evaluation conditions and optionally propose a candidate."""
    _validate_output_format(output_format)
    state = _state(ctx)
    try:
        suite = load_suite(suite_path)
        models = {
            alias: create_model(state.config, alias) for alias in suite.suite.executors
        }
        summary = asyncio.run(
            EvaluationRunner(
                ExperimentRepository(state.database_path),
                PydanticAIExecutor(),
            ).run(
                suite=suite,
                skill_snapshot=snapshot_skill(skill_directory),
                models=models,
                redacted_config=state.config.model_dump(mode="json"),
                harness_version="skill-eval/0.1",
            )
        )
    except (HarnessError, PersistenceError, ValueError) as error:
        _fail(str(error))

    payload = {
        "experiment_id": summary.experiment_id,
        "queued_attempts": summary.queued_attempts,
        "completed_attempts": summary.completed_attempts,
        "failed_attempts": summary.failed_attempts,
    }
    if enhance_after:
        try:
            payload["enhancement"] = _propose_candidate(
                state, ExperimentRepository(state.database_path), summary.experiment_id
            )
        except (PersistenceError, ValueError) as error:
            _fail(str(error))
    if output_format == "json":
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    else:
        typer.echo(
            f"Experiment {summary.experiment_id}: {summary.completed_attempts}/"
            f"{summary.queued_attempts} completed, {summary.failed_attempts} failed"
        )


@app.command()
def resume(
    ctx: typer.Context,
    experiment_id: Annotated[str, typer.Argument(help="Interrupted experiment ID.")],
    output_format: Annotated[
        str, typer.Option("--format", help="Output format: text or json.")
    ] = "text",
) -> None:
    """Resume queued or interrupted attempts using persisted replay snapshots."""
    _validate_output_format(output_format)
    state = _state(ctx)
    repository = ExperimentRepository(state.database_path)
    try:
        aliases = repository.experiment_executor_aliases(experiment_id)
        models = {alias: create_model(state.config, alias) for alias in aliases}
        summary = asyncio.run(
            EvaluationRunner(repository, PydanticAIExecutor()).resume(
                experiment_id=experiment_id, models=models
            )
        )
    except (HarnessError, PersistenceError, ValueError, KeyError) as error:
        _fail(str(error))
    payload = {
        "experiment_id": summary.experiment_id,
        "resumed_attempts": summary.queued_attempts,
        "completed_attempts": summary.completed_attempts,
        "failed_attempts": summary.failed_attempts,
    }
    typer.echo(
        json.dumps(payload, indent=2, sort_keys=True)
        if output_format == "json"
        else f"Experiment {summary.experiment_id}: resumed {summary.queued_attempts} attempts"
    )


@app.command()
def report(
    ctx: typer.Context,
    experiment_id: Annotated[str, typer.Argument(help="Persisted experiment ID.")],
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: text or json."),
    ] = "text",
) -> None:
    """Render a concise status report from persisted attempts."""
    _validate_output_format(output_format)
    repository = ExperimentRepository(_state(ctx).database_path)
    attempts = repository.list_attempts(experiment_id)
    report_rows = repository.list_report_rows(experiment_id)
    status_counts = Counter(str(attempt["status"]) for attempt in attempts)
    scores_by_condition: dict[str, list[float]] = defaultdict(list)
    paired_scores: dict[tuple[str, int, str], dict[str, float]] = defaultdict(dict)
    try:
        for row in report_rows:
            score = row["grade_pass_rate"]
            if score is None:
                continue
            condition = str(row["condition_name"])
            numeric_score = float(score)
            scores_by_condition[condition].append(numeric_score)
            alias = str(
                json.loads(str(row["settings_json"])).get(
                    "configured_alias", row["model_id"]
                )
            )
            paired_scores[(str(row["eval_case_id"]), int(row["repetition"]), alias)][
                condition
            ] = numeric_score
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        _fail(f"experiment contains malformed report metadata: {error}")
    condition_pass_rates = {
        condition: sum(scores) / len(scores)
        for condition, scores in sorted(scores_by_condition.items())
    }
    paired_deltas: dict[str, list[float]] = defaultdict(list)
    for scores in paired_scores.values():
        baseline = scores.get("without_skill")
        if baseline is None:
            continue
        for condition, score in scores.items():
            if condition != "without_skill":
                paired_deltas[condition].append(score - baseline)
    payload = {
        "experiment_id": experiment_id,
        "attempt_count": len(attempts),
        "status_counts": dict(sorted(status_counts.items())),
        "condition_pass_rates": condition_pass_rates,
        "paired_pass_rate_deltas": {
            condition: sum(deltas) / len(deltas)
            for condition, deltas in sorted(paired_deltas.items())
        },
        "attempts": attempts,
    }
    if output_format == "json":
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    else:
        typer.echo(f"Experiment {experiment_id}: {len(attempts)} attempts")
        for status, count in sorted(status_counts.items()):
            typer.echo(f"  {status}: {count}")


@app.command()
def enhance(
    ctx: typer.Context,
    experiment_id: Annotated[str, typer.Argument(help="Experiment to improve.")],
    output_format: Annotated[
        str, typer.Option("--format", help="Output format: text or json.")
    ] = "text",
    apply_candidate: Annotated[
        str | None, typer.Option("--apply", help="Candidate ID to apply.")
    ] = None,
    skill_directory: Annotated[
        Path | None,
        typer.Option("--skill-dir", help="Target skill directory for --apply."),
    ] = None,
    yes: Annotated[
        bool, typer.Option("--yes", help="Apply without interactive confirmation.")
    ] = False,
) -> None:
    """Propose a candidate, or explicitly review and apply an existing candidate."""
    _validate_output_format(output_format)
    state = _state(ctx)
    repository = ExperimentRepository(state.database_path)
    if apply_candidate is not None:
        if skill_directory is None:
            _fail("--skill-dir is required with --apply")
        try:
            candidate = repository.get_candidate(apply_candidate)
            source = repository.get_skill_snapshot(str(candidate["source_snapshot_id"]))
            revision = repository.get_skill_snapshot(
                str(candidate["candidate_snapshot_id"])
            )
            diff = skill_markdown_diff(
                str(source["skill_md"]), str(revision["skill_md"])
            )
            typer.echo(diff or "No SKILL.md changes in this candidate.")
            if not yes and not typer.confirm("Apply this candidate to SKILL.md?"):
                typer.echo("Not applied.")
                return
            apply_skill_markdown(
                skill_directory=skill_directory,
                source=str(source["skill_md"]),
                candidate=str(revision["skill_md"]),
            )
        except (PersistenceError, ValueError) as error:
            _fail(str(error))
        typer.echo(f"Applied candidate {apply_candidate} to {skill_directory}.")
        return
    try:
        payload = _propose_candidate(state, repository, experiment_id)
    except (PersistenceError, ValueError) as error:
        _fail(str(error))
    payload["experiment_id"] = experiment_id
    candidate_id = payload["candidate_id"]
    typer.echo(
        json.dumps(payload, indent=2, sort_keys=True)
        if output_format == "json"
        else f"Proposed candidate {candidate_id}; review it before applying."
    )


def _propose_candidate(
    state: AppState, repository: ExperimentRepository, experiment_id: str
) -> dict[str, object]:
    """Create and holdout-evaluate a candidate without applying it."""
    enhancer_alias = state.config.defaults.enhancer
    if enhancer_alias is None:
        raise EnhancementError(
            "configure defaults.enhancer before requesting a proposal"
        )
    source = repository.experiment_source_snapshot(experiment_id)
    model = create_model(state.config, enhancer_alias)
    proposal = asyncio.run(
        propose_skill_revision(
            model=model,
            source_skill_md=str(source["skill_md"]),
            failure_summary=repository.failure_summary(experiment_id),
        )
    )
    model_id = repository.store_model(
        provider=model.provider_kind,
        model_name=model.model_name,
        settings={
            "configured_alias": model.alias,
            "provider_alias": model.provider_alias,
        },
    )
    try:
        manifest = json.loads(str(source["manifest_json"]))
    except json.JSONDecodeError as error:
        raise PersistenceError("source snapshot has invalid manifest JSON") from error
    candidate_snapshot_id = repository.store_skill_snapshot(
        experiment_id=experiment_id,
        parent_snapshot_id=str(source["id"]),
        manifest=manifest,
        skill_md=proposal.skill_md,
    )
    for resource in repository.list_skill_resources(str(source["id"])):
        repository.store_skill_resource(
            skill_snapshot_id=candidate_snapshot_id,
            path=str(resource["path"]),
            content=bytes(resource["content"]),
        )
    candidate_id = repository.create_candidate(
        experiment_id=experiment_id,
        source_snapshot_id=str(source["id"]),
        candidate_snapshot_id=candidate_snapshot_id,
        enhancer_model_id=model_id,
        mode="full-skill",
        rationale=proposal.rationale,
    )
    executor_models = {
        alias: create_model(state.config, alias)
        for alias in repository.experiment_executor_aliases(experiment_id)
    }
    summary = asyncio.run(
        EvaluationRunner(repository, PydanticAIExecutor()).evaluate_candidate(
            candidate_id=candidate_id, models=executor_models
        )
    )
    return {
        "candidate_id": candidate_id,
        "candidate_snapshot_id": candidate_snapshot_id,
        "rationale": proposal.rationale,
        "skill_md": proposal.skill_md,
        "holdout_attempts": summary.queued_attempts,
    }


@app.command("native-route")
def native_route(
    runtime: Annotated[
        Literal["claude", "codex", "pi", "opencode"],
        typer.Argument(help="Runtime: claude, codex, pi, or opencode."),
    ],
    skill_directory: Annotated[
        Path, typer.Argument(help="Skill directory to expose natively.")
    ],
    suite_path: Annotated[
        Path, typer.Option("--suite", help="Suite providing routing prompts.")
    ],
    output_format: Annotated[
        str, typer.Option("--format", help="Output format: text or json.")
    ] = "text",
) -> None:
    """Check native skill discovery through Claude, Codex, Pi, or OpenCode."""
    _validate_output_format(output_format)
    try:
        results = run_native_route_check(
            runtime=runtime,
            skill=validate_skill(skill_directory),
            suite=load_suite(suite_path),
        )
    except (NativeRouteError, ValueError) as error:
        _fail(str(error))
    payload = {"runtime": runtime, "results": [result.__dict__ for result in results]}
    typer.echo(
        json.dumps(payload, indent=2, sort_keys=True)
        if output_format == "json"
        else f"{runtime}: {sum(result.status == 'succeeded' for result in results)}/{len(results)} completed"
    )


def main() -> None:
    """Compatibility wrapper for direct module invocation."""
    app()
