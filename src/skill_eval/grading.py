"""Safe deterministic assertion grading for isolated attempt outputs."""

# pyright: reportMissingImports=false
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .persistence import ExperimentRepository
from .suites import AssertionSpec


@dataclass(frozen=True)
class GradeResult:
    """A provider-neutral deterministic assertion outcome."""

    assertion_id: str
    passed: bool
    evidence: str
    score: float | None = None


def grade_assertions(
    output_directory: Path,
    assertions: Iterable[AssertionSpec],
    *,
    max_read_bytes: int = 1_000_000,
) -> list[GradeResult]:
    """Grade supported assertions without following output paths outside the sandbox."""
    root = output_directory.resolve()
    if not root.is_dir():
        return [
            GradeResult(
                assertion_id=assertion.id,
                passed=False,
                evidence=f"attempt output directory is unavailable: {root}",
            )
            for assertion in assertions
        ]
    return [
        _grade_assertion(root, assertion, max_read_bytes) for assertion in assertions
    ]


def persist_deterministic_grades(
    repository: ExperimentRepository,
    *,
    attempt_id: str,
    grader_id: str,
    results: Iterable[GradeResult],
) -> list[str]:
    """Persist each deterministic result after its attempt reaches a terminal state."""
    return [
        repository.add_grade(
            attempt_id=attempt_id,
            grader_id=grader_id,
            assertion_id=result.assertion_id,
            passed=result.passed,
            score=result.score,
            evidence=result.evidence,
        )
        for result in results
    ]


def _grade_assertion(
    root: Path, assertion: AssertionSpec, max_read_bytes: int
) -> GradeResult:
    target = (root / assertion.path).resolve()
    if not target.is_relative_to(root):
        return GradeResult(
            assertion_id=assertion.id,
            passed=False,
            evidence=f"assertion path escapes output directory: {assertion.path}",
        )
    if not target.is_file():
        return GradeResult(
            assertion_id=assertion.id,
            passed=False,
            evidence=f"expected output file does not exist: {assertion.path}",
        )
    if assertion.type == "file_exists":
        return GradeResult(
            assertion_id=assertion.id,
            passed=True,
            evidence=f"output file exists: {assertion.path}",
            score=1.0,
        )

    if target.stat().st_size > max_read_bytes:
        return GradeResult(
            assertion_id=assertion.id,
            passed=False,
            evidence=f"output file exceeds deterministic read limit: {assertion.path}",
        )
    try:
        content = target.read_text(encoding="utf-8")
    except OSError as error:
        return GradeResult(
            assertion_id=assertion.id,
            passed=False,
            evidence=f"could not read output file {assertion.path}: {error}",
        )

    expected = assertion.text or ""
    passed = expected in content
    evidence = (
        f"output file contains expected text: {assertion.path}"
        if passed
        else f"output file does not contain expected text: {assertion.path}"
    )
    return GradeResult(
        assertion_id=assertion.id,
        passed=passed,
        evidence=evidence,
        score=1.0 if passed else 0.0,
    )
