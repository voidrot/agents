"""Paired execution orchestration over portable suites and isolated workspaces."""

# pyright: reportMissingImports=false
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Protocol

from .executor import ExecutionRequest, ExecutionResult
from .grading import grade_assertions, persist_deterministic_grades
from .harness import (
    AttemptWorkspace,
    HarnessError,
    SkillSnapshot,
    collect_artifacts,
    isolated_workspace,
    rehydrated_replay_sources,
)
from .persistence import ExperimentRepository
from .providers import ResolvedModel
from .suites import (
    CapabilityProfile,
    EvalCaseSpec,
    ResolvedSuite,
    resolve_capability_profile,
)


class AttemptExecutor(Protocol):
    """The small executor seam used by the scheduler and deterministic tests."""

    async def run(self, request: ExecutionRequest) -> ExecutionResult: ...


@dataclass(frozen=True)
class EvaluationSummary:
    """Persisted experiment identity and terminal-attempt counts."""

    experiment_id: str
    queued_attempts: int
    completed_attempts: int
    failed_attempts: int


class EvaluationRunner:
    """Create, queue, execute, grade, and persist a paired experiment sequentially."""

    def __init__(
        self, repository: ExperimentRepository, executor: AttemptExecutor
    ) -> None:
        self.repository = repository
        self.executor = executor

    async def run(
        self,
        *,
        suite: ResolvedSuite,
        skill_snapshot: SkillSnapshot,
        models: Mapping[str, ResolvedModel],
        redacted_config: Mapping[str, object],
        harness_version: str,
    ) -> EvaluationSummary:
        """Run every requested condition/model/case/repetition under one profile."""
        profile = resolve_capability_profile(suite.suite.capability_profile)
        missing_models = set(suite.suite.executors) - set(models)
        if missing_models:
            names = ", ".join(sorted(missing_models))
            raise ValueError(
                f"suite references unconfigured executor model(s): {names}"
            )

        config_snapshot_id = self.repository.store_config_snapshot(redacted_config)
        experiment_id = self.repository.create_experiment(
            skill_name=skill_snapshot.skill.name,
            skill_sha256=skill_snapshot.sha256,
            eval_set_sha256=suite.sha256,
            capability_profile=profile.id,
            harness_version=harness_version,
            config_snapshot_id=config_snapshot_id,
            suite_yaml=suite.source_yaml,
            capability_profile_json=profile.model_dump_json(),
        )
        skill_snapshot_id = self.repository.store_skill_snapshot(
            experiment_id=experiment_id,
            manifest=skill_snapshot.manifest,
            skill_md=(skill_snapshot.skill.directory / "SKILL.md").read_text(
                encoding="utf-8"
            ),
        )
        _store_skill_resources(
            self.repository,
            skill_snapshot_id=skill_snapshot_id,
            skill_snapshot=skill_snapshot,
        )
        deterministic_grader_id = self.repository.store_model(
            provider="skill-eval",
            model_name="deterministic-grader",
            settings={"assertion_schema": 1},
        )
        model_ids = {
            alias: _store_executor_model(self.repository, model)
            for alias, model in models.items()
            if alias in suite.suite.executors
        }
        case_ids = {
            case.id: self.repository.add_eval_case(
                experiment_id=experiment_id,
                case_id=f"{experiment_id}:{case.id}",
                prompt=case.prompt,
                assertions=[
                    assertion.model_dump(mode="json") for assertion in case.assertions
                ],
                input_artifacts=[
                    {"path": str(path)} for path in suite.fixture_paths[case.id]
                ],
            )
            for case in suite.suite.cases
        }
        _store_fixture_snapshots(
            self.repository,
            experiment_id=experiment_id,
            case_ids=case_ids,
            suite=suite,
            max_bytes=profile.max_output_bytes,
        )
        condition_ids = {
            condition: self.repository.add_condition(
                experiment_id=experiment_id,
                condition_id=f"{experiment_id}:{condition}",
                name=condition,
                skill_context=_condition_context(condition, skill_snapshot),
            )
            for condition in suite.suite.conditions
        }

        request_data: dict[str, tuple[ResolvedModel, EvalCaseSpec, str]] = {}
        for case in suite.suite.cases:
            for condition in suite.suite.conditions:
                for alias in suite.suite.executors:
                    for repetition in range(suite.suite.repetitions):
                        attempt_id = self.repository.queue_attempt(
                            experiment_id=experiment_id,
                            eval_case_id=case_ids[case.id],
                            model_id=model_ids[alias],
                            condition_id=condition_ids[condition],
                            skill_snapshot_id=skill_snapshot_id,
                            repetition=repetition,
                        )
                        request_data[attempt_id] = (models[alias], case, condition)

        await self._drain_queued_attempts(
            experiment_id=experiment_id,
            request_data=request_data,
            suite=suite,
            skill_snapshot=skill_snapshot,
            profile=profile,
            grader_id=deterministic_grader_id,
        )

        attempts = self.repository.list_attempts(experiment_id)
        failed_attempts = sum(attempt["status"] != "succeeded" for attempt in attempts)
        return EvaluationSummary(
            experiment_id=experiment_id,
            queued_attempts=len(request_data),
            completed_attempts=len(attempts),
            failed_attempts=failed_attempts,
        )

    async def resume(
        self,
        *,
        experiment_id: str,
        models: Mapping[str, ResolvedModel],
        skill_snapshot_id: str | None = None,
    ) -> EvaluationSummary:
        """Re-run only interrupted work from immutable replay sources."""
        existing_attempts = self.repository.list_attempts(experiment_id)
        if not existing_attempts:
            raise ValueError(f"experiment has no attempts to resume: {experiment_id}")
        snapshot_ids = {
            str(attempt["skill_snapshot_id"]) for attempt in existing_attempts
        }
        if skill_snapshot_id is None:
            if len(snapshot_ids) != 1:
                raise ValueError(
                    "resume requires a selected skill snapshot for candidate experiments"
                )
            skill_snapshot_id = next(iter(snapshot_ids))
        if skill_snapshot_id not in snapshot_ids:
            raise ValueError("selected skill snapshot is not part of this experiment")
        self.repository.requeue_interrupted_attempts(
            experiment_id, skill_snapshot_id=skill_snapshot_id
        )
        with rehydrated_replay_sources(
            self.repository,
            experiment_id=experiment_id,
            skill_snapshot_id=skill_snapshot_id,
        ) as (suite, skill_snapshot):
            profile = resolve_capability_profile(suite.suite.capability_profile)
            model_ids = {
                _store_executor_model(self.repository, model): model
                for model in models.values()
            }
            grader_id = self.repository.store_model(
                provider="skill-eval",
                model_name="deterministic-grader",
                settings={"assertion_schema": 1},
            )
            cases = {case.id: case for case in suite.suite.cases}
            attempts = self.repository.list_attempts(experiment_id)
            request_data = {
                attempt["id"]: (
                    model_ids[str(attempt["model_id"])],
                    cases[
                        str(attempt["eval_case_id"]).removeprefix(f"{experiment_id}:")
                    ],
                    str(attempt["condition_id"]).removeprefix(f"{experiment_id}:"),
                )
                for attempt in attempts
                if attempt["status"] == "queued"
                and attempt["skill_snapshot_id"] == skill_snapshot_id
            }
            if len(request_data) != sum(a["status"] == "queued" for a in attempts):
                raise ValueError(
                    "active configuration cannot reproduce this experiment's model mapping"
                )
            await self._drain_queued_attempts(
                experiment_id=experiment_id,
                request_data=request_data,
                suite=suite,
                skill_snapshot=skill_snapshot,
                profile=profile,
                grader_id=grader_id,
            )
        attempts = self.repository.list_attempts(experiment_id)
        return EvaluationSummary(
            experiment_id=experiment_id,
            queued_attempts=len(request_data),
            completed_attempts=len(attempts),
            failed_attempts=sum(
                attempt["status"] != "succeeded" for attempt in attempts
            ),
        )

    async def _drain_queued_attempts(
        self,
        *,
        experiment_id: str,
        request_data: Mapping[str, tuple[ResolvedModel, EvalCaseSpec, str]],
        suite: ResolvedSuite,
        skill_snapshot: SkillSnapshot,
        profile: CapabilityProfile,
        grader_id: str,
    ) -> None:
        """Execute, grade, and persist each queued attempt in scheduler order."""
        while attempt := self.repository.claim_next_attempt(experiment_id):
            model, case, condition = request_data[attempt.id]
            with isolated_workspace(
                skill_snapshot=skill_snapshot, suite=suite, case=case
            ) as workspace:
                result = await self.executor.run(
                    ExecutionRequest(
                        model=model,
                        case=case,
                        condition=condition,
                        skill_snapshot=skill_snapshot,
                        workspace=workspace,
                        profile=profile,
                    )
                )
                result = _collect_result_artifacts(result, workspace, profile)
                self.repository.complete_attempt(
                    attempt_id=attempt.id,
                    status=result.status,
                    transcript=result.raw_messages_json or result.transcript,
                    error=result.error,
                    input_tokens=result.input_tokens,
                    output_tokens=result.output_tokens,
                    tool_calls=result.tool_calls,
                )
                persist_deterministic_grades(
                    self.repository,
                    attempt_id=attempt.id,
                    grader_id=grader_id,
                    results=grade_assertions(
                        workspace.output_directory, case.assertions
                    ),
                )
                for artifact in collect_artifacts(workspace, profile):
                    self.repository.add_artifact(
                        attempt_id=attempt.id,
                        path=artifact.path,
                        content=artifact.content,
                        media_type=artifact.media_type,
                        max_bytes=profile.max_output_bytes,
                    )

    async def evaluate_candidate(
        self, *, candidate_id: str, models: Mapping[str, ResolvedModel]
    ) -> EvaluationSummary:
        """Queue the candidate's full-skill condition on blinded holdout cases only."""
        candidate = self.repository.get_candidate(candidate_id)
        experiment_id = str(candidate["experiment_id"])
        snapshot_id = str(candidate["candidate_snapshot_id"])
        with rehydrated_replay_sources(
            self.repository, experiment_id=experiment_id, skill_snapshot_id=snapshot_id
        ) as (suite, _):
            if "with_full_skill" not in suite.suite.conditions:
                raise ValueError(
                    "candidate evaluation requires the with_full_skill condition"
                )
            model_ids = {
                alias: _store_executor_model(self.repository, model)
                for alias, model in models.items()
            }
            for case in suite.suite.cases:
                if case.partition != "holdout":
                    continue
                for alias in suite.suite.executors:
                    for repetition in range(suite.suite.repetitions):
                        self.repository.queue_attempt(
                            experiment_id=experiment_id,
                            eval_case_id=f"{experiment_id}:{case.id}",
                            model_id=model_ids[alias],
                            condition_id=f"{experiment_id}:with_full_skill",
                            skill_snapshot_id=snapshot_id,
                            candidate_id=candidate_id,
                            repetition=repetition,
                        )
        return await self.resume(
            experiment_id=experiment_id, models=models, skill_snapshot_id=snapshot_id
        )


def _store_executor_model(
    repository: ExperimentRepository, model: ResolvedModel
) -> str:
    return repository.store_model(
        provider=model.provider_kind,
        model_name=model.model_name,
        settings={
            "configured_alias": model.alias,
            "provider_alias": model.provider_alias,
        },
    )


def _store_skill_resources(
    repository: ExperimentRepository,
    *,
    skill_snapshot_id: str,
    skill_snapshot: SkillSnapshot,
) -> None:
    """Persist every bundled regular file so resume does not read a mutable skill tree."""
    for path in sorted(skill_snapshot.skill.directory.rglob("*")):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise HarnessError(f"skill contains unsupported symbolic link: {path}")
        repository.store_skill_resource(
            skill_snapshot_id=skill_snapshot_id,
            path=path.relative_to(skill_snapshot.skill.directory).as_posix(),
            content=path.read_bytes(),
        )


def _store_fixture_snapshots(
    repository: ExperimentRepository,
    *,
    experiment_id: str,
    case_ids: Mapping[str, str],
    suite: ResolvedSuite,
    max_bytes: int,
) -> None:
    """Store every declared fixture file before execution can observe mutable source paths."""
    for case_id, fixtures in suite.fixture_paths.items():
        for fixture in fixtures:
            files = [fixture] if fixture.is_file() else sorted(fixture.rglob("*"))
            for path in files:
                if not path.is_file():
                    continue
                if path.is_symlink():
                    raise HarnessError(
                        f"fixture contains unsupported symbolic link: {path}"
                    )
                content = path.read_bytes()
                if len(content) > max_bytes:
                    raise HarnessError(
                        f"fixture exceeds {max_bytes} byte replay limit: {path}"
                    )
                repository.store_input_artifact(
                    experiment_id=experiment_id,
                    eval_case_id=case_ids[case_id],
                    path=path.relative_to(suite.base_directory).as_posix(),
                    content=content,
                )


def _condition_context(
    condition: str, skill_snapshot: SkillSnapshot
) -> dict[str, object]:
    if condition == "without_skill":
        return {"condition": condition}
    if condition == "with_metadata_only":
        return {
            "condition": condition,
            "name": skill_snapshot.skill.name,
            "description": skill_snapshot.skill.description,
        }
    if condition == "with_full_skill":
        return {
            "condition": condition,
            "skill_sha256": skill_snapshot.sha256,
            "resources": skill_snapshot.manifest,
        }
    raise ValueError(f"unsupported evaluation condition: {condition}")


def _collect_result_artifacts(
    result: ExecutionResult,
    workspace: AttemptWorkspace,
    profile: CapabilityProfile,
) -> ExecutionResult:
    """Fail a run explicitly when its output cannot be collected safely."""
    try:
        collect_artifacts(workspace, profile)
    except HarnessError as error:
        return replace(
            result,
            status="failed",
            error={"type": type(error).__name__, "message": str(error)},
        )
    return result
