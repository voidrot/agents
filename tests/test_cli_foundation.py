"""Foundation behavior for the installable CLI and automatic SQLite upgrades."""

# pyright: reportMissingImports=false
from __future__ import annotations

import asyncio
import json
import sqlite3
from pathlib import Path

import pytest
from pydantic_ai.models.test import TestModel
from typer.testing import CliRunner

from skill_eval.cli import app
from skill_eval.config import AppConfig, ConfigurationError, load_config
from skill_eval.enhancement import (
    EnhancementError,
    apply_skill_markdown,
    propose_skill_revision,
    skill_markdown_diff,
)
from skill_eval.evaluator import EvaluationRunner
from skill_eval.executor import ExecutionRequest, PydanticAIExecutor, ToolSandbox
from skill_eval.grading import (
    GradeResult,
    grade_assertions,
    persist_deterministic_grades,
)
from skill_eval.harness import (
    collect_artifacts,
    isolated_workspace,
    rehydrated_replay_sources,
    snapshot_skill,
)
from skill_eval.persistence import ExperimentRepository, PersistenceError
from skill_eval.providers import ProviderConfigurationError, ResolvedModel, create_model
from skill_eval.skills import SkillValidationError, package_skill, validate_skill
from skill_eval.storage import backup_database, database_status, migrate_database
from skill_eval.suites import (
    AssertionSpec,
    SuiteError,
    load_suite,
    resolve_capability_profile,
)

runner = CliRunner()


def create_skill(directory: Path) -> Path:
    directory.mkdir()
    (directory / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Use this for safe examples.\n---\n\n# Example\n",
        encoding="utf-8",
    )
    return directory


def test_startup_migrates_a_new_database_and_is_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "state" / "skill-evals.db"

    assert migrate_database(database) == "0005_skill_resources"
    assert migrate_database(database) == "0005_skill_resources"
    assert database_status(database) == (
        "0005_skill_resources",
        "0005_skill_resources",
    )

    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT version_num FROM alembic_version"
        ).fetchone() == ("0005_skill_resources",)
        assert connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'attempt'"
        ).fetchone()


def test_database_backup_uses_a_consistent_sqlite_copy(tmp_path: Path) -> None:
    database = tmp_path / "skill-evals.db"
    migrate_database(database)

    backup = backup_database(database)

    assert backup.exists()
    assert database_status(backup) == (
        "0005_skill_resources",
        "0005_skill_resources",
    )


def test_startup_upgrades_a_historical_0001_database(tmp_path: Path) -> None:
    database = tmp_path / "historical.db"
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
        )
        connection.execute(
            "INSERT INTO alembic_version (version_num) VALUES ('0001_initial_metadata')"
        )
        connection.execute(
            "CREATE TABLE application_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT NOT NULL)"
        )

    assert migrate_database(database) == "0005_skill_resources"
    assert database_status(database) == (
        "0005_skill_resources",
        "0005_skill_resources",
    )


def test_cli_migrates_before_validating_a_skill(tmp_path: Path) -> None:
    database = tmp_path / "skill-evals.db"
    skill = create_skill(tmp_path / "example-skill")

    result = runner.invoke(
        app,
        ["--database", str(database), "validate", str(skill), "--format", "json"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["valid"] is True
    assert payload["schema_revision"] == "0005_skill_resources"
    assert database_status(database) == (
        "0005_skill_resources",
        "0005_skill_resources",
    )


def test_repository_persists_and_claims_a_paired_attempt(tmp_path: Path) -> None:
    database = tmp_path / "skill-evals.db"
    migrate_database(database)
    repository = ExperimentRepository(database)
    config_id = repository.store_config_snapshot({"version": 1, "providers": {}})
    model_id = repository.store_model(
        provider="ollama", model_name="qwen3", settings={"temperature": 0}
    )
    experiment_id = repository.create_experiment(
        skill_name="example-skill",
        skill_sha256="skill-hash",
        eval_set_sha256="eval-hash",
        capability_profile="restricted-filesystem-v1",
        harness_version="0.1",
        config_snapshot_id=config_id,
    )
    case_id = repository.add_eval_case(
        experiment_id=experiment_id,
        prompt="Create the requested output.",
        assertions=[{"id": "output-exists", "type": "file_exists", "path": "out.txt"}],
    )
    condition_id = repository.add_condition(
        experiment_id=experiment_id,
        name="without_skill",
        skill_context={"mode": "omitted"},
    )
    snapshot_id = repository.store_skill_snapshot(
        experiment_id=experiment_id,
        manifest={"SKILL.md": "skill-hash"},
        skill_md="# Example skill\n",
    )
    candidate_snapshot_id = repository.store_skill_snapshot(
        experiment_id=experiment_id,
        parent_snapshot_id=snapshot_id,
        manifest={"SKILL.md": "candidate-hash"},
        skill_md="# Improved example skill\n",
    )
    candidate_id = repository.create_candidate(
        experiment_id=experiment_id,
        source_snapshot_id=snapshot_id,
        candidate_snapshot_id=candidate_snapshot_id,
        enhancer_model_id=model_id,
        mode="full-skill",
        rationale="Clarify the required output.",
    )
    attempt_id = repository.queue_attempt(
        experiment_id=experiment_id,
        eval_case_id=case_id,
        model_id=model_id,
        condition_id=condition_id,
        skill_snapshot_id=snapshot_id,
        repetition=0,
    )

    claim = repository.claim_next_attempt(experiment_id)
    assert claim is not None
    assert claim.id == attempt_id
    assert claim.status == "running"
    assert repository.claim_next_attempt(experiment_id) is None
    assert repository.requeue_interrupted_attempts(experiment_id) == 1
    claim = repository.claim_next_attempt(experiment_id)
    assert claim is not None
    assert repository.requeue_interrupted_attempts(experiment_id) == 1
    claim = repository.claim_next_attempt(experiment_id)
    assert claim is not None

    repository.complete_attempt(
        attempt_id=attempt_id,
        status="succeeded",
        transcript="Created out.txt",
        input_tokens=10,
        output_tokens=20,
        duration_ms=35,
        tool_calls=2,
    )
    persist_deterministic_grades(
        repository,
        attempt_id=attempt_id,
        grader_id=model_id,
        results=[
            GradeResult(
                assertion_id="output-exists",
                passed=True,
                evidence="out.txt exists",
                score=1.0,
            )
        ],
    )
    repository.add_artifact(attempt_id=attempt_id, path="out.txt", content=b"done\n")

    with pytest.raises(PersistenceError, match="running"):
        repository.complete_attempt(attempt_id=attempt_id, status="failed")

    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT status FROM attempt WHERE id = ?", (attempt_id,)
        ).fetchone() == ("succeeded",)
        assert connection.execute(
            "SELECT tool_calls FROM attempt WHERE id = ?", (attempt_id,)
        ).fetchone() == (2,)
        assert connection.execute(
            "SELECT passed FROM grade WHERE attempt_id = ?", (attempt_id,)
        ).fetchone() == (1,)
        assert connection.execute(
            "SELECT content FROM artifact WHERE attempt_id = ?", (attempt_id,)
        ).fetchone() == (b"done\n",)
        assert connection.execute(
            "SELECT candidate_snapshot_id FROM candidate WHERE id = ?", (candidate_id,)
        ).fetchone() == (candidate_snapshot_id,)

    assert repository.list_attempts(experiment_id)[0]["status"] == "succeeded"
    report = runner.invoke(
        app,
        ["--database", str(database), "report", experiment_id, "--format", "json"],
    )
    assert report.exit_code == 0, report.output
    report_payload = json.loads(report.output)
    assert report_payload["status_counts"] == {"succeeded": 1}
    assert report_payload["condition_pass_rates"] == {"without_skill": 1.0}
    assert report_payload["paired_pass_rate_deltas"] == {}


def test_config_rejects_literal_secrets(tmp_path: Path) -> None:
    config = tmp_path / "config.yaml"
    config.write_text(
        "providers:\n  openai:\n    api_key: do-not-store-me\n", encoding="utf-8"
    )

    with pytest.raises(ConfigurationError, match="api_key"):
        load_config(config)


def test_isolated_workspace_copies_only_declared_inputs_and_collects_output(
    tmp_path: Path,
) -> None:
    skill = create_skill(tmp_path / "example-skill")
    (skill / "references").mkdir()
    (skill / "references" / "guide.md").write_text("Guide\n", encoding="utf-8")
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "input.txt").write_text("input\n", encoding="utf-8")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        """executors: [local]
cases:
  - id: write-output
    prompt: Write output from input.
    fixtures: [fixtures/input.txt]
""",
        encoding="utf-8",
    )
    suite = load_suite(suite_path)
    skill_snapshot = snapshot_skill(skill)
    case = suite.suite.cases[0]

    with isolated_workspace(
        skill_snapshot=skill_snapshot, suite=suite, case=case
    ) as workspace:
        assert (
            workspace.skill_directory / "references" / "guide.md"
        ).read_text() == "Guide\n"
        assert (
            workspace.input_directory / "fixtures" / "input.txt"
        ).read_text() == "input\n"
        (workspace.output_directory / "result.txt").write_text(
            "done\n", encoding="utf-8"
        )
        artifacts = collect_artifacts(
            workspace,
            resolve_capability_profile(suite.suite.capability_profile),
        )
        root = workspace.root

    assert not root.exists()
    assert [(artifact.path, artifact.content) for artifact in artifacts] == [
        ("result.txt", b"done\n")
    ]


def test_executor_tools_are_sandboxed_and_test_model_returns_normalized_result(
    tmp_path: Path,
) -> None:
    skill = create_skill(tmp_path / "example-skill")
    fixture = tmp_path / "fixture.txt"
    fixture.write_text("input\n", encoding="utf-8")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        """executors: [test]
cases:
  - id: execute
    prompt: Respond without tools.
    fixtures: [fixture.txt]
""",
        encoding="utf-8",
    )
    suite = load_suite(suite_path)
    skill_snapshot = snapshot_skill(skill)
    profile = resolve_capability_profile(suite.suite.capability_profile)
    model = ResolvedModel(
        alias="test",
        provider_alias="test",
        provider_kind="test",
        model_name="test",
        model=TestModel(call_tools=[]),
    )

    with isolated_workspace(
        skill_snapshot=skill_snapshot,
        suite=suite,
        case=suite.suite.cases[0],
    ) as workspace:
        sandbox = ToolSandbox(workspace, profile)
        assert sandbox.read_file("inputs/fixture.txt") == "input\n"
        assert sandbox.write_output("nested/result.txt", "done\n").startswith("wrote")
        assert sandbox.tool_calls == 2

        result = asyncio.run(
            PydanticAIExecutor().run(
                ExecutionRequest(
                    model=model,
                    case=suite.suite.cases[0],
                    condition="without_skill",
                    skill_snapshot=skill_snapshot,
                    workspace=workspace,
                    profile=profile,
                )
            )
        )

    assert result.status == "succeeded"
    assert result.raw_messages_json is not None
    assert result.input_tokens is not None


def test_evaluation_runner_executes_paired_conditions_and_persists_attempts(
    tmp_path: Path,
) -> None:
    database = tmp_path / "skill-evals.db"
    migrate_database(database)
    skill = create_skill(tmp_path / "example-skill")
    fixture = tmp_path / "fixture.txt"
    fixture.write_text("snapshot me\n", encoding="utf-8")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        """executors: [test]
repetitions: 1
conditions: [without_skill, with_full_skill]
cases:
  - id: execute
    prompt: Respond without tools.
    fixtures: [fixture.txt]
""",
        encoding="utf-8",
    )
    suite = load_suite(suite_path)
    model = ResolvedModel(
        alias="test",
        provider_alias="test",
        provider_kind="test",
        model_name="test",
        model=TestModel(call_tools=[]),
    )

    summary = asyncio.run(
        EvaluationRunner(ExperimentRepository(database), PydanticAIExecutor()).run(
            suite=suite,
            skill_snapshot=snapshot_skill(skill),
            models={"test": model},
            redacted_config={"version": 1, "models": {"test": {}}},
            harness_version="test",
        )
    )

    assert summary.queued_attempts == 2
    assert summary.completed_attempts == 2
    assert summary.failed_attempts == 0
    attempts = ExperimentRepository(database).list_attempts(summary.experiment_id)
    assert {attempt["status"] for attempt in attempts} == {"succeeded"}
    assert {attempt["tool_calls"] for attempt in attempts} == {0}
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT path, content FROM input_artifact"
        ).fetchall() == [("fixture.txt", b"snapshot me\n")]
    fixture.write_text("changed after experiment\n", encoding="utf-8")
    with rehydrated_replay_sources(
        ExperimentRepository(database),
        experiment_id=summary.experiment_id,
        skill_snapshot_id=str(attempts[0]["skill_snapshot_id"]),
    ) as (replay_suite, replay_skill):
        assert replay_suite.fixture_paths["execute"][0].read_text() == "snapshot me\n"
        assert replay_skill.sha256 == snapshot_skill(skill).sha256
    with sqlite3.connect(database) as connection:
        connection.execute(
            "UPDATE attempt SET status = 'running', finished_at = NULL WHERE id = ?",
            (attempts[0]["id"],),
        )
    resumed = asyncio.run(
        EvaluationRunner(ExperimentRepository(database), PydanticAIExecutor()).resume(
            experiment_id=summary.experiment_id, models={"test": model}
        )
    )
    assert resumed.queued_attempts == 1
    assert {
        attempt["status"]
        for attempt in ExperimentRepository(database).list_attempts(
            summary.experiment_id
        )
    } == {"succeeded"}
    repository = ExperimentRepository(database)
    source_snapshot_id = str(attempts[0]["skill_snapshot_id"])
    candidate_snapshot_id = repository.store_skill_snapshot(
        experiment_id=summary.experiment_id,
        parent_snapshot_id=source_snapshot_id,
        manifest=snapshot_skill(skill).manifest,
        skill_md=(skill / "SKILL.md").read_text(encoding="utf-8"),
    )
    for resource in repository.list_skill_resources(source_snapshot_id):
        repository.store_skill_resource(
            skill_snapshot_id=candidate_snapshot_id,
            path=str(resource["path"]),
            content=bytes(resource["content"]),
        )
    model_id = repository.store_model(
        provider="test",
        model_name="test",
        settings={"configured_alias": "test", "provider_alias": "test"},
    )
    candidate_id = repository.create_candidate(
        experiment_id=summary.experiment_id,
        source_snapshot_id=source_snapshot_id,
        candidate_snapshot_id=candidate_snapshot_id,
        enhancer_model_id=model_id,
        mode="full-skill",
    )
    candidate_summary = asyncio.run(
        EvaluationRunner(repository, PydanticAIExecutor()).evaluate_candidate(
            candidate_id=candidate_id, models={"test": model}
        )
    )
    assert candidate_summary.queued_attempts == 1


def test_candidate_diff_and_application_require_an_unchanged_source(
    tmp_path: Path,
) -> None:
    skill = create_skill(tmp_path / "apply-skill")
    source = (skill / "SKILL.md").read_text(encoding="utf-8")
    candidate = source.replace(
        "Use this for safe examples.", "Use this for clearer examples."
    )
    assert "clearer" in skill_markdown_diff(source, candidate)
    apply_skill_markdown(skill_directory=skill, source=source, candidate=candidate)
    assert (skill / "SKILL.md").read_text(encoding="utf-8") == candidate
    with pytest.raises(EnhancementError, match="differs"):
        apply_skill_markdown(skill_directory=skill, source=source, candidate=candidate)


def test_enhancement_proposal_returns_a_valid_complete_skill() -> None:
    model = ResolvedModel(
        alias="enhancer",
        provider_alias="test",
        provider_kind="test",
        model_name="test",
        model=TestModel(
            custom_output_args={
                "skill_md": "---\nname: example-skill\ndescription: Improved safe examples.\n---\n\n# Example\n",
                "rationale": "Clarifies the expected output.",
            }
        ),
    )
    proposal = asyncio.run(
        propose_skill_revision(
            model=model,
            source_skill_md="---\nname: example-skill\ndescription: Use examples.\n---\n\n# Example\n",
            failure_summary="- output-exists: output was missing",
        )
    )
    assert proposal.rationale == "Clarifies the expected output."
    assert "Improved safe examples" in proposal.skill_md


def test_deterministic_grading_reports_per_assertion_evidence(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    (output / "result.txt").write_text("ready for review\n", encoding="utf-8")
    assertions = [
        {"id": "exists", "type": "file_exists", "path": "result.txt"},
        {"id": "contains", "type": "contains", "path": "result.txt", "text": "ready"},
        {"id": "missing", "type": "contains", "path": "result.txt", "text": "absent"},
        {"id": "not-created", "type": "file_exists", "path": "not-created.txt"},
    ]

    results = grade_assertions(
        output,
        [AssertionSpec.model_validate(assertion) for assertion in assertions],
    )

    assert [(result.assertion_id, result.passed) for result in results] == [
        ("exists", True),
        ("contains", True),
        ("missing", False),
        ("not-created", False),
    ]
    assert results[1].score == 1.0
    assert "does not contain" in results[2].evidence


def test_suite_loading_resolves_fixtures_and_enforces_a_baseline(
    tmp_path: Path,
) -> None:
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "input.txt").write_text("input\n", encoding="utf-8")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        """schema_version: 1
executors: [local]
cases:
  - id: write-output
    prompt: Write the requested output.
    fixtures: [fixtures/input.txt]
    assertions:
      - id: output-exists
        type: file_exists
        path: output.txt
      - id: output-content
        type: contains
        path: output.txt
        text: ready
""",
        encoding="utf-8",
    )

    suite = load_suite(suite_path)

    assert suite.suite.conditions == ["without_skill", "with_full_skill"]
    assert suite.fixture_paths["write-output"] == (fixtures / "input.txt",)
    assert (
        resolve_capability_profile(suite.suite.capability_profile).allow_network
        is False
    )


def test_suite_rejects_fixture_paths_outside_its_directory(tmp_path: Path) -> None:
    (tmp_path.parent / "outside.txt").write_text("outside\n", encoding="utf-8")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        """executors: [local]
cases:
  - id: escaping-case
    prompt: Do not escape.
    fixtures: [../outside.txt]
""",
        encoding="utf-8",
    )

    with pytest.raises(SuiteError, match="escapes"):
        load_suite(suite_path)


def test_provider_factory_supports_ollama_and_openai_compatible_endpoints(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = AppConfig.model_validate(
        {
            "providers": {
                "ollama-local": {
                    "kind": "ollama",
                    "base_url": "http://localhost:11434/v1",
                },
                "gateway": {
                    "kind": "openai-compatible",
                    "base_url": "https://gateway.example/v1",
                    "api_key_env": "GATEWAY_API_KEY",
                },
            },
            "models": {
                "local": {"provider": "ollama-local", "model": "qwen3"},
                "remote": {"provider": "gateway", "model": "test-model"},
            },
        }
    )

    local = create_model(config, "local")
    assert local.provider_kind == "ollama"
    assert local.model_name == "qwen3"

    with pytest.raises(ProviderConfigurationError, match="GATEWAY_API_KEY"):
        create_model(config, "remote")

    monkeypatch.setenv("GATEWAY_API_KEY", "test-key")
    remote = create_model(config, "remote")
    assert remote.provider_kind == "openai-compatible"
    assert remote.model_name == "test-model"


def test_strict_validation_rejects_a_reference_outside_skill_root(
    tmp_path: Path,
) -> None:
    skill = create_skill(tmp_path / "example-skill")
    (skill / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Use this for safe examples.\n---\n\n[escape](../secret.md)\n",
        encoding="utf-8",
    )

    with pytest.raises(SkillValidationError, match="escapes skill root"):
        validate_skill(skill, strict=True)


def test_skill_package_is_deterministic(tmp_path: Path) -> None:
    skill = create_skill(tmp_path / "example-skill")
    (skill / "references").mkdir()
    (skill / "references" / "guide.md").write_text("Guide\n", encoding="utf-8")
    first_directory = tmp_path / "first"
    second_directory = tmp_path / "second"

    first = package_skill(skill, first_directory)
    second = package_skill(skill, second_directory)

    assert first.read_bytes() == second.read_bytes()
