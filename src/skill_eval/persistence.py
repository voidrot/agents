"""Repository operations for durable, provider-neutral experiment state."""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


class PersistenceError(RuntimeError):
    """Raised when persisted experiment state is invalid or cannot be written."""


ATTEMPT_STATUSES = frozenset(
    {
        "queued",
        "running",
        "succeeded",
        "failed",
        "timeout",
        "rate_limited",
        "unsupported",
        "cancelled",
    }
)
_TERMINAL_ATTEMPT_STATUSES = ATTEMPT_STATUSES - {"queued", "running"}


@dataclass(frozen=True)
class AttemptRecord:
    """The scheduler-facing portion of a persisted attempt."""

    id: str
    experiment_id: str
    eval_case_id: str
    model_id: str
    condition_id: str
    skill_snapshot_id: str
    candidate_id: str | None
    repetition: int
    status: str
    started_at: str | None


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class ExperimentRepository:
    """SQLite repository with atomic queue claiming for future schedulers."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path.expanduser()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        try:
            connection = sqlite3.connect(self.database_path)
        except sqlite3.Error as error:
            raise PersistenceError(
                f"could not open experiment database: {error}"
            ) from error
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA busy_timeout = 30000")
            yield connection
        except sqlite3.Error as error:
            connection.rollback()
            raise PersistenceError(f"database operation failed: {error}") from error
        finally:
            connection.close()

    def store_config_snapshot(self, config: Mapping[str, Any]) -> str:
        """Deduplicate and persist a redacted config snapshot by content hash."""
        content = yaml.safe_dump(dict(config), sort_keys=True, allow_unicode=True)
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        snapshot_id = f"config_{digest}"
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO config_snapshot (id, sha256, redacted_yaml, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(sha256) DO NOTHING
                """,
                (snapshot_id, digest, content, _timestamp()),
            )
            connection.commit()
        return snapshot_id

    def store_model(
        self,
        *,
        provider: str,
        model_name: str,
        settings: Mapping[str, Any],
    ) -> str:
        """Deduplicate a resolved executor, grader, or enhancer model."""
        settings_json = _canonical_json(settings)
        fingerprint = _canonical_json(
            {"provider": provider, "model_name": model_name, "settings": dict(settings)}
        )
        model_id = f"model_{hashlib.sha256(fingerprint.encode('utf-8')).hexdigest()}"
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO model (id, provider, model_name, settings_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO NOTHING
                """,
                (model_id, provider, model_name, settings_json),
            )
            connection.commit()
        return model_id

    def create_experiment(
        self,
        *,
        skill_name: str,
        skill_sha256: str,
        eval_set_sha256: str,
        capability_profile: str,
        harness_version: str,
        config_snapshot_id: str | None,
        suite_yaml: str | None = None,
        capability_profile_json: str | None = None,
        experiment_id: str | None = None,
    ) -> str:
        """Create an immutable experiment envelope before scheduling attempts."""
        identifier = experiment_id or _new_id("experiment")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO experiment (
                    id, created_at, skill_name, skill_sha256, eval_set_sha256,
                    capability_profile, harness_version, config_snapshot_id,
                    suite_yaml, capability_profile_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    _timestamp(),
                    skill_name,
                    skill_sha256,
                    eval_set_sha256,
                    capability_profile,
                    harness_version,
                    config_snapshot_id,
                    suite_yaml,
                    capability_profile_json,
                ),
            )
            connection.commit()
        return identifier

    def store_input_artifact(
        self,
        *,
        experiment_id: str,
        eval_case_id: str,
        path: str,
        content: bytes,
        media_type: str | None = None,
        artifact_id: str | None = None,
    ) -> str:
        """Persist immutable fixture content so a resumed attempt never reads a changed file."""
        identifier = artifact_id or _new_id("input")
        digest = hashlib.sha256(content).hexdigest()
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO input_artifact (id, experiment_id, eval_case_id, path, media_type, sha256, content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    experiment_id,
                    eval_case_id,
                    path,
                    media_type,
                    digest,
                    content,
                ),
            )
            connection.commit()
        return identifier

    def add_eval_case(
        self,
        *,
        experiment_id: str,
        prompt: str,
        assertions: Sequence[Mapping[str, Any]],
        input_artifacts: Sequence[Mapping[str, Any]] = (),
        case_id: str | None = None,
    ) -> str:
        """Persist one immutable evaluation case using an ID, never prompt text."""
        identifier = case_id or _new_id("case")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO eval_case (id, experiment_id, prompt, assertions_json, input_artifacts_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    experiment_id,
                    prompt,
                    _canonical_json(assertions),
                    _canonical_json(input_artifacts),
                ),
            )
            connection.commit()
        return identifier

    def add_condition(
        self,
        *,
        experiment_id: str,
        name: str,
        skill_context: Mapping[str, Any],
        condition_id: str | None = None,
    ) -> str:
        """Persist one explicit baseline or skill condition."""
        identifier = condition_id or _new_id("condition")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO condition (id, experiment_id, name, skill_context_json)
                VALUES (?, ?, ?, ?)
                """,
                (identifier, experiment_id, name, _canonical_json(skill_context)),
            )
            connection.commit()
        return identifier

    def store_skill_snapshot(
        self,
        *,
        experiment_id: str,
        manifest: Mapping[str, Any],
        skill_md: str,
        parent_snapshot_id: str | None = None,
        snapshot_id: str | None = None,
    ) -> str:
        """Persist a complete skill revision for reproducibility and candidate diffs."""
        manifest_json = _canonical_json(manifest)
        digest = hashlib.sha256(f"{manifest_json}\0{skill_md}".encode()).hexdigest()
        identifier = snapshot_id or _new_id("skill")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO skill_snapshot (
                    id, experiment_id, parent_snapshot_id, sha256, manifest_json, skill_md, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    experiment_id,
                    parent_snapshot_id,
                    digest,
                    manifest_json,
                    skill_md,
                    _timestamp(),
                ),
            )
            connection.commit()
        return identifier

    def store_skill_resource(
        self,
        *,
        skill_snapshot_id: str,
        path: str,
        content: bytes,
        media_type: str | None = None,
        resource_id: str | None = None,
    ) -> str:
        """Persist one bundled skill file for replay and candidate auditability."""
        identifier = resource_id or _new_id("resource")
        digest = hashlib.sha256(content).hexdigest()
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO skill_resource (id, skill_snapshot_id, path, media_type, sha256, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (identifier, skill_snapshot_id, path, media_type, digest, content),
            )
            connection.commit()
        return identifier

    def queue_attempt(
        self,
        *,
        experiment_id: str,
        eval_case_id: str,
        model_id: str,
        condition_id: str,
        repetition: int,
        skill_snapshot_id: str,
        candidate_id: str | None = None,
        attempt_id: str | None = None,
    ) -> str:
        """Add a queued, uniquely paired attempt without claiming it."""
        if repetition < 0:
            raise PersistenceError("repetition must be non-negative")
        identifier = attempt_id or _new_id("attempt")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO attempt (
                    id, experiment_id, eval_case_id, model_id, condition_id,
                    skill_snapshot_id, candidate_id, repetition, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'queued')
                """,
                (
                    identifier,
                    experiment_id,
                    eval_case_id,
                    model_id,
                    condition_id,
                    skill_snapshot_id,
                    candidate_id,
                    repetition,
                ),
            )
            connection.commit()
        return identifier

    def claim_next_attempt(self, experiment_id: str) -> AttemptRecord | None:
        """Atomically claim the next queued attempt for a single scheduler worker."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT id, experiment_id, eval_case_id, model_id, condition_id,
                       skill_snapshot_id, candidate_id, repetition, status, started_at
                FROM attempt
                WHERE experiment_id = ? AND status = 'queued'
                ORDER BY eval_case_id, condition_id, model_id, repetition, id
                LIMIT 1
                """,
                (experiment_id,),
            ).fetchone()
            if row is None:
                connection.commit()
                return None
            started_at = _timestamp()
            updated = connection.execute(
                "UPDATE attempt SET status = 'running', started_at = ? WHERE id = ? AND status = 'queued'",
                (started_at, row["id"]),
            )
            if updated.rowcount != 1:
                connection.rollback()
                raise PersistenceError("attempt claim lost to another scheduler")
            connection.commit()
            return AttemptRecord(
                id=row["id"],
                experiment_id=row["experiment_id"],
                eval_case_id=row["eval_case_id"],
                model_id=row["model_id"],
                condition_id=row["condition_id"],
                skill_snapshot_id=row["skill_snapshot_id"],
                candidate_id=row["candidate_id"],
                repetition=row["repetition"],
                status="running",
                started_at=started_at,
            )

    def requeue_interrupted_attempts(
        self, experiment_id: str, *, skill_snapshot_id: str | None = None
    ) -> int:
        """Return abandoned running attempts to the queue without touching terminal results."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            updated = connection.execute(
                """
                UPDATE attempt
                SET status = 'queued', started_at = NULL
                WHERE experiment_id = ? AND status = 'running'
                  AND (? IS NULL OR skill_snapshot_id = ?)
                """,
                (experiment_id, skill_snapshot_id, skill_snapshot_id),
            )
            connection.commit()
        return updated.rowcount

    def complete_attempt(
        self,
        *,
        attempt_id: str,
        status: str,
        transcript: str | None = None,
        error: Mapping[str, Any] | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        cost_usd: float | None = None,
        duration_ms: int | None = None,
        tool_calls: int | None = None,
    ) -> None:
        """Finalize a claimed attempt, retaining result/error diagnostics separately."""
        if status not in _TERMINAL_ATTEMPT_STATUSES:
            raise PersistenceError(
                f"attempt completion requires a terminal status, got {status!r}"
            )
        with self._connection() as connection:
            updated = connection.execute(
                """
                UPDATE attempt
                SET status = ?, finished_at = ?, transcript = ?, error_json = ?,
                    input_tokens = ?, output_tokens = ?, cost_usd = ?, duration_ms = ?, tool_calls = ?
                WHERE id = ? AND status = 'running'
                """,
                (
                    status,
                    _timestamp(),
                    transcript,
                    _canonical_json(error) if error is not None else None,
                    input_tokens,
                    output_tokens,
                    cost_usd,
                    duration_ms,
                    tool_calls,
                    attempt_id,
                ),
            )
            if updated.rowcount != 1:
                connection.rollback()
                raise PersistenceError(
                    "attempt must be running before it can be completed"
                )
            connection.commit()

    def add_grade(
        self,
        *,
        attempt_id: str,
        grader_id: str,
        assertion_id: str,
        passed: bool,
        evidence: str,
        score: float | None = None,
        grade_id: str | None = None,
    ) -> str:
        """Persist a deterministic or judge grade without conflating their models."""
        identifier = grade_id or _new_id("grade")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO grade (id, attempt_id, grader_id, assertion_id, passed, score, evidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    attempt_id,
                    grader_id,
                    assertion_id,
                    1 if passed else 0,
                    score,
                    evidence,
                ),
            )
            connection.commit()
        return identifier

    def add_artifact(
        self,
        *,
        attempt_id: str,
        path: str,
        content: bytes,
        media_type: str | None = None,
        artifact_id: str | None = None,
        max_bytes: int = 1_000_000,
    ) -> str:
        """Persist a bounded output artifact with its content hash."""
        if len(content) > max_bytes:
            raise PersistenceError(
                f"artifact exceeds maximum size of {max_bytes} bytes"
            )
        identifier = artifact_id or _new_id("artifact")
        digest = hashlib.sha256(content).hexdigest()
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO artifact (id, attempt_id, path, media_type, sha256, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (identifier, attempt_id, path, media_type, digest, content),
            )
            connection.commit()
        return identifier

    def create_candidate(
        self,
        *,
        experiment_id: str,
        source_snapshot_id: str,
        candidate_snapshot_id: str,
        enhancer_model_id: str,
        mode: str,
        status: str = "proposed",
        rationale: str | None = None,
        selection: Mapping[str, Any] | None = None,
        candidate_id: str | None = None,
    ) -> str:
        """Persist a reviewable enhancement candidate without applying it."""
        if mode not in {"full-skill", "metadata-only"}:
            raise PersistenceError(f"unsupported candidate mode: {mode!r}")
        identifier = candidate_id or _new_id("candidate")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO candidate (
                    id, experiment_id, source_snapshot_id, candidate_snapshot_id,
                    enhancer_model_id, mode, status, rationale, selection_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identifier,
                    experiment_id,
                    source_snapshot_id,
                    candidate_snapshot_id,
                    enhancer_model_id,
                    mode,
                    status,
                    rationale,
                    _canonical_json(selection) if selection is not None else None,
                    _timestamp(),
                ),
            )
            connection.commit()
        return identifier

    def get_skill_snapshot(self, snapshot_id: str) -> dict[str, Any]:
        """Return one immutable skill snapshot."""
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM skill_snapshot WHERE id = ?", (snapshot_id,)
            ).fetchone()
        if row is None:
            raise PersistenceError(f"skill snapshot does not exist: {snapshot_id}")
        return dict(row)

    def get_candidate(self, candidate_id: str) -> dict[str, Any]:
        """Return a persisted candidate for evaluation or explicit application."""
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM candidate WHERE id = ?", (candidate_id,)
            ).fetchone()
        if row is None:
            raise PersistenceError(f"candidate does not exist: {candidate_id}")
        return dict(row)

    def experiment_source_snapshot(self, experiment_id: str) -> dict[str, Any]:
        """Return the sole original skill snapshot used by an experiment."""
        with self._connection() as connection:
            rows = connection.execute(
                """SELECT DISTINCT skill_snapshot.id, skill_snapshot.manifest_json, skill_snapshot.skill_md
                FROM attempt JOIN skill_snapshot ON skill_snapshot.id = attempt.skill_snapshot_id
                WHERE attempt.experiment_id = ?""",
                (experiment_id,),
            ).fetchall()
        if len(rows) != 1:
            raise PersistenceError(
                "enhancement requires exactly one source skill snapshot"
            )
        return dict(rows[0])

    def failure_summary(self, experiment_id: str) -> str:
        """Return bounded deterministic-grade evidence for an enhancement prompt."""
        with self._connection() as connection:
            rows = connection.execute(
                """SELECT grade.assertion_id, grade.evidence FROM grade
                JOIN attempt ON attempt.id = grade.attempt_id
                WHERE attempt.experiment_id = ? AND grade.passed = 0
                ORDER BY attempt.id, grade.assertion_id LIMIT 50""",
                (experiment_id,),
            ).fetchall()
        return "\n".join(f"- {row['assertion_id']}: {row['evidence']}" for row in rows)

    def experiment_executor_aliases(self, experiment_id: str) -> set[str]:
        """Return configured aliases used by persisted attempts."""
        with self._connection() as connection:
            rows = connection.execute(
                """SELECT DISTINCT model.settings_json FROM attempt
                JOIN model ON model.id = attempt.model_id WHERE attempt.experiment_id = ?""",
                (experiment_id,),
            ).fetchall()
        try:
            return {
                str(json.loads(row["settings_json"])["configured_alias"])
                for row in rows
            }
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            raise PersistenceError(
                "experiment has no resumable configured-model aliases"
            ) from error

    def list_input_artifacts(self, experiment_id: str) -> list[dict[str, Any]]:
        """Return immutable fixture blobs for materializing a replay suite."""
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT eval_case_id, path, content FROM input_artifact WHERE experiment_id = ? ORDER BY path",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_skill_resources(self, skill_snapshot_id: str) -> list[dict[str, Any]]:
        """Return immutable skill blobs for one snapshot."""
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT path, content FROM skill_resource WHERE skill_snapshot_id = ? ORDER BY path",
                (skill_snapshot_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_experiment(self, experiment_id: str) -> dict[str, Any]:
        """Return one experiment envelope or fail before attempting a resume."""
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM experiment WHERE id = ?", (experiment_id,)
            ).fetchone()
        if row is None:
            raise PersistenceError(f"experiment does not exist: {experiment_id}")
        return dict(row)

    def list_report_rows(self, experiment_id: str) -> list[dict[str, Any]]:
        """Return attempt outcomes joined to stable condition/model labels and grades."""
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT attempt.id, attempt.eval_case_id, attempt.repetition, attempt.status,
                       condition.name AS condition_name, model.id AS model_id, model.settings_json,
                       AVG(grade.passed) AS grade_pass_rate, COUNT(grade.id) AS grade_count
                FROM attempt
                JOIN condition ON condition.id = attempt.condition_id
                JOIN model ON model.id = attempt.model_id
                LEFT JOIN grade ON grade.attempt_id = attempt.id
                WHERE attempt.experiment_id = ?
                GROUP BY attempt.id
                ORDER BY attempt.eval_case_id, condition.name, attempt.model_id, attempt.repetition
                """,
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_attempts(self, experiment_id: str) -> list[dict[str, Any]]:
        """Return normalized attempt rows for a future report renderer."""
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT id, eval_case_id, model_id, condition_id, skill_snapshot_id,
                       candidate_id, repetition, status, started_at, finished_at,
                       input_tokens, output_tokens, cost_usd, duration_ms, tool_calls, error_json, transcript
                FROM attempt
                WHERE experiment_id = ?
                ORDER BY eval_case_id, condition_id, model_id, repetition, id
                """,
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]
